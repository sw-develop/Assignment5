from django.urls import path

from research.views import ResearchRetrieveView, SearchResearchView, RecentListView

urlpatterns = [
    path('/recent', RecentListView.as_view(), name='recent'),
    path('/<str:number>', ResearchRetrieveView.as_view(), name='detail'),
    path('', SearchResearchView.as_view(), name='search-research'),
]