from fastapi import FastAPI, Query
from index import result

app = FastAPI()

@app.get("/")
async def root():
    return {"message": "Hello World"}

@app.get("/query")
async def handle_query(text: str = Query(..., description="Your natural language query")):
    return result(text)

if __name__ == "__main__":
    import uvicorn
    uvicorn.run("app.main:app", host="0.0.0.0", port=10000, reload=True)
