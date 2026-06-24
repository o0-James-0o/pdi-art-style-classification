
from pathlib import Path

PROJECT_ROOT = Path(__file__).resolve().parents[1]
DATA_RAW = PROJECT_ROOT / "data" / "raw"
DATA_PROCESSED = PROJECT_ROOT / "data" / "processed"
RESULTS_DIR = PROJECT_ROOT / "results"

# Classes oficiais do recorte usado no artigo.
# Isso evita o aviso da pasta Abstract_Expressionism, que fazia parte de uma versão anterior.
TARGET_CLASSES = [
    "Impressionism",
    "Cubism",
    "Baroque",
    "Realism",
]

# Tamanho pequeno o suficiente para DCT manual e execução em notebook/PC comum.
IMAGE_SIZE = 64

# O recorte baixado possui 50 pinturas por classe.
MAX_IMAGES_PER_CLASS = 50

# Bloco padrão da DCT, igual ao JPEG clássico.
DCT_BLOCK_SIZE = 8

# Matriz de quantização simplificada inspirada no JPEG luminância.
QUANTIZATION_MATRIX_8X8 = [
    [16, 11, 10, 16, 24, 40, 51, 61],
    [12, 12, 14, 19, 26, 58, 60, 55],
    [14, 13, 16, 24, 40, 57, 69, 56],
    [14, 17, 22, 29, 51, 87, 80, 62],
    [18, 22, 37, 56, 68,109,103, 77],
    [24, 35, 55, 64, 81,104,113, 92],
    [49, 64, 78, 87,103,121,120,101],
    [72, 92, 95, 98,112,100,103, 99],
]

# Hiperparâmetros estudados no KNN.
K_VALUES = [1, 3, 5, 7, 9, 11]

RANDOM_STATE = 42
TEST_SIZE = 0.30
