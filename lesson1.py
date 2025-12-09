import streamlit as st

def run():
    st.header("🐍 Dzień 1 – Zmienne i typy danych")
    
    st.markdown("""
    ## Czym są zmienne?
    Zmienne to jak pudełka w pamięci komputera, które przechowują dane.
    W Pythonie tworzymy je po prostu przypisując wartość.
    """)
    
    st.code("""# Przykłady zmiennych
nazwa_rośliny = "Pszenica ozima"
powierzchnia_ha = 2.5
czy_nawieziona = True
data_siewu = "2023-09-15"

print("Roślina:", nazwa_rośliny)
print("Powierzchnia:", powierzchnia_ha, "ha")
print("Nawożona?:", czy_nawieziona)
""", language="python")
    
    st.markdown("""
    ### Typy danych w Pythonie:
    - **str** (string) - tekst, np. `"pszenica"`
    - **int** (integer) - liczby całkowite, np. `100`
    - **float** - liczby dziesiętne, np. `25.5`
    - **bool** (boolean) - wartości logiczne `True` lub `False`
    """)
    
    st.subheader("🎯 Ćwiczenie praktyczne")
    
    col1, col2 = st.columns(2)
    
    with col1:
        roślina = st.text_input("Nazwa rośliny:", "Pszenica ozima")
        powierzchnia = st.number_input("Powierzchnia [ha]:", 1.0, 100.0, 2.5)
    
    with col2:
        odmiana = st.selectbox("Odmiana:", ["Boomer", "Aubusson", "KWS Donau"])
        plon = st.slider("Szacowany plon [t/ha]:", 4.0, 12.0, 7.5)
    
    if st.button("🖨️ Wyświetl dane pola"):
        st.success(f"**Dane pola:**")
        st.info(f"Roślina: {roślina}")
        st.info(f"Odmiana: {odmiana}")
        st.info(f"Powierzchnia: {powierzchnia} ha")
        st.info(f"Szacowany plon: {plon} t/ha")
        
        # Obliczenia
        całkowity_plon = powierzchnia * plon
        st.warning(f"**Całkowity szacowany plon: {całkowity_plon:.1f} ton**")
    
    st.divider()
    
    st.subheader("✅ Quiz")
    
    q1 = st.radio(
        "Jakiego typu danych użyjesz do zapisu nazwy rośliny?",
        ["int", "str", "float", "bool"]
    )
    
    if q1:
        if q1 == "str":
            st.success("✅ Poprawnie! Nazwy zapisujemy jako tekst (string).")
        else:
            st.error("❌ Spróbuj jeszcze raz. Nazwy roślin to tekst.")
    
    st.markdown("---")
    st.caption("© Kurs Python - Automatyzacja w rolnictwie")