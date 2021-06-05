from ex.ex0.models import Article
from django.shortcuts import redirect, redirect


def populate(request):
    movie_list = [
        {
            "title": 1,
            "author": "The Phantom Menace",
            "synopsis": "Rick McCallum",
            "content": "1999-05-19"
        },
        {
            "title": 2,
            "author": "The Phantom Menace",
            "synopsis": "Rick McCallum",
            "content": "1999-05-19"
        },
         {
            "title": 3,
            "author": "The Phantom Menace",
            "synopsis": "Rick McCallum",
            "content": "1999-05-19"
        },
         {
            "title": 4,
            "author": "The Phantom Menace",
            "synopsis": "Rick McCallum",
            "content": "1999-05-19"
        }
    ]
    result = []
    for i in movie_list:
        try:
            Article.objects.create(
                title=i['title'],
                episode_nb=i['episode_nb'],
                director=i['director'],
                producer=i['producer'],
                release_date=i['release_date']
            )
            result.append("OK")
        except Exception as e:
            result.append(e)
    return HttpResponse("<br />".join([str(i) for i in result]))