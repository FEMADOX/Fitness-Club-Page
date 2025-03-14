from django.contrib.auth import get_user_model
from rest_framework import status, viewsets
from rest_framework.permissions import IsAuthenticated
from rest_framework.request import Request
from rest_framework.response import Response
from rest_framework_simplejwt.authentication import JWTAuthentication

from workoutplan.exceptions import KwargIntException
from workoutplan.serializers import WorkoutPlanSerializer
from workoutplan.services.workout_plan_service import (
    WorkoutPlanService,
)


class WorkoutPlanViewSet(viewsets.ModelViewSet):
    serializer_class = WorkoutPlanSerializer
    queryset = WorkoutPlanService.get_all_workout_plans()
    authentication_classes = [JWTAuthentication]
    permission_classes = [IsAuthenticated]

    def list(self, request: Request) -> Response:
        user = get_user_model().objects.get(pk=request.user.pk)
        status_filter = request.query_params.get("status")
        workout_plans = WorkoutPlanService.get_all_workout_plans_filtered(
            status_filter,
            user,
        )

        serializer = self.get_serializer(workout_plans, many=True)

        return Response(serializer.data)

    def retrieve(self, request: Request, **kwargs: dict[str, str]) -> Response:
        user = get_user_model().objects.get(pk=request.user.pk)

        try:
            workoutplan_pk = int(kwargs["pk"])  # type: ignore[]
        except ValueError as error:
            raise KwargIntException from error

        response = WorkoutPlanService.user_owner_workoutplan_validation(
            user,
            workoutplan_pk,
        )

        if not response["success"]:
            return Response(response["message"], int(response["status"]))

        workoutplan = WorkoutPlanService.get_workout_plan_of_user(
            user,
            workoutplan_pk,
        )
        serializer = self.get_serializer(workoutplan)

        return Response(data=serializer.data, status=status.HTTP_200_OK)

    def create(self, request: Request) -> Response:
        data = request.data

        # Serializer Validation
        self.get_serializer(data=data).is_valid(raise_exception=True)

        user = get_user_model().objects.get(pk=request.user.pk)

        response = WorkoutPlanService.create_workout_plan(
            data,
            user,
        )

        return Response(response["message"], status=response["status"])
