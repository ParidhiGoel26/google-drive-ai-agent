from fastapi import APIRouter
from app.models.schemas import ChatRequest
from app.agents.graph import agent

router = APIRouter()


@router.post("/chat")
async def chat(req: ChatRequest):

    try:

        result = agent.invoke({
            "user_input": req.message
        })

        return result

    except Exception as e:

        return {
            "error": str(e)
        }