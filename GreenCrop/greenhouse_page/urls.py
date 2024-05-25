from django.urls import path
from .views import *
urlpatterns = [
    path('auth/', auth, name='auth_page'),
    path('sign_in/', sign_in, name='sign_in'),
    path('profile/', profile, name='profile'),
    path('add_gr_hs/', add_gr_hs, name='add_gr_hs'),
]
