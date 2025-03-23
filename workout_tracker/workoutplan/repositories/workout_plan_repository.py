from typing import Any

from django.contrib.auth.models import AbstractBaseUser, User
from django.db.models.manager import BaseManager

from common.exceptions import (
    ExerciseDoesntExistException,
    NoStatusPlansException,
    NoWorkoutsInPlanException,
    PlanDoesnExistException,
    UserDoesnExistException,
    UserIsntOwnerException,
)
from workoutplan.models import Exercise, Workout, WorkoutPlan


class WorkoutPlanRepository:
    @staticmethod
    def create(**kwargs: Any) -> WorkoutPlan:  # noqa: ANN401
        return WorkoutPlan.objects.create(**kwargs)

    # Searching
    @staticmethod
    def get_all(
        user: User | AbstractBaseUser | None = None,
    ) -> BaseManager[WorkoutPlan]:
        if user:
            UserRepository.user_exist(user.pk)
            return WorkoutPlan.objects.filter(user=user)
        return WorkoutPlan.objects.all()

    @staticmethod
    def get_workoutplan(
        pk: int,
        user: User | AbstractBaseUser,
    ) -> WorkoutPlan:
        WorkoutPlanRepository.workoutplan_exist(pk)
        WorkoutPlanRepository.is_user_owner(user, pk)
        return WorkoutPlan.objects.filter(user=user).get(pk=pk)

    @staticmethod
    def filter_by_status(
        status: str,
        user: User | AbstractBaseUser,
    ) -> BaseManager[WorkoutPlan]:
        if not WorkoutPlan.objects.filter(user=user, status=status).exists():
            raise NoStatusPlansException

        return WorkoutPlanRepository.get_all(user).filter(status=status)

    # Validations
    @staticmethod
    def workoutplan_exist(workoutplan_pk: int) -> None:
        try:
            WorkoutPlan.objects.get(pk=workoutplan_pk)
        except WorkoutPlan.DoesNotExist as error:
            raise PlanDoesnExistException from error

    @staticmethod
    def is_user_owner(user: User | AbstractBaseUser, workout_plan_pk: int) -> None:
        WorkoutPlanRepository.workoutplan_exist(workout_plan_pk)
        try:
            WorkoutPlan.objects.get(pk=workout_plan_pk, user=user)
        except WorkoutPlan.DoesNotExist as error:
            raise UserIsntOwnerException from error


class WorkoutRepository:
    @staticmethod
    def get_workouts_ended(
        user: User | AbstractBaseUser,
    ) -> BaseManager[Workout]:
        workout_plans = WorkoutPlanRepository.filter_by_status(
            status="ENDED",
            user=user,
        )
        return WorkoutRepository.filter_by_plan(workout_plans)

    @staticmethod
    def filter_by_plan(workout_plan: BaseManager[WorkoutPlan]) -> BaseManager[Workout]:
        workouts = Workout.objects.filter(workout_plans__in=workout_plan)
        if not workouts.exists():
            raise NoWorkoutsInPlanException
        return workouts

    @staticmethod
    def filter_by_exercise(
        pk: int,
    ) -> BaseManager[Workout]:
        ExerciseRepository.exercise_exist(pk)
        return Workout.objects.filter(exercise=pk)


class ExerciseRepository:
    @staticmethod
    def exercise_exist(pk: int) -> None:
        try:
            Exercise.objects.get(pk=pk)
        except Exercise.DoesNotExist as error:
            raise ExerciseDoesntExistException from error


class UserRepository:
    @staticmethod
    def user_exist(pk: int) -> None:
        try:
            User.objects.get(pk=pk)
        except User.DoesNotExist as error:
            raise UserDoesnExistException from error
