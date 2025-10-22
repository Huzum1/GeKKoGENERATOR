import streamlit as st
import random
import json
from datetime import datetime
from collections import Counter

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

# ============================
# STRATEGII DE GENERARE
# ============================

def strategie_echilibru_perfect(numar_numere, numar_min, numar_max):
    """Strategie 1: Distribuție echilibrată pe zone"""
    zone_size = (numar_max - numar_min + 1) // 3
    numere_per_zona = numar_numere // 3
    rest = numar_numere % 3
    
    zona1 = list(range(numar_min, numar_min + zone_size))
    zona2 = list(range(numar_min + zone_size, numar_min + 2*zone_size))
    zona3 = list(range(numar_min + 2*zone_size, numar_max + 1))
    
    combinatie = []
    combinatie.extend(random.sample(zona1, min(numere_per_zona + (1 if rest > 0 else 0), len(zona1))))
    combinatie.extend(random.sample(zona2, min(numere_per_zona + (1 if rest > 1 else 0), len(zona2))))
    combinatie.extend(random.sample(zona3, min(numere_per_zona, len(zona3))))
    
    # Completează dacă e nevoie
    while len(combinatie) < numar_numere:
        num = random.randint(numar_min, numar_max)
        if num not in combinatie:
            combinatie.append(num)
    
    return sorted(combinatie[:numar_numere])

def strategie_pare_impare(numar_numere, numar_min, numar_max):
    """Strategie 2: Echilibru 50/50 pare/impare"""
    pare = [x for x in range(numar_min, numar_max + 1) if x % 2 == 0]
    impare = [x for x in range(numar_min, numar_max + 1) if x % 2 != 0]
    
    numar_pare = numar_numere // 2
    numar_impare = numar_numere - numar_pare
    
    # Variație aleatorie: 50/50, 45/55 sau 55/45
    variatie = random.choice([-1, 0, 1])
    numar_pare += variatie
    numar_impare -= variatie
    
    combinatie = []
    if len(pare) >= numar_pare:
        combinatie.extend(random.sample(pare, numar_pare))
    if len(impare) >= numar_impare:
        combinatie.extend(random.sample(impare, numar_impare))
    
    return sorted(combinatie)

def strategie_frecventa_hot(numar_numere, numar_min, numar_max, runde_salvate):
    """Strategie 3: Favorizează numere frecvente din istoric"""
    if not runde_salvate:
        return sorted(random.sample(range(numar_min, numar_max + 1), numar_numere))
    
    # Calculează frecvența
    toate_numerele = [num for runda in runde_salvate for num in runda]
    frecventa = Counter(toate_numerele)
    
    # Top 30% cele mai frecvente
    numere_hot = [num for num, freq in frecventa.most_common(int((numar_max - numar_min + 1) * 0.3))]
    numere_hot = [n for n in numere_hot if numar_min <= n <= numar_max]
    
    # 60% din combinație = numere hot, 40% = random
    numar_hot = int(numar_numere * 0.6)
    numar_random = numar_numere - numar_hot
    
    combinatie = []
    if len(numere_hot) >= numar_hot:
        combinatie.extend(random.sample(numere_hot, numar_hot))
    
    numere_restante = [n for n in range(numar_min, numar_max + 1) if n not in combinatie]
    combinatie.extend(random.sample(numere_restante, min(numar_random, len(numere_restante))))
    
    return sorted(combinatie[:numar_numere])

def strategie_mixare_cold_hot(numar_numere, numar_min, numar_max, runde_salvate):
    """Strategie 4: Combină numere hot + cold + medii"""
    if not runde_salvate:
        return sorted(random.sample(range(numar_min, numar_max + 1), numar_numere))
    
    toate_numerele = [num for runda in runde_salvate for num in runda]
    frecventa = Counter(toate_numerele)
    
    # Toate numerele posibile
    toate_posibile = set(range(numar_min, numar_max + 1))
    
    # Categorii
    numere_hot = [num for num, freq in frecventa.most_common(20)]
    numere_cold = list(toate_posibile - set(frecventa.keys())) + \
                  [num for num, freq in frecventa.most_common()[-20:]]
    numere_medii = list(set(frecventa.keys()) - set(numere_hot) - set(numere_cold))
    
    # Distribuție: 33% hot, 33% cold, 33% medii
    numere_per_categorie = numar_numere // 3
    rest = numar_numere % 3
    
    combinatie = []
    combinatie.extend(random.sample(numere_hot, min(numere_per_categorie + (1 if rest > 0 else 0), len(numere_hot))))
    combinatie.extend(random.sample(numere_cold, min(numere_per_categorie + (1 if rest > 1 else 0), len(numere_cold))))
    if numere_medii:
        combinatie.extend(random.sample(numere_medii, min(numere_per_categorie, len(numere_medii))))
    
    # Completează dacă e nevoie
    while len(combinatie) < numar_numere:
        num = random.randint(numar_min, numar_max)
        if num not in combinatie:
            combinatie.append(num)
    
    return sorted(combinatie[:numar_numere])

