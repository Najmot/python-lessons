import streamlit as st

def run():
    st.header("🗃️ Dzień 6 – Bazy danych SQL")
    
    st.progress(85)
    st.caption("Postęp w kursie: 85%")
    
    st.markdown("""
    ## 📊 Przechowywanie danych rolniczych
    
    W tej lekcji poznasz podstawy pracy z bazą danych SQLite w Pythonie.
    Nauczysz się tworzyć tabele, zapisywać w nich dane (np. plony z pól) i odczytywać je.
    
    ### Kluczowe pojęcia:
    - **SQLite** - lekka baza danych w jednym pliku
    - **Połączenie z bazą** (`sqlite3.connect()`)
    - **Kursor** - do wykonywania poleceń SQL
    - **Zapytania** `CREATE TABLE`, `INSERT`, `SELECT`
    """)
    
    st.subheader("💻 Przykład: Tabela z danymi pól")
    
    st.code("""import sqlite3

# Połączenie z bazą (plik zostanie utworzony)
polaczenie = sqlite3.connect('dane_rolnicze.db')
kursor = polaczenie.cursor()

# Utworzenie tabeli
kursor.execute('''
    CREATE TABLE IF NOT EXISTS pola (
        id INTEGER PRIMARY KEY,
        nazwa TEXT,
        powierzchnia REAL,
        plon REAL,
        data_siewu TEXT
    )
''')

# Wstawienie przykładowych danych
kursor.execute('''
    INSERT INTO pola (nazwa, powierzchnia, plon, data_siewu)
    VALUES (?, ?, ?, ?)
''', ('Pole A', 5.2, 8.3, '2023-09-15'))

polaczenie.commit()
polaczenie.close()
print("✅ Dane zapisane do bazy!")
""", language='python')
    
    # Ćwiczenie
    st.subheader("🎯 Ćwiczenie: Zapisz swoje dane")
    
    with st.expander("Kliknij, aby rozwinąć ćwiczenie"):
        st.write("""
        1. Zmodyfikuj powyższy kod, aby dodać do tabeli swoje własne pole.
        2. Użyj zmiennych: `nazwa = 'Twoje pole'`, `powierzchnia = 3.8`, `plon = 7.5`.
        3. Sprawdź, czy plik `dane_rolnicze.db` pojawił się w folderze z kodem.
        """)
    
    st.markdown("---")
    if st.button("🏠 Strona główna"):
        st.session_state.selected_lesson = None
        st.rerun()
