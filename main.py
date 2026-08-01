from fastapi import FastAPI

app = FastAPI(title="Lorica API")


@app.get("/")
async def hello():
    return {"message": "Hello, World!"}
