from collections import defaultdict
from django.conf import settings
from django.http import HttpRequest, HttpResponse
import psycopg2
from django.shortcuts import render, redirect
from django import forms
import json


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
        CREATE TABLE ex08_planets(
            id SERIAL PRIMARY KEY,
            name VARCHAR(64) UNIQUE NOT NULL,
            climate VARCHAR(128),
            diameter INTEGER,
            orbital_period INTEGER,
            population bigint,
            rotation_period INTEGER,
            surface_water real,
            terrain VARCHAR(128)
        );
        CREATE TABLE ex08_people(
            id SERIAL PRIMARY KEY,
            name VARCHAR(64) UNIQUE NOT NULL,
            birth_year VARCHAR(32),
            gender VARCHAR(32),
            eye_color VARCHAR(32),
            hair_color VARCHAR(32),
            height bigint,
            mass real,
            homeworld VARCHAR(64) REFERENCES ex08_planets(name)
        );
        """
        with conn.cursor() as curs:
            curs.execute(SQL_QUERY)
        conn.commit()
    except Exception as e:
        return HttpResponse(e)
    return HttpResponse("OK")


def populate(request):
    result = []
    conn = psycopg2.connect(
        dbname=settings.DATABASES['default']['NAME'],
        user=settings.DATABASES['default']['USER'],
        password=settings.DATABASES['default']['PASSWORD'],
        host=settings.DATABASES['default']['HOST'],
        port=settings.DATABASES['default']['PORT'],
    )
    SQL_QUERY1 = """
    INSERT INTO ex08_planets(
        name,
        climate,
        diameter,
        orbital_period,
        population,
        rotation_period,
        surface_water,
        terrain
    )
    VALUES(
        %s, %s, %s, %s, %s, %s, %s, %s
    );
    """
    planet_list=[]
    fd = open("ex08/planets.csv", 'r')
    while True:
        line = fd.readline()
        if not line: break
        tmp = line.split('	')
        planet_list.append(tmp)
    with conn.cursor() as curs:
        for p in planet_list:
            try:
                curs.execute(SQL_QUERY1, [
                    p[0] if p[0] != 'NULL' else None,
                    p[1] if p[1] != 'NULL' else None,
                    p[2] if p[2] != 'NULL' else None,
                    p[3] if p[3] != 'NULL' else None,
                    p[4] if p[4] != 'NULL' else None,
                    p[5] if p[5] != 'NULL' else None,
                    p[6] if p[6] != 'NULL' else None,
                    p[7] if p[7] != 'NULL' else None
                    ])
                result.append("OK")
                conn.commit()
            except psycopg2.DatabaseError as e:
                result.append(e)
                conn.rollback()  
        result.append("  ====== planet inserted!  ====== ")
    curs.close()
    fd.close()
    SQL_QUERY2 = """
    INSERT INTO ex08_people(
        name,
        birth_year,
        gender,
        eye_color,
        hair_color,
        height,
        mass,
        homeworld
    )
    VALUES(
        %s, %s, %s, %s, %s, %s, %s, %s
    );
    """
    people_list=[]
    fd = open("ex08/people.csv", 'r')
    while True:
        line = fd.readline()
        if not line: break
        tmp = line.split('	')
        people_list.append(tmp)
    with conn.cursor() as curs:
        for n in people_list:
            try:
                curs.execute(SQL_QUERY2, [
                    n[0] if n[0] != 'NULL' else None,
                    n[1] if n[1] != 'NULL' else None,
                    n[2] if n[2] != 'NULL' else None,
                    n[3] if n[3] != 'NULL' else None,
                    n[4] if n[4] != 'NULL' else None,
                    n[5] if n[5] != 'NULL' else None,
                    n[6] if n[6] != 'NULL' else None,
                    n[7].strip() if n[7].strip() != 'NULL' else None
                    ])
                result.append("OK")
                conn.commit()
            except psycopg2.DatabaseError as e:
                result.append(e)
                conn.rollback() 
    fd.close()
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
        SQL_QUERY1 = """
        select ex08_people.name,homeworld,ex08_planets.climate from ex08_people right join ex08_planets on ex08_people.homeworld = ex08_planets.name where ex08_planets.climate like '%windy%' order by ex08_people.name;
        """
        with conn.cursor() as curs:
            curs.execute(SQL_QUERY1)
            datas = curs.fetchall()

    except Exception as e:
        return HttpResponse("No data available") 
    return render(request, 'base_08_sort.html', {'peoples': datas})
