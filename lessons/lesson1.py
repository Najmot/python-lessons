import streamlit as st
import pandas as pd
from io import StringIO
import sys
from contextlib import redirect_stdout
import unittest

# ========== CZĘŚĆ 1: TEORIA (Corey Schafer style) ==========
def teoria():
    st.header("🐍 Dzień 1 – Zmienne, typy i operacje")
    st.progress(15)
    
    st.markdown("""
    ## 📚 **Podstawy jak u Corego Schafera** - Czyste, praktyczne przykłady
    
    ### Zmienne to nie "pudełka", a **etykiety przyklejone do obiektów**
    ```python
    # ZŁE podejście (myślenie "pudełkowe")
    box = "wartość"  # ❌
    
    # DOBRE podejście (Pythonowe)
    label = obiekt    # ✅ Etykieta "label" wskazuje na obiekt w pamięci
    ```
    
    ### Typy danych w praktyce rolniczej:
    """)
    
    # Przykłady w tabeli
    dane_przyklady = {
        'Typ': ['str', 'int', 'float', 'bool', 'list', 'dict'],
        'Przykład': [
            '"Pszenica ozima", "GLINIASTA"',
            '100 (kg nawozu), 5 (liczba pól)',
            '25.5 (plon t/ha), 750.99 (cena zł/t)',
            'True (czy nawożone), False (czy zbierane)',
            '[8.3, 7.9, 9.2] (plony z pól)',
            '{"pole": "A", "powierzchnia": 5.2, "nawożone": True}'
        ],
        'Użycie': [
            'Nazwy, opisy, tekst',
            'Liczby całkowite',
            'Pomiary, ceny, wagi',
            'Warunki logiczne',
            'Kolekcje danych',
            'Struktury złożone'
        ]
    }
    
    df = pd.DataFrame(dane_przyklady)
    st.dataframe(df, use_container_width=True, hide_index=True)
    
    st.markdown("""
    ### 🔍 **Wskazówka od Corego**: Używaj `type()` aby sprawdzać typy:
    ```python
    plon = 8.3
    print(type(plon))  # <class 'float'>
    print(isinstance(plon, float))  # True
    ```
    """)

# ========== CZĘŚĆ 2: ĆWICZENIE KROK-PO-KROKU (Jose Portilla style) ==========
def cwiczenie_interaktywne():
    st.subheader("🎯 **Ćwiczenie krok-po-kroku** (jak u Josego Portilli)")
    
    st.markdown("""
    ### Zadanie: Stwórz kartę pola uprawnego
    
    Będziemy krok po kroku tworzyć program do przechowywania danych pola.
    Śledź instrukcje i wypełniaj brakujący kod.
    """)
    
    # Krok 1
    with st.expander("📝 **KROK 1: Zdefiniuj zmienne podstawowe**", expanded=True):
        st.code("""# Tutaj wpisz swój kod:
nazwa_pola = "___"  # Wpisz nazwę pola (tekst)
powierzchnia = ___   # Wpisz powierzchnię w ha (liczba dziesiętna)
rodzaj_gleby = "___" # Wpisz typ gleby (tekst)
""")
        
        col1, col2, col3 = st.columns(3)
        with col1:
            user_nazwa = st.text_input("Nazwa pola:", "Pole A", key="nazwa1")
        with col2:
            user_powierzchnia = st.number_input("Powierzchnia (ha):", 0.1, 100.0, 5.2, key="pow1")
        with col3:
            user_gleba = st.selectbox("Rodzaj gleby:", ["Gliniasta", "Piaszczysta", "Ilasta", "Torfiasta"], key="gleba1")
        
        if st.button("🔍 Sprawdź KROK 1", key="check1"):
            try:
                # Symulacja wykonania kodu użytkownika
                test_code = f"""
nazwa_pola = "{user_nazwa}"
powierzchnia = {user_powierzchnia}
rodzaj_gleby = "{user_gleba}"
"""
                exec(test_code)
                st.success("✅ Doskonale! Zmienne zdefiniowane poprawnie.")
                st.info(f"**Typ `nazwa_pola`:** {type(user_nazwa).__name__}")
                st.info(f"**Typ `powierzchnia`:** {type(user_powierzchnia).__name__}")
            except Exception as e:
                st.error(f"❌ Błąd: {e}")

