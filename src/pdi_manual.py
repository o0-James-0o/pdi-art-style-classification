
from collections import deque
import math
import numpy as np


def rgb_to_gray_manual(img_rgb: np.ndarray) -> np.ndarray:
    """Converte RGB para cinza usando luminância ponderada."""
    img = img_rgb.astype(np.float64)
    gray = 0.299 * img[:, :, 0] + 0.587 * img[:, :, 1] + 0.114 * img[:, :, 2]
    return np.clip(gray, 0, 255)


def resize_bilinear_manual(img: np.ndarray, new_h: int, new_w: int) -> np.ndarray:
    """Redimensionamento bilinear manual para imagens 2D ou 3D."""
    if img.ndim == 2:
        h, w = img.shape
        channels = None
    else:
        h, w, channels = img.shape

    if h == new_h and w == new_w:
        return img.copy()

    if img.ndim == 2:
        out = np.zeros((new_h, new_w), dtype=np.float64)
    else:
        out = np.zeros((new_h, new_w, channels), dtype=np.float64)

    y_scale = (h - 1) / max(new_h - 1, 1)
    x_scale = (w - 1) / max(new_w - 1, 1)

    for i in range(new_h):
        y = i * y_scale
        y0 = int(math.floor(y))
        y1 = min(y0 + 1, h - 1)
        wy = y - y0
        for j in range(new_w):
            x = j * x_scale
            x0 = int(math.floor(x))
            x1 = min(x0 + 1, w - 1)
            wx = x - x0
            top = (1 - wx) * img[y0, x0] + wx * img[y0, x1]
            bottom = (1 - wx) * img[y1, x0] + wx * img[y1, x1]
            out[i, j] = (1 - wy) * top + wy * bottom

    return np.clip(out, 0, 255)


def pad_edge_manual(img: np.ndarray, pad_h: int, pad_w: int) -> np.ndarray:
    """Padding por replicação de borda, implementado sem np.pad."""
    h, w = img.shape
    out = np.zeros((h + 2 * pad_h, w + 2 * pad_w), dtype=np.float64)
    out[pad_h:pad_h+h, pad_w:pad_w+w] = img

    # Topo e base
    for i in range(pad_h):
        out[i, pad_w:pad_w+w] = img[0, :]
        out[pad_h+h+i, pad_w:pad_w+w] = img[-1, :]

    # Laterais, incluindo cantos
    for j in range(pad_w):
        out[:, j] = out[:, pad_w]
        out[:, pad_w+w+j] = out[:, pad_w+w-1]

    return out


def convolve2d_manual(img_gray: np.ndarray, kernel: np.ndarray) -> np.ndarray:
    """Convolução 2D manual para imagem em escala de cinza."""
    img = img_gray.astype(np.float64)
    kernel = np.array(kernel, dtype=np.float64)
    kh, kw = kernel.shape
    pad_h, pad_w = kh // 2, kw // 2
    padded = pad_edge_manual(img, pad_h, pad_w)
    h, w = img.shape
    out = np.zeros((h, w), dtype=np.float64)

    # Convolução: inverte a máscara.
    k = kernel[::-1, ::-1]
    for i in range(h):
        for j in range(w):
            region = padded[i:i+kh, j:j+kw]
            out[i, j] = np.sum(region * k)
    return out


def mean_filter_3x3_manual(img_gray: np.ndarray) -> np.ndarray:
    kernel = np.ones((3, 3), dtype=np.float64) / 9.0
    return np.clip(convolve2d_manual(img_gray, kernel), 0, 255)


def gaussian_filter_3x3_manual(img_gray: np.ndarray) -> np.ndarray:
    kernel = np.array([[1, 2, 1], [2, 4, 2], [1, 2, 1]], dtype=np.float64) / 16.0
    return np.clip(convolve2d_manual(img_gray, kernel), 0, 255)


