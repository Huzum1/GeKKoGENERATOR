import streamlit as st
import random
import json
from datetime import datetime

# Configurare pagină
st.set_page_config(
    page_title="GENERATOR DE BANI ♣️ - GeKKo 🐲",
    page_icon="🐲",
    layout="wide"
)

# Inițializare session state
if 'runde_salvate' not in st.session_state:
    st.session_state.runde_salvate = []
if 'combinatii_generate' not in st.session_state:
    st.session_state.combinatii_generate = []

# Funcții helper
def valideaza_runda(runda_text, numar_numere_asteptat, numar_min, numar_max):
    """Validează o rundă introdusă de utilizator"""
    try:
        # Curăță spațiile și împarte după virgulă
        numere = [int(x.strip()) for x in runda_text.strip().split(',')]
        
        # Verifică că sunt cel puțin 1 număr
        if len(numere) < 1:
            return False, "Eroare: Runda trebuie să conțină cel puțin un număr"
        
        # FĂRĂ VERIFICARE DE INTERVAL - ORICE NUMERE SUNT ACCEPTATE
        return True, numere
    except ValueError:
        return False, "Eroare: Format invalid - folosește virgulă între numere (ex: 2, 6, 8, 55, 45, 37, 27)"

def genereaza_combinatii(numar_combinatii, numar_numere, numar_min, numar_max, runde_existente=[]):
    """Generează combinații aleatorii de numere"""
    combinatii = []
    
    for i in range(numar_combinatii):
        # Generează o combinație aleatorie unică
        combinatie = sorted(random.sample(range(numar_min, numar_max + 1), numar_numere))
        combinatii.append(combinatie)
    
    return combinatii

def formateaza_combinatie(id_combinatie, combinatie):
    """Formatează o combinație în formatul ID, numere"""
    numere_str = ' '.join(map(str, combinatie))
    return f"{id_combinatie}, {numere_str}"

# HEADER
st.title("🐲 GENERATOR DE BANI ♣️ - GeKKo 🐲")
st.markdown("---")

# MAIN PAGE

# Configurare INIȚIALĂ (definită înainte de orice altceva)
# Valorile se vor actualiza mai jos în interfață
if 'numar_min' not in st.session_state:
    st.session_state.numar_min = 1
if 'numar_max' not in st.session_state:
    st.session_state.numar_max = 49
if 'numar_numere_per_combinatie' not in st.session_state:
    st.session_state.numar_numere_per_combinatie = 7

# Secțiunea 1: ISTORIC RUNDE
st.header("📋 Istoric Runde")

col1, col2 = st.columns([2, 1])

with col1:
    # Import fișier
    uploaded_file = st.file_uploader(
        "📁 Importă runde din fișier .txt",
        type=['txt'],
        help="Fiecare rundă pe o linie nouă, numere separate prin virgulă. FĂRĂ LIMITE - orice numere și orice cantitate!"
    )
    
    if uploaded_file is not None:
        try:
            content = uploaded_file.read().decode('utf-8')
            linii = content.strip().split('\n')
            
            runde_noi = []
            erori = []
            
            for idx, linie in enumerate(linii, 1):
                if linie.strip():
                    valid, rezultat = valideaza_runda(
                        linie,
                        st.session_state.numar_numere_per_combinatie,
                        st.session_state.numar_min,
                        st.session_state.numar_max
                    )
                    if valid:
                        runde_noi.append(rezultat)
                    else:
                        erori.append(f"Linia {idx}: {rezultat}")
            
            if runde_noi:
                st.session_state.runde_salvate.extend(runde_noi)
                st.success(f"✅ {len(runde_noi)} runde valide au fost importate!")
            
            if erori:
                with st.expander("⚠️ Vezi erorile la import"):
                    for eroare in erori:
                        st.error(eroare)
        
        except Exception as e:
            st.error(f"❌ Eroare la citirea fișierului: {str(e)}")

with col2:
    if st.session_state.runde_salvate:
        if st.button("🗑️ Șterge toate rundele", type="secondary"):
            st.session_state.runde_salvate = []
            st.rerun()

# Adăugare manuală - ASCUNSĂ în expander
with st.expander("✍️ Adaugă runde manual"):
    runda_manuala = st.text_area(
        f"Introduceți rundele (FĂRĂ LIMITE - orice numere, orice cantitate)",
        height=150,
        placeholder=f"Exemplu:\n2, 6, 8, 155, 245\n500, 1000, 2500, 5000\n1, 2, 3, 4, 5, 6, 7, 8, 9, 10",
        help="Fiecare rundă pe o linie nouă - COMPLET LIBER, fără limite!",
        key="text_area_runde"
    )
    
    if st.button("➕ Adaugă rundele", type="primary"):
        if runda_manuala.strip():
            linii = runda_manuala.strip().split('\n')
            runde_adaugate = 0
            
            for linie in linii:
                if linie.strip():
                    valid, rezultat = valideaza_runda(
                        linie,
                        st.session_state.numar_numere_per_combinatie,
                        st.session_state.numar_min,
                        st.session_state.numar_max
                    )
                    if valid:
                        st.session_state.runde_salvate.append(rezultat)
                        runde_adaugate += 1
                    else:
                        st.error(rezultat)
            
            if runde_adaugate > 0:
                st.success(f"✅ {runde_adaugate} runde valide au fost adăugate!")
                st.rerun()
        else:
            st.warning("⚠️ Introduceți cel puțin o rundă!")

