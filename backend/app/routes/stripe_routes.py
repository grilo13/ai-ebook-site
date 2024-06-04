from fastapi import APIRouter, Request, HTTPException, Header
from backend.app.schemas.schemas import CreateEbook
from backend.app.stripe.stripe_handler import StripeHandler

stripe_handler = StripeHandler()

router = APIRouter(tags=['stripe_routes'])


@router.post("/create-checkout-session-sell")
async def create_checkout_session_sell(payload: CreateEbook):
    try:
        checkout_session = stripe_handler.create_checkout_session(topic=payload.topic,
                                                                  target_audience=payload.target_audience)
        print(checkout_session)
        print("checkout session redirect url", checkout_session.url)
        return {'redirect_url': checkout_session.url}
    except Exception as e:
        print(e)
        raise HTTPException(status_code=400, detail=str(e))


@router.post("/stripe_webhooks")
async def webhook(event: dict,
                  request: Request,
                  stripe_signature=Header(None)):
    try:
        payload = await request.body()
        return stripe_handler.handle_webhook(event, stripe_signature, payload)
    except Exception as e:
        print("Error", str(e))
        raise HTTPException(status_code=400, detail=str(e))