def sobel_manual(img_gray: np.ndarray):
    """Sobel manual. Retorna Gx, Gy e magnitude normalizada 0-255."""
    gx_kernel = np.array([[-1, 0, 1], [-2, 0, 2], [-1, 0, 1]], dtype=np.float64)
    gy_kernel = np.array([[-1, -2, -1], [0, 0, 0], [1, 2, 1]], dtype=np.float64)
    gx = convolve2d_manual(img_gray, gx_kernel)
    gy = convolve2d_manual(img_gray, gy_kernel)
    mag = np.sqrt(gx ** 2 + gy ** 2)
    if mag.max() > 0:
        mag_norm = 255.0 * mag / mag.max()
    else:
        mag_norm = mag
    return gx, gy, mag_norm


def histogram_manual(img_gray: np.ndarray, bins: int = 256, value_range=(0, 255)) -> np.ndarray:
    """Histograma manual para imagem 2D."""
    img = np.clip(img_gray, value_range[0], value_range[1])
    hist = np.zeros(bins, dtype=np.float64)
    min_v, max_v = value_range
    scale = bins / (max_v - min_v + 1e-12)
    flat = img.ravel()
    for v in flat:
        idx = int((v - min_v) * scale)
        if idx >= bins:
            idx = bins - 1
        if idx < 0:
            idx = 0
        hist[idx] += 1
    return hist


def entropy_manual(img_gray: np.ndarray, bins: int = 256) -> float:
    hist = histogram_manual(img_gray, bins=bins)
    total = hist.sum()
    if total == 0:
        return 0.0
    probs = hist / total
    ent = 0.0
    for p in probs:
        if p > 0:
            ent -= p * math.log2(p)
    return float(ent)


def otsu_threshold_manual(img_gray: np.ndarray) -> int:
    """Otsu manual: escolhe o limiar que maximiza variância entre classes."""
    hist = histogram_manual(img_gray, bins=256)
    total = hist.sum()
    if total == 0:
        return 0

    sum_total = 0.0
    for t in range(256):
        sum_total += t * hist[t]

    weight_bg = 0.0
    sum_bg = 0.0
    max_between = -1.0
    threshold = 0

    for t in range(256):
        weight_bg += hist[t]
        if weight_bg == 0:
            continue
        weight_fg = total - weight_bg
        if weight_fg == 0:
            break
        sum_bg += t * hist[t]
        mean_bg = sum_bg / weight_bg
        mean_fg = (sum_total - sum_bg) / weight_fg
        between = weight_bg * weight_fg * (mean_bg - mean_fg) ** 2
        if between > max_between:
            max_between = between
            threshold = t
    return int(threshold)


def threshold_manual(img_gray: np.ndarray, threshold: int) -> np.ndarray:
    """Binarização manual: pixels acima do limiar viram 1."""
    h, w = img_gray.shape
    out = np.zeros((h, w), dtype=np.uint8)
    for i in range(h):
        for j in range(w):
            out[i, j] = 1 if img_gray[i, j] > threshold else 0
    return out


def erode_manual(binary: np.ndarray, kernel_size: int = 3) -> np.ndarray:
    """Erosão binária manual com elemento estruturante quadrado."""
    b = (binary > 0).astype(np.uint8)
    h, w = b.shape
    r = kernel_size // 2
    out = np.zeros_like(b)
    for i in range(h):
        for j in range(w):
            ok = 1
            for di in range(-r, r + 1):
                for dj in range(-r, r + 1):
                    y, x = i + di, j + dj
                    if y < 0 or y >= h or x < 0 or x >= w or b[y, x] == 0:
                        ok = 0
                        break
                if ok == 0:
                    break
            out[i, j] = ok
    return out


def dilate_manual(binary: np.ndarray, kernel_size: int = 3) -> np.ndarray:
    """Dilatação binária manual com elemento estruturante quadrado."""
    b = (binary > 0).astype(np.uint8)
    h, w = b.shape
    r = kernel_size // 2
    out = np.zeros_like(b)
    for i in range(h):
        for j in range(w):
            val = 0
            for di in range(-r, r + 1):
                for dj in range(-r, r + 1):
                    y, x = i + di, j + dj
                    if 0 <= y < h and 0 <= x < w and b[y, x] == 1:
                        val = 1
                        break
                if val == 1:
                    break
            out[i, j] = val
    return out


