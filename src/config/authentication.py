from rest_framework.authentication import BaseAuthentication
from django.utils import timezone
from src.apps.accounts.services import user_session_service


class SessionAuthentication(BaseAuthentication):
    def authenticate(self, request):
        session_id = request.COOKIES.get("sessionid")
        if session_id:
            session = user_session_service._repository.model.objects.filter(
                session_id=session_id
            ).first()

            if session and session.is_active and session.expires_at > timezone.now():
                return (session.user, None)

        return None
