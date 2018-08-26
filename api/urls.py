from django.urls import path
from api.views.permissions import PermissionList, PermissionDetail, GroupList, GroupDetail
from api.views.company import CompanyList, CompanyDetail, CompanyOverView
from api.views.category import CategoryList, CategoryDetail
from api.views.attribute import AttributeList, AttributeDetail, AttributeListProduct
from api.views.product import ProductList, ProductDetail, ProductListCategory
from api.views.table import TableList, TableDetail
from api.views.avaliation import AvaliationList, AvaliationDetail
from api.views.order import OrderList, OrderDetail, OrderListTable
from api.views.owner import RegisterOwner, OwnerDetail
from api.views.client import (
    RegisterClient, ClientDetail, ClientListCompanies, ClientListProducts,
    ClientListCategories, ClientListProductsByCategories, ClientListAttributes,
    ClientListAttributesByProducts
)
from api.views.employee import EmployeeDetail, EmployeeList
from api.views.user import UserDetail
from api.views.ingredient import IngredientList, IngredientDetail

from rest_framework_simplejwt.views import TokenObtainPairView, TokenRefreshView


urlpatterns = [
    path('clients/register', RegisterClient.as_view()),
    path('clients/<int:pk>',ClientDetail.as_view()),
    path('clients/companies',ClientListCompanies.as_view()),
    path('clients/companies/<int:pk>/attributes',ClientListAttributes.as_view()),
    path('clients/companies/<int:pk>/products',ClientListProducts.as_view()),
    path('clients/companies/<int:pk>/products/<int:product_pk>/attributes',ClientListAttributesByProducts.as_view()),
    path('clients/companies/<int:pk>/categories',ClientListCategories.as_view()),
    path('clients/companies/<int:pk>/categories/<int:category_id/products',ClientListProductsByCategories.as_view()),

    path('companies/<int:company_id>/categories', CategoryList.as_view()),
    path('companies/<int:company_id>/categories/<int:pk>', CategoryDetail.as_view()),
    path('companies/<int:company_id>/categories/<int:pk>/products', ProductListCategory.as_view()),

    path('companies/<int:company_id>/attributes', AttributeList.as_view()),
    path('companies/<int:company_id>/attributes/<int:pk>', AttributeDetail.as_view()),

    path('companies/<int:company_id>/employees', EmployeeList.as_view()),
    path('companies/<int:company_id>/employees/<int:pk>', EmployeeDetail.as_view()),

    path('companies/<int:company_id>/products',ProductList.as_view()),
    path('companies/<int:company_id>/products/<int:pk>',ProductDetail.as_view()),
    path('companies/<int:company_id>/products/<int:pk>/attributes',AttributeListProduct.as_view()),

    path('companies/<int:company_id>/ingredients',IngredientList.as_view()),
    path('companies/<int:company_id>/ingredients/<int:pk>',IngredientDetail.as_view()),

    path('companies/<int:company_id>/tables', TableList.as_view()),
    path('companies/<int:company_id>/tables/<int:pk>', TableDetail.as_view()),
    path('companies/<int:company_id>/tables/<int:pk>/orders', OrderListTable.as_view()),

    path('companies/<int:company_id>/orders',OrderList.as_view()),
    path('companies/<int:company_id>/orders/<int:pk>',OrderDetail.as_view()),

    path('companies/<int:company_id>/avaliations', AvaliationList.as_view()),
    path('companies/<int:company_id>/avaliations/<int:pk>', AvaliationDetail.as_view()),

    path('companies/<int:company_id>/overview', CompanyOverView.as_view()),

    path('permissions',PermissionList.as_view()),
    path('permissions/<int:pk>',PermissionDetail.as_view()),
    path('permissions/groups',GroupList.as_view()),
    path('permissions/groups/<int:pk>',GroupDetail.as_view()),

    path('owners/register', RegisterOwner.as_view()),
    path('owners/<int:pk>',OwnerDetail.as_view()),

    path('token',TokenObtainPairView.as_view()),
    path('token/refresh',TokenRefreshView.as_view()),

    path('users/<int:pk>', UserDetail.as_view()),
    path('users/<int:pk>/companies', CompanyList.as_view()),
    path('users/<int:user_pk>/companies/<int:company_id>', CompanyDetail.as_view())

]