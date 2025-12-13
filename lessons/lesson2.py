import streamlit as st

def run():
    st.header("🔢 Dzień 2 – Operacje matematyczne i warunki")
    
    st.markdown("""
    ## Operacje matematyczne w Pythonie
    Python może wykonywać wszystkie podstawowe operacje matematyczne.
    """)
    
    st.code("""# Operacje na danych rolniczych
powierzchnia = 5.2  # ha
plon_na_ha = 8.3   # t/ha

# Mnożenie - obliczanie całkowitego plonu
całkowity_plon = powierzchnia * plon_na_ha
print(f"Całkowity plon: {całkowity_plon:.1f} ton")

# Dzielenie - obliczanie potrzebnego nawozu
nawóz_na_ha = 150  # kg/ha
całkowity_nawóz = powierzchnia * nawóz_na_ha
print(f"Potrzebny nawóz: {całkowity_nawóz} kg")
""", language="python")
    
    st.subheader("🧮 Kalkulator nawożenia")
    
    col1, col2 = st.columns(2)
    
    with col1:
        powierzchnia = st.number_input("Powierzchnia [ha]:", 0.1, 100.0, 5.0, key="l2_pow")
        dawka_n = st.number_input("Dawka N [kg/ha]:", 0, 300, 150, key="l2_n")
    
    with col2:
        dawka_p = st.number_input("Dawka P₂O₅ [kg/ha]:", 0, 200, 80, key="l2_p")
        dawka_k = st.number_input("Dawka K₂O [kg/ha]:", 0, 200, 120, key="l2_k")
    
    if st.button("Oblicz potrzeby nawozowe"):
        całkowite_N = powierzchnia * dawka_n
        całkowite_P = powierzchnia * dawka_p
        całkowite_K = powierzchnia * dawka_k
        
        st.success("**Potrzeby nawozowe:**")
        
        col_a, col_b, col_c = st.columns(3)
        with col_a:
            st.metric("Azot (N)", f"{całkowite_N:.0f} kg")
        with col_b:
            st.metric("Fosfor (P₂O₅)", f"{całkowite_P:.0f} kg")
        with col_c:
            st.metric("Potas (K₂O)", f"{całkowite_K:.0f} kg")
        
        # Koszt
        cena_n = 4.5  # zł/kg
        cena_p = 3.2
        cena_k = 3.0
        
        koszt = (całkowite_N * cena_n) + (całkowite_P * cena_p) + (całkowite_K * cena_k)
        st.warning(f"**Szacowany koszt nawozów: {koszt:.2f} zł**")
    
    st.divider()
    
    st.subheader("🌧️ Warunki - decyzje w programie")
    
    st.code("""# Przykład warunku - czy podlewać?
wilgotność_gleby = 35  # procent
temperatura = 28      # °C

if wilgotność_gleby < 40 and temperatura > 25:
    print("⚠️ Niski poziom wilgoci przy wysokiej temp. - potrzeba nawadniania")
elif wilgotność_gleby < 30:
    print("🚨 Bardzo niska wilgotność - pilne nawadnianie!")
else:
    print("✅ Wilgotność w normie")
""", language="python")
    
    wilgotność = st.slider("Wilgotność gleby [%]:", 0, 100, 35)
    temperatura = st.slider("Temperatura powietrza [°C]:", 0, 40, 25)
    
    if st.button("Sprawdź potrzebę nawadniania"):
        if wilgotność < 30:
            st.error("🚨 BARDZO NISKA WILGOTNOŚĆ! Pilne nawadnianie konieczne!")
        elif wilgotność < 40 and temperatura > 25:
            st.warning("⚠️ Zalecane nawadnianie - niska wilgotność przy wysokiej temperaturze")
        else:
            st.success("✅ Wilgotność w normie - nawadnianie niepotrzebne")
    
    st.divider()
    
    st.subheader("✅ Quiz")
    
    q2 = st.radio(
        "Który operator oznacza 'i' (oba warunki muszą być spełnione)?",
        ["and", "or", "not", "xor"]
    )
    
    if q2:
        if q2 == "and":
            st.success("✅ Poprawnie! Operator 'and' wymaga spełnienia obu warunków.")
        else:
            st.error("❌ Spróbuj jeszcze raz.")
    
    st.markdown("---")
    st.caption("© Kurs Python - Automatyzacja w rolnictwie")
