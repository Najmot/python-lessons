import streamlit as st
import pandas as pd
import unittest
from io import StringIO
from contextlib import redirect_stdout
from abc import ABC, abstractmethod
from typing import List, Optional
from dataclasses import dataclass

def teoria():
    st.header("🏗️ Dzień 4 – OOP, SOLID i czysty kod")
    st.progress(60)
    
    st.markdown("""
    ## 🏛️ **Zasady SOLID jak u ArjanCodes - Praktyczne zastosowania w rolnictwie**
    """)
    
    solid_data = {
        'Zasada': ['S - Single Responsibility', 'O - Open/Closed', 'L - Liskov Substitution', 
                   'I - Interface Segregation', 'D - Dependency Inversion'],
        'Definicja': [
            'Klasa ma jeden powód do zmiany',
            'Otwarta na rozszerzenia, zamknięta na modyfikacje',
            'Podklasy mogą zastąpić nadklasy',
            'Wiele specyficznych interfejsów > jeden ogólny',
            'Zależności od abstrakcji, nie implementacji'
        ],
        'Przykład rolniczy': [
            'Oddzielna klasa do obliczeń plonów i osobna do raportowania',
            'Możliwość dodania nowego typu nawozu bez zmiany istniejącego kodu',
            'Klasa PoleEkologiczne może zastąpić klasę Pole wszędzie',
            'Oddzielne interfejsy: Nawadnialne, Nawozowe, Zbieralne',
            'Pole zależy od interfejsu Nawoz, a nie konkretnego nawozu NPK'
        ]
    }
    
    st.dataframe(pd.DataFrame(solid_data), use_container_width=True, hide_index=True)
    
    st.markdown("""
    ### 🎯 **Wskazówka Corey'ego Schafera**: Używaj @property dla kontroli dostępu
    ```python
    class Pole:
        def __init__(self, powierzchnia):
            self._powierzchnia = powierzchnia  # Prywatne
        
        @property
        def powierzchnia(self):
            return self._powierzchnia
        
        @powierzchnia.setter  
        def powierzchnia(self, value):
            if value <= 0:
                raise ValueError("Powierzchnia musi być > 0")
            self._powierzchnia = value
    ```
    """)

def cwiczenie_interaktywne():
    st.subheader("🎯 **Refaktoryzacja spaghetti code**")
    
    st.markdown("""
    ### Przed refaktoryzacją (zły kod):
    ```python
    # SPAGHETTI CODE - wszystko w jednej funkcji
    def przetworz_dane(nazwa, plon, powierzchnia, gleba, cena, czy_nawozone):
        # 100 linii kodu robiącego wszystko...
        if plon > 8 and gleba == "gliniasta":
            if czy_nawozone:
                wartosc = plon * powierzchnia * cena * 1.1
            else:
                wartosc = plon * powierzchnia * cena
        # ... i tak dalej przez wiele if-else
        return {"wartosc": wartosc, "decyzja": "nawozic"}
    ```
    """)
    
    st.subheader("✍️ **Twoje zadanie:**")
    
    # Edytor kodu do refaktoryzacji
    zly_kod = st.text_area("Zrefaktoryzuj ten kod:", height=200, value="""# DO UZUPEŁNIENIA - Stwórz czyste klasy i funkcje

class Pole:
    pass  # TODO: Stwórz klasę z odpowiednimi właściwościami

class KalkulatorWartosci:
    pass  # TODO: Oddziel logikę obliczeń

class DecydentNawozenia:
    pass  # TODO: Oddziel logikę decyzyjną

def przetworz_dane_refaktoryzowane(nazwa, plon, powierzchnia, gleba, cena, czy_nawozone):
    # TODO: Użyj powyższych klas
    return {"status": "niezaimplementowane"}
""")
    
    if st.button("🔍 Sprawdź refaktoryzację", key="check_refactor"):
        # Proste testy
        test_cases = [
            (8.5, 5.0, "gliniasta", 800, True),
            (6.0, 3.0, "piaszczysta", 750, False)
        ]
        
        try:
            exec(zly_kod, globals())
            
            for plon, pow, gleba, cena, nawoz in test_cases:
                result = przetworz_dane_refaktoryzowane(
                    "Test", plon, pow, gleba, cena, nawoz
                )
                st.write(f"**Test:** {result}")
            
            st.success("✅ Kod wykonany - sprawdź czy struktura jest lepsza!")
        except Exception as e:
            st.error(f"❌ Błąd: {e}")

