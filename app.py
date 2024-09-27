from fastapi import FastAPI, HTTPException
from fastapi.responses import StreamingResponse
from fastapi.middleware.cors import CORSMiddleware
from models import *
from assistant import *


bots = {}

app = FastAPI()

origins = [
    "http://localhost",
    "http://localhost:3000",
    "http://localhost:3001",
    "http://45.126.3.252:3000",
    "https://hunter-project.vercel.app",
]

headers = {
    "Cache-Control": "no-cache",
    "Content-Type": "text/event-stream",
    "Transfer-Encoding": "chunked",
}

app.add_middleware(
    CORSMiddleware,
    allow_origins=origins,  # List of allowed origins
    allow_credentials=True,
    allow_methods=["*"],  # Allows all methods
    allow_headers=["*"],  # Allows all headers
)


@app.post("/history")
async def get_history(request: HistoryRequest):
    print(request)
    uid = request.userId
    if bots.get(uid) is None:
        bots[uid] = Assistant(uid)

    return bots[uid].history

@app.post("/clear")
async def clear_history(request: HistoryRequest):
    print(request)
    uid = request.userId
    if bots.get(uid) is None:
        bots[uid] = Assistant(uid)

    bots[uid].initialize()
    return {"messaage": "success"}

@app.post("/chat")
async def chat(chat_message: ChatRequest):
    print(chat_message)
    uid = chat_message.userId
    if bots.get(uid) is None:
        bots[uid] = Assistant(uid)

    return StreamingResponse(
        bots[uid].chat(chat_message.message),
        headers=headers
    )

@app.post("/search")
async def chat(request: SearchRequest):
    print(request)
    uid, search_type, service_type, location, radius = request.userId, request.searchType, request.serviceType, request.location, miles_to_kilometers(float(request.radius))
    places = filterPlaces(search_type, service_type)
    search_result = search_place_in_radius(location, radius, places)
    search_result = [] if search_result[0].get("search_result") is not None else search_result
    return search_result

@app.post("/aisearch")
async def chat(request: AIRequest):
    print(request)
    uid,search_content = request.userId, request.content
    if bots.get(uid) is None:
        bots[uid] = Assistant(uid)
    result = bots[uid].aisearch(search_content)
    return result

if __name__ == "__main__":
    import uvicorn
    uvicorn.run(app, host="0.0.0.0", port=8000)