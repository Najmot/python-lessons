import streamlit as st
import pandas as pd
import numpy as np
import matplotlib.pyplot as plt
import unittest
from io import StringIO
from contextlib import redirect_stdout
from typing import List, Dict

def teoria():
    st.header("🔄 Dzień 3 – Pętle, kolekcje i analiza danych")
    st.progress(45)
    
    st.markdown("""
    ## 📊 **Analiza danych jak u Corey'ego Schafera - Praktyczne zastosowania**
    
    ### Kiedy używać jakiej pętli?
    """)
    
    petle_data = {
        'Pętla': ['for', 'while', 'list comprehension', 'generator'],
        'Gdy używać': [
            'Iteracja po znanej kolekcji (listy, zakresy)',
            'Nieznana liczba iteracji (np. aż warunek spełniony)',
            'Transformacja listy w jedną linię',
            'Duże zbiory danych (leniwe obliczenia)'
        ],
        'Przykład rolniczy': [
            'Przeglądanie plonów z wszystkich pól',
            'Symulacja wzrostu aż osiągnie cel',
            'Obliczenie plonów dla wszystkich pól',
            'Przetwarzanie danych z czujników w czasie rzeczywistym'
        ]
    }
    
    st.dataframe(pd.DataFrame(petle_data), use_container_width=True, hide_index=True)
    
    st.markdown("""
    ### 🎯 **Wskazówka Josego Portilli**: Zawsze miej plan iteracji!
    ```python
    # ZŁE - bez planu
    i = 0
    while True:  # ❌ Nieskończona pętla?
        i += 1
    
    # DOBRE - z warunkiem stopu
    dni = 0
    while wzrost < 100:  # ✅ Jasny warunek stopu
        wzrost += dzienny_wzrost
        dni += 1
    ```
    """)

def cwiczenie_interaktywne():
    st.subheader("🎯 **Analiza plonów z wielu pól**")
    
    # Generowanie przykładowych danych
    np.random.seed(42)
    liczba_pol = st.slider("Liczba pól do analizy:", 3, 20, 10)
    
    # Symulacja danych
    pola_nazwy = [f"Pole {i+1}" for i in range(liczba_pol)]
    plony = np.random.uniform(5.0, 12.0, liczba_pol).round(1)
    powierzchnie = np.random.uniform(2.0, 8.0, liczba_pol).round(1)
    
    # Tabela danych
    df = pd.DataFrame({
        'Pole': pola_nazwy,
        'Plon (t/ha)': plony,
        'Powierzchnia (ha)': powierzchnie
    })
    
    st.dataframe(df, use_container_width=True)
    
    # Analiza
    st.subheader("📈 **Wyniki analizy:**")
    
    col1, col2, col3 = st.columns(3)
    
    with col1:
        # Użycie pętli for
        suma_plonow = 0
        for plon in plony:
            suma_plonow += plon
        sredni_plon = suma_plonow / len(plony)
        st.metric("Średni plon (for)", f"{sredni_plon:.1f} t/ha")
    
    with col2:
        # Użycie list comprehension
        calkowite_plony = [p * pow for p, pow in zip(plony, powierzchnie)]
        suma_calkowita = sum(calkowite_plony)
        st.metric("Całkowity plon", f"{suma_calkowita:.1f} t")
    
    with col3:
        # Znajdź najlepsze pole
        najlepsze_idx = np.argmax(plony)
        st.metric("Najlepsze pole", f"{pola_nazwy[najlepsze_idx]}: {plony[najlepsze_idx]} t/ha")

