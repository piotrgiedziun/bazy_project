from bazy.models import *
from django.contrib import admin

class MieszkanieAdmin(admin.ModelAdmin):
    raw_id_fields = ('brama',)
    autocomplete_lookup_fields = {
        'fk': ['brama'],
    }
    def brama__ulica(self, o):
        return o.brama.ulica

    def brama__miejscowosc(self, o):
        return o.brama.miejscowosc

    list_display = ('numer_mieszkania', 'mieszkaniec', 'brama')
    list_filter = ['brama__ulica', 'brama__miejscowosc']
    search_fields = ['brama__ulica', 'brama__miejscowosc']

class OplatyAdmin(admin.ModelAdmin):

    def mieszkanie__mieszkaniec(self, o):
        return o.mieszkanie.mieszkaniec

    list_display = ('mieszkanie', 'mieszkanie__mieszkaniec', 'data_platnosci', 'oplaty_type', 'saldo')
    list_filter = ['mieszkanie__brama', 'mieszkanie', 'mieszkanie__mieszkaniec', 'data_platnosci', 'oplaty_type']
    search_fields = ['mieszkanie__brama__ulica', 'mieszkanie__brama__miejscowosc', 'mieszkanie__mieszkaniec__nazwisko']

class NewsyAdmin(admin.ModelAdmin):
    raw_id_fields = ('mieszkancy',)
    autocomplete_lookup_fields = {
        'm2m': ['mieszkancy'],
        }

    def tresc__trim(self, o):
        return o.tresc[:50]+(len(o.tresc)>50 and ["..."] or [""])[0]

    list_display = ('tytul', 'tresc__trim', 'data')
    list_filter = ['data', 'mieszkancy']
    search_fields =  ('tytul', 'tresc__trim')

class MieszkaniecAdmin(admin.ModelAdmin):
    def imie__nazwisko(self, o):
        return "%s %s" % (o.imie, o.nazwisko)

    list_display = ('imie__nazwisko', 'imie', 'nazwisko', 'telefon', 'mieszkanie')
    list_filter = ['mieszkanie__brama__ulica', 'mieszkanie__brama__miejscowosc', 'mieszkanie__brama']
    search_fields = ['mieszkanie__brama__ulica', 'mieszkanie__brama__miejscowosc']

class WplatyAdmin(admin.ModelAdmin):
    list_display = ('data_wplaty', 'saldo')
    list_filter = ['mieszkanie__brama', 'mieszkanie', 'mieszkanie__mieszkaniec', 'data_wplaty']
    search_fields = ['mieszkanie__brama__ulica', 'mieszkanie__brama__miejscowosc', 'mieszkanie__mieszkaniec__nazwisko']

admin.site.register(Mieszkanie, MieszkanieAdmin)
admin.site.register(Newsy, NewsyAdmin)
admin.site.register(Mieszkaniec, MieszkaniecAdmin)
admin.site.register(Brama)
admin.site.register(Oplaty, OplatyAdmin)
admin.site.register(Oplaty_type)
admin.site.register(Wplaty, WplatyAdmin)
