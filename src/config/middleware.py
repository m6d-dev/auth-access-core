from django.utils.deprecation import MiddlewareMixin
from src.apps.accounts.services import user_session_service
from django.utils import timezone
from django.contrib.auth.models import AnonymousUser


class SessionAuthenticationMiddleware(MiddlewareMixin):
    def process_request(self, request):
        session_id = request.COOKIES.get("sessionid")
        user = None
        is_authenticated = False

        if session_id:
            session_dto = user_session_service._repository.model.objects.filter(
                {"session_id": session_id}
            ).first()

            if (
                session_dto
                and session_dto.is_active
                and session_dto.expires_at > timezone.now()
            ):
                user = session_dto.user
                is_authenticated = True

        request.user = user or AnonymousUser()
        request.user.is_authenticated = is_authenticated
