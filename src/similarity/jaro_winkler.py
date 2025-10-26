"""
Jaro-Winkler Similarity Algorithm

EXPLICACIÓN MATEMÁTICA:
El algoritmo Jaro-Winkler es una variante mejorada del Jaro, optimizada para strings cortos
y errores tipográficos.

JARO DISTANCE (base):
    jaro = (m / |s1| + m / |s2| + (m - t) / m) / 3

Donde:
- m: Número de caracteres coincidentes
- t: Número de transposiciones (coincidencias fuera de orden)
- |s1|, |s2|: Longitudes de los strings
- Rango de coincidencia: max(|s1|, |s2|) / 2 - 1

JARO-WINKLER (mejorado):
    jaro_winkler = jaro + (l * p * (1 - jaro))

Donde:
- l: Longitud del prefijo común (máximo 4)
- p: Factor de escala (típicamente 0.1)

INTERPRETACIÓN:
- 0: No hay similitud
- 1: Similitud máxima (strings idénticos)

CASOS DE USO:
- Detección de errores tipográficos
- Coincidencia de nombres
- Duplicados aproximados
"""

def jaro_similarity(s1, s2):
    """
    Calcula la similitud Jaro entre dos strings
    
    Args:
        s1 (str): Primer string
        s2 (str): Segundo string
        
    Returns:
        dict: Diccionario con:
            - jaro: Similitud Jaro
            - matches: Número de caracteres coincidentes
            - transpositions: Número de transposiciones
            - match_window: Ventana de búsqueda
    """
    
    s1 = str(s1).lower()
    s2 = str(s2).lower()
    
    len1, len2 = len(s1), len(s2)
    
    if len1 == 0 and len2 == 0:
        return {
            'jaro': 1.0,
            'matches': 0,
            'transpositions': 0,
            'match_window': 0
        }
    
    if len1 == 0 or len2 == 0:
        return {
            'jaro': 0.0,
            'matches': 0,
            'transpositions': 0,
            'match_window': 0
        }
    
    # Calcular ventana de búsqueda (match window)
    match_window = max(len1, len2) // 2 - 1
    if match_window < 0:
        match_window = 0
    
    # Arreglos para marcar caracteres coincidentes
    s1_matches = [False] * len1
    s2_matches = [False] * len2
    
    matches = 0
    transpositions = 0
    
    # Encontrar caracteres coincidentes
    for i in range(len1):
        start = max(0, i - match_window)
        end = min(i + match_window + 1, len2)
        
        for j in range(start, end):
            if s2_matches[j] or s1[i] != s2[j]:
                continue
            s1_matches[i] = True
            s2_matches[j] = True
            matches += 1
            break
    
    if matches == 0:
        return {
            'jaro': 0.0,
            'matches': 0,
            'transpositions': 0,
            'match_window': match_window
        }
    
    # Contar transposiciones
    k = 0
    for i in range(len1):
        if not s1_matches[i]:
            continue
        while not s2_matches[k]:
            k += 1
        if s1[i] != s2[k]:
            transpositions += 1
        k += 1
    
    # Calcular Jaro
    jaro = (matches / len1 + 
            matches / len2 + 
            (matches - transpositions / 2) / matches) / 3
    
    return {
        'jaro': jaro,
        'matches': matches,
        'transpositions': transpositions // 2,
        'match_window': match_window
    }


