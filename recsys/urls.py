from django.urls import path
from .views import *

urlpatterns = [
    path('teste/', teste),
    path('addUsers/', addUsers),
    path('addRatings', addRatings),
    path('cb/', cb),
    path('cf/', cf),
    path('svd/', svd_rec)
]