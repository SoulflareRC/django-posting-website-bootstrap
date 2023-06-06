from allauth.account.views import *
from allauth.account.urls import urlpatterns
from allauth.account.forms import SignupForm
from allauth.account.adapter import DefaultAccountAdapter
from allauth.socialaccount.adapter import DefaultSocialAccountAdapter
from allauth.account.models import EmailAddress
from allauth.socialaccount.models import SocialLogin
class MySocialAccountAdapter(DefaultSocialAccountAdapter):
    def pre_social_login(self, request, sociallogin):
        print("Hello from the social account adapter!")
        print(sociallogin)
        # social account already exists, so this is just a login
        if sociallogin.is_existing:
            print("Social account already exists")
            return

        # some social logins don't have an email address
        if not sociallogin.email_addresses:
            print("Social account doesn't have an email address")
            return

        # find the first verified email that we get from this sociallogin
        verified_email = None
        for email in sociallogin.email_addresses:
            print(type(email))
            print([f.name for f in EmailAddress._meta.get_fields()])
            print(email.email,email.verified,email.id)
            if email.verified:
                verified_email = email
                break

        # no verified emails found, nothing more to do
        if not verified_email:
            if 'email' not in sociallogin.account.extra_data:
                return

                # check if given email address already exists.
                # Note: __iexact is used to ignore cases
            try:
                email = sociallogin.account.extra_data['email'].lower()
                print("Email from extra data:",email)
                email_address = EmailAddress.objects.get(email__iexact=email)
                print(email_address.user,email_address.id,email_address.verified,email_address.email)
                # if it does not, let allauth take care of this new social account
                email = email_address
            except EmailAddress.DoesNotExist:
                return

        # check if given email address already exists as a verified email on
        # an existing user's account
        try:
            existing_email = EmailAddress.objects.get(email__iexact=email.email, verified=True)
        except EmailAddress.DoesNotExist:
            print("Email address doesn't exist!")
            return

        # if it does, connect this new social login to the existing user
        sociallogin.connect(request, existing_email.user)
