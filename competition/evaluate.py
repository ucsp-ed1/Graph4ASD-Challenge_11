import pandas as pd
import sys
from sklearn.metrics import f1_score, accuracy_score, precision_score, recall_score

def main(pred_path, label_path, score_path):
    labels = pd.read_csv(label_path).sort_values("id")
    preds = pd.read_csv(pred_path).sort_values("id")
    labels.rename(columns={'y_pred': 'y_true'}, inplace=True)
    merged = labels.merge(preds, on="id", how="inner")
    
    if len(merged) != len(labels):
        raise ValueError("ID mismatch between predictions and labels")

    f1_sc = f1_score(merged["y_true"], merged["y_pred"], average="macro")
    acc_sc = accuracy_score(merged["y_true"], merged["y_pred"])
    prec_sc = precision_score(merged["y_true"], merged["y_pred"])
    rec_sc = recall_score(merged["y_true"], merged["y_pred"])
    
    print(f"MACRO F1 SCORE={f1_sc:.8f}")
    print(f"ACCURACY SCORE={acc_sc:.8f}")
    print(f"PRECISION SCORE={prec_sc:.8f}")
    print(f"RECALL SCORE={rec_sc:.8f}")
    
    with open(score_path, "w") as f:
        f.write(f"{f1_sc:.6f},{acc_sc:.6f},{prec_sc:.6f},{rec_sc:.6f}")

if __name__ == "__main__":
    main(sys.argv[1], sys.argv[2], sys.argv[3])