# L-CIS (Local Code Intelligence System)

Transformer 기반 AI 코드 취약점 분석 시스템

---

## Overview

L-CIS는 C/C++ 및 Python 코드를 분석하여 취약 가능성을 탐지하고, AI 기반 코드 이해 및 설명 기능을 제공하는 로컬 기반 코드 인텔리전스 프로젝트입니다.

본 프로젝트에서는:

* TF-IDF 기반 Baseline 모델 구축
* CodeBERT Transformer Fine-tuning
* PyTorch 기반 학습 파이프라인 구현
* HuggingFace Trainer 활용
* AST 기반 코드 구조 분석
* Local LLM(Ollama) 기반 코드 설명 생성

등을 직접 구현하며 Transformer 기반 코드 분석 및 inference pipeline을 실험했습니다.

---

## Tech Stack

| 분야            | 기술                         |
| ------------- | -------------------------- |
| Language      | Python                     |
| Deep Learning | PyTorch                    |
| Transformer   | CodeBERT                   |
| LLM Framework | HuggingFace Transformers   |
| Local LLM     | Ollama                     |
| ML Baseline   | scikit-learn               |
| Parsing       | Python AST                 |
| Backend       | FastAPI                    |
| Frontend      | Streamlit                  |
| Vector DB     | ChromaDB                   |
| Dataset       | CodeXGLUE Defect Detection |

---

## System Pipeline

Code Input
→ AST Structure Analysis
→ Transformer Semantic Analysis (CodeBERT)
→ Vulnerability Prediction
→ Local LLM Explanation
→ Result Visualization

TF-IDF baseline model used for comparison experiments

---

## Implemented Features

| Feature                        | Status |
| ------------------------------ | ------ |
| TF-IDF Baseline Model          | ✅      |
| CodeBERT Fine-tuning           | ✅      |
| HuggingFace Trainer Pipeline   | ✅      |
| Vulnerability Classification   | ✅      |
| F1 / Accuracy Evaluation       | ✅      |
| Inference Prediction           | ✅      |
| AST Analysis (Python)          | ✅      |
| Local LLM Integration (Ollama) | ✅      |
| Streamlit UI                   | ✅      |
| FastAPI Backend                | ✅      |
| RAG Pipeline                   | 🔄     |
| CFG / DFG Structural Analysis  | 🔄     |
| Attention Visualization (XAI)  | 🔄     |

---

## AI/Transformer Training

### Baseline Model

* TF-IDF Vectorization
* Logistic Regression
* scikit-learn 기반 분류 모델

### Transformer Model

* microsoft/codebert-base
* HuggingFace Trainer 기반 Fine-tuning
* Sequence Classification 방식 적용

Pipeline:
Code → Tokenizer → Embedding → Transformer → Classification

---

## Training Result

| Model                | F1 Score | Environment           |
| -------------------- | -------- | --------------------  | 
| TF-IDF Baseline      | 0.53     | CPU                   |
| CodeBERT (Best Validation Checkpoint) | 0.63     | CPU subset fine-tuning |

Additional large-scale GPU fine-tuning and structural analysis integration are planned for future improvements.

Notes
* Fine-tuning performed using PyTorch and HuggingFace Transformers
* Validation-based checkpoint evaluation applied
* Best performance observed around checkpoint-6000
* Additional GPU-based large-scale training planned

## Inference Example

Input Code:

```c
char buf[10];
strcpy(buf, input);
```

Prediction:

* Vulnerable Code
* Confidence Score: 0.50

---

## Key Learnings

본 프로젝트를 통해 다음과 같은 경험을 수행했습니다.

* Transformer 기반 코드 임베딩 이해
* HuggingFace 기반 Fine-tuning 경험
* Tokenization / Embedding / Logits / Loss 분석
* PyTorch 기반 학습 및 평가 파이프라인 구현
* Baseline ML 모델과 Transformer 모델 성능 비교
* 코드 분석 AI 시스템 구조 설계 경험
* Local LLM 기반 코드 설명 생성 경험

---

## Dataset

### CodeXGLUE Defect Detection

* C/C++ 함수 단위 취약점 데이터셋
* Vulnerability Label (0 / 1) 제공
* CodeBERT Fine-tuning 학습에 활용

Dataset:
https://huggingface.co/datasets/google/code_x_glue_cc_defect_detection

---

## Future Improvements

* GPU 기반 Full Fine-tuning
* CFG / DFG 기반 구조 분석
* tree-sitter 기반 다중 언어 AST 지원
* RAG 기반 취약점 근거 검색
* Attention Visualization 기반 Explainable AI

---

## Author

GitHub:
https://github.com/ksjprince-hue/LCIS
