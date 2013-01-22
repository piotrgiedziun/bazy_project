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

class NewsyAdmin(admin.ModelAdmin):
    raw_id_fields = ('mieszkancy',)
    autocomplete_lookup_fields = {
        'm2m': ['mieszkancy'],
        }

class MieszkaniecAdmin(admin.ModelAdmin):
    list_filter = ['mieszkanie__brama__ulica', 'mieszkanie__brama__miejscowosc', 'mieszkanie__brama']
    search_fields = ['mieszkanie__brama__ulica', 'mieszkanie__brama__miejscowosc']

admin.site.register(Mieszkanie, MieszkanieAdmin)
admin.site.register(Newsy, NewsyAdmin)
admin.site.register(Mieszkaniec, MieszkaniecAdmin)
admin.site.register(Brama)
admin.site.register(Oplaty)
admin.site.register(Oplaty_type)
