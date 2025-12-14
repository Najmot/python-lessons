import streamlit as st
import pandas as pd
import sqlite3
import unittest
import tempfile
from io import StringIO
from contextlib import redirect_stdout, contextmanager
from pathlib import Path
from typing import List, Dict, Optional, Any
from datetime import datetime
import hashlib

def teoria():
    st.header("🗃️ Dzień 6 – Bazy danych i ORM")
    st.progress(90)
    
    st.markdown("""
    ## 🏗️ **Normalizacja baz danych na przykładzie gospodarstwa**
    
    ### Formy normalizacji (1NF, 2NF, 3NF):
    """)
    
    normalizacja_data = {
        'Forma': ['1NF - Pierwsza forma normalna', '2NF - Druga forma normalna', 
                 '3NF - Trzecia forma normalna', 'Denormalizacja'],
        'Zasada': [
            'Bez powtarzających się grup, wartości atomowe',
            'Zależność od całego klucza głównego',
            'Brak zależności przechodnich (tylko od klucza)',
            'Celowe łamanie normalizacji dla wydajności'
        ],
        'Przykład': [
            'Zamiast `"nawozy: NPK, wapno, saletra"` → osobne wiersze',
            'Tabela `pole_nawozy` z kluczem `(pole_id, nawóz_id)`',
            'Przeniesienie `cena_nawozu` z tabeli `pola` do `nawozy`',
            'Dodanie `suma_plonow` do tabeli `pola` (obliczalne!)'
        ]
    }
    
    st.dataframe(pd.DataFrame(normalizacja_data), use_container_width=True, hide_index=True)
    
    st.markdown("""
    ### 🎯 **Wskazówka ArjanCodes**: Używaj migracji bazy danych!
    ```python
    # ZŁE - zmiany schematu w kodzie
    CREATE TABLE pola (nazwa TEXT, plon REAL)
    # Potem: ALTER TABLE pola ADD COLUMN gleba TEXT  # ❌
    
    # DOBRE - system migracji
    migrations = [
        "CREATE TABLE pola (nazwa TEXT, plon REAL)",
        "ALTER TABLE pola ADD COLUMN gleba TEXT",
        "CREATE INDEX idx_pola_plon ON pola(plon)"
    ]
    
    class DatabaseMigrator:
        def apply_migration(self, version: int):
            # Uruchamia migracje sekwencyjnie
            # Zapisuje wersję w tabeli `schema_version`
            pass  # ✅
    ```
    """)

