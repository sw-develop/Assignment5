from django_filters     import rest_framework as filters

from research.models    import ResearchInformation


class ResearchFilter(filters.FilterSet):
    name                = filters.CharFilter(field_name="name", lookup_expr="icontains")
    range               = filters.CharFilter(field_name="range", lookup_expr="icontains")
    code                = filters.CharFilter(field_name="code", lookup_expr="icontains")
    institute           = filters.CharFilter(field_name="institute", lookup_expr="icontains")
    stage               = filters.CharFilter(field_name="stage", lookup_expr="icontains")
    min_target_number   = filters.NumberFilter(field_name="target_number", lookup_expr="gte")
    max_target_number   = filters.NumberFilter(field_name="target_number", lookup_expr="lte")
    office              = filters.CharFilter(field_name="office", lookup_expr="icontains")

    class Meta:
        model = ResearchInformation
        exclude = ('number', 'period', 'created_at', 'updated_at')
