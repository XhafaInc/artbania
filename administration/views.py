from django.shortcuts import render,redirect
from django.views import View
from artcenter.models import Artist,Acts,Art
from administration.forms import ArtistForm,ActsForm,ArtsForm
from django.http import HttpResponse
from django import forms
class AdministrationView(View):
    template='administration/main.html'
    def get(self,request):
        user=request.user
        if user.is_authenticated and user.is_staff:
            links=['artists','acts','arts']
            args={'links':links}
            return render(request,self.template,args)
class LinkView(View):
    template='administration/artist.html'
    def get(self,request,link):
        user=request.user
        if user.is_authenticated and user.is_staff:
            if link=='artists':
                artist_full_name=[i.name+' '+i.last_name for i in Artist.objects.all()]
                link_name=[elem.replace(' ','_').lower() for elem in artist_full_name]
                full_name=zip(artist_full_name,link_name)
                args={'elements':full_name,'link':link}
                return render(request,self.template,args)
            elif link=='acts':
                acts=[i.act_name for i in Acts.objects.all()]
                acts_link=[act.replace(' ','_').lower() for act in acts]
                joined_acts=zip(acts,acts_link)
                args={'elements':joined_acts,'link':link}
                return render(request,self.template,args)
            elif link=='arts':
                acts=[art.art for art in Art.objects.all()]
                acts_link=[act.lower() for act in acts]
                joined_acts=zip(acts,acts_link)
                args={'elements':joined_acts,'link':link}
                return render(request,self.template,args)
class ArtistAddView(View):
    template='administration/artistadd.html'
    def get(self,request):
        user=request.user
        if user.is_authenticated and user.is_staff:
            all_acts=[act.acts.all() for act in Artist.objects.all()]
            acts_list=[all_acts[i][y] for i in range(len(all_acts)) for y in range(len(all_acts[i]))]
            free_acts=Acts.objects.exclude(act_name__in=acts_list)
            if len(free_acts)==0:
                acts_error={'acts_error':'No acts available'}
                return render(request,self.template,acts_error)
            artist_form=ArtistForm()
            artist_form.fields['acts']=forms.ModelMultipleChoiceField(widget=forms.CheckboxSelectMultiple,queryset=free_acts)
            args={'artist_form':artist_form}
            return render(request,self.template,args)
    def post(self,request):
        user=request.user
        if user.is_authenticated and user.is_staff:
            artist_form=ArtistForm(request.POST,request.FILES)
            print(artist_form.errors)
            name=artist_form.cleaned_data['name']
            last_name=artist_form.cleaned_data['last_name']
            artist_object=Artist.objects.filter(name=name,last_name=last_name)
            if len(artist_object)==0:
                biography=artist_form.cleaned_data['biography']
                acts=artist_form.cleaned_data['acts']
                image=artist_form.cleaned_data['image']
                city=artist_form.cleaned_data['city']
                art=artist_form.cleaned_data['art']
                date_of_birth=artist_form.cleaned_data['date_of_birth']
                date_of_death=artist_form.cleaned_data['date_of_death']
                artist_object=Artist(name=name,last_name=last_name,biography=biography,image=image,city=city,art=art,date_of_birth=date_of_birth,date_of_death=date_of_death)
                artist_object.save()
                for elem in acts:
                    artist_object.acts.add(elem)
                return redirect('administration:artistadd')
            return render(request,self.template,{'artist_form':artist_form})
class ArtistUpdateView(View):
    artist_template='administration/artistadmin.html'
    def get(self,request,artist_name):
        user=request.user
        if user.is_authenticated and user.is_staff:
            full_name=artist_name.split('_')
            if len(full_name)==2:
                name=full_name[0].capitalize()
                last_name=full_name[1].capitalize()
                artist_object=Artist.objects.filter(name=name,last_name=last_name)
                if len(artist_object)==1:
                    artist_acts=[act.acts.all() for act in artist_object]
                    artist_act_list=[act for act in artist_acts[0]]
                    artist_object=artist_object[0]
                    biography=artist_object.biography
                    excluded_artist=Artist.objects.exclude(name=name,last_name=last_name)
                    if excluded_artist==[]:  
                        accepted_acts=[act for act in Acts.objects.all()]
                    else:
                        artists_acts=[act.acts.all() for act in excluded_artist]
                        act_list=[artists_acts[i][y] for i in range(len(artists_acts)) for y in range(len(artists_acts[i]))]
                        accepted_acts=[act for act in Acts.objects.exclude(act_name__in=act_list)]
                    city=artist_object.city
                    art=artist_object.art
                    image=artist_object.image
                    date_of_birth=artist_object.date_of_birth
                    date_of_death=artist_object.date_of_death
                    artist_form=ArtistForm()
                    artist_form.fields['name'].initial=name
                    artist_form.fields['last_name'].initial=last_name
                    artist_form.fields['image'].initial=image
                    artist_form.fields['biography'].initial=biography
                    artist_form.fields['city'].initial=city
                    artist_form.fields['art'].initial=art
                    artist_form.fields['date_of_birth'].initial=date_of_birth
                    artist_form.fields['date_of_death'].initial=date_of_death
                    artist_form.fields['acts']=forms.ModelMultipleChoiceField(widget=forms.CheckboxSelectMultiple,queryset=Acts.objects.filter(act_name__in=accepted_acts),initial=[elem for elem in artist_act_list])
                    args={'artist_form':artist_form,'image':image}
                    return render(request,self.artist_template,args)
    def post(self,request,artist_name):
        user=request.user
        if user.is_authenticated and user.is_staff:
            full_name=artist_name.split('_')
            if len(full_name)==2:
                name=full_name[0].capitalize()
                last_name=full_name[1].capitalize()
                artist_object=Artist.objects.filter(name=name,last_name=last_name)
                if len(artist_object)==1:
                    artist_form=ArtistForm(request.POST,request.FILES)
                    if artist_form.is_valid():
                        name=artist_form.cleaned_data['name']
                        last_name=artist_form.cleaned_data['last_name']
                        biography=artist_form.cleaned_data['biography']
                        image=artist_form.cleaned_data['image']
                        acts=artist_form.cleaned_data['acts']
                        city=artist_form.cleaned_data['city']
                        art=artist_form.cleaned_data['art']
                        date_of_birth=artist_form.cleaned_data['date_of_birth']
                        date_of_death=artist_form.cleaned_data['date_of_death']
                        if image==None:
                            image=artist_object[0].image.name
                            id=artist_object[0].id
                            artist=Artist(id,name=name,last_name=last_name,biography=biography,image=image,city=city,art=art,date_of_birth=date_of_birth,date_of_death=date_of_death).save()
                            artist_object[0].acts.set(acts)
                            new_name=name+'_'+last_name.lower()
                            return redirect('/administration/artists/'+new_name)
                        else:
                            id=artist_object[0].id
                            artist=Artist(id,name=name,last_name=last_name,biography=biography,image=image,city=city,art=art,date_of_birth=date_of_birth,date_of_death=date_of_death).save()
                            artist_object[0].acts.set(acts)
                            new_name=name+'_'+last_name.lower()
                            return redirect('/administration/artists/'+new_name)
