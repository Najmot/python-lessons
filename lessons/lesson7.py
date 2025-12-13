import streamlit as st
import matplotlib.pyplot as plt
import numpy as np

def run():
    st.header("📈 Dzień 7 – Wizualizacje danych")
    
    st.progress(100)
    st.caption("Postęp w kursie: 100% 🎉")
    
    st.markdown("""
    ## 📊 Prezentacja danych na wykresach
    
    Ostatnia lekcja! Nauczysz się tworzyć czytelne wykresy z danych rolniczych
    za pomocą biblioteki Matplotlib. Dzięki temu będziesz mógł wizualnie analizować
    plony, koszty i trendy.
    """)
    
    st.subheader("📉 Przykładowe wykresy")
    
    # Przykładowe dane
    miesiace = ['Sty', 'Lut', 'Mar', 'Kwi', 'Maj', 'Cze']
    plony = [5.2, 5.8, 6.5, 7.8, 8.9, 9.2]
    koszty = [1200, 1350, 1100, 1400, 1600, 1550]
    
    col1, col2 = st.columns(2)
    
    with col1:
        st.markdown("**Wykres liniowy - plony w czasie**")
        fig, ax = plt.subplots()
        ax.plot(miesiace, plony, marker='o', color='green', linewidth=2)
        ax.set_xlabel('Miesiąc')
        ax.set_ylabel('Plon (t/ha)')
        ax.grid(True, alpha=0.3)
        st.pyplot(fig)
    
    with col2:
        st.markdown("**Wykres słupkowy - koszty nawożenia**")
        fig, ax = plt.subplots()
        ax.bar(miesiace, kosztsy, color='orange', alpha=0.7)
        ax.set_xlabel('Miesiąc')
        ax.set_ylabel('Koszt (zł)')
        st.pyplot(fig)
    
    # Interaktywny element
    st.subheader("🎨 Stwórz własny wykres")
    
    wybrane_miesiace = st.multiselect(
        "Wybierz miesiące do wykresu:",
        miesiace,
        default=miesiace[:3]
    )
    
    if wybrane_miesiace:
        # Filtruj dane
        indeksy = [miesiace.index(m) for m in wybrane_miesiace]
        filtrowane_plony = [plony[i] for i in indeksy]
        
        fig, ax = plt.subplots()
        ax.bar(wybrane_miesiace, filtrowane_plony, color='skyblue')
        ax.set_title('Twoje porównanie plonów')
        st.pyplot(fig)
    
    st.markdown("---")
    st.balloons()
    st.success("🎉 **Gratulacje! Ukończyłeś cały kurs!**")
    
    if st.button("🏠 Powrót do strony głównej"):
        st.session_state.selected_lesson = None
        st.rerun()
