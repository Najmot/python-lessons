import streamlit as st
import pandas as pd
import numpy as np
import matplotlib.pyplot as plt
import plotly.express as px
import plotly.graph_objects as go
from plotly.subplots import make_subplots
import seaborn as sns
import unittest
from io import StringIO, BytesIO
from contextlib import redirect_stdout
import base64
from datetime import datetime, timedelta
import json
import tempfile
from pathlib import Path

# Konfiguracja strony
st.set_page_config(layout="wide", page_title="Wizualizacje i Dashboard")

def teoria():
    st.header("📈 Dzień 7 – Wizualizacje, dashboardy i deployment")
    st.progress(100)
    
    col1, col2 = st.columns([2, 1])
    
    with col1:
        st.markdown("""
        ## 🎨 **Dashboardy biznesowe jak u ArjanCodes - Storytelling z danymi**
        
        ### Zasady efektywnej wizualizacji:
        1. **Know your audience** - Inny dashboard dla rolnika, inny dla inwestora
        2. **Less is more** - Mniej elementów = lepsza czytelność
        3. **Story over data** - Opowiedz historię, nie pokazuj tylko liczb
        4. **Consistency** - Spójne kolory, skale, typy wykresów
        5. **Actionable insights** - Dashboard powinien prowadzić do decyzji
        """)
    
    with col2:
        st.success("""
        **🎯 Cel lekcji:**
        - Stworzyć interaktywny dashboard
        - Zoptymalizować wydajność wizualizacji
        - Wdrożyć aplikację na Streamlit Cloud
        - Zabezpieczyć i monitorować deployment
        """)
    
    st.markdown("""
    ### 📊 **Porównanie bibliotek wizualizacji:**
    """)
    
    viz_libs = {
        'Biblioteka': ['Matplotlib', 'Seaborn', 'Plotly', 'Altair', 'Bokeh'],
        'Mocne strony': [
            'Pełna kontrola, stabilna',
            'Ładne domyślne style, prosta',
            'Interaktywność, łatwość użycia',
            'Deklaratywna, wektorowa',
            'Interaktywność, streaming'
        ],
        'Słabe strony': [
            'Mało interaktywna, verbose',
            'Ograniczona interaktywność',
            'Większy rozmiar, zależności',
            'Mniej kontroli nad szczegółami',
            'Krzywa uczenia się'
        ],
        'Kiedy używać': [
            'Publikacje naukowe, pełna kontrola',
            'Eksploracja danych, szybkie prototypowanie',
            'Dashboardy, aplikacje webowe',
            'Raporty, wizualizacje statyczne',
            'Aplikacje real-time, streaming'
        ]
    }
    
    st.dataframe(pd.DataFrame(viz_libs), use_container_width=True, hide_index=True)
    
    st.markdown("""
    ### 🎯 **Wskazówka Corey'ego Schafera**: Automatyzuj generowanie raportów!
    ```python
    # ZŁE - ręczne tworzenie raportów
    plt.figure()
    plt.plot(dane)
    plt.savefig('raport.png')  # ❌ Manualne
    
    # DOBRE - automatyczny pipeline
    class RaportGenerator:
        def generuj_raport_miesieczny(self, rok, miesiac):
            # Automatycznie pobiera dane
            # Generuje wykresy
            # Eksportuje do PDF/HTML
            # Wysyła mailem
            pass  # ✅
    ```
    """)

