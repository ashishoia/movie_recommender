import streamlit as st
import pandas as pd
import numpy as np
import pickle
import requests
import time

movies = pickle.load(open("model/movie_list.pkl", "rb"))
similar = pickle.load(open("model/similarity.pkl", "rb"))
movies_df = pd.DataFrame(movies)


def fetch_poster(movies_id):
    tmdb_id = movies_id
    api_key = "330018326c4140e05777de814498a62a"

    url = f"https://api.themoviedb.org/3/movie/{tmdb_id}?api_key={api_key}"

    headers = {
        "accept": "application/json",
        "Authorization": "Bearer 330018326c4140e05777de814498a62a"
    }

    response = requests.get(url, headers=headers)
    data = response.json()

    return "https://image.tmdb.org/t/p/w500/" + data['poster_path']


def fetch_link(movies_id):
    tmdb_id = movies_id
    api_key = "330018326c4140e05777de814498a62a"

    url = f"https://api.themoviedb.org/3/movie/{tmdb_id}?api_key={api_key}"

    headers = {
        "accept": "application/json",
        "Authorization": "Bearer 330018326c4140e05777de814498a62a"
    }

    response = requests.get(url, headers=headers)
    data = response.json()

    return data['homepage']


def recommendation(movie_name):
    movie_index = movies_df[movies_df['title'] == movie_name].index[0]
    distances = similar[movie_index]
    movies_list = sorted(list(enumerate(distances)), reverse=True, key=lambda x: x[1])[
                  1:6]  # it returns an array of tuples

    poster = []
    for j in movies_list:
        movies_id = movies_df.iloc[j[0]].movie_id
        poster.append(fetch_poster(movies_id))

    link = []
    for k in movies_list:
        movies_id = movies_df.iloc[k[0]].movie_id
        link.append(fetch_link(movies_id))
    movies_recommended = []
    for i in movies_list:  # i is a tuple here
        movies_recommended.append(movies_df.iloc[i[0]].title)  # i[0] will give me the index of that movie
    return movies_recommended, poster, link


disclaimer_message = (
    "Dear User,\n\n"
    "We are committed to providing you with the best movie recommendations based on the available data. "
    "We are constantly working to enhance our movie database and recommend the latest films. "
    "However, please note that the dataset may not be exhaustive, and there might be chances of errors or omissions. "
    "We appreciate your understanding and apologize for any inconvenience caused."
)




st.title(':grey[_Movie_]  :red[Recommender] :sunglasses:')

selected_movie = st.sidebar.selectbox('Select movies to recommend', movies_df['title'].values)

if st.button('Recommend movie'):
    name, poster1, link1 = recommendation(selected_movie)
    col1, col2, = st.columns(2)
    with col1:
        st.markdown(f"<div style='white-space: pre-wrap;'>{name[0]}</div>", unsafe_allow_html=True)
        st.markdown(f"<img src='{poster1[0]}' style='border-radius: 10px; max-width: 100%;' />", unsafe_allow_html=True)
        st.markdown(link1[0], unsafe_allow_html=True)
    with col2:
        st.markdown(f"<div style='white-space: pre-wrap;'>{name[1]}</div>", unsafe_allow_html=True)
        st.markdown(f"<img src='{poster1[1]}' style='border-radius: 10px; max-width: 100%;' />", unsafe_allow_html=True)
        st.markdown(link1[1], unsafe_allow_html=True)
    col3, col4 = st.columns(2)
    with col3:
        st.markdown(f"<div style='white-space: pre-wrap;'>{name[2]}</div>", unsafe_allow_html=True)
        st.markdown(f"<img src='{poster1[2]}' style='border-radius: 10px; max-width: 100%;' />", unsafe_allow_html=True)
        st.markdown(link1[2], unsafe_allow_html=True)
    with col4:
        st.markdown(f"<div style='white-space: pre-wrap;'>{name[3]}</div>", unsafe_allow_html=True)
        st.markdown(f"<img src='{poster1[3]}' style='border-radius: 10px; max-width: 100%;' />", unsafe_allow_html=True)
        st.markdown(link1[3], unsafe_allow_html=True)
    col5, col6 = st.columns(2)
    with col5:
        st.markdown(f"<div style='white-space: pre-wrap;'>{name[4]}</div>", unsafe_allow_html=True)
        st.markdown(f"<img src='{poster1[4]}' style='border-radius: 10px; max-width: 100%;' />", unsafe_allow_html=True)
        st.markdown(link1[4], unsafe_allow_html=True)


if st.button("Disclaimer"):
    disclaimer_placeholder = st.empty()
    disclaimer_placeholder.info(disclaimer_message)
    time.sleep(5)  # Adjust the delay as needed
    disclaimer_placeholder.empty()
