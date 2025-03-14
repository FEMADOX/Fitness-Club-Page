from django.contrib.auth.models import AbstractBaseUser, User
from django.db.models.manager import BaseManager

from workoutplan.models import WorkoutPlan


class WorkoutPlanRepository:
    @staticmethod
    def get_all(
        user: User | AbstractBaseUser | None = None,
    ) -> BaseManager[WorkoutPlan]:
        if user:
            return WorkoutPlan.objects.filter(user=user)
        return WorkoutPlan.objects.all()

    @staticmethod
    def get_workoutplan(
        workoutplan_pk: int,
        user: User | AbstractBaseUser,
    ) -> WorkoutPlan:
        return WorkoutPlan.objects.filter(user=user).get(pk=workoutplan_pk)

    @staticmethod
    def create(**kwargs: dict) -> WorkoutPlan:
        return WorkoutPlan.objects.create(**kwargs)

    @staticmethod
    def filter_by_status(
        status: str,
        user: User | AbstractBaseUser,
    ) -> BaseManager[WorkoutPlan]:
        return WorkoutPlanRepository.get_all(user).filter(status=status)

    @staticmethod
    def workoutplan_exist(workoutplan_pk: int) -> bool:
        try:
            WorkoutPlan.objects.get(pk=workoutplan_pk)
            return True
        except WorkoutPlan.DoesNotExist:
            return False

    @staticmethod
    def is_user_owner(user: User | AbstractBaseUser, workoutplan_pk: int) -> bool:
        if user.workoutplan_set.filter(pk=workoutplan_pk).exists():  # type: ignore[]
            return True
        return isinstance(user, User) and user.is_staff
