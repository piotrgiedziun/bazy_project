# -*- coding: utf-8 -*-
from django.db import models
from django.contrib.auth.models import User

class Mieszkaniec(models.Model):
    mieszkanie = models.OneToOneField('Mieszkanie')
    user = models.ForeignKey(User, unique=True)
    imie = models.CharField(max_length=60)
    nazwisko = models.CharField(max_length=60)
    telefon = models.CharField(max_length=11)

    class Meta:
        db_table = "mieszkaniec"
        verbose_name = u"Mieszkaniec"
        verbose_name_plural = u"Mieszkańcy"

    def __unicode__(self):
        return u"%s %s" % (self.imie, self.nazwisko)

    @staticmethod
    def autocomplete_search_fields():
        return ('id__iexact', 'nazwisko__icontains','imie__icontains', 'mieszkanie__brama__ulica__icontains', 'mieszkanie__brama__miejscowosc__icontains')

class Brama(models.Model):
    numer_bramy = models.CharField(max_length=45)
    ulica = models.CharField(max_length=45)
    miejscowosc = models.CharField(max_length=45)
    kod_pocztowy = models.CharField(max_length=45)
    saldo = models.FloatField(default=0)

    @staticmethod
    def autocomplete_search_fields():
        return ('numer_bramy__iexact', 'miejscowosc__icontains', 'ulica__icontains', 'kod_pocztowy__icontains',)

    class Meta:
        db_table = "brama"
        verbose_name = u"Brame"
        verbose_name_plural = u"Bramy"

    def __unicode__(self):
        return u"ul.%s brama %s " % (self.ulica, self.numer_bramy)

class Mieszkanie(models.Model):
    brama = models.ForeignKey(Brama)
    numer_mieszkania = models.CharField(max_length=10)

    class Meta:
        db_table = "mieszkanie"
        verbose_name = u"Mieszkanie"
        verbose_name_plural = u"Mieszkania"

    def __unicode__(self):
        return "%s %s mieszkanie %s" % (self.brama.ulica, self.brama.numer_bramy, self.numer_mieszkania)

class Newsy(models.Model):
    mieszkancy = models.ManyToManyField(Mieszkaniec)
    tytul = models.CharField(max_length=60)
    tresc = models.TextField()
    data = models.DateTimeField(auto_now_add=True)

    class Meta:
        db_table = "newsy"
        ordering = ['-data', '-pk']
        verbose_name = u"Newsa"
        verbose_name_plural = u"Newsy"

    def __unicode__(self):
        return self.tytul

class Oplaty_type(models.Model):
    name = models.CharField(max_length=60)
    global_saldo = models.BooleanField(default=False)

    class Meta:
        db_table = "oplaty_type"
        verbose_name = u"Typ opłate"
        verbose_name_plural = u"Typy opłat"

    def __unicode__(self):
        return u"%s" % (self.name,)

class Oplaty(models.Model):
    mieszkanie = models.ForeignKey(Mieszkanie)
    oplaty_type = models.ForeignKey(Oplaty_type)
    data_platnosci = models.DateField()
    saldo = models.DecimalField(decimal_places=2, max_digits=10)

    class Meta:
        db_table = "oplaty"
        verbose_name = u"Opłate"
        verbose_name_plural = u"Opłaty"

    def __unicode__(self):
        return u"Opłata #%d" % (self.pk,)

class Wplaty(models.Model):
    oplaty = models.OneToOneField(Oplaty)
    data_wplaty = models.DateField()

    class Meta:
        db_table = "wplaty"
        verbose_name = u"Wpłate"
        verbose_name_plural = u"Wpłaty"