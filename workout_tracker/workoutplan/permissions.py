from django.contrib.auth import get_user_model
from django.contrib.auth.models import User
from rest_framework.permissions import BasePermission
from rest_framework.request import Request
from rest_framework.views import APIView


class IsUserOrAdmin(BasePermission):
    def has_permission(self, request: Request, view: APIView) -> bool:
        try:
            user = get_user_model().objects.get(pk=request.user.pk)
            user_id = view.kwargs.get("pk")

            if not user_id:
                return user.is_staff

            return bool(
                (user.is_authenticated and user.pk == int(user_id))
                or user.is_staff,
            )
        except User.DoesNotExist:
            return False
        except ValueError:
            return False
