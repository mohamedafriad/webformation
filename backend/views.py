from django.shortcuts import render, redirect
from django.http import HttpResponseRedirect
from django.core.mail import send_mail
from django.conf import settings
from .models import Formation, Participant, Inscription
from .forms import ParticipantForm, ContactForm, ConnexionForm

#la page d'accueil
def index(request):
    formations=Formation.objects.all()
    return render(request, template_name="index.html", context={'formations': formations})

#Traitement de la connexion à l'espace personnel
def connexion(request):
    if request.method == "POST":
        form = ConnexionForm(request.POST)
        if form.is_valid():
            participant = Participant.objects.get(email=form.cleaned_data['email'])
            formations=Formation.objects.all()
            request.session['connected'] = True
            request.session['user'] = participant.__str__()
            return render(request, template_name="espace.html", context={'participant': participant, 'formations': formations})
            #return render(request, template_name="connexion.html", context={'form': form, 'connected': False})
        else:
            return render(request, template_name="connexion.html", context={'form': form, 'connected': False})
    else:
        form = ConnexionForm()
        return render(request, template_name="connexion.html", context={'form': form, 'connected': False})

def deconnexion(request):
    request.session['connected'] = False
    request.session['user'] = None
    return redirect('front')

#envoie un email au bénéficiaire après l'inscription à la formation
def send_email_success(email):
    try:
        subject = "Merci pour votre inscription à la formation"
        message = "Votre inscription a été validée. Soyez au rendz-vous! Merci."
        email_from = settings.EMAIL_HOST_USER
        recipient_list = [email,]
        send_mail(subject, message, email_from, recipient_list )
        return True
    except:
        return False


#Tritament de l'action d'inscription rapide
def inscription(request, formation_pk=None):
    try:
        if formation_pk:
            formation = Formation.objects.get(pk=formation_pk)
            if formation.etat != "O":
                return redirect('formations-list')
        else:
            return redirect('formations-list')
    except:
        return redirect('formations-list')
    form = ParticipantForm()
    if request.method=="POST":
        form = ParticipantForm(request.POST)
        if form.is_valid():
            participant = form.save()
            inscription = Inscription(formation= formation, participant = participant)
            inscription.save()
            formation.participants.add(inscription)
            send_email_success(participant.email)
            return redirect('formations-list')
        else:
            return render(request, template_name="inscription.html", context={'formation': formation, 'form': form})
    else:
        return render(request, template_name="inscription.html", context={'formation': formation, 'form': form})


def formations(request):
    search=request.GET.get("search_formation")
    connected = request.session.get("connected")
    if search:
        formations=Formation.objects.filter(sujet__contains=search)
    else:
        formations=Formation.objects.all()
    return render(request, template_name="formations.html", context={'formations': formations, 'connected': connected})


def send_email_contact(email, message):
    try:
        subject = "Nouveau message déposé sur la plateforme web formation"
        message = message
        email_from = email
        recipient_list = [settings.EMAIL_HOST_USER, 'm.afriad@gmail.com']
        send_mail(subject, message, email_from, recipient_list )
        return True
    except:
        return False


def contact(request):
    if request.method=="POST":
        form = ContactForm(request.POST)
        if form.is_valid():
            mail_message =  "Message de la part de : %s %s ; son téléphone : %s ; le texte du message est : %s" %(form.cleaned_data['nom'], form.cleaned_data['prenom'], form.cleaned_data['telephone'], form.cleaned_data['message'])
            send_email_contact(form.cleaned_data['email'], mail_message)
            message = 1
            return render(request, template_name="contact.html", context={'message': message})
        else:
            return render(request, template_name="contact.html", context={'form': form})
    else:
        form= ContactForm()
        return render(request, template_name="contact.html", context ={'form': form })