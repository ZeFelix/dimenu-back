from django.urls import path
from .views import *

urlpatterns = [
    path('teste/', teste),
    path('addUsers/', addUsers),
    path('addRatings', addRatings),
    path('cb/', cb),
    path('cf/', cf),
    path('company/<int:companyID>/user/<int:userID>/svd/', svd_rec)
]