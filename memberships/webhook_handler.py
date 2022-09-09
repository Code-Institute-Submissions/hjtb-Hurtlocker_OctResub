from django.conf import settings
from django.http import HttpResponse
from django.shortcuts import get_object_or_404
from django.views.decorators.csrf import csrf_exempt
from django.views.decorators.http import require_POST
from django.core.mail import send_mail
from django.template.loader import render_to_string
from datetime import datetime as dt
import stripe
from profiles.models import Profile


@require_POST
@csrf_exempt
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


    def _payment_success_email(self, email_data):
        """
        Send an email on successful payment
        """

        user_email = email_data['email']
        subject = render_to_string(
            'memberships/payment_success_email/payment_success_email_subject.txt',
            {'email_data': email_data})
        body = render_to_string(
            'memberships/payment_success_email/payment_success_email_body.txt',
            {'email_data': email_data,
             'contact_email': settings.DEFAULT_FROM_EMAIL})

        send_mail(subject, body, settings.DEFAULT_FROM_EMAIL, [user_email])


    def handle_payment_succeeded(self, event):
        """
        Handle invoice.paid webhook from stripe
        """

        session = event['data']['object']
        customer = session.customer
        customer_email = session.customer_email
        subscription = session.subscription
        last_payment = dt.fromtimestamp(
            session.created).strftime("%H:%M:%S, %d %B %Y")
        try:
            current_profile = get_object_or_404(
                Profile, email=customer_email)
            stripe.api_key = settings.STRIPE_SECRET_KEY
        except Exception as e:

            return HttpResponse(
                content=f"""
                Invoice Paid Webhook received, error retrieving data:
                {event['type']} error: {e}
                """, status=400)

        current_profile.is_subscribed = True
        current_profile.stripe_customer_id = customer
        current_profile.stripe_subscription_id = subscription

        try:
            current_profile.save()

            email_data = {
                'first_name': current_profile.first_name,
                'customer': customer,
                'subscription': subscription,
                'email': current_profile.email,
                'last_payment': last_payment,
            }
            self._payment_success_email(email_data)

        except Exception as e:
            return HttpResponse(
                content=f"""
                Invoice Paid Webhook received: {event['type']} error: {e}
                """, status=400)

        return HttpResponse(content=f"""
        Invoice Paid Webhook received: {event['type']}
        """, status=200)


    def _payment_failed_email(self, email_data):
        """
        send an email when a payment fails
        """

        user_email = email_data['email']
        subject = render_to_string(
            'memberships/payment_failed_email/payment_failed_email_subject.txt',
            {'email_data': email_data})
        body = render_to_string(
            'memberships/payment_failed_email/payment_failed_email_body.txt',
            {'email_data': email_data,
             'contact_email': settings.DEFAULT_FROM_EMAIL})

        send_mail(subject, body, settings.DEFAULT_FROM_EMAIL, [user_email])


    def handle_payment_failed(self, event):
        """
        Remove user access and direct them to the customer portal
        """

        session = event['data']['object']
        customer_email = session.customer_email
        last_payment = dt.fromtimestamp(
            session.created).strftime("%H:%M:%S, %d %B %Y")
        try:
            current_profile = get_object_or_404(Profile, email=customer_email)
            current_profile.is_subscribed = False
            current_profile.save()
            email_data = {
                'first_name': current_profile.first_name,
                'email': current_profile.email,
                'last_payment': last_payment,
            }

            self._payment_failed_email(email_data)
            return HttpResponse(
                content=f"""
                    Payment Failed Webhook received, error retrieving data:
                    {event['type']}. User access suspended
                    """, status=200
                    )

        except Exception as e:
            return HttpResponse(
                content=f"""
                Payment Failed Webhook received: {event['type']} error: {e}
                """, status=400)



    def _membership_deleted_email(self, email_data):
        """
        Send an email on subscription cancellation
        """

        user_email = email_data['email']
        subject = render_to_string(
            'memberships/subscription_ended_email/subscription_ended_email_subject.txt',
            {'email_data': email_data})
        body = render_to_string(
            'memberships/subscription_ended_email/subscription_ended_email_body.txt',
            {'email_data': email_data,
             'contact_email': settings.DEFAULT_FROM_EMAIL})

        send_mail(subject, body, settings.DEFAULT_FROM_EMAIL, [user_email])


    def _renewed_subscription_email(self, email_data):
        """
        Send an email when a subscription is renewed
        """

        user_email = email_data['email']
        subject = render_to_string(
            'memberships/renewed_subscription_email/renewed_subscription_email_subject.txt',
            {'email_data': email_data})
        body = render_to_string(
            'memberships/renewed_subscription_email/renewed_subscription_email_body.txt',
            {'email_data': email_data,
             'contact_email': settings.DEFAULT_FROM_EMAIL})

        send_mail(subject, body, settings.DEFAULT_FROM_EMAIL, [user_email])


    def handle_subscription_updated(self, event):
        """
        A view to handle subscription updates
        """
        now = dt.now()
        timestamp_now = dt.timestamp(now)
        stripe.api_key = settings.STRIPE_SECRET_KEY
        session = event['data']['object']
        try:
            customer = stripe.Customer.retrieve(session.customer)
            customer_email = customer.email
            subscription = session.id
            current_profile = get_object_or_404(
                Profile, email=customer_email
                )

        except Exception as e:
            return HttpResponse(
                content=f"""
                Subscription Update Webhook received, error retrieving data:
                {event['type']} error: {e}
                """, status=400
                )

        if session.canceled_at:
            cancelled_seconds = session.canceled_at
            cancelled_date = dt.fromtimestamp(
                cancelled_seconds).strftime("%d %B %Y")
            subscription_end_seconds = session.current_period_end
            subscription_end_date = dt.fromtimestamp(
                subscription_end_seconds).strftime("%d %B %Y")

            current_profile.subscription_end = subscription_end_seconds
            current_profile.stripe_customer_id = customer.id
            current_profile.stripe_subscription_id = f"""
            [CANCELLED] on {cancelled_date}, id:{subscription}
            """
            try:
                current_profile.save()
                email_data = {
                    'first_name': current_profile.first_name,
                    'email': current_profile.email,
                    'subscription_end': subscription_end_date,
                }

                self._membership_deleted_email(email_data)
                return HttpResponse(
                    content=f"""Webhook received: {event['type']},
                    {subscription} renewed""", status=200
                )
            except Exception as e:
                return HttpResponse(
                    content=f"""
                    Cancellation Webhook received: {event['type']} error: {e}
                    """, status=400)

        elif (timestamp_now - session.start_date) > 60 and session.status == 'active':
            subscription_end_seconds = session.current_period_end
            subscription_end_date = dt.fromtimestamp(
                subscription_end_seconds).strftime("%d %B %Y")
            current_profile.is_subscribed = True
            current_profile.subscription_end = subscription_end_seconds
            current_profile.stripe_customer_id = customer.id
            current_profile.stripe_subscription_id = subscription

            try:
                current_profile.save()
                email_data = {
                    'first_name': current_profile.first_name,
                    'email': current_profile.email,
                    'subscription': subscription,
                    'customer': customer.id,
                }

                self._renewed_subscription_email(email_data)
                return HttpResponse(
                    content=f"""Webhook received: {event['type']},
                    {subscription} renewed""", status=200
                )

            except Exception as e:
                return HttpResponse(
                    content=f"""
                    Webhook received: {event['type']} error: {e}
                    """, status=400)
        else:
            return HttpResponse(content=f"""
            Subscription Update Webhook received: {event['type']}
            """, status=200)