# ========== CZĘŚĆ 3: MINI-PROJEKT Z TESTAMI (ArjanCodes style) ==========
def mini_projekt_z_testami():
    st.subheader("🚀 **Mini-projekt z testami jednostkowymi** (jak u ArjanCodes)")
    
    st.markdown("""
    ### Projekt: Klasa `PoleUprawne`
    
    Stwórzmy klasę zgodnie z zasadami czystego kodu. Klasa powinna:
    1. Przechowywać dane pola
    2. Obliczać szacowany plon
    3. Sprawdzać poprawność danych
    """)
    
    # Edytor kodu
    kod_projektu = st.text_area(
        "✍️ **Napisz klasę `PoleUprawne` tutaj:**",
        height=250,
        value="""class PoleUprawne:
    def __init__(self, nazwa, powierzchnia, gleba, plon_standardowy=8.0):
        self.nazwa = nazwa
        self.powierzchnia = powierzchnia  # w ha
        self.gleba = gleba
        self.plon_standardowy = plon_standardowy  # t/ha
    
    def szacowany_plon(self):
        # TODO: oblicz całkowity plon (powierzchnia * plon_standardowy)
        return 0.0
    
    def czy_opłacalne(self, koszt_nawozenia, cena_za_tonę=800):
        # TODO: sprawdź czy zysk > koszt * 1.5
        przychod = self.szacowany_plon() * cena_za_tonę
        return przychod > (koszt_nawozenia * 1.5)
    
    def __str__(self):
        # TODO: zwróć ładny opis pola
        return f\"Pole: {self.nazwa}\"
""",
        key="kod_klasy"
    )
    
    if st.button("🧪 **Uruchom testy jednostkowe**", key="testy_button"):
        # Utworzenie pliku testowego w pamięci
        test_code = f"""
import unittest

{kod_projektu}

class TestPoleUprawne(unittest.TestCase):
    def setUp(self):
        self.pole = PoleUprawne("Testowe", 5.0, "Gliniasta", 8.5)
    
    def test_szacowany_plon(self):
        # Test obliczeń
        expected = 5.0 * 8.5  # 42.5
        result = self.pole.szacowany_plon()
        self.assertAlmostEqual(result, expected, places=2,
                             msg=f"Oczekiwano {{expected}}, otrzymano {{result}}")
    
    def test_czy_opłacalne(self):
        # Test opłacalności
        self.pole.powierzchnia = 10.0
        self.pole.plon_standardowy = 8.0
        # Przychód: 10 * 8 * 800 = 64,000
        # Próg: 20,000 * 1.5 = 30,000
        self.assertTrue(self.pole.czy_opłacalne(20000),
                       "Powinno być opłacalne")
        self.assertFalse(self.pole.czy_opłacalne(50000),
                        "Nie powinno być opłacalne")
    
    def test_reprezentacja(self):
        # Test metody __str__
        result = str(self.pole)
        self.assertIn("Pole:", result)
        self.assertIn("Testowe", result)

if __name__ == '__main__':
    unittest.main()
"""
        
        # Uruchomienie testów
        f = StringIO()
        with redirect_stdout(f):
            test_suite = unittest.TestLoader().loadTestsFromTestCase(
                type('TestPoleUprawne', (unittest.TestCase,), {
                    'setUp': lambda self: exec(f"self.pole = PoleUprawne('Testowe', 5.0, 'Gliniasta', 8.5)", globals()),
                    'test_szacowany_plon': lambda self: self.assertAlmostEqual(
                        eval("self.pole.szacowany_plon()"), 42.5, places=2
                    ),
                    'test_czy_opłacalne': lambda self: (
                        exec("self.pole.powierzchnia = 10.0; self.pole.plon_standardowy = 8.0"),
                        self.assertTrue(eval("self.pole.czy_opłacalne(20000)")),
                        self.assertFalse(eval("self.pole.czy_opłacalne(50000)"))
                    ),
                    'test_reprezentacja': lambda self: self.assertIn("Pole:", str(eval("self.pole")))
                })
            )
            runner = unittest.TextTestRunner(stream=f, verbosity=2)
            result = runner.run(test_suite)
        
        output = f.getvalue()
        
        # Wyświetlenie wyników
        st.subheader("📊 **Wyniki testów:**")
        st.code(output)
        
        if result.wasSuccessful():
            st.balloons()
            st.success("🎉 **Wszystkie testy przeszły!** Twój kod jest wysokiej jakości!")
        else:
            st.error("❌ **Niektóre testy nie przeszły.** Popraw kod i spróbuj ponownie.")
            st.info("💡 **Wskazówka:** Upewnij się, że metody zwracają poprawne wartości.")

