from rest_framework import mixins, viewsets, filters

from .permissions import IsAdminIsSuperuser


class CustomViewSetMixin(
    mixins.CreateModelMixin, mixins.ListModelMixin,
    mixins.DestroyModelMixin, viewsets.GenericViewSet
):
    """Кастомный миксин для ViewSet c Create, List, Destroy методами."""

    permission_classes = [IsAdminIsSuperuser]
    filter_backends = [filters.SearchFilter]
    search_fields = ['name']
    lookup_field = 'slug'
