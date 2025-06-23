from django.urls import include, path

urlpatterns = [
    path('api/v1/', include('api_v1.calendar_main.routes.calendar_router')),
]