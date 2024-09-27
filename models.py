from pydantic import BaseModel


class ChatRequest(BaseModel):
    userId: str
    websearch: str
    message: str

class SearchRequest(BaseModel):
    userId: str
    searchType: str
    serviceType: str
    location: str
    radius: str

class AIRequest(BaseModel):
    userId: str
    content: str

class HistoryRequest(BaseModel):
    userId: str