def strategie_distanta_uniforma(numar_numere, numar_min, numar_max):
    """Strategie 5: Spacing echidistant între numere"""
    distanta_medie = (numar_max - numar_min) // numar_numere
    
    combinatie = []
    current = numar_min + random.randint(0, distanta_medie)
    
    for i in range(numar_numere):
        if current <= numar_max:
            combinatie.append(current)
            # Variație aleatorie în spacing: ±30%
            variatie = random.randint(int(distanta_medie * 0.7), int(distanta_medie * 1.3))
            current += variatie
        else:
            break
    
    # Completează dacă e nevoie
    while len(combinatie) < numar_numere:
        num = random.randint(numar_min, numar_max)
        if num not in combinatie:
            combinatie.append(num)
    
    return sorted(combinatie[:numar_numere])

def strategie_fibonacci(numar_numere, numar_min, numar_max):
    """Strategie 6: Bazat pe secvența Fibonacci"""
    # Generează secvența Fibonacci în intervalul dat
    fib = [1, 2]
    while fib[-1] < numar_max:
        fib.append(fib[-1] + fib[-2])
    
    fib_in_range = [f for f in fib if numar_min <= f <= numar_max]
    
    # 70% fibonacci, 30% random
    numar_fib = min(int(numar_numere * 0.7), len(fib_in_range))
    numar_random = numar_numere - numar_fib
    
    combinatie = []
    if fib_in_range:
        combinatie.extend(random.sample(fib_in_range, min(numar_fib, len(fib_in_range))))
    
    numere_restante = [n for n in range(numar_min, numar_max + 1) if n not in combinatie]
    combinatie.extend(random.sample(numere_restante, min(numar_random, len(numere_restante))))
    
    return sorted(combinatie[:numar_numere])

def strategie_evita_consecutive(numar_numere, numar_min, numar_max):
    """Strategie 7: Zero numere consecutive"""
    combinatie = []
    numere_disponibile = list(range(numar_min, numar_max + 1))
    
    while len(combinatie) < numar_numere and numere_disponibile:
        num = random.choice(numere_disponibile)
        combinatie.append(num)
        
        # Elimină numărul și vecinii săi
        numere_disponibile = [n for n in numere_disponibile 
                            if n != num and n != num-1 and n != num+1]
    
    # Dacă nu s-au putut genera suficiente, completează cu condiție relaxată
    while len(combinatie) < numar_numere:
        num = random.randint(numar_min, numar_max)
        if num not in combinatie:
            # Verifică doar că nu e direct consecutiv cu ultimul
            if not combinatie or abs(num - combinatie[-1]) > 1:
                combinatie.append(num)
    
    return sorted(combinatie[:numar_numere])

def strategie_multipli(numar_numere, numar_min, numar_max):
    """Strategie 8: Favorizează multipli de 3, 5, 7"""
    multipli_3 = [x for x in range(numar_min, numar_max + 1) if x % 3 == 0]
    multipli_5 = [x for x in range(numar_min, numar_max + 1) if x % 5 == 0]
    multipli_7 = [x for x in range(numar_min, numar_max + 1) if x % 7 == 0]
    
    # Distribuție: 30% mult3, 25% mult5, 20% mult7, 25% random
    num_m3 = int(numar_numere * 0.3)
    num_m5 = int(numar_numere * 0.25)
    num_m7 = int(numar_numere * 0.2)
    num_random = numar_numere - (num_m3 + num_m5 + num_m7)
    
    combinatie = []
    if multipli_3:
        combinatie.extend(random.sample(multipli_3, min(num_m3, len(multipli_3))))
    if multipli_5:
        candidati = [n for n in multipli_5 if n not in combinatie]
        combinatie.extend(random.sample(candidati, min(num_m5, len(candidati))))
    if multipli_7:
        candidati = [n for n in multipli_7 if n not in combinatie]
        combinatie.extend(random.sample(candidati, min(num_m7, len(candidati))))
    
    numere_restante = [n for n in range(numar_min, numar_max + 1) if n not in combinatie]
    combinatie.extend(random.sample(numere_restante, min(num_random, len(numere_restante))))
    
    return sorted(combinatie[:numar_numere])

