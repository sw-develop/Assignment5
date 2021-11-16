from rest_framework.generics import RetrieveAPIView

from research.models import ResearchInformation
from .serializers    import ResearchInformationSerializer


class ResearchRetrieveView(RetrieveAPIView):
    queryset = ResearchInformation.objects.all()
    serializer_class = ResearchInformationSerializer
    lookup_field = 'number'