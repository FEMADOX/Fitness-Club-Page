from django.contrib.auth import get_user_model
from rest_framework import generics, status, viewsets
from rest_framework.decorators import action
from rest_framework.permissions import AllowAny
from rest_framework.request import Request
from rest_framework.response import Response
from rest_framework_simplejwt.authentication import JWTAuthentication
from rest_framework_simplejwt.exceptions import TokenError
from rest_framework_simplejwt.serializers import TokenObtainPairSerializer
from rest_framework_simplejwt.tokens import RefreshToken
from rest_framework_simplejwt.views import TokenObtainPairView

from common.permissions import IsUserOrAdmin
from workout_auth.serializers import CustomTokenRefreshSerializer, UserSerializer
from workoutplan.services.workout_plan_service import WorkoutPlanService


class UserViewSet(viewsets.ModelViewSet):
    queryset = get_user_model().objects.all()
    serializer_class = UserSerializer
    authentication_classes = [JWTAuthentication]
    permission_classes = [IsUserOrAdmin]

    @action(methods=["get"], detail=False, url_path="generate-workouts-report")
    def generate_user_report(self, request: Request) -> Response:
        user = get_user_model().objects.get(pk=request.user.pk)

        report = WorkoutPlanService.generate_plans_report(user)

        return Response(report, status=status.HTTP_200_OK)

    @action(
        methods=["get"],
        detail=False,
        url_path=r"exercise-progress/(?P<exercise_id>\d+)",
    )
    def user_exercise_progress(
        self,
        request: Request,
        exercise_id: int,
    ) -> Response:
        user = get_user_model().objects.get(pk=request.user.pk)

        response = WorkoutPlanService.get_exercise_progress(
            user,
            exercise_id,
        )

        return Response(response, status=status.HTTP_200_OK)


class SignUpView(generics.CreateAPIView):
    queryset = get_user_model().objects.all()
    serializer_class = UserSerializer
    permission_classes = [AllowAny]

    def post(self, request: Request) -> Response:
        serializer = self.get_serializer(data=request.data)
        serializer.is_valid(raise_exception=True)

        user = serializer.save()
        return Response(
            {
                "user": UserSerializer(user).data,
                "message": "User Created Successfully",
            },
            status.HTTP_201_CREATED,
        )


class LoginView(TokenObtainPairView):
    serializer_class = TokenObtainPairSerializer
    permission_classes = [AllowAny]


class LogoutView(generics.GenericAPIView):
    serializer_class = CustomTokenRefreshSerializer
    authentication_classes = [JWTAuthentication]
    permission_classes = [IsUserOrAdmin]

    def post(self, request: Request) -> Response:
        try:
            refresh_token = request.data["refresh"]
            token = RefreshToken(refresh_token)
            token.blacklist()

            return Response(
                {
                    "message": "Successfully logged out",
                },
                status.HTTP_200_OK,
            )
        except KeyError:
            return Response(
                {
                    "message": "Refresh token is required",
                },
                status.HTTP_400_BAD_REQUEST,
            )
        except TokenError:
            return Response(
                {
                    "message": "Token is invalid or expired",
                },
                status.HTTP_400_BAD_REQUEST,
            )
