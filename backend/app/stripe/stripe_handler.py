import stripe
from backend.app.core.config import settings


class StripeHandler:
    def __init__(self):
        self.STRIPE_API_SECRET = settings.STRIPE_API_SECRET
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


if __name__ == '__main__':
    stripe_handler = StripeHandler()
    stripe_handler.create_checkout_session(topic="teste", target_audience="test")