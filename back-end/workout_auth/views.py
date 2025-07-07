from django.contrib.auth import get_user_model
from rest_framework import generics, status, viewsets
from rest_framework.decorators import action
from rest_framework.exceptions import AuthenticationFailed, ValidationError
from rest_framework.permissions import AllowAny
from rest_framework.request import Request
from rest_framework.response import Response
from rest_framework_simplejwt.authentication import JWTAuthentication
from rest_framework_simplejwt.exceptions import TokenError
from rest_framework_simplejwt.serializers import TokenObtainPairSerializer
from rest_framework_simplejwt.tokens import RefreshToken, Token
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
        username = request.data.get("username")
        password = request.data.get("password")

        if not username or not password:
            return Response(
                {
                    "message": "Username and password are required",
                },
                status.HTTP_406_NOT_ACCEPTABLE,
            )

        User = get_user_model()  # noqa: N806

        if User.objects.get(username=username, password=password):
            return self._login_existing_user(username, password)

        user_data = self._create_new_user(username, password)

        if user_data.status_code == status.HTTP_201_CREATED:
            return self._login_existing_user(
                user_data.data["access"],  # type: ignore
                user_data.data["refresh"],  # type: ignore
            )

        return user_data

    def _create_new_user(self, username: str, password: str) -> Response:
        """Create a new user.

        Args:
            request (Request): The request object containing user data.

        Returns:
            Response: The response object containing the result of the user creation.
            Response -> {
                "username": str,  # Access token
                "refresh": str,  # Refresh token
                "message": str,  # Success message
            }
        """
        user_data = {"username": username, "password": password}
        serializer = self.get_serializer(data=user_data)
        try:
            serializer.is_valid(raise_exception=True)

            serializer.save()

            return Response(
                {
                    "username": username,
                    "password": password,
                    "message": "User Created Successfully",
                },
                status.HTTP_201_CREATED,
            )
        except ValidationError as error:
            return Response(
                {
                    "message": str(error),
                },
                status.HTTP_400_BAD_REQUEST,
            )
        except Exception as error:  # noqa: BLE001
            return Response(
                {
                    "message": str(error),
                },
                status.HTTP_400_BAD_REQUEST,
            )

    def _login_existing_user(self, username: str, password: str) -> Response:
        """Log in an existing user and return their tokens.

        Args:
            username (str): The username of the user.
            password (str): The password of the user.

        Returns:
            Response: A response containing the user's tokens or an error message.
            Response -> {
                "access": str,  # Access token
                "refresh": str,  # Refresh token
                "message": str,  # Success message
            }
        """
        try:
            token_serializer = TokenObtainPairSerializer(
                data={
                    "username": username,
                    "password": password,
                },
            )
            token_serializer.is_valid(raise_exception=True)
            tokens = token_serializer.validated_data

            return Response(
                {
                    "access": tokens["access"],
                    "refresh": tokens["refresh"],
                    "message": "User Logged Successfully",
                },
                status.HTTP_200_OK,
            )
        except AuthenticationFailed:
            return Response(
                {
                    "message": "Invalid Credentials",
                },
                status.HTTP_401_UNAUTHORIZED,
            )
        except ValidationError as error:
            return Response(
                {
                    "message": str(error),
                },
                status.HTTP_400_BAD_REQUEST,
            )
        except Exception as error:  # noqa: BLE001
            return Response(
                {
                    "message": str(error),
                },
                status.HTTP_400_BAD_REQUEST,
            )


class LoginView(TokenObtainPairView):
    serializer_class = TokenObtainPairSerializer
    permission_classes = [AllowAny]

    def post(self, request: Request) -> Response:
        try:
            token_serializer = TokenObtainPairSerializer(data=request.data)
            token_serializer.is_valid(raise_exception=True)
            tokens = token_serializer.validated_data

            return Response(
                {
                    "access": tokens["access"],
                    "refresh": tokens["refresh"],
                    "message": "User Logged Successfully",
                },
                status.HTTP_200_OK,
            )
        except AuthenticationFailed:
            return Response(
                {
                    "message": "Invalid Credentials",
                },
                status.HTTP_401_UNAUTHORIZED,
            )
        except Exception as error:  # noqa: BLE001
            return Response(
                {
                    "message": str(error),
                },
                status.HTTP_400_BAD_REQUEST,
            )


class LogoutView(generics.GenericAPIView):
    serializer_class = CustomTokenRefreshSerializer
    authentication_classes = [JWTAuthentication]
    permission_classes = [IsUserOrAdmin]

    def post(self, request: Request) -> Response:
        try:
            refresh_token: Token | None = request.data["refresh"]  # type: ignore
            token = RefreshToken(refresh_token)
            if token.check_blacklist():
                return Response(
                    {
                        "message": "Token is already blacklisted",
                    },
                    status.HTTP_409_CONFLICT,
                )
            token.blacklist()

            return Response(
                {
                    "message": "Successfully logged out",
                },
                status.HTTP_200_OK,
            )
        # except KeyError:
        #     return Response(
        #         {
        #             "message": "Refresh token is required",
        #         },
        #         status.HTTP_400_BAD_REQUEST,
        #     )
        except TokenError:
            return Response(
                {
                    "message": "Token is invalid or expired",
                },
                status.HTTP_406_NOT_ACCEPTABLE,
            )
        except Exception as error:  # noqa: BLE001
            return Response(
                {
                    "message": str(error),
                },
                status.HTTP_400_BAD_REQUEST,
            )
