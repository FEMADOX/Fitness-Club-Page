from django.urls import include, path
from rest_framework.routers import DefaultRouter

from workoutplan.views import WorkoutPlanViewSet

router = DefaultRouter()

router.register(r"workoutplan", WorkoutPlanViewSet, "workoutplan")

urlpatterns = [
    path("", include(router.urls)),
]
