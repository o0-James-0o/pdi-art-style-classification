"""Executa extração de características e treinamento em sequência."""
import subprocess
import sys


def run(cmd):
    print("\n$", " ".join(cmd))
    subprocess.check_call(cmd)


if __name__ == "__main__":
    run([sys.executable, "run_extract_features.py"])
    run([sys.executable, "run_train_models.py"])
