from fastapi import APIRouter


router = APIRouter(prefix="/api/private")


@router.get("/capabilities")
def capabilities() -> dict[str, list[str]]:
    return {
        "capabilities": [
            "search",
            "ask",
            "citations",
            "local-ingestion",
            "document-management",
        ]
    }
