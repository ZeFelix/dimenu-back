from django.urls import path
from api.views.permissions import PermissionList, PermissionDetail, GroupList, GroupDetail
from api.views.company import CompanyList, CompanyDetail
from api.views.user import CustomUserList,CustomUserDetail, CustomUserRegister
from api.views.category import CategoryList, CategoryDetail
from api.views.attribute import AttributeList, AttributeDetail
from api.views.product import ProductList, ProductDetail
from api.views.table import TableList, TableDetail
from api.views.avaliation import AvaliationList, AvaliationDetail
from api.views.order import OrderList, OrderDetail

from rest_framework_simplejwt.views import TokenObtainPairView, TokenRefreshView


urlpatterns = [
    path('token',TokenObtainPairView.as_view()),
    path('token/refresh',TokenRefreshView.as_view()),
    path('permissions',PermissionList.as_view()),
    path('permissions/<int:pk>',PermissionDetail.as_view()),
    path('permissions/groups',GroupList.as_view()),
    path('permissions/groups/<int:pk>',GroupDetail.as_view()),
    path('companies', CompanyList.as_view()),
    path('companies/<int:pk>', CompanyDetail.as_view()),
    path('users/register', CustomUserRegister.as_view()),
    path('companies/<int:company_id>/users', CustomUserList.as_view()),
    path('companies/<int:company_id>/users/<int:pk>', CustomUserDetail.as_view()),
    path('companies/<int:company_id>/categories', CategoryList.as_view()),
    path('companies/<int:company_id>/categories/<int:pk>', CategoryDetail.as_view()),
    path('companies/<int:company_id>/attributes', AttributeList.as_view()),
    path('companies/<int:company_id>/attributes/<int:pk>', AttributeDetail.as_view()),
    path('companies/<int:company_id>/products',ProductList.as_view()),
    path('companies/<int:company_id>/products/<int:pk>',ProductDetail.as_view()),
    path('companies/<int:company_id>/tables', TableList.as_view()),
    path('companies/<int:company_id>/tables/<int:pk>', TableDetail.as_view()),
    path('companies/<int:company_id>/orders',OrderList.as_view()),
    path('companies/<int:company_id>/orders/<int:pk>',OrderDetail.as_view()),
    path('companies/<int:company_id>/avaliations', AvaliationList.as_view()),
    path('companies/<int:company_id>/avaliations/<int:pk>', AvaliationDetail.as_view())
]