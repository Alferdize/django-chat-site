from .models import Users
import django_filters

class UserFilter(django_filters.FilterSet):
    class Meta:
        model = Users
        fields = ['username', 'name', 'number', ]