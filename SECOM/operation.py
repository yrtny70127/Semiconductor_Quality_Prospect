
# 1) 컬럼별 결측률 상위 30개
missing_rate = df.isna().mean().sort_values(ascending=False)
print(missing_rate.head(30))

plt.figure(figsize=(8, 6))
missing_rate.head(30).plot(kind="barh")
plt.title("Top 30 Missing Rates")
plt.gca().invert_yaxis()
plt.tight_layout()
plt.show()

# 2) 행별 결측률 분포
row_missing = df.isna().mean(axis=1)

plt.figure(figsize=(6, 4))
sns.histplot(row_missing, bins=30, kde=True)
plt.title("Row-wise Missing Ratio")
plt.tight_layout()
plt.show()

# 3) 결측 패턴 히트맵 (샘플 200행)
sample = df.sample(min(200, len(df)), random_state=42)
plt.figure(figsize=(12, 6))
sns.heatmap(sample.isna(), cbar=False)
plt.title("Missing Pattern (sample)")
plt.tight_layout()
plt.show()

# 4) 타깃별 결측률 비교 (Pass/Fail 컬럼이 있을 때)
if "Pass/Fail" in df.columns:
    missing_by_target = df.groupby("Pass/Fail").apply(lambda x: x.isna().mean())
    print(missing_by_target.head())

dafafafafafafadadadaadadadada