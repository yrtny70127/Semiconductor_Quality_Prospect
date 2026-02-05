import seaborn as sns
import matplotlib.pyplot as plt
import numpy as np
import pandas as pd

# =========================================
# 7) 공정별 추가 시각화 (Violin Plot 적용 버전)
# =========================================

def plot_violin_by_defect(df_t, tool_name, target_col="Defect", max_cols=6):
    """박스플롯 대신 분포까지 보여주는 바이올린 플롯 사용"""
    num_cols = [c for c in df_t.columns if pd.api.types.is_numeric_dtype(df_t[c]) and c != target_col]
    cols = num_cols[:max_cols]
    if not cols:
        print(f"{tool_name}: numeric columns 없음")
        return

    # 서브플롯 설정 (한 화면에 여러 개 배치)
    ncols = 3
    nrows = int(np.ceil(len(cols) / ncols))
    fig, axes = plt.subplots(nrows, ncols, figsize=(5*ncols, 4*nrows))
    fig.suptitle(f"[{tool_name}] Feature Distribution by {target_col}", fontsize=16)
    axes = axes.flatten()

    for i, c in enumerate(cols):
        # sns.violinplot 사용
        sns.violinplot(x=target_col, y=c, data=df_t, ax=axes[i], inner="quartile", palette="muted")
        axes[i].set_title(f"{c}")
        axes[i].set_xlabel("Target (0:Normal, 1:Defect)")
        axes[i].set_ylabel("Value")

    # 남는 칸 제거
    for j in range(i + 1, len(axes)):
        fig.delaxes(axes[j])

    plt.tight_layout(rect=[0, 0.03, 1, 0.95])
    plt.show()

# --- 나머지 함수들은 동일하게 유지하되, 호출부만 업데이트 ---

def plot_kde_overlap(df_t, tool_name, target_col="Defect", max_cols=4):
    num_cols = [c for c in df_t.columns if pd.api.types.is_numeric_dtype(df_t[c]) and c != target_col]
    cols = num_cols[:max_cols]
    if not cols: return
    for c in cols:
        plt.figure(figsize=(8, 4))
        sns.kdeplot(data=df_t, x=c, hue=target_col, fill=True, common_norm=False, palette="Set1")
        plt.title(f"{tool_name} KDE - {c}")
        plt.show()

def plot_top_corr_pairs(df_t, tool_name, topk=10):
    num_cols = [c for c in df_t.columns if pd.api.types.is_numeric_dtype(df_t[c])]
    if len(num_cols) < 2: return
    c = df_t[num_cols].corr()
    pairs = []
    for i in range(len(num_cols)):
        for j in range(i+1, len(num_cols)):
            a, b = num_cols[i], num_cols[j]
            val = c.loc[a, b]
            if pd.isna(val): continue
            pairs.append((a, b, float(val), float(abs(val))))
    pairs = sorted(pairs, key=lambda x: x[3], reverse=True)[:topk]
    out = pd.DataFrame(pairs, columns=["feat_a", "feat_b", "corr", "abs_corr"])
    print(f"{tool_name} top corr pairs:")
    display(out)

def plot_scatter_top_pairs(df_t, tool_name, topk=3):
    num_cols = [c for c in df_t.columns if pd.api.types.is_numeric_dtype(df_t[c])]
    if len(num_cols) < 2: return
    c = df_t[num_cols].corr().abs()
    pairs = []
    for i in range(len(num_cols)):
        for j in range(i+1, len(num_cols)):
            a, b = num_cols[i], num_cols[j]
            val = c.loc[a, b]
            if pd.isna(val): continue
            pairs.append((a, b, float(val)))
    pairs = sorted(pairs, key=lambda x: x[2], reverse=True)[:topk]
    for a, b, v in pairs:
        plt.figure(figsize=(6, 5))
        sns.scatterplot(data=df_t, x=a, y=b, hue=target_col, alpha=0.5)
        plt.title(f"{tool_name}: {a} vs {b} (|corr|={v:.2f})")
        plt.show()

def plot_cdf_tail(df_t, tool_name, col):
    if col not in df_t.columns or not pd.api.types.is_numeric_dtype(df_t[col]): return
    s = df_t[col].dropna().sort_values()
    y = np.arange(1, len(s)+1) / len(s)
    plt.figure(figsize=(8, 4))
    plt.plot(s, y)
    plt.axhline(0.99, color='red', linestyle='--', alpha=0.5) # 99% 라인 추가
    plt.title(f"{tool_name} CDF - {col}")
    plt.ylabel("CDF")
    plt.show()

# =========================================
# 실행부 (루프)
# =========================================
for tool_name, df_t in tool_raw.items():
    print(f"\n{'='*30}\n[RUNNING ANALYSIS] Tool: {tool_name}\n{'='*30}")
    
    # 1. 바이올린 플롯 호출 (Boxplot 대체)
    plot_violin_by_defect(df_t, tool_name, target_col=target_col, max_cols=6)
    
    # 

    # 2. KDE 오버랩 (Seaborn으로 더 깔끔하게 출력)
    plot_kde_overlap(df_t, tool_name, target_col=target_col, max_cols=4)
    
    # 3. 상관관계 요약
    plot_top_corr_pairs(df_t, tool_name, topk=10)
    
    # 4. 산점도 (Hue 추가하여 불량 분포 시각화)
    plot_scatter_top_pairs(df_t, tool_name, topk=3)

    # 5. CDF tail 분석
    for col in ["Particle_Count", "Vibration_Level", "Stage_Alignment_Error"]:
        if col in df_t.columns:
            plot_cdf_tail(df_t, tool_name, col)