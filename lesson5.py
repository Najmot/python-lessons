import streamlit as st

def run():
    st.header("📁 Dzień 5 – Praca z plikami")
    st.info("Ta lekcja jest w przygotowaniu. Pobierz aktualizację kursu!")
    
    st.markdown("""
    ## Automatyzacja zadań z plikami
    
    W tej lekcji nauczysz się:
    
    1. Odczytywanie danych z plików CSV (np. dane z kombajnu)
    2. Zapis wyników analiz do plików
    3. Automatyzacja raportów rolniczych
    4. Przetwarzanie danych pogodowych
    
    ### Przykładowy schemat:
    ```python
    # Odczytywanie danych z pliku CSV
    import csv
    
    with open('dane_plonow.csv', 'r') as plik:
        czytnik = csv.reader(plik)
        for wiersz in czytnik:
            print(wiersz)
    ```
    """)