def jaro_winkler_similarity(s1, s2, scaling_factor=0.1):
    """
    Calcula la similitud Jaro-Winkler entre dos strings
    
    Args:
        s1 (str): Primer string
        s2 (str): Segundo string
        scaling_factor (float): Factor de escala (default 0.1, rango [0, 0.25])
        
    Returns:
        dict: Diccionario con:
            - jaro_winkler: Similitud Jaro-Winkler
            - jaro: Similitud Jaro (base)
            - common_prefix: Prefijo común
            - common_prefix_length: Longitud del prefijo (máx 4)
            - scaling_factor: Factor usado
    """
    
    s1 = str(s1).lower()
    s2 = str(s2).lower()
    
    # Obtener Jaro
    jaro_result = jaro_similarity(s1, s2)
    jaro = jaro_result['jaro']
    
    # Encontrar prefijo común (máximo 4 caracteres)
    prefix_len = 0
    for i in range(min(len(s1), len(s2), 4)):
        if s1[i] == s2[i]:
            prefix_len += 1
        else:
            break
    
    # Limitar factor de escala
    scaling_factor = min(scaling_factor, 0.25)
    
    # Calcular Jaro-Winkler
    jaro_winkler = jaro + (prefix_len * scaling_factor * (1 - jaro))
    
    common_prefix = s1[:prefix_len]
    
    return {
        'jaro_winkler': jaro_winkler,
        'jaro': jaro,
        'common_prefix': common_prefix,
        'common_prefix_length': prefix_len,
        'scaling_factor': scaling_factor,
        'matches': jaro_result['matches'],
        'transpositions': jaro_result['transpositions'],
        'match_window': jaro_result['match_window']
    }


def jaro_winkler_distance(s1, s2, scaling_factor=0.1):
    """
    Calcula la distancia Jaro-Winkler (1 - Similitud Jaro-Winkler)
    
    Args:
        s1 (str): Primer string
        s2 (str): Segundo string
        scaling_factor (float): Factor de escala
        
    Returns:
        float: Distancia Jaro-Winkler
    """
    result = jaro_winkler_similarity(s1, s2, scaling_factor)
    return 1.0 - result['jaro_winkler']


def jaro_winkler_detailed(s1, s2, scaling_factor=0.1):
    """
    Calcula Jaro-Winkler con explicación paso a paso
    
    Args:
        s1 (str): Primer string
        s2 (str): Segundo string
        scaling_factor (float): Factor de escala
        
    Returns:
        dict: Diccionario con detalles del cálculo
    """
    
    s1_lower = str(s1).lower()
    s2_lower = str(s2).lower()
    
    # Paso 1: Obtener Jaro
    jaro_result = jaro_similarity(s1_lower, s2_lower)
    jaro_score = jaro_result['jaro']
    
    # Paso 2: Calcular prefijo común
    prefix_len = 0
    prefix = ""
    for i in range(min(len(s1_lower), len(s2_lower), 4)):
        if s1_lower[i] == s2_lower[i]:
            prefix_len += 1
            prefix += s1_lower[i]
        else:
            break
    
    # Paso 3: Aplicar fórmula Jaro-Winkler
    scaling_factor = min(scaling_factor, 0.25)
    jaro_winkler_score = jaro_score + (prefix_len * scaling_factor * (1 - jaro_score))
    
    return {
        'texto1': s1,
        'texto2': s2,
        'paso_1_longitud_s1': len(s1_lower),
        'paso_1_longitud_s2': len(s2_lower),
        'paso_2_ventana_coincidencia': jaro_result['match_window'],
        'paso_3_caracteres_coincidentes': jaro_result['matches'],
        'paso_4_transposiciones': jaro_result['transpositions'],
        'paso_5_jaro_formula': f"(m/|s1| + m/|s2| + (m-t)/m) / 3 = ({jaro_result['matches']}/{len(s1_lower)} + {jaro_result['matches']}/{len(s2_lower)} + ({jaro_result['matches']}-{jaro_result['transpositions']})/{jaro_result['matches']}) / 3",
        'paso_5_jaro_resultado': round(jaro_score, 4),
        'paso_6_prefijo_comun': prefix,
        'paso_6_longitud_prefijo': prefix_len,
        'paso_7_factor_escala': scaling_factor,
        'paso_8_jaro_winkler_formula': f"jaro + (l × p × (1 - jaro)) = {round(jaro_score, 4)} + ({prefix_len} × {scaling_factor} × (1 - {round(jaro_score, 4)}))",
        'resultado_jaro_winkler': round(jaro_winkler_score, 4),
        'resultado_distancia_jaro_winkler': round(1.0 - jaro_winkler_score, 4)
    }