# ========== CZĘŚĆ 4: QUIZ Z NATYCHMIASTOWĄ WERYFIKACJĄ ==========
def quiz():
    st.subheader("📝 **Quiz sprawdzający**")
    
    questions = [
        {
            "question": "Która zasada dotyczy nazewnictwa zmiennych w Pythonie?",
            "options": [
                "Można używać polskich znaków",
                "Muszą zaczynać się od liczby",
                "Wielkość liter ma znaczenie",
                "Nie można używać podkreślnika"
            ],
            "correct": 2,
            "explanation": "✅ Python rozróżnia wielkość liter: `pole` ≠ `Pole` ≠ `POLE`"
        },
        {
            "question": "Jaki typ danych będzie miał wynik: `3 * 1.5`?",
            "options": ["int", "str", "float", "bool"],
            "correct": 2,
            "explanation": "✅ Mnożenie int przez float daje float (4.5)"
        }
    ]
    
    score = 0
    for i, q in enumerate(questions):
        st.markdown(f"**Pytanie {i+1}: {q['question']}**")
        answer = st.radio(
            f"Wybierz odpowiedź:",
            q['options'],
            key=f"quiz_{i}",
            index=None
        )
        
        if answer:
            if answer == q['options'][q['correct']]:
                st.success(f"✅ Poprawnie! {q['explanation']}")
                score += 1
            else:
                st.error(f"❌ Niepoprawnie. {q['explanation']}")
    
    if score == len(questions):
        st.balloons()
        st.success(f"🏆 **Perfekcyjnie! {score}/{len(questions)} punktów!**")

# ========== CZĘŚĆ 5: CHALLENGE ZAAWANSOWANY ==========
def challenge():
    st.subheader("⚡ **Challenge zaawansowany** (dla chętnych)")
    
    st.markdown("""
    ### Zadanie: Analiza wielu pól
    
    Stwórz listę 3-5 obiektów `PoleUprawne` i napisz funkcję, która:
    1. Obliczy łączny szacowany plon ze wszystkich pól
    2. Znajdzie pole z najwyższym plonem na hektar
    3. Posortuje pola według opłacalności
    
    **Wskazówki:**
    - Użyj list comprehension
    - Wykorzystaj funkcję `sorted()` z parametrem `key`
    - Dodaj własne testy jednostkowe
    """)
    
    if st.button("🔄 Pokaż przykładowe rozwiązanie", key="challenge_sol"):
        st.code("""# Przykładowe rozwiązanie
def analiza_pol(lista_pol):
    # 1. Łączny plon
    laczny_plon = sum(p.szacowany_plon() for p in lista_pol)
    
    # 2. Pole z najwyższym plonem/ha
    najwyzsze = max(lista_pol, key=lambda p: p.plon_standardowy)
    
    # 3. Sortowanie według opłacalności (przy stałych kosztach)
    posortowane = sorted(lista_pol, 
                        key=lambda p: p.szacowany_plon() * 800,  # przychód
                        reverse=True)
    
    return {
        "laczny_plon": laczny_plon,
        "najwyzsze_plon": najwyzsze,
        "ranking": posortowane
    }

# Testy
import unittest
class TestAnaliza(unittest.TestCase):
    def test_laczny_plon(self):
        pola = [
            PoleUprawne("A", 5, "glina", 8),
            PoleUprawne("B", 3, "piasek", 6)
        ]
        result = analiza_pol(pola)
        self.assertEqual(result["laczny_plon"], (5*8) + (3*6))
""")

# ========== GŁÓWNA FUNKCJA ==========
def run():
    # Nawigacja między sekcjami
    st.sidebar.markdown("## 📖 Nawigacja lekcji")
    section = st.sidebar.radio(
        "Przejdź do sekcji:",
        ["📚 Teoria", "🎯 Ćwiczenie", "🚀 Projekt", "📝 Quiz", "⚡ Challenge"],
        key="nav"
    )
    
    # Wyświetlenie wybranej sekcji
    if section == "📚 Teoria":
        teoria()
    elif section == "🎯 Ćwiczenie":
        cwiczenie_interaktywne()
    elif section == "🚀 Projekt":
        mini_projekt_z_testami()
    elif section == "📝 Quiz":
        quiz()
    elif section == "⚡ Challenge":
        challenge()
    
    # Stopka z nawigacją
    st.markdown("---")
    col1, col2, col3 = st.columns([1, 2, 1])
    with col1:
        if st.button("⏮️ Poprzednia lekcja"):
            st.session_state.selected_lesson = "lesson0"  # Zmień odpowiednio
            st.rerun()
    with col2:
        if st.button("🏠 Strona główna"):
            if "selected_lesson" in st.session_state:
                del st.session_state.selected_lesson
            st.rerun()
    with col3:
        if st.button("Następna lekcja ⏭️"):
            st.session_state.selected_lesson = "lesson2"
            st.rerun()

# Uruchomienie lekcji
if __name__ == "__main__":
    run()
