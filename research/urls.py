from django.urls import path, include

from research.views import ResearchRetrieveView, SearchResearchView

urlpatterns = [
    path('/<str:number>', ResearchRetrieveView.as_view(), name='detail'),
    path('', SearchResearchView.as_view(), name='search-research'),
]