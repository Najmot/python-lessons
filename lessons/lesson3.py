import streamlit as st

def run():
    st.header("🔄 Dzień 3 – Pętle i struktury danych")
    st.info("Ta lekcja jest w przygotowaniu. Pobierz aktualizację kursu!")
    
    st.markdown("""
    ## Co nauczysz się w tej lekcji?
    
    1. **Pętle for** - automatyzacja powtarzających się zadań
    2. **Listy** - przechowywanie kolekcji danych
    3. **Słowniki** - struktury klucz-wartość
    4. **Praktyczny przykład**: Analiza plonów z wielu pól
    
    ## Przykładowy kod:
    ```python
    # Lista plonów z różnych pól
    plony = [7.8, 8.2, 6.9, 9.1, 7.5]
    
    # Obliczanie średniego plonu
    suma = 0
    for plon in plony:
        suma += plon
    
    średni_plon = suma / len(plony)
    print(f"Średni plon: {średni_plon} t/ha")
    ```
    """)
    
    if st.button("Przetestuj pętlę for"):
        plony = [7.8, 8.2, 6.9, 9.1, 7.5]
        
        st.write("**Plony z poszczególnych pól [t/ha]:**")
        for i, plon in enumerate(plony, 1):
            st.write(f"Pole {i}: {plon} t/ha")
        
        średni = sum(plony) / len(plony)
        st.success(f"Średni plon: {średni:.2f} t/ha")
