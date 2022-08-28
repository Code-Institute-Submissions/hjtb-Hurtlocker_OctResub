from django.http import HttpResponse


class Stripe_Webhook_Handler:
    """
    Handle webhooks from Stripe
    """

    def __init__(self, request):
        self.request = request

    def handle_event(self, event):
        """
        Handle random webhook events
        """
        return HttpResponse(
            content=f"Unexpected webhook received: {event['type']}", status=200
        )

    def payment_success(self, event):
        """
        A view to handle payment success
        """
