"""This module builds the filters for the app"""
import django_filters
from django_filters import DateFilter

from .models import *

class OrderFilter(django_filters.FilterSet):
    """builds a filter for the Order model""" 
    start_date = DateFilter(field_name='date_created', lookup_expr='gte') #gte means greater than or equal to
    end_date = DateFilter(field_name='date_created', lookup_expr='lte')
    class Meta:
        model = Order
        fields = '__all__'
        exclude = ['customer', 'date_created', 'note']