import torch
import torch.nn.functional as F

from transformers import (
    AutoTokenizer,
    AutoModelForSequenceClassification
)

# =========================
# 1. 저장된 모델 불러오기
# =========================

MODEL_PATH = "./results/checkpoint-1125"

tokenizer = AutoTokenizer.from_pretrained(MODEL_PATH)

model = AutoModelForSequenceClassification.from_pretrained(MODEL_PATH)

model.eval()

# =========================
# 2. 테스트 코드 입력
# =========================

code = """
char buffer[10];
strcpy(buffer, input);
"""

# =========================
# 3. Tokenize
# =========================

inputs = tokenizer(
    code,
    return_tensors="pt",
    truncation=True,
    padding="max_length",
    max_length=128
)

# =========================
# 4. 모델 예측
# =========================

with torch.no_grad():

    outputs = model(**inputs)

# logits 추출
logits = outputs.logits

# softmax 확률 변환
probs = F.softmax(logits, dim=-1)

# 가장 높은 클래스 선택
pred_class = torch.argmax(probs, dim=-1).item()

# 확률 값
confidence = probs[0][pred_class].item()

# =========================
# 5. 결과 출력
# =========================

print("\n=== Code Vulnerability Prediction ===\n")

print(code)

print("-" * 50)

if pred_class == 1:
    print("Prediction : Vulnerable Code")
else:
    print("Prediction : Safe Code")

print(f"Confidence : {confidence:.2%}")