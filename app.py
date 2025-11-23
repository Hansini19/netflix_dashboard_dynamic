import streamlit as st
import pandas as pd
import plotly.express as px

# Load dynamic dataset
URL = "https://raw.githubusercontent.com/Hansini19/netflix_dashboard_dynamic/refs/heads/main/netflix_titles.csv"
df = pd.read_csv(URL)

st.set_page_config(page_title="Netflix Dashboard", layout="wide")
st.title("📊 Netflix Movies & TV Series Dashboard")

# Sidebar filters
st.sidebar.header("Filters")
selected_type = st.sidebar.multiselect("Select Type", df['type'].unique())
selected_country = st.sidebar.multiselect("Select Country", df['country'].dropna().unique())
selected_year = st.sidebar.slider("Release Year", 1925, 2021, (1925, 2021))

# Apply filters
filtered_df = df.copy()

if selected_type:
    filtered_df = filtered_df[filtered_df["type"].isin(selected_type)]
if selected_country:
    filtered_df = filtered_df[filtered_df["country"].isin(selected_country)]

filtered_df = filtered_df[
    (filtered_df["release_year"] >= selected_year[0]) &
    (filtered_df["release_year"] <= selected_year[1])
]

# KPIs
col1, col2, col3 = st.columns(3)
col1.metric("Total Titles", len(filtered_df))
col2.metric("Movies Count", len(filtered_df[filtered_df["type"] == "Movie"]))
col3.metric("TV Shows Count", len(filtered_df[filtered_df["type"] == "TV Show"]))

st.markdown("---")

# 1. Pie Chart - Movies vs TV Shows
fig1 = px.pie(filtered_df, names='type', title="Movies vs TV Shows")
st.plotly_chart(fig1, use_container_width=True)

# 2. Content Added Over Years (Line Chart)
year_count = filtered_df['release_year'].value_counts().reset_index()
year_count.columns = ['year', 'count']
fig2 = px.line(year_count.sort_values('year'), x='year', y='count',
               title="Content Added Over the Years")
st.plotly_chart(fig2, use_container_width=True)

# 3. Top Genres (Bar Chart)
df['listed_in'] = df['listed_in'].astype(str)
all_genres = df['listed_in'].str.split(',').explode().str.strip()
top_genres = all_genres.value_counts().head(10).reset_index()
top_genres.columns = ['genre', 'count']

fig3 = px.bar(top_genres, x='genre', y='count', title="Top 10 Genres")
st.plotly_chart(fig3, use_container_width=True)

# 4. Duration Distribution (Box Plot)
movies_df = df[df['type'] == 'Movie'].copy()
movies_df['duration_num'] = movies_df['duration'].str.replace(" min", "", regex=False).astype(float)

fig4 = px.box(movies_df, y='duration_num', title="Movie Duration Distribution (Minutes)")
st.plotly_chart(fig4, use_container_width=True)

# 5. Histogram of Release Years
fig5 = px.histogram(df, x='release_year', nbins=30, title="Release Year Distribution")
st.plotly_chart(fig5, use_container_width=True)

# 6. Country with Most Content (Horizontal Bar Chart)
country_count = df['country'].dropna().str.split(',').explode().str.strip().value_counts().head(10)
country_df = country_count.reset_index()
country_df.columns = ['country', 'count']

fig6 = px.bar(country_df, x='count', y='country', orientation='h',
              title="Top 10 Countries by Content")
st.plotly_chart(fig6, use_container_width=True)

# 7. Genre Treemap
fig7 = px.treemap(top_genres, path=['genre'], values='count',
                  title="Genre Treemap")
st.plotly_chart(fig7, use_container_width=True)

# 8. Heatmap: Country vs Release Year
heatmap_df = df[['country', 'release_year']].dropna()
heatmap_df['country'] = heatmap_df['country'].str.split(',').str[0]

pivot = heatmap_df.pivot_table(index='country', columns='release_year', aggfunc='size', fill_value=0)

fig8 = px.imshow(pivot, aspect="auto", title="Heatmap: Country vs Release Year")
st.plotly_chart(fig8, use_container_width=True)
