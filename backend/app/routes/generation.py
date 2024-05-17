from fastapi import APIRouter, Request
from fastapi.responses import HTMLResponse

router = APIRouter(tags=['generation'])


# GET endpoint
@router.get("/form", response_class=HTMLResponse)
async def load_form(request: Request):
    return 200
