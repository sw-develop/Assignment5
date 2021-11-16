from django_filters.rest_framework  import DjangoFilterBackend
from rest_framework.filters         import OrderingFilter, SearchFilter
from rest_framework.generics        import RetrieveAPIView, ListAPIView

from research.models    import ResearchInformation
from .filters           import ResearchFilter
from .serializers       import ResearchInformationSerializer


class ResearchRetrieveView(RetrieveAPIView):
    queryset            = ResearchInformation.objects.all()
    serializer_class    = ResearchInformationSerializer
    lookup_field        = 'number'


class SearchResearchView(ListAPIView):
    queryset            = ResearchInformation.objects.all()
    serializer_class    = ResearchInformationSerializer
    filter_backends     = [DjangoFilterBackend, OrderingFilter, SearchFilter]
    filterset_class     = ResearchFilter
    ordering            = ['-updated_at']
    search_fields       = ['name', 'number', 'range', 'code', 'institute', 'stage', 'office']
