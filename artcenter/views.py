from django.shortcuts import render
from django.views import View
from artcenter.models import *
class MapView(View):
    template='artcenter/map.html'
    def get(self,request):
        city_name=request.GET.get('city')
        art_name=request.GET.get('art')
        if city_name:
            city_object=City.objects.filter(city=city_name.capitalize())
            if len(city_object)==1:
                if not art_name:
                    artist_objects=Artist.objects.filter(city=city_object[0])
                    if len(artist_objects)>0:
                        arts=list(set([art.art.art for art in artist_objects]))
                        return render(request,self.template,{'arts':arts,'city':city_name})
                else:
                    art_object=Art.objects.filter(art=art_name.capitalize())
                    if len(art_object)==1:
                        artist_objects=Artist.objects.filter(city__in=city_object,art__in=art_object)
                        if len(artist_objects)>0:
                            return render(request,self.template,{'artist_objects':artist_objects,'city':city_name,'art':art_name})
        return render(request,self.template)
class ArtistProfileView(View):
    template='artcenter/profile.html'
    def get(self,request,city_name,art,artist_name):
        city_object=City.objects.filter(city=city_name.capitalize())
        if len(city_object)==1:
            art_object=Art.objects.filter(art=art.capitalize())
            if len(art_object)==1:
                splited_name=artist_name.split('_')
                if len(splited_name)==2:
                    name,last_name=splited_name
                    artist_object=Artist.objects.filter(name=name.capitalize(),last_name=last_name.capitalize(),city__in=city_object,art__in=art_object)
                    return render(request,self.template,{'artist_object':artist_object[0],'date_of_birth':artist_object[0].date_of_birth,'date_of_death':artist_object[0].date_of_death})
