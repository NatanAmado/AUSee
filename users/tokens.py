# users/tokens.py

from django.contrib.auth.tokens import PasswordResetTokenGenerator
import six

class AccountActivationTokenGenerator(PasswordResetTokenGenerator):
    def _make_hash_value(self, user, timestamp):
        """
        Create a hash value that includes the user's primary key, timestamp, and email.
        This ensures the token is unique to the user and doesn't change unless the user's
        email or active status changes.
        """
        return (
            six.text_type(user.pk) + 
            six.text_type(timestamp) + 
            six.text_type(user.is_active) +
            six.text_type(user.email)
        )

account_activation_token = AccountActivationTokenGenerator()
