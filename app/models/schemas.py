from pydantic import BaseModel

# ── Pydantic이란? ─────────────────────────────────────────
# FastAPI가 데이터 검증에 사용하는 라이브러리예요.
# BaseModel을 상속받으면 타입이 안 맞을 때 자동으로 에러를 내줘요.
# 예: source_code에 숫자를 넣으면 자동으로 400 에러 반환

class AnalyzeRequest(BaseModel):
    """클라이언트 → FastAPI 로 보내는 요청 형태"""
    source_code: str
    filename: str = "unknown.py"  # 기본값 설정


class FunctionInfo(BaseModel):
    """함수 하나의 분석 결과"""
    name: str
    lineno: int       # line number: 몇 번째 줄에 있는지
    args: list[str]   # 인자 목록 예: ["a", "b"]
    is_async: bool    # async def인지 여부
    complexity: int   # 복잡도 점수


class ClassInfo(BaseModel):
    """클래스 하나의 분석 결과"""
    name: str
    lineno: int
    bases: list[str]             # 상속받는 클래스 예: ["BaseModel"]
    methods: list[FunctionInfo]  # 클래스 안의 메서드들


class AnalyzeResponse(BaseModel):
    """FastAPI → 클라이언트 로 돌려주는 응답 형태"""
    filename: str
    total_lines: int
    complexity_score: int        # 전체 함수 복잡도 합산
    functions: list[FunctionInfo]
    classes: list[ClassInfo]
    imports: list[str]
    errors: list[str]
    llm_analysis: str = ""   # LLM 분석 결과 텍스트
    llm_error: str = ""      # LLM 오류 메시지 (있을 때만)