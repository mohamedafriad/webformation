from django.contrib import admin
from .models import Formation, Participant, Inscription

class InscriptionInline(admin.TabularInline):
    model = Inscription
    extra = 1
    auotocomplete_fields=['formation', 'participant']
    fields =['formation', 'participant']


class FormationAdmin(admin.ModelAdmin):
    list_display=('id', 'code', 'sujet', 'date_debut', 'prix', 'lieu', 'etat', 'nbre_place', 'place_dispo', 'nb_inscriptions', 'nb_presents')
    inlines = [InscriptionInline,]
    list_filter =('etat',)
    list_editable = ('id',)
    list_display_links= ('code', 'sujet')


class ParticipantAdmin(admin.ModelAdmin):
    list_display=('__str__', 'code', 'email', 'telephone', 'age', 'niveau')
    inlines = [InscriptionInline,]


class InscriptionAdmin(admin.ModelAdmin):
    list_display = ('formation', 'participant', 'date_inscription', 'present', 'note_formation', 'note_formateur')
    list_filter = ('formation', 'participant__niveau', 'present')
    list_editable = ('present',)


admin.site.register(Formation, FormationAdmin)
admin.site.register(Participant, ParticipantAdmin)
admin.site.register( Inscription, InscriptionAdmin)
