from django.urls import path, include

from research.views import ResearchRetrieveView

urlpatterns = [
    path('/<str:number>', ResearchRetrieveView.as_view(), name='detail'),
]