def cwiczenie_interaktywne():
    st.subheader("🎯 **CRUD operations z interfejsem Streamlit**")
    
    # Połączenie z bazą w pamięci
    conn = sqlite3.connect(':memory:', check_same_thread=False)
    cursor = conn.cursor()
    
    # Utworzenie schematu
    cursor.execute("""
    CREATE TABLE IF NOT EXISTS pola (
        id INTEGER PRIMARY KEY AUTOINCREMENT,
        nazwa TEXT NOT NULL UNIQUE,
        powierzchnia REAL CHECK(powierzchnia > 0),
        gleba TEXT CHECK(gleba IN ('gliniasta', 'piaszczysta', 'ilasta', 'torfiasta')),
        plon_ubiegloroczny REAL,
        data_zasiewu DATE,
        created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
    )
    """)
    
    cursor.execute("""
    CREATE TABLE IF NOT EXISTS zabiegi (
        id INTEGER PRIMARY KEY AUTOINCREMENT,
        pole_id INTEGER REFERENCES pola(id) ON DELETE CASCADE,
        typ TEXT CHECK(typ IN ('nawozenie', 'oprysk', 'nawadnianie', 'zbior')),
        data DATE NOT NULL,
        koszt REAL,
        opis TEXT,
        created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
    )
    """)
    
    conn.commit()
    
    st.markdown("### 📝 **Operacje na bazie danych**")
    
    # CRUD interface
    tab1, tab2, tab3, tab4 = st.tabs(["➕ Dodaj pole", "👁️ Przeglądaj", "✏️ Edytuj", "📊 Statystyki"])
    
    with tab1:
        st.subheader("Dodaj nowe pole")
        
        with st.form("dodaj_pole_form"):
            col1, col2 = st.columns(2)
            with col1:
                nazwa = st.text_input("Nazwa pola*")
                powierzchnia = st.number_input("Powierzchnia (ha)*", 0.1, 100.0, 5.0)
                gleba = st.selectbox("Typ gleby*", ['gliniasta', 'piaszczysta', 'ilasta', 'torfiasta'])
            with col2:
                plon = st.number_input("Plon ubiegłoroczny (t/ha)", 0.0, 20.0, 8.0)
                data_zasiewu = st.date_input("Data zasiewu")
            
            if st.form_submit_button("💾 Zapisz pole"):
                if nazwa:
                    try:
                        cursor.execute("""
                            INSERT INTO pola (nazwa, powierzchnia, gleba, plon_ubiegloroczny, data_zasiewu)
                            VALUES (?, ?, ?, ?, ?)
                        """, (nazwa, powierzchnia, gleba, plon, data_zasiewu))
                        conn.commit()
                        st.success(f"✅ Dodano pole: {nazwa}")
                    except sqlite3.IntegrityError:
                        st.error("❌ Pole o tej nazwie już istnieje!")
                else:
                    st.error("❌ Nazwa pola jest wymagana!")
    
    with tab2:
        st.subheader("Przeglądaj pola")
        
        # Filtrowanie
        col1, col2 = st.columns(2)
        with col1:
            min_plon = st.slider("Minimalny plon (t/ha):", 0.0, 15.0, 0.0)
        with col2:
            gleba_filtr = st.multiselect("Gleba:", ['gliniasta', 'piaszczysta', 'ilasta', 'torfiasta'])
        
        # Zapytanie z filtrami
        query = "SELECT id, nazwa, powierzchnia, gleba, plon_ubiegloroczny FROM pola WHERE 1=1"
        params = []
        
        if min_plon > 0:
            query += " AND plon_ubiegloroczny >= ?"
            params.append(min_plon)
        
        if gleba_filtr:
            query += " AND gleba IN (" + ",".join(["?"] * len(gleba_filtr)) + ")"
            params.extend(gleba_filtr)
        
        df = pd.read_sql_query(query, conn, params=params)
        
        if not df.empty:
            st.dataframe(df, use_container_width=True, hide_index=True)
            
            # Statystyki
            st.subheader("📈 Podsumowanie:")
            col1, col2, col3 = st.columns(3)
            with col1:
                st.metric("Liczba pól", len(df))
            with col2:
                st.metric("Średni plon", f"{df['plon_ubiegloroczny'].mean():.1f} t/ha")
            with col3:
                st.metric("Łączna powierzchnia", f"{df['powierzchnia'].sum():.1f} ha")
        else:
            st.info("ℹ️ Brak pól spełniających kryteria")
    
    with tab3:
        st.subheader("Edytuj lub usuń")
        
        # Wybór pola do edycji
        pola_options = cursor.execute("SELECT id, nazwa FROM pola ORDER BY nazwa").fetchall()
        if pola_options:
            wybrane_pole = st.selectbox(
                "Wybierz pole:",
                [f"{p[0]}: {p[1]}" for p in pola_options]
            )
            pole_id = int(wybrane_pole.split(":")[0])
            
            col1, col2 = st.columns(2)
            with col1:
                if st.button("✏️ Edytuj pole"):
                    st.session_state.edytuj_pole_id = pole_id
                    st.rerun()
            with col2:
                if st.button("🗑️ Usuń pole"):
                    cursor.execute("DELETE FROM pola WHERE id = ?", (pole_id,))
                    conn.commit()
                    st.success("✅ Pole usunięte")
                    st.rerun()
        else:
            st.info("ℹ️ Brak pól w bazie")
    
    with tab4:
        st.subheader("Statystyki zaawansowane")
        
        # Zaawansowane zapytania
        zapytania = {
            "Plon według gleby": """
                SELECT gleba, 
                       AVG(plon_ubiegloroczny) as sredni_plon,
                       COUNT(*) as liczba_pol,
                       SUM(powierzchnia) as laczna_powierzchnia
                FROM pola 
                GROUP BY gleba 
                ORDER BY sredni_plon DESC
            """,
            "Top 5 najlepszych pól": """
                SELECT nazwa, plon_ubiegloroczny, powierzchnia,
                       plon_ubiegloroczny * powierzchnia as calkowity_plon
                FROM pola 
                ORDER BY plon_ubiegloroczny DESC 
                LIMIT 5
            """,
            "Powierzchnia w czasie": """
                SELECT strftime('%Y-%m', created_at) as miesiac,
                       SUM(powierzchnia) as nowa_powierzchnia,
                       (SELECT SUM(powierzchnia) 
                        FROM pola p2 
                        WHERE strftime('%Y-%m', p2.created_at) <= strftime('%Y-%m', p1.created_at)
                       ) as laczna_powierzchnia
                FROM pola p1
                GROUP BY strftime('%Y-%m', created_at)
                ORDER BY miesiac
            """
        }
        
        wybrane_zapytanie = st.selectbox("Wybierz raport:", list(zapytania.keys()))
        
        df_raport = pd.read_sql_query(zapytania[wybrane_zapytanie], conn)
        st.dataframe(df_raport, use_container_width=True)
        
        # Wizualizacja
        if not df_raport.empty and 'sredni_plon' in df_raport.columns:
            st.bar_chart(df_raport.set_index('gleba')['sredni_plon'])
    
    # Zamknięcie połączenia
    conn.close()

