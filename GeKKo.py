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
if 'strategii_selectate' not in st.session_state:
    st.session_state.strategii_selectate = []

# ============================
# STRATEGII DE GENERARE - OPTIMIZATE PENTRU 4/4
# ============================

def strategie_random_standard(numar_numere, numar_min, numar_max, runde_existente=[]):
    """Strategie 0: Random standard (original)"""
    return sorted(random.sample(range(numar_min, numar_max + 1), numar_numere))

def strategie_echilibru_perfect(numar_numere, numar_min, numar_max, runde_existente=[]):
    """Strategie 1: Distribuție echilibrată pe zone
    Pentru 4 numere: 1-1-2 sau 2-1-1 distribuit pe 3 zone"""
    interval = numar_max - numar_min + 1
    zone_size = interval // 3
    
    zona1 = list(range(numar_min, numar_min + zone_size))
    zona2 = list(range(numar_min + zone_size, numar_min + 2*zone_size))
    zona3 = list(range(numar_min + 2*zone_size, numar_max + 1))
    
    if numar_numere == 4:
        # Pentru 4 numere: variază între 1-1-2, 1-2-1, 2-1-1
        distributii = [(1,1,2), (1,2,1), (2,1,1)]
        dist = random.choice(distributii)
    else:
        # Pentru alte cantități
        numere_per_zona = numar_numere // 3
        rest = numar_numere % 3
        dist = (numere_per_zona + (1 if rest > 0 else 0),
                numere_per_zona + (1 if rest > 1 else 0),
                numere_per_zona)
    
    combinatie = []
    combinatie.extend(random.sample(zona1, min(dist[0], len(zona1))))
    combinatie.extend(random.sample(zona2, min(dist[1], len(zona2))))
    combinatie.extend(random.sample(zona3, min(dist[2], len(zona3))))
    
    while len(combinatie) < numar_numere:
        num = random.randint(numar_min, numar_max)
        if num not in combinatie:
            combinatie.append(num)
    
    return sorted(combinatie[:numar_numere])

def strategie_pare_impare(numar_numere, numar_min, numar_max, runde_existente=[]):
    """Strategie 2: Echilibru pare/impare
    Pentru 4 numere: 2 pare + 2 impare (sau 3+1, 1+3)"""
    pare = [x for x in range(numar_min, numar_max + 1) if x % 2 == 0]
    impare = [x for x in range(numar_min, numar_max + 1) if x % 2 != 0]
    
    if numar_numere == 4:
        # Variație: 2-2, 3-1, 1-3
        distributii = [(2,2), (3,1), (1,3)]
        dist = random.choice(distributii)
        numar_pare, numar_impare = dist
    else:
        numar_pare = numar_numere // 2
        numar_impare = numar_numere - numar_pare
        variatie = random.choice([-1, 0, 1])
        numar_pare += variatie
        numar_impare -= variatie
    
    combinatie = []
    if len(pare) >= numar_pare:
        combinatie.extend(random.sample(pare, numar_pare))
    if len(impare) >= numar_impare:
        combinatie.extend(random.sample(impare, numar_impare))
    
    return sorted(combinatie)

def strategie_frecventa_hot(numar_numere, numar_min, numar_max, runde_existente=[]):
    """Strategie 3: Favorizează numere frecvente
    Pentru 4 numere: 2-3 HOT + 1-2 random"""
    if not runde_existente:
        return sorted(random.sample(range(numar_min, numar_max + 1), numar_numere))
    
    toate_numerele = [num for runda in runde_existente for num in runda]
    frecventa = Counter(toate_numerele)
    
    numere_hot = [num for num, freq in frecventa.most_common(23)]
    numere_hot = [n for n in numere_hot if numar_min <= n <= numar_max]
    
    if numar_numere == 4:
        # 2-3 din HOT, restul random
        numar_hot = random.choice([2, 3])
    else:
        numar_hot = int(numar_numere * 0.6)
    
    numar_random = numar_numere - numar_hot
    
    combinatie = []
    if len(numere_hot) >= numar_hot:
        combinatie.extend(random.sample(numere_hot, numar_hot))
    
    numere_restante = [n for n in range(numar_min, numar_max + 1) if n not in combinatie]
    combinatie.extend(random.sample(numere_restante, min(numar_random, len(numere_restante))))
    
    return sorted(combinatie[:numar_numere])

def strategie_top23_focus(numar_numere, numar_min, numar_max, runde_existente=[]):
    """Strategie 4: 3 din TOP 23 + 1 din rest
    Pentru 4 numere: 2-3 din TOP 23 + 1-2 din rest"""
    if not runde_existente:
        return sorted(random.sample(range(numar_min, numar_max + 1), numar_numere))
    
    toate_numerele = [num for runda in runde_existente for num in runda]
    frecventa = Counter(toate_numerele)
    
    top23 = [num for num, freq in frecventa.most_common(23)]
    top23 = [n for n in top23 if numar_min <= n <= numar_max]
    
    restul = [n for n in range(numar_min, numar_max + 1) if n not in top23]
    
    if numar_numere == 4:
        # Variație: 2+2 sau 3+1
        numar_top = random.choice([2, 3])
    else:
        numar_top = min(3, numar_numere - 1)
    
    numar_rest = numar_numere - numar_top
    
    combinatie = []
    if len(top23) >= numar_top:
        combinatie.extend(random.sample(top23, numar_top))
    if len(restul) >= numar_rest:
        combinatie.extend(random.sample(restul, numar_rest))
    
    return sorted(combinatie)