def mini_projekt():
    st.subheader("🚀 **System klas z dziedziczeniem i polimorfizmem**")
    
    kod = st.text_area("✍️ **Zaimplementuj hierarchię klas:**", height=400, value="""from abc import ABC, abstractmethod
from typing import List

class Uprawa(ABC):
    '''Abstrakcyjna klasa bazowa dla wszystkich upraw'''
    def __init__(self, nazwa: str, powierzchnia: float):
        self.nazwa = nazwa
        self.powierzchnia = powierzchnia
        self._plon = 0.0
    
    @property
    def plon(self) -> float:
        return self._plon
    
    @plon.setter
    def plon(self, value: float):
        if value < 0:
            raise ValueError("Plon nie może być ujemny")
        self._plon = value
    
    @abstractmethod
    def oblicz_przychod(self, cena_za_tonę: float) -> float:
        '''Każda podklasa musi zaimplementować'''
        pass
    
    @abstractmethod
    def wymagania_wodne(self) -> str:
        '''Zwraca opis wymagań wodnych'''
        pass

class Zboze(Uprawa):
    '''Klasa dla upraw zbożowych'''
    def __init__(self, nazwa: str, powierzchnia: float, odmiana: str):
        super().__init__(nazwa, powierzchnia)
        self.odmiana = odmiana
        self._wspolczynnik_plonu = 1.0
    
    # TODO: Zaimplementuj metody abstrakcyjne
    def oblicz_przychod(self, cena_za_tonę: float) -> float:
        return 0.0
    
    def wymagania_wodne(self) -> str:
        return ""

class Warzywo(Uprawa):
    '''Klasa dla upraw warzywnych'''
    def __init__(self, nazwa: str, powierzchnia: float, okres_wegetacji: int):
        super().__init__(nazwa, powierzchnia)
        self.okres_wegetacji = okres_wegetacji  # w dniach
    
    # TODO: Zaimplementuj metody abstrakcyjne
    def oblicz_przychod(self, cena_za_tonę: float) -> float:
        return 0.0
    
    def wymagania_wodne(self) -> str:
        return ""

class EkologicznaUprawa(Zboze):
    '''Specjalna klasa dla upraw ekologicznych'''
    def __init__(self, nazwa: str, powierzchnia: float, odmiana: str, certyfikat: str):
        super().__init__(nazwa, powierzchnia, odmiana)
        self.certyfikat = certyfikat
        self._wspolczynnik_plonu = 0.8  # Niższe plony w ekologii
    
    # TODO: Nadpisz metody dla specyfiki ekologicznej
    def oblicz_przychod(self, cena_za_tonę: float) -> float:
        # Cena wyższa o 50% dla produktów ekologicznych
        return 0.0
""")
    
    if st.button("🧪 Testy OOP", key="testy4"):
        test_code = f"""
import unittest

{kod}

class TestUprawy(unittest.TestCase):
    def test_abstrakcyjnosc(self):
        '''Klasa Uprawa powinna być abstrakcyjna'''
        with self.assertRaises(TypeError):
            u = Uprawa("test", 1.0)
    
    def test_zboze_implementacja(self):
        z = Zboze("Pszenica", 5.0, "Boomer")
        z.plon = 8.5
        self.assertEqual(z.plon, 8.5)
        self.assertIsInstance(z, Uprawa)
    
    def test_ekologiczna_dziedziczenie(self):
        e = EkologicznaUprawa("Pszenica ekologiczna", 3.0, "EkoGold", "EU Organic")
        self.assertIsInstance(e, Zboze)
        self.assertIsInstance(e, Uprawa)
        self.assertEqual(e.certyfikat, "EU Organic")
    
    def test_wspolczynnik_plonu(self):
        z = Zboze("Pszenica", 5.0, "Standard")
        e = EkologicznaUprawa("Pszenica eko", 5.0, "Eko", "Cert")
        # TODO: Sprawdź czy współczynniki są różne
    
    def test_polimorfizm(self):
        uprawy: List[Uprawa] = [
            Zboze("Pszenica", 5.0, "A"),
            Warzywo("Marchew", 2.0, 90)
        ]
        for u in uprawy:
            # Powinno działać dla każdej podklasy
            result = u.wymagania_wodne()
            self.assertIsInstance(result, str)

if __name__ == '__main__':
    unittest.main()
"""
        
        f = StringIO()
        with redirect_stdout(f):
            try:
                exec(test_code)
                st.success("✅ Testy OOP wykonane!")
            except Exception as e:
                st.error(f"❌ Błąd: {e}")
        
        st.code(f.getvalue())

