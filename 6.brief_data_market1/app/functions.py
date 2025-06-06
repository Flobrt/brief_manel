import requests as re
import pandas as pd


def resquet_name(product_name: str, langue: str = '*', page_size: int = 10) -> pd.DataFrame:
    '''
        Function to request product data from Open Food Facts based on product name and language.
        Parameters:
            - product_name (str): The name of the product to search for.
            - langue (str): The language code for the product data. Default is '*', which means all languages.
            - page_size (int): The number of products to return per page. Default is 10.
        Returns:
            - pd.DataFrame: A DataFrame containing the product data with columns for product name, language, brands, nutrition grades, and ecoscore grade.
    '''
    
    if langue == '*':
        product_name = product_name.lower()
        url = f"https://search.openfoodfacts.org/search?q={product_name}&page_size={page_size}&page=1&fields=product_name%2Clang%2Cbrands%2Cnutrition_grades%2Cecoscore_grade"
        df = pd.DataFrame(re.get(url).json().get('hits'))
    
    else: 
        product_name = product_name.lower()
        url = f"https://search.openfoodfacts.org/search?langs={langue}&q={product_name}&page_size={page_size}&page=1&fields=product_name%2Clang%2Cbrands%2Cnutrition_grades%2Cecoscore_grade"
        df = pd.DataFrame(re.get(url).json().get('hits'))
        
    return df