def strategie_cuadrante_extreme(numar_numere, numar_min, numar_max):
    """Strategie 9: Accent pe primul și ultimul cuadrant"""
    interval = numar_max - numar_min + 1
    cuadrant1 = list(range(numar_min, numar_min + interval // 4))
    cuadrant4 = list(range(numar_max - interval // 4 + 1, numar_max + 1))
    mijloc = list(range(numar_min + interval // 4, numar_max - interval // 4 + 1))
    
    # 40% + 40% + 20%
    num_c1 = int(numar_numere * 0.4)
    num_c4 = int(numar_numere * 0.4)
    num_mijloc = numar_numere - num_c1 - num_c4
    
    combinatie = []
    combinatie.extend(random.sample(cuadrant1, min(num_c1, len(cuadrant1))))
    combinatie.extend(random.sample(cuadrant4, min(num_c4, len(cuadrant4))))
    combinatie.extend(random.sample(mijloc, min(num_mijloc, len(mijloc))))
    
    return sorted(combinatie[:numar_numere])

def strategie_oglinda(numar_numere, numar_min, numar_max):
    """Strategie 10: Perechi simetrice față de centru"""
    centru = (numar_min + numar_max) / 2
    
    combinatie = []
    numere_sub_centru = [n for n in range(numar_min, int(centru) + 1)]
    
    # Generează jumătate numere sub centru
    numar_perechi = numar_numere // 2
    numere_selectate = random.sample(numere_sub_centru, min(numar_perechi, len(numere_sub_centru)))
    
    for num in numere_selectate:
        combinatie.append(num)
        # Oglinda: numar_max + numar_min - num
        oglinda = numar_max + numar_min - num
        if oglinda != num and numar_min <= oglinda <= numar_max:
            combinatie.append(oglinda)
    
    # Completează dacă e nevoie
    while len(combinatie) < numar_numere:
        num = random.randint(numar_min, numar_max)
        if num not in combinatie:
            combinatie.append(num)
    
    return sorted(combinatie[:numar_numere])

# Dicționar cu toate strategiile
STRATEGII = {
    "🎯 Random Standard (Original)": {
        "func": None,  # Va folosi logica originală
        "descriere": "Generare aleatoare pură - fără restricții"
    },
    "⚖️ Echilibru Perfect (Zone 33-33-33)": {
        "func": strategie_echilibru_perfect,
        "descriere": "Distribuție echilibrată pe 3 zone egale"
    },
    "🔢 Pare/Impare 50/50": {
        "func": strategie_pare_impare,
        "descriere": "Echilibru între numere pare și impare"
    },
    "🔥 Frecvență HOT": {
        "func": strategie_frecventa_hot,
        "descriere": "Favorizează numerele frecvente din istoric (necesită runde salvate)"
    },
    "❄️🔥 Mixare COLD+HOT": {
        "func": strategie_mixare_cold_hot,
        "descriere": "Combină numere fierbinți, reci și medii (necesită runde salvate)"
    },
    "📏 Distanță Uniformă": {
        "func": strategie_distanta_uniforma,
        "descriere": "Spacing echidistant între numere"
    },
    "🌀 Fibonacci Adaptat": {
        "func": strategie_fibonacci,
        "descriere": "Bazat pe secvența Fibonacci în intervalul dat"
    },
    "🚫➡️ Evită Consecutive": {
        "func": strategie_evita_consecutive,
        "descriere": "Zero numere consecutive (ex: 5,6)"
    },
    "🔢 Multipli 3-5-7": {
        "func": strategie_multipli,
        "descriere": "Favorizează multipli de 3, 5 și 7"
    },
    "📐 Cuadrante Extreme": {
        "func": strategie_cuadrante_extreme,
        "descriere": "Accent pe primul și ultimul cuadrant (40%-40%-20%)"
    },
    "🪞 Oglindă Matematică": {
        "func": strategie_oglinda,
        "descriere": "Perechi simetrice față de centrul intervalului"
    }
}

# ============================
# FUNCȚII HELPER ORIGINALE
# ============================

def valideaza_runda(runda_text, numar_numere_asteptat, numar_min, numar_max):
    """Validează o rundă introdusă de utilizator"""
    try:
        numere = [int(x.strip()) for x in runda_text.strip().split(',')]
        
        if len(numere) < 1:
            return False, "Eroare: Runda trebuie să conțină cel puțin un număr"
        
        return True, numere
    except ValueError:
        return False, "Eroare: Format invalid - folosește virgulă între numere (ex: 2, 6, 8, 55, 45, 37, 27)"

def genereaza_combinatii(numar_combinatii, numar_numere, numar_min, numar_max, strategie_selectata, runde_existente=[]):
    """Generează combinații folosind strategia selectată"""
    combinatii = []
    
    strategie_info = STRATEGII[strategie_selectata]
    strategie_func = strategie_info["func"]
    
    for i in range(numar_combinatii):
        if strategie_func is None:
            # Strategie originală (random standard)
            combinatie = sorted(random.sample(range(numar_min, numar_max + 1), numar_numere))
        else:
            # Aplică strategia selectată
            if strategie_selectata in ["🔥 Frecvență HOT", "❄️🔥 Mixare COLD+HOT"]:
                combinatie = strategie_func(numar_numere, numar_min, numar_max, runde_existente)
            else:
                combinatie = strategie_func(numar_numere, numar_min, numar_max)
        
        combinatii.append(combinatie)
    
    return combinatii

def formateaza_combinatie(id_combinatie, combinatie):
    """Formatează o combinație în formatul ID, numere"""
    numere_str = ' '.join(map(str, combinatie))
    return f"{id_combinatie}, {numere_str}"

# ============================
# INTERFAȚĂ STREAMLIT
# ============================

# HEADER
st.title("🐲 GENERATOR DE BANI ♣️ - GeKKo 🐲")
st.markdown("---")

# Configurare INIȚIALĂ
if 'numar_min' not in st.session_state:
    st.session_state.numar_min = 1
if 'numar_max' not in st.session_state:
    st.session_state.numar_max = 49
if 'numar_numere_per_combinatie' not in st.session_state:
    st.session_state.numar_numere_per_combinatie = 7
if 'strategie_selectata' not in st.session_state:
    st.session_state.strategie_selectata = "🎯 Random Standard (Original)"

# ============================
# SECȚIUNE STRATEGII (NOU)
# ============================
st.header("🎲 Strategii de Generare")

col_strat1, col_strat2 = st.columns([2, 1])

with col_strat1:
    strategie_aleasa = st.selectbox(
        "Selectează strategia de generare:",
        options=list(STRATEGII.keys()),
        index=list(STRATEGII.keys()).index(st.session_state.strategie_selectata),
        help="Fiecare strategie folosește un algoritm diferit pentru generarea numerelor"
    )
    st.session_state.strategie_selectata = strategie_aleasa
    
    # Afișare descriere strategie
    st.info(f"ℹ️ **{STRATEGII[strategie_aleasa]['descriere']}**")

with col_strat2:
    # Preset rapid pentru Keno Cehia
    if st.button("🇨🇿 Preset Keno Cehia", type="secondary", use_container_width=True):
        st.session_state.numar_min = 1
        st.session_state.numar_max = 66
        st.session_state.numar_numere_per_combinatie = 12
        st.success("✅ Configurat pentru Keno Cehia 12/66!")
        st.rerun()

st.markdown("---")

# ============================
# SECȚIUNEA 1: ISTORIC RUNDE
# ============================
st.header("📋 Istoric Runde")

col1, col2 = st.columns([2, 1])

with col1:
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

# Adăugare manuală
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

# ============================
# SECȚIUNEA CONFIGURARE
# ============================
st.markdown("### ⚙️ Configurare")

numar_min = 1
st.session_state.numar_min = numar_min

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

# ============================
# SECȚIUNEA GENERARE
# ============================
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
    st.markdown("<br>", unsafe_allow_html=True)
    if st.button("🚀 GENEREAZĂ", type="primary", use_container_width=True):
        with st.spinner(f'Generare folosind strategia: {strategie_aleasa}...'):
            combinatii = genereaza_combinatii(
                numar_combinatii,
                numar_numere_per_combinatie,
                numar_min,
                numar_max,
                strategie_aleasa,
                st.session_state.runde_salvate
            )
            st.session_state.combinatii_generate = combinatii
            st.success(f"✅ {len(combinatii)} combinații generate cu strategia: **{strategie_aleasa}**!")

st.markdown("---")

# ============================
# SECȚIUNEA REZULTATE
# ============================
if st.session_state.combinatii_generate:
    st.header("📊 Rezultate Generate")
    
    # Pregătim textul
    toate_variantele = '\n'.join([
        formateaza_combinatie(i+1, comb) 
        for i, comb in enumerate(st.session_state.combinatii_generate)
    ])
    
    with st.expander("📋 Vezi textul pentru copiere manuală (dacă e nevoie)"):
        st.code(toate_variantele, language=None)
    
    st.markdown("---")
    
    # Preview
    st.subheader(f"📜 Preview combinații ({len(st.session_state.combinatii_generate)} total)")
    
    toate_combinatii_text = []
    for i, comb in enumerate(st.session_state.combinatii_generate, 1):
        toate_combinatii_text.append(formateaza_combinatie(i, comb))
    
    st.text_area(
        "Primele 10 vizibile, scroll pentru restul:",
        value='\n'.join(toate_combinatii_text),
        height=300,
        disabled=True,
        key="preview_toate_combinatiile"
    )
    
    st.markdown("---")
    
    # ============================
    # SECȚIUNEA EXPORT
    # ============================
    st.header("💾 Export")
    
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
    "🐲 GENERATOR DE BANI ♣️ - GeKKo 🐲 | Noroc la joc!<br>"
    "<small>Versiunea cu 10 Strategii Avansate de Generare</small>"
    "</div>",
    unsafe_allow_html=True
)
