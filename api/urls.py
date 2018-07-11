from django.urls import path
from api.views.company import CompanyList, CompanyDetail
from api.views.user import CustomUserList,CustomUserDetail
from api.views.category import CategoryList, CategoryDetail
from api.views.attribute import AttributeList, AttributeDetail

urlpatterns = [
    path('companies', CompanyList.as_view()),
    path('companies/<int:pk>', CompanyDetail.as_view()),
    path('companies/<int:company_id>/users', CustomUserList.as_view()),
    path('companies/<int:company_id>/users/<int:pk>', CustomUserDetail.as_view()),
    path('companies/<int:company_id>/categories', CategoryList.as_view()),
    path('companies/<int:company_id>/categories/<int:pk>', CategoryDetail.as_view()),
    path('companies/<int:company_id>/attributes', AttributeList.as_view()),
    path('companies/<int:company_id>/attributes/<int:pk>', AttributeDetail.as_view()),
]