from fastapi import FastAPI
from app.routes import users

app = FastAPI()  # ✅ Change 'route' to 'app'

app.include_router(users.router)

@app.get("/")
def home():
    return {"message": "Welcome to FastAPI Auth"}

if __name__ == "__main__":
    import uvicorn

    uvicorn.run("main:app", host="0.0.0.0", port=2345)