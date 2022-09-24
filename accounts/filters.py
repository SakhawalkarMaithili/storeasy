from pyexpat import model

from attr import field
import django_filters
from django_filters import DateFilter, CharFilter

from .models import *

class OrderFilter (django_filters.FilterSet):
    start_date = DateFilter(field_name='date_created', lookup_expr='gte')
    end_date = DateFilter(field_name='date_created', lookup_expr='lte')
    product_name = CharFilter(field_name='product__name', lookup_expr='icontains')  # even if we right few starting letters, it will search the right word
    class Meta:
        model = Order
        fields = '__all__'
        exclude = ['customer', 'date_created', 'product']       # does not include the fields included in the list, in the displayed form