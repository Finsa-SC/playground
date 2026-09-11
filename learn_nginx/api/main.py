from fastapi import FastAPI

app = FastAPI(title="My First API")


@app.get("/")
def root():
    return {"message": "Hello from FastAPI behind Nginx! 🚀"}


@app.get("/health")
def health():
    return {"status": "ok"}


@app.get("/hello/{name}")
def hello(name: str):
    return {"message": f"Hello, {name}!"}