def mini_projekt():
    st.subheader("🚀 **ORM-like layer z migracjami**")
    
    kod = st.text_area("✍️ **Zaimplementuj `BazaDanychRolnicza`:**", height=500, value="""import sqlite3
import json
from pathlib import Path
from typing import List, Dict, Optional, Any
from datetime import datetime
from contextlib import contextmanager
import hashlib

class BazaDanychRolnicza:
    '''Warstwa abstrakcji nad SQLite z migracjami i walidacją'''
    
    def __init__(self, sciezka_bazy: str = "gospodarstwo.db"):
        self.sciezka = Path(sciezka_bazy)
        self.polaczenie = None
        
        # Definicja migracji wersja -> SQL
        self.migracje = [
            # Wersja 1 - schemat początkowy
            \"\"\"
            CREATE TABLE IF NOT EXISTS schema_version (
                version INTEGER PRIMARY KEY,
                applied_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
            );
            
            CREATE TABLE pola (
                id INTEGER PRIMARY KEY AUTOINCREMENT,
                nazwa TEXT NOT NULL UNIQUE,
                powierzchnia REAL NOT NULL CHECK(powierzchnia > 0),
                gleba TEXT NOT NULL CHECK(gleba IN ('gliniasta', 'piaszczysta', 'ilasta')),
                created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
            );
            \"\"\",
            # Wersja 2 - dodanie plonów
            \"\"\"
            ALTER TABLE pola ADD COLUMN plon_ubiegloroczny REAL;
            CREATE INDEX idx_pola_plon ON pola(plon_ubiegloroczny);
            \"\"\",
            # Wersja 3 - tabela zabiegów
            \"\"\"
            CREATE TABLE zabiegi (
                id INTEGER PRIMARY KEY AUTOINCREMENT,
                pole_id INTEGER NOT NULL REFERENCES pola(id) ON DELETE CASCADE,
                typ TEXT NOT NULL CHECK(typ IN ('nawozenie', 'oprysk', 'nawadnianie')),
                data DATE NOT NULL,
                koszt REAL DEFAULT 0,
                opis TEXT,
                created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
            );
            CREATE INDEX idx_zabiegi_pole ON zabiegi(pole_id);
            \"\"\"
        ]
    
    @contextmanager
    def polacz(self):
        '''Context manager dla połączenia z bazą'''
        conn = sqlite3.connect(self.sciezka)
        conn.row_factory = sqlite3.Row  # Zwraca słowniki
        try:
            yield conn
            conn.commit()
        except Exception:
            conn.rollback()
            raise
        finally:
            conn.close()
    
    def zainicjalizuj_baze(self):
        '''Uruchamia migracje do najnowszej wersji'''
        with self.polacz() as conn:
            # Sprawdź aktualną wersję
            conn.execute('''
                CREATE TABLE IF NOT EXISTS schema_version (
                    version INTEGER PRIMARY KEY,
                    applied_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
                )
            ''')
            
            aktualna = conn.execute('SELECT MAX(version) as ver FROM schema_version').fetchone()['ver']
            aktualna = aktualna or 0
            
            # Zastosuj brakujące migracje
            for i in range(aktualna, len(self.migracje)):
                conn.executescript(self.migracje[i])
                conn.execute('INSERT INTO schema_version (version) VALUES (?)', (i + 1,))
            
            return len(self.migracje)  # Zwraca nową wersję
    
    # TODO: Dodaj metody CRUD z walidacją
    def dodaj_pole(self, nazwa: str, powierzchnia: float, gleba: str, plon: Optional[float] = None) -> bool:
        '''Dodaje pole z walidacją danych'''
        pass
    
    def znajdz_pola(self, filtr: Optional[Dict] = None) -> List[Dict]:
        '''Znajduje pola według filtrów'''
        pass
    
    def raport_miesieczny(self, rok: int, miesiac: int) -> Dict:
        '''Generuje raport miesięczny'''
        pass
    
    def backup_bazy(self, sciezka_backupu: str):
        '''Tworzy backup bazy z weryfikacją'''
        pass

class PoleModel:
    '''Model reprezentujący pole (Data Class pattern)'''
    def __init__(self, id: Optional[int] = None, nazwa: str = "", 
                 powierzchnia: float = 0.0, gleba: str = "", plon: Optional[float] = None):
        self.id = id
        self.nazwa = nazwa
        self.powierzchnia = powierzchnia
        self.gleba = gleba
        self.plon = plon
        self.created_at = datetime.now()
    
    def to_dict(self) -> Dict:
        return {k: v for k, v in self.__dict__.items() if not k.startswith('_')}
    
    @classmethod
    def from_dict(cls, data: Dict) -> 'PoleModel':
        return cls(**data)
    
    def validate(self) -> List[str]:
        '''Walidacja modelu - zwraca listę błędów'''
        errors = []
        if not self.nazwa.strip():
            errors.append("Nazwa jest wymagana")
        if self.powierzchnia <= 0:
            errors.append("Powierzchnia musi być > 0")
        if self.gleba not in ['gliniasta', 'piaszczysta', 'ilasta']:
            errors.append("Nieprawidłowy typ gleby")
        if self.plon is not None and self.plon < 0:
            errors.append("Plon nie może być ujemny")
        return errors
""")
    
    if st.button("🧪 Testy ORM i migracji", key="testy6"):
        test_code = f"""
import unittest
import tempfile
import json
from pathlib import Path

{kod}

class TestBazaDanychRolnicza(unittest.TestCase):
    def setUp(self):
        self.temp_dir = tempfile.mkdtemp()
        self.sciezka_bazy = Path(self.temp_dir) / "test.db"
        self.baza = BazaDanychRolnicza(str(self.sciezka_bazy))
    
    def tearDown(self):
        import shutil
        shutil.rmtree(self.temp_dir)
    
    def test_inicjalizacja_bazy(self):
        '''Testuje migracje bazy danych'''
        wersja = self.baza.zainicjalizuj_baze()
        self.assertEqual(wersja, 3)  # Mamy 3 migracje
        
        # Sprawdź czy tabele istnieją
        with self.baza.polacz() as conn:
            # Tabela pola
            result = conn.execute(
                "SELECT name FROM sqlite_master WHERE type='table' AND name='pola'"
            ).fetchone()
            self.assertIsNotNone(result)
            
            # Tabela zabiegi
            result = conn.execute(
                "SELECT name FROM sqlite_master WHERE type='table' AND name='zabiegi'"
            ).fetchone()
            self.assertIsNotNone(result)
            
            # Wersja schematu
            result = conn.execute("SELECT MAX(version) as ver FROM schema_version").fetchone()
            self.assertEqual(result['ver'], 3)
    
    def test_context_manager(self):
        '''Testuje context manager połączenia'''
        with self.baza.polacz() as conn:
            self.assertIsInstance(conn, sqlite3.Connection)
            self.assertEqual(conn.row_factory, sqlite3.Row)  # Sprawdź row_factory
    
    def test_pole_model_validation(self):
        '''Testuje walidację modelu Pole'''
        # Poprawne pole
        pole1 = PoleModel(nazwa="Testowe", powierzchnia=5.0, gleba="gliniasta", plon=8.5)
        errors1 = pole1.validate()
        self.assertEqual(len(errors1), 0)
        
        # Niepoprawne pole
        pole2 = PoleModel(nazwa="", powierzchnia=-1, gleba="nieznana", plon=-5)
        errors2 = pole2.validate()
        self.assertGreater(len(errors2), 0)
        self.assertIn("Nazwa jest wymagana", errors2)
        self.assertIn("Powierzchnia musi być > 0", errors2)
        self.assertIn("Nieprawidłowy typ gleby", errors2)
        self.assertIn("Plon nie może być ujemny", errors2)
    
    def test_pole_model_serialization(self):
        '''Testuje serializację/deserializację modelu'''
        pole = PoleModel(id=1, nazwa="Test", powierzchnia=5.0, gleba="gliniasta", plon=8.5)
        
        # To dict
        data = pole.to_dict()
        self.assertEqual(data['nazwa'], "Test")
        self.assertEqual(data['powierzchnia'], 5.0)
        
        # From dict
        pole2 = PoleModel.from_dict(data)
        self.assertEqual(pole2.nazwa, "Test")
        self.assertEqual(pole2.powierzchnia, 5.0)

if __name__ == '__main__':
    unittest.main()
"""
        
        f = StringIO()
        with redirect_stdout(f):
            try:
                exec(test_code)
                st.success("✅ Testy ORM wykonane!")
            except Exception as e:
                st.error(f"❌ Błąd: {e}")
        
        st.code(f.getvalue())

