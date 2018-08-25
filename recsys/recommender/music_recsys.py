import pandas as pd
import numpy as np
from scipy.sparse import csr_matrix
from django.conf import settings
import redis

REDIS_INSTANCE = redis.StrictRedis(host=settings.REDIS_HOST, port = settings.REDIS_PORT, db = settings.REDIS_DB)

def setData():  

  pd.set_option('display.float_format', lambda x: '%.3f' % x)

  user_dataset = '/home/anderson/Downloads/lastfm-dataset-360K/usersha1-artmbid-artname-plays.tsv'
  profile_dataset = '/home/anderson/Downloads/lastfm-dataset-360K/usersha1-profile.tsv'

  user_data = pd.read_table(user_dataset,
                            header = None, nrows = 2e7,
                            names = ['users', 'musicbrainz-artist-id', 'artist-name', 'plays'],
                            usecols = ['users', 'artist-name', 'plays'])
  # user_profiles = pd.read_table(profile_dataset,
  #                           header = None,
  #                           names = ['users', 'gender', 'age', 'country', 'signup'],
  #                           usecols = ['users', 'country'])

  REDIS_INSTANCE.set('user_data', user_data.to_msgpack(compress='zlib'))

def getData():
  data = REDIS_INSTANCE.get('user_data')
  user_data = pd.read_msgpack(data)
  print(user_data)