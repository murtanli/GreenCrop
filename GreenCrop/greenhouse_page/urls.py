from django.urls import path
from .views import *
urlpatterns = [
    path('auth/', auth, name='auth_page'),
    path('sign_in/', sign_in, name='sign_in'),
    path('profile/', profile, name='profile'),
    path('add_gr_hs/', add_gr_hs, name='add_gr_hs'),
    path('logout/', logout_func, name='logout'),
    path('save_gr_hs/', save_gr_hs, name='save_gr_hs'),
    path('all_gr_hs/', all_gr_hs, name='all_gr_hs'),
    path('map_data/', map_data, name='map_data'),
    path('update_control/', update_control, name='update_control'),
    path('graph_view/', graph_view, name='graph_view'),
    path('monitoring_gr_hs/<int:greenhouse_id>', monitoring_gr_hs, name='monitoring_gr_hs'),
    path('save_db/<int:greenhouse_id>', save_db.as_view(), name='save_db'),
    path('test/', test, name='test'),
]
