from django.urls import path
from .views import *

urlpatterns = [    
    path('add_users/<int:numPessoas>/', addUsers),
    path('company/<int:companyID>/add_ratings/', addRatings),
    path('company/<int:companyID>/user/<int:userID>/get_recommends/', svd_rec),
    path('contentbased_recommends/', cb),
]