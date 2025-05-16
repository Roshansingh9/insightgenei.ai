from fastapi import FastAPI, Query
from src.index import result
from fastapi.middleware.cors import CORSMiddleware

app = FastAPI()


# Add CORS middleware to allow requests from your frontend
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],  # In production, replace with specific origins
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)


@app.get("/")
async def root():
    return {"message": "Hello World"}

@app.get("/query")
async def handle_query(text: str = Query(..., description="Your natural language query")):
    return result(text)

if __name__ == "__main__":
    import uvicorn
    uvicorn.run("app.main:app", host="0.0.0.0", port=10000, reload=True)
