"""
Treina e avalia modelos simples com as características extraídas.

Entrada:
    results/features.csv

Saídas:
    results/model_comparison.csv
    results/classification_report_best.csv
    results/confusion_matrix_best.png
    results/knn_k_variation.png
    results/experiment_summary.json

Correção importante:
    Este script força X e y para numpy.ndarray. Isso evita erro de indexação
    entre pandas/pyarrow e scikit-learn em algumas instalações do Python.
"""
import json
import numpy as np
import pandas as pd

from sklearn.model_selection import train_test_split
from sklearn.preprocessing import StandardScaler
from sklearn.pipeline import Pipeline
from sklearn.neighbors import KNeighborsClassifier
from sklearn.linear_model import LogisticRegression
from sklearn.metrics import (
    accuracy_score,
    precision_recall_fscore_support,
    classification_report,
    confusion_matrix,
)

from src.config import RESULTS_DIR, K_VALUES, TEST_SIZE, RANDOM_STATE
from src.visualize import save_confusion_matrix, save_barplot


def evaluate_model(name, model, X_train, X_test, y_train, y_test):
    model.fit(X_train, y_train)
    pred = model.predict(X_test)

    acc = accuracy_score(y_test, pred)
    precision, recall, f1, _ = precision_recall_fscore_support(
        y_test, pred, average="macro", zero_division=0
    )

    return {
        "model": name,
        "accuracy": float(acc),
        "precision_macro": float(precision),
        "recall_macro": float(recall),
        "f1_macro": float(f1),
        "predictions": np.asarray(pred, dtype=object),
        "fitted_model": model,
    }


def main():
    features_path = RESULTS_DIR / "features.csv"
    if not features_path.exists():
        raise FileNotFoundError("Execute primeiro: python run_extract_features.py")

    df = pd.read_csv(features_path)

    if "label" not in df.columns:
        raise ValueError("A coluna 'label' não foi encontrada em results/features.csv")

    # Remove colunas de identificação. O restante deve ser numérico.
    feature_cols = [c for c in df.columns if c not in ["image_path", "label"]]

    # Converte explicitamente para NumPy para evitar ArrowExtensionArray/pyarrow.
    X_df = df[feature_cols].apply(pd.to_numeric, errors="coerce")
    X_df = X_df.replace([np.inf, -np.inf], np.nan).fillna(0.0)
    X = X_df.to_numpy(dtype=np.float64)
    y = df["label"].astype(str).to_numpy(dtype=object)

    labels, counts = np.unique(y, return_counts=True)
    print("Classes encontradas no features.csv:")
    for label, count in zip(labels, counts):
        print(f"- {label}: {count} imagens")

    if len(labels) < 2:
        raise ValueError("É necessário ter pelo menos 2 classes para treinar os modelos.")

    if np.min(counts) < 2:
        raise ValueError("Cada classe precisa ter pelo menos 2 imagens para divisão treino/teste estratificada.")

    X_train, X_test, y_train, y_test = train_test_split(
        X,
        y,
        test_size=TEST_SIZE,
        random_state=RANDOM_STATE,
        stratify=y,
    )

    results = []
    raw_results = []

    for k in K_VALUES:
        if k > len(y_train):
            print(f"[AVISO] Ignorando KNN k={k}, pois há apenas {len(y_train)} amostras de treino.")
            continue

        model = Pipeline([
            ("scaler", StandardScaler()),
            ("knn", KNeighborsClassifier(n_neighbors=k)),
        ])

        res = evaluate_model(f"KNN_k={k}", model, X_train, X_test, y_train, y_test)
        raw_results.append(res)
        results.append({
            key: res[key]
            for key in ["model", "accuracy", "precision_macro", "recall_macro", "f1_macro"]
        })

    logreg = Pipeline([
        ("scaler", StandardScaler()),
        ("logreg", LogisticRegression(max_iter=3000, random_state=RANDOM_STATE)),
    ])

    res = evaluate_model("LogisticRegression", logreg, X_train, X_test, y_train, y_test)
    raw_results.append(res)
    results.append({
        key: res[key]
        for key in ["model", "accuracy", "precision_macro", "recall_macro", "f1_macro"]
    })

    results_df = pd.DataFrame(results).sort_values("f1_macro", ascending=False)
    results_df.to_csv(RESULTS_DIR / "model_comparison.csv", index=False)

    best_name = results_df.iloc[0]["model"]
    best = next(r for r in raw_results if r["model"] == best_name)

    labels_sorted = sorted([str(x) for x in np.unique(y)])

    report = classification_report(
        y_test,
        best["predictions"],
        labels=labels_sorted,
        output_dict=True,
        zero_division=0,
    )
    pd.DataFrame(report).transpose().to_csv(RESULTS_DIR / "classification_report_best.csv")

    cm = confusion_matrix(y_test, best["predictions"], labels=labels_sorted)
    save_confusion_matrix(
        cm,
        labels_sorted,
        RESULTS_DIR / "confusion_matrix_best.png",
        title=f"Matriz de confusão - {best_name}",
    )

    knn_df = results_df[results_df["model"].str.startswith("KNN")].copy()
    if len(knn_df) > 0:
        save_barplot(
            knn_df,
            "model",
            "f1_macro",
            RESULTS_DIR / "knn_k_variation.png",
            "Variação do K no KNN",
            "F1 macro",
        )

    summary = {
        "best_model": str(best_name),
        "feature_count": int(len(feature_cols)),
        "train_samples": int(len(y_train)),
        "test_samples": int(len(y_test)),
        "labels": labels_sorted,
    }

    with open(RESULTS_DIR / "experiment_summary.json", "w", encoding="utf-8") as f:
        json.dump(summary, f, ensure_ascii=False, indent=2)

    print("\nComparação de modelos:")
    print(results_df.to_string(index=False))
    print(f"\nMelhor modelo: {best_name}")
    print(f"Saídas salvas em: {RESULTS_DIR}")


if __name__ == "__main__":
    main()
