from fastapi import FastAPI

app = FastAPI(
    title="L-CIS",
    description="Local Code Intelligence System",
    version="0.1.0"
)

@app.get("/")
def root():
    return {"message": "L-CIS 서버 작동 중"}

@app.get("/health")
def health_check():
    return {"status": "ok"}
