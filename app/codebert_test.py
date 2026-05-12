from transformers import AutoTokenizer, AutoModel
import torch

# CodeBERT 모델 이름
MODEL_NAME = "microsoft/codebert-base"

# tokenizer 불러오기
tokenizer = AutoTokenizer.from_pretrained(MODEL_NAME)

# 모델 불러오기
model = AutoModel.from_pretrained(MODEL_NAME)

# 테스트용 C 코드
code = """
int main() {
    char buf[10];
    strcpy(buf, input);
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

print("=== Tokenized Input ===")
print(inputs)

# embedding 추출
with torch.no_grad():
    outputs = model(**inputs)

# 마지막 hidden state
embeddings = outputs.last_hidden_state

print("\n=== Embedding Shape ===")
print(embeddings.shape)