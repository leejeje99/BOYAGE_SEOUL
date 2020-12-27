from django.urls import path
from . import views

app_name = 'map'


urlpatterns = [
    path('', views.main, name = 'mains' ),
    path('search/', views.search, name = 'search'),
    path('map_contents/<int:pk>/', views.map_contents, name='map_contents'),
    path('place_upload/', views.place_upload, name = 'place_upload'),

    # path('map/', views.map, name = 'map' ),
    # path('guide/', views.guide, name = 'guide' ),
    # path('video/', views.video, name = 'video' ),
]