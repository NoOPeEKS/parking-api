import uvicorn
from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware

from routes import event, parking, historic, list_parkings

app = FastAPI()
app.include_router(event.router)
app.include_router(parking.router)
app.include_router(historic.router)
app.include_router(list_parkings.router)


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
    return {"message": "API Working"}


if __name__ == "__main__":
    uvicorn.run("main:app", host="0.0.0.0", port=8080, reload=True)
