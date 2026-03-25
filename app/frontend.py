import streamlit as st
import requests

# st.set_page_config: 브라우저 탭 제목이랑 아이콘 설정
st.set_page_config(page_title="L-CIS", page_icon="🔍")

# st.title: 화면 제일 위에 큰 제목 표시
st.title("🔍 L-CIS")
st.caption("Local Code Intelligence System")

# st.text_area: 여러 줄 입력창
# height: 입력창 높이 (픽셀)
code = st.text_area("분석할 코드를 입력하세요", height=300)

# st.button: 버튼
# 버튼 클릭하면 if 블록 실행
if st.button("분석 시작"):

    # 코드가 비어있으면 경고
    if not code.strip():
        st.warning("코드를 입력해주세요!")

    else:
        # FastAPI 서버로 POST 요청
        # requests.post: HTTP POST 요청을 보내는 함수
        # json 파라미터: 딕셔너리를 자동으로 JSON으로 변환해서 전송
        try:
            response = requests.post(
                "http://127.0.0.1:8000/analysis/ast",
                json={
                    "source_code": code,
                    "filename": "uploaded.py"
                }
            )

            # 응답 성공 (200)
            if response.status_code == 200:
                result = response.json()  # JSON 응답 → Python 딕셔너리 변환

                st.success("분석 완료!")

                # 기본 정보
                col1, col2 = st.columns(2)  # 화면을 2칸으로 나눔
                col1.metric("전체 라인 수", result["total_lines"])
                col2.metric("전체 복잡도", result["complexity_score"])

                # import 목록
                if result["imports"]:
                    st.subheader("📦 Import 목록")
                    st.write(result["imports"])

                # 함수 목록
                if result["functions"]:
                    st.subheader("⚙️ 함수 목록")
                    for func in result["functions"]:
                        st.write(f"**{func['name']}()** - {func['lineno']}번째 줄 / 복잡도: {func['complexity']}")

                # 클래스 목록
                if result["classes"]:
                    st.subheader("🏗️ 클래스 목록")
                    for cls in result["classes"]:
                        st.write(f"**{cls['name']}** - {cls['lineno']}번째 줄")
                        for method in cls["methods"]:
                            st.write(f"　└ {method['name']}() / 복잡도: {method['complexity']}")

                # 에러
                if result["errors"]:
                    st.subheader("❌ 에러")
                    for err in result["errors"]:
                        st.error(err)

            else:
                st.error(f"서버 오류: {response.status_code}")

            if response.status_code == 200:
                result = response.json()
                if result.get("llm_error"):
                    st.error(f"LLM 분석 오류: {result['llm_error']}")
                elif result.get("llm_analysis"):
                    st.subheader("🤖 LLM 분석 결과")
                    st.write(result["llm_analysis"])
        except requests.exceptions.ConnectionError:
            # FastAPI 서버가 꺼져있을 때
            st.error("FastAPI 서버에 연결할 수 없어요. 서버가 실행 중인지 확인해주세요!")
            