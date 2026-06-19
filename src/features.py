import numpy as np
from .config import DCT_BLOCK_SIZE, QUANTIZATION_MATRIX_8X8
from .pdi_manual import (
    rgb_to_gray_manual,
    resize_bilinear_manual,
    gaussian_filter_3x3_manual,
    sobel_manual,
    histogram_manual,
    entropy_manual,
    otsu_threshold_manual,
    threshold_manual,
    opening_manual,
    closing_manual,
    connected_components_manual,
    block_process_dct_quantization_manual,
    mse_manual,
    psnr_manual,
)


def _moments_manual(values: np.ndarray):
    vals = values.astype(np.float64).ravel()
    n = len(vals)
    if n == 0:
        return 0.0, 0.0, 0.0, 0.0
    mean = float(np.sum(vals) / n)
    centered = vals - mean
    var = float(np.sum(centered ** 2) / n)
    std = float(np.sqrt(var))
    if std == 0:
        return mean, std, 0.0, 0.0
    skew = float(np.sum((centered / std) ** 3) / n)
    kurt = float(np.sum((centered / std) ** 4) / n)
    return mean, std, skew, kurt


def _hist_features_channel(channel: np.ndarray, bins: int = 16, prefix: str = "hist"):
    hist = histogram_manual(channel, bins=bins)
    total = hist.sum()
    if total > 0:
        hist = hist / total
    names = [f"{prefix}_{i:02d}" for i in range(bins)]
    return names, hist.astype(float).tolist()


def _frequency_band_features(coeffs: np.ndarray, block_size: int = 8):
    """
    Mede energia por faixas simples dentro de cada bloco DCT 8x8.
    Baixa: u+v <= 2; média: 3 <= u+v <= 6; alta: u+v > 6.
    """
    h, w = coeffs.shape
    low = 0.0
    mid = 0.0
    high = 0.0
    total = 0.0
    for i in range(0, h, block_size):
        for j in range(0, w, block_size):
            block = coeffs[i:i+block_size, j:j+block_size]
            for u in range(block.shape[0]):
                for v in range(block.shape[1]):
                    e = float(block[u, v] ** 2)
                    total += e
                    if u + v <= 2:
                        low += e
                    elif u + v <= 6:
                        mid += e
                    else:
                        high += e
    if total == 0:
        return 0.0, 0.0, 0.0
    return low / total, mid / total, high / total


def extract_features_and_artifacts(img_rgb: np.ndarray, image_size: int = 128):
    """
    Executa todo o pipeline para uma imagem.

    Retorna:
    - features: dict numérico para ML;
    - artifacts: imagens intermediárias para análise visual;
    - compression: métricas de compressão/DCT.
    """
    resized = resize_bilinear_manual(img_rgb, image_size, image_size)
    resized = np.clip(resized, 0, 255).astype(np.uint8)

    gray = rgb_to_gray_manual(resized)
    filtered = gaussian_filter_3x3_manual(gray)
    gx, gy, grad = sobel_manual(filtered)

    otsu_t = otsu_threshold_manual(filtered)
    mask = threshold_manual(filtered, otsu_t)
    opened = opening_manual(mask, 3)
    morph = closing_manual(opened, 3)

    q_matrix = np.array(QUANTIZATION_MATRIX_8X8, dtype=np.float64)
    coeffs, qcoeffs, recon = block_process_dct_quantization_manual(
        filtered, q_matrix=q_matrix, block_size=DCT_BLOCK_SIZE
    )

    features = {}

    # Estatísticas de cor e histogramas por canal.
    for c, name in enumerate(["R", "G", "B"]):
        channel = resized[:, :, c].astype(np.float64)
        mean, std, skew, kurt = _moments_manual(channel)
        features[f"mean_{name}"] = mean
        features[f"std_{name}"] = std
        features[f"skew_{name}"] = skew
        features[f"kurt_{name}"] = kurt
        names, vals = _hist_features_channel(channel, bins=16, prefix=f"hist_{name}")
        for n, v in zip(names, vals):
            features[n] = v

    # Estatísticas de cinza.
    mean_g, std_g, skew_g, kurt_g = _moments_manual(gray)
    features["mean_gray"] = mean_g
    features["std_gray"] = std_g
    features["skew_gray"] = skew_g
    features["kurt_gray"] = kurt_g
    features["entropy_gray"] = entropy_manual(gray, bins=256)

    names, vals = _hist_features_channel(gray, bins=16, prefix="hist_gray")
    for n, v in zip(names, vals):
        features[n] = v

    # Bordas.
    edge_binary = threshold_manual(grad, int(max(20, otsu_threshold_manual(grad))))
    features["edge_density"] = float(edge_binary.sum() / edge_binary.size)
    features["grad_mean"] = float(np.mean(grad))
    features["grad_std"] = float(np.std(grad))
    features["grad_entropy"] = entropy_manual(grad, bins=256)

    # Segmentação e morfologia.
    fg_ratio = float(morph.sum() / morph.size)
    bg_ratio = 1.0 - fg_ratio
    n_comp, areas = connected_components_manual(morph)
    largest = max(areas) if areas else 0
    features["otsu_threshold"] = float(otsu_t)
    features["foreground_ratio"] = fg_ratio
    features["background_ratio"] = bg_ratio
    features["components_count"] = float(n_comp)
    features["largest_component_ratio"] = float(largest / morph.size)

    # Frequência/compressão.
    low_e, mid_e, high_e = _frequency_band_features(coeffs, DCT_BLOCK_SIZE)
    zeros_ratio = float(np.sum(qcoeffs == 0) / qcoeffs.size)
    features["dct_energy_low"] = low_e
    features["dct_energy_mid"] = mid_e
    features["dct_energy_high"] = high_e
    features["dct_zero_ratio"] = zeros_ratio
    features["dct_entropy_quantized"] = entropy_manual(qcoeffs, bins=256)
    features["reconstruction_mse"] = mse_manual(filtered[:recon.shape[0], :recon.shape[1]], recon)
    features["reconstruction_psnr"] = psnr_manual(filtered[:recon.shape[0], :recon.shape[1]], recon)

    artifacts = {
        "resized_rgb": resized,
        "gray": gray,
        "filtered": filtered,
        "gradient": grad,
        "mask": mask * 255,
        "morphology": morph * 255,
        "dct_log": np.log1p(np.abs(coeffs)),
        "reconstruction": recon,
    }

    compression = {
        "entropy_gray": features["entropy_gray"],
        "dct_zero_ratio": zeros_ratio,
        "mse": features["reconstruction_mse"],
        "psnr": features["reconstruction_psnr"],
        "dct_energy_low": low_e,
        "dct_energy_mid": mid_e,
        "dct_energy_high": high_e,
    }

    return features, artifacts, compression
