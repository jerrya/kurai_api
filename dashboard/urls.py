from django.urls import path
from rest_framework.urlpatterns import format_suffix_patterns
from dashboard import views

urlpatterns = [
    # path('get/', views.RetrieveEvents.as_view()),
]

urlpatterns = format_suffix_patterns(urlpatterns)