# Afișare runde salvate
if st.session_state.runde_salvate:
    st.info(f"💾 **Au fost introduse {len(st.session_state.runde_salvate)} runde valide** (salvate în browser)")
    
    with st.expander("👁️ Vezi rundele salvate"):
        for idx, runda in enumerate(st.session_state.runde_salvate, 1):
            st.text(f"{idx}. [{len(runda)} numere] {', '.join(map(str, runda))}")

st.markdown("---")

# Secțiunea CONFIGURARE - MINIMALISTĂ și COMPACTĂ
st.markdown("### ⚙️ Configurare")

# Număr minim rămâne ascuns, mereu 1
numar_min = 1
st.session_state.numar_min = numar_min

# Afișăm doar Max și Numere
col1, col2 = st.columns(2)

with col1:
    numar_max = st.number_input(
        "Max",
        min_value=2,
        max_value=999999,
        value=st.session_state.numar_max,
        step=1,
        key='input_numar_max'
    )
    st.session_state.numar_max = numar_max

with col2:
    numar_numere_per_combinatie = st.number_input(
        "Numere",
        min_value=1,
        max_value=1000,
        value=st.session_state.numar_numere_per_combinatie,
        step=1,
        key='input_numar_numere'
    )
    st.session_state.numar_numere_per_combinatie = numar_numere_per_combinatie

st.markdown("---")

# Secțiunea GENERARE - COMPACTĂ
col_gen1, col_gen2 = st.columns([1, 2])

with col_gen1:
    numar_combinatii = st.number_input(
        "Câte combinații",
        min_value=1,
        max_value=100000,
        value=100,
        step=10
    )

with col_gen2:
    st.markdown("<br>", unsafe_allow_html=True)  # Spațiu pentru aliniere
    if st.button("🚀 GENEREAZĂ", type="primary", use_container_width=True):
        with st.spinner('Generare...'):
            combinatii = genereaza_combinatii(
                numar_combinatii,
                numar_numere_per_combinatie,
                numar_min,
                numar_max,
                st.session_state.runde_salvate
            )
            st.session_state.combinatii_generate = combinatii
            st.success(f"✅ {len(combinatii)} combinații generate!")

st.markdown("---")

# Secțiunea 4: PREVIEW REZULTATE
if st.session_state.combinatii_generate:
    st.header("📊 Rezultate Generate")
    
    # Pregătim toate variantele pentru copiere
    toate_variantele = '\n'.join([
        formateaza_combinatie(i+1, comb) 
        for i, comb in enumerate(st.session_state.combinatii_generate)
    ])
    
    # EXPANDER pentru copiere manuală - SIMPLU și EFICIENT
    with st.expander("📋 Vezi textul pentru copiere manuală (dacă e nevoie)"):
        st.code(toate_variantele, language=None)
    
    st.markdown("---")
    
    # Preview în CHENAR SCROLLABLE - TOATE combinațiile
    st.subheader(f"📜 Preview combinații ({len(st.session_state.combinatii_generate)} total)")
    
    # Cream textul cu TOATE combinațiile
    toate_combinatii_text = []
    for i, comb in enumerate(st.session_state.combinatii_generate, 1):
        toate_combinatii_text.append(formateaza_combinatie(i, comb))
    
    # Text area scrollable cu TOATE combinațiile
    st.text_area(
        "Primele 10 vizibile, scroll pentru restul:",
        value='\n'.join(toate_combinatii_text),
        height=300,
        disabled=True,
        key="preview_toate_combinatiile"
    )
    
    st.markdown("---")
    
    # Secțiunea 5: EXPORT
    st.header("💾 Export")
    
    # Generează conținutul fișierului
    continut_fisier = '\n'.join([
        formateaza_combinatie(i+1, comb)
        for i, comb in enumerate(st.session_state.combinatii_generate)
    ])
    
    timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
    nume_fisier = f"combinatii_loto_{timestamp}.txt"
    
    st.download_button(
        label="📥 Descarcă .txt",
        data=continut_fisier,
        file_name=nume_fisier,
        mime="text/plain",
        type="primary",
        use_container_width=True
    )
    
    st.success(f"✅ Fișierul va fi salvat ca: {nume_fisier}")

# Footer
st.markdown("---")
st.markdown(
    "<div style='text-align: center; color: gray;'>"
    "🐲 GENERATOR DE BANI ♣️ - GeKKo 🐲 | Noroc la joc!"
    "</div>",
    unsafe_allow_html=True
)