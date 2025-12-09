import streamlit as st

def run():
    st.header("⚙️ Dzień 4 – Funkcje i moduły")
    st.info("Ta lekcja jest w przygotowaniu. Pobierz aktualizację kursu!")
    
    st.markdown("""
    ## Funkcje w Pythonie
    
    Funkcje pozwalają na grupowanie kodu, który można wielokrotnie używać.
    
    ### Przykład funkcji do obliczeń rolniczych:
    ```python
    def oblicz_plon(powierzchnia, plon_na_ha):
        \"\"\"
        Oblicza całkowity plon z pola.
        
        Parametry:
        powierzchnia -- powierzchnia w hektarach
        plon_na_ha -- plon w tonach na hektar
        
        Zwraca:
        Całkowity plon w tonach
        \"\"\"
        return powierzchnia * plon_na_ha
    
    # Użycie funkcji
    wynik = oblicz_plon(5.2, 8.3)
    print(f"Plon: {wynik} ton")
    ```
    """)