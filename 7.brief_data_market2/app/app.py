import streamlit as st
from functions import *

st.title("App EcoScore")
st.markdown("---")

# Ajouter un utilisateur
st.subheader('Ajouter un utilisateur')
nom = st.text_input("Entrez le nom de l'utilisateur :", "Utilisateur1")
email = st.text_input("Entrez l'email de l'utilisateur :", "user1")
if st.button("Ajouter l'utilisateur"):
    insert_user(nom, email)
    st.success(f"Utilisateur {nom} ajouté avec succès.")
    
st.markdown("---")
st.subheader('Requete')
product_name                = st.text_input("Entrez le nom d'un produit :", "Nutella")
langue                      = st.selectbox(
                                "Sélectionnez la langue des produits à afficher :",
                                ("*", "fr", "en", "de", "es", "it", "nl", "pt", "pl", "ru", "zh")
                            )
nomber_produit_par_page     = st.number_input(
                                "Nombre de produits par page :",
                                min_value=1,
                                max_value=1000,
                                value=10,
                                step=1
                            )

# Bouton exécution
if st.button("Exécuter la requête"):
    try:
        # Récupération des produits
        st.session_state.df = resquet_name(product_name, langue, nomber_produit_par_page)

    except Exception as e:
        st.error(f"Erreur lors de l'exécution de la requête : {e}")

# Si on a déjà des résultats stockés
if "df" in st.session_state:
    df = st.session_state.df

    # Outputs
    st.write(f"Nombre de produits trouvés : {len(df)}")    
    st.dataframe(df)

    # Sélectionner un utilisateur 
    user_list = get_user_id()
    if len(user_list) == 0:
        st.warning("Aucun utilisateur trouvé. Veuillez ajouter un utilisateur avant d'insérer des produits.")

    else:
        user_names = [user[0] for user in user_list]
        selected_user = st.selectbox("Sélectionnez un utilisateur :", user_names)
        user_id = [user[1] for user in user_list if user[0] == selected_user][0]

        if st.button("Insérer les produits dans la base de données"):
            try:
                insert_products(df, user_id)
                st.success(f"Produits insérés avec succès pour l'utilisateur {selected_user}.")
            except Exception as e:
                st.error(f"Erreur lors de l'insertion en base : {e}")
