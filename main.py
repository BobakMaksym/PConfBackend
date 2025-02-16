from fastapi import FastAPI
import uvicorn


app = FastAPI()


@app.get("/")
def home():
    return "hello"


if __name__ == "__main__":
    uvicorn.run(app="main:app", host="localhost", port=8000, reload=True)
