# noqa: INP001
import logging
from collections.abc import Callable
from typing import Any
from unittest.mock import MagicMock

import pytest
from django.contrib.auth.models import User

from workoutplan.models import Workout, WorkoutPlan
from workoutplan.repositories.workout_plan_repository import WorkoutPlanRepository

logger = logging.getLogger(__name__)


class TestWorkoutPlanRepository:
    def setup_method(self, method: Callable[..., Any]) -> None:
        logger.info("Test setup %s", method)

    def teardown_method(self, method: Callable[..., Any]) -> None:
        logger.info("Test teardown %s", method)
        assert User.objects.count() == 1

    @pytest.mark.django_db
    def test_class(self, user_fixture: User) -> None:
        user = User.objects.get(username="testuser")
        assert user == user_fixture


# @pytest.fixture
# def mock_user(db) -> User:  # noqa: ANN001, ARG001
#     return User.objects.create(username="testuser", password="testpassword")
# user = MagicMock(spect=User)
# user.pk = 1
# user.username = "testuser"
# user.password = "testpassword"
# return user


# @pytest.fixture
# def workout_plan_fixture(db) -> WorkoutPlan:  # noqa: ANN001, ARG001
#     return WorkoutPlan.objects.create(
#         pk=1,
#         user=User.objects.create(username="testuser", password="testpassword"),
#     )
# workout_plan = MagicMock(spec=WorkoutPlan)
# workout_plan.pk = 1
# workout_plan.workouts = MagicMock()


# @pytest.fixture
# def workout_fixture(db) -> list[MagicMock]:  # noqa: ANN001, ARG001
#     return [MagicMock(spec=Workout, pk=index) for index in range(1, 4)]


# @pytest.fixture
# def mock_exercise() -> MagicMock:
#     return MagicMock(spec=Exercise)


# @pytest.mark.django_db
@pytest.mark.skip
def test_create_user() -> None:
    user = User.objects.create(username="testuser", password="testpassword")
    assert user.pk is not None


# @pytest.mark.skip
@pytest.mark.django_db
def test_create_workout_plan(
    user_fixture: User,
    workout_fixture: Workout,
) -> None:
    WorkoutPlan.objects.create = MagicMock(return_value=MagicMock(spec=WorkoutPlan))
    Workout.objects.bulk_create = MagicMock()
    workout_plan = WorkoutPlanRepository.create(
        kwargs={
            "user": user_fixture,
            "workouts": workout_fixture,
            "schedule_date": None,
            "status": "ACTIVE",
        },
    )
    assert workout_plan is not None
    logger.info("Workout Plan create %s", workout_plan)
    WorkoutPlan.objects.create.assert_called_once()
    Workout.objects.bulk_create.assert_called_once_with(workout_fixture)


@pytest.mark.django_db
def test_update_workout_plan(
    workout_plan_fixture: WorkoutPlan,
    workout_fixture: Workout,
    workouts_fixture: list[Workout],
) -> None:
    Workout.objects.bulk_create = MagicMock()
    workout_plan_fixture.workouts.clear = MagicMock()
    workout_plan_fixture.workouts.add = MagicMock()
    workout_plan_fixture.save = MagicMock()

    updated_plan = WorkoutPlanRepository.update(
        workout_plan=workout_plan_fixture,
        workouts=workouts_fixture,
        schedule_date=None,
        status=None,
    )

    assert updated_plan is not None
    logger.info("Updated Workout Plan %s", updated_plan)
    workout_plan_fixture.workouts.clear.assert_called_once()
    workout_plan_fixture.workouts.add.assert_called_once_with(workout_fixture)
    workout_plan_fixture.save.assert_called_once()


@pytest.mark.django_db
def test_partial_update_workout_plan(
    workout_plan_fixture: WorkoutPlan,
    workouts_fixture: list[Workout],
) -> None:
    Workout.objects.bulk_create = MagicMock()
    workout_plan_fixture.workouts.clear = MagicMock()
    workout_plan_fixture.workouts.add = MagicMock()
    workout_plan_fixture.save = MagicMock()

    updated_plan = WorkoutPlanRepository.partial_update(
        workout_plan=workout_plan_fixture,
        workouts=workouts_fixture,
        schedule_date=None,
        status=None,
    )

    assert updated_plan is not None
    logger.info("Partial Updated Workout Plan %s", updated_plan)
    workout_plan_fixture.workouts.clear.assert_called_once()
    workout_plan_fixture.workouts.add.assert_called_once()
    workout_plan_fixture.save.assert_called_once()


@pytest.mark.django_db
def test_filter_by_status(user_fixture: User) -> None:
    WorkoutPlan.objects.filter = MagicMock(return_value=MagicMock())
    WorkoutPlanRepository.get_all = MagicMock(return_value=MagicMock())

    workout_plans = WorkoutPlanRepository.filter_by_status(
        status="ACTIVE",
        user=user_fixture,
    )

    assert workout_plans is not None
    logger.info("Workout plans filter by status %s", workout_plans)

    WorkoutPlan.objects.filter.assert_called_once_with(
        user=user_fixture,
        status="ACTIVE",
    )


@pytest.mark.skip
def test_get_workoutplan(user_fixture: User) -> None:
    WorkoutPlan.objects.filter = MagicMock(return_value=MagicMock())
    WorkoutPlan.objects.filter().get = MagicMock(
        return_value=MagicMock(spec=WorkoutPlan),
    )

    workout_plan = WorkoutPlanRepository.get_workoutplan(pk=1, user=user_fixture)

    assert workout_plan is not None
    logger.info("Getting the Workout Plan %s", workout_plan)
    WorkoutPlan.objects.filter.assert_called_once_with(user=user_fixture)
    WorkoutPlan.objects.filter().get.assert_called_once_with(pk=1)
