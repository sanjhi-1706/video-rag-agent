from fastapi import FastAPI

app = FastAPI(title="Video RAG Agent")

@app.get("/")
def root():
    return {"message": "API is running 🚀"}