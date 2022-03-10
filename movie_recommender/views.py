from django.http import HttpResponse, HttpResponseRedirect
from django.shortcuts import render
import pickle
import pandas as pd
import requests


def fetch_poster(id):
    response = requests.get(
        f'https://api.themoviedb.org/3/movie/{id}?api_key=8334251229d9dd3ae1936eab4fc66c62&language=en-US')
    data = response.json()
    return 'https://image.tmdb.org/t/p/w500' + data['poster_path']


def recommend(movie):
    movie_index = movies[movies['title'] == movie].index[0]
    distances = similarity[movie_index]
    movies_list = sorted(list(enumerate(distances)),
                         reverse=True, key=lambda x: x[1])[1:6]

    recommended_movies = []
    recommended_movie_posters = []
    for i in movies_list:
        movie_id = movies.iloc[i[0]].movie_id
        # fetch poster from api
        recommended_movie_posters.append(fetch_poster(movie_id))
        recommended_movies.append(movies.iloc[i[0]].title)
    return recommended_movies, recommended_movie_posters

    # Create your views here.
movies_dict = pickle.load(open('movie_dict.pkl', 'rb'))
movies = pd.DataFrame(movies_dict)

# similarity matrix
similarity = pickle.load(open('similarity.pkl', 'rb'))


def index(request):
    titles = list(movies['title'])
    context = {"movies_list": titles}
    if request.GET.get('selectedMovie'):
        selectedMovie = request.GET.get('selectedMovie')
        recommended_movies, recommended_movie_posters = recommend(
            selectedMovie)
        context["recommended_movies"] = recommended_movies
        context["recommended_movie_posters"] = recommended_movie_posters
        context['selectedMovie'] = selectedMovie

    return render(request, 'movie_recommender/index.html', context)
