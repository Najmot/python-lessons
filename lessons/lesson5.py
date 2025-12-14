import streamlit as st
import pandas as pd
import unittest
import tempfile
import logging
from io import StringIO
from contextlib import redirect_stdout, contextmanager
from pathlib import Path
from typing import Optional, Dict, Any
import json
import csv
import traceback
from datetime import datetime

def teoria():
    st.header("📁 Dzień 5 – Pliki, wyjątki i obsługa błędów")
    st.progress(75)
    
    st.markdown("""
    ## 🛡️ **Professional error handling jak u ArjanCodes**
    
    ### Hierarchia wyjątków w Pythonie:
    ```
    BaseException
    ├── KeyboardInterrupt
    ├── SystemExit
    └── Exception
        ├── ValueError, TypeError, KeyError
        ├── IOError (OSError)
        │   ├── FileNotFoundError
        │   └── PermissionError
        └── RuntimeError
    ```
    
    ### Własne wyjątki dla domeny rolniczej:
    """)
    
    wyjatki_data = {
        'Wyjątek': ['NiewystarczajacyPlonError', 'NieprawidlowaGlebaError', 
                   'BrakWodyError', 'PrzekroczonyBudzetError', 'NieznanaOdmianaError'],
        'Kiedy rzucać': [
            'Plon < minimalny wymagany',
            'Gleba nie spełnia wymagań uprawy',
            'Brak wody do nawadniania',
            'Koszt nawożenia > budżet',
            'Podano nieznaną odmianę'
        ],
        'Przykład': [
            '`raise NiewystarczajacyPlonError(aktualny=5.0, wymagany=7.0)`',
            '`raise NieprawidlowaGlebaError(gleba="piasek", wymagana="glina")`',
            '`raise BrakWodyError(zasoby=1000, wymagane=1500)`',
            '`raise PrzekroczonyBudzetError(budzet=5000, koszt=6000)`',
            '`raise NieznanaOdmianaError(odmiana="XYZ", dostepne=["A","B"])`'
        ]
    }
    
    st.dataframe(pd.DataFrame(wyjatki_data), use_container_width=True, hide_index=True)
    
    st.markdown("""
    ### 🎯 **Wskazówka Josego Portilli**: Zawsze loguj wyjątki!
    ```python
    # ZŁE - tracisz informację o błędzie
    try:
        oblicz_plon()
    except:
        pass  # ❌ CICHY BŁĄD!
    
    # DOBRE - loguj i obsłuż
    try:
        oblicz_plon()
    except NiewystarczajacyPlonError as e:
        logger.error(f"Plon niewystarczający: {e}")
        wyslij_alert()
    except Exception as e:
        logger.exception("Nieoczekiwany błąd")
        raise  # ✅ Przekaż dalej z kontekstem
    ```
    """)

def cwiczenie_interaktywne():
    st.subheader("🎯 **Import/export danych z walidacją**")
    
    # Przykładowe dane CSV
    przykladowy_csv = """pole,plon,powierzchnia,gleba,cena
Pole A,8.3,5.2,gliniasta,850
Pole B,7.9,3.8,piaszczysta,820
Pole C,9.2,7.1,gliniasta,880
Pole D,6.8,4.5,ilasta,800"""
    
    st.text_area("📄 **Przykładowy plik CSV:**", przykladowy_csv, height=150)
    
    # Upload pliku
    uploaded_file = st.file_uploader("Lub wgraj własny plik CSV:", type=['csv'])
    
    if uploaded_file or st.button("Użyj przykładowych danych", key="use_sample"):
        try:
            # Wczytaj dane
            if uploaded_file:
                df = pd.read_csv(uploaded_file)
            else:
                df = pd.read_csv(StringIO(przykladowy_csv))
            
            st.success(f"✅ Wczytano {len(df)} wierszy")
            st.dataframe(df, use_container_width=True)
            
            # Walidacja
            st.subheader("🔍 **Wyniki walidacji:**")
            
            errors = []
            warnings = []
            
            # Sprawdź wymagane kolumny
            required_cols = {'pole', 'plon', 'powierzchnia'}
            missing = required_cols - set(df.columns)
            if missing:
                errors.append(f"Brakujące kolumny: {missing}")
            
            # Sprawdź wartości liczbowe
            if 'plon' in df.columns:
                invalid_plon = df[df['plon'] <= 0]
                if not invalid_plon.empty:
                    errors.append(f"Nieprawidłowy plon w wierszach: {list(invalid_plon.index)}")
            
            if 'powierzchnia' in df.columns:
                invalid_pow = df[df['powierzchnia'] <= 0]
                if not invalid_pow.empty:
                    errors.append(f"Nieprawidłowa powierzchnia w wierszach: {list(invalid_pow.index)}")
            
            # Wyświetl wyniki
            if errors:
                st.error("❌ **Błędy krytyczne:**")
                for err in errors:
                    st.write(f"- {err}")
            else:
                st.success("✅ Brak błędów krytycznych")
            
            if warnings:
                st.warning("⚠️ **Ostrzeżenia:**")
                for warn in warnings:
                    st.write(f"- {warn}")
            
            # Eksport poprawionych danych
            if st.button("📤 Eksportuj poprawione dane do JSON", key="export"):
                # Konwersja do JSON
                json_data = df.to_dict(orient='records')
                st.download_button(
                    label="Pobierz JSON",
                    data=json.dumps(json_data, indent=2, ensure_ascii=False),
                    file_name="dane_pol_poprawione.json",
                    mime="application/json"
                )
                
        except Exception as e:
            st.error(f"❌ Błąd przetwarzania: {str(e)}")
            st.code(traceback.format_exc())

def mini_projekt():
    st.subheader("🚀 **Menadżer raportów z logowaniem**")
    
    kod = st.text_area("✍️ **Zaimplementuj `ManagerRaportow`:**", height=450, value="""import logging
import json
import csv
from pathlib import Path
from typing import Dict, List, Any, Optional
from datetime import datetime
import traceback

class BlednyFormatDanychError(Exception):
    '''Własny wyjątek dla błędów w danych'''
    def __init__(self, komunikat: str, dane_problemowe: Any = None):
        super().__init__(komunikat)
        self.dane_problemowe = dane_problemowe
        self.czas = datetime.now()

class ManagerRaportow:
    '''Klasa do zarządzania raportami z pełną obsługą błędów i logowaniem'''
    
    def __init__(self, katalog_raportow: str = "raporty"):
        self.katalog = Path(katalog_raportow)
        self.katalog.mkdir(exist_ok=True)
        
        # Konfiguracja loggera
        self.logger = logging.getLogger(__name__)
        if not self.logger.handlers:
            handler = logging.FileHandler(self.katalog / "aplikacja.log")
            formatter = logging.Formatter(
                '%(asctime)s - %(name)s - %(levelname)s - %(message)s'
            )
            handler.setFormatter(formatter)
            self.logger.addHandler(handler)
            self.logger.setLevel(logging.INFO)
    
    def zapisz_raport_json(self, dane: Dict, nazwa_pliku: str) -> bool:
        '''Zapisuje raport w formacie JSON z walidacją'''
        # TODO: Zaimplementuj z obsługą błędów i logowaniem
        try:
            # Walidacja danych
            if not isinstance(dane, dict):
                raise BlednyFormatDanychError("Dane muszą być słownikiem", dane)
            
            # Sprawdź klucze wymagane
            wymagane_klucze = {'data', 'tytul', 'dane'}
            brakujace = wymagane_klucze - set(dane.keys())
            if brakujace:
                raise BlednyFormatDanychError(
                    f"Brakujące klucze: {brakujace}", 
                    list