class ArtistRemoveView(View):
    def get(self,request,artist_name):
        user=request.user
        if user.is_authenticated and user.is_staff:
            full_name=artist_name.split('_')
            if len(full_name)==2:
                name=full_name[0].capitalize()
                last_name=full_name[1].capitalize()
                artist_object=Artist.objects.filter(name=name,last_name=last_name)
                if len(artist_object)==1:
                    artist_object.delete()
                    return redirect("administration:artistadd")
class ActsAddView(View):
    template='administration/add_acts.html'
    def get(self,request):
        user=request.user
        if user.is_authenticated and user.is_staff:
            act_form=ActsForm()
            return render(request,self.template,{'act_form':act_form})
    def post(self,request):
        user=request.user
        if user.is_authenticated and user.is_staff:
            act_form=ActsForm(request.POST)
            if act_form.is_valid():
                act_name=act_form.cleaned_data['act_name']
                act_object=Acts.objects.filter(act_name=act_name)
                if len(act_object)==0:
                    act=Acts(act_name=act_name.capitalize()).save()
                    return redirect("administration:acts_add")
class ActsUpdateView(View):
    template='administration/acts_update.html'
    def get(self,request,act_name):
        user=request.user
        if user.is_authenticated and user.is_staff:
            act_name=act_name.replace('_',' ').capitalize()
            act_object=Acts.objects.filter(act_name=act_name)
            if len(act_object)==1:
                acts_form=ActsForm()
                act_name=act_object[0].act_name
                acts_form.fields['act_name'].initial=act_name
                return render(request,self.template,{'acts_form':acts_form})
    def post(self,request,act_name):
        user=request.user
        if user.is_authenticated and user.is_staff:
            act_name=act_name.replace('_',' ').capitalize()
            act_object=Acts.objects.filter(act_name=act_name)
            if len(act_object)==1:
                acts_form=ActsForm(request.POST)
                if acts_form.is_valid():
                    act_name=acts_form.cleaned_data['act_name']
                    id=act_object[0].id
                    Acts(id=id,act_name=act_name).save()
                    new_name=act_name.replace(' ','_').lower()
                    return redirect('/administration/acts/'+new_name)
class ActsRemoveView(View):
    def get(self,request,act_name):
        user=request.user
        if user.is_authenticated and user.is_staff:
            act_name=act_name.replace('_',' ').capitalize()
            act_object=Acts.objects.filter(act_name=act_name)
            if len(act_object)==1:
                act_object.delete()
                return redirect('/administration/acts')
class ArtsAddView(View):
    template='administration/add_arts.html'
    def get(self,request):
        user=request.user
        if user.is_authenticated and user.is_staff:
            art_form=ArtsForm()
            return render(request,self.template,{'art_form':art_form})
    def post(self,request):
        user=request.user
        if user.is_authenticated and user.is_staff:
            art_form=ArtsForm(request.POST)
            if art_form.is_valid():
                art_name=art_form.cleaned_data['art']
                art_object=Art.objects.filter(art=art_name)
                if len(art_object)==0:
                    act=Art(art=art_name).save()
                    return redirect("administration:arts_add")
class ArtsUpdateView(View):
    template='administration/arts_update.html'
    def get(self,request,art_name):
        user=request.user
        if user.is_authenticated and user.is_staff:
            art_object=Art.objects.filter(art=art_name.capitalize())
            if len(art_object)==1:
                art_name=art_object[0].art
                arts_form=ArtsForm()
                arts_form.fields['art'].initial=art_name
                return render(request,self.template,{'arts_form':arts_form})
    def post(self,request,art_name):
        user=request.user
        if user.is_authenticated and user.is_staff:
            art_object=Art.objects.filter(art=art_name.capitalize())
            print(art_object)
            if len(art_object)==1:
                arts_form=ArtsForm(request.POST)
                if arts_form.is_valid():
                    art_name=arts_form.cleaned_data['art']
                    id=art_object[0].id
                    Art(id=id,art=art_name).save()
                    return redirect('/administration/arts/'+art_name.lower())
class ArtsRemoveView(View):
    def get(self,request,art_name):
        user=request.user
        if user.is_authenticated and user.is_staff:
            art_object=Art.objects.filter(art=art_name.capitalize())
            print(art_object)
            if len(art_object)==1:
                art_object.delete()
                return redirect('/administration/arts')
