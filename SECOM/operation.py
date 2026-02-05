
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

dafafafafafafadadadaadadadadadadaddㅇㅇㅇdddddd



# =========================================
# 4) Target Distribution (Pass/Fail Ratio)
# =========================================
counts = df['Pass/Fail'].value_counts().sort_index()
labels = ['Pass (0)', 'Fail (1)']
colors = ['#4CAF50', '#F44336']

fig, axes = plt.subplots(1, 2, figsize=(12, 4))

axes[0].bar(labels, counts.values, color=colors, edgecolor='black')
for i, v in enumerate(counts.values):
    axes[0].text(i, v + 20, f'{v}', ha='center', fontweight='bold')
axes[0].set_ylabel('Sample Count')
axes[0].set_title('Pass/Fail Distribution')

axes[1].pie(counts.values, labels=labels, colors=colors, autopct='%1.1f%%',
            startangle=90, textprops={'fontsize': 12})
axes[1].set_title('Pass/Fail Ratio')

plt.tight_layout()
plt.show()

print(f'Pass: {counts.iloc[0]} ({counts.iloc[0]/len(df)*100:.1f}%)')
print(f'Fail: {counts.iloc[1]} ({counts.iloc[1]/len(df)*100:.1f}%)')
print(f'Imbalance ratio: 1:{counts.iloc[0]//counts.iloc[1]}')


# =========================================
# 4-1) Pass vs Fail KDE Comparison (Top Features)
# =========================================
valid_cols = [c for c in feat_cols if df[c].isna().mean() <= 0.4]

pass_data = df.loc[df['Pass/Fail'] == 0, valid_cols]
fail_data = df.loc[df['Pass/Fail'] == 1, valid_cols]

mean_diff = (fail_data.mean() - pass_data.mean()).abs()
pooled_std = df[valid_cols].std().replace(0, np.nan)
effect_size = (mean_diff / pooled_std).dropna().sort_values(ascending=False)

top_features = effect_size.head(24).index.tolist()
print(f'KDE visualization: top {len(top_features)} features by effect size')
print(f'Top 5: {top_features[:5]}')

n_cols = 4
n_rows = math.ceil(len(top_features) / n_cols)
fig, axes = plt.subplots(n_rows, n_cols, figsize=(20, n_rows * 3.5))
axes = axes.flatten()

for i, col in enumerate(top_features):
    ax = axes[i]
    for label, name, color in [(0, 'Pass', '#4CAF50'), (1, 'Fail', '#F44336')]:
        subset = df.loc[df['Pass/Fail'] == label, col].dropna()
        if len(subset) > 1:
            subset.plot.kde(ax=ax, label=name, color=color, alpha=0.7)
    ax.set_title(f'{col} (d={effect_size[col]:.3f})', fontsize=10)
    ax.legend(fontsize=8)
    ax.set_ylabel('')

for j in range(len(top_features), len(axes)):
    axes[j].set_visible(False)

plt.suptitle('Pass vs Fail KDE Comparison (Top Features by Effect Size)', fontsize=14, y=1.02)
plt.tight_layout()
plt.show()



# =========================================
# 4-2) Pass vs Fail Boxplot (Top Features)
# =========================================
top12 = top_features[:12]

n_cols = 4
n_rows = math.ceil(len(top12) / n_cols)
fig, axes = plt.subplots(n_rows, n_cols, figsize=(20, n_rows * 4))
axes = axes.flatten()

for i, col in enumerate(top12):
    ax = axes[i]
    plot_df = df[[col, 'Pass/Fail']].dropna()
    plot_df.boxplot(column=col, by='Pass/Fail', ax=ax,
                   boxprops=dict(linewidth=1.5),
                   medianprops=dict(color='red', linewidth=2))
    ax.set_title(col, fontsize=11)
    ax.set_xlabel('')
    ax.set_xticklabels(['Pass', 'Fail'])

for j in range(len(top12), len(axes)):
    axes[j].set_visible(False)

plt.suptitle('Pass vs Fail Boxplot (Top 12 Features)', fontsize=14, y=1.02)
plt.tight_layout()
plt.show()



# =========================================
# 4-3) RF Feature Importance (Quick Exploration)
# =========================================
X_temp = df[valid_cols].fillna(df[valid_cols].median())
y_temp = df['Pass/Fail']

rf_temp = RandomForestClassifier(
    n_estimators=200, max_depth=10, random_state=42, n_jobs=-1,
    class_weight='balanced'
)
rf_temp.fit(X_temp, y_temp)

importances = pd.Series(rf_temp.feature_importances_, index=valid_cols)
top30 = importances.sort_values(ascending=False).head(30)

plt.figure(figsize=(12, 8))
top30.sort_values().plot.barh(color='steelblue', edgecolor='black')
plt.xlabel('Feature Importance')
plt.title('Random Forest Feature Importance (Top 30)')
plt.tight_layout()
plt.show()

print('=== Top 10 Importance ===')
for col, imp in top30.head(10).items():
    print(f'  {col:>5s}: {imp:.4f}')

dadadadadadadadadadadadadadadadadad