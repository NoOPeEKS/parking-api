import uvicorn
from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware

# from app.routes import chat, index

app = FastAPI()
# app.include_router(index.router)
# app.include_router(chat.router)


app.add_middleware(
    CORSMiddleware,
    {
        "allow_origins": "*",
        "allow_credentials": True,
        "allow_methods": "*",
        "allow_headers": "*",
    },
)


@app.get("/")
def read_root():
    return {"message": "hola"}


if __name__ == "__main__":
    uvicorn.run("app.main:app", host="0.0.0.0", port=80, reload=True)
