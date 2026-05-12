# 상단에 추가
import torch
print(f"GPU 사용 가능: {torch.cuda.is_available()}")
print(f"GPU 이름: {torch.cuda.get_device_name(0)}")
from datasets import load_dataset
from transformers import (
    AutoTokenizer,
    AutoModelForSequenceClassification,
    TrainingArguments,
    Trainer
)

import numpy as np
from sklearn.metrics import accuracy_score, f1_score

# =========================
# 1. 데이터셋 로드
# =========================

dataset = load_dataset("google/code_x_glue_cc_defect_detection")

# =========================
# 2. tokenizer 로드
# =========================

MODEL_NAME = "microsoft/codebert-base"

tokenizer = AutoTokenizer.from_pretrained(MODEL_NAME)

# =========================
# 3. tokenize 함수
# =========================

def tokenize_function(example):

    tokens = tokenizer(
        example["func"],
        truncation=True,
        padding="max_length",
        max_length=256
    )

    # bool -> int
    tokens["labels"] = 1 if example["target"] else 0

    return tokens


# 데이터 tokenize
tokenized_dataset = dataset.map(tokenize_function)

# PyTorch tensor 형식 지정
tokenized_dataset.set_format(
    type="torch",
    columns=["input_ids", "attention_mask", "labels"]
)
# =========================
# 4. 모델 로드
# =========================

model = AutoModelForSequenceClassification.from_pretrained(
    MODEL_NAME,
    num_labels=2,
    problem_type="single_label_classification"
)

# =========================
# 5. 평가 함수
# =========================

def compute_metrics(eval_pred):

    logits, labels = eval_pred

    predictions = np.argmax(logits, axis=-1)

    acc = accuracy_score(labels, predictions)
    f1 = f1_score(labels, predictions)

    return {
        "accuracy": acc,
        "f1": f1
    }

# =========================
# 6. 학습 설정
# =========================

training_args = TrainingArguments(
    output_dir="./results",

    eval_strategy="epoch",

    save_strategy="epoch",

    per_device_train_batch_size=8,

    per_device_eval_batch_size=8,

    num_train_epochs=1,

    logging_dir="./logs",

    logging_steps=50
)

# =========================
# 7. Trainer 생성
# =========================

trainer = Trainer(
    model=model,

    args=training_args,

    train_dataset=tokenized_dataset["train"],

    eval_dataset=tokenized_dataset["validation"],

    compute_metrics=compute_metrics
)

# =========================
# 8. 학습 시작
# =========================

trainer.train()

# =========================
# 9. 평가
# =========================

results = trainer.evaluate()

print(results)