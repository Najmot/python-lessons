import streamlit as st
import pandas as pd
import unittest
from io import StringIO
from contextlib import redirect_stdout

def teoria():
    st.header("🔢 Dzień 2 – Operacje, warunki i logika biznesowa")
    st.progress(30)
    
    st.markdown("""
    ## 📊 **Jak Corey Schafer: Pisz kod, który opowiada historię**
    
    ### Operatory porównania w praktyce rolniczej:
    """)
    
    # Tabela z przykładami
    operatory = {
        'Operator': ['==', '!=', '>', '<', '>=', '<='],
        'Przykład': [
            '`plon == 8.3` (czy równy wzorcowi?)',
            '`gleba != "piach"` (czy nie jest piaszczysta?)',
            '`temperatura > 25` (czy za gorąco?)',
            '`wilgotność < 30` (czy za sucho?)',
            '`powierzchnia >= 5.0` (minimalna wielkość pola)',
            '`koszt <= 1000` (maksymalny budżet)'
        ],
        'Użycie': [
            'Równość',
            'Różność',
            'Większość',
            'Mniejszość',
            'Większe/równe',
            'Mniejsze/równe'
        ]
    }
    
    st.dataframe(pd.DataFrame(operatory), use_container_width=True, hide_index=True)
    
    st.markdown("""
    ### 🎯 **Wskazówka Josego Portilli**: Zawsze testuj brzegowe przypadki!
    ```python
    # TESTUJ WARTOŚCI BRZEGOWE!
    wilgotnosc = 30.0
    czy_podlewac = wilgotnosc <= 30  # True czy False?
    # Odpowiedź zależy od specyfikacji biznesowej!
    ```
    """)

def cwiczenie_interaktywne():
    st.subheader("🎯 **Decyzje biznesowe w rolnictwie**")
    
    col1, col2 = st.columns(2)
    with col1:
        plon = st.slider("Plon (t/ha):", 2.0, 15.0, 7.5, 0.1)
        cena = st.number_input("Cena (zł/t):", 500, 1500, 850)
    with col2:
        koszt_nawozenia = st.number_input("Koszt nawożenia (zł/ha):", 0, 2000, 1200)
        wilgotnosc = st.slider("Wilgotność gleby (%):", 0, 100, 45)
    
    # Logika decyzyjna
    decyzje = []
    
    # Decyzja 1: Czy opłacalne?
    przychod = plon * cena
    if przychod > koszt_nawozenia * 1.3:
        decyzje.append(("✅ OPŁACALNE", f"Przychód ({przychod:.0f}zł) > Koszt + 30%"))
    else:
        decyzje.append(("❌ NIEOPŁACALNE", f"Przychód ({przychod:.0f}zł) za niski"))
    
    # Decyzja 2: Czy podlewać?
    if wilgotnosc < 35 and plon > 6:
        decyzje.append(("💧 PODLEWAĆ", f"Wilgotność ({wilgotnosc}%) za niska przy dobrym plonie"))
    elif wilgotnosc < 25:
        decyzje.append(("🚨 PILNIE PODLEWAĆ", "Krytycznie sucho!"))
    else:
        decyzje.append(("⏸️ NIE PODLEWAĆ", "Wilgotność w normie"))
    
    # Wyświetl decyzje
    st.subheader("🤖 **Decyzje systemu:**")
    for status, opis in decyzje:
        st.markdown(f"**{status}**: {opis}")

