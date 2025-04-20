import streamlit as st
import pandas as pd
import seaborn as sns
import matplotlib.pyplot as plt
from collections import Counter

# App configuration
st.set_page_config(page_title = "Netflix EDA", layout = "wide")
sns.set(style = 'whitegrid')

# Load dataset
@st.cache_data
def load_data():
    df = pd.read_csv("netflix_titles.csv")
    df['date_added'] = pd.to_datetime(df['date_added'], format = 'mixed', errors = 'coerce')
    df['year_added'] = df['date_added'].dt.year
    return df.drop_duplicates()

df = load_data()


# Sidebar
st.sidebar.title("Netflix EDA Dashboard")
st.sidebar.markdown("Use this app to explore Netflix TV Shows & Movies.")

# App title
st.title("Netflix Movies & TV Shows - EDA")
st.markdown("""
Welcome to an interactive data visualization dashboard for Netflix content.  
Use the charts below to explore insights about content types, release trends, countries, ratings, and genres.
""")

# Layout: 2 Columns - Type & Country
col1, col2 = st.columns(2)

with col1:
    st.subheader("Content Type Distribution")
    sns.countplot(data = df, x = 'type')
    st.pyplot(plt.gcf())
    plt.clf()

with col2:
    st.subheader("Top 10 Countries with Most Content")
    top_countries = df['country'].value_counts().head(10)
    top_countries.plot(kind = 'barh', color = 'tomato')
    plt.xlabel("Number of Titles")
    plt.gca().invert_yaxis()
    st.pyplot(plt.gcf())
    plt.clf()

# Content Added Per Year
st.subheader("Content Added to Netflix Per Year")
df['year_added'].value_counts().sort_index().plot(kind = 'bar', color = 'skyblue')
plt.xlabel("Year")
plt.ylabel("Number of Titles Added")
st.pyplot(plt.gcf())
plt.clf()

# Most Common Ratings
st.subheader("Most Common Content Ratings")
sns.countplot(data = df, y = 'rating', order = df['rating'].value_counts().index[:10], palette='viridis')
plt.xlabel("Count")
plt.ylabel("Rating")
st.pyplot(plt.gcf())
plt.clf()

# Most Common Genres
st.subheader("Top 10 Genres on Netflix")
genre_list = df['listed_in'].dropna().str.split(', ')
flat_genres = [genre for sublist in genre_list for genre in sublist]
genre_counts = Counter(flat_genres)
genre_df = pd.DataFrame(genre_counts.most_common(10), columns = ['Genre', 'Count'])
sns.barplot(x = 'Count', y = 'Genre', data = genre_df, palette='pastel')
st.pyplot(plt.gcf())
plt.clf()

# Footer
st.markdown("---")
st.markdown("Made with ❤️ using Streamlit · Data source: [Netflix Kaggle Dataset](https://www.kaggle.com/datasets/shivamb/netflix-shows)")