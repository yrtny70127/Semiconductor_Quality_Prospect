# 🔍 Semiconductor Manufacturing Defect Prediction

반도체 제조 공정 센서 데이터를 활용하여  
**불량(Defect) 여부를 예측하는 이진 분류 모델**을 구축한 프로젝트입니다.

---

## 1️⃣ Problem Definition

반도체 제조 공정은 수백 개의 센서 변수를 포함하는 고차원 구조이며,  
결함 발생은 단일 변수로 설명되지 않는 **다변수·비선형 문제**입니다.

### 주요 특징
- 591개 센서 변수
- 결함 비율 6.6% (극단적 클래스 불균형)
- 선형 분리 어려움 (PCA/t-SNE 상 명확한 분리 없음)

➡ 단일 모델이 아닌 **전략적 앙상블 접근 필요**

---

## 2️⃣ Data & Preprocessing

### 📌 Dataset
- SECOM Dataset
- 1,567 samples / 591 features
- Target: Defect (0: 정상, 1: 불량)

### 📌 Preprocessing
- 결측 비율 50% 이상 변수 제거
- 잔여 결측치 중앙값 대체
- 최종 변수 수: 194개

### 📌 Feature Selection
- Train 데이터 기준 ANOVA 활용
- 상위 20개 주요 변수 선정

### 📌 Data Split
- Stratified 7 : 1.5 : 1.5 (Train / Valid / Test)
- 클래스 비율 유지

---

## 3️⃣ Modeling Strategy

### ① 후보 모델 5종
- Logistic Regression  
- Random Forest  
- XGBoost  
- HistGradientBoosting  
- LightGBM  

### ② 샘플링 전략 3종
- Baseline (원본)
- SMOTE (Over-sampling)
- Random Under Sampling

➡ **5 모델 × 3 샘플링 = 15개 조합 실험**

---

## 4️⃣ Metric-Driven Model Selection

### 평가 지표
- Recall (불량 검출 최우선)
- Specificity (정상 오탐 최소화)
- Balanced Accuracy (불균형 보정 지표)

Balanced Accuracy 정의:

\[
BalAcc = (Recall + Specificity) / 2
\]

각 지표 기준 Top1 모델 선정 후  
**지표별 강점 모델 조합 앙상블 전략 적용**

---

## 5️⃣ Ensemble Optimization

### 🔹 방식
- Soft Voting 기반 확률 평균
- Weight Grid 탐색
- Threshold 조정 (Recall–Specificity 균형 최적화)

### 🔹 최적 파라미터
- Best Weights: `[4, 1, 1]`
- Threshold: `0.46`
- Validation BalAcc: `0.8136`

➡ Recall Top 모델에 가중 강화

---

## 6️⃣ Final Test Performance (SECOM)

| Metric | Score |
|--------|-------|
| Recall | 0.812 |
| Specificity | 0.623 |
| Balanced Accuracy | 0.717 |

✔ 불량 검출 성능 안정 유지  
✔ Validation 대비 과도한 성능 저하 없음  
✔ 운영 환경 적용 가능 수준 확보  

---

## 7️⃣ Stability Verification (10 Seeds)

Multi-seed 실험 결과:

- Test BalAcc: `0.655 ± 0.062`
- 변동폭 제한적 (min 0.578 ~ max 0.764)
- 특정 시드 의존성 없음

➡ 모델 구조의 재현성 및 안정성 확보

---

## 8️⃣ External Dataset Validation

Kaggle Wafer Manufacturing Dataset 적용  
동일 전략으로 재실험

### Test 성능

| Metric | Score |
|--------|-------|
| Recall | 0.818 |
| Specificity | 0.877 |
| Balanced Accuracy | 0.847 |

✔ 데이터셋 변경 후에도 성능 구조 유지  
✔ Recall 중심 전략의 환경 독립성 확인  
✔ 앙상블 구조의 데이터 적응성 검증  

---

## 🧠 Key Contributions

- 불균형 데이터 환경에서 **지표 기반 Top1 앙상블 전략 제안**
- 단순 모델 선택이 아닌 **의사결정 경계 최적화 접근**
- Multi-seed 및 외부 데이터셋 검증을 통한 일반화 확인

---

## 🚀 Conclusion

본 프로젝트는  

> 불량 검출 중심 설계를 유지하면서도  
> 일반화 가능한 균형 성능을 확보한 실전형 앙상블 구조를 구현하였습니다.
