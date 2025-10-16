import streamlit as st
from functions import insert_game, get_games, get_merged_data

st.title("App Ecogames")
st.markdown("---")

# Ajouter un utilisateur
st.subheader('Ajouter un jeu')
nom = st.text_input("Entrez le nom du jeu :", "Celeste")
url = st.text_input("Entrez son URL instant gaming:", "https://www.instant-gaming.com/en/8003-buy-celeste-pc-mac-game-steam/")
if st.button("Ajouter le jeu"):
    insert_game(nom, url)
    st.success(f"Jeu {nom} ajouté avec succès.")

df = get_games()
st.markdown("---")
st.subheader("Jeux dans la base de données")
st.dataframe(df)

st.markdown("---")
st.subheader("Jeux et leurs prix")
df_prices = get_merged_data()
st.dataframe(df_prices)