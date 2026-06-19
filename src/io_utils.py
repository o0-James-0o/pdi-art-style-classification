from pathlib import Path
import cv2
import numpy as np

IMAGE_EXTENSIONS = {".jpg", ".jpeg", ".png", ".bmp", ".webp"}


def list_images(root: Path):
    """Lista imagens em subpastas de classe."""
    root = Path(root)
    paths = []
    for p in sorted(root.rglob("*")):
        if p.suffix.lower() in IMAGE_EXTENSIONS:
            paths.append(p)
    return paths


def read_image_rgb(path: Path) -> np.ndarray:
    """
    Lê imagem com OpenCV apenas para entrada, conforme regra do trabalho.
    Retorna RGB uint8.
    """
    img_bgr = cv2.imread(str(path), cv2.IMREAD_COLOR)
    if img_bgr is None:
        raise ValueError(f"Não foi possível ler a imagem: {path}")
    # Conversão BGR->RGB por indexação manual, sem cv2.cvtColor.
    return img_bgr[:, :, ::-1].copy()


def save_image_rgb(path: Path, img_rgb: np.ndarray):
    """Salva imagem usando OpenCV apenas para saída."""
    path = Path(path)
    path.parent.mkdir(parents=True, exist_ok=True)
    img = np.clip(img_rgb, 0, 255).astype(np.uint8)
    img_bgr = img[:, :, ::-1]
    ok = cv2.imwrite(str(path), img_bgr)
    if not ok:
        raise ValueError(f"Não foi possível salvar a imagem: {path}")


def save_gray(path: Path, img_gray: np.ndarray):
    path = Path(path)
    path.parent.mkdir(parents=True, exist_ok=True)
    img = np.clip(img_gray, 0, 255).astype(np.uint8)
    ok = cv2.imwrite(str(path), img)
    if not ok:
        raise ValueError(f"Não foi possível salvar a imagem: {path}")
