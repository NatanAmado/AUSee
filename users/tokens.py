# users/tokens.py

import six
import hashlib
import time
from datetime import datetime, timedelta
from django.conf import settings

class SimpleTokenGenerator:
    """
    A simpler token generator that doesn't rely on Django's PasswordResetTokenGenerator.
    This should be more reliable across different environments.
    """
    # Token validity period in days
    TOKEN_VALIDITY_DAYS = 7
    
    def make_token(self, user):
        """
        Generate a token for the given user that expires after TOKEN_VALIDITY_DAYS.
        """
        # Current timestamp in seconds
        timestamp = int(time.time())
        
        # Create a hash using user info and a secret key
        hash_string = (
            str(user.pk) + 
            str(user.username) + 
            str(timestamp) + 
            settings.SECRET_KEY
        )
        
        # Create a SHA256 hash
        token_hash = hashlib.sha256(hash_string.encode('utf-8')).hexdigest()
        
        # Return timestamp and hash combined
        return f"{timestamp}-{token_hash[:20]}"
    
    def check_token(self, user, token):
        """
        Check if the token is valid for the given user.
        """
        try:
            # Split token into timestamp and hash
            timestamp_str, hash_part = token.split('-')
            timestamp = int(timestamp_str)
            
            # Check if token has expired
            current_time = int(time.time())
            if current_time - timestamp > self.TOKEN_VALIDITY_DAYS * 24 * 60 * 60:
                return False
            
            # Recreate the hash for verification
            hash_string = (
                str(user.pk) + 
                str(user.username) + 
                str(timestamp) + 
                settings.SECRET_KEY
            )
            
            # Create a SHA256 hash
            token_hash = hashlib.sha256(hash_string.encode('utf-8')).hexdigest()
            
            # Compare the first 20 chars of the hash
            return token_hash[:20] == hash_part
        except (ValueError, TypeError, AttributeError):
            return False
        
    def __str__(self):
        return f"SimpleTokenGenerator(validity={self.TOKEN_VALIDITY_DAYS} days)"

# Create an instance of the token generator
account_activation_token = SimpleTokenGenerator()
