from django.urls import path
from . import views,sentimate_analysis

urlpatterns = [    
#    path('dashboard',sentimate_analysis.main,name='main'),
     path('dashboard',sentimate_analysis.main,name='main'),
     path('profile',views.profile,name='profile'),
    
]