"""
Baixa e organiza uma amostra balanceada do WikiArt via Hugging Face.

Uso:
    pip install datasets
    python download_wikiart_huggingface.py

Saída:
    data/raw/<classe>/*.jpg

"""
from pathlib import Path
from collections import defaultdict
import re

from src.config import DATA_RAW, TARGET_CLASSES, MAX_IMAGES_PER_CLASS


def safe_name(name: str) -> str:
    name = name.replace(" ", "_")
    return re.sub(r"[^A-Za-z0-9_\-]", "", name)


def main():
    try:
        from datasets import load_dataset
    except ImportError as exc:
        raise ImportError("Instale primeiro: pip install datasets") from exc

    print("Carregando dataset huggan/wikiart...")
    ds = load_dataset("huggan/wikiart", split="train", streaming=True)

    # Para datasets com ClassLabel, recupera nomes das classes.
    info_ds = load_dataset("huggan/wikiart", split="train[:1]")
    style_feature = info_ds.features["style"]
    style_names = getattr(style_feature, "names", None)
    if style_names is None:
        raise RuntimeError("Não foi possível obter nomes das classes de estilo.")

    target_set = set(TARGET_CLASSES)
    counts = defaultdict(int)
    DATA_RAW.mkdir(parents=True, exist_ok=True)
    for cls in TARGET_CLASSES:
        (DATA_RAW / cls).mkdir(parents=True, exist_ok=True)

    for item in ds:
        style_idx = item["style"]
        style_name = style_names[style_idx]
        style_name = style_name.replace(" ", "_")

        if style_name not in target_set:
            continue
        if MAX_IMAGES_PER_CLASS is not None and counts[style_name] >= MAX_IMAGES_PER_CLASS:
            if all(counts[c] >= MAX_IMAGES_PER_CLASS for c in TARGET_CLASSES):
                break
            continue

        img = item["image"].convert("RGB")
        out_path = DATA_RAW / style_name / f"{safe_name(style_name)}_{counts[style_name]:04d}.jpg"
        img.save(out_path, quality=95)
        counts[style_name] += 1
        print(f"{style_name}: {counts[style_name]}")

    print("Finalizado.")
    print(dict(counts))


if __name__ == "__main__":
    main()
