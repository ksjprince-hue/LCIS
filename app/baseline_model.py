from datasets import load_dataset
import pandas as pd

from sklearn.model_selection import train_test_split
from sklearn.feature_extraction.text import TfidfVectorizer
from sklearn.linear_model import LogisticRegression
from sklearn.metrics import accuracy_score, f1_score, classification_report

# 데이터셋 로드
dataset = load_dataset("google/code_x_glue_cc_defect_detection")

train_data = dataset["train"]

# DataFrame 변환
rows = []

for item in train_data:
    rows.append({
        "code": item["func"],
        "label": int(item["target"])
    })

df = pd.DataFrame(rows)

print(df.head())

# 입력(X), 정답(y)
X = df["code"]
y = df["label"]

# train / test 분리
X_train, X_test, y_train, y_test = train_test_split(
    X,
    y,
    test_size=0.2,
    random_state=42
)

# TF-IDF 벡터화
vectorizer = TfidfVectorizer(
    max_features=5000
)

X_train_tfidf = vectorizer.fit_transform(X_train)
X_test_tfidf = vectorizer.transform(X_test)

# 모델 생성
model = LogisticRegression(max_iter=1000)

# 학습
model.fit(X_train_tfidf, y_train)

# 예측
y_pred = model.predict(X_test_tfidf)

# 평가
print("Accuracy:", accuracy_score(y_test, y_pred))
print("F1 Score:", f1_score(y_test, y_pred))

print("\n=== Classification Report ===")
print(classification_report(y_test, y_pred))