from django.shortcuts import render
import redis
from django.conf import settings
from django.http import HttpResponse
# Create your views here.

r = redis.StrictRedis(host=settings.REDIS_HOST, port = settings.REDIS_PORT, db = settings.REDIS_DB)

def teste(request):

    return HttpResponse("teste")