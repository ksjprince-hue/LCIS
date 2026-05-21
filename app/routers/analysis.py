from fastapi import APIRouter, HTTPException
from modules.ast_analyzer import ASTAnalyzer, FunctionData, ClassData
from modules.llm_connector import analyze_with_llm
from models.schemas import AnalyzeRequest, AnalyzeResponse, FunctionInfo, ClassInfo

# APIRouter: FastAPI 앱을 기능별로 분리하는 도구
# prefix="/analysis" → 이 파일의 모든 엔드포인트는 /analysis/ 로 시작
# tags=["analysis"]  → Swagger UI에서 그룹으로 묶여서 표시됨
router = APIRouter(prefix="/analysis", tags=["analysis"])

# 서버 시작할 때 한 번만 생성(메모리 낭비 방지)
analyzer = ASTAnalyzer()


def _to_function_info(f: FunctionData) -> FunctionInfo:
    """
    내부 dataclass → 응답용 Pydantic 스키마 변환
    ast_analyzer 내부에서 쓰던 FunctionData를
    클라이언트한테 보낼 FunctionInfo 형태로 바꿔요
    """
    return FunctionInfo(
        name=f.name,
        lineno=f.lineno,
        args=f.args,
        is_async=f.is_async,
        complexity=f.complexity,
    )


# @router.post: POST 요청을 받는 엔드포인트 정의
# "/ast": URL 경로 → 실제 주소는 /analysis/ast
# response_model: 응답 형태를 AnalyzeResponse로 강제
@router.post("/ast", response_model=AnalyzeResponse)
async def analyze_ast(req: AnalyzeRequest):
    """
    POST /analysis/ast
    요청: { "source_code": "...", "filename": "test.py" }
    응답: AST 분석 결과 JSON
    """

    if not req.source_code.strip():
        # HTTPException: HTTP 에러 반환하는 방법
        # 400: Bad Request → 클라이언트가 잘못 보낸 요청
        raise HTTPException(status_code=400, detail="source_code가 비어있어요")

    # 분석 실행
    ast_result = analyzer.analyze(req.source_code)

    # AST 결과 + 원본 코드를 LLM한테 전달
    llm_result = analyze_with_llm(req.source_code, ast_result)

    # ASTResult → AnalyzeResponse 변환해서 반환
    return AnalyzeResponse(
        filename=req.filename,
        total_lines=ast_result.total_lines,
        complexity_score=ast_result.complexity_score,
        functions=[_to_function_info(f) for f in ast_result.functions],
        classes=[
            ClassInfo(
                name=c.name,
                lineno=c.lineno,
                bases=c.bases,
                methods=[_to_function_info(m) for m in c.methods],
            )
            for c in ast_result.classes
        ],
        imports=ast_result.imports,
        errors=ast_result.errors,
        # LLM 결과 추가
        llm_analysis=llm_result["response"] if llm_result["success"] else "",
        llm_error=llm_result["error"] if not llm_result["success"] else "",
    )