from collections import defaultdict
from django.conf import settings
from django.http import HttpRequest, HttpResponse
import psycopg2
from django.shortcuts import render, redirect
from django import forms


def init(request: HttpRequest):
    try:
        conn = psycopg2.connect(
            dbname=settings.DATABASES['default']['NAME'],
            user=settings.DATABASES['default']['USER'],
            password=settings.DATABASES['default']['PASSWORD'],
            host=settings.DATABASES['default']['HOST'],
            port=settings.DATABASES['default']['PORT'],
        )
        SQL_QUERY = """
        CREATE TABLE ex06_movies(
            title VARCHAR(64) UNIQUE NOT NULL,
            episode_nb INTEGER PRIMARY KEY,
            opening_crawl TEXT,
            producer VARCHAR(128) NOT NULL,
            director VARCHAR(32) NOT NULL,
            release_date DATE NOT NULL,
            created TIMESTAMP NOT NULL DEFAULT NOW(),
            updated TIMESTAMP NOT NULL DEFAULT NOW()
        );
        CREATE OR REPLACE FUNCTION update_changetimestamp_column()
        RETURNS TRIGGER AS $$
        BEGIN
        NEW.updated = now(); NEW.created = OLD.created;
        RETURN NEW;
        END;
        $$ language 'plpgsql';
        CREATE TRIGGER update_films_changetimestamp BEFORE UPDATE
        ON ex06_movies FOR EACH ROW EXECUTE PROCEDURE 
        update_changetimestamp_column();
        """
        with conn.cursor() as curs:
            curs.execute(SQL_QUERY)
        conn.commit()
    except Exception as e:
        return HttpResponse(e)
    return HttpResponse("OK")


def populate(request):
    movies = [
        {
            "episode_nb": 1,
            "title": "The Phantom Menace",
            "director": "George Lucas",
            "producer": "Rick McCallum",
            "release_date": "1999-05-19"
        },
        {
            "episode_nb": 2,
            "title": "Attack of the Clones",
            "director": "George Lucas",
            "producer": "Rick McCallum",
            "release_date": "2002-05-16"
        },
        {
            "episode_nb": 3,
            "title": "Revenge of the Sith",
            "director": "George Lucas",
            "producer": "Rick McCallum",
            "release_date": "2005-05-19"
        },
        {
            "episode_nb": 4,
            "title": "A New Hope",
            "director": "George Lucas",
            "producer": "Gary Kurtz, Rick McCallum",
            "release_date": "1977-05-25"
        },
        {
            "episode_nb": 5,
            "title": "The Empire Strikes Back",
            "director": "Irvin Kershner",
            "producer": "Gary Kurtz, Rick McCallum",
            "release_date": "1980-05-17"
        },
        {
            "episode_nb": 6,
            "title": "Return of the Jedi",
            "director": "Richard Marquand",
            "producer": "Howard G. Kazanjian, George Lucas, Rick McCallum",
            "release_date": "1983-05-25"
        },
        {
            "episode_nb": 7,
            "title": "The Force Awakens",
            "director": "J. J. Abrams",
            "producer": "Kathleen Kennedy, J. J. Abrams, Bryan Burk",
            "release_date": "2015-12-11"
        }
    ]
    try:
        result = []
        conn = psycopg2.connect(
            dbname=settings.DATABASES['default']['NAME'],
            user=settings.DATABASES['default']['USER'],
            password=settings.DATABASES['default']['PASSWORD'],
            host=settings.DATABASES['default']['HOST'],
            port=settings.DATABASES['default']['PORT'],
        )
        SQL_QUERY = """
        INSERT INTO ex06_movies(
            episode_nb, 
            title, 
            director, 
            producer, 
            release_date
        )
        VALUES(
            %s, %s, %s, %s, %s
        );
        """
        with conn.cursor() as curs:
            for movie in movies:
                try:
                    curs.execute(SQL_QUERY, [
                        movie['episode_nb'],
                        movie['title'],
                        movie['director'],
                        movie['producer'],
                        movie['release_date']])
                    result.append("OK")
                    conn.commit()
                except psycopg2.DatabaseError as e:
                    result.append(e)
                    conn.rollback()                                   
    except Exception as e:
        return HttpResponse("No data available") 
    return HttpResponse("<br />".join([str(i) for i in result]))


def display(request):
    try:
        conn = psycopg2.connect(
            dbname=settings.DATABASES['default']['NAME'],
            user=settings.DATABASES['default']['USER'],
            password=settings.DATABASES['default']['PASSWORD'],
            host=settings.DATABASES['default']['HOST'],
            port=settings.DATABASES['default']['PORT'],
        )
        SQL_QUERY = """
        SELECT * FROM ex06_movies;
        """
        with conn.cursor() as curs:
            curs.execute(SQL_QUERY)
            tuple_list = curs.fetchall()
    except Exception as e:
        return HttpResponse("No data available") 
    return render(request, 'base_06.html', {'movies': tuple_list})

class TextChoose(forms.Form):
    titles = forms.ChoiceField(choices=(), required=True)
    update = forms.CharField(required=True)
    def __init__(self, choices=(), *args, **kwargs):
        super(TextChoose, self).__init__(*args, **kwargs)
        self.fields['titles'].choices = choices

def update(request: HttpRequest):
    try:
        conn = psycopg2.connect(
            dbname=settings.DATABASES['default']['NAME'],
            user=settings.DATABASES['default']['USER'],
            password=settings.DATABASES['default']['PASSWORD'],
            host=settings.DATABASES['default']['HOST'],
            port=settings.DATABASES['default']['PORT'],
        )
        SQL_QUERY = """
        SELECT * FROM ex06_movies;
        """
        curs = conn.cursor()
        curs.execute(SQL_QUERY)
        movies = curs.fetchall()
        choices = ((movie[0], movie[0]) for movie in movies)
        if request.method == 'POST':
            data = TextChoose(choices, request.POST)
            if data.is_valid():
                SQL_QUERY = """
                UPDATE ex06_movies SET opening_crawl = %s WHERE title = %s;
                """
                curs.execute(SQL_QUERY, [data.cleaned_data['update'], data.cleaned_data['titles']])
                conn.commit()
            curs.close()
            return redirect(request.path)
        curs.close()
        return render(request, 'remove_05.html', {'choice_field': TextChoose(choices)})
    except Exception as e:
        print(e)
        return HttpResponse("No data available")