def mini_projekt():
    st.subheader("🚀 **System decyzyjny z testami**")
    
    kod = st.text_area("✍️ **Stwórz klasę `DecyzjeRolnicze`:**", height=300, value="""class DecyzjeRolnicze:
    def __init__(self, plon, cena, koszt_nawozenia, wilgotnosc):
        self.plon = plon  # t/ha
        self.cena = cena  # zł/t
        self.koszt_nawozenia = koszt_nawozenia  # zł/ha
        self.wilgotnosc = wilgotnosc  # %
    
    def czy_oplacalne(self, marza_minimalna=1.3):
        # TODO: Zwróć True jeśli przychód > koszt * marza_minimalna
        przychod = self.plon * self.cena
        return False
    
    def decyzja_nawadniania(self):
        # TODO: Zwróć string z decyzją
        # - "podlewać" jeśli wilgotnosc < 35 i plon > 6
        # - "pilnie podlewać" jeśli wilgotnosc < 25
        # - "nie podlewać" w innych przypadkach
        return "brak decyzji"
    
    def raport(self):
        # TODO: Zwróć słownik z wszystkimi danymi i decyzjami
        return {}
""")
    
    if st.button("🧪 Uruchom testy", key="testy2"):
        # Testy jednostkowe
        test_code = f"""
import unittest

{kod}

class TestDecyzje(unittest.TestCase):
    def test_czy_oplacalne(self):
        d = DecyzjeRolnicze(8.0, 800, 5000, 40)
        # Przychód: 8 * 800 = 6400, Koszt: 5000 * 1.3 = 6500
        self.assertFalse(d.czy_oplacalne())
        
        d2 = DecyzjeRolnicze(10.0, 900, 5000, 40)
        # Przychód: 9000 > 6500
        self.assertTrue(d2.czy_oplacalne())
    
    def test_decyzja_nawadniania(self):
        d1 = DecyzjeRolnicze(7.0, 800, 5000, 30)  # plon>6, wilg<35
        self.assertIn("podlewać", d1.decyzja_nawadniania().lower())
        
        d2 = DecyzjeRolnicze(5.0, 800, 5000, 20)  # wilg<25
        self.assertIn("pilnie", d2.decyzja_nawadniania().lower())

if __name__ == '__main__':
    unittest.main()
"""
        
        f = StringIO()
        with redirect_stdout(f):
            try:
                exec(test_code)
                st.success("✅ Testy wykonane pomyślnie!")
            except Exception as e:
                st.error(f"❌ Błąd: {e}")
        
        st.code(f.getvalue())

def quiz():
    st.subheader("📝 **Quiz: Logika biznesowa**")
    
    q1 = st.radio(
        "Kiedy warto podlewać pole według logiki biznesowej?",
        ["Zawsze rano", "Tylko gdy plon > 6 t/ha i wilgotność < 35%", "Co 3 dni bez względu na warunki", "Tylko w lipcu"],
        key="q2_1"
    )
    
    if q1 == "Tylko gdy plon > 6 t/ha i wilgotność < 35%":
        st.success("✅ Poprawnie! To optymalizacja zużycia wody.")
    
    q2 = st.radio(
        "Jaki operator użyjesz do sprawdzenia czy plon jest WYŻSZY niż 8 t/ha?",
        ["plon = 8", "plon > 8", "plon < 8", "plon != 8"],
        key="q2_2"
    )
    
    if q2 == "plon > 8":
        st.success("✅ Operator '>' sprawdza czy wartość jest większa.")

def challenge():
    st.subheader("⚡ **Challenge: Optymalizacja decyzji**")
    
    st.markdown("""
    ### Zadanie: System rekomendacji nawozów
    
    Rozszerz klasę `DecyzjeRolnicze` o:
    1. **Metodę `rekomenduj_nawoz()`** która sugeruje nawóz na podstawie gleby
    2. **Metodę `symuluj_scenariusz()`** która testuje "co jeśli" zmienimy cenę/plon
    3. **Testy jednostkowe** dla nowych metod
    
    **Dane referencyjne:**
    - Gleba "gliniasta" → nawóz NPK 8-8-8
    - Gleba "piaszczysta" → nawóz z azotem 12-4-4
    - Inne gleby → nawóz uniwersalny 10-10-10
    """)

def run():
    st.sidebar.markdown("## 📖 Nawigacja lekcji 2")
    section = st.sidebar.radio(
        "Przejdź do:",
        ["📚 Teoria", "🎯 Ćwiczenie", "🚀 Projekt", "📝 Quiz", "⚡ Challenge"],
        key="nav2"
    )
    
    if section == "📚 Teoria": teoria()
    elif section == "🎯 Ćwiczenie": cwiczenie_interaktywne()
    elif section == "🚀 Projekt": mini_projekt()
    elif section == "📝 Quiz": quiz()
    elif section == "⚡ Challenge": challenge()
    
    st.markdown("---")
    col1, col2, col3 = st.columns([1, 2, 1])
    with col1:
        if st.button("⏮️ Lekcja 1", key="prev2"):
            st.session_state.selected_lesson = "lesson1"
            st.rerun()
    with col2:
        if st.button("🏠 Strona główna", key="home2"):
            if "selected_lesson" in st.session_state:
                del st.session_state.selected_lesson
            st.rerun()
    with col3:
        if st.button("Lekcja 3 ⏭️", key="next2"):
            st.session_state.selected_lesson = "lesson3"
            st.rerun()

if __name__ == "__main__":
    run()
