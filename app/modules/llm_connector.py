import requests
# requests: HTTP 요청 보내는 라이브러리
# Ollama 서버(11434 포트)한테 POST 요청 보낼 때 사용

from modules.ast_analyzer import ASTResult

# Ollama 서버 주소
OLLAMA_URL = "http://localhost:11434/api/generate"
MODEL_NAME = "deepseek-coder:1.3b"  # 나중에 더 큰 모델로 바꿀 때 여기만 수정


def build_prompt(source_code: str, ast_result: ASTResult) -> str:
    """
    AST 분석 결과 + 원본 코드를 프롬프트로 가공하는 함수

    """

    # AST 결과에서 주요 정보 추출
    imports = ", ".join(ast_result.imports) if ast_result.imports else "없음"
    func_names = ", ".join(f.name for f in ast_result.functions) if ast_result.functions else "없음"
    complexity = ast_result.complexity_score

    # 프롬프트 조립
    prompt = f"""당신은 보안 코드 분석 전문가입니다. 아래 파이썬 코드를 한국어로 분석하세요.
      

[분석 데이터]
- 임포트: {imports}
- 함수 목록: {func_names}
- 복잡도 점수: {complexity}

[소스 코드]
{source_code}

반드시 한국어로 답변해주세요.
다음 내용을 포함해주세요:
1. 보안 취약점 (있는 경우)
2. 리팩토링 제안
3. 간단한 설명

간결하고 구체적으로 작성해주세요."""

    return prompt


def analyze_with_llm(source_code: str, ast_result: ASTResult) -> dict:
    """
    LLM 분석 실행하는 메인 함수
    성공하면 → {"success": True, "response": "LLM 답변"}
    실패하면 → {"success": False, "error": "에러 메시지"}
    """

    prompt = build_prompt(source_code, ast_result)

    try:
        response = requests.post(
            OLLAMA_URL,
            json={
                "model": MODEL_NAME,
                "prompt": prompt,
                "stream": False,  # 스트리밍 없이 한 번에 응답 받기
            },
            timeout=300  # 로컬 LLM이 느릴 수 있어서 2분 여유
        )

        if response.status_code == 200:
            # Ollama 응답 형태: {"response": "LLM 답변 텍스트", ...}
            data = response.json()
            return {
                "success": True,
                "response": data["response"]
            }
        else:
            return {
                "success": False,
                "error": f"Ollama 서버 오류: {response.status_code}"
            }

    except requests.exceptions.ConnectionError:
        # Ollama 서버가 꺼져있을 때
        return {
            "success": False,
            "error": "Ollama 서버에 연결할 수 없어요. Ollama가 실행 중인지 확인해주세요."
        }
    except requests.exceptions.Timeout:
        # 응답이 너무 오래 걸릴 때
        return {
            "success": False,
            "error": "응답 시간이 초과됐어요. 모델이 너무 느린 것 같아요."
        }
