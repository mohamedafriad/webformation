from django.db import models
from django.core.mail import send_mail, send_mass_mail
from django.conf import settings


ETATS_FORMATION = (
    ('O', 'Ouverte'),
    ('F', 'Fermée'),
    ('A', 'Annulée'),
    ('R', 'Reportée'),
    ('T', 'Terminée'),
)

NIVEAUX_PARTICIPANT = (
    ('S', 'Sans'),
    ('P', 'Primaire'),
    ('C', 'Collégial'),
    ('S', 'Secondaire'),
    ('F', 'Formation Professionnelle'),
    ('U', 'Universitaire'),
    ('I', 'Ingénierie'),
)

class Participant(models.Model):
    code = models.CharField("Code", max_length=250, blank=True)
    nom = models.CharField("Nom", max_length=250)
    prenom = models.CharField("Prénom", max_length=250)
    cin = models.CharField("CIN", max_length=250, blank=True, null=True)
    adresse = models.CharField("Adresse", max_length=250, blank=True, null=True)
    telephone = models.CharField("Téléphone", max_length=250, blank=True, null=True)
    email = models.CharField("e-mail", max_length=250, blank=True, null=True)
    niveau = models.CharField("Niveau", max_length=250, blank=True, null=True, choices=NIVEAUX_PARTICIPANT) #niveau scolaire
    age = models.PositiveSmallIntegerField("Age", blank=True, null=True)
    #formation = models.ManyToManyField(Formation,related_name="participants", through=Inscription)

    def __str__(self):
        return "%s %s" %(self.nom, self.prenom)


class Formation(models.Model):
    code = models.CharField("Code", max_length=250)
    sujet = models.CharField("Sujet", max_length=250)
    date_debut = models.DateTimeField("Date Début")
    date_fin = models.DateTimeField("Date Fin")
    nbre_place = models.PositiveSmallIntegerField("Nbre Place", default=20)
    prix =models.DecimalField("Prix", max_digits=20, decimal_places=2, default=0)
    lieu = models.CharField("Lieu", max_length=250)
    domaine = models.CharField("Domaine", max_length=250)
    participant = models.ManyToManyField(Participant, through="Inscription")
    etat = models.CharField("Etat", max_length=250, blank=True, null=True, choices=ETATS_FORMATION, default='O') #choix : ouverte, terminee, annulee, reportee

    def __str__(self):
        return self.code

    def nb_inscriptions(self):
        return int(self.participants.count())

    def nb_presents(self):
        return int(self.participants.filter(present=True).count())

    def place_dispo(self):
        return int(self.nbre_place - self.nb_inscriptions())

    class Meta:
        ordering=['-date_debut']

from django.db.models.signals import post_save
from django.dispatch import receiver

@receiver(post_save, sender=Formation)
def Formation_saved(sender, instance, created, **kwargs):
    if created:
        subject = "NOUVELLE FORMATION PROGRAMMEE"
        message = "Je vous annonce qu'une nouvelle formation intitulée '%s' est programmée le %s.\n Les inscriptions sont ouvertes sur la plateforme.\n Soyez au RDV.\n Cordialement" %(instance.sujet, instance.date_debut)
        email_from = settings.EMAIL_HOST_USER
        #recipients = [p.email for i in Participant.objects.all()]
        datatuple = ()
        for p in Participant.objects.all():
            datatuple += ((subject, message, email_from, [p.email]),)
        datatuple += ((subject, message, email_from, ['m.afriad@gmail.com']),)
        send_mass_mail( datatuple )
        print("Messages envoyés")
    else:
        pass

PRESENCE = (
    (False, 'Non'),
    (True, 'Oui'),
)

class Inscription(models.Model):
    formation = models.ForeignKey(Formation, related_name="participants", on_delete= models.CASCADE)
    participant = models.ForeignKey(Participant, related_name="formations", on_delete= models.CASCADE)
    date_inscription = models.DateTimeField("Date Inscription", auto_now_add=True)
    present = models.BooleanField("Présent?", default=False, choices = PRESENCE )
    note_formation = models.PositiveSmallIntegerField("Note formation", null=True, blank=True)
    note_formateur = models.PositiveSmallIntegerField("Note formateur", null=True, blank=True)

    def __str__(self):
        return "Inscription %s - %s" %(self.formation.code, self.participant)

    class Meta:
        ordering =['-date_inscription']