def strategie_mixare_cold_hot(numar_numere, numar_min, numar_max, runde_existente=[]):
    """Strategie 5: Mix HOT + COLD + WARM
    Pentru 4 numere: 1 HOT + 1 COLD + 2 WARM"""
    if not runde_existente:
        return sorted(random.sample(range(numar_min, numar_max + 1), numar_numere))
    
    toate_numerele = [num for runda in runde_existente for num in runda]
    frecventa = Counter(toate_numerele)
    toate_posibile = set(range(numar_min, numar_max + 1))
    
    numere_hot = [num for num, freq in frecventa.most_common(20)]
    numere_cold = list(toate_posibile - set(frecventa.keys())) + \
                  [num for num, freq in frecventa.most_common()[-20:]]
    numere_warm = list(set(frecventa.keys()) - set(numere_hot) - set(numere_cold))
    
    if numar_numere == 4:
        # 1 HOT + 1 COLD + 2 WARM
        combinatie = []
        if numere_hot:
            combinatie.append(random.choice(numere_hot))
        if numere_cold:
            combinatie.append(random.choice(numere_cold))
        if numere_warm and len(numere_warm) >= 2:
            combinatie.extend(random.sample(numere_warm, 2))
    else:
        numere_per_categorie = numar_numere // 3
        combinatie = []
        if numere_hot:
            combinatie.extend(random.sample(numere_hot, min(numere_per_categorie, len(numere_hot))))
        if numere_cold:
            combinatie.extend(random.sample(numere_cold, min(numere_per_categorie, len(numere_cold))))
        if numere_warm:
            combinatie.extend(random.sample(numere_warm, min(numere_per_categorie, len(numere_warm))))
    
    while len(combinatie) < numar_numere:
        num = random.randint(numar_min, numar_max)
        if num not in combinatie:
            combinatie.append(num)
    
    return sorted(combinatie[:numar_numere])

def strategie_distanta_uniforma(numar_numere, numar_min, numar_max, runde_existente=[]):
    """Strategie 6: Spacing echidistant
    Pentru 4 numere: distanță medie ~15-20 unități"""
    if numar_numere == 4:
        # Spacing țintă: 15-20 unități pentru Keno 66
        distanta_medie = (numar_max - numar_min) // 5  # ~13 pentru 66
    else:
        distanta_medie = (numar_max - numar_min) // numar_numere
    
    combinatie = []
    current = numar_min + random.randint(0, distanta_medie)
    
    for i in range(numar_numere):
        if current <= numar_max:
            combinatie.append(current)
            variatie = random.randint(int(distanta_medie * 0.7), int(distanta_medie * 1.3))
            current += variatie
        else:
            break
    
    while len(combinatie) < numar_numere:
        num = random.randint(numar_min, numar_max)
        if num not in combinatie:
            combinatie.append(num)
    
    return sorted(combinatie[:numar_numere])

def strategie_evita_consecutive(numar_numere, numar_min, numar_max, runde_existente=[]):
    """Strategie 7: Zero numere consecutive
    Optim pentru 4 numere"""
    combinatie = []
    numere_disponibile = list(range(numar_min, numar_max + 1))
    
    while len(combinatie) < numar_numere and numere_disponibile:
        num = random.choice(numere_disponibile)
        combinatie.append(num)
        numere_disponibile = [n for n in numere_disponibile 
                            if n != num and n != num-1 and n != num+1]
    
    while len(combinatie) < numar_numere:
        num = random.randint(numar_min, numar_max)
        if num not in combinatie:
            if not combinatie or all(abs(num - c) > 1 for c in combinatie):
                combinatie.append(num)
    
    return sorted(combinatie[:numar_numere])

def strategie_multipli(numar_numere, numar_min, numar_max, runde_existente=[]):
    """Strategie 8: Multipli de 3, 5, 7
    Pentru 4 numere: 1-2 multipli + 2-3 random"""
    multipli_3 = [x for x in range(numar_min, numar_max + 1) if x % 3 == 0]
    multipli_5 = [x for x in range(numar_min, numar_max + 1) if x % 5 == 0]
    multipli_7 = [x for x in range(numar_min, numar_max + 1) if x % 7 == 0]
    
    if numar_numere == 4:
        # 1-2 multipli + restul random
        num_multipli = random.choice([1, 2])
    else:
        num_multipli = int(numar_numere * 0.4)
    
    num_random = numar_numere - num_multipli
    
    # Combină toți multiplii
    toti_multiplii = list(set(multipli_3 + multipli_5 + multipli_7))
    
    combinatie = []
    if toti_multiplii and len(toti_multiplii) >= num_multipli:
        combinatie.extend(random.sample(toti_multiplii, num_multipli))
    
    numere_restante = [n for n in range(numar_min, numar_max + 1) if n not in combinatie]
    combinatie.extend(random.sample(numere_restante, min(num_random, len(numere_restante))))
    
    return sorted(combinatie[:numar_numere])

