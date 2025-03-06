# users/tokens.py

from django.contrib.auth.tokens import PasswordResetTokenGenerator

class AccountActivationTokenGenerator(PasswordResetTokenGenerator):
    def _make_hash_value(self, user, timestamp):
        # This method will return a hash value that includes the user's primary key and the timestamp.
        # The hash will change if the user's `is_active` status changes, which will invalidate the token
        # after the account is activated.
        return str(user.pk) + str(timestamp) + str(user.is_active)

account_activation_token = AccountActivationTokenGenerator()
