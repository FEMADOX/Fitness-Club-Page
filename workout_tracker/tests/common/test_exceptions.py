# noqa: INP001
from unittest.mock import MagicMock

import pytest
from django.db.models.manager import BaseManager

from common.exceptions import (
    ExerciseDoesntExistException,
    KwargIntException,  # noqa: F401
    NoStatusPlansException,
    NoWorkoutsInPlanException,
    NoWorkoutsWithExerciseException,
    PlanDoesntExistException,
    UserDoesnExistException,  # noqa: F401
    UserIsntOwnerException,  # noqa: F401
)
from tests.workoutplan.repositories.test_workout_plan_repository import logger
from workoutplan.models import Exercise, Workout, WorkoutPlan
from workoutplan.repositories.workout_plan_repository import (
    ExerciseRepository,
    UserRepository,  # noqa: F401
    WorkoutPlanRepository,
    WorkoutRepository,  # noqa: F401
)

# Optimized exception tests


@pytest.mark.django_db
@pytest.mark.parametrize(
    ("mock_method", "exception", "repository_method", "args"),
    [
        # Exercise Doesnt Exist Test
        (
            # Mock Method
            lambda: MagicMock(side_effect=Exercise.DoesNotExist),
            # Exception
            ExerciseDoesntExistException,
            # Repository Method
            ExerciseRepository.exercise_exist,
            # Args
            {"pk": 1},
        ),
        # No Status Plans Test
        (
            # Mock Method
            lambda: MagicMock(
                return_value=MagicMock(exists=MagicMock(return_value=False)),
            ),
            # Exception
            NoStatusPlansException,
            # Repository Method
            WorkoutPlanRepository.filter_by_status,
            # Args
            {"status": "ACTIVE", "user": MagicMock()},
        ),
        # No Workouts in Plan Test
        (
            # Mock Method
            lambda: MagicMock(
                return_value=MagicMock(exists=MagicMock(return_value=False)),
            ),
            # Exception
            NoWorkoutsInPlanException,
            # Repository Method
            WorkoutRepository.filter_by_plan,
            # Args
            {"workout_plan": MagicMock(spec=BaseManager[WorkoutPlan()])},
        ),
        # No Workouts with Exercise Test
        (
            # Mock Method
            lambda: MagicMock(side_effect=NoWorkoutsWithExerciseException),
            # Exception
            NoWorkoutsWithExerciseException,
            # Repository Method
            WorkoutRepository.filter_by_exercise,
            # Args
            {"pk": 1},
        ),
        # Plan Doesnt Exist Test
        (
            # Mock Method
            lambda: MagicMock(side_effect=PlanDoesntExistException),
            # Exception
            PlanDoesntExistException,
            # Repository Method
            WorkoutPlanRepository.get_workoutplan,
            # Args
            {"pk": 1, "user": MagicMock()},
        ),
    ],
)
def test_exceptions(mock_method, exception, repository_method, args) -> None:  # noqa: ANN001
    # Mock the required method
    if "Exercise" in repository_method.__qualname__:
        Exercise.objects.get = mock_method()
    elif "WorkoutPlan" in repository_method.__qualname__:
        if repository_method.__name__ == "filter_by_status":
            WorkoutPlan.objects.filter = mock_method()
        elif repository_method.__name__ == "get_workoutplan":
            WorkoutPlan.objects.filter().get = mock_method()
    elif "Workout" in repository_method.__qualname__:
        if repository_method.__name__ == "filter_by_plan":
            Workout.objects.filter = mock_method()
        elif repository_method.__name__ == "filter_by_exercise":
            Exercise.objects.get = MagicMock(return_value=MagicMock(spec=Exercise))
            # Exercise.objects.get = mock_method()
            Workout.objects.filter = MagicMock

    # Assert the exception is raised
    with pytest.raises(exception):
        repository_method(**args)

    logger.info(f"The exception {exception.__name__} raises correctly")
