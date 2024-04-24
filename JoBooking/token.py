from django.contrib.auth.tokens import PasswordResetTokenGenerator
from six import text_type
class TokenVerification(PasswordResetTokenGenerator):
    def _make_hash_value(self, user, timestamp):
        return (
                text_type(user.pk) +
                text_type(timestamp) +
                text_type(user.checked_email)

        )
activation_compte = TokenVerification()
