from rest_framework import permissions
import jwt
from django.conf import settings
from api.models import *
from django.core.exceptions import ObjectDoesNotExist

class CustomPermissions(permissions.BasePermission):
    """
    Classe customizada para identificar se o usuário é criador ou pertence a empresa
    """

    def has_permission(self, request, view):
        """
        Return `True` if permission is granted, `False` otherwise.
        """
        if request.method in permissions.SAFE_METHODS:
            return True

        token = request.META["HTTP_AUTHORIZATION"].replace("Bearer ","")
        company_id = view.kwargs["company_id"]

        try:
            payload = jwt.decode(token, settings.SECRET_KEY)
        except jwt.ExpiredSignatureError:
            msg = 'Signature expired. Please log in again.'
            raise exceptions.AuthenticationFailed(msg)
        except jwt.InvalidTokenError:
            msg = 'Invalid token. Please log in again.' 
            raise exceptions.AuthenticationFailed(msg)

        try:
            user = User.objects.get(pk=payload['user_id'])
            company = Company.objects.get(pk=company_id)
        except User.DoesNotExist:
            msg = 'No user matching this token was found.'
            raise exceptions.AuthenticationFailed(msg)
        except Company.DoesNotExist:
            msg = 'Company not matching this id.'
            raise exceptions.AuthenticationFailed(msg)
        
        try:
            user.client
            return True
        except ObjectDoesNotExist:
            try:
                owner = user.owner
                if owner == company.owner:
                    return True
            except ObjectDoesNotExist:
                employee = user.employee
                
                if employee in company.employee:
                    return True
        
        return False

class CustomPermissionsEmployee(permissions.BasePermission):
    """
    Classe customizada para identificar se o usuário é o dono dos seus dados
    """

    def has_permission(self, request, view):
        """
        Return `True` if permission is granted, `False` otherwise.
        """

        token = request.META["HTTP_AUTHORIZATION"].replace("Bearer ","")
        company_id = view.kwargs["company_id"]

        try:
            payload = jwt.decode(token, settings.SECRET_KEY)
        except jwt.ExpiredSignatureError:
            msg = 'Signature expired. Please log in again.'
            raise exceptions.AuthenticationFailed(msg)
        except jwt.InvalidTokenError:
            msg = 'Invalid token. Please log in again.' 
            raise exceptions.AuthenticationFailed(msg)

        try:
            user = User.objects.get(pk=payload['user_id'])
            company = Company.objects.get(pk=company_id)
        except User.DoesNotExist:
            msg = 'No user matching this token was found.'
            raise exceptions.AuthenticationFailed(msg)
        except Company.DoesNotExist:
            msg = 'Company not matching this id.'
            raise exceptions.AuthenticationFailed(msg)
        
        try:
            user.client
            return False
        except ObjectDoesNotExist:
            try:
                owner = user.owner
                if owner == company.owner:
                    return True
            except ObjectDoesNotExist:
                employee = user.employee
                if employee in company.employee:
                    return True
        
        return False
 


class CustomPermissionsOrder(permissions.BasePermission):
    """
    Classe customizada para identificar se o usuário é criador ou pertence a empresa dona das orders
    Caso seja um client:
        o get de todas as ordes não será permitido;
        o put, get de uma order e delete só será permitido caso sejá o criador da order
    """

    def has_permission(self, request, view):
        """
        Return `True` if permission is granted, `False` otherwise.
        """
        
        token = request.META["HTTP_AUTHORIZATION"].replace("Bearer ","")
        company_id = view.kwargs["company_id"]

        try:
            payload = jwt.decode(token, settings.SECRET_KEY)
        except jwt.ExpiredSignatureError:
            msg =  'Signature expired. Please log in again.'
            raise exceptions.AuthenticationFailed(msg)
        except jwt.InvalidTokenError:
            msg = 'Invalid token. Please log in again.' 
            raise exceptions.AuthenticationFailed(msg)

        try:
            user = User.objects.get(pk=payload['user_id'])
            company = Company.objects.get(pk=company_id)
        except User.DoesNotExist:
            msg = 'No user matching this token was found.'
            raise exceptions.AuthenticationFailed(msg)
        except Company.DoesNotExist:
            msg = 'Company not matching this id.'
            raise exceptions.AuthenticationFailed(msg)
        
        try:
            user.client
            order_id = view.kwargs["pk"]
            order = Order.objects.get(pk=order_id)               
            if user == order.client:
                return True
        except KeyError:
            """
            Provavelmente indica que é o get all de todas as orders do client
            'pk' não existe no request
            """
            return True

        except ObjectDoesNotExist:
            try:
                owner = user.owner
                if owner == company.owner:
                    return True
            except ObjectDoesNotExist:
                employee = user.employee
                
                if employee in company.employee:
                    return True
        
        return False
 

