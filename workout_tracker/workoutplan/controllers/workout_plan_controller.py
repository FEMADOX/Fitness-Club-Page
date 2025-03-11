from django.contrib.auth.models import User
from rest_framework import status, viewsets
from rest_framework.permissions import IsAuthenticated
from rest_framework.request import Request
from rest_framework.response import Response
from rest_framework_simplejwt.authentication import JWTAuthentication

from workoutplan.serializers import WorkoutPlanSerializer
from workoutplan.services.workout_plan_service import WorkoutPlanService


class WorkoutPlanViewSet(viewsets.ModelViewSet):
    serializer_class = WorkoutPlanSerializer
    queryset = WorkoutPlanService.get_all_workout_plans()
    authentication_classes = [JWTAuthentication]
    permission_classes = [IsAuthenticated]

    def list(self, request: Request) -> Response:
        status_filter = request.query_params.get("status")
        workout_plans = WorkoutPlanService.get_filtered_workout_plans(status_filter)
        serializer = self.get_serializer(workout_plans, many=True)
        return Response(serializer.data)

    def create(self, request: Request) -> Response:
        data = request.data
        user = request.user

        if isinstance(user, User):
            response = WorkoutPlanService.create_workout_plan(
                data,
                user,
            )

            if response.get("success"):
                return Response(response["message"], status=status.HTTP_201_CREATED)

            return Response(response["message"], status=status.HTTP_400_BAD_REQUEST)

        return Response(
            {"message": "User is not authenticated"},
            status=status.HTTP_401_UNAUTHORIZED,
        )

        # if response.get("success"):
        #     return Response(response["message"], status=status.HTTP_201_CREATED)
        # return Response(response["message"], status=status.HTTP_400_BAD_REQUEST)
