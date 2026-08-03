from fastapi import FastAPI

app = FastAPI(title="Lorica API", docs_url="/", redoc_url=None)

if __name__ == "__main__":
    import uvicorn

    uvicorn.run(app, port=5000)
