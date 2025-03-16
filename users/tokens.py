# users/tokens.py

from django.contrib.auth.tokens import PasswordResetTokenGenerator
import six
from datetime import datetime

class AccountActivationTokenGenerator(PasswordResetTokenGenerator):
    # Override key_salt to use a custom salt for this specific token
    key_salt = "ausee.account.activation.token"
    
    # Set a longer timeout (7 days instead of the default 3)
    # This is in seconds: 7 days * 24 hours * 60 minutes * 60 seconds
    token_timeout = 7 * 24 * 60 * 60
    
    def _make_hash_value(self, user, timestamp):
        """
        Create a hash value that includes the user's primary key, timestamp, and email.
        This ensures the token is unique to the user and doesn't change unless the user's
        email or active status changes.
        
        We're using a more stable approach by removing the is_active field from the hash
        since that's what we're changing during activation.
        """
        # Use username instead of email for more stability
        login_timestamp = '' if user.last_login is None else user.last_login.replace(microsecond=0, tzinfo=None).timestamp()
        return (
            six.text_type(user.pk) + 
            six.text_type(timestamp) + 
            six.text_type(user.username) +
            six.text_type(login_timestamp)
        )

account_activation_token = AccountActivationTokenGenerator()
