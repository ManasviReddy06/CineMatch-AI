import streamlit as st
import pickle
import pandas as pd
import plotly.express as px

movies = pickle.load(open('models/movies.pkl', 'rb'))
similarity = pickle.load(open('models/similarity.pkl', 'rb'))

page = st.sidebar.selectbox(
    "Navigation",
    ["Home", "Mood Recommender", "Analytics", "About"]
)

def recommend(movie):

    movie_index = movies[movies['title'] == movie].index[0]

    distances = similarity[movie_index]

    movies_list = sorted(
        list(enumerate(distances)),
        reverse=True,
        key=lambda x: x[1]
    )[1:6]

    recommendations = []

    for i in movies_list:
        recommendations.append(
            (
                movies.iloc[i[0]].title,
                round(i[1] * 100, 2)
            )
        )

    return recommendations


if page == "Home":

    st.title("🎬 CineMatch AI")

    col1, col2, col3 = st.columns(3)

    with col1:
        st.metric("Movies", "4,818")

    with col2:
        st.metric("Features", "5,000")

    with col3:
        st.metric("Algorithm", "TF-IDF")

    st.markdown("""
    Discover movies you'll love using machine learning-powered recommendations.

    This system analyzes movie content using:
    - Genres
    - Keywords
    - Cast
    - Directors
    - Plot Overview
    """)

    st.markdown("## How It Works")

    st.write("""
    1. User selects a movie.
    2. The system analyzes genres, keywords, cast, directors, and overview.
    3. TF-IDF converts text into vectors.
    4. Cosine Similarity finds related movies.
    5. Top matching movies are recommended.
    """)

    selected_movie = st.selectbox(
        "Choose a Movie",
        sorted(movies['title'].values)
    )

    if st.button("Recommend"):

        recommendations = recommend(selected_movie)

        for movie, score in recommendations:

            with st.container():

                st.markdown("---")

                st.subheader(movie)

                st.metric(
                    label="Match Score",
                    value=f"{score}%"
                )

    st.markdown("---")

    st.caption(
        "Built using Python, Scikit-Learn, Pandas, TF-IDF, Cosine Similarity and Streamlit."
    )
elif page == "Mood Recommender":

    st.title("🎭 Mood-Based Movie Discovery")

    mood = st.selectbox(
        "How are you feeling today?",
        [
            "Mind Bending",
            "Action Packed",
            "Romantic",
            "Feel Good",
            "Sci-Fi"
        ]
    )

    if mood == "Mind Bending":

        movies_list = [
            "Inception",
            "Interstellar",
            "Shutter Island",
            "The Prestige",
            "Memento"
        ]

    elif mood == "Action Packed":

        movies_list = [
            "The Dark Knight",
            "Mad Max: Fury Road",
            "Gladiator",
            "Avatar",
            "John Carter"
        ]

    elif mood == "Romantic":

        movies_list = [
            "Titanic",
            "The Notebook",
            "Pearl Harbor",
            "A Walk to Remember",
            "The Great Gatsby"
        ]

    elif mood == "Feel Good":

        movies_list = [
            "Finding Nemo",
            "Up",
            "Toy Story",
            "Frozen",
            "Ratatouille"
        ]

    else:

        movies_list = [
            "Interstellar",
            "Avatar",
            "The Martian",
            "Gravity",
            "Star Trek"
        ]

    st.subheader("Recommended Movies")

    for movie in movies_list:
        st.success(movie)
elif page == "Analytics":

    st.title("📊 Analytics Dashboard")

    st.subheader("Top 10 Most Frequent Keywords")

    keyword_count = {}

    for tags in movies['tags']:

        words = tags.split()

        for word in words:
            keyword_count[word] = keyword_count.get(word, 0) + 1

    df = pd.DataFrame(
        keyword_count.items(),
        columns=['Keyword', 'Count']
    )

    df = df.sort_values(
        by='Count',
        ascending=False
    ).head(10)

    fig = px.bar(
        df,
        x='Keyword',
        y='Count',
        title='Most Frequent Keywords'
    )

    st.plotly_chart(fig, use_container_width=True)

elif page == "About":

    st.title("About CineMatch AI")

    st.write("""
    CineMatch AI is a machine learning based movie recommendation system.

    Technologies Used:
    - Python
    - Pandas
    - Scikit-Learn
    - TF-IDF
    - Cosine Similarity
    - Streamlit
    """)