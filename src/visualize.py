from pathlib import Path
import matplotlib.pyplot as plt
import numpy as np


def _norm_for_show(img):
    arr = np.asarray(img, dtype=float)
    if arr.ndim == 2:
        mn, mx = arr.min(), arr.max()
        if mx > mn:
            arr = (arr - mn) / (mx - mn)
        return arr
    return np.clip(arr / 255.0, 0, 1)


def save_pipeline_figure(artifacts: dict, output_path: Path, title: str = "Pipeline visual"):
    output_path = Path(output_path)
    output_path.parent.mkdir(parents=True, exist_ok=True)

    items = [
        ("Original", artifacts["resized_rgb"], None),
        ("Cinza", artifacts["gray"], "gray"),
        ("Filtro espacial", artifacts["filtered"], "gray"),
        ("Sobel", artifacts["gradient"], "gray"),
        ("Otsu", artifacts["mask"], "gray"),
        ("Morfologia", artifacts["morphology"], "gray"),
        ("DCT log", artifacts["dct_log"], "gray"),
        ("Reconstruída", artifacts["reconstruction"], "gray"),
    ]

    fig, axes = plt.subplots(2, 4, figsize=(14, 7))
    fig.suptitle(title)
    for ax, (name, img, cmap) in zip(axes.ravel(), items):
        if cmap == "gray":
            ax.imshow(_norm_for_show(img), cmap="gray")
        else:
            ax.imshow(_norm_for_show(img))
        ax.set_title(name)
        ax.axis("off")
    plt.tight_layout()
    fig.savefig(output_path, dpi=200, bbox_inches="tight")
    plt.close(fig)


def save_confusion_matrix(cm, labels, output_path: Path, title: str = "Matriz de confusão"):
    output_path = Path(output_path)
    output_path.parent.mkdir(parents=True, exist_ok=True)
    fig, ax = plt.subplots(figsize=(8, 6))
    im = ax.imshow(cm)
    ax.set_title(title)
    ax.set_xlabel("Predito")
    ax.set_ylabel("Real")
    ax.set_xticks(range(len(labels)))
    ax.set_yticks(range(len(labels)))
    ax.set_xticklabels(labels, rotation=45, ha="right")
    ax.set_yticklabels(labels)
    for i in range(cm.shape[0]):
        for j in range(cm.shape[1]):
            ax.text(j, i, str(cm[i, j]), ha="center", va="center")
    fig.colorbar(im, ax=ax)
    plt.tight_layout()
    fig.savefig(output_path, dpi=200, bbox_inches="tight")
    plt.close(fig)


def save_barplot(df, x_col, y_col, output_path: Path, title: str, ylabel: str):
    output_path = Path(output_path)
    output_path.parent.mkdir(parents=True, exist_ok=True)
    fig, ax = plt.subplots(figsize=(8, 5))
    ax.bar(df[x_col].astype(str), df[y_col])
    ax.set_title(title)
    ax.set_ylabel(ylabel)
    ax.set_xlabel(x_col)
    plt.xticks(rotation=45, ha="right")
    plt.tight_layout()
    fig.savefig(output_path, dpi=200, bbox_inches="tight")
    plt.close(fig)