class CustomPermissionsOrderTable(permissions.BasePermission):
    """
    Classe customizada para identificar se o usuário é criador ou pertence a empresa dona das orders daquela mesa
    Caso seja um client não poderá listar por mesa nesse momento
    """

    def has_permission(self, request, view):
        """
        Return `True` if permission is granted, `False` otherwise.
        """
        
        token = request.META["HTTP_AUTHORIZATION"].replace("Bearer ","")
        company_id = view.kwargs["company_id"]

        try:
            payload = jwt.decode(token, settings.SECRET_KEY)
        except jwt.ExpiredSignatureError:
            msg 'Signature expired. Please log in again.'
            raise exceptions.AuthenticationFailed(msg)
        except jwt.InvalidTokenError:
            msg 'Invalid token. Please log in again.' 
            raise exceptions.AuthenticationFailed(msg)

        try:
            user = User.objects.get(pk=payload['user_id'])
            company = Company.objects.get(pk=company_id)
        except User.DoesNotExist:
            msg = 'No user matching this token was found.'
            raise exceptions.AuthenticationFailed(msg)
        except Company.DoesNotExist:
            msg = 'Company not matching this id.'
            raise exceptions.AuthenticationFailed(msg)
        
        try:
            user.client
            return False
        except ObjectDoesNotExist:
            try:
                owner = user.owner
                if owner == company.owner:
                    return True
            except ObjectDoesNotExist:
                employee = user.employee
                
                if employee in company.employee:
                    return True
        
        return False


class CustomPermissionsClient(permissions.BasePermission):
    """
    Classe customizada para permitir que o client dono das suas informações tenha acessa a elas
    """

    def has_permission(self, request, view):
        """
        Return `True` if permission is granted, `False` otherwise.
        """
        
        token = request.META["HTTP_AUTHORIZATION"].replace("Bearer ","")
        client_id = view.kwargs["pk"]

        try:
            payload = jwt.decode(token, settings.SECRET_KEY)
        except jwt.ExpiredSignatureError:
            msg = 'Signature expired. Please log in again.'
            raise exceptions.AuthenticationFailed(msg)
        except jwt.InvalidTokenError:
            msg = 'Invalid token. Please log in again.' 
            raise exceptions.AuthenticationFailed(msg)

        try:
            user = User.objects.get(pk=payload['user_id'])
            company = Company.objects.get(pk=company_id)
        except User.DoesNotExist:
            msg = 'No user matching this token was found.'
            raise exceptions.AuthenticationFailed(msg)
        except Company.DoesNotExist:
            msg = 'Company not matching this id.'
            raise exceptions.AuthenticationFailed(msg)
        
        try:
            user.client
            if user.client.id == client_id:
                return True
        except ObjectDoesNotExist:
            return False
        
        return False


class CustomPermissionsOwner(permissions.BasePermission):
    """
    Classe customizada para permitir que o owner dono das suas informações tenha acessa a elas
    """

    def has_permission(self, request, view):
        """
        Return `True` if permission is granted, `False` otherwise.
        """
        
        token = request.META["HTTP_AUTHORIZATION"].replace("Bearer ","")
        owner_id = view.kwargs["pk"]

        try:
            payload = jwt.decode(token, settings.SECRET_KEY)
        except jwt.ExpiredSignatureError:
            msg = 'Signature expired. Please log in again.'
            raise exceptions.AuthenticationFailed(msg)
        except jwt.InvalidTokenError:
            msg = 'Invalid token. Please log in again.' 
            raise exceptions.AuthenticationFailed(msg)

        try:
            user = User.objects.get(pk=payload['user_id'])
        except User.DoesNotExist:
            msg = 'No user matching this token was found.'
            raise exceptions.AuthenticationFailed(msg)
        except Company.DoesNotExist:
            msg = 'Company not matching this id.'
            raise exceptions.AuthenticationFailed(msg)
        
        try:
            user.owner
            if user.owner.id == owner_id:
                return True
        except ObjectDoesNotExist:
            return False
        
        return False

