from collections import defaultdict
from django.conf import settings
from django.http import HttpRequest, HttpResponse
import psycopg2


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
        CREATE TABLE ex00_movies(
            title VARCHAR(64) UNIQUE NOT NULL,
            episode_nb INTEGER PRIMARY KEY,
            opening_crawl TEXT,
            producer VARCHAR(128) NOT NULL,
            director VARCHAR(32) NOT NULL,
            release_date DATE NOT NULL
        );
        COMMIT;
        """

        with conn.cursor() as curs:
            curs.execute(SQL_QUERY)
    except Exception as e:
        return HttpResponse("Data already handled") 
    return HttpResponse("OK")


