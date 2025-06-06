import streamlit as st
import pandas as pd
from functions import resquet_name


st.title("App EcoScore")

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
product_null_or_not_null    = st.selectbox(
                                "Sélectionnez le type de produits à afficher :",
                                ("Tous les produits", "Produits avec une note nutritionnelle non nulle", "Produits avec une note ecoscrore non nulle")
                            )



# Bouton exécution
if st.button("Exécuter la requête"):
    try:
        if product_null_or_not_null == "Tous les produits":
            df = resquet_name(product_name, langue, nomber_produit_par_page)
        
            # Outputs
            st.write(f"Nombre de produits trouvés : {len(df)}")    
            st.dataframe(df)
            # Download
            csv = df.to_csv(index=False).encode('utf-8') 
            st.download_button(
                label="📥 Télécharger les données en CSV",
                data=csv,
                file_name='export.csv',
                mime='text/csv'
            )
        
        elif product_null_or_not_null == "Produits avec une note nutritionnelle non nulle":
            df = resquet_name(product_name, langue, nomber_produit_par_page)
            number_product_null = df['nutrition_grades'].isnull().sum()
            df_not_null = df[(df['nutrition_grades'].notnull()) & (df['nutrition_grades'] != 'unknown')]
            
            # Outputs
            st.write(f"Nombre de produits trouvés : {len(df)}")
            st.write(f"Nombre de produits avec une note nutritionnelle nulle : {len(df) - len(df_not_null)}")
            st.write(f"Nombre de produits avec une note nutritionnelle non nulle : {len(df_not_null)}")
            st.dataframe(df_not_null)

            # Download
            csv = df_not_null.to_csv(index=False).encode('utf-8') 
            st.download_button(
                label="📥 Télécharger les données en CSV",
                data=csv,
                file_name='export.csv',
                mime='text/csv'
            )
            
        elif product_null_or_not_null == "Produits avec une note ecoscrore non nulle":
            df = resquet_name(product_name, langue, nomber_produit_par_page)
            number_product_null = df['ecoscore_grade'].isnull().sum()
            df_not_null = df[(df['ecoscore_grade'].notnull()) & (df['ecoscore_grade'] != 'unknown')]
            
            # Outputs
            st.write(f"Nombre de produits trouvés : {len(df)}")
            st.write(f"Nombre de produits avec une note ecoscrore nulle : {len(df) - len(df_not_null)}")
            st.write(f"Nombre de produits avec une note ecoscrore non nulle : {len(df_not_null)}")
            st.dataframe(df_not_null)   
            
            # Download
            csv = df_not_null.to_csv(index=False).encode('utf-8') 
            st.download_button(
                label="📥 Télécharger les données en CSV",
                data=csv,
                file_name='export.csv',
                mime='text/csv'
            )
    except Exception as e:
        st.error(f"Erreur : {e}")

