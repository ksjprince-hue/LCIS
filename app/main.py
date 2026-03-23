from fastapi import FastAPI
from routers.analysis import router as analysis_router

app = FastAPI(
    title="L-CIS",
    description="Local Code Intelligence System",
    version="0.1.0"
)

# include_router: 만들어둔 라우터를 메인 앱에 등록
# 이렇게 분리하는 이유:
# 나중에 routers/llm.py, routers/rag.py 추가할 때
# main.py는 여기 한 줄만 추가하면 돼요
app.include_router(analysis_router)


@app.get("/")
def root():
    return {"message": "L-CIS 서버 작동 중"}

@app.get("/health")
def health_check():
    return {"status": "ok"}