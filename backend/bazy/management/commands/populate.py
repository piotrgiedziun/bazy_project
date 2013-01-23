# -*- coding: utf-8 -*-
from django.core.management.base import BaseCommand, CommandError
from django.contrib.auth.models import User
from optparse import make_option
import sqlite3, random, os.path
from bazy.models import *
import datetime

DATABASE_PATH = os.path.join("..", "populate.db")

class Populate:

    def __init__(self, database, population_size, population_per_home):
        self.population_size = population_size
        self.population_per_home = population_per_home

        # clear
        self.names = []
        self.addresses = []

        self.database = database
        self.c = self.database.cursor()

    def __delete__(self, instance):
        self.database.commit()
        self.database.close()

    def get_names(self):
        for row in self.c.execute('SELECT imie,nazwisko FROM names ORDER BY RANDOM() LIMIT %d'
                                  % (self.population_size,)):
            self.names.append({
                'imie': row[0],
                'nazwisko': row[1]
            })

    def get_addressese(self):
        for row in self.c.execute('SELECT street,city,code FROM addresses ORDER BY RANDOM() LIMIT %d'
                                  % (self.population_size/self.population_per_home,)):
            self.addresses.append({
                'ulica': row[0],
                'miejscowosc': row[1],

                'kod': row[2]
            })

    def start(self):
        self.get_names()
        self.get_addressese()

        # populate Oplaty_type
        oplaty_types = ['czynsz', 'kredyt', 'rozlicznienie wody', \
            'rozlicznie ciepła', 'garaż', 'wykup gruntu', 'fundusz remontowy', 'inne']
        for oplaty_type in oplaty_types:
            Oplaty_type(name=oplaty_type).save()

        oplaty_types = Oplaty_type.objects.all()

        homes_count = -1
        for i in range(len(self.names)):
            if i % self.population_per_home == 0:
                homes_count+=1
                brama = Brama(
                    numer_bramy=random.randrange(1, 100),
                    ulica=self.addresses[homes_count]['ulica'],
                    miejscowosc=self.addresses[homes_count]['miejscowosc']
                )
                brama.save()

            user =  User.objects.create_user('user%d' % (i,), 'user%d@localhost.com' % (i,), 'user%d' % (i,))

            mieszkanie = Mieszkanie(
                brama = brama,
                numer_mieszkania = (i % self.population_per_home)+1
            )
            mieszkanie.save()

            mieszkaniec = Mieszkaniec(
                user=user,
                imie=self.names[i]['imie'],
                nazwisko=self.names[i]['nazwisko'],
                mieszkanie=mieszkanie)
            mieszkaniec.save()

        # populate Oplaty
        for mieszkaniec in Mieszkaniec.objects.all():
            for miesiac in range(1,13):
                for oplaty_type in oplaty_types:
                    if random.randrange(0,10) != 0:
                        Oplaty(
                            mieszkanie=mieszkaniec.mieszkanie,
                            oplaty_type=oplaty_type,
                            data_platnosci=datetime.date(2013, miesiac, 1),
                            saldo=float(random.randrange(10,100)),
                        ).save()

        # populate news for each user
        for i in range(0, 20):
            n = Newsy(tytul="To jest wiadomosc numer %d proszę się z nią zapoznać" % (i,),tresc="testowa tresc",)
            n.save()
            n.mieszkancy.add(*[m.id for m in Mieszkaniec.objects.all()]),
            n.save()


class Command(BaseCommand):
    args = 'population_size population_per_home'
    help = 'Populate database'
    option_list = BaseCommand.option_list + (
        make_option('--clear',
            action='store_true',
            dest='clear',
            default=False,
            help='Clear database before populating'),
        )

    def handle(self, *args, **options):

        if options['clear']:
            self.stdout.write('Clearing database...\n')
            Oplaty_type.objects.all().delete()
            self.stdout.write('Flushed table "oplaty_type"\n')
            Oplaty.objects.all().delete()
            self.stdout.write('Flushed table "oplaty"\n')
            Mieszkaniec.objects.all().delete()
            self.stdout.write('Flushed table "mieszkaniec"\n')
            Mieszkanie.objects.all().delete()
            self.stdout.write('Flushed table "mieszkanie"\n')
            Brama.objects.all().delete()
            self.stdout.write('Flushed table "brama"\n')
            Newsy.objects.all().delete()
            self.stdout.write('Flushed table "newsy"\n')
            User.objects.filter(is_staff=False).delete()
            self.stdout.write('Flushed table "user (except root account)\n')

            if len(Mieszkaniec.objects.all()) == 0 and len(Brama.objects.all()) == 0 and len(Mieszkanie.objects.all()) == 0:
                self.stdout.write('Status: OK\n')
            else:
                self.stdout.write('Status: ERROR\n')

        if len(args) >= 1 and args[0].isdigit():
            population_size = int(args[0])
        else:
            population_size = input("Enter population size (default: 20): ")

        if len(args) >= 2 and args[1].isdigit():
            population_per_home = int(args[1])
        else:
            population_per_home = input("Enter population per home (default: 5): ")

        p = Populate(sqlite3.connect(DATABASE_PATH), population_size, population_per_home)
        p.start()
        self.stdout.write('Successfully populated\n')