"""
Executa o pipeline clássico em todas as imagens do dataset local.

Entrada esperada:
    data/raw/Impressionism/*.jpg
    data/raw/Cubism/*.jpg
    data/raw/Baroque/*.jpg
    data/raw/Abstract_Expressionism/*.jpg
    data/raw/Realism/*.jpg

Saídas:
    results/features.csv
    results/compression_metrics.csv
    results/visual_pipeline/*.png
"""
from pathlib import Path
import random
import pandas as pd
from tqdm import tqdm

from src.config import DATA_RAW, RESULTS_DIR, TARGET_CLASSES, IMAGE_SIZE, MAX_IMAGES_PER_CLASS, RANDOM_STATE
from src.io_utils import read_image_rgb
from src.features import extract_features_and_artifacts
from src.visualize import save_pipeline_figure


def main():
    random.seed(RANDOM_STATE)
    features_rows = []
    compression_rows = []
    visual_dir = RESULTS_DIR / "visual_pipeline"
    visual_dir.mkdir(parents=True, exist_ok=True)

    for class_name in TARGET_CLASSES:
        class_dir = DATA_RAW / class_name
        if not class_dir.exists():
            print(f"[AVISO] Pasta ausente: {class_dir}")
            continue

        image_paths = []
        for ext in ["*.jpg", "*.jpeg", "*.png", "*.bmp", "*.webp"]:
            image_paths.extend(class_dir.glob(ext))
        image_paths = sorted(image_paths)
        random.shuffle(image_paths)
        if MAX_IMAGES_PER_CLASS is not None:
            image_paths = image_paths[:MAX_IMAGES_PER_CLASS]

        print(f"Classe {class_name}: {len(image_paths)} imagens")
        saved_visual = 0

        for path in tqdm(image_paths, desc=class_name):
            try:
                img = read_image_rgb(path)
                feats, artifacts, comp = extract_features_and_artifacts(img, IMAGE_SIZE)
            except Exception as exc:
                print(f"[ERRO] {path}: {exc}")
                continue

            row = {"image_path": str(path), "label": class_name}
            row.update(feats)
            features_rows.append(row)

            comp_row = {"image_path": str(path), "label": class_name}
            comp_row.update(comp)
            compression_rows.append(comp_row)

            # Salva uma figura por classe para o artigo/apresentação.
            if saved_visual < 2:
                out_name = f"{class_name}_{saved_visual+1}_{path.stem[:40]}.png".replace(" ", "_")
                save_pipeline_figure(
                    artifacts,
                    visual_dir / out_name,
                    title=f"Pipeline clássico - {class_name}",
                )
                saved_visual += 1

    if not features_rows:
        raise RuntimeError("Nenhuma imagem processada. Verifique data/raw/<classe>/")

    RESULTS_DIR.mkdir(parents=True, exist_ok=True)
    pd.DataFrame(features_rows).to_csv(RESULTS_DIR / "features.csv", index=False)
    pd.DataFrame(compression_rows).to_csv(RESULTS_DIR / "compression_metrics.csv", index=False)
    print(f"OK: características salvas em {RESULTS_DIR / 'features.csv'}")
    print(f"OK: métricas DCT/entropia salvas em {RESULTS_DIR / 'compression_metrics.csv'}")


if __name__ == "__main__":
    main()
