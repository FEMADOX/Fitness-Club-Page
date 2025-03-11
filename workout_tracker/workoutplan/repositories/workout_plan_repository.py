from django.contrib.auth.models import User
from django.db.models.manager import BaseManager

from workoutplan.models import WorkoutPlan


class WorkoutPlanRepository:

    @staticmethod
    def get_all() -> BaseManager[WorkoutPlan]:
        return WorkoutPlan.objects.all()

    @staticmethod
    def filter_by_status(status: str) -> BaseManager[WorkoutPlan]:
        return WorkoutPlan.objects.filter(status=status)

    @staticmethod
    def create(**kwargs: dict) -> WorkoutPlan:
        return WorkoutPlan.objects.create(**kwargs)

    @staticmethod
    def get_by_user(user: User) -> BaseManager[WorkoutPlan]:
        return WorkoutPlan.objects.filter(user=user)
