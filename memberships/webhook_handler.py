from django.conf import settings
from django.http import HttpResponse
from django.shortcuts import get_object_or_404
from django.views.decorators.csrf import csrf_exempt
from django.views.decorators.http import require_POST
from django.core.mail import send_mail
from django.template.loader import render_to_string
from datetime import datetime
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


    def _new_subscription_email(self, email_data):
        """
        Send an email when a subscription is created
        """

        user_email = email_data['email']
        subject = render_to_string(
            'memberships/new_subscription_email/new_subscription_email_subject.txt',
            {'email_data': email_data})
        body = render_to_string(
            'memberships/new_subscription_email/new_subscription_email_body.txt',
            {'email_data': email_data,
             'contact_email': settings.DEFAULT_FROM_EMAIL})

        send_mail(subject, body, settings.DEFAULT_FROM_EMAIL, [user_email])


    def handle_checkout_complete(self, event):
        """
        Update the customers with subscription_id
        """

        session = event['data']['object']
        client_reference_id = session.client_reference_id
        subscription = session.subscription
        customer = session.customer

        try:
            current_profile = get_object_or_404(
                Profile, user_id=client_reference_id)
            stripe.api_key = settings.STRIPE_SECRET_KEY
        except Exception as e:
            print(e)
            return HttpResponse(content=e, status=400)

        current_profile.stripe_customer_id = customer
        current_profile.stripe_subscription_id = subscription

        try:
            current_profile.save()
            email_data = {
                'first_name': current_profile.first_name,
                'email': current_profile.email,
                'customer': customer,
                'subscription': subscription,
            }
            self._new_subscription_email(email_data)
        except Exception as e:
            print(e)
            return HttpResponse(content=e, status=400)

        print(f"{current_profile.user} just subscribed.")
        return HttpResponse(content=f"""
        Webhook received: {event['type']}
        """, status=200)


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
        Handle invoice.payment_succeeded webhook from stripe
        """

        session = event['data']['object']
        customer = session.customer
        customer_email = session.customer_email
        subscription = session.subscription
        last_payment = datetime.fromtimestamp(
            session.created).strftime("%H:%M:%S, %d %B %Y")
        try:
            current_profile = get_object_or_404(
                Profile, email=customer_email)
            stripe.api_key = settings.STRIPE_SECRET_KEY
        except Exception as e:
            print(e)
            return HttpResponse(content=e, status=400) 

        current_profile.is_subscribed = True
        current_profile.stripe_customer_id = customer
        current_profile.stripe_subscription_id = subscription

        try:
            current_profile.save()

            email_data = {
                'first_name': current_profile.first_name,
                'email': current_profile.email,
                'last_payment': last_payment,
            }
            self._payment_success_email(email_data)

        except Exception as e:
            print(e)
            return HttpResponse(content=e, status=400)
        print(f"{current_profile.user} just subscribed.")
        return HttpResponse(content=f"""
        Webhook received: {event['type']}
        """, status=200)


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
            'memberships/new_subscription_email/new_subscription_email_subject.txt',
            {'email_data': email_data})
        body = render_to_string(
            'memberships/new_subscription_email/new_subscription_email_body.txt',
            {'email_data': email_data,
             'contact_email': settings.DEFAULT_FROM_EMAIL})

        send_mail(subject, body, settings.DEFAULT_FROM_EMAIL, [user_email])


    def handle_subscription_updated(self, event):
        """
        A view to handle subscription updates
        """
        session = event['data']['object']
        customer = stripe.Customer.retrieve(session.customer)
        customer_email = customer.email
        subscription = session.id

        try:
            current_profile = get_object_or_404(
                Profile, email=customer_email
                )
            stripe.api_key = settings.STRIPE_SECRET_KEY

        except Exception as e:
            print(e)
            return HttpResponse(
                content=f'Webhook received: {event["type"]}.\
                    Profile or subscription does not exist', status=404)

        if session.canceled_at:
            cancelled_seconds = session.canceled_at
            cancelled_date = datetime.fromtimestamp(
                cancelled_seconds).strftime("%d %B %Y")
            subscription_end_seconds = session.current_period_end
            subscription_end_date = datetime.fromtimestamp(
                subscription_end_seconds).strftime("%d %B %Y")

            current_profile.subscription_end = subscription_end_seconds
            current_profile.stripe_customer_id = customer
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

            except Exception as e:
                print(e)
                return HttpResponse(
                    content=f"""
                    Webhook received: {event["type"]} error: {e}
                    """, status=400)

        else:
            subscription_end_seconds = session.current_period_end
            subscription_end_date = datetime.fromtimestamp(
                subscription_end_seconds).strftime("%d %B %Y")
            current_profile.is_subscribed = True
            current_profile.subscription_end = subscription_end_seconds
            current_profile.stripe_customer_id = customer
            current_profile.stripe_subscription_id = subscription

            try:
                current_profile.save()
                email_data = {
                    'first_name': current_profile.first_name,
                    'email': current_profile.email,
                }

                self._renewed_subscription_email(email_data)
                return HttpResponse(
                    content=f"""Webhook received: {event['type']},
                    {subscription} renewed""", status=200
                )

            except Exception as e:
                print(e)
                return HttpResponse(
                    content=f"""
                    Webhook received: {event["type"]} error: {e}
                    """, status=400)


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
        last_payment = datetime.fromtimestamp(
            session.created).strftime("%H:%M:%S, %d %B %Y")
        customer_portal_url = settings.STRIPE_CUSTOMER_PORTAL_URL
        try:
            current_profile = get_object_or_404(Profile, email=customer_email)
            current_profile.is_subscribed = False
            current_profile.save()
            email_data = {
                'first_name': current_profile.first_name,
                'email': current_profile.email,
                'last_payment': last_payment,
                'customer_portal_url': customer_portal_url,
            }

            self._payment_failed_email(email_data)
            return HttpResponse(
                content=f'Webhook received: {event["type"]}.\
                    User access suspended', status=200)

        except Exception as e:
            print(e)
            return HttpResponse(
                content=f"""
                Webhook received: {event["type"]} error: {e}
                """, status=400)

