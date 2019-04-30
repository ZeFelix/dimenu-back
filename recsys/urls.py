from django.urls import path
from .views import *

urlpatterns = [
    path('add_users/<int:numPessoas>/', addUsers),
    path('company/<int:companyID>/add_ratings/', addRatings),
    path('company/<int:companyID>/user/<int:userID>/iter_svd/', iterSVD),
    path('company/<int:companyID>/user/<int:userID>/hybrid/', hybrid_recsys),
    path('company/<int:companyID>/user/<int:userID>/cb/', cb_recsys),
]
