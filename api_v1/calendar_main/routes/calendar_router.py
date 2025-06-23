# api_v1/calendar_main/routes/calendar_router.py
from rest_framework.routers import DefaultRouter

from api_v1.calendar_main.controllers.calendar import (
    EventController, # Changed from EventControler to EventController (typo fixed)
    EventTypeController,
    DepartmentController,
    ContactController,
    AdditionalObservationController,
)

router = DefaultRouter()
router.register(r'events', EventController, basename='event')
router.register(r'event-types', EventTypeController, basename='event-type')
router.register(r'departments', DepartmentController, basename='department')
router.register(r'contacts', ContactController, basename='contact')
router.register(r'additional-observations', AdditionalObservationController, basename='additional-observation')

urlpatterns = router.urls