def cwiczenie_interaktywne():
    st.subheader("🎯 **Interaktywny dashboard rolniczy**")
    
    # Generowanie przykładowych danych
    np.random.seed(42)
    miesiace = ['Sty', 'Lut', 'Mar', 'Kwi', 'Maj', 'Cze', 'Lip', 'Sie', 'Wrz', 'Paź', 'Lis', 'Gru']
    
    # Symulacja danych rocznych
    dane = {
        'miesiac': miesiace * 3,
        'rok': ['2022']*12 + ['2023']*12 + ['2024']*12,
        'typ': ['plon']*36 + ['koszt']*36 + ['cena']*36,
        'wartosc': np.concatenate([
            np.random.normal(8, 1.5, 36),  # plony
            np.random.normal(1200, 300, 36),  # koszty
            np.random.normal(850, 100, 36)  # ceny
        ])
    }
    
    df = pd.DataFrame(dane)
    
    # Filtry
    st.sidebar.header("🔍 Filtry dashboardu")
    
    selected_years = st.sidebar.multiselect(
        "Wybierz lata:",
        options=['2022', '2023', '2024'],
        default=['2023', '2024']
    )
    
    selected_metrics = st.sidebar.multiselect(
        "Wybierz metryki:",
        options=['plon', 'koszt', 'cena'],
        default=['plon', 'koszt']
    )
    
    # Filtruj dane
    filtered_df = df[
        (df['rok'].isin(selected_years)) & 
        (df['typ'].isin(selected_metrics))
    ]
    
    # Layout dashboardu
    col1, col2 = st.columns([2, 1])
    
    with col1:
        st.subheader("📈 Trendy czasowe")
        
        if not filtered_df.empty:
            # Wykres liniowy Plotly
            fig = px.line(
                filtered_df, 
                x='miesiac', 
                y='wartosc', 
                color='typ',
                line_dash='rok',
                title='Trendy miesięczne',
                labels={'wartosc': 'Wartość', 'miesiac': 'Miesiąc'},
                height=400
            )
            
            # Dodanie slidera zakresu
            fig.update_layout(
                xaxis=dict(
                    rangeselector=dict(
                        buttons=list([
                            dict(count=1, label="1m", step="month", stepmode="backward"),
                            dict(count=6, label="6m", step="month", stepmode="backward"),
                            dict(count=1, label="YTD", step="year", stepmode="todate"),
                            dict(step="all")
                        ])
                    ),
                    rangeslider=dict(visible=True),
                    type="category"
                )
            )
            
            st.plotly_chart(fig, use_container_width=True)
    
    with col2:
        st.subheader("📊 Podsumowanie")
        
        # KPI cards
        if not filtered_df.empty:
            # Średni plon
            avg_yield = filtered_df[filtered_df['typ'] == 'plon']['wartosc'].mean()
            st.metric("Średni plon", f"{avg_yield:.1f} t/ha", 
                     delta=f"{(avg_yield - 8):+.1f} vs. target")
            
            # Średni koszt
            avg_cost = filtered_df[filtered_df['typ'] == 'koszt']['wartosc'].mean()
            st.metric("Średni koszt", f"{avg_cost:.0f} zł/ha")
            
            # ROI
            avg_price = filtered_df[filtered_df['typ'] == 'cena']['wartosc'].mean()
            roi = (avg_yield * avg_price) / avg_cost if avg_cost > 0 else 0
            st.metric("ROI", f"{roi:.2f}", 
                     delta="Wskaźnik zwrotu")
        
        # Wykres kołowy udziału kosztów
        if 'koszt' in selected_metrics:
            cost_breakdown = {
                'Nawozy': 40,
                'Paliwo': 25,
                'Robocizna': 20,
                'Maszyny': 15
            }
            
            fig_pie = px.pie(
                values=list(cost_breakdown.values()),
                names=list(cost_breakdown.keys()),
                title='Struktura kosztów',
                hole=0.4
            )
            st.plotly_chart(fig_pie, use_container_width=True)
    
    # Drugi rząd - zaawansowane wizualizacje
    st.subheader("🔍 Zaawansowane analizy")
    
    tab1, tab2, tab3 = st.tabs(["Korelacje", "Histogram", "Mapa cieplna"])
    
    with tab1:
        # Macierz korelacji
        corr_data = pd.DataFrame({
            'Plon': np.random.normal(8, 1.5, 100),
            'Temperatura': np.random.normal(18, 5, 100),
            'Opady': np.random.normal(50, 20, 100),
            'Wilgotność': np.random.normal(60, 15, 100)
        })
        
        corr_matrix = corr_data.corr()
        
        fig_corr = px.imshow(
            corr_matrix,
            text_auto=True,
            aspect="auto",
            color_continuous_scale='RdBu',
            title='Korelacja między zmiennymi'
        )
        st.plotly_chart(fig_corr, use_container_width=True)
    
    with tab2:
        # Histogram z krzywą gęstości
        fig_hist = px.histogram(
            filtered_df[filtered_df['typ'] == 'plon'],
            x='wartosc',
            nbins=20,
            marginal="rug",
            title='Rozkład plonów',
            labels={'wartosc': 'Plon (t/ha)'}
        )
        st.plotly_chart(fig_hist, use_container_width=True)
    
    with tab3:
        # Mapa cieplna czasowa
        heatmap_data = filtered_df.pivot_table(
            index='miesiac',
            columns='rok',
            values='wartosc',
            aggfunc='mean'
        ).reindex(miesiace)
        
        fig_heat = px.imshow(
            heatmap_data,
            text_auto=True,
            aspect="auto",
            title='Mapa cieplna - porównanie lat',
            labels=dict(x="Rok", y="Miesiąc", color="Wartość")
        )
        st.plotly_chart(fig_heat, use_container_width=True)
    
    # Eksport dashboardu
    st.sidebar.markdown("---")
    st.sidebar.subheader("📤 Eksport")
    
    if st.sidebar.button("💾 Eksportuj do HTML"):
        # Generowanie HTML raportu
        html_content = f"""
        <html>
        <head><title>Dashboard Rolniczy</title></head>
        <body>
            <h1>Dashboard Rolniczy - {datetime.now().strftime('%Y-%m-%d')}</h1>
            <p>Wygenerowano: {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}</p>
            <p>Lata: {', '.join(selected_years)}</p>
            <p>Metryki: {', '.join(selected_metrics)}</p>
        </body>
        </html>
        """
        
        st.sidebar.download_button(
            label="⬇️ Pobierz raport",
            data=html_content,
            file_name=f"dashboard_{datetime.now().strftime('%Y%m%d_%H%M%S')}.html",
            mime="text/html"
        )

def mini_projekt():
    st.subheader("🚀 **Deployment aplikacji na Streamlit Cloud**")
    
    st.markdown("""
    ### 📋 **Kroki deploymentu:**
    
    1. **Przygotowanie kodu**
       ```python
       # requirements.txt - ZAWSZE precyzyjne wersje!
       streamlit==1.28.0
       pandas==2.0.3
       plotly==5.17.0
       numpy==1.24.0
       matplotlib==3.7.0
       ```
    
    2. **Struktura projektu**
       ```
       your-app/
       ├── app.py              # Główny plik
       ├── requirements.txt    # Zależności
       ├── .streamlit/         # Konfiguracja
       │   └── config.toml
       └── pages/              # Dodatkowe strony
           └── 2_analiza.py
       ```
    
    3. **Konfiguracja (.streamlit/config.toml)**
       ```toml
       [theme]
       primaryColor = "#4CAF50"
       backgroundColor = "#FFFFFF"
       secondaryBackgroundColor = "#F0F2F6"
       textColor = "#31333F"
       font = "sans serif"
       
       [server]
       maxUploadSize = 200  # MB
       enableCORS = false
       ```
    """)
    
    # Generator requirements.txt
    st.subheader("🧰 Generator requirements.txt")
    
    libraries = st.multiselect(
        "Wybierz biblioteki dla Twojej aplikacji:",
        [
            "streamlit", "pandas", "numpy", "plotly", "matplotlib",
            "seaborn", "scikit-learn", "sqlalchemy", "pytest",
            "python-dotenv", "cryptography", "pillow"
        ],
        default=["streamlit", "pandas", "numpy", "plotly"]
    )
    
    versions = {}
    for lib in libraries:
        col1, col2 = st.columns([3, 1])
        with col1:
            st.write(f"**{lib}**")
        with col2:
            version = st.selectbox(
                f"Wersja {lib}",
                ["==1.0.0", "==latest", ">=1.0.0", ""],
                key=f"ver_{lib}",
                label_visibility="collapsed"
            )
            versions[lib] = version
    
    if st.button("📄 Generuj requirements.txt"):
        req_content = "\n".join([f"{lib}{ver}" for lib, ver in versions.items()])
        st.code(req_content, language="text")
        
        st.download_button(
            label="⬇️ Pobierz requirements.txt",
            data=req_content,
            file_name="requirements.txt",
            mime="text/plain"
        )
    
    # Deployment checklist
    st.subheader("✅ Checklista przed deploymentem")
    
    checklist_items = {
        "Czy requirements.txt ma precyzyjne wersje?": False,
        "Czy sekrety są w .env (NIE w kodzie)?": False,
        "Czy testy przechodzą?": False,
        "Czy logowanie jest skonfigurowane?": False,
        "Czy error pages są obsłużone?": False,
        "Czy CORS jest skonfigurowany?": False,
        "Czy rozmiar uploadu jest limitowany?": False
    }
    
    for item, default in checklist_items.items():
        checklist_items[item] = st.checkbox(item, value=default)
    
    all_checked = all(checklist_items.values())
    
    if all_checked:
        st.success("🎉 Wszystkie punkty odhaczone! Możesz deployować!")
        
        # Przycisk deploymentu (symulacja)
        if st.button("🚀 Zdeployuj na Streamlit Cloud"):
            st.balloons()
            st.info("""
            **Kroki deploymentu:**
            1. Pushuj kod na GitHub
            2. Zaloguj się na streamlit.io/cloud
            3. Kliknij "New app"
            4. Wybierz repo i branch
            5. Wpisz ścieżkę do app.py
            6. Kliknij "Deploy"
            
            **Twoja aplikacja będzie dostępna pod:**  
            `https://nazwa-twojej-aplikacji.streamlit.app`
            """)
    else:
        st.warning("⚠️ Ukończ checklistę przed deploymentem!")

def quiz():
    st.subheader("📝 **Quiz: Wizualizacja i deployment**")
    
    q1 = st.radio(
        "Która zasada dotyczy efektywnego dashboardu?",
        ["Im więcej wykresów tym lepiej", 
         "Każdy wykres powinien prowadzić do akcji/decyzji",
         "Używaj jak najwięcej kolorów",
         "Ukryj dane źródłowe"],
        key="q7_1"
    )
    
    if q1 == "Każdy wykres powinien prowadzić do akcji/decyzji":
        st.success("✅ Dashboard ma dostarczać actionable insights!")
    
    q2 = st.radio(
        "Dlaczego w requirements.txt powinny być precyzyjne wersje?",
        ["Żeby kod był ładniejszy",
         "Żeby uniknąć breaking changes przy deploymentzie",
         "Żeby aplikacja była szybsza",
         "To wymóg Streamlit Cloud"],
        key="q7_2"
    )
    
    if q2 == "Żeby uniknąć breaking changes przy deploymentzie":
        st.success("✅ Precyzyjne wersje gwarantują powtarzalność środowiska.")

def challenge():
    st.subheader("⚡ **Challenge: CI/CD i monitoring**")
    
    st.markdown("""
    ### Zadanie: Profesjonalny pipeline deploymentu
    
    Zaimplementuj pełny pipeline CI/CD:
    1. **Automatyczne testy** przy każdym pushu (GitHub Actions)
    2. **Automatyczny deployment** na Streamlit Cloud po merge do main
    3. **Monitoring** aplikacji (uptime, performance, errors)
    4. **Alerty** gdy coś się zepsuje
    
    **Wymagania:**
    - GitHub Actions workflow z testami
    - Automatyczny deployment na staging/production
    - Integracja z Sentry/Bugsnag dla error tracking
    - Uptime monitoring (pingdom/statuscake)
    - Performance monitoring (Lighthouse scores)
    
    **Konfiguracja .github/workflows/deploy.yml:**
    ```yaml
    name: Deploy to Streamlit Cloud
    on:
      push:
        branches: [main]
      pull_request:
        branches: [main]
    
    jobs:
      test:
        runs-on: ubuntu-latest
        steps:
          - uses: actions/checkout@v2
          - uses: actions/setup-python@v2
          - run: pip install -r requirements.txt
          - run: python -m pytest tests/ -v
    
      deploy:
        needs: test
        runs-on: ubuntu-latest
        if: github.ref == 'refs/heads/main'
        steps:
          - run: |
              # Skrypt deploymentu
              echo "Deploying to Streamlit Cloud..."
    ```
    
    **Bonus:** Canary deployments i rollback automation
    """)

def run():
    st.sidebar.markdown("## 📖 Nawigacja lekcji 7")
    section = st.sidebar.radio(
        "Przejdź do:",
        ["📚 Teoria", "🎯 Ćwiczenie", "🚀 Projekt", "📝 Quiz", "⚡ Challenge"],
        key="nav7"
    )
    
    if section == "📚 Teoria": teoria()
    elif section == "🎯 Ćwiczenie": cwiczenie_interaktywne()
    elif section == "🚀 Projekt": mini_projekt()
    elif section == "📝 Quiz": quiz()
    elif section == "⚡ Challenge": challenge()
    
    # Stopka z certyfikatem
    st.markdown("---")
    
    col1, col2, col3 = st.columns([1, 2, 1])
    
    with col1:
        if st.button("⏮️ Lekcja 6", key="prev7"):
            st.session_state.selected_lesson = "lesson6"
            st.rerun()
    
    with col2:
        if st.button("🎓 Generuj certyfikat ukończenia", key="certificate"):
            st.balloons()
            st.success("""
            🎉 **GRATULACJE! Ukończyłeś cały kurs!**
            
            **Certyfikat ukończenia:**  
            Kurs Python dla Rolnictwa - Wersja Premium  
            **Imię:** ...  
            **Data:** ...  
            **Umiejętności:** Python, Streamlit, OOP, Bazy danych, Dashboardy
            
            *Certyfikat dostępny do pobrania po implementacji systemu certyfikatów*
            """)
    
    with col3:
        if st.button("🏠 Strona główna", key="home7"):
            if "selected_lesson" in st.session_state:
                del st.session_state.selected_lesson
            st.rerun()

if __name__ == "__main__":
    run()
