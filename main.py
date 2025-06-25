from fastapi import FastAPI, HTTPException, Request
from pydantic import BaseModel
from auth import authenticate_user
from rag import get_answer

app = FastAPI()

class LoginRequest(BaseModel):
    email: str
    password: str

class QueryRequest(BaseModel):
    query: str
    role: str
    
@app.get("/")
async def root():
    return {"message": "✅ FinSolve RAG Chatbot backend is up and running!"}
    
@app.post("/login")
def login(payload: LoginRequest):
    user = authenticate_user(payload.email, payload.password)
    if not user:
        raise HTTPException(status_code=401, detail="Invalid credentials")
    return user

@app.post("/query")
def query(payload: QueryRequest):
    answer, sources = get_answer(payload.query, payload.role)
    return {"answer": answer, "sources": sources}
