# Semiconductor Process Data Visualization Pipeline
# 목적: 상관관계가 약한 공정 데이터에서 '관계성'을 설명하기 위한 시각화 세트
# - Correlation heatmap
# - Defect 기준 분포 비교 (Boxplot)
# - Threshold/분포 비교 (Histogram)
# - 2D 조합 효과 (Scatter)
# - Model 기반 Feature Importance

import pandas as pd
import numpy as np
import matplotlib.pyplot as plt
import seaborn as sns

from sklearn.model_selection import train_test_split
from sklearn.impute import SimpleImputer
from sklearn.preprocessing import StandardScaler
from sklearn.pipeline import Pipeline
from sklearn.ensemble import RandomForestClassifier

# ==============================
# 1. 데이터 로드 (경로 수정 가능)
# ==============================

DATA_PATH = "data/secom/secom.data"
LABEL_PATH = "data/secom/secom_labels.data"

X = pd.read_csv(DATA_PATH, sep=" ", header=None)
y = pd.read_csv(LABEL_PATH, sep=" ", header=None)
y.columns = ["label", "timestamp"]

# Defect 라벨 정리 (1: Pass, -1: Fail → 0/1)
y["Defect"] = (y["label"] == -1).astype(int)

# 컬럼명 지정
X.columns = [f"Sensor_{i}" for i in range(X.shape[1])]

df = X.copy()
df["Defect"] = y["Defect"]

print("Data shape:", df.shape)
print(df["Defect"].value_counts())

# ==============================
# 2. 결측치 비율 높은 컬럼 제거
# ==============================

nan_threshold = 0.8
valid_cols = df.columns[df.isna().mean() < nan_threshold]
df = df[valid_cols]

print("After NaN filtering:", df.shape)

# ==============================
# 3. Correlation Heatmap (샘플 일부)
# ==============================

sample_cols = list(df.columns[:15]) + ["Defect"]

plt.figure(figsize=(10, 8))
sns.heatmap(df[sample_cols].corr(), cmap="coolwarm", center=0)
plt.title("Correlation Heatmap (Sample Sensors)")
plt.tight_layout()
plt.show()

# ==============================
# 4. Defect 기준 분포 비교 (Boxplot)
# ==============================

boxplot_sensors = sample_cols[:3]

for col in boxplot_sensors:
    plt.figure(figsize=(4, 4))
    sns.boxplot(x="Defect", y=col, data=df)
    plt.title(f"Distribution of {col} by Defect")
    plt.tight_layout()
    plt.show()

# ==============================
# 5. Threshold / Histogram 비교
# ==============================

hist_sensor = boxplot_sensors[0]

plt.figure(figsize=(6, 4))
sns.histplot(
    data=df,
    x=hist_sensor,
    hue="Defect",
    bins=40,
    stat="density",
    common_norm=False,
    alpha=0.6
)
plt.title(f"Histogram of {hist_sensor} by Defect")
plt.tight_layout()
plt.show()

# ==============================
# 6. 2D 조합 효과 시각화
# ==============================

if len(boxplot_sensors) >= 2:
    plt.figure(figsize=(6, 5))
    sns.scatterplot(
        data=df,
        x=boxplot_sensors[0],
        y=boxplot_sensors[1],
        hue="Defect",
        alpha=0.5
    )
    plt.title("2D Conditional Scatter (Combination Effect)")
    plt.tight_layout()
    plt.show()

# ==============================
# 7. RandomForest 기반 Feature Importance
# ==============================

X = df.drop(columns=["Defect"])
y = df["Defect"]

X_train, X_test, y_train, y_test = train_test_split(
    X, y, test_size=0.2, stratify=y, random_state=42
)

pipe = Pipeline([
    ("imputer", SimpleImputer(strategy="median")),
    ("scaler", StandardScaler()),
    ("model", RandomForestClassifier(
        n_estimators=200,
        max_depth=None,
        random_state=42,
        n_jobs=-1
    ))
])

pipe.fit(X_train, y_train)

rf = pipe.named_steps["model"]
importances = pd.Series(rf.feature_importances_, index=X.columns)

# 상위 중요 센서 시각화
top_k = 10
plt.figure(figsize=(6, 5))
importances.sort_values(ascending=False).head(top_k).plot(kind="barh")
plt.gca().invert_yaxis()
plt.title("Top Feature Importances (Random Forest)")
plt.tight_layout()
plt.show()

print("Top important sensors:")
print(importances.sort_values(ascending=False).head(top_k))