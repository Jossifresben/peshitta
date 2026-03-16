# Puentes Semánticos / Semantic Bridges — Plan

## Concepto

En las lenguas semíticas, las raíces trilíteras forman familias de palabras. A veces una palabra derivada se aleja semánticamente de su raíz original (*drift*). Estos "outliers" frecuentemente conectan con el campo semántico CENTRAL de otra raíz — creando un **puente semántico** entre familias.

### Ejemplo: R-W-KH → R-KH-M

```
R-W-KH (espíritu, viento)              R-KH-M (misericordia, compasión)
├── ruakh (heb.) = espíritu, viento     ├── rakhamim (heb.) = misericordia
├── reakh (heb.) = aroma               ├── rekhem (heb.) = útero
├── ruh (ár.) = espíritu               ├── rahman (ár.) = misericordioso
├── rih (ár.) = viento                 ├── rahma (ár.) = misericordia
└── raha (ár.) = descanso ⚡ OUTLIER    └── ...
         │
         └──── puente semántico ────────────┘
              "descanso/confort" ↔ "compasión/ternura"
```

El outlier *raha* (descanso, confort) no encaja en "espíritu/viento" pero su campo semántico de cuidado/alivio conecta con R-KH-M (compasión).

### Ejemplo: E-L-M → S-T-R

```
E-L-M (mundo, eternidad)
├── olam (heb.) = mundo, eternidad
├── alam (ár.) = mundo
├── alim (ár.) = sabio
└── alam (heb.) = esconder ⚡ OUTLIER
         │
         └──── puente semántico → S-T-R (esconder, cubrir)
              ├── seter (heb.) = escondite
              ├── satr (ár.) = cubierta
              └── ...
```

## Valor Lingüístico

1. **Muestra cómo las lenguas semíticas forman una red de significado**, no familias aisladas
2. **Revela patrones de drift semántico** comunes a las tres lenguas
3. **Herramienta pedagógica**: ayuda a entender por qué palabras aparentemente no relacionadas comparten raíz
4. **Único**: ningún recurso online ofrece esta visualización de puentes entre raíces

## Arquitectura de Datos

### En cognates.json

Agregar campo `semantic_bridges` a nivel de raíz:

```json
{
  "r-w-kh": {
    "root_syriac": "ܪܘܚ",
    "gloss_en": "spirit, wind",
    "gloss_es": "espíritu, viento",
    "hebrew": [...],
    "arabic": [...],
    "outliers": ["raha"],
    "semantic_bridges": {
      "raha": {
        "target_root": "r-kh-m",
        "bridge_concept_en": "The comfort/rest meaning bridges to the compassion/mercy field",
        "bridge_concept_es": "El significado de descanso/confort conecta con el campo de compasión/misericordia",
        "relationship": "semantic_neighbor"
      }
    }
  }
}
```

### Tipos de relación

| Tipo | Descripción | Ejemplo |
|------|-------------|---------|
| `semantic_neighbor` | Significados cercanos en distinta raíz | raha (descanso) → R-KH-M (compasión) |
| `antonym_root` | Significado opuesto en otra raíz | outlier de "luz" → raíz de "oscuridad" |
| `metonymic_shift` | Desplazamiento metonímico | "esconder" (E-L-M) → S-T-R (cubrir) |
| `functional_drift` | Función gramatical cambió el significado | sustantivización que alejó el sentido |

## Generación con Claude

### Script: `scripts/generate_bridges.py`

Para cada outlier ya identificado:

```
PROMPT:
Root: R-W-KH (spirit, wind)
Outlier: raha (Arabic) = rest, comfort
This word's meaning has drifted from the core semantic field of spirit/wind.

Which OTHER Semitic triliteral root has "rest/comfort" as part of its CORE
semantic field? Consider roots in Hebrew, Arabic, and Syriac.

Return JSON:
{
  "target_root": "r-kh-m",
  "bridge_concept_en": "...",
  "bridge_concept_es": "...",
  "relationship": "semantic_neighbor|antonym_root|metonymic_shift|functional_drift"
}

If no clear bridge exists, return: {"target_root": null}
```

