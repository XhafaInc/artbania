from django.urls import path
from artcenter.views import *
app_name='artcenter'
urlpatterns = [
    path('',MapView.as_view(),name='map'),
    path('city/<city_name>/<art>/<artist_name>/',ArtistProfileView.as_view(),name='artist_profile'),
]
