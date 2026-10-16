import torch
import numpy as np

from datasets import load_dataset
from modules.model_config import get_codebert_model_path
from transformers import (
    AutoTokenizer,
    AutoModelForSequenceClassification,
    Trainer
)

# =========================
# 1. 저장된 모델 불러오기
# =========================

MODEL_PATH = get_codebert_model_path("./results/checkpoint-375")

tokenizer = AutoTokenizer.from_pretrained(MODEL_PATH)

model = AutoModelForSequenceClassification.from_pretrained(MODEL_PATH)

# =========================
# 2. 데이터셋 로드
# =========================

dataset = load_dataset("google/code_x_glue_cc_defect_detection")

# validation 일부만 사용
dataset["validation"] = dataset["validation"].select(range(10))

# =========================
# 3. tokenize 함수
# =========================

def tokenize_function(example):

    tokens = tokenizer(
        example["func"],
        truncation=True,
        padding="max_length",
        max_length=128
    )

    tokens["labels"] = 1 if example["target"] else 0

    return tokens

# tokenize 적용
tokenized_dataset = dataset.map(tokenize_function)

# tensor 형식 변환
tokenized_dataset.set_format(
    type="torch",
    columns=["input_ids", "attention_mask", "labels"]
)

# =========================
# 4. Trainer 생성
# =========================

trainer = Trainer(model=model)

# =========================
# 5. 예측 수행
# =========================

predictions = trainer.predict(tokenized_dataset["validation"])

# logits -> 예측 클래스
pred_labels = np.argmax(predictions.predictions, axis=-1)

# 실제값
true_labels = predictions.label_ids

# =========================
# 6. 결과 출력
# =========================

print("\n=== 예측 결과 ===\n")

for i in range(len(pred_labels)):

    print(f"[샘플 {i}]")

    print(f"실제값 : {true_labels[i]}")
    print(f"예측값 : {pred_labels[i]}")

    print("-" * 40)
