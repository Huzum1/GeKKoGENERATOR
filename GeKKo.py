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
        
        # Verifică intervalul
        for num in numere:
            if num < numar_min or num > numar_max:
                return False, f"Eroare: Numerele trebuie să fie în intervalul {numar_min}-{numar_max}"
        
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

# SIDEBAR - Configurare
st.sidebar.header("⚙️ Configurare")

numar_min = st.sidebar.number_input(
    "Număr minim",
    min_value=1,
    max_value=100,
    value=1,
    step=1
)

numar_max = st.sidebar.number_input(
    "Număr maxim",
    min_value=numar_min + 1,
    max_value=200,
    value=49,
    step=1
)

numar_numere_per_combinatie = st.sidebar.number_input(
    "Câte numere per combinație",
    min_value=1,
    max_value=20,
    value=7,
    step=1
)

st.sidebar.markdown("---")
st.sidebar.info(f"📊 Configurare curentă:\n- Interval: {numar_min} - {numar_max}\n- Numere per combinație: {numar_numere_per_combinatie}")

# MAIN PAGE

# Secțiunea 1: ISTORIC RUNDE
st.header("📋 Istoric Runde")

col1, col2 = st.columns([2, 1])

with col1:
    # Import fișier
    uploaded_file = st.file_uploader(
        "📁 Importă runde din fișier .txt",
        type=['txt'],
        help="Fiecare rundă pe o linie nouă, numere separate prin virgulă. Rundele pot avea număr diferit de numere."
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
                        numar_numere_per_combinatie,
                        numar_min,
                        numar_max
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

# Adăugare manuală
st.subheader("✍️ Adaugă runde manual")

runda_manuala = st.text_area(
    f"Introduceți rundele (orice număr de numere per rundă, separate prin virgulă)",
    height=150,
    placeholder=f"Exemplu:\n2, 6, 8, 55, 45\n12, 23, 34, 45, 16, 28, 39, 41\n5, 15, 25",
    help="Fiecare rundă pe o linie nouă - rundele pot avea numere diferite"
)

if st.button("➕ Adaugă rundele", type="primary"):
    if runda_manuala.strip():
        linii = runda_manuala.strip().split('\n')
        runde_adaugate = 0
        
        for linie in linii:
            if linie.strip():
                valid, rezultat = valideaza_runda(
                    linie,
                    numar_numere_per_combinatie,
                    numar_min,
                    numar_max
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

# Secțiunea 2: CÂTE COMBINAȚII SĂ GENEREZE
st.header("🎲 Generare Combinații")

numar_combinatii = st.number_input(
    "Câte combinații să genereze",
    min_value=1,
    max_value=100000,
    value=100,
    step=10
)

# Secțiunea 3: BUTON GENERARE
if st.button("🚀 GENEREAZĂ COMBINAȚII", type="primary", use_container_width=True):
    with st.spinner('Se generează combinațiile...'):
        combinatii = genereaza_combinatii(
            numar_combinatii,
            numar_numere_per_combinatie,
            numar_min,
            numar_max,
            st.session_state.runde_salvate
        )
        st.session_state.combinatii_generate = combinatii
        st.success(f"✅ {len(combinatii)} combinații generate cu succes!")

st.markdown("---")

# Secțiunea 4: PREVIEW REZULTATE
if st.session_state.combinatii_generate:
    st.header("📊 Rezultate Generate")
    
    # BUTON COPIAZĂ TOATE - SUS, VIZIBIL
    col1, col2, col3 = st.columns([1, 2, 1])
    with col2:
        toate_variantele = '\n'.join([
            formateaza_combinatie(i+1, comb) 
            for i, comb in enumerate(st.session_state.combinatii_generate)
        ])
        
        st.markdown("### 📋 Copiază toate variantele")
        st.code(toate_variantele, language=None)
        
        if st.button("📋 COPIAZĂ TOATE VARIANTELE", type="primary", use_container_width=True):
            st.info("✅ Selectează textul de mai sus și copiază-l (Ctrl+C / Cmd+C)")
    
    st.markdown("---")
    
    # Preview primele 10
    st.subheader(f"👀 Preview - Primele 10 din {len(st.session_state.combinatii_generate)} combinații")
    
    preview_data = []
    for i in range(min(10, len(st.session_state.combinatii_generate))):
        preview_data.append({
            'ID': i + 1,
            'Combinație': ' '.join(map(str, st.session_state.combinatii_generate[i]))
        })
    
    st.table(preview_data)
    
    # Container scrollable pentru TOATE
    with st.expander(f"📜 Vezi toate cele {len(st.session_state.combinatii_generate)} combinații (scrollable)"):
        toate_combinatii_text = []
        for i, comb in enumerate(st.session_state.combinatii_generate, 1):
            toate_combinatii_text.append(formateaza_combinatie(i, comb))
        
        st.text_area(
            "Toate combinațiile",
            value='\n'.join(toate_combinatii_text),
            height=400,
            disabled=True
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