def quiz():
    st.subheader("📝 **Quiz: Bazy danych**")
    
    q1 = st.radio(
        "Co oznacza ACID w kontekście baz danych?",
        ["Atomicity, Consistency, Isolation, Durability",
         "Access, Control, Integrity, Data",
         "Automation, Coding, Integration, Development",
         "Analysis, Calculation, Input, Output"],
        key="q6_1"
    )
    
    if q1 == "Atomicity, Consistency, Isolation, Durability":
        st.success("✅ ACID gwarantuje niezawodność transakcji.")
    
    q2 = st.radio(
        "Jaka jest różnica między INNER JOIN a LEFT JOIN?",
        ["INNER JOIN zwraca tylko pasujące wiersze, LEFT JOIN wszystkie z lewej tabeli",
         "LEFT JOIN jest szybszy niż INNER JOIN",
         "INNER JOIN używa indeksów, LEFT JOIN nie",
         "Nie ma różnicy"],
        key="q6_2"
    )
    
    if q2 == "INNER JOIN zwraca tylko pasujące wiersze, LEFT JOIN wszystkie z lewej tabeli":
        st.success("✅ LEFT JOIN zachowuje wszystkie wiersze z lewej tabeli, nawet bez dopasowania.")

def challenge():
    st.subheader("⚡ **Challenge: Replikacja i optymalizacja**")
    
    st.markdown("""
    ### Zadanie: Zaawansowane techniki bazodanowe
    
    Zaimplementuj system który:
    1. **Replikacja danych** między bazą główną a cache (Redis/SQLite in-memory)
    2. **Zapytania zaawansowane** z optymalizacją wydajności
    3. **Full-text search** dla opisów pól i zabiegów
    4. **Materialized views** dla często używanych raportów
    
    **Wymagania:**
    - System cache'owania wyników zapytań
    - Optymalizacja zapytań z użyciem EXPLAIN QUERY PLAN
    - Full-text search z użyciem FTS5 (SQLite)
    - Automatyczne odświeżanie materialized views
    - Monitoring wydajności zapytań
    
    **Bonus:** Replikacja do bazy zdalnej (PostgreSQL) przez wal replikację
    """)

def run():
    st.sidebar.markdown("## 📖 Nawigacja lekcji 6")
    section = st.sidebar.radio(
        "Przejdź do:",
        ["📚 Teoria", "🎯 Ćwiczenie", "🚀 Projekt", "📝 Quiz", "⚡ Challenge"],
        key="nav6"
    )
    
    if section == "📚 Teoria": teoria()
    elif section == "🎯 Ćwiczenie": cwiczenie_interaktywne()
    elif section == "🚀 Projekt": mini_projekt()
    elif section == "📝 Quiz": quiz()
    elif section == "⚡ Challenge": challenge()
    
    st.markdown("---")
    col1, col2, col3 = st.columns([1, 2, 1])
    with col1:
        if st.button("⏮️ Lekcja 5", key="prev6"):
            st.session_state.selected_lesson = "lesson5"
            st.rerun()
    with col2:
        if st.button("🏠 Strona główna", key="home6"):
            if "selected_lesson" in st.session_state:
                del st.session_state.selected_lesson
            st.rerun()
    with col3:
        if st.button("Lekcja 7 ⏭️", key="next6"):
            st.session_state.selected_lesson = "lesson7"
            st.rerun()

if __name__ == "__main__":
    run()
