# L-CIS 개발 일지

## 📅 2026-03-18 (Day 1)

### ✅ 오늘 한 것
- Python 3.14 설치 및 환경 세팅
- VSCode 설치 및 프로젝트 폴더 구성
- 가상환경 (lcis-env) 생성
- FastAPI, Uvicorn, Streamlit 패키지 설치
- FastAPI 기본 서버 구현 (`app/main.py`)
- 서버 정상 작동 확인 (`http://127.0.0.1:8000`)
- API 문서 페이지 확인 (`http://127.0.0.1:8000/docs`)
- Git 설치 및 GitHub 저장소 연결
- 첫 커밋 & push 완료

### 🗂️ 현재 프로젝트 구조
```
lcis/
├── lcis-env/          # 가상환경 (GitHub에 올라가지 않음)
└── app/
    ├── routers/       # API 라우터 (예정)
    ├── models/        # AI 모델 (예정)
    ├── services/      # 비즈니스 로직 (예정)
    ├── __init__.py
    └── main.py        # FastAPI 서버 진입점
```

### 🔜 다음에 할 것
- AST 분석 모듈 구현 (`app/services/ast_analyzer.py`)
- Python 코드 입력 → 함수·변수·위험패턴 추출

### 🐛 오늘 만난 문제들
- Python 3.14 최신 버전이라 uvicorn 호환 오류 → 코드 들여쓰기 수정으로 해결
- PowerShell 보안 정책으로 가상환경 활성화 오류 → Command Prompt로 전환해서 해결
- Git push 시 README 충돌 → `--allow-unrelated-histories` 로 해결
- vim 편집기에서 `:wq` 커밋 메시지에 포함되는 해프닝 😅

---

## 📅 2026-03-23 (Day 2)

### ✅ 오늘 한 것
- AST 분석 모듈 구현 (`app/modules/ast_analyzer.py`)
- FastAPI 라우터 연결 (`app/routers/analysis.py`)
- 데이터 스키마 정의 (`app/models/schemas.py`)
- Streamlit 프론트엔드 구현 (`app/frontend.py`)
- 코드 입력 → AST 분석 → 결과 시각화 전체 흐름 완성

### 🗂️ 현재 프로젝트 구조
```
lcis/
└── app/
    ├── models/
    │   └── schemas.py       # 요청/응답 데이터 형태 정의
    ├── modules/
    │   └── ast_analyzer.py  # AST 분석 엔진
    ├── routers/
    │   └── analysis.py      # API 엔드포인트
    ├── frontend.py          # Streamlit UI
    └── main.py
```

### 🔜 다음에 할 것
- 로컬 LLM 연결 (Ollama + DeepSeek-Coder)

### 🐛 오늘 만난 문제들
- 포트 충돌 (이전 uvicorn 프로세스 미종료) → `taskkill /f /im python.exe` 로 해결
- `__init__.py` 누락으로 모듈 import 오류 → 각 폴더에 추가해서 해결
- git push 충돌 → `git pull origin main --rebase` 로 해결

---

## 📅 2026-03-24 (Day 3)

### ✅ 오늘 한 것
- Ollama 설치 및 DeepSeek-Coder 1.3B 모델 다운로드
- 로컬 LLM 연결 모듈 구현 (`app/modules/llm_connector.py`)
- AST 분석 결과 + 원본 코드를 프롬프트로 가공하여 LLM에 전달
- FastAPI 라우터에 LLM 분석 결과 추가 (`app/routers/analysis.py`)
- Streamlit UI에 LLM 분석 결과 표시 (`app/frontend.py`)
- 코드 입력 → AST 분석 → LLM 분석 → 결과 시각화 전체 흐름 완성

### 🗂️ 현재 프로젝트 구조
```
lcis/
└── app/
    ├── models/
    │   └── schemas.py          # 요청/응답 데이터 형태 정의
    ├── modules/
    │   ├── ast_analyzer.py     # AST 분석 엔진
    │   └── llm_connector.py    # 로컬 LLM 연결 모듈
    ├── routers/
    │   └── analysis.py         # API 엔드포인트
    ├── frontend.py             # Streamlit UI
    └── main.py
```

### 🔜 다음에 할 것
- PyTorch Classifier 구현 (코드 위험도 0~1 출력)

### 🐛 오늘 만난 문제들
- `result` 변수명 오타 → `ast_result` 로 통일해서 해결
- `fuctions` 오타 → `functions` 로 수정
- LLM 응답 타임아웃 → timeout 값 120초로 설정
- LLM 한국어 응답 미지원 → 1.3B 모델 한계, 추후 더 큰 모델로 교체 예정
- LLM 결과 표시 코드 들여쓰기 오류 → 위치 수정으로 해결

---