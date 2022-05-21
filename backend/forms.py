from django import forms
from .models import Participant

#formulaire d'inscription à la formation = de creation d'un nouveau particiapnt
class ParticipantForm(forms.ModelForm):
    class Meta:
        model = Participant
        fields = ['cin', 'nom', 'prenom', 'age', 'telephone', 'email', 'niveau']


#formulaire de contact => chaque message est envoye par mail a l'admin
class ContactForm(forms.Form):
    nom = forms.CharField(required=True)
    prenom = forms.CharField(required= True)
    message = forms.CharField(widget=forms.Textarea, required=True)
    telephone = forms.CharField(required = False)
    email = forms.EmailField(required=True)


#formulaire d'inscription pour avoir un espace personnel
class InscriptionForm(forms.Form):
    username = forms.CharField(required =True)
    email = forms.EmailField(required=True)
    #mot_passe = forms.CharField(required=True, widget=forms.PasswordInputField())
    #mot_passe_confirm = forms.CharField(required=True, widget=forms.PasswordInputField())
    telephone = forms.CharField(required=False)

