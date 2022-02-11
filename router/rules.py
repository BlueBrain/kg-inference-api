from fastapi import APIRouter

router = APIRouter()

@router.get("/rules")
async def get_all_rules(name: str):
    pass
