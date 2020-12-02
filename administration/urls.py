from django.urls import path
from django.conf import settings
from administration.views import *
app_name='administration'
urlpatterns = [
    path('',AdministrationView.as_view(),name='main'),
    path('<link>/',LinkView.as_view(),name='link'),
    path('artists/add/',ArtistAddView.as_view(),name='artistadd'),
    path('artists/<artist_name>/',ArtistUpdateView.as_view(),name='artist_update'),
    path('artists/<artist_name>/remove/',ArtistRemoveView.as_view(),name='artist_remove'),
    path('acts/add',ActsAddView.as_view(),name='acts_add'),
    path('acts/<act_name>/',ActsUpdateView.as_view(),name='acts_update'),
    path('acts/<act_name>/remove/',ActsRemoveView.as_view(),name='acts_remove'),
    path('arts/add',ArtsAddView.as_view(),name='arts_add'),
    path('arts/<art_name>/',ArtsUpdateView.as_view(),name='arts_update'),
    path('arts/<art_name>/remove/',ArtsRemoveView.as_view(),name='arts_remove'),
]
