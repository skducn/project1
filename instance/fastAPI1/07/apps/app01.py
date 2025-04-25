from fastapi import APIRouter

app01 = APIRouter()

@app01.get("/user/{id}")
def get_user(id: int):
    return {"user_id": id}