def quiz():
    st.subheader("📝 **Quiz: OOP i SOLID**")
    
    q1 = st.radio(
        "Która zasada SOLID mówi o tym, że klasa powinna mieć jeden powód do zmiany?",
        ["Open/Closed", "Single Responsibility", "Liskov Substitution", "Dependency Inversion"],
        key="q4_1"
    )
    
    if q1 == "Single Responsibility":
        st.success("✅ Poprawnie! SRP = Single Responsibility Principle.")
    
    q2 = st.radio(
        "Co oznacza dekorator `@abstractmethod` w klasie?",
        ["Metoda jest opcjonalna", "Metoda musi być zaimplementowana w podklasach", 
         "Metoda jest statyczna", "Metoda jest prywatna"],
        key="q4_2"
    )
    
    if q2 == "Metoda musi być zaimplementowana w podklasach":
        st.success("✅ Abstrakcyjne metody wymuszają implementację w podklasach.")

def challenge():
    st.subheader("⚡ **Challenge: Wzorzec Strategy**")
    
    st.markdown("""
    ### Zadanie: Strategie nawożenia
    
    Zaimplementuj wzorzec Strategy dla różnych strategii nawożenia:
    1. **Strategia intensywna** - maksymalizuje plon, wysokie koszty
    2. **Strategia ekologiczna** - naturalne nawozy, niższe plony
    3. **Strategia zrównoważona** - optymalizuje koszt/plon
    
    **Wymagania:**
    - Interfejs `StrategiaNawozenia` z metodą `oblicz_dawke(pole: Pole) -> float`
    - Trzy implementacje interfejsu
    - Klasa `Pole` używa strategii przez kompozycję (nie dziedziczenie)
    - Możliwość zmiany strategii w runtime
    - Testy jednostkowe dla każdej strategii
    """)

def run():
    st.sidebar.markdown("## 📖 Nawigacja lekcji 4")
    section = st.sidebar.radio(
        "Przejdź do:",
        ["📚 Teoria", "🎯 Ćwiczenie", "🚀 Projekt", "📝 Quiz", "⚡ Challenge"],
        key="nav4"
    )
    
    if section == "📚 Teoria": teoria()
    elif section == "🎯 Ćwiczenie": cwiczenie_interaktywne()
    elif section == "🚀 Projekt": mini_projekt()
    elif section == "📝 Quiz": quiz()
    elif section == "⚡ Challenge": challenge()
    
    st.markdown("---")
    col1, col2, col3 = st.columns([1, 2, 1])
    with col1:
        if st.button("⏮️ Lekcja 3", key="prev4"):
            st.session_state.selected_lesson = "lesson3"
            st.rerun()
    with col2:
        if st.button("🏠 Strona główna", key="home4"):
            if "selected_lesson" in st.session_state:
                del st.session_state.selected_lesson
            st.rerun()
    with col3:
        if st.button("Lekcja 5 ⏭️", key="next4"):
            st.session_state.selected_lesson = "lesson5"
            st.rerun()

if __name__ == "__main__":
    run()
