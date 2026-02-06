from sklearn.decomposition import PCA
from sklearn.preprocessing import StandardScaler, MinMaxScaler
from sklearn.impute import SimpleImputer
from sklearn.ensemble import RandomForestClassifier
from sklearn.manifold import TSNE

X = df.drop(columns=['Pass/Fail'])
y = df['Pass/Fail']

# [전략 1] 결측치 비율 분포 (Large Scale 대응)
missing_ratio = X.isnull().mean()
plt.figure(figsize=(10, 5))
plt.hist(missing_ratio, bins=50, color='#6EC5E9', edgecolor='black')
plt.title('Distribution of Missing Values (Column-wise)')
plt.xlabel('Missing Ratio (0.0 ~ 1.0)')
plt.ylabel('Count of Columns')
plt.grid(axis='y', alpha=0.3)
plt.savefig('missing_values_hist.png') # 결과 저장
plt.show()

# [전략 2] 타겟(Pass/Fail)과 상관관계가 높은 Top 센서 추출
imputer = SimpleImputer(strategy='mean')
X_imputed = pd.DataFrame(imputer.fit_transform(X), columns=X.columns)

correlations = X_imputed.corrwith(y)
top_pos = correlations.nlargest(10)  # 양의 상관관계 Top 10
top_neg = correlations.nsmallest(10) # 음의 상관관계 Top 10
top_corr = pd.concat([top_pos, top_neg])

plt.figure(figsize=(12, 6))
colors = ['red' if x < 0 else 'blue' for x in top_corr.values]
top_corr.plot(kind='bar', color=colors)
plt.title('Top Positive & Negative Correlations with Pass/Fail')
plt.ylabel('Correlation Coefficient')
plt.axhline(0, color='black', linewidth=0.8)
plt.grid(axis='y', alpha=0.3)
plt.show()

# [전략 3] PCA 차원 축소 시각화 (590차원 -> 2차원)
scaler = StandardScaler()
X_scaled = scaler.fit_transform(X_imputed)

pca = PCA(n_components=2)
X_pca = pca.fit_transform(X_scaled)
pca_df = pd.DataFrame(data=X_pca, columns=['PC1', 'PC2'])
pca_df['Target'] = y.values

plt.figure(figsize=(8, 8))
sns.scatterplot(data=pca_df, x='PC1', y='PC2', hue='Target', 
                alpha=0.6, palette={-1: 'blue', 1: 'red'})
plt.title('PCA: 2D Projection of Sensor Data')
plt.show()

# [전략 4] 랜덤 포레스트 기반 중요 변수(Feature Importance) 추출
rf = RandomForestClassifier(n_estimators=100, random_state=42, n_jobs=-1)
rf.fit(X_imputed, y)

importances = pd.Series(rf.feature_importances_, index=X.columns)
top_features = importances.nlargest(10)

plt.figure(figsize=(10, 6))
top_features.sort_values().plot(kind='barh', color='green')
plt.title('Top 10 Important Features (Random Forest)')
plt.xlabel('Importance Score')
plt.show()

# [전략 5] Top 10 중요 변수의 분포 상세 비교 (Boxplot)
top_10_cols = top_features.index[:10]

fig, axes = plt.subplots(2, 5, figsize=(20, 10)) 
axes = axes.flatten() 

for i, col in enumerate(top_10_cols):
    sns.boxplot(x=y, y=X_imputed[col], ax=axes[i], palette='Set2')
    axes[i].set_title(f'Top {i+1}: Sensor {col}')
    axes[i].set_xlabel('Pass(-1) vs Fail(1)')

plt.tight_layout()
plt.show()

# [전략 6] t-SNE 시각화 (비선형 차원 축소)

scaler = StandardScaler()
X_scaled = scaler.fit_transform(X_imputed)

# 속도를 위해 perplexity=30, iter=1000 설정
tsne = TSNE(n_components=2, random_state=42, perplexity=30)
X_tsne = tsne.fit_transform(X_scaled)

tsne_df = pd.DataFrame(data=X_tsne, columns=['Dim1', 'Dim2'])
tsne_df['Target'] = y.values

plt.figure(figsize=(10, 8))
sns.scatterplot(data=tsne_df, x='Dim1', y='Dim2', hue='Target', 
                palette={-1: 'lightgrey', 1: 'red'}, alpha=0.7, style='Target')
plt.title('t-SNE Visualization (Red: Fail, Grey: Pass)')
plt.show()

# [전략 7] Top 20 센서 간의 클러스터맵 (변수 간 관계 파악)
# ---------------------------------------------------------
# 모든 변수를 다 그리면 너무 복잡하므로, 타겟과 상관관계 높은 Top 20만 선정
correlations = X_imputed.corrwith(y).abs()
top_20_cols = correlations.nlargest(20).index
X_top20 = X_imputed[top_20_cols]

# 변수 간의 상관관계 계산
corr_matrix = X_top20.corr()

plt.figure(figsize=(12, 10))
sns.clustermap(corr_matrix, annot=True, fmt=".2f", cmap='coolwarm', 
               figsize=(12, 12), tree_kws=dict(linewidths=1.5))
plt.title('ClusterMap of Top 20 Correlated Features', pad=20)
plt.show()

# [전략 8] 평행 좌표 그래프 (Parallel Coordinates)
# 값의 범위가 다르면 비교가 불가능하므로 Min-Max Scaling 필수
minmax_scaler = MinMaxScaler()
X_norm = pd.DataFrame(minmax_scaler.fit_transform(X_imputed), columns=X.columns)

# Top 10 중요한 변수만 뽑아서 흐름 비교
top_10_cols = correlations.nlargest(10).index
plot_df = X_norm[top_10_cols].copy()
plot_df['Target'] = y.values

# 시각화 가독성을 위해 데이터 샘플링 (Fail은 전부 포함, Pass는 100개만 샘플링)
df_fail = plot_df[plot_df['Target'] == 1]
df_pass = plot_df[plot_df['Target'] == 0].sample(n=100, random_state=42)
final_plot_df = pd.concat([df_pass, df_fail])

plt.figure(figsize=(15, 6))
pd.plotting.parallel_coordinates(final_plot_df, 'Target', color=('#43a2ca', '#f03b20'), alpha=0.5)
plt.title('Parallel Coordinates Plot (Top 10 Features)')
plt.xlabel('Sensor Features')
plt.ylabel('Normalized Value (0-1)')
plt.xticks(rotation=45)
plt.grid(True, alpha=0.3)
plt.show()



ㅇㅁㅇㅁㅇㅁㅇㅁㅇㅁㅇㅁㅇㅁㅇㅁㅇㅁㅇㅁㅇㅁ