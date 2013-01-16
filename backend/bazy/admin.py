from bazy.models import *
from django.contrib import admin

class MieszkanieAdmin(admin.ModelAdmin):

    def brama__ulica(self, o):
        return o.brama.ulica

    def brama__miejscowosc(self, o):
        return o.brama.miejscowosc


    list_display = ('numer_mieszkania', 'mieszkaniec', 'brama')
    list_filter = ['brama__ulica', 'brama__miejscowosc']
    search_fields = ['brama__ulica', 'brama__miejscowosc']

admin.site.register(Mieszkanie, MieszkanieAdmin)
admin.site.register(Mieszkaniec)
admin.site.register(Brama)
admin.site.register(Oplaty)
admin.site.register(Oplaty_type)
admin.site.register(Newsy)
