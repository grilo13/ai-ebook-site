from fastapi import APIRouter, Request, HTTPException, Header
from fastapi.responses import HTMLResponse
from starlette.responses import JSONResponse
from backend.app.schemas.schemas import CreateEbook
import random
import time
from backend.app.runner import Runner
from backend.app.stripe.stripe_handler import StripeHandler

router = APIRouter(tags=['generation'])

stripe_handler = StripeHandler()

tasks = {}


def update_task_status(id, status, url=None):
    tasks[id] = {"status": status, "url": url}


# GET endpoint
@router.get("/form", response_class=HTMLResponse)
async def load_form(request: Request):
    return 200


@router.post("/create_ebook_preview", response_class=JSONResponse)
async def create_ebook_preview(payload: CreateEbook):
    print("creating ebook preview")

    id = str(random.getrandbits(32)) + str(time.time())
    print("identifier", id)
    tasks[id] = {"status": "processing", "url": None}

    Runner().create_ebook(
        topic=payload.topic,
        target_audience=payload.target_audience,
        # recipient_email='pedromv1317@gmail.com',
        preview=True,
        sell=False,
        callback=update_task_status,
        id=id
    )

    try:
        return {'id': id}
    except Exception as err:
        raise HTTPException(status_code=400, detail=err.__str__())


@router.post("/stripe_webhooks")
async def webhook(event: dict,
                  request: Request,
                  stripe_signature=Header(None)):
    try:
        payload = await request.body()
        return stripe_handler.handle_webhook(event, stripe_signature, payload), 200
    except Exception as e:
        print("Error", str(e))
        return {"error": str(e)}, 400


@router.get("/check_ebook_status/{id:str}", response_class=JSONResponse)
async def check_ebook_status(id: str):
    task = tasks.get(id)
    print("task", task)
    if task and task["status"] == "completed":
        return {"status": task.get("status"), "file_url": task.get("url")}
    return {"error": "Ebook not ready yet"}


@router.get("/get_pdf/{id:str}")
async def get_pdf(id: str):
    task = tasks.get(id)
    if task and task["status"] == "completed":
        print("returning file url", task.get('url'))
        return {"file_url": task.get('url')}
    return {"error": "PDF not ready"}
