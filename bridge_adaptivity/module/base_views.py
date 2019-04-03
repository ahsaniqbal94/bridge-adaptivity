"""
Base views for models.
"""
# coding: utf-8
import logging

from module.mixins.views import BackURLMixin, OnlyMyObjectsMixin
from module.models import Collection, CollectionOrder, ModuleGroup

log = logging.getLogger(__name__)


class BaseGetFormKwargs(OnlyMyObjectsMixin, BackURLMixin):
    """
    Base class for get form kwargs by self.model parameter.
    """

    def get_form_kwargs(self):
        kwargs = super().get_form_kwargs()
        model_field_names = [f.name for f in self.model._meta.fields]
        filtered_get = {key: value for key, value in self.request.GET.items() if key in model_field_names}
        if filtered_get and not self.request.POST:
            kwargs['initial'] = filtered_get
        return kwargs


class BaseModuleGroupView(BaseGetFormKwargs):
    """
    Base view for Group (Module).
    """

    slug_url_kwarg = 'group_slug'
    slug_field = 'slug'
    model = ModuleGroup


class BaseCollectionView(OnlyMyObjectsMixin, BackURLMixin):
    """
    Base view for Collection.
    """

    fields = ['name', 'slug', 'metadata', 'owner']
    slug_url_kwarg = 'slug'
    slug_field = 'slug'
    model = Collection
    ordering = ['id']

    def get_avaliable_resources(self, qs):
        result_query = qs.filter(**{self.owner_field: self.request.user})
        result_query = result_query.union(qs.filter(collection_groups__owner=self.request.user))
        result_query = result_query.union(qs.filter(collection_groups__contributors=self.request.user))
        return result_query.distinct()


class BaseCollectionOrderView(BaseGetFormKwargs):
    """
    Base view for CollectionOrder.
    """

    model = CollectionOrder
    ordering = ['group', 'order']