def opening_manual(binary: np.ndarray, kernel_size: int = 3) -> np.ndarray:
    return dilate_manual(erode_manual(binary, kernel_size), kernel_size)


def closing_manual(binary: np.ndarray, kernel_size: int = 3) -> np.ndarray:
    return erode_manual(dilate_manual(binary, kernel_size), kernel_size)


def connected_components_manual(binary: np.ndarray):
    """Conta componentes conectados 8-vizinhos e retorna áreas."""
    b = (binary > 0).astype(np.uint8)
    h, w = b.shape
    visited = np.zeros_like(b, dtype=np.uint8)
    areas = []
    dirs = [(-1,-1), (-1,0), (-1,1), (0,-1), (0,1), (1,-1), (1,0), (1,1)]

    for i in range(h):
        for j in range(w):
            if b[i, j] == 1 and visited[i, j] == 0:
                q = deque([(i, j)])
                visited[i, j] = 1
                area = 0
                while q:
                    y, x = q.popleft()
                    area += 1
                    for dy, dx in dirs:
                        ny, nx = y + dy, x + dx
                        if 0 <= ny < h and 0 <= nx < w:
                            if b[ny, nx] == 1 and visited[ny, nx] == 0:
                                visited[ny, nx] = 1
                                q.append((ny, nx))
                areas.append(area)
    return len(areas), areas


def dct_matrix_manual(n: int = 8) -> np.ndarray:
    """Matriz ortonormal da DCT-II."""
    C = np.zeros((n, n), dtype=np.float64)
    for u in range(n):
        alpha = math.sqrt(1.0 / n) if u == 0 else math.sqrt(2.0 / n)
        for x in range(n):
            C[u, x] = alpha * math.cos(((2 * x + 1) * u * math.pi) / (2 * n))
    return C


def dct2_block_manual(block: np.ndarray, C: np.ndarray) -> np.ndarray:
    """DCT 2D manual por multiplicação matricial C f C^T."""
    return C @ block @ C.T


def idct2_block_manual(coeff: np.ndarray, C: np.ndarray) -> np.ndarray:
    """IDCT 2D manual."""
    return C.T @ coeff @ C


def block_process_dct_quantization_manual(img_gray: np.ndarray, q_matrix: np.ndarray, block_size: int = 8):
    """
    Aplica DCT 8x8, quantização, desquantização e reconstrução.
    Retorna coeficientes, coeficientes quantizados e imagem reconstruída.
    """
    img = img_gray.astype(np.float64)
    h, w = img.shape
    h2 = h - (h % block_size)
    w2 = w - (w % block_size)
    img = img[:h2, :w2]

    C = dct_matrix_manual(block_size)
    coeffs = np.zeros_like(img)
    qcoeffs = np.zeros_like(img)
    recon = np.zeros_like(img)
    q = np.array(q_matrix, dtype=np.float64)

    for i in range(0, h2, block_size):
        for j in range(0, w2, block_size):
            block = img[i:i+block_size, j:j+block_size] - 128.0
            dct_block = dct2_block_manual(block, C)
            q_block = np.round(dct_block / q)
            deq = q_block * q
            rec_block = idct2_block_manual(deq, C) + 128.0
            coeffs[i:i+block_size, j:j+block_size] = dct_block
            qcoeffs[i:i+block_size, j:j+block_size] = q_block
            recon[i:i+block_size, j:j+block_size] = rec_block

    return coeffs, qcoeffs, np.clip(recon, 0, 255)


def mse_manual(a: np.ndarray, b: np.ndarray) -> float:
    diff = a.astype(np.float64) - b.astype(np.float64)
    return float(np.mean(diff ** 2))


def psnr_manual(a: np.ndarray, b: np.ndarray) -> float:
    mse = mse_manual(a, b)
    if mse == 0:
        return float("inf")
    return float(20 * math.log10(255.0 / math.sqrt(mse)))
