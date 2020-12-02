from django.contrib import admin
from django.urls import path,include,re_path
from artcenter import urls as artcenterurls
from accounts import urls as accountsurls
from administration import urls as administrationurls
from accounts import urls as accountsurls
from django.conf import settings
from django.views.static import serve
urlpatterns = [
    re_path(r'^static/(?:.*)$', serve, {'document_root': settings.STATIC_ROOT, }),
    path('admin/', admin.site.urls),
    path('administration/',include(administrationurls)),
    path('accounts/',include(accountsurls)),
    path('media/<path>', serve,{'document_root': settings.MEDIA_ROOT}),
    path('',include(artcenterurls)),

]