### Ejecución

1. Leer cognates.json → buscar todos los roots con `outliers` no vacíos
2. Para cada outlier, preguntar a Claude cuál es la raíz destino
3. Validar que la raíz destino EXISTE en nuestro cognates.json (si no, ignorar)
4. Guardar en `semantic_bridges`

## Visualización en D3.js

### Interacción

1. Outlier se muestra con borde punteado (ya implementado)
2. Al hacer **click** en un outlier:
   - Se expande el grafo
   - Muestra la raíz destino como un nuevo nodo central secundario
   - Línea punteada dorada conecta el outlier con la nueva raíz
   - Los cognados de la raíz destino aparecen como nodos satélite
3. Click de nuevo para colapsar

### Layout

```
                    ┌─────────────┐
                    │  R-KH-M     │ ← raíz destino (nuevo centro)
                    │ misericordia│
                    └──────┬──────┘
                       ╱   │   ╲
                 rahman  rahma  rakhamim

           ·····puente·····
           ·               ·
      ┌────┴────┐
      │  raha   │ ← outlier (click para expandir)
      │descanso │
      └────┬────┘
           │
     ┌─────┴─────┐
     │  R-W-KH   │ ← raíz original (centro)
     │espíritu   │
     └─────┬─────┘
        ╱  │  ╲
   ruakh  ruh  rih
```

### Colores

| Elemento | Color |
|----------|-------|
| Raíz original (centro) | Marrón (#8B4513) |
| Cognados regulares | Azul (heb), Verde (ár), Terracota (sir) |
| Outlier | Borde punteado dorado |
| Puente (línea) | Dorado punteado, animado |
| Raíz destino | Marrón claro (#B8860B) |
| Cognados de raíz destino | Azul/Verde más claro (tono pastel) |

## Fases de Implementación

### Fase 1: Datos ✅
- [x] Crear `scripts/generate_bridges.py`
- [x] Ejecutar sobre todos los outliers identificados (651 outliers → 363 bridges)
- [x] Validar y corregir textos de concepto (98 mismatches corregidos)
- [x] Guardar en cognates.json

### Fase 2: API ✅
- [x] Modificar `/api/root-family` para incluir `semantic_bridges` en respuesta
- [x] Reutilizar `/api/root-family?root=<target>` para obtener familia de raíz destino
- [x] Agregar fallback de correspondencias sonoras semíticas (S↔SH, TH↔T, D↔TH, TS↔S)

### Fase 3: Visualizador ✅
- [x] Hacer outliers clickeables (cursor pointer, tooltip "Click para ver puente")
- [x] Fetch de raíz destino al hacer click
- [x] Animar expansión del grafo con nuevos nodos (fade in 400ms)
- [x] Agregar línea punteada dorada de puente (animada con CSS)
- [x] Click para colapsar (fade out 300ms)
- [x] Modo pantalla completa (Fullscreen API)

### Fase 4: UX ✅
- [x] Tooltip en outlier: "Click para explorar puente → TARGET-ROOT"
- [x] Concepto de puente mostrado en tooltip
- [x] Leyenda actualizada con símbolo de puente (anillo dorado pulsante)
- [x] Transición animada suave al expandir/colapsar
- [x] Outliers con puente: anillo dorado pulsante + borde sólido + etiqueta "🔗 bridge"
- [x] Outliers sin puente: borde punteado dorado + color atenuado (sin cambios)
- [x] Texto de significado con word-wrap (2 líneas) para evitar truncamiento
- [x] Burbujas más grandes (heb/ar 52px, syr 48px, centro 64px)

## Resultados Finales

- 651 outliers detectados (de 3,780 cognados)
- 363 puentes semánticos generados (56% de outliers tienen puente válido)
- 207 raíces con al menos un puente
- 0 mismatches en textos de concepto

## Estado: ✅ COMPLETADO (2026-03-16)
