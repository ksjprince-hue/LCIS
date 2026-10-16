from modules.model_config import get_codebert_model_path
from transformers import (
    AutoTokenizer,
    AutoModelForSequenceClassification
)

import torch

MODEL_NAME = get_codebert_model_path("./results/checkpoint-6000")

# tokenizer
tokenizer = AutoTokenizer.from_pretrained(MODEL_NAME)

# classification model
model = AutoModelForSequenceClassification.from_pretrained(
    MODEL_NAME
)

# 테스트 코드
code = """
#include <stdio.h>

int main() {
    char password[4];

    scanf("%s", password);

    return 0;
}
"""

# tokenize
inputs = tokenizer(
    code,
    return_tensors="pt",
    truncation=True,
    padding=True,
    max_length=512
)

# prediction
with torch.no_grad():

    outputs = model(**inputs)

# logits
logits = outputs.logits

# softmax
probs = torch.softmax(logits, dim=-1)

prediction = torch.argmax(probs, dim=-1)

print("=== Prediction Result ===")

print("Prediction:", prediction.item())

print("Confidence:", probs.max().item())

print("Logits:", logits)

print("Probabilities:", probs)
