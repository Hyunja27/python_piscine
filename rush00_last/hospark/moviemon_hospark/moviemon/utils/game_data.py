from ..settings import basic_data
from typing import Dict, List, Tuple
import requests
import json
import pickle
import random
import os

def load_data(path:str="session.bin"):
    try:
        f = open(path, "rb")
        data = pickle.load(f)
        f.close()
        return data
    except Exception as e:
        return None

def save_data(data, path:str="session.bin"):
    try:
        f = open(path,"wb")
        pickle.dump(data, f)
        f.close()
        return data
    except:
        return None

def make_save_dir():
    if not os.path.isdir("saved_game"):
        os.mkdir("saved_game")

def save_session_data(data):
    make_save_dir()
    try:
        f = open("saved_game/session.bin", "wb")
        pickle.dump(data, f)
        f.close()
        return data
    except:
        return None

class G_Data():
    px: int = basic_data.PLAYER_INIT_POSITION[0]
    py: int = basic_data.PLAYER_INIT_POSITION[1]
    captured_list: list = []
    left_moviemon: list = []
    moviemon: dict = {}
    total_moviemon: list = []
    movieballCount: int = basic_data.START_BALL_AMOUNT
    strength : int = len(captured_list)

    def dump(self):
        return {
            "px": self.px,
            "py": self.py,
            "captured_list": self.captured_list,
            "left_moviemon": self.left_moviemon,
            "total_moviemon": self.total_moviemon,
            "moviemon": self.moviemon,
            "movieballCount" : self.movieballCount,
            "strength" : self.strength
        }

    def load(data):
        result = G_Data()
        result.px = data["px"]
        result.py = data["py"]
        result.captured_list = data["captured_list"]
        result.left_moviemon = data["left_moviemon"]
        result.total_moviemon = data["total_moviemon"]
        result.movieballCount = data["movieballCount"]
        result.strength = len(data["captured_list"])
        return result

    def get_random_movie(self):
        pick = random.randint(0, len(self.left_moviemon) - 1)
        return self.left_moviemon[pick]

    def get_movie(self, id):
        temp = {}
        for i in self.total_moviemon:
            for key, values in i.items() :
                temp[key] = values
        return temp[id]

    def get_strength(self):
        return len(self.captured_list)

    def load_default_settings():
        result = G_Data()
        URL = "http://www.omdbapi.com/"
        for id in basic_data.IMDB_LIST:
            params = {
                "apikey": basic_data.OMDB_API_KEY,
                "i": id
            }
            try:
                data = requests.get(URL, params=params).json()
                result.moviemon[id] = {
                    "title": data["Title"],
                    "year": data["Year"],
                    "director": data["Director"],
                    "poster": data["Poster"],
                    "rating": float(data["imdbRating"]),
                    "plot": data["Plot"],
                    "actors": data["Actors"],
                }
            except Exception as e:
                assert e
        return result






        # f = open("test.json", 'r')
        # data = json.load(f)
        # f.close()
        # for key, value in data.items():
        #     result.captured_list.append(key)
        #     result.moviemon[key] = {
        #         "title": value["Title"],
        #         "year": value["Year"],
        #         "director": value["Director"],
        #         "poster": value["Poster"],
        #         "rating": float(value["imdbRating"]),
        #         "plot": value["Plot"],
        #         "actors": value["Actors"],
        #     }