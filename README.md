# L-CIS (Local Code Intelligence System)

> AI 기반 Python 코드 분석 시스템 — 구조 분석 · 위험도 판단 · 설명 생성

![Python](https://img.shields.io/badge/Python-3.14-blue)
![FastAPI](https://img.shields.io/badge/FastAPI-0.1.0-green)
![Status](https://img.shields.io/badge/Status-In%20Development-orange)

## 프로젝트 개요

Python 코드를 입력받아 AST 구조 분석, AI 위험도 판단, LLM 설명 생성까지
하나의 파이프라인으로 처리하는 End-to-End 코드 분석 시스템입니다.

## 기술 스택

| 분야 | 기술 |
|---|---|
| Backend | FastAPI, Uvicorn |
| AI/ML | PyTorch, HuggingFace (CodeBERT) |
| LLM | Ollama |
| Vector DB | ChromaDB |
| Parsing | Python AST, tree-sitter |
| Frontend | Streamlit |

## 구현 현황

| 기능 | 상태 |
|---|---|
| FastAPI 서버 기본 구조 | ✅ 완료 |
| AST 코드 구조 분석 | 🔄 진행 예정 |
| PyTorch 위험도 모델 | 🔄 진행 예정 |
| CodeBERT Transformer 분석 | 🔄 진행 예정 |
| Attention 시각화 (XAI) | 🔄 진행 예정 |
| LLM 코드 설명 생성 | 🔄 진행 예정 |
| RAG 파이프라인 | 🔄 진행 예정 |
| Streamlit UI | 🔄 진행 예정 |

## 시스템 아키텍처
```
코드 입력 → AST 분석 → PyTorch 위험도 판단
→ CodeBERT 의미 분석 → LLM 설명 생성
→ RAG 근거 보강 → Attention 시각화 → 결과 출력
```

## 개발 일지

[DEVLOG.md](./DEVLOG.md) 참고
