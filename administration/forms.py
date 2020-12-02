from django import forms
from artcenter.models import Artist,Acts,Art
class ArtistForm(forms.ModelForm):
    class Meta:
        model=Artist
        fields='__all__'
    biography=forms.CharField(widget=forms.Textarea(attrs={'rows':15, 'cols':150}))
    acts=forms.ModelMultipleChoiceField(widget=forms.CheckboxSelectMultiple,queryset=Acts.objects.all())
class ActsForm(forms.ModelForm):
    class Meta:
        model=Acts
        fields='__all__'
class ArtsForm(forms.ModelForm):
    class Meta:
        model=Art
        fields='__all__'