def strategie_cuadrante_extreme(numar_numere, numar_min, numar_max, runde_existente=[]):
    """Strategie 9: Accent pe capete
    Pentru 4 numere: 2 din start + 2 din final"""
    interval = numar_max - numar_min + 1
    
    if numar_numere == 4:
        # 2 + 2 de la capete
        cuadrant1 = list(range(numar_min, numar_min + interval // 4))
        cuadrant4 = list(range(numar_max - interval // 4 + 1, numar_max + 1))
        
        combinatie = []
        combinatie.extend(random.sample(cuadrant1, min(2, len(cuadrant1))))
        combinatie.extend(random.sample(cuadrant4, min(2, len(cuadrant4))))
    else:
        cuadrant1 = list(range(numar_min, numar_min + interval // 4))
        cuadrant4 = list(range(numar_max - interval // 4 + 1, numar_max + 1))
        mijloc = list(range(numar_min + interval // 4, numar_max - interval // 4 + 1))
        
        num_c1 = int(numar_numere * 0.4)
        num_c4 = int(numar_numere * 0.4)
        num_mijloc = numar_numere - num_c1 - num_c4
        
        combinatie = []
        combinatie.extend(random.sample(cuadrant1, min(num_c1, len(cuadrant1))))
        combinatie.extend(random.sample(cuadrant4, min(num_c4, len(cuadrant4))))
        combinatie.extend(random.sample(mijloc, min(num_mijloc, len(mijloc))))
    
    return sorted(combinatie[:numar_numere])

def strategie_oglinda(numar_numere, numar_min, numar_max, runde_existente=[]):
    """Strategie 10: Perechi simetrice
    Pentru 4 numere: 2 perechi oglindă"""
    centru = (numar_min + numar_max) / 2
    
    if numar_numere == 4:
        # 2 perechi simetrice
        numere_sub_centru = [n for n in range(numar_min, int(centru) + 1)]
        numere_selectate = random.sample(numere_sub_centru, 2)
        
        combinatie = []
        for num in numere_selectate:
            combinatie.append(num)
            oglinda = numar_max + numar_min - num
            if oglinda != num and numar_min <= oglinda <= numar_max:
                combinatie.append(oglinda)
    else:
        numere_sub_centru = [n for n in range(numar_min, int(centru) + 1)]
        numar_perechi = numar_numere // 2
        numere_selectate = random.sample(numere_sub_centru, min(numar_perechi, len(numere_sub_centru)))
        
        combinatie = []
        for num in numere_selectate:
            combinatie.append(num)
            oglinda = numar_max + numar_min - num
            if oglinda != num and numar_min <= oglinda <= numar_max:
                combinatie.append(oglinda)
    
    while len(combinatie) < numar_numere:
        num = random.randint(numar_min, numar_max)
        if num not in combinatie:
            combinatie.append(num)
    
    return sorted(combinatie[:numar_numere])

def strategie_fibonacci(numar_numere, numar_min, numar_max, runde_existente=[]):
    """Strategie 11: Fibonacci adaptat
    Pentru 4 numere: 2-3 Fibonacci + 1-2 random"""
    fib = [1, 2]
    while fib[-1] < numar_max:
        fib.append(fib[-1] + fib[-2])
    
    fib_in_range = [f for f in fib if numar_min <= f <= numar_max]
    
    if numar_numere == 4:
        numar_fib = random.choice([2, 3])
    else:
        numar_fib = min(int(numar_numere * 0.6), len(fib_in_range))
    
    numar_random = numar_numere - numar_fib
    
    combinatie = []
    if fib_in_range:
        combinatie.extend(random.sample(fib_in_range, min(numar_fib, len(fib_in_range))))
    
    numere_restante = [n for n in range(numar_min, numar_max + 1) if n not in combinatie]
    combinatie.extend(random.sample(numere_restante, min(numar_random, len(numere_restante))))
    
    return sorted(combinatie[:numar_numere])

def strategie_temperatura_graduala(numar_numere, numar_min, numar_max, runde_existente=[]):
    """Strategie 12: 3 HOT + 6 WARM + 3 COLD
    Pentru 4 numere: 1 HOT + 2 WARM + 1 COLD"""
    if not runde_existente:
        return sorted(random.sample(range(numar_min, numar_max + 1), numar_numere))
    
    toate_numerele = [num for runda in runde_existente for num in runda]
    frecventa = Counter(toate_numerele)
    toate_posibile = list(range(numar_min, numar_max + 1))
    
    # Sortare după frecvență
    sorted_freq = sorted([(num, freq) for num, freq in frecventa.items()], 
                        key=lambda x: x[1], reverse=True)
    
    total = len(toate_posibile)
    hot_threshold = total // 5  # Top 20%
    cold_threshold = total - total // 5  # Bottom 20%
    
    hot = [num for num, freq in sorted_freq[:hot_threshold]]
    cold_candidates = set(toate_posibile) - set(frecventa.keys())
    cold = list(cold_candidates) + [num for num, freq in sorted_freq[cold_threshold:]]
    warm = [num for num in toate_posibile if num not in hot and num not in cold]
    
    if numar_numere == 4:
        combinatie = []
        if hot:
            combinatie.append(random.choice(hot))
        if warm and len(warm) >= 2:
            combinatie.extend(random.sample(warm, 2))
        if cold:
            combinatie.append(random.choice(cold))
    else:
        num_hot = max(1, int(numar_numere * 0.25))
        num_cold = max(1, int(numar_numere * 0.25))
        num_warm = numar_numere - num_hot - num_cold
        
        combinatie = []
        if hot:
            combinatie.extend(random.sample(hot, min(num_hot, len(hot))))
        if warm:
            combinatie.extend(random.sample(warm, min(num_warm, len(warm))))
        if cold:
            combinatie.extend(random.sample(cold, min(num_cold, len(cold))))
    
    while len(combinatie) < numar_numere:
        num = random.randint(numar_min, numar_max)
        if num not in combinatie:
            combinatie.append(num)
    
    return sorted(combinatie[:numar_numere])

def strategie_salturi_prime(numar_numere, numar_min, numar_max, runde_existente=[]):
    """Strategie 13: Numere prime
    Pentru 4 numere: 2 prime + 2 non-prime"""
    def este_prim(n):
        if n < 2:
            return False
        for i in range(2, int(n**0.5) + 1):
            if n % i == 0:
                return False
        return True
    
    prime = [n for n in range(numar_min, numar_max + 1) if este_prim(n)]
    non_prime = [n for n in range(numar_min, numar_max + 1) if not este_prim(n)]
    
    if numar_numere == 4:
        num_prime = 2
        num_non_prime = 2
    else:
        num_prime = numar_numere // 2
        num_non_prime = numar_numere - num_prime
    
    combinatie = []
    if prime and len(prime) >= num_prime:
        combinatie.extend(random.sample(prime, num_prime))
    if non_prime and len(non_prime) >= num_non_prime:
        combinatie.extend(random.sample(non_prime, num_non_prime))
    
    return sorted(combinatie)

def strategie_suma_controlata(numar_numere, numar_min, numar_max, runde_existente=[]):
    """Strategie 14: Sumă controlată
    Pentru 4 numere: sumă între 130-140 (media ~134 pentru 1-66)"""
    if numar_numere == 4:
        suma_min, suma_max = 130, 140
    else:
        # Media teoretică
        media_per_numar = (numar_min + numar_max) / 2
        suma_medie = media_per_numar * numar_numere
        suma_min = suma_medie * 0.85
        suma_max = suma_medie * 1.15
    
    max_incercari = 1000
    for _ in range(max_incercari):
        combinatie = sorted(random.sample(range(numar_min, numar_max + 1), numar_numere))
        suma = sum(combinatie)
        if suma_min <= suma <= suma_max:
            return combinatie
    
    # Fallback: returnează orice combinație
    return sorted(random.sample(range(numar_min, numar_max + 1), numar_numere))

def strategie_atractie_magnetica(numar_numere, numar_min, numar_max, runde_existente=[]):
    """Strategie 15: Distanță minimă 3 între numere
    Pentru 4 numere: |N[i] - N[i+1]| ≥ 3"""
    combinatie = []
    numere_disponibile = list(range(numar_min, numar_max + 1))
    
    while len(combinatie) < numar_numere and numere_disponibile:
        if not combinatie:
            num = random.choice(numere_disponibile)
        else:
            # Filtrează numerele prea apropiate de ultimul adăugat
            candidati = [n for n in numere_disponibile if abs(n - combinatie[-1]) >= 3]
            if not candidati:
                break
            num = random.choice(candidati)
        
        combinatie.append(num)
        numere_disponibile.remove(num)
    
    # Completează dacă e nevoie (relaxare condiție)
    while len(combinatie) < numar_numere:
        num = random.randint(numar_min, numar_max)
        if num not in combinatie:
            combinatie.append(num)
    
    return sorted(combinatie[:numar_numere])

def strategie_percentile(numar_numere, numar_min, numar_max, runde_existente=[]):
    """Strategie 16: Percentile 25-50-25
    Pentru 4 numere: 1 din 0-25%, 2 din 25-75%, 1 din 75-100%"""
    interval = numar_max - numar_min + 1
    
    p25 = numar_min + interval // 4
    p75 = numar_min + 3 * interval // 4
    
    zona1 = list(range(numar_min, p25))
    zona2 = list(range(p25, p75))
    zona3 = list(range(p75, numar_max + 1))
    
    if numar_numere == 4:
        combinatie = []
        if zona1:
            combinatie.append(random.choice(zona1))
        if zona2 and len(zona2) >= 2:
            combinatie.extend(random.sample(zona2, 2))
        if zona3:
            combinatie.append(random.choice(zona3))
    else:
        num_z1 = int(numar_numere * 0.25)
        num_z3 = int(numar_numere * 0.25)
        num_z2 = numar_numere - num_z1 - num_z3
        
        combinatie = []
        if zona1:
            combinatie.extend(random.sample(zona1, min(num_z1, len(zona1))))
        if zona2:
            combinatie.extend(random.sample(zona2, min(num_z2, len(zona2))))
        if zona3:
            combinatie.extend(random.sample(zona3, min(num_z3, len(zona3))))
    
    while len(combinatie) < numar_numere:
        num = random.randint(numar_min, numar_max)
        if num not in combinatie:
            combinatie.append(num)
    
    return sorted(combinatie[:numar_numere])

def strategie_perechi_incrucisate(numar_numere, numar_min, numar_max, runde_existente=[]):
    """Strategie 17: Perechi (mic, mare) cu diferență 30-40
    Pentru 4 numere: 2 perechi încrucișate"""
    if numar_numere == 4:
        # 2 perechi
        numar_perechi = 2
    else:
        numar_perechi = numar_numere // 2
    
    combinatie = []
    numere_mici = list(range(numar_min, numar_min + (numar_max - numar_min) // 3))
    
    for _ in range(numar_perechi):
        if numere_mici:
            mic = random.choice([n for n in numere_mici if n not in combinatie])
            diferenta = random.randint(30, 40)
            mare = min(mic + diferenta, numar_max)
            
            if mare not in combinatie:
                combinatie.append(mic)
                combinatie.append(mare)
    
    while len(combinatie) < numar_numere:
        num = random.randint(numar_min, numar_max)
        if num not in combinatie:
            combinatie.append(num)
    
    return sorted(combinatie[:numar_numere])

def strategie_curcubeu(numar_numere, numar_min, numar_max, runde_existente=[]):
    """Strategie 18: Exact 2 numere din fiecare decadă
    Pentru 4 numere: 1 număr din 4 decade diferite"""
    decade = []
    current = numar_min
    decade_size = 10
    
    while current <= numar_max:
        decada = list(range(current, min(current + decade_size, numar_max + 1)))
        if decada:
            decade.append(decada)
        current += decade_size
    
    if numar_numere == 4:
        # Ia 1 număr din 4 decade diferite
        decade_selectate = random.sample(decade, min(4, len(decade)))
        combinatie = [random.choice(dec) for dec in decade_selectate]
    else:
        numere_per_decada = max(1, numar_numere // len(decade))
        combinatie = []
        
        for dec in decade:
            if len(combinatie) < numar_numere:
                combinatie.extend(random.sample(dec, min(numere_per_decada, len(dec))))
    
    while len(combinatie) < numar_numere:
        num = random.randint(numar_min, numar_max)
        if num not in combinatie:
            combinatie.append(num)
    
    return sorted(combinatie[:numar_numere])

def strategie_rotatie_ciclica(numar_numere, numar_min, numar_max, runde_existente=[]):
    """Strategie 19: Rotație pe 6 zone
    Pentru 4 numere: 1-2 numere din 2-4 zone"""
    interval = numar_max - numar_min + 1
    zone_size = interval // 6
    
    zone = []
    for i in range(6):
        start = numar_min + i * zone_size
        end = numar_min + (i + 1) * zone_size if i < 5 else numar_max + 1
        zona = list(range(start, end))
        if zona:
            zone.append(zona)
    
    if numar_numere == 4:
        # Alege 2-4 zone, ia 1-2 numere din fiecare
        numar_zone = random.choice([2, 3, 4])
        zone_selectate = random.sample(zone, min(numar_zone, len(zone)))
        
        combinatie = []
        numere_per_zona = numar_numere // numar_zone
        rest = numar_numere % numar_zone
        
        for idx, zona in enumerate(zone_selectate):
            nr = numere_per_zona + (1 if idx < rest else 0)
            combinatie.extend(random.sample(zona, min(nr, len(zona))))
    else:
        combinatie = []
        numere_per_zona = max(1, numar_numere // len(zone))
        
        for zona in zone:
            if len(combinatie) < numar_numere:
                combinatie.extend(random.sample(zona, min(numere_per_zona, len(zona))))
    
    while len(combinatie) < numar_numere:
        num = random.randint(numar_min, numar_max)
        if num not in combinatie:
            combinatie.append(num)
    
    return sorted(combinatie[:numar_numere])

def strategie_ai_hybrid(numar_numere, numar_min, numar_max, runde_existente=[]):
    """Strategie 20: AI HYBRID - Combină top 5 strategii
    Pentru 4 numere: Rotație între cele mai bune strategii"""
    strategii_top = [
        strategie_echilibru_perfect,
        strategie_frecventa_hot,
        strategie_distanta_uniforma,
        strategie_top23_focus,
        strategie_suma_controlata
    ]
    
    # Alege aleator una din top 5
    strategie_aleasa = random.choice(strategii_top)
    return strategie_aleasa(numar_numere, numar_min, numar_max, runde_existente)

# Dicționar cu toate strategiile
STRATEGII = {
    "🎯 Random Standard": {
        "func": strategie_random_standard,
        "descriere": "Generare aleatoare pură - fără restricții",
        "optim_4": "✅ Universal"
    },
    "⚖️ Echilibru Perfect": {
        "func": strategie_echilibru_perfect,
        "descriere": "Zone 1-1-2 sau 2-1-1",
        "optim_4": "🔥 Recomandat 4/4"
    },
    "🔢 Pare/Impare 50/50": {
        "func": strategie_pare_impare,
        "descriere": "2 pare + 2 impare (sau 3+1)",
        "optim_4": "🔥 Recomandat 4/4"
    },
    "🔥 Frecvență HOT": {
        "func": strategie_frecventa_hot,
        "descriere": "2-3 HOT + 1-2 random (necesită istoric)",
        "optim_4": "🔥 Recomandat 4/4"
    },
    "🎯 TOP 23 Focus": {
        "func": strategie_top23_focus,
        "descriere": "2-3 din TOP 23 + rest (necesită istoric)",
        "optim_4": "🔥 Recomandat 4/4"
    },
    "❄️🔥 Mix COLD+HOT": {
        "func": strategie_mixare_cold_hot,
        "descriere": "1 HOT + 2 WARM + 1 COLD (necesită istoric)",
        "optim_4": "✅ Bun pentru 4/4"
    },
    "📏 Distanță Uniformă": {
        "func": strategie_distanta_uniforma,
        "descriere": "Spacing ~15-20 unități",
        "optim_4": "✅ Bun pentru 4/4"
    },
    "🚫➡️ Evită Consecutive": {
        "func": strategie_evita_consecutive,
        "descriere": "Zero numere consecutive (5,6)",
        "optim_4": "✅ Bun pentru 4/4"
    },
    "🔢 Multipli 3-5-7": {
        "func": strategie_multipli,
        "descriere": "1-2 multipli + 2-3 random",
        "optim_4": "✅ Bun pentru 4/4"
    },
    "📐 Cuadrante Extreme": {
        "func": strategie_cuadrante_extreme,
        "descriere": "2 start + 2 final",
        "optim_4": "🔥 Recomandat 4/4"
    },
    "🪞 Oglindă Matematică": {
        "func": strategie_oglinda,
        "descriere": "2 perechi simetrice",
        "optim_4": "✅ Bun pentru 4/4"
    },
    "🌀 Fibonacci Adaptat": {
        "func": strategie_fibonacci,
        "descriere": "2-3 Fibonacci + 1-2 random",
        "optim_4": "✅ Bun pentru 4/4"
    },
    "🌡️ Temperatură Graduală": {
        "func": strategie_temperatura_graduala,
        "descriere": "1 HOT + 2 WARM + 1 COLD (necesită istoric)",
        "optim_4": "✅ Bun pentru 4/4"
    },
    "⚡ Salturi Prime": {
        "func": strategie_salturi_prime,
        "descriere": "2 prime + 2 non-prime",
        "optim_4": "✅ Bun pentru 4/4"
    },
    "🎲 Sumă Controlată": {
        "func": strategie_suma_controlata,
        "descriere": "Sumă 130-140 (optim 4/66)",
        "optim_4": "🔥 Recomandat 4/4"
    },
    "🧲 Atracție Magnetică": {
        "func": strategie_atractie_magnetica,
        "descriere": "Distanță ≥3 între numere",
        "optim_4": "✅ Bun pentru 4/4"
    },
    "📊 Percentile 25-50-25": {
        "func": strategie_percentile,
        "descriere": "1 start + 2 mijloc + 1 final",
        "optim_4": "✅ Bun pentru 4/4"
    },
    "🎭 Perechi Încrucișate": {
        "func": strategie_perechi_incrucisate,
        "descriere": "2 perechi (mic+mare, Δ30-40)",
        "optim_4": "✅ Bun pentru 4/4"
    },
    "🌈 Curcubeu (Rainbow)": {
        "func": strategie_curcubeu,
        "descriere": "1 număr din 4 decade diferite",
        "optim_4": "✅ Bun pentru 4/4"
    },
    "🔄 Rotație Ciclică": {
        "func": strategie_rotatie_ciclica,
        "descriere": "1-2 numere din 2-4 zone",
        "optim_4": "✅ Bun pentru 4/4"
    },
    "🧠 AI HYBRID": {
        "func": strategie_ai_hybrid,
        "descriere": "Combină top 5 strategii automat",
        "optim_4": "🔥 Recomandat 4/4"
    }
}

# ============================
# FUNCȚII HELPER
# ============================

def valideaza_runda(runda_text, numar_numere_asteptat, numar_min, numar_max):
    """Validează o rundă introdusă de utilizator"""
    try:
        numere = [int(x.strip()) for x in runda_text.strip().split(',')]
        if len(numere) < 1:
            return False, "Eroare: Runda trebuie să conțină cel puțin un număr"
        return True, numere
    except ValueError:
        return False, "Eroare: Format invalid - folosește virgulă între numere"

def genereaza_combinatii(numar_combinatii, numar_numere, numar_min, numar_max, strategii_selectate, runde_existente=[]):
    """Generează combinații folosind strategiile selectate (rotație)"""
    if not strategii_selectate:
        strategii_selectate = ["🎯 Random Standard"]
    
    combinatii = []
    
    for i in range(numar_combinatii):
        # Rotație între strategii
        strategie_curenta = strategii_selectate[i % len(strategii_selectate)]
        strategie_func = STRATEGII[strategie_curenta]["func"]
        
        combinatie = strategie_func(numar_numere, numar_min, numar_max, runde_existente)
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
st.markdown("### Optimizat pentru 4/4 numere • Cehia Keno Rapido 12/66")
st.markdown("---")

# Configurare INIȚIALĂ
if 'numar_min' not in st.session_state:
    st.session_state.numar_min = 1
if 'numar_max' not in st.session_state:
    st.session_state.numar_max = 66
if 'numar_numere_per_combinatie' not in st.session_state:
    st.session_state.numar_numere_per_combinatie = 4

# ============================
# SECȚIUNEA 1: ISTORIC RUNDE
# ============================
st.header("📋 Istoric Runde")

col1, col2 = st.columns([2, 1])

with col1:
    uploaded_file = st.file_uploader(
        "📁 Importă runde din fișier .txt",
        type=['txt'],
        help="Fiecare rundă pe o linie nouă, numere separate prin virgulă"
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
                # Nu mai salvăm toate pentru a evita lag-ul
                # Păstrăm doar ultimele 100 pentru strategii HOT/COLD
                st.session_state.runde_salvate = runde_noi[-100:] if len(runde_noi) > 100 else runde_noi
                st.success(f"✅ {len(runde_noi)} runde procesate (salvate ultimele {len(st.session_state.runde_salvate)})!")
            
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
        f"Introduceți rundele",
        height=150,
        placeholder=f"Exemplu:\n7, 27, 22, 34, 59, 14, 55, 52, 47, 41, 51, 11\n51, 3, 61, 10, 27, 55, 24, 39, 12, 14, 65, 58",
        help="Fiecare rundă pe o linie nouă",
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
                        runde_adaugate += 1
                        # Salvăm doar pentru procesare temporară
                        if runde_adaugate <= 100:  # Limităm la 100
                            if runde_adaugate not in st.session_state.runde_salvate:
                                st.session_state.runde_salvate.append(rezultat)
                    else:
                        st.error(rezultat)
            
            if runde_adaugate > 0:
                st.success(f"✅ {runde_adaugate} runde valide au fost adăugate!")
                st.rerun()
        else:
            st.warning("⚠️ Introduceți cel puțin o rundă!")

# Afișare runde salvate
if st.session_state.runde_salvate:
    with st.expander("👁️ Vezi rundele salvate"):
        for idx, runda in enumerate(st.session_state.runde_salvate, 1):
            st.text(f"{idx}. [{len(runda)} numere] {', '.join(map(str, runda))}")

st.markdown("---")

# ============================
# SECȚIUNEA CONFIGURARE
# ============================
st.header("⚙️ Configurare")

col_conf1, col_conf2, col_conf3 = st.columns(3)

with col_conf1:
    numar_max = st.number_input(
        "Max",
        min_value=2,
        max_value=999999,
        value=st.session_state.numar_max,
        step=1,
        key='input_numar_max'
    )
    st.session_state.numar_max = numar_max

with col_conf2:
    numar_numere_per_combinatie = st.number_input(
        "Numere per bilet",
        min_value=1,
        max_value=1000,
        value=st.session_state.numar_numere_per_combinatie,
        step=1,
        key='input_numar_numere'
    )
    st.session_state.numar_numere_per_combinatie = numar_numere_per_combinatie

with col_conf3:
    if st.button("🇨🇿 Preset Keno 4/66", type="secondary", use_container_width=True):
        st.session_state.numar_min = 1
        st.session_state.numar_max = 66
        st.session_state.numar_numere_per_combinatie = 4
        st.success("✅ Configurat: 4 numere din 66!")
        st.rerun()

st.session_state.numar_min = 1  # Mereu 1

st.markdown("---")

# ============================
# SECȚIUNEA GENERARE + STRATEGII
# ============================
st.header("🚀 Generare Combinații")

# Configurare generare
col_gen1, col_gen2 = st.columns([1, 2])

with col_gen1:
    numar_combinatii = st.number_input(
        "Câte combinații să generez",
        min_value=1,
        max_value=100000,
        value=100,
        step=10,
        key="input_numar_combinatii"
    )

with col_gen2:
    st.markdown("**Sfat:** Selectează 2-5 strategii pentru diversitate optimă!")

# ============================
# STRATEGII - 2 COLOANE (5+5)
# ============================
st.subheader("🎲 Selectează Strategiile (bifează 1 sau mai multe)")

strategii_keys = list(STRATEGII.keys())
jumatate = len(strategii_keys) // 2 + 1

col_strat1, col_strat2 = st.columns(2)

with col_strat1:
    for strategie in strategii_keys[:jumatate]:
        checked = st.checkbox(
            f"{strategie}",
            value=strategie in st.session_state.strategii_selectate,
            key=f"check_{strategie}",
            help=f"{STRATEGII[strategie]['descriere']} • {STRATEGII[strategie]['optim_4']}"
        )
        
        if checked and strategie not in st.session_state.strategii_selectate:
            st.session_state.strategii_selectate.append(strategie)
        elif not checked and strategie in st.session_state.strategii_selectate:
            st.session_state.strategii_selectate.remove(strategie)

with col_strat2:
    for strategie in strategii_keys[jumatate:]:
        checked = st.checkbox(
            f"{strategie}",
            value=strategie in st.session_state.strategii_selectate,
            key=f"check_{strategie}",
            help=f"{STRATEGII[strategie]['descriere']} • {STRATEGII[strategie]['optim_4']}"
        )
        
        if checked and strategie not in st.session_state.strategii_selectate:
            st.session_state.strategii_selectate.append(strategie)
        elif not checked and strategie in st.session_state.strategii_selectate:
            st.session_state.strategii_selectate.remove(strategie)

# Info strategii selectate
if st.session_state.strategii_selectate:
    st.success(f"✅ **{len(st.session_state.strategii_selectate)} strategii selectate:** {', '.join(st.session_state.strategii_selectate)}")
else:
    st.warning("⚠️ Nicio strategie selectată - va folosi Random Standard")

# Butoane rapide
st.markdown("#### ⚡ Preseturi Rapide:")
col_preset1, col_preset2, col_preset3, col_preset4 = st.columns(4)

with col_preset1:
    if st.button("🔥 TOP 5 Recomandate", use_container_width=True):
        st.session_state.strategii_selectate = [
            "⚖️ Echilibru Perfect",
            "🔢 Pare/Impare 50/50",
            "🔥 Frecvență HOT",
            "📐 Cuadrante Extreme",
            "🎲 Sumă Controlată"
        ]
        st.rerun()

with col_preset2:
    if st.button("❄️🔥 Mix Temperaturi", use_container_width=True):
        st.session_state.strategii_selectate = [
            "🔥 Frecvență HOT",
            "❄️🔥 Mix COLD+HOT",
            "🌡️ Temperatură Graduală"
        ]
        st.rerun()

with col_preset3:
    if st.button("📊 Matematice", use_container_width=True):
        st.session_state.strategii_selectate = [
            "🪞 Oglindă Matematică",
            "🌀 Fibonacci Adaptat",
            "⚡ Salturi Prime",
            "🔢 Multipli 3-5-7"
        ]
        st.rerun()

with col_preset4:
    if st.button("🗑️ Resetează Tot", type="secondary", use_container_width=True):
        st.session_state.strategii_selectate = []
        st.rerun()

st.markdown("---")

# BUTON GENERARE PRINCIPAL
if st.button("🚀 GENEREAZĂ COMBINAȚII", type="primary", use_container_width=True):
    strategii_active = st.session_state.strategii_selectate if st.session_state.strategii_selectate else ["🎯 Random Standard"]
    
    with st.spinner(f'🎲 Generare cu {len(strategii_active)} strategii...'):
        combinatii = genereaza_combinatii(
            numar_combinatii,
            numar_numere_per_combinatie,
            st.session_state.numar_min,
            numar_max,
            strategii_active,
            st.session_state.runde_salvate
        )
        st.session_state.combinatii_generate = combinatii
        st.success(f"✅ {len(combinatii)} combinații generate cu strategiile: **{', '.join(strategii_active)}**!")
        st.balloons()

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
    
    with st.expander("📋 Vezi textul pentru copiere manuală"):
        st.code(toate_variantele, language=None)
    
    st.markdown("---")
    
    # Preview
    st.subheader(f"📜 Preview combinații ({len(st.session_state.combinatii_generate)} total)")
    
    toate_combinatii_text = []
    for i, comb in enumerate(st.session_state.combinatii_generate, 1):
        toate_combinatii_text.append(formateaza_combinatie(i, comb))
    
    st.text_area(
        "Scroll pentru toate combinațiile:",
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
    nume_fisier = f"keno_{numar_numere_per_combinatie}numere_{timestamp}.txt"
    
    col_exp1, col_exp2 = st.columns([2, 1])
    
    with col_exp1:
        st.download_button(
            label=f"📥 Descarcă {len(st.session_state.combinatii_generate)} combinații (.txt)",
            data=continut_fisier,
            file_name=nume_fisier,
            mime="text/plain",
            type="primary",
            use_container_width=True
        )
    
    with col_exp2:
        st.info(f"📁 **{nume_fisier}**")

# Footer
st.markdown("---")
st.markdown(
    "<div style='text-align: center; color: gray;'>"
    "🐲 GENERATOR DE BANI ♣️ - GeKKo 🐲 | Noroc la joc!<br>"
    "<small>V2.0 • 21 Strategii • Optimizat 4/4 • Cehia Keno Rapido</small>"
    "</div>",
    unsafe_allow_html=True
)
