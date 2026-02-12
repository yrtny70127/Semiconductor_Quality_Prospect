import json
import os
import sys

# Forces utf-8 for stdout/stderr just in case
sys.stdout.reconfigure(encoding='utf-8')

nb_path = "Semi-defect_finder_New.ipynb"
print(f"CWD: {os.getcwd()}")
print(f"Target file: {nb_path}")

try:
    with open(nb_path, "r", encoding="utf-8") as f:
        nb = json.load(f)
    print("Loaded notebook JSON.")
except Exception as e:
    print(f"Failed to load notebook: {e}")
    sys.exit(1)

new_code = """# --- Confusion Matrix 1x3 (각 지표 Top 1, 필터 적용) ---
fig, axes = plt.subplots(1, 3, figsize=(15, 5))
row_metrics = ["Recall", "Specificity", "BalAcc"]

for idx, metric in enumerate(row_metrics):
    # Top 1 모델 가져오기
    top_m = get_top3_filtered(df_results, metric).iloc[0]
    
    combo = top_m["model"]
    m = trained_models[combo]
    proba = m.predict_proba(X_valid)[:, 1]
    pred = (proba >= 0.5).astype(int)
    cm = confusion_matrix(y_valid, pred)
    
    ax = axes[idx]
    sns.heatmap(cm, annot=True, fmt="d", cmap="Blues",
                xticklabels=["Pass", "Fail"], yticklabels=["Pass", "Fail"], ax=ax)
    
    val = top_m[metric]
    filt = "(Spec≥0.3)" if metric == "Recall" else "(Rec≥0.3)" if metric == "Specificity" else ""
    
    ax.set_title(f"Top 1 {metric} {filt}\\n{combo}\\n({metric}={val:.3f})", fontsize=11)
    ax.set_xlabel("Predicted")
    ax.set_ylabel("Actual")

plt.suptitle("Confusion Matrix: Top 1 by Recall / Specificity / BalAcc (lower limit filter)", y=1.05, fontsize=14)
plt.tight_layout()
plt.show()
"""

new_source = [line + "\\n" for line in new_code.splitlines()]

target_str = "# --- Confusion Matrix 3x3"

found = False
for i, cell in enumerate(nb["cells"]):
    if cell["cell_type"] == "code":
        source_joined = "".join(cell["source"])
        if target_str in source_joined:
            print(f"Found target cell at index {i}")
            cell["source"] = new_source
            found = True
            break

if found:
    try:
        with open(nb_path, "w", encoding="utf-8") as f:
            json.dump(nb, f, indent=1, ensure_ascii=False)
        print("Notebook updated successfully.")
    except Exception as e:
        print(f"Error writing file: {e}")
        # Try writing to a new file as fallback
        fallback = "Semi-defect_finder_New_fixed.ipynb"
        print(f"Attempting fallback to {fallback}")
        with open(fallback, "w", encoding="utf-8") as f:
            json.dump(nb, f, indent=1, ensure_ascii=False)
        print(f"Written to fallback: {fallback}")
else:
    print("Target cell NOT found in any code cell.")
