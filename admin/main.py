from fastapi import FastAPI

app = FastAPI(title="Bot Admin Panel API")


@app.get("/")
async def read_root():
    return {"status": "ok", "message": "Admin panel is running."}



