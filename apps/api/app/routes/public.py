from fastapi import APIRouter


router = APIRouter(prefix="/api/public")


@router.get("/capabilities")
def capabilities() -> dict[str, list[str]]:
    return {"capabilities": ["search", "ask", "citations"]}
