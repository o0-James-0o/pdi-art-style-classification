from datasets import load_dataset
from pathlib import Path
from tqdm import tqdm
import re

# ============================
# CONFIGURAÇÃO DO RECORTE
# ============================

DATASET_NAME = "huggan/wikiart"

TARGET_STYLES = [
    "Impressionism",
    "Cubism",
    "Baroque",
    "Realism"
]

IMAGES_PER_STYLE = 50
OUTPUT_DIR = Path("data/raw")
IMAGE_SIZE = (256, 256)


def safe_name(text):
    """
    Remove caracteres problemáticos para nomes de arquivos e pastas.
    """
    text = text.replace(" ", "_")
    text = re.sub(r"[^a-zA-Z0-9_\\-]", "", text)
    return text


def get_style_name(example, style_feature):
    """
    Converte o rótulo numérico do estilo para o nome textual.
    Em alguns datasets, o estilo pode vir como número.
    Em outros, pode vir como texto.
    """
    style_value = example["style"]

    if isinstance(style_value, int):
        return style_feature.int2str(style_value)

    return str(style_value)


def main():
    print("Carregando WikiArt em modo streaming...")
    dataset = load_dataset(
        DATASET_NAME,
        split="train",
        streaming=True
    )

    style_feature = dataset.features["style"]

    counts = {style: 0 for style in TARGET_STYLES}

    for style in TARGET_STYLES:
        folder = OUTPUT_DIR / safe_name(style)
        folder.mkdir(parents=True, exist_ok=True)

    total_needed = len(TARGET_STYLES) * IMAGES_PER_STYLE

    print("Baixando recorte enxuto...")
    progress = tqdm(total=total_needed)

    for example in dataset:
        style_name = get_style_name(example, style_feature)

        if style_name not in TARGET_STYLES:
            continue

        if counts[style_name] >= IMAGES_PER_STYLE:
            continue

        image = example["image"].convert("RGB")
        image = image.resize(IMAGE_SIZE)

        style_folder = OUTPUT_DIR / safe_name(style_name)
        image_id = counts[style_name]

        output_path = style_folder / f"{safe_name(style_name)}_{image_id:03d}.jpg"
        image.save(output_path, quality=95)

        counts[style_name] += 1
        progress.update(1)

        if all(counts[style] >= IMAGES_PER_STYLE for style in TARGET_STYLES):
            break

    progress.close()

    print("\\nRecorte finalizado!")
    print("Imagens salvas em:", OUTPUT_DIR)

    for style, count in counts.items():
        print(f"{style}: {count} imagens")


if __name__ == "__main__":
    main()