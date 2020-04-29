from django.urls import path
from . import views

from .views import getRandomVersion

urlpatterns = [
    path('dashboard',views.loadDashboardPage,name='dashboard'),
    path('data/v'+getRandomVersion(), views.get_data),
]


print(getRandomVersion())