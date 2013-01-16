from django.core.management.base import BaseCommand, CommandError
from optparse import make_option
import sqlite3
import random
from bazy.models import *

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

            mieszkaniec = Mieszkaniec(
                imie=self.names[i]['imie'],
                nazwisko=self.names[i]['nazwisko']
            )
            mieszkaniec.save()

            Mieszkanie(
                mieszkaniec = mieszkaniec,
                brama = brama,
                numer_mieszkania = (i % self.population_per_home)+1
            ).save()

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
            Mieszkaniec.objects.all().delete()
            self.stdout.write('Flushed table "mieszkaniec"\n')
            Brama.objects.all().delete()
            self.stdout.write('Flushed table "brama"\n')
            Mieszkanie.objects.all().delete()
            self.stdout.write('Flushed table "mieszkanie"\n')

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

        p = Populate(sqlite3.connect('../populate.db'), population_size, population_per_home)
        p.start()
        self.stdout.write('Successfully populated\n')