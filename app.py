import streamlit as st
import requests
from PIL import Image
from io import BytesIO

st.set_page_config(page_title="MoodFlix", page_icon="🎬", layout="wide")

# Your OMDb API Key
OMDB_API_KEY = "de463e37"

st.title("🎬 MoodFlix")
st.subheader("Tell us your mood → Get perfect movie recommendations")

# Better & Simpler Mood to Keyword Mapping (works well with OMDb)
mood_to_keywords = {
    "Happy": "comedy",
    "Romantic": "romance",
    "Sad": "drama",
    "Excited": "action",
    "Relaxed": "comedy",
    "Scared": "horror",
    "Angry": "action",
    "Peaceful": "drama"
}

# Questions
col1, col2 = st.columns(2)

with col1:
    energy = st.radio("Energy level right now:", 
                      ["High (Excited)", "Medium", "Low (Chill)"])

with col2:
    emotion = st.selectbox("Main emotion right now:", 
                           ["Happy", "Romantic", "Sad", "Excited", "Relaxed", "Scared", "Angry", "Peaceful"])

if st.button("🎥 Get My Movie Recommendations", type="primary"):
    mood = emotion
    if energy == "High (Excited)":
        mood = "Excited"
    elif energy == "Low (Chill)":
        mood = "Relaxed"

    keyword = mood_to_keywords.get(mood, "comedy")

    with st.spinner(f"Finding {mood} movies for you..."):
        url = f"http://www.omdbapi.com/?apikey={OMDB_API_KEY}&s={keyword}&type=movie"
        response = requests.get(url)
        data = response.json()

        if data.get("Response") == "True" and data.get("Search"):
            movies = data.get("Search", [])[:8]
            
            st.success(f"Here are great movies for your **{mood}** mood! 🎉")

            cols = st.columns(4)
            for i, movie in enumerate(movies):
                with cols[i % 4]:
                    # Get detailed info
                    detail_url = f"http://www.omdbapi.com/?apikey={OMDB_API_KEY}&i={movie['imdbID']}"
                    detail = requests.get(detail_url).json()

                    poster_url = detail.get("Poster")
                    if poster_url and poster_url != "N/A":
                        try:
                            img_response = requests.get(poster_url)
                            img = Image.open(BytesIO(img_response.content))
                            st.image(img, use_column_width=True)
                        except:
                            st.image("https://via.placeholder.com/300x450?text=No+Poster", use_column_width=True)
                    else:
                        st.image("https://via.placeholder.com/300x450?text=No+Poster", use_column_width=True)

                    st.subheader(movie["Title"])
                    st.caption(f"⭐ IMDb: {detail.get('imdbRating', 'N/A')}/10 • {detail.get('Year', '')}")
                    st.caption(f"Genre: {detail.get('Genre', 'N/A')}")
                    st.caption(f"Perfect for {mood.lower()} mood")
                    
                    st.markdown(f"[🔗 View on IMDb](https://www.imdb.com/title/{movie['imdbID']}/)")
        else:
            st.error(f"Sorry, no results found for '{keyword}'. Try a different mood.")

st.caption("MoodFlix • Powered by OMDb API")