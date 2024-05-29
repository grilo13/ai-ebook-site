import json

import stripe
from backend.app.core.config import settings


class StripeHandler:
    def __init__(self):
        self.STRIPE_API_SECRET = settings.STRIPE_API_SECRET
        # This is your Stripe CLI webhook secret for testing your endpoint locally.
        self.STRIPE_ENDPOINT_SECRET = settings.STRIPE_ENDPOINT_SECRET
        stripe.api_key = self.STRIPE_API_SECRET
        self.FRONTEND_URL = settings.FRONTEND_URL

    def create_checkout_session(self, topic: str, target_audience: str):
        product = stripe.Product.create(
            name=(
                f"E-Book with topic: '{topic}' for target audience:"
                f" '{target_audience}'"
            ),
        )
        print(product.id)
        unit_amount = 99
        price = stripe.Price.create(
            unit_amount=unit_amount,
            currency="usd",
            product=product.id,
            metadata={
                "topic": topic,
                "target_audience": target_audience,
                # "sell": sell,
            },
        )

        checkout_session = stripe.checkout.Session.create(
            line_items=[
                {
                    # Provide the exact Price ID (for example, pr_1234) of the product you want to sell
                    "price": price.id,
                    "quantity": 1,
                },
            ],
            mode="payment",
            success_url=self.FRONTEND_URL + "/success",
            cancel_url=self.FRONTEND_URL + "?canceled",
        )

        # Save these identifiers
        print(f"Success! Here is your product price id: {product.id}")
        print("price", price.values())
        print("checkout session", checkout_session)

    def handle_webhook(self, event, stripe_signature, payload):
        print("webhook for fulfill order")
        event = None
        print("payload", payload)
        print("stripe signature", stripe_signature)

        try:
            event = stripe.Webhook.construct_event(
                payload, stripe_signature, self.STRIPE_ENDPOINT_SECRET
            )
        except ValueError as e:
            # Invalid payload
            raise e
        except stripe.error.SignatureVerificationError as e:
            # Invalid signature
            raise e

        print("event type", event['type'])
        # Handle the event
        if event['type'] == 'checkout.session.completed':
            payload_eval = json.loads(payload.decode("utf-8"))
            print("payload_eval", payload_eval)
            customer_email = payload_eval["data"]["object"]["customer_details"]["email"]
            print("customer_email", customer_email)

            # Retrieve the session. If you require line items in the response, you may include them
            # by expanding line_items.
            session = stripe.checkout.Session.retrieve(
                event['data']['object']['id'],
                expand=['line_items'],
            )

            line_items = session.line_items
            print("line items", line_items)
            # Fulfill the purchase...
            for line_item in line_items:
                self.fulfill_order(line_item, customer_email)

        return {'success': True}

    def fulfill_order(self, line_item, recipient_email: str):
        # TODO: fill me in with the creation of the ebook
        print("Fulfilling order")
        print("email", recipient_email)


if __name__ == '__main__':
    stripe_handler = StripeHandler()
    stripe_handler.create_checkout_session(topic="teste", target_audience="test")