def mini_projekt():
    st.subheader("🚀 **Klasa AnalizatorPol z testami**")
    
    kod = st.text_area("✍️ **Stwórz klasę `AnalizatorPol`:**", height=350, value="""class AnalizatorPol:
    def __init__(self, nazwy_pol: List[str], plony: List[float], powierzchnie: List[float]):
        if len(nazwy_pol) != len(plony) != len(powierzchnie):
            raise ValueError("Wszystkie listy muszą mieć tę samą długość")
        self.nazwy_pol = nazwy_pol
        self.plony = plony  # t/ha
        self.powierzchnie = powierzchnie  # ha
    
    def statystyki_podstawowe(self) -> Dict:
        '''Zwraca słownik z podstawowymi statystykami'''
        # TODO: Oblicz średni plon, całkowity plon, pole z max plonem
        return {
            "sredni_plon": 0.0,
            "calkowity_plon": 0.0,
            "najlepsze_pole": "",
            "najlepszy_plon": 0.0
        }
    
    def pola_powyzej_progu(self, prog: float) -> List[str]:
        '''Zwraca nazwy pól z plonem powyżej podanego progu'''
        # TODO: Użyj list comprehension
        return []
    
    def symuluj_zwiekszenie_plonow(self, procent: float) -> Dict:
        '''Symuluje zwiększenie wszystkich plonów o podany procent'''
        # TODO: Zwróć nowe statystyki po zwiększeniu
        return {}
    
    def raport_csv(self, sciezka: str = "raport_pol.csv"):
        '''Zapisuje raport do pliku CSV'''
        import csv
        # TODO: Zapisz dane do CSV
        pass
""")
    
    if st.button("🧪 Uruchom testy", key="testy3"):
        test_code = f"""
import unittest
import tempfile
import os

{kod}

class TestAnalizatorPol(unittest.TestCase):
    def setUp(self):
        self.nazwy = ["Pole A", "Pole B", "Pole C"]
        self.plony = [8.3, 7.9, 9.2]
        self.powierzchnie = [5.2, 3.8, 7.1]
        self.analizator = AnalizatorPol(self.nazwy, self.plony, self.powierzchnie)
    
    def test_statystyki_podstawowe(self):
        stats = self.analizator.statystyki_podstawowe()
        self.assertAlmostEqual(stats["sredni_plon"], (8.3+7.9+9.2)/3, places=1)
        self.assertEqual(stats["najlepsze_pole"], "Pole C")
        self.assertAlmostEqual(stats["najlepszy_plon"], 9.2, places=1)
    
    def test_pola_powyzej_progu(self):
        result = self.analizator.pola_powyzej_progu(8.0)
        self.assertIn("Pole A", result)
        self.assertIn("Pole C", result)
        self.assertNotIn("Pole B", result)
    
    def test_symulacja(self):
        result = self.analizator.symuluj_zwiekszenie_plonow(10)  # +10%
        # 9.2 * 1.1 = 10.12
        self.assertGreater(result.get("najlepszy_plon", 0), 10.0)
    
    def test_csv_export(self):
        with tempfile.NamedTemporaryFile(mode='w', delete=False, suffix='.csv') as f:
            sciezka = f.name
            self.analizator.raport_csv(sciezka)
            self.assertTrue(os.path.exists(sciezka))
            with open(sciezka, 'r') as check_file:
                content = check_file.read()
                self.assertIn("Pole A", content)
        os.unlink(sciezka)

if __name__ == '__main__':
    unittest.main()
"""
        
        f = StringIO()
        with redirect_stdout(f):
            try:
                exec(test_code, globals())
                st.success("✅ Testy wykonane!")
            except Exception as e:
                st.error(f"❌ Błąd: {e}")
        
        st.code(f.getvalue())

def quiz():
    st.subheader("📝 **Quiz: Pętle i analiza**")
    
    q1 = st.radio(
        "Która pętla NIE nadaje się do iteracji po liście?",
        ["for element in lista:", "while i < len(lista):", "for i in range(len(lista)):", "while True: (bez break)"],
        key="q3_1"
    )
    
    if q1 == "while True: (bez break)":
        st.success("✅ Poprawnie! To stworzyłoby nieskończoną pętlę.")
    
    q2 = st.radio(
        "Co zwróci `[x*2 for x in range(3)]`?",
        ["[0, 1, 2]", "[0, 2, 4]", "[0, 2]", "Błąd"],
        key="q3_2"
    )
    
    if q2 == "[0, 2, 4]":
        st.success("✅ List comprehension: 0*2=0, 1*2=2, 2*2=4")

def challenge():
    st.subheader("⚡ **Challenge: Optymalizacja wydajności**")
    
    st.markdown("""
    ### Zadanie: Analiza dużego zbioru danych
    
    Masz 1000 pól z danymi. Zoptymalizuj kod:
    1. **Użyj generatorów** zamiast list dla dużych obliczeń
    2. **Zaimplementuj caching** wyników pośrednich
    3. **Dodaj progres bar** dla długich obliczeń
    4. **Napisz testy wydajnościowe** porównujące różne implementacje
    
    **Dane:** Każde pole ma: nazwę, plon (5-15 t/ha), powierzchnię (1-10 ha), typ gleby
    
    **Cel:** Znajdź 10% najlepszych pół do inwestycji w nawóz premium.
    """)

def run():
    st.sidebar.markdown("## 📖 Nawigacja lekcji 3")
    section = st.sidebar.radio(
        "Przejdź do:",
        ["📚 Teoria", "🎯 Ćwiczenie", "🚀 Projekt", "📝 Quiz", "⚡ Challenge"],
        key="nav3"
    )
    
    if section == "📚 Teoria": teoria()
    elif section == "🎯 Ćwiczenie": cwiczenie_interaktywne()
    elif section == "🚀 Projekt": mini_projekt()
    elif section == "📝 Quiz": quiz()
    elif section == "⚡ Challenge": challenge()
    
    st.markdown("---")
    col1, col2, col3 = st.columns([1, 2, 1])
    with col1:
        if st.button("⏮️ Lekcja 2", key="prev3"):
            st.session_state.selected_lesson = "lesson2"
            st.rerun()
    with col2:
        if st.button("🏠 Strona główna", key="home3"):
            if "selected_lesson" in st.session_state:
                del st.session_state.selected_lesson
            st.rerun()
    with col3:
        if st.button("Lekcja 4 ⏭️", key="next3"):
            st.session_state.selected_lesson = "lesson4"
            st.rerun()

if __name__ == "__main__":
    run()
