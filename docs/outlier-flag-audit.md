# Auditoría de flags `outlier` en `data/cognates.json`

Generado por `scripts/audit_outlier_flags.py` (modelo `claude-opus-4-5`).
**Informe únicamente — no se ha modificado `data/cognates.json`.**

## Resumen

| Métrica | Valor |
|---|---|
| Raíces con ≥1 flag | 258 |
| Raíces auditadas | 258 |
| Raíces con error de API/parseo | 0 |
| Flags revisados | 620 |
| Flags que deberían **eliminarse** (falsos positivos) | 340 |
| Flags **confirmados** como outliers genuinos | 280 |
| Veredictos con confianza baja/media | 109 |
| Coste real | $2.89 |

El 55% de los flags revisados son falsos positivos.

## Cambios propuestos (flags a eliminar)

340 entradas. Cada una debería perder `"outlier": true`.

| Raíz | Gloss (es) | Lang | Translit | Significado | Conf. | Justificación |
|---|---|---|---|---|---|---|
| `T-w-b` | bueno, bienaventurado | ar | ta'abbā | ser benévolo, comportarse bien | high | Ser benévolo y comportarse bien expresan directamente el campo semántico de bueno/bienaventurado. |
| `T-y-b` | bueno, preparar | heb | mattovah | lo mejor | high | Significa 'lo mejor', directamente derivado de 'bueno' (glosa); forma nominal superlativa, no divergencia semántica. |
| `a-l-p` | aprender, enseñar; mil | ar | ta'allafa | estar familiarizado, asociarse | high | Familiarizarse/asociarse deriva de 'aprender': volverse acostumbrado, conocer bien algo o alguien. |
| `a-l-p` | aprender, enseñar; mil | ar | ma'lūf | común, habitual | high | Común/habitual deriva de 'aprender/familiarizarse': lo que se ha llegado a conocer bien, lo acostumbrado. |
| `a-l-p` | aprender, enseñar; mil | ar | ta'līf | composición, compilación | high | Composición/compilación es extensión de 'enseñar': reunir y organizar conocimiento, producir obra escrita. |
| `a-l-p` | aprender, enseñar; mil | heb | allīf | domesticado, dócil | high | Domesticado/dócil es extensión natural de 'enseñar': animal adiestrado, que ha aprendido a obedecer. |
| `a-m-n` | confiar, amén | heb | aman | ser fiel/confiar | high | Significa exactamente 'ser fiel/confiar', que es el gloss del root; etiquetado erróneo evidente. |
| `a-m-n` | confiar, amén | heb | omanut | arte | medium | Arte deriva de 'habilidad confiable/maestría'; el artesano (oman) es alguien en quien se confía por su pericia. |
| `a-m-r` | decir | ar | 'amārah | señal, indicio | high | Una señal o indicio es algo que 'dice' o comunica información; extensión metafórica directa de 'decir'. |
| `a-n-sh` | hombre, humano | heb | ish | hombre | high | Significa 'hombre', exactamente el gloss de la raíz; aunque la forma es irregular, es cognado semántico directo. |
| `a-r-e` | tierra, terreno | ar | ma'radah | lugar de la tierra, terreno | high | Significa 'lugar de la tierra, terreno', extensión locativa directa del gloss 'tierra, terreno'. |
| `a-r-e` | tierra, terreno | ar | ardíyyah | planta baja, piso bajo | high | 'Planta baja' deriva de 'tierra/suelo' — el piso que está al nivel de la tierra. |
| `a-r-e` | tierra, terreno | heb | arká | suelo, superficie de la tierra | high | Significa 'suelo, superficie de la tierra', directamente dentro del campo semántico de 'tierra, terreno'. |
| `a-s-r` | atar, ligar | ar | 'asrah | familia, linaje | high | Familia/linaje deriva de 'atar': los lazos familiares son vínculos que unen a las personas, extensión metafórica directa. |
| `a-s-r` | atar, ligar | ar | 'isārah | cautiverio, esclavitud | high | Cautiverio/esclavitud es exactamente el estado de estar atado o ligado; extensión semántica clara del gloss 'atar, ligar'. |
| `a-th-r` | lugar, tierra | ar | ʾāthārī | arqueológico | high | Arqueológico deriva de 'huella/vestigio' (athar), extensión natural de lugar/tierra como sitio de restos. |
| `a-th-y` | venir, llegar | ar | ma'ab | regreso, vuelta | high | Regreso/vuelta implica volver a venir, extensión semántica directa del concepto de llegar. |
| `a-th-y` | venir, llegar | ar | 'atin | que viene, futuro | high | Que viene/futuro es participio activo de venir, describe al que viene, derivación directa del gloss. |
| `a-th-y` | venir, llegar | ar | ītā' | traer, entregar | high | Traer/entregar es causativo de venir: hacer llegar algo, extensión morfológica estándar. |
| `a-th-y` | venir, llegar | heb | t'via | traer, llevar | high | Traer/llevar es causativo de venir: hacer que algo venga, extensión morfológica estándar del gloss. |
| `a-th-y` | venir, llegar | heb | bi'a | llegada, venida | high | Llegada/venida es el sustantivo verbal de venir/llegar, parafrasea directamente el gloss. |
| `a-y-l` | árbol, poder | ar | ʾillah | causa, razón | medium | Causa/razón puede derivar de 'poder' como fuerza causal o principio activo detrás de eventos. |
| `a-z-l` | ir | ar | ma'āzil | dificultades, problemas | medium | Dificultades como 'cosas que se van/pierden' o 'situaciones de las que uno debe irse' — extensión metafórica plausible de 'ir/quitar'. |
| `b-T-l` | cesar, estar ocioso | ar | batil | falso/vano | high | 'Falso/vano' deriva directamente de 'ser nulo/cesar': lo que cesa de valer es vano o inválido. |
| `b-T-l` | cesar, estar ocioso | ar | baatil | falso, vano | high | Duplicado de ar:2; 'falso/vano' es extensión semántica natural de 'nulo/cesar'. |
| `b-e-a` | buscar, pedir | ar | maṭlūb | buscado, requerido | high | Participio pasivo de ṭalaba 'pedir/buscar'; 'buscado/requerido' es el resultado directo de la acción del glosa. |
| `b-h-th` | avergonzarse | ar | bahata | calumniar; quedarse atónito | high | Calumniar causa vergüenza a la víctima; quedarse atónito es parálisis emocional relacionada con la vergüenza intensa. |
| `b-h-th` | avergonzarse | ar | bahita | estar atónito | high | Estar atónito/estupefacto es extensión semántica de la parálisis que produce la vergüenza extrema. |
| `b-h-th` | avergonzarse | ar | buhtān | calumnia | high | Calumnia es el acto que causa vergüenza injusta a otro; desarrollo causativo claro desde 'avergonzar'. |
| `b-kh-r` | primogénito | ar | bukrah | mañana | high | Mañana como 'parte temprana del día' conecta con primogénito como 'primero en tiempo'; extensión semántica de primacía temporal. |
| `b-kh-r` | primogénito | ar | bākir | temprano | high | Temprano expresa la misma noción de 'primero en el tiempo' que subyace a primogénito; extensión natural del concepto de primacía. |
| `b-kh-r` | primogénito | ar | ibtakara | inventar | medium | Inventar como 'ser el primero en crear algo' deriva del sentido de primacía; quien inventa es el 'primogénito' de una idea. |
| `b-r-a` | crear, hijo | heb | bri' | sano, saludable | high | Sano/saludable es extensión natural de 'crear': algo bien creado, en buen estado, completo en su creación. |
| `b-y-sh` | malo, malvado | heb | mevuyash | avergonzado, abochornado | high | Vergüenza es consecuencia natural de maldad; estar avergonzado conecta con 'malo' como estado resultante de hacer/ser malo. |
| `b-y-th` | casa | ar | biyát | pernoctación | high | Pernoctación (pasar la noche) deriva del verbo bāta 'pasar la noche en casa'; extensión verbal directa del concepto de casa/hogar. |
| `b-y-th` | casa | ar | biyawíy | casero | high | Casero/homely es derivación adjetival directa de 'casa'; significa literalmente 'relativo al hogar', sin divergencia semántica. |
| `d-b-r` | guiar, conducir | heb | midbar | desierto | medium | El desierto es 'lugar donde se conduce/guía' ganado; extensión locativa del concepto de guiar/pastorear rebaños. |
| `d-k-y` | puro, limpio | ar | zakāt | limosna, caridad | high | Zakāt significa 'purificación' del alma/riqueza mediante la caridad; es extensión directa de 'puro/limpio' en sentido ritual y espiritual. |
| `d-kh-l` | temer | heb | dakhal | temer (arameo bíblico) | high | Significa exactamente 'temer', igual que el gloss; ser arameo bíblico no lo hace divergente. |
| `d-kh-r` | recordar, varón | ar | tadhkira | billete/recordatorio | high | Un billete/ticket es un 'recordatorio' escrito de una transacción; extensión directa de 'recordar' vía forma nominal instrumental. |
| `d-m-a` | parecerse, sangre | ar | Adam | Adán | high | Préstamo hebreo del mismo nombre propio; comparte la misma conexión etimológica tradicional con sangre/semejanza. |
| `d-m-a` | parecerse, sangre | heb | adam | hombre/Adán | high | Adán/adam deriva de 'adamah' (tierra) pero también conecta con 'dam' (sangre) – etimología popular bíblica bien establecida. |
| `d-m-r` | sorprenderse, admirarse | ar | madhúsh | atónito, asombrado | high | Madhúsh significa atónito/asombrado, traducción directa del gloss sorprenderse/admirarse. |
| `d-m-y` | asemejar, imagen | ar | dumyah | muñeca, figura | high | Muñeca/figura es extensión directa de 'imagen'; una muñeca es una figura o imagen pequeña de persona. |
| `d-r-sh` | buscar, interpretar (midrash) | ar | daris | estudiante | high | Estudiante es agente de estudiar/buscar conocimiento; extensión directa del campo semántico de buscar/interpretar. |
| `d-r-sh` | buscar, interpretar (midrash) | ar | durūs | estudios | high | Estudios es nominalización de estudiar, que deriva de buscar/interpretar; pertenece claramente al dominio semántico. |
| `d-y-n` | juzgar | ar | madina | ciudad | high | Madina deriva de d-y-n como 'lugar donde se juzga/gobierna'; la ciudad es sede de autoridad y juicio. |
| `d-y-n` | juzgar | ar | dīnah | ciudad | high | Dīnah es variante de madina; ciudad como centro de jurisdicción conecta directamente con 'juzgar'. |
| `e-b-d` | hacer, servir | heb | i'bud | procesamiento, elaboración | high | Procesamiento/elaboración es extensión directa de 'hacer': procesar algo es trabajarlo o hacerlo, derivación nominal regular. |
| `e-b-r` | pasar, cruzar | ar | ibra | lección/moraleja | high | Ibra (lección) es extensión metafórica: algo que se 'atraviesa' mentalmente para extraer enseñanza. |
| `e-b-r` | pasar, cruzar | heb | ivri | hebreo | high | Ivri (hebreo) deriva de 'los que cruzan' (el río), etnónimo clásico basado en la raíz 'cruzar'. |
| `e-d-l` | reprender, culpar | ar | taʿdīl | modificación, corrección | medium | Corrección/modificación puede conectarse con reprender: corregir errores es cercano a censurar faltas. |
| `e-d-th` | iglesia, asamblea | ar | 'īd | fiesta, festividad | high | Fiesta/festividad se conecta directamente con asamblea: reunión periódica comunitaria para celebrar, extensión natural del concepto. |
| `e-g-l` | becerro, apresurarse | ar | 'ajiil | acelerado, rápido | high | El gloss incluye 'apresurarse/hasten'; 'acelerado/rápido' es sinónimo directo de ese campo semántico. |
| `e-g-l` | becerro, apresurarse | ar | 'ujuul | apresurarse, precipitarse | high | El gloss incluye 'apresurarse/hasten'; 'apresurarse, precipitarse' restates exactamente ese significado. |
| `e-h-d` | recordar, testificar | ar | ta'ahhud | compromiso | high | Compromiso deriva directamente de 'ahd (pacto/promesa); es la forma V nominal que significa asumir un pacto, extensión natural del gloss 'testificar'. |
| `e-l-th` | causa, razón | ar | 'alīl | enfermo, débil, afligido | high | Extensión semántica directa: 'illa significa también 'enfermedad', y 'alīl es 'el afectado por una causa/dolencia'. |
| `e-l-y` | subir, alto | heb | ma'alah | grado/escalón | high | Un escalón/grado es literalmente aquello por donde se sube; extensión directa de 'subir, alto'. |
| `e-m-m` | pueblo, nación | ar | 'amm | general/público | high | Lo 'general/público' deriva naturalmente de 'pueblo/nación' — lo que pertenece a toda la gente, extensión semántica directa. |
| `e-m-r` | habitar, morar | ar | 'umr | vida/edad | high | Vida/edad deriva de 'tiempo que uno habita el mundo'; extensión metafórica bien documentada. |
| `e-m-r` | habitar, morar | ar | 'Umar | Omar (nombre) | high | Nombre propio derivado directamente de la raíz عمر (vida/habitar); no es divergencia semántica. |
| `e-m-r` | habitar, morar | heb | 'ammīr | abundante, próspero | medium | Próspero/abundante puede derivar de 'lugar habitado floreciente'; extensión metafórica plausible. |
| `e-m-r` | habitar, morar | heb | ma'ămār | ensamblaje, estructura | medium | Estructura/ensamblaje se conecta con construir, que es extensión natural de habitar (cf. árabe 'amara). |
| `e-n-a` | responder | ar | 'aniinun | gemido | high | Gemido es una forma de respuesta vocal/expresión; extensión semántica de responder con sonido. |
| `e-n-a` | responder | heb | 'an'vah | humildad | high | Humildad conecta con ע-נ-ה en sentido de someterse/responder con deferencia; extensión figurativa legítima. |
| `e-r-b` | mezclar, garantizar, oeste | ar | ḡaríb | extranjero, raro | high | Extensión semántica clara: 'oeste' → 'donde el sol se pone/se va' → 'el que viene de lejos' → 'extranjero, extraño'. |
| `e-r-s` | cama, lecho | ar | ʿarsh | trono | high | Un trono es un asiento elevado/ceremonial; extensión directa del campo semántico de mueble para reclinarse (cama, lecho, diván). |
| `e-r-s` | cama, lecho | ar | ʿarrāsh | tapicero, acolchador | high | Tapicero/acolchador es agente que fabrica o repara camas, colchones y muebles; derivación agentiva directa del glosa. |
| `e-w-l` | iniquidad, injusticia | ar | ʿawl | injusticia, parcialidad | high | Significa 'injusticia, parcialidad', directamente dentro del campo semántico del gloss. |
| `e-w-l` | iniquidad, injusticia | ar | ʿāʾil | necesitado, indigente | medium | El indigente sufre injusticia; puente semántico plausible: quien padece iniquidad queda necesitado. |
| `e-w-l` | iniquidad, injusticia | heb | ʿāval | ser injusto, ser inicuo | high | Significa exactamente 'ser injusto, inicuo', traducción directa del gloss 'iniquidad, injusticia'. |
| `e-w-l` | iniquidad, injusticia | heb | ʿevel | injusticia, iniquidad | high | Significa 'injusticia, iniquidad', idéntico al gloss de la raíz. |
| `e-w-l` | iniquidad, injusticia | heb | ʿavlā | injusticia, agravio | high | Significa 'injusticia, agravio', sinónimo exacto del gloss 'iniquidad, injusticia'. |
| `e-y-n` | ojo, fuente | ar | mu'ayana | inspección | high | Inspección deriva directamente de 'ojo' (ver con los propios ojos), extensión verbal estándar del campo semántico. |
| `e-y-n` | ojo, fuente | ar | 'ayyaan | vigilante, observador | high | Vigilante/observador es quien usa los ojos para observar; extensión agentiva directa del significado 'ojo'. |
| `e-z-l` | hilar, perezoso | ar | ʿazala | aislar | medium | Aislar puede derivar de 'hilar' (separar fibras) o conectarse con 'perezoso' (apartado, inactivo); puente semántico plausible. |
| `e-z-l` | hilar, perezoso | ar | ʿazl | aislamiento | medium | Aislamiento como extensión nominal de aislar; mismo puente semántico que el verbo raíz. |
| `e-z-l` | hilar, perezoso | ar | ʿazīl | solitario | medium | Solitario conecta con perezoso (persona apartada/retraída) y con hilar (acción solitaria); extensión semántica razonable. |
| `e-z-z` | ser fuerte | heb | ma'oz | fortaleza/refugio | high | Fortaleza/refugio es extensión locativa directa de 'ser fuerte'; compare árabe ma'izzun 'lugar fortificado' del mismo patrón morfológico. |
| `g-b-r` | hombre, ser fuerte | ar | jabr | álgebra/coerción | high | Coerción deriva directamente de 'fuerza'; álgebra viene del árabe 'al-jabr' (restauración/recomposición forzada), extensión metafórica del sentido de forzar/reparar. |
| `g-b-y` | elegir, escoger | heb | gaviv | depósito, reserva | high | Depósito/reserva es extensión de 'recolectar' (cognados árabes), que deriva de elegir/seleccionar para guardar. |
| `g-l-a` | revelar | ar | jullā' | muy claro, evidente | high | «Muy claro, evidente» es extensión directa de «revelar»: lo revelado se vuelve claro/evidente. |
| `g-m-r` | completar, terminar | ar | ʾijmār | conclusión, finalización | high | Conclusión/finalización es traducción directa del gloss completar/terminar. |
| `g-n-y` | jardín | ar | junna | paraíso | high | Paraíso es extensión directa de jardín; el Jardín del Edén es el paradigma de paraíso en lenguas semíticas. |
| `g-z-r` | cortar, circuncidar | ar | jazira | isla (cortada del continente) | high | La propia glosa explica el puente: isla = 'cortada del continente'; extensión metafórica directa de 'cortar'. |
| `g-z-r` | cortar, circuncidar | ar | jazr | reflujo, marea baja | high | El reflujo 'corta' o retira el agua de la costa; extensión semántica natural del concepto de cortar/separar. |
| `h-l-k` | caminar, ir | heb | mahol | danzarín | high | Danzar es una forma rítmica de caminar/moverse; extensión natural del dominio semántico de 'ir, caminar'. |
| `h-p-k` | voltear, invertir | heb | hefekh | opuesto, contrario | high | Lo opuesto/contrario es el resultado semántico directo de 'voltear/invertir' — lo invertido es lo opuesto. |
| `h-p-k` | voltear, invertir | heb | hepekh | oposición, contrario | high | Oposición/contrario deriva naturalmente de 'invertir' — estar en oposición es estar volteado respecto a otro. |
| `h-w-y` | ser, llegar a ser | ar | huwa | él (pronombre) | high | El pronombre 'él' deriva de la raíz 'ser'; es el que 'es', extensión gramatical directa del concepto de existencia. |
| `h-w-y` | ser, llegar a ser | ar | hawiyya | identidad | high | Identidad es 'lo que uno es', derivación nominal abstracta directa del verbo 'ser'. |
| `h-w-y` | ser, llegar a ser | ar | hawiyyah | identidad | high | Duplicado de ar:1; identidad deriva directamente de 'ser' como cualidad esencial. |
| `h-w-y` | ser, llegar a ser | ar | mahwan | lugar donde algo se convierte en | high | Significado es exactamente 'lugar donde algo llega a ser', paráfrasis locativa directa del gloss. |
| `k-h-n` | sacerdote | ar | kahin | adivino/sacerdote | high | La propia glosa incluye 'sacerdote'; adivino es función sacerdotal antigua, extensión directa del rol religioso. |
| `k-h-n` | sacerdote | ar | kahana | adivinación | high | Adivinación era función central del sacerdocio antiguo; extensión semántica natural del oficio sacerdotal. |
| `k-h-n` | sacerdote | ar | kaahina | sacerdotisa | high | Sacerdotisa es simplemente la forma femenina de sacerdote; parafrasea directamente la glosa. |
| `k-h-n` | sacerdote | ar | takahhan-na | adivinar | high | Adivinar era actividad propia del sacerdote/kohen; derivación verbal del rol sacerdotal adivinatorio. |
| `k-n-sh` | reunir, congregar | ar | kanz | tesoro, acumulación | high | Tesoro/acumulación es extensión directa de 'reunir': acumular riquezas es reunirlas en un lugar. |
| `k-n-y` | reunir, llamar | ar | kanā | llamar | high | Llamar por sobrenombre corresponde exactamente al gloss 'call by name'; no hay divergencia. |
| `k-n-y` | reunir, llamar | ar | takanná | llamarse por un apodo o sobrenombre | high | Forma reflexiva de 'llamar por nombre'; extensión morfológica directa del gloss. |
| `k-n-y` | reunir, llamar | ar | kinyah | apodo, sobrenombre | high | Sustantivo derivado de 'llamar por nombre'; el apodo es el nombre dado, dentro del gloss. |
| `k-n-y` | reunir, llamar | heb | kana | dar título | high | Dar título es extensión directa de 'llamar' (call by name); nombrar/titular es el mismo campo semántico. |
| `k-p-r` | negar, aldea | ar | kāfira | mujer incrédula | high | Forma femenina de kāfir; 'mujer incrédula' deriva directamente del gloss 'negar'. |
| `k-p-r` | negar, aldea | heb | kofér | incrédulo, escéptico | high | Incrédulo es extensión agentiva directa de 'negar': el que niega (la fe) es un incrédulo. |
| `k-r-h` | estar enfermo, débil | ar | kariha | detestar, aborrecer | high | Puente claro: lo enfermo/débil causa aversión; 'detestar' deriva de la repugnancia hacia lo enfermizo. |
| `k-r-h` | estar enfermo, débil | ar | makrūh | detestable | high | Derivación directa de kariha; 'detestable' es lo que provoca rechazo, extensión semántica de enfermedad/debilidad. |
| `k-r-h` | estar enfermo, débil | ar | karīh | repulsivo, desagradable | high | 'Repulsivo, desagradable' conecta con enfermedad: lo enfermo genera repugnancia, desarrollo semántico común. |
| `k-s-y` | cubrir, ocultar | heb | mékhusseh | escondido, oculto | high | El gloss incluye explícitamente 'ocultar'; 'escondido, oculto' es participio pasivo directo del significado raíz. |
| `k-w-n` | ser correcto, correcto | ar | kawn | universo, ser | high | El 'universo' (kawn) deriva de 'ser/existir'; es la totalidad de lo que ES, extensión nominal directa del gloss. |
| `k-w-n` | ser correcto, correcto | ar | kawini | ser, existir | high | 'Ser, existir' es sinónimo directo de la raíz K-W-N en árabe; no hay divergencia semántica. |
| `k-w-n` | ser correcto, correcto | ar | ka'in | ser, entidad | high | 'Ser, entidad' (ka'in) es el participio activo de kana; nombra lo que existe, extensión nominal directa. |
| `k-w-n` | ser correcto, correcto | ar | takawwun | formación, desarrollo | high | 'Formación, desarrollo' (takawwun) es el proceso de llegar a ser; extensión verbal reflexiva del gloss. |
| `kh-T-y` | pecar | ar | makhṭū' | erróneo | high | En árabe خطأ abarca tanto 'error' como 'pecado'; 'erróneo' es extensión directa del sentido de equivocarse/fallar moralmente. |
| `kh-b-l` | corromper, destruir | ar | habala | estar embarazada | high | Metáfora común: 'estar atada/ligada' (con cuerda) → embarazo; el cordón umbilical conecta ambos sentidos semánticos. |
| `kh-b-l` | corromper, destruir | ar | ḥabal | quedar embarazada | high | Misma extensión metafórica: cuerda/atar → embarazo; el vínculo con ḥabl 'cuerda/cordón umbilical' es bien documentado. |
| `kh-b-r` | compañero, unir | ar | ḥabara | unir, juntar | high | "Unir, juntar" corresponde exactamente a la glosa "unir" de la raíz; no hay divergencia alguna. |
| `kh-b-r` | compañero, unir | ar | ḥabīr | experto, entendido | high | "Experto" deriva de "compañero/asociado" → quien comparte conocimiento; extensión semántica clara del campo de la raíz. |
| `kh-d-a` | uno, alegrarse | ar | waḥīd | único, solitario | high | Único/solitario es extensión directa de 'uno'; ser único deriva naturalmente de la unidad. |
| `kh-d-r` | rodear | ar | ḥadara | descender, rodear | high | El significado 'rodear' coincide exactamente con el glosa de la raíz. |
| `kh-d-r` | rodear | ar | ḥādir | que rodea | high | Participio activo de 'rodear'; significa literalmente 'que rodea', idéntico al glosa. |
| `kh-d-r` | rodear | heb | ḥadarah | envoltura | high | Una envoltura es algo que rodea un objeto; extensión directa del significado 'rodear'. |
| `kh-d-th` | nuevo, renovar | ar | hadith | relato/hadiz | high | Hadith significa 'relato nuevo/reciente'; extensión semántica directa de 'nuevo' a 'noticia/narración reciente'. |
| `kh-d-th` | nuevo, renovar | ar | ḥudathā' | modernos, jóvenes | high | Plural de 'joven/moderno'; los jóvenes son los 'nuevos', extensión natural del glosa 'nuevo'. |
| `kh-d-th` | nuevo, renovar | ar | muḥaddath | reciente, moderno | high | Significa 'reciente, moderno' — prácticamente sinónimo del glosa 'nuevo, renovar'. |
| `kh-k-m` | ser sabio | ar | hukm | juicio/gobierno | high | Juicio/gobierno deriva de sabiduría por extensión semántica: el sabio juzga y gobierna con discernimiento. |
| `kh-k-m` | ser sabio | ar | ḥukúmah | gobierno | high | Gobierno es extensión institucional del concepto de sabiduría aplicada al juicio y administración pública. |
| `kh-k-m` | ser sabio | ar | ḥákim | gobernante, juez | high | Gobernante/juez deriva naturalmente de sabio: quien posee sabiduría ejerce autoridad para juzgar. |
| `kh-l-l` | profanar, comenzar (halal) | ar | halíl | esposo, amante | medium | Esposo/amante deriva de 'lo lícito' (حلال): la pareja legalmente permitida; extensión semántica clara del concepto de licitud. |
| `kh-l-l` | profanar, comenzar (halal) | ar | mahíll | lugar, sitio | high | Duplicado de ar:3 (mahall); 'lugar' deriva de حَلَّ 'establecerse/detenerse', extensión locativa estándar de la raíz. |
| `kh-l-p` | cambiar, en lugar de | ar | khilaf | desacuerdo | high | Desacuerdo deriva de 'cambiar/diferir': cuando dos partes intercambian posiciones opuestas, hay desacuerdo. |
| `kh-l-p` | cambiar, en lugar de | ar | ikhtilaf | diferencia | high | Diferencia es extensión directa de 'cambiar': lo que cambia entre dos cosas es su diferencia. |
| `kh-l-p` | cambiar, en lugar de | ar | mukhalifah | oposición, desacuerdo | high | Oposición deriva de 'ir en contra/cambiar de dirección', extensión semántica clara de la raíz. |
| `kh-l-p` | cambiar, en lugar de | ar | takhallufu | atraso, retraso | medium | Atraso significa 'quedarse atrás' mientras otros avanzan/cambian; extensión de sucesión/reemplazo temporal. |
| `kh-l-q` | afeitar, porción | ar | khaliiQ | apropiado, digno | high | Deriva de 'crear': lo creado para algo es 'apropiado/digno' para ello; extensión semántica clara. |
| `kh-l-q` | afeitar, porción | ar | khallaaQ | creativo, imaginativo | high | Forma intensiva de 'crear' (خلق); 'muy creador' → 'creativo/imaginativo' es derivación directa. |
| `kh-p-y` | cubrir, lavar | ar | ḥāfin | descalzo | medium | Descalzo (sin cubierta en los pies) deriva semánticamente de 'cubrir' por negación; el participio activo indica ausencia de cobertura. |
| `kh-r-m` | anatema, consagrar, destruir | heb | ḥaru'm | prohibición, veto | high | Prohibición/veto es extensión directa de 'anatema/ban'; algo bajo anatema está prohibido. Los cognados árabes confirman este desarrollo semántico. |
| `kh-r-n` | otro, diferente | ar | takharrara | separarse, apartarse | high | Separarse es extensión natural de 'otro/diferente': volverse otro, apartarse del grupo. |
| `kh-r-p` | reprochar, invierno | ar | khārif | criticón, censor | high | Un 'criticón/censor' es agente de la acción de reprochar; extensión agentiva directa del gloss. |
| `kh-r-p` | reprochar, invierno | ar | khurfah | oprobio, vergüenza | high | 'Oprobio, vergüenza' es sinónimo directo de 'reproach'; coincide exactamente con el gloss. |
| `kh-r-sh` | ser sordo, arar | ar | aḥ·ra·sha | quedar sordo | high | El gloss incluye 'be deaf'; 'quedar sordo' es exactamente ese significado en forma causativa/incoativa. |
| `kh-r-sh` | ser sordo, arar | heb | kheresh | sordo | high | El gloss incluye explícitamente 'ser sordo'; 'sordo' traduce directamente ese significado. |
| `kh-r-th` | fin, último | ar | khārij | exterior, externo | high | Exterior/externo indica lo que está 'más allá del límite', extensión natural de 'fin/extremo'. |
| `kh-r-th` | fin, último | ar | kharaja | salir, irse | high | Salir significa cruzar el límite hacia afuera; extensión verbal directa del concepto de 'fin/extremo'. |
| `kh-r-th` | fin, último | ar | khuruuj | salida, éxodo | high | Salida/éxodo es el sustantivo de 'salir', misma extensión semántica de cruzar el límite. |
| `kh-s-m` | amordazar, envidiar | ar | ḥasama | zanjar, resolver | medium | Zanjar/resolver puede derivar de 'cortar' o 'cerrar' un asunto, extensión metafórica de amordazar/obstruir. |
| `kh-s-m` | amordazar, envidiar | ar | ḥaṣīm | envidiado | high | Envidiado es derivación directa del significado 'envidiar' incluido en el gloss. |
| `kh-s-r` | carecer, necesitar | ar | khasira | perder | high | Perder es extensión semántica natural de carecer: quien pierde algo pasa a carecer de ello. |
| `kh-s-r` | carecer, necesitar | ar | khasir | perdedor | high | Perdedor deriva de perder, que conecta con carecer; es agentivo de la misma extensión semántica. |
| `kh-s-r` | carecer, necesitar | ar | makshur | empobrecido, perdido | high | Empobrecido/perdido implica estado de carencia, extensión directa del campo semántico de la raíz. |
| `kh-sh` | sufrir, padecer | ar | ikhsās | sensación, percepción | high | La sensación/percepción es extensión directa de 'sufrir/sentir dolor'; el campo semántico incluye toda experiencia sensorial. |
| `kh-t-a` | pecar | ar | makhtá'a | error | high | El significado 'error' es extensión directa de 'pecar/errar'; el cognate ar:0 ya muestra que la raíz incluye 'errar/equivocarse'. |
| `kh-w-h` | mostrar, declarar | ar | ḥawwā' | Eva (nombre propio femenino) | medium | Eva se interpreta tradicionalmente como 'la que da vida/declara'; el nombre propio deriva de la raíz semítica asociada a mostrar o vivificar. |
| `kh-w-r` | mirar, blanco | ar | hiwar | diálogo | high | حِوَار deriva de حَوَرَ 'volver/mirar'; diálogo es intercambio de miradas/atención entre interlocutores. |
| `kh-w-r` | mirar, blanco | ar | huriyya | hurí (mujer de ojos claros) | high | Hurí significa 'mujer de ojos blancos/claros', directamente del gloss 'blanco' — no es divergente. |
| `kh-w-r` | mirar, blanco | ar | hayyara | confundir, perturbar | medium | حَيَّرَ 'confundir' deriva de hacer que alguien mire en varias direcciones sin orientarse, extensión de 'mirar'. |
| `kh-y-b` | culpable, deber | ar | wa-jib | obligatorio, debido | high | «Obligatorio, debido» es extensión directa de «deber»; la obligación implica deuda moral o legal. |
| `kh-y-b` | culpable, deber | ar | maw-jub | obligado, requerido | high | «Obligado, requerido» pertenece claramente al campo semántico de «deber». |
| `kh-y-b` | culpable, deber | ar | mah-yub | culpable, responsable | high | «Culpable, responsable» coincide exactamente con el glosa «culpable, deber». |
| `kh-y-l` | fuerza, poder | ar | hila | astucia/estratagema | high | Astucia/estratagema deriva de 'fuerza mental, capacidad ingeniosa'; extensión metafórica de poder/habilidad. |
| `kh-y-l` | fuerza, poder | ar | hilatun | estratagema, truco | high | Duplicado de ar:0; estratagema es extensión de poder como habilidad/ingenio para lograr algo. |
| `l-b-n` | blanco, ladrillo | ar | laban | leche; ladrillo | high | Leche es blanca (extensión de 'blanco'); ladrillo coincide exactamente con el gloss. |
| `l-b-n` | blanco, ladrillo | ar | lubnā | tipo de jazmín blanco | high | Jazmín blanco nombrado por su color; extensión nominal directa del gloss 'blanco'. |
| `l-b-n` | blanco, ladrillo | heb | levānāh | luna | high | La luna se llama 'la blanca' por su color; extensión metafórica directa del gloss 'blanco'. |
| `l-kh-m` | pan, luchar | ar | liḥām | soldadura | high | Soldadura une/combate materiales; extensión metafórica clara de 'luchar/unir' en el campo semántico de la raíz. |
| `l-kh-m` | pan, luchar | ar | mulāḥim | épica, narración heroica | high | Épica/narración heroica deriva directamente de 'luchar/batalla'; malāḥim son relatos de combates y guerras. |
| `l-sh-n` | lengua, idioma | heb | lēshīn | acusar, delatar | high | Acusar/delatar deriva metafóricamente de 'lengua' como instrumento de habla maliciosa o denuncia verbal; extensión semántica clara. |
| `l-w-y` | Leví, acompañar | ar | liwā' | estandarte, bandera | medium | Estandarte puede derivar de 'lo que acompaña/une' al grupo; símbolo que agrupa a seguidores. |
| `l-w-y` | Leví, acompañar | ar | lāwwā' | abanderado, estandarte | medium | Abanderado es agente de liwā' (estandarte); si liwā' conecta con acompañar, este también lo hace. |
| `m-l-l` | hablar, palabra | ar | malla | aburrirse/dictar | high | El significado 'dictar' está directamente conectado con 'hablar, palabra'; el sentido 'aburrirse' es secundario pero coexiste en la misma entrada. |
| `m-l-p` | enseñar | ar | 'allama | enseñar | high | Significa exactamente 'enseñar', idéntico al gloss de la raíz. |
| `m-l-p` | enseñar | ar | mu'allim | maestro | high | Derivación agentiva directa: 'el que enseña' = maestro, dentro del campo semántico. |
| `m-l-p` | enseñar | ar | mutaʿallim | estudiante, aprendiz | high | Forma reflexiva/pasiva de enseñar: 'el que recibe enseñanza' = estudiante. |
| `m-l-p` | enseñar | ar | maʿlūm | conocido, sabido | high | Participio pasivo: 'lo enseñado/transmitido' → 'conocido, sabido'; extensión natural. |
| `m-l-p` | enseñar | ar | taʿlīm | educación, instrucción | high | Sustantivo verbal de 'enseñar' = educación/instrucción, sinónimo directo del gloss. |
| `m-n-y` | contar, nombrar | ar | maniyyah | destino, sino | high | Destino como 'lo asignado/contado (por Dios)' es extensión directa de contar/designar. |
| `m-n-y` | contar, nombrar | ar | manūn | predestinado, designado | high | Predestinado/designado es sinónimo directo del gloss 'appoint/nombrar'. |
| `m-r-y` | señor, amo | ar | mar' | hombre/persona | medium | De 'señor/amo' a 'hombre/persona' hay puente semántico: el amo es un hombre libre, extensión metonímica común. |
| `m-r-y` | señor, amo | ar | imra'a | mujer | medium | Extensión femenina de mar' (hombre); si 'hombre' deriva de 'señor', 'mujer' es contraparte morfológica natural. |
| `m-r-y` | señor, amo | heb | mari | mi señor (arameo, no hebreo) | high | Significa exactamente 'mi señor', traducción directa del gloss; ser arameo no es divergencia semántica. |
| `m-r-y` | señor, amo | heb | maran | nuestro señor (arameo, no hebreo) | high | Significa 'nuestro señor', forma pronominal del gloss; el dialecto arameo no constituye divergencia semántica. |
| `m-sh-r` | campamento | heb | shārar | comandar, gobernar | high | Comandar/gobernar deriva del concepto de campamento militar: quien dirige el campamento manda las tropas. |
| `m-sh-r` | campamento | heb | shārīr | oficial, comandante | high | Oficial/comandante es extensión agentiva natural: el que está al mando del campamento militar. |
| `m-sh-r` | campamento | heb | shārōt | liderazgo, comando | high | Liderazgo/comando es extensión nominal abstracta del dominio de dirigir un campamento militar. |
| `m-t-y` | alcanzar, llegar | ar | maṭiyy | de larga distancia, alejado | high | 'Larga distancia/alejado' describe lo que se alcanza tras avanzar; extensión semántica natural de 'alcanzar, llegar'. |
| `m-t-y` | alcanzar, llegar | ar | maṭiyyah | montura, bestia de carga | high | La montura es el medio instrumental para llegar/alcanzar destinos; derivación nominal del concepto de 'llegar'. |
| `m-t-y` | alcanzar, llegar | heb | maṭṭeh | vara, bastón | high | Una vara/bastón es lo que se extiende (mata = extender); derivación instrumental directa del significado 'alcanzar/extender'. |
| `m-t-y` | alcanzar, llegar | heb | maṭṭā | hacia abajo, descendente | high | 'Hacia abajo' es la dirección del movimiento cuando algo se inclina/extiende; extensión espacial directa de 'alcanzar'. |
| `n-T-r` | guardar, vigilar | ar | nazara | mirar/observar | high | Mirar/observar es extensión natural de guardar/vigilar; vigilar requiere observar, desarrollo semántico común. |
| `n-T-r` | guardar, vigilar | ar | nazar | vista/mirada | high | Vista/mirada es nominalización de observar; guardar implica mantener la vista, puente claro. |
| `n-T-r` | guardar, vigilar | ar | manzar | vista/panorama | high | Vista/panorama deriva de observar; lo que se vigila se mira, extensión nominal locativa. |
| `n-T-r` | guardar, vigilar | ar | naẓir | observador | high | Observador es agentivo de observar/vigilar; quien guarda es quien observa, mismo campo semántico. |
| `n-T-r` | guardar, vigilar | ar | muntaẓir | vigilante | high | Vigilante significa exactamente guardián; restates el gloss directamente, no es outlier. |
| `n-T-r` | guardar, vigilar | ar | manẓar | vista, aspecto | high | Vista/aspecto deriva de observar; extensión nominal del acto de mirar/vigilar. |
| `n-b-a` | profetizar | ar | nab'un | noticia, información | high | 'Noticia/información' conecta con profetizar: el profeta comunica mensajes/noticias divinas. |
| `n-b-a` | profetizar | ar | inbāʾun | anuncio | high | 'Anuncio' es extensión natural de profetizar; profetizar es anunciar mensajes divinos. |
| `n-b-a` | profetizar | heb | n'vu'ah | profecía | high | Significa 'profecía', traducción directa del gloss 'profetizar'; duplicado de heb:2. |
| `n-b-a` | profetizar | heb | nib'ah | predicción | high | 'Predicción' es extensión directa de 'profetizar'; el profeta predice eventos futuros. |
| `n-g-d` | atraer, guiar | ar | najid | excelente, destacado | medium | Najid 'excelente' puede derivar de 'destacado/sobresaliente', extensión de quien guía o es atraído hacia adelante. |
| `n-kh-m` | consolar, consolación | ar | nahama | carraspear/gemir | medium | Gemir/groan se conecta con expresar dolor o pena, estado que precede a recibir consuelo; puente semántico plausible. |
| `n-kh-r` | extranjero, extraño | ar | nakīr | rechazo, negación | high | Rechazo/negación deriva de 'no reconocer' (nakira); negar algo es tratarlo como extraño o desconocido, extensión semántica clara. |
| `n-kh-r` | extranjero, extraño | ar | nikārah | extranjerismo | high | Extranjerismo es sinónimo directo del gloss 'extranjero, extraño'; no hay divergencia alguna. |
| `n-kh-sh` | cobre, serpiente | ar | naḥasa | pronosticar, adivinar | high | Mismo puente: 'serpiente' del gloss conecta con adivinación mediante observación de serpientes, extensión semántica atestiguada. |
| `n-kh-sh` | cobre, serpiente | heb | nāḥaš | adivinar, pronosticar | high | El gloss incluye 'serpiente'; la adivinación por serpientes (ofiomancia) es práctica antigua bien documentada, puente semántico claro. |
| `n-p-l` | caer | ar | infíllal | caer | high | Significa exactamente 'caer', idéntico al gloss de la raíz; etiqueta claramente errónea. |
| `n-p-q` | salir | ar | nafaqa | gastar | high | Gastar = hacer salir dinero/recursos; extensión metafórica directa de 'salir'. |
| `n-p-q` | salir | ar | nafaq | túnel | high | Túnel = lugar por donde se sale, extensión locativa/instrumental de 'salir'. |
| `n-p-q` | salir | heb | nafaq | salir (arameo bíblico) | high | Significa exactamente 'salir', igual que el gloss; ser arameo bíblico no es divergencia semántica. |
| `n-p-sh` | alma, ser | heb | nifšî | mi alma, mi ser | high | Es simplemente 'mi alma/mi ser' con sufijo posesivo; parafrasea directamente el gloss 'alma, ser'. |
| `n-s-b` | tomar | heb | nasav | tomar (arameo) | high | Significa exactamente 'tomar', que es el gloss de la raíz; el dialecto arameo no justifica marcar como outlier. |
| `n-s-b` | tomar | heb | n'siyyá | tentativa, ensayo | medium | Tentativa/ensayo deriva de 'tomar' como acción de emprender o intentar algo; extensión semántica plausible. |
| `n-sh-q` | besar | ar | manāshiq | orificios nasales | high | Orificios nasales es extensión locativa de inhalar/oler, significado atestiguado en árabe para esta raíz. |
| `n-ts-r` | Nazaret, guardar | ar | naṣr | victoria, ayuda | high | Victoria y ayuda derivan directamente de 'guardar/defender'; quien guarda/protege otorga victoria al protegido. |
| `n-ts-r` | Nazaret, guardar | ar | manṣūr | victorioso, triunfante | high | Victorioso es extensión participial de naṣara (ayudar/defender); el protegido resulta triunfante por la defensa recibida. |
| `p-l-g` | dividir, mitad | heb | pəlīgāh | escisión, disensión | high | Escisión y disensión son extensiones directas de 'dividir': una división en grupo o facción es semánticamente idéntica al gloss. |
| `p-l-kh` | trabajar, servir | ar | falāḥah | agricultura, labranza | high | Agricultura/labranza es extensión nominal directa de 'trabajar' — el trabajo agrícola es el sentido primario del trabajo semítico. |
| `p-q-d` | mandar, ordenar | ar | faqada | perder/echar de menos | high | Hebreo paqad incluye 'visitar/pasar revista'; quien visita nota la ausencia → 'perder/echar de menos' es extensión semántica documentada. |
| `p-q-d` | mandar, ordenar | ar | muftaqad | extrañado | high | Participio pasivo de 'echar de menos'; derivación regular del campo 'visitar/notar ausencia' presente en el hebreo. |
| `p-q-d` | mandar, ordenar | ar | faqid | el desaparecido, el fallecido | high | Adjetivo de 'perdido/ausente'; persona cuya ausencia se constata al pasar revista, extensión directa de paqad 'visitar/contar'. |
| `p-q-d` | mandar, ordenar | ar | faqadān | pérdida, ausencia | high | Sustantivo verbal de faqada; 'pérdida/ausencia' resulta de 'visitar y notar falta', puente semántico claro. |
| `p-q-d` | mandar, ordenar | ar | iftaqada | echar de menos, extrañar | high | Forma VIII reflexiva; 'extrañar' deriva de 'inspeccionar y notar ausencia', paralelo a tafaqqada 'inspeccionar'. |
| `p-r-q` | salvar, redimir | ar | furqan | diferencia, separación | medium | Furqan en contexto coránico significa salvación/criterio divino que separa verdad de falsedad, conectando con redención. |
| `p-r-s` | extender, desplegar | ar | farraqa | separar/dividir | high | Separar/dividir es extensión directa de 'extender/desplegar': lo extendido se separa en partes. |
| `p-r-s` | extender, desplegar | ar | farrrash | personal de limpieza | high | Farrāsh deriva de 'extender alfombras/ropa de cama'; agentivo de la acción de desplegar. |
| `p-r-sh` | separar, distinguir | ar | farasha | extender/esparcir | high | Extender/esparcir implica separar elementos distribuyéndolos; es extensión semántica natural del concepto de separar. |
| `p-r-sh` | separar, distinguir | ar | farsh | alfombra, tapete | high | Alfombra es objeto que se extiende/esparce; derivación nominal instrumental directa de 'extender', puente claro con 'separar'. |
| `p-r-sh` | separar, distinguir | ar | furshah | cepillo | medium | Cepillo tiene cerdas separadas/esparcidas; derivación instrumental plausible de la noción de separar/extender. |
| `p-s-q` | cortar, decidir | ar | infiṣāl | separación | high | infiṣāl (separación) es derivación directa de faṣala (separar), forma VII del mismo campo semántico del gloss. |
| `p-w-m` | boca | heb | piyyut | poema litúrgico | high | Piyyut deriva de 'boca' vía la poesía como expresión oral; el hebreo lo formó como 'composición de la boca'. |
| `q-d-m` | antes, frente, preceder | ar | taqdím | presentación, ofrecimiento | high | Presentar algo es 'ponerlo adelante/al frente'; taqdím es el sustantivo verbal de qaddama, extensión directa del gloss 'frente, preceder'. |
| `q-l-l` | ser ligero, veloz; maldecir | ar | qalíl | poco, escaso | high | 'Poco/escaso' deriva directamente de 'ser ligero' — lo que pesa poco es escaso en cantidad. |
| `q-l-s` | alabar, burlarse | ar | qals | burla, mofa | high | El gloss incluye explícitamente 'burlarse/mock'; 'burla/mofa' es el sustantivo derivado directo de ese significado. |
| `q-r-n` | cuerno, esquina | ar | qaran | emparejarse, juntarse | high | Emparejarse deriva de juntar dos cuernos o dos puntas; extensión semántica natural del concepto de cuerno/punta. |
| `q-r-n` | cuerno, esquina | ar | muqarran | cornudo, con cuernos | high | Significa literalmente 'con cuernos'; es derivación adjetival directa del gloso 'cuerno'. |
| `q-r-n` | cuerno, esquina | heb | karan | irradiar, brillar | high | Extensión metafórica documentada: los cuernos de Moisés 'irradiaban'; el cuerno como símbolo de rayos luminosos. |
| `q-r-n` | cuerno, esquina | heb | keren | rayo de luz, cuerno | high | Incluye explícitamente 'cuerno' en su definición y 'rayo de luz' es extensión metafórica directa del cuerno radiante. |
| `q-r-sh` | congelar, ser frío | heb | qarash | congelar | high | El significado 'congelar' es idéntico al gloss de la raíz; no hay divergencia alguna. |
| `q-sh-y` | duro, difícil | ar | qasāwah | dureza, crueldad | high | Crueldad es extensión metafórica natural de dureza/severidad; mismo campo semántico que el gloss 'duro, difícil'. |
| `q-w-m` | levantarse, pararse | ar | iqama | residencia | high | Residencia deriva de 'establecerse, quedarse en pie en un lugar'; extensión directa de levantarse/pararse. |
| `q-w-m` | levantarse, pararse | ar | quwaama | enderezar | high | Enderezar es causativo de 'estar de pie/recto'; extensión morfológica estándar del glosa. |
| `q-w-m` | levantarse, pararse | ar | istaqaama | estar recto | high | Estar recto es sinónimo directo de pararse erguido; no hay divergencia semántica alguna. |
| `q-y-m` | levantarse, estar de pie | ar | qayyim | supervisor, director | high | Supervisor es 'el que se mantiene de pie sobre algo', vigilando; extensión metafórica clara del glosa. |
| `q-y-m` | levantarse, estar de pie | heb | qiyum | existencia | high | Existencia deriva de 'mantenerse en pie' → 'persistir, existir'; extensión semántica estándar en semítico. |
| `q-y-m` | levantarse, estar de pie | heb | qomah | estatura, altura | high | Estatura/altura es literalmente 'lo que se levanta' o 'cuánto se eleva uno al estar de pie'; extensión directa. |
| `q-y-m` | levantarse, estar de pie | heb | haqamah | establecimiento, fundación | high | Establecer/fundar es causativo de 'levantar': hacer que algo se ponga en pie; derivación morfológica regular. |
| `r-b-a` | grande, rabí | ar | rabib | hijastro, criado | high | Rabib (hijastro/criado) deriva de rabba 'criar/educar'; quien es criado por otro, extensión agentiva directa del gloss. |
| `r-b-a` | grande, rabí | heb | ribbo | miríada | high | Miríada ('diez mil') deriva directamente del sentido de 'grande/gran cantidad'; extensión numérica natural del gloss. |
| `r-b-e` | cuatro | ar | rub' | cuarto | high | Cuarto es una cuarta parte, derivación fraccional directa del numeral cuatro. |
| `r-b-e` | cuatro | ar | ruba'i | cuadruple, cuaternario | high | Cuádruple/cuaternario significa relativo a cuatro, adjetivo derivado directamente del numeral. |
| `r-b-e` | cuatro | heb | rova' | cuarto, barrio | high | Un 'cuarto' (quarter) es una cuarta parte, derivación directa del numeral cuatro. |
| `r-b-e` | cuatro | heb | rabba'at | cuarteta | high | Cuarteta significa grupo de cuatro, extensión nominal directa del numeral cuatro. |
| `r-b-e` | cuatro | heb | ribu'a | cuadrado | high | Cuadrado deriva de cuatro lados iguales, extensión geométrica estándar del numeral. |
| `r-b-e` | cuatro | heb | merubba' | cuadrado, rectangular | high | Cuadrado/rectangular refiere a figura de cuatro lados, derivación geométrica del numeral. |
| `r-b-y` | grande, mucho, rabí | ar | rabīb | hijastro, entenado | high | Rabīb deriva de rabbā (criar/educar); el hijastro es 'el criado/educado', extensión semántica directa del concepto de criar. |
| `r-d-p` | perseguir | ar | radaf | parte trasera, retaguardia | high | La retaguardia es lo que sigue detrás; extensión espacial directa de 'seguir/perseguir'. |
| `r-d-y` | viajar, caminar | ar | rada | perecer; ir | high | El significado 'ir' está explícito y es sinónimo directo del glosa 'viajar, caminar'. |
| `r-e-n` | pensamiento, mente | heb | rə'ut | voluntad, deseo | high | Voluntad/deseo es extensión natural de pensamiento/mente: lo que la mente quiere o intenciona. |
| `r-e-y` | pastorear, apacentar | ar | mar'ā | pasto, pradera | high | Pasto/pradera es el sustantivo locativo estándar de 'pastorear'; derivación morfológica regular, no divergencia. |
| `r-e-y` | pastorear, apacentar | heb | mar'eh | pastizal, pradera | high | Pastizal/pradera es el lugar donde se pastorea; extensión locativa directa del gloss 'pastorear'. |
| `r-g-l` | pie | ar | rajūl | viril | high | De 'pie' a 'hombre (que camina)' a 'viril/masculino' es extensión semántica directa atestiguada en árabe (rijāl = hombres). |
| `r-g-l` | pie | ar | rajjala | ir a pie | high | Significa exactamente 'ir a pie', derivación verbal directa del sustantivo 'pie'; no hay divergencia alguna. |
| `r-g-z` | ira, enojo | ar | rajaza | temblar/recitar | high | Temblar es manifestación física de ira/agitación, paralelo exacto al hebreo ragaz; recitar es extensión secundaria. |
| `r-g-z` | ira, enojo | ar | rajíz | furioso, airado | high | Furioso/airado es sinónimo directo del gloss ira/enojo; no hay divergencia semántica alguna. |
| `r-kh-q` | estar lejos | ar | rahiq | néctar (vino raro/lejano) | medium | El néctar/vino raro se llama así por ser 'lejano' o difícil de obtener; extensión metafórica de rareza/distancia. |
| `r-sh-y` | malvado | ar | rašāwah | soborno | high | Soborno es forma concreta de maldad/acto malvado; extensión semántica clara del concepto de conducta perversa. |
| `r-sh-y` | malvado | ar | riŝwah | soborno | high | Soborno representa un acto moralmente malo; conexión directa con 'malvado' como comportamiento corrupto y perverso. |
| `r-w-kh` | espíritu, viento | ar | raha | descanso/comodidad | high | Extensión semántica clara: viento/respirar → alivio → descanso/comodidad; mismo desarrollo en hebreo hitravea(ḥ). |
| `r-w-kh` | espíritu, viento | ar | rāwaḥa | descansar, tener reposo | high | Mismo puente que ar:2: respirar/tomar aire → descansar; paralelo exacto con hebreo hitravea(ḥ) en la familia. |
| `r-y-m` | ser alto, exaltar | ar | rammah | montaña, collina | high | Montaña/colina es extensión directa de 'ser alto'; lugar elevado pertenece al campo semántico del glosa. |
| `r-y-sh` | cabeza, jefe | heb | rē'shît | comienzo, principio | high | «Comienzo» deriva directamente de «cabeza» como parte inicial o primera de algo; extensión metafórica estándar. |
| `s-b-r` | esperar, predicar | heb | savar | pensar/suponer | high | Pensar/suponer es extensión natural de esperar: esperar implica formar expectativas mentales, suponer algo futuro. |
| `s-e-r` | hacer, visitar, cabello | ar | suʿarāʾ | poetas | medium | Shiʿr (poesía) deriva de shaʿara 'percibir/sentir'; relacionado con raíz S-ʿ-R aunque glosa no lo refleja bien. |
| `s-g-a` | ser muchos, crecer | ar | sajjā | cubrir, extenderse | medium | Extenderse es desarrollo natural de crecer; lo que crece se extiende y cubre espacio. |
| `s-g-a` | ser muchos, crecer | ar | istījāʾ | abundancia, riqueza | high | Abundancia y riqueza son sinónimos directos de 'ser muchos'; no hay divergencia semántica. |
| `s-h-d` | testificar, mártir | ar | mashhad | escena/lugar de martirio | high | Mashhad es derivación locativa regular: 'lugar de testimonio/martirio', extensión directa del gloss 'testificar, mártir'. |
| `s-k-l` | ser necio, insensato | ar | sakkala | engañar | high | Engañar (deceive) se vincula semánticamente con 'necio': hacer actuar neciamente a otro o aprovecharse de su insensatez. |
| `s-k-l` | ser necio, insensato | ar | sukkāl | tonto | high | Sukkāl significa 'persona necia/tonta', que es exactamente el gloss de la raíz; no hay divergencia alguna. |
| `s-k-n` | habitar, peligro | ar | sakīna | tranquilidad, presencia divina | high | Sakīna deriva de 'calmarse/habitar'; la tranquilidad es el estado de estar asentado, y la presencia divina es paralelo semántico exacto al hebreo shekhinah. |
| `s-k-n` | habitar, peligro | heb | shekhinah | presencia divina | high | Shekhinah es literalmente 'morada/presencia que habita'; extensión nominal directa de 'habitar' aplicada a la presencia divina que mora entre el pueblo. |
| `s-n-q` | necesitar | ar | ḥājah | necesidad | high | "Necesidad" es el sustantivo directo del verbo "necesitar"; es la forma nominal básica del gloss, no divergencia. |
| `s-r-q` | vacío, vano | ar | saraqa | robar (vaciar) | high | Robar como 'vaciar' un lugar de sus bienes es extensión metafórica clara del concepto de vacío. |
| `s-r-q` | vacío, vano | ar | sarāqah | robo, hurto | high | Nominal derivado de 'robar/vaciar'; el puente semántico vacío→robo está establecido en ar:0. |
| `s-r-q` | vacío, vano | ar | surqah | hurto, robo | high | Sinónimo de sarāqah, mismo puente: robo implica dejar vacío, extensión metonímica válida. |
| `s-r-q` | vacío, vano | ar | isrāq | saqueo, despojo | high | Saqueo/despojo es intensificación de robar; vaciar completamente un lugar, extensión directa del gloss. |
| `s-y-r` | esperar, tener esperanza | ar | maṣbūr | paciente, que tiene paciencia | high | Participio pasivo de ṣabara 'ser paciente'; paciencia es extensión directa de esperar. |
| `sh-a-d` | demonio | ar | shad | opresión, tiranía | high | Opresión y tiranía son características asociadas a demonios y fuerzas malignas; extensión directa del campo semántico demoníaco. |
| `sh-a-d` | demonio | heb | shadad | destruir, devastar | high | Demonios causan destrucción y devastación; extensión semántica natural del campo 'demonio' hacia sus acciones destructivas. |
| `sh-a-l` | preguntar, pedir | ar | mas'ala | cuestión/asunto | high | Mas'ala es 'cosa preguntada/solicitada', extensión nominal directa de 'preguntar' → asunto, cuestión. |
| `sh-a-l` | preguntar, pedir | ar | mas'ul | responsable | high | Mas'ul significa 'aquel a quien se pregunta/pide cuentas', extensión pasiva directa de 'preguntar'. |
| `sh-a-l` | preguntar, pedir | heb | Shaul | Saúl (pedido) | high | Nombre propio que literalmente significa 'pedido/solicitado', participio pasivo de la raíz 'pedir'. |
| `sh-a-l` | preguntar, pedir | heb | mash'il | el que presta | high | Prestar es extensión semántica: quien presta responde a una petición; forma causativa/derivada de 'pedir'. |
| `sh-b-th` | sábado, descansar | ar | subat | letargo/sueño profundo | high | Letargo/sueño profundo es extensión directa de descansar: estado de reposo extremo o inactividad. |
| `sh-b-th` | sábado, descansar | ar | masbūt | paralizado, inactivo | high | Paralizado/inactivo es extensión semántica de cesar/descansar: estado de completa inactividad. |
| `sh-d-r` | enviar | ar | masdar | fuente/infinitivo | high | 'Fuente' es el punto de donde algo es enviado/emitido; extensión metafórica clara del acto de enviar. |
| `sh-d-r` | enviar | ar | maṣdar | fuente, origen | high | Duplicado de ar:1; 'fuente, origen' deriva metafóricamente de 'lugar desde donde se envía/emana'. |
| `sh-d-r` | enviar | heb | shadar | enviar (arameo) | high | Significa exactamente 'enviar', igual que el gloss; ser arameo no lo hace divergente. |
| `sh-d-r` | enviar | heb | sho'leiach | el que envía | high | 'El que envía' es derivación agentiva directa de 'enviar'; no hay divergencia semántica. |
| `sh-d-r` | enviar | heb | shilú'ach | envío, despacho | high | 'Envío, despacho' es el sustantivo verbal de 'enviar'; extensión nominal estándar. |
| `sh-kh-n` | habitar (Shekiná) | ar | sukun | quietud | high | La quietud es extensión semántica natural de habitar: asentarse implica calma y reposo, como muestra ar:0 'habitar/calmarse'. |
| `sh-l-t` | gobernar, dominar | heb | shelet | letrero/escudo | medium | El escudo es símbolo de poder/autoridad del gobernante; el letrero es objeto que ejerce control sobre el espacio público. |
| `sh-m-e` | oír, escuchar | heb | mishma | significado | high | Extensión semántica clara: lo que se oye/escucha implica lo que se entiende, de ahí 'significado/implicación'. |
| `sh-m-e` | oír, escuchar | heb | nish'má | sonar, resonar | high | Nif'al pasivo de 'oír': 'ser oído' equivale a 'sonar/resonar'; derivación morfológica estándar del gloss. |
| `sh-p-r` | ser bello, trompeta (shofar) | ar | sur | Tiro (cuerno) | medium | Tiro se asocia con cuerno/trompeta en la glosa; la nota '(cuerno)' indica conexión con shofar. |
| `sh-p-r` | ser bello, trompeta (shofar) | ar | tasfeer | silbar | high | Silbar es extensión natural de trompeta/shofar; ambos producen sonido soplando aire. |
| `sh-r-a` | comenzar, soltar | heb | shriirut | arbitrariedad | medium | De 'soltar' → 'sin restricción' → 'actuar a voluntad propia' → 'arbitrariedad'; extensión semántica plausible. |
| `sh-r-y` | comenzar, habitar, soltar | ar | mashra' | punto de partida, fuente | high | Punto de partida y fuente son extensiones directas del significado 'comenzar' presente en el gloss. |
| `sh-r-y` | comenzar, habitar, soltar | heb | mishrah | jurisdicción, autoridad | medium | Jurisdicción/autoridad puede derivar de 'habitar' → dominio territorial, o de 'comenzar' → fundamento de gobierno. |
| `sh-w-q` | calle, mercado | ar | suq | mercado | high | Significa 'mercado', traducción directa del gloss de la raíz. |
| `sh-w-q` | calle, mercado | heb | shuq | mercado, calle | high | Significa exactamente 'mercado, calle', idéntico al gloss de la raíz. |
| `t-e-n` | cargar, llevar | ar | ṭāʿūn | peste | high | La peste 'apuñala' o ataca al cuerpo; extensión metafórica de 'apuñalar' como enfermedad que hiere/penetra. |
| `t-e-n` | cargar, llevar | ar | ṭāʿin | atacante, crítico | high | Participio activo de ṭaʿana 'apuñalar'; 'atacante/crítico' es quien ataca literal o verbalmente, extensión directa. |
| `th-r-e` | puerta, portón | ar | darb | camino/puerta | high | Incluye explícitamente 'puerta' en su definición; 'camino' es extensión natural de paso/entrada. |
| `th-r-e` | puerta, portón | ar | matrūk | dejado abierto (como una puerta) | high | Significa 'dejado abierto como una puerta', estado directamente relacionado con puertas. |
| `th-r-e` | puerta, portón | heb | tar'a | puerta (arameo) | high | Significa 'puerta' en arameo, traducción directa del gloss; dialecto hermano no es divergencia. |
| `th-r-e` | puerta, portón | heb | tar'il | puerta grande | high | Significa 'puerta grande', extensión directa del gloss 'puerta, portón'. |
| `th-r-e` | puerta, portón | heb | t'riya | acto de abrir una puerta | high | Significa 'acto de abrir una puerta', derivación verbal directa del campo semántico de puerta. |
| `th-r-e` | puerta, portón | heb | tarpef | umbral de puerta | high | Significa 'umbral de puerta', parte constitutiva de una puerta, mismo campo semántico. |
| `th-r-ts` | enderezar, corregir | ar | turs | escudo | medium | Escudo como 'lo firme/sólido' conecta con enderezar; objeto que mantiene recto/firme al guerrero. |
| `ts-b-n` | voluntad, deseo | heb | khafiytsa | apetencia, ansia | high | Apetencia/ansia es extensión directa de voluntad/deseo; el anhelo intenso pertenece al mismo campo semántico. |
| `ts-e-r` | despreciar, pequeño | ar | istighār | menosprecio, desdén | high | El gloss incluye 'despreciar'; 'menosprecio/desdén' es exactamente ese significado, no hay divergencia semántica. |
| `ts-l-y` | orar, crucificar | heb | mits'lé'a | rejilla, parrilla | medium | Una parrilla/rejilla conecta con crucifixión por la estructura de barras cruzadas; extensión instrumental plausible. |
| `y-b-l` | traer, llevar | heb | yovel | año del jubileo | high | Yovel deriva del cuerno de carnero que 'lleva/porta' el sonido proclamando el jubileo; extensión instrumental clara. |
| `y-h-b` | dar | ar | wahīb | generoso | high | Generoso es quien da; extensión agentiva directa del significado 'dar'. |
| `y-h-b` | dar | ar | mawḥūb | talentoso/dotado | high | Talentoso/dotado = 'a quien se le ha dado'; participio pasivo de 'dar', extensión clara. |
| `y-l-d` | dar a luz, nacer | heb | moledet | patria | high | Patria/homeland deriva de 'lugar de nacimiento'; extensión locativa directa de 'nacer' — puente semántico claro. |
| `y-l-p` | aprender | heb | mul'mad | erudito, docto | high | Erudito/docto es resultado directo de aprender; participio pasivo causativo del verbo 'aprender'. |
| `y-m-m` | mar, día | heb | yammah | hacia el mar | high | Es extensión directiva/locativa de 'mar': 'hacia el mar' deriva directamente del gloss 'mar'. |
| `y-r-kh` | mes | heb | leyarêkha | menstruar | high | Menstruar deriva directamente de 'mes' por el ciclo mensual; extensión semántica natural y universal. |
| `y-th-b` | sentarse, habitar | ar | wādib | constante, perseverante | medium | Constante/perseverante se deriva de permanecer sentado o establecido; extensión figurativa de habitar. |
| `y-th-b` | sentarse, habitar | ar | mawḍib | que permanece en su sitio | high | Que permanece en su sitio es paráfrasis directa del concepto de sentarse/habitar en un lugar. |
| `y-w-m` | día | ar | yawm al-qiyama | Día del Juicio | high | Es literalmente 'día de la resurrección'; yawm significa día, el compuesto pertenece directamente al campo semántico del gloss. |
| `z-b-n` | tiempo, comprar | ar | zabun | cliente | high | Cliente deriva de 'comprar'; el cliente es quien compra, extensión agentiva directa del glosa. |
| `z-b-n` | tiempo, comprar | ar | zabā'in | clientes, compradores | high | Plural de cliente/comprador; extensión agentiva directa del significado 'comprar' en el glosa. |
| `z-b-n` | tiempo, comprar | ar | zabīn | cliente, comprador | high | Cliente/comprador es derivación agentiva directa de 'comprar', uno de los significados del glosa. |
| `z-b-n` | tiempo, comprar | heb | zimmen | invitar/preparar | high | Invitar/preparar deriva de fijar un tiempo; relacionado semánticamente con 'tiempo' mediante programación temporal. |
| `z-b-n` | tiempo, comprar | heb | zīmūn | preparación, cita | high | Preparación y cita son extensiones directas del concepto de tiempo; una cita es un momento fijado. |
| `z-b-n` | tiempo, comprar | heb | zōmēn | invitar, organizar | high | Invitar y organizar implican fijar un tiempo para algo; extensión natural del glosa 'tiempo'. |
| `z-b-n` | tiempo, comprar | heb | zimnūt | temporalidad, carácter temporal | high | Temporalidad es literalmente la cualidad abstracta de 'tiempo'; parafrasea directamente el glosa. |
| `z-m-n` | tiempo, invitar | heb | zimún | invitación, convocatoria | high | El gloss incluye 'invitar'; 'invitación, convocatoria' es el sustantivo derivado directo de ese significado. |
| `z-y-n` | arma | ar | zayān | daño, perjuicio | medium | Daño/perjuicio conecta con arma: las armas causan daño, extensión semántica natural por metonimia. |

## Flags confirmados (outliers genuinos)

280 entradas. Sin cambios.

| Raíz | Gloss (es) | Lang | Translit | Significado | Conf. | Justificación |
|---|---|---|---|---|---|---|
| `T-l-y` | niño, joven | ar | talā | seguir, recitar | high | talā (seguir, recitar) no tiene puente semántico con 'niño/joven'; es raíz homónima T-L-W distinta de T-L-Y. |
| `T-w-b` | bueno, bienaventurado | ar | ṭawb | ladrillo, bloque | high | Ladrillo/bloque no tiene puente semántico con bueno/bienaventurado; probablemente raíz homónima. |
| `a-b-d` | perecer, destruir | ar | abada | eternidad (cognado semántico) | medium | أَبَدَ 'eternidad' es raíz homónima distinta (ʾ-b-d II); no hay puente claro entre 'perecer' y 'eternidad'. |
| `a-b-d` | perecer, destruir | ar | ʿabad | adorar, rendir culto | high | عَبَد (ʿ-b-d) con ʿayn inicial es raíz diferente ('servir/adorar'), no cognado de ʾ-b-d ('perecer'). |
| `a-b-d` | perecer, destruir | ar | ʿābid | adorador, devoto | high | عَابِد deriva de ʿ-b-d ('adorar'), raíz distinta con ʿayn; no relacionada semánticamente con 'perecer'. |
| `a-b-d` | perecer, destruir | ar | ʿabūd | sometido, sujeto | high | عَبُود pertenece a ʿ-b-d ('someter/servir'), raíz diferente fonológicamente de ʾ-b-d ('perecer'). |
| `a-r-z` | misterio | ar | arz | cedro | high | Cedro es un árbol; no hay puente semántico con misterio. Raíz homónima distinta (cf. heb:0 también cedro). |
| `a-th-r` | lugar, tierra | ar | ʾāthara | preferir, elegir | medium | Preferir/elegir no tiene puente claro con lugar/tierra; probablemente raíz homónima árabe. |
| `a-y-d` | mano | heb | yadid | querido, amado | high | Yadid deriva de raíz Y-D-D (amar), no de Y-D (mano); homofonía parcial pero raíces distintas. |
| `a-y-d` | mano | heb | y'didut | amistad, fraternidad | high | Y'didut es derivado de Y-D-D (amistad/amor), raíz separada de Y-D (mano); sin puente semántico. |
| `a-y-d` | mano | heb | yadua | conocido, famoso | high | Yadua deriva de Y-D-ʿ (conocer), raíz completamente distinta de Y-D/ʾ-Y-D (mano). |
| `a-y-l` | árbol, poder | heb | eleh | estos | high | Pronombre demostrativo 'estos' sin conexión semántica con árbol o poder; raíz homónima diferente. |
| `a-y-n` | dónde, ojo | ar | 'âwana | ayudar, colaborar | high | ʿāwana 'ayudar' pertenece a raíz ʿ-W-N, no guarda relación semántica con 'ojo' o 'dónde'. |
| `a-y-n` | dónde, ojo | heb | 'ânâh | responder, contestar | high | ʿānâh 'responder' deriva de raíz ʿ-N-Y, no de ʿ-Y-N 'ojo/dónde'; sin puente semántico plausible. |
| `a-z-l` | ir | ar | 'iyyāl | ciervo | high | Ciervo no tiene puente semántico claro con 'ir'; probablemente raíz homónima distinta (ʔ-y-l). |
| `b-T-l` | cesar, estar ocioso | ar | batal | héroe/nulo | medium | El sentido 'héroe' no deriva de 'cesar/ocioso'; probablemente raíz homónima fusionada. El sentido 'nulo' sí conecta. |
| `b-r-a` | crear, hijo | heb | barur | claro, puro | medium | Barur deriva de B-R-R (purificar/seleccionar), raíz distinta de B-R-A (crear); no hay puente semántico claro. |
| `b-r-y` | crear, hijo | heb | barūr | claro, puro | medium | Barūr 'claro, puro' deriva de raíz B-R-R (purificar), no de B-R-' (crear) ni de relación filial; sin puente semántico claro. |
| `b-s-r` | carne | ar | bišārah | buena noticia | medium | Igual que heb:2, 'buena noticia' deriva de raíz homónima B-Š-R 'anunciar', distinta semánticamente de 'carne'. |
| `b-s-r` | carne | heb | bissûr | anuncio, noticia | medium | Significado 'anuncio/noticia' no conecta claramente con 'carne'; posible raíz homónima B-Ś-R II 'anunciar'. |
| `d-g-l` | mentir, engañar | heb | degel | bandera, estandarte | high | Bandera/estandarte no tiene puente semántico plausible con mentir/engañar; probable raíz homónima D-G-L distinta. |
| `d-kh-l` | temer | ar | dakhala | entrar | high | 'Entrar' no tiene puente semántico con 'temer'; son raíces homófonas distintas en árabe. |
| `d-kh-l` | temer | ar | dukhul | entrada | high | 'Entrada' deriva de 'entrar', sin conexión semántica con 'temer'; misma raíz homófona diferente. |
| `d-m-r` | sorprenderse, admirarse | ar | damara | destruir, arruinar | medium | Destruir/arruinar no tiene puente semántico claro con sorprenderse/admirarse; probablemente raíz homónima. |
| `d-m-r` | sorprenderse, admirarse | ar | damirah | estar destruido, arruinado | medium | Estar destruido es extensión pasiva de ar:0; misma divergencia semántica sin puente a admirarse. |
| `d-m-r` | sorprenderse, admirarse | ar | madmúr | destruido, arruinado | medium | Participio pasivo de damara (destruir); pertenece al campo de destrucción, no de asombro. |
| `d-m-y` | asemejar, imagen | ar | damiya | sangrar; asemejarse | high | El significado 'sangrar' pertenece a otra raíz D-M-Y (sangre/dam); es homonimia, no extensión semántica de 'asemejar'. |
| `d-n-kh` | brillar, amanecer | ar | nāḥa | lamentarse, quejarse | high | Lamentarse no tiene puente semántico con brillar o amanecer; parece raíz homónima distinta. |
| `d-n-kh` | brillar, amanecer | ar | nadā | rocío, humedad | high | Rocío/humedad carece de conexión semántica con brillar o amanecer; raíz distinta o metátesis no semánticamente relacionada. |
| `e-b-r` | pasar, cruzar | ar | ʿibra | aguja, lección | medium | El significado 'aguja' (إِبْرَة) pertenece a otra raíz (أ-ب-ر); posible confusión por homofonía parcial. |
| `e-d-l` | reprender, culpar | ar | ʿadala | ser justo | high | Ser justo no tiene puente semántico claro con reprender/culpar; raíz homónima ع-د-ل distinta de ع-د-ل 'censurar'. |
| `e-d-l` | reprender, culpar | ar | ʿadl | justicia, equidad | high | Justicia/equidad pertenece a raíz ع-د-ل 'equilibrar', no a la raíz siríaca 'reprender'; sin puente semántico. |
| `e-d-l` | reprender, culpar | ar | ʿādil | justo, equitativo | high | Justo/equitativo deriva de 'ser justo', raíz homónima sin conexión con reprender o culpar. |
| `e-d-r` | ayudar | ar | 'adhara | excusar | medium | Excusar implica exonerar de culpa, no ayudar activamente; el puente semántico es tenue aunque posible vía 'defender'. |
| `e-d-r` | ayudar | ar | 'udhr | excusa | medium | Excusa como sustantivo se aleja del sentido de ayuda activa; posible conexión vía 'justificación' pero débil. |
| `e-d-th` | iglesia, asamblea | ar | 'āda | costumbre | medium | Costumbre/hábito deriva de raíz ʕ-W-D (volver, repetir), no de ʕ-D-T (asamblea); raíces homónimas distintas. |
| `e-d-th` | iglesia, asamblea | ar | 'awda | regreso, vuelta | high | Regreso/vuelta pertenece a raíz ʕ-W-D (retornar), diferente semánticamente de asamblea/iglesia; sin puente claro. |
| `e-d-th` | iglesia, asamblea | ar | ta'wīd | acostumbramiento, habituación | high | Habituación deriva de ʕ-W-D (repetir/acostumbrar), raíz distinta de ʕ-D-T (asamblea); no hay conexión semántica. |
| `e-g-l` | becerro, apresurarse | heb | 'iggul | círculo, redondo | medium | El sentido 'círculo/redondo' parece derivar de raíz homónima ע-ג-ל relacionada con rodar, sin puente claro a 'becerro' o 'apresurarse'. |
| `e-l-l` | entrar | ar | 'illa | causa/enfermedad | high | El significado 'enfermedad/causa' no tiene conexión semántica evidente con 'entrar'; raíz árabe probablemente distinta. |
| `e-l-l` | entrar | ar | 'illah | causa, razón | high | Igual que ar:1, 'causa/razón' carece de puente semántico con 'entrar'; raíz homónima en árabe. |
| `e-l-l` | entrar | heb | 'olal | niño pequeño | medium | No hay puente semántico claro entre 'entrar' y 'niño pequeño'; posible raíz homónima o extensión muy oscura. |
| `e-l-m` | mundo, eternidad | heb | 'alem | ocultar, esconder | medium | ʿ-L-M 'esconder' es probablemente raíz homónima distinta de 'mundo/eternidad'; sin puente semántico claro entre ocultar y eternidad/mundo. |
| `e-l-th` | causa, razón | heb | 'āliyl | acto, hecho, hazaña | medium | Significa 'acto, hazaña' sin conexión clara con 'causa/razón'; posible raíz homónima E-L-L (hacer). |
| `e-m-r` | habitar, morar | heb | 'amar | amontonar gavillas | high | Amontonar gavillas no tiene puente semántico claro con 'habitar/morar'; probable raíz homónima ע-מ-ר. |
| `e-m-r` | habitar, morar | heb | 'omer | gavilla/medida | high | Gavilla/medida de grano no se conecta con habitar; raíz homónima distinta en hebreo. |
| `e-m-r` | habitar, morar | heb | ma'amar | gavilla | high | Gavilla pertenece al campo agrícola, sin puente a habitar/morar; raíz homónima. |
| `e-m-r` | habitar, morar | heb | 'āmīr | gavilla, haz | high | Gavilla/haz es término agrícola sin conexión semántica con habitar; homónimo. |
| `e-n-a` | responder | ar | 'anatul | paciencia | medium | Paciencia (أناة) probablemente de raíz distinta أ-ن-ي; sin vínculo semántico evidente con responder. |
| `e-n-a` | responder | ar | 'ina'un | recipiente | high | Recipiente (إناء) es de raíz diferente أ-ن-ي/و-ع-ي; sin conexión semántica con responder. |
| `e-n-a` | responder | heb | 'anayah | pobreza | medium | Pobreza deriva de otra raíz ע-נ-י (afligir/oprimir), no de responder; sin puente semántico claro. |
| `e-n-y` | responder | ar | taʿānin | sufrimiento, penuria | medium | Sufrimiento/penuria deriva de عَنِيَ (sufrir), raíz homónima distinta de 'responder'; sin puente semántico claro. |
| `e-n-y` | responder | heb | 'ăniyyût | modestia, humildad | medium | Humildad proviene de raíz ע-נ-ה II (afligir/humillar), distinta semánticamente de responder; posible homónimo. |
| `e-r-q` | huir | ar | 'irq | vena/raíz | high | Vena/raíz no tiene puente semántico claro con 'huir'; probablemente raíz homónima árabe distinta. |
| `e-r-q` | huir | ar | ma'raq | lugar de sudor | high | Lugar de sudor deriva del campo semántico 'sudar', no de 'huir'; raíz árabe homónima diferente. |
| `e-r-s` | cama, lecho | ar | ʿarīsh | emparrado, enramada | medium | Emparrado/enramada es estructura de ramas para plantas; no hay puente claro con cama/lecho como mueble para dormir. |
| `e-sh-n` | ser fuerte | heb | 'ashan | humo | high | Humo no tiene puente semántico plausible con 'ser fuerte'; probable raíz homónima hebraica distinta. |
| `e-sh-n` | ser fuerte | heb | 'ashen | humear | high | Humear es acción relacionada con humo, no con fuerza; sin conexión etimológica clara al gloss. |
| `e-th-r` | rico | ar | 'athará | tropezar, caer | high | Tropezar/caer no tiene puente semántico con 'rico'; probablemente raíces homónimas que convergieron en forma. |
| `e-th-r` | rico | ar | 'ithārah | tropiezo, obstáculo | high | Tropiezo/obstáculo carece de conexión semántica con riqueza; sin extensión metafórica plausible. |
| `e-th-r` | rico | ar | mu'tathir | que tropieza, que se cae | high | Quien tropieza no tiene relación semántica con rico; derivado de raíz homónima distinta. |
| `e-y-r` | vigilar, despertar | ar | ʿayr | asno, burro | high | Asno/burro no tiene puente semántico claro con vigilar o despertar; probablemente raíz homónima. |
| `e-y-r` | vigilar, despertar | ar | ʿayyara | reprender, criticar | medium | Reprender/criticar carece de conexión evidente con vigilar/despertar; posible raíz homónima ع-ي-ر. |
| `g-b-a` | elegir, escoger | ar | jabā | recaudar, reunir | medium | Recaudar/reunir (collect/gather) carece de puente claro con elegir/escoger; probablemente raíces homónimas G-B-Y vs G-B-'. |
| `g-b-a` | elegir, escoger | ar | jābī | recaudador, cobrador | medium | Derivado de jabā (recaudar); recaudador no tiene conexión semántica evidente con elegir/escoger. |
| `g-b-a` | elegir, escoger | ar | majbī | recaudador de impuestos | medium | Recaudador de impuestos deriva de jabā (recaudar), sin puente semántico hacia elegir/escoger. |
| `g-b-y` | elegir, escoger | heb | gavah | alzar(se), elevarse | high | Significa 'alzarse, elevarse' sin conexión semántica con 'elegir, escoger'; probablemente raíz homónima G-B-H. |
| `g-l-l` | rodar, Galilea | ar | jalla | ser grande/majestuoso | high | Ser grande/majestuoso no tiene puente semántico claro con rodar; probablemente raíz homónima árabe J-L-L distinta. |
| `g-l-l` | rodar, Galilea | ar | ijlal | veneración | high | Veneración deriva de la raíz árabe de grandeza/majestad, no del concepto de rodar; sin puente plausible. |
| `g-l-l` | rodar, Galilea | ar | jalāl | grandeza, majestad | high | Grandeza/majestad pertenece al campo semántico de J-L-L árabe (ser grande), sin conexión con rodar. |
| `g-l-l` | rodar, Galilea | ar | jalīl | magnífico, ilustre | high | Magnífico/ilustre deriva de grandeza, no de rodar; raíz homónima sin desarrollo semántico compartido. |
| `g-m-l` | camello, retribuir | ar | tajammala | arreglarse, embellecerse | high | Deriva de raíz homónima ج-م-ل 'belleza' (jamīl), no de 'camello' ni 'retribuir'; sin puente semántico. |
| `g-m-l` | camello, retribuir | ar | jammala | embellecer, adornar | high | Pertenece a raíz homónima ج-م-ل 'belleza', distinta de 'camello/retribuir'; divergencia genuina. |
| `g-m-r` | completar, terminar | ar | jamara | reunir brasas | high | Reunir brasas no tiene puente semántico claro con completar/terminar; probablemente raíz homónima. |
| `g-m-r` | completar, terminar | ar | jamr | brasas | high | Brasas como sustantivo no se conecta con el campo semántico de completar; raíz homónima árabe. |
| `g-m-r` | completar, terminar | ar | jummar | piedras (ritual) | high | Piedras rituales (jamarat del Hajj) no tienen conexión semántica con completar/terminar. |
| `g-m-r` | completar, terminar | ar | jamarah | reunir brasas | high | Duplicado de ar:0; reunir brasas no se conecta con completar/terminar. |
| `g-n-b` | robar | ar | janaba | evitar/apartar | high | Árabe ج-ن-ب 'evitar/apartar' es raíz homónima distinta; no hay puente semántico con 'robar'. |
| `g-n-b` | robar | ar | janib | lado | high | 'Lado' deriva de ج-ن-ب 'estar al lado/evitar', raíz homónima sin conexión semántica con 'robar'. |
| `g-n-b` | robar | ar | ijtanaba | evitar | high | Forma VIII de ج-ن-ب 'evitar'; raíz árabe distinta de la hebrea גנב 'robar', sin puente plausible. |
| `g-n-y` | jardín | ar | janān | corazón, interior | medium | Corazón/interior no tiene puente semántico claro con jardín; probablemente raíz homónima G-N-N 'cubrir/ocultar'. |
| `g-r-sh` | expulsar, divorciar | ar | jarsh | desmenuzar | high | Desmenuzar (triturar) no tiene puente semántico claro con expulsar/divorciar; posible raíz homónima. |
| `g-r-sh` | expulsar, divorciar | ar | jarash | desmoronar | high | Desmoronar tampoco conecta con expulsar/divorciar; mismo problema de homonimia con ar:0. |
| `g-r-sh` | expulsar, divorciar | ar | tard | expulsión | high | Tard (ط-ر-د) tiene radicales distintos de G-R-SH; no es cognado, es sinónimo de otra raíz. |
| `h-l-k` | caminar, ir | ar | halaka | perecer | high | هَلَكَ 'perecer' carece de puente semántico claro con 'caminar, ir'; probablemente raíz homónima distinta. |
| `h-w-a` | ser, estar | ar | hawā | caer, descender | high | hawā 'caer' deriva de raíz H-W-Y distinta; no hay puente semántico con 'ser/estar'. |
| `k-a-p` | roca, piedra | ar | kāhin | sacerdote, adivino | high | Kāhin (sacerdote/adivino) no tiene puente semántico con roca/piedra; probablemente raíz homónima K-H-N. |
| `k-a-p` | roca, piedra | ar | kūfah | ciudad en Irak | medium | Nombre propio de ciudad sin conexión semántica clara con roca/piedra; etimología disputada, sin puente evidente. |
| `k-m-r` | sacerdote pagano | ar | kamara | cubrir, ocultar | high | Cubrir/ocultar no tiene relación semántica demostrable con 'sacerdote pagano'; raíz homónima distinta. |
| `k-m-r` | sacerdote pagano | ar | kammara | cubrir, ocultar | high | Forma intensiva de 'cubrir'; mismo caso que ar:0, sin puente al significado de sacerdote. |
| `k-m-r` | sacerdote pagano | ar | kumrah | capota, cubierta | high | Capota/cubierta deriva del campo semántico de cubrir, no de sacerdote pagano; raíz homónima. |
| `k-m-r` | sacerdote pagano | heb | qamar | curvarse, arquearse | high | Curvarse/arquearse no tiene puente semántico claro con 'sacerdote pagano'; probablemente raíz homónima K-M-R distinta. |
| `k-m-r` | sacerdote pagano | heb | qomer | cúpula, bóveda | high | Cúpula/bóveda deriva del sentido de curvar, no de sacerdote; raíz homónima sin conexión al glosa. |
| `k-n-sh` | reunir, congregar | heb | konés | multa, sanción | high | קֹנֵס (multa) deriva de raíz K-N-S distinta (imponer pena); no hay puente semántico con 'reunir, congregar'. |
| `k-p-n` | hambre | ar | kafana | envolver, amortajar | high | Amortajar/envolver no tiene puente semántico con hambre; raíz árabe K-F-N homónima distinta. |
| `k-p-n` | hambre | ar | kafan | mortaja, sudario | high | Mortaja/sudario deriva de envolver, sin conexión con hambre; raíz homónima confirmada. |
| `k-p-n` | hambre | heb | kipén | empacar, envolver | high | Envolver/empacar no tiene conexión semántica con hambre; probablemente raíz homónima K-P-N distinta. |
| `k-p-n` | hambre | heb | kéfen | mortaja, sudario | high | Mortaja/sudario pertenece al campo semántico de envolver, no de hambre; raíz homónima. |
| `k-r-m` | viña | ar | karim | generoso, noble | high | Karim 'generoso/noble' deriva de raíz K-R-M árabe distinta (generosidad), no de 'viña'; homonimia, no extensión semántica. |
| `k-r-m` | viña | ar | mukrim | que honra, que agasaja | high | Mukrim 'que honra' pertenece a la raíz árabe de generosidad/honor, no a 'viña'; son raíces homónimas convergentes. |
| `k-r-s` | vientre, matriz | ar | kursiyy | silla, trono | medium | Silla/trono no tiene puente semántico claro con vientre/matriz; probablemente raíz homónima K-R-S diferente. |
| `k-r-s` | vientre, matriz | ar | karāsah | cuaderno, libro | high | Cuaderno/libro no guarda relación semántica con vientre/matriz; deriva de raíz distinta relacionada con hojas/papel. |
| `k-r-z` | predicar, proclamar | ar | katib | escritor, autor | high | كَاتِب (escritor) deriva de la raíz K-T-B (escribir), no de K-R-Z (predicar); error de asignación de raíz. |
| `k-r-z` | predicar, proclamar | ar | kutub | libros | high | كُتْب (libros) pertenece a K-T-B (escribir), no a K-R-Z (predicar); raíz completamente diferente. |
| `k-r-z` | predicar, proclamar | ar | kitabah | escritura | high | كِتَابَة (escritura) es de K-T-B, sin relación con K-R-Z (predicar); cognado erróneamente incluido. |
| `k-s-p` | plata, dinero | ar | kasúf | eclipse | high | Eclipse (kusūf) deriva de raíz K-S-F 'cubrir/ocultar', homónima pero semánticamente distinta de K-S-B 'ganar' o K-S-P 'plata'. |
| `k-s-p` | plata, dinero | ar | kisfun | pedazo, fragmento | high | Kisfun 'pedazo/fragmento' pertenece a K-S-F 'romper/fragmentar', raíz homónima sin puente semántico con 'plata/dinero'. |
| `k-sh-l` | tropezar | ar | kasila | ser perezoso | medium | Pereza no deriva claramente de tropezar; posible raíz homónima o desarrollo semántico muy oscuro sin puente evidente. |
| `k-sh-l` | tropezar | ar | kas·l | pereza | medium | Sustantivo 'pereza' sin conexión semántica clara con 'tropezar'; no hay puente metafórico obvio. |
| `k-sh-l` | tropezar | ar | ka·sil | perezoso | medium | Adjetivo 'perezoso' no muestra vínculo semántico con tropezar; probable raíz homónima en árabe. |
| `kh-a-r` | mirar, libre | ar | maḥẓūr | prohibido, vedado | high | maḥẓūr deriva de raíz Ḥ-Ẓ-R (prohibir, cercar), no de Ḫ-Y-R/Ḥ-R-R; inclusión errónea en esta familia. |
| `kh-d-a` | uno, alegrarse | heb | kḥad | agudo, afilado | high | Agudo/afilado no tiene puente semántico claro con 'uno' o 'alegrarse'; probablemente raíz homónima KH-D-D. |
| `kh-d-y` | alegrarse, gozo | ar | ḥadāṯa | novedad, modernidad | medium | Novedad/modernidad pertenece a raíz ḤDṮ (ser nuevo), no a ḤDY (alegrarse); homónimos distintos. |
| `kh-d-y` | alegrarse, gozo | heb | ḥāder | habitación, cuarto | high | Habitación/cuarto no tiene puente semántico con alegrarse/gozo; raíz homónima ḤDR distinta. |
| `kh-d-y` | alegrarse, gozo | heb | ḥādāh | agudo, puntiagudo | high | Agudo/puntiagudo no tiene conexión con alegría; raíz ḤDD diferente que se confunde fonéticamente. |
| `kh-l-b` | leche | heb | ḥelvāh | manteca | medium | Manteca/sebo refiere a grasa animal sólida, no a leche; posible confusión con raíz KH-L-V (grasa), no extensión clara de 'leche'. |
| `kh-l-m` | soñar | ar | hilm | paciencia/clemencia | high | Hilm (paciencia/clemencia) es raíz homónima distinta; no hay puente semántico plausible entre soñar y paciencia. |
| `kh-l-m` | soñar | ar | ḥalīm | paciente, clemente | high | Ḥalīm (paciente/clemente) deriva de hilm, raíz homónima separada de 'soñar'; significados genuinamente no relacionados. |
| `kh-r-n` | otro, diferente | heb | hitḥarer | liberarse, emanciparse | medium | Liberarse/emanciparse no tiene puente claro con 'otro'; probable confusión con raíz Ḥ-R-R (libertad). |
| `kh-r-th` | fin, último | heb | ḥarā | estar enojado, enfurecerse | high | Estar enojado no tiene puente semántico claro con 'fin/último'; raíz homónima ח-ר-ה distinta. |
| `kh-r-th` | fin, último | heb | ḥorev | sequía, desolación | high | Sequía/desolación pertenece a raíz ח-ר-ב (secar), sin conexión con 'fin/último'. |
| `kh-s-d` | reprochar (heb. chesed = misericordia) | ar | hasada | envidiar | high | El gloss es 'reprochar'; 'envidiar' es un campo semántico diferente sin puente claro al reproche o misericordia. |
| `kh-s-d` | reprochar (heb. chesed = misericordia) | ar | hasad | envidia | high | La 'envidia' no tiene conexión semántica evidente con 'reprochar' ni con 'misericordia'; divergencia genuina. |
| `kh-s-d` | reprochar (heb. chesed = misericordia) | ar | hasid | envidioso | high | 'Envidioso' no se relaciona con 'reprochar' ni 'misericordia'; son campos semánticos distintos sin puente. |
| `kh-s-d` | reprochar (heb. chesed = misericordia) | ar | hasud | envidioso | high | 'Envidioso' carece de conexión semántica con el reproche o la misericordia; outlier genuino. |
| `kh-s-d` | reprochar (heb. chesed = misericordia) | ar | tahasad | tener envidia mutua | high | 'Tener envidia mutua' no tiene puente semántico al reproche ni a la misericordia; divergencia real. |
| `kh-s-m` | amordazar, envidiar | ar | ḥaṣūm | obstinado, inflexible | medium | Obstinado/inflexible no tiene puente claro con amordazar ni envidiar; posible raíz homónima. |
| `kh-w-h` | mostrar, declarar | heb | havvāyāh | existencia, ser | high | El significado 'existencia, ser' proviene de la raíz H-W-Y (ser), no de KH-W-H (mostrar); son raíces homónimas distintas. |
| `kh-w-y` | mostrar, declarar | ar | muḵbir | informador, denunciante | high | Esta palabra deriva de raíz خ-ب-ر (informar), no de ح-و-ي (mostrar); es un error de asignación de raíz. |
| `kh-y-l` | fuerza, poder | ar | hawwala | transformar, cambiar | medium | Transformar/cambiar no tiene puente claro con fuerza/poder; probablemente raíz homónima Ḥ-W-L distinta. |
| `kh-y-y` | vivir, vida | ar | ḥayyiz | espacio, esfera | high | ḥayyiz (espacio, esfera) deriva de raíz ḥ-w-z (contener, abarcar), no de ḥ-y-y (vivir); sin puente semántico. |
| `kh-z-y` | ver, visión | ar | raʾyah | visión, perspectiva | high | raʾyah deriva de la raíz R-ʾ-Y (رأى), no de KH-Z-Y; es un cognado semántico pero no etimológico de esta familia. |
| `l-m-d` | aprender, enseñar | ar | malma7 | característica | high | مَلْمَح (característica/rasgo) deriva de la raíz ل-م-ح (vislumbrar/percibir), no de ل-م-د (aprender); raíces homónimas distintas. |
| `l-w-y` | Leví, acompañar | ar | lawā | torcer, girar | high | Torcer/girar no tiene puente semántico claro con acompañar o el nombre Leví; probablemente raíz homónima. |
| `l-w-y` | Leví, acompañar | ar | lawya | torsión, giro | high | Torsión/giro es extensión de torcer, sin conexión con acompañar; misma raíz homónima que ar:0. |
| `m-l-l` | hablar, palabra | ar | mutamallil | aburrido, hastiado | medium | El significado 'aburrido, hastiado' no tiene puente semántico claro con 'hablar, palabra'; posible raíz homónima M-L-L. |
| `m-l-l` | hablar, palabra | ar | tamallu | aburrimiento, hastío | medium | El significado 'aburrimiento, hastío' carece de conexión semántica con 'hablar, palabra'; probablemente raíz homónima. |
| `m-l-th` | palabra, asunto | ar | tamallaka | apoderarse, adueñarse | high | Deriva de M-L-K (poseer/reinar), raíz diferente de la glosa 'palabra, asunto'. |
| `m-l-th` | palabra, asunto | ar | malakut | reino, soberanía | high | Pertenece a raíz M-L-K (soberanía), no relacionada semánticamente con 'palabra'. |
| `m-l-th` | palabra, asunto | ar | malik | rey, soberano | high | Malik (rey) es de M-L-K (reinar), raíz independiente sin puente a 'palabra/asunto'. |
| `m-l-th` | palabra, asunto | heb | mulkah | reino, dominio | high | Pertenece a la raíz M-L-K (reinar), no a M-L-TH (palabra); son raíces homónimas distintas. |
| `m-l-th` | palabra, asunto | heb | malkut | realeza, soberanía | high | Deriva de M-L-K (reino/reinar), raíz distinta de M-L-TH (palabra/asunto). |
| `m-n-y` | contar, nombrar | ar | munwá | intención, propósito | medium | Intención/propósito no tiene puente claro con contar/nombrar; probablemente de raíz homónima M-N-W (desear). |
| `m-sh-kh` | ungir (Mesías/Mashiaj) | ar | mas'kub | derramado, vertido | high | mas'kub (مَسْكُوب) deriva de S-K-B 'derramar/verter', no de M-S-H 'ungir/frotar'; raíz diferente. |
| `m-sh-kh` | ungir (Mesías/Mashiaj) | heb | mashmi'd | destructivo, dañino | high | mashmi'd (מַשְׁמִיד) deriva de la raíz SH-M-D 'destruir', no de M-SH-KH 'ungir'; inclusión errónea. |
| `n-g-d` | atraer, guiar | ar | najd | meseta, altiplano | medium | Meseta/altiplano es término geográfico sin puente claro a 'atraer/guiar'; posible raíz homónima o desarrollo semántico opaco. |
| `n-kh-m` | consolar, consolación | ar | tanahnaha | carraspear | medium | Carraspear (aclarar la garganta) es acción física sin vínculo semántico claro con consolar o consolación. |
| `n-kh-th` | descender | ar | manhut | tallado | high | Tallar/esculpir deriva de raíz homónima N-Ḥ-T árabe distinta; sin puente semántico con 'descender'. |
| `n-kh-th` | descender | ar | nāḥit | escultor | high | Escultor deriva de N-Ḥ-T 'tallar', raíz homónima sin conexión etimológica con 'descender'. |
| `n-p-l` | caer | ar | náfil | supererogatario | medium | Supererogatario (acto voluntario extra) no tiene puente semántico claro con 'caer'; posible raíz homónima N-F-L. |
| `n-s-b` | tomar | ar | nasīb | pariente, familiar | medium | Pariente/familiar proviene de la raíz árabe N-S-B 'linaje', homónima pero semánticamente distinta de 'tomar'. |
| `n-s-b` | tomar | ar | mansūb | atribuido, relacionado | medium | Atribuido/relacionado pertenece al campo semántico de 'linaje/atribución', raíz homónima distinta de 'tomar'. |
| `n-sh-a` | mujeres | ar | nawasha | hurtar, robar | high | Hurtar/robar no tiene puente semántico plausible con 'mujeres'; raíz diferente o convergencia formal. |
| `n-sh-a` | mujeres | ar | naʾīshun | pobre, indigente | high | Pobre/indigente no guarda relación semántica con 'mujeres'; sin puente metafórico identificable. |
| `n-sh-a` | mujeres | heb | nāshāh | prestar, dar un préstamo | high | Prestar/dar préstamo no tiene conexión semántica con 'mujeres'; raíz homónima N-SH-H distinta. |
| `n-sh-q` | besar | ar | shumūm | perfumes | high | Shumūm deriva de raíz SH-M-M (oler), no de N-SH-Q; error de clasificación, no cognado real. |
| `n-sh-q` | besar | heb | nesheq | arma/armamento | medium | Arma/armamento no tiene puente semántico claro con besar; probablemente raíz homónima N-SH-Q distinta. |
| `p-g-r` | cuerpo | ar | fujūr | inmoralidad, libertinaje | high | Inmoralidad/libertinaje no tiene puente semántico claro con 'cuerpo'; deriva de raíz homófona F-J-R 'brotar/amanecer'. |
| `p-g-r` | cuerpo | ar | fajīr | roto, desgarrado | high | Roto/desgarrado pertenece al campo semántico de F-J-R 'romper/brotar', sin conexión etimológica con 'cuerpo'. |
| `p-r-e` | pagar, dar fruto | ar | firʿawn | faraón | high | Faraón es préstamo del egipcio (pr-ꜥꜣ), no derivación semítica de pagar/fructificar; etimología externa. |
| `p-r-e` | pagar, dar fruto | heb | pāraʿ | revelarse, desordenar | high | Rebelarse/desordenar no tiene puente semántico claro con pagar o dar fruto; probablemente raíz homónima. |
| `p-r-q` | salvar, redimir | ar | firqa | grupo/secta | medium | Grupo/secta se deriva de 'separar' pero no conecta claramente con 'salvar/redimir'; es extensión de un sentido diferente de la raíz. |
| `p-r-q` | salvar, redimir | ar | fariq | diferente, distinto | high | Adjetivo 'diferente/distinto' deriva de 'separar/distinguir', no de 'salvar/redimir'; sin puente semántico al gloss. |
| `p-r-q` | salvar, redimir | ar | iftaraqa | separarse, dividirse | high | Separarse/dividirse es extensión de 'separar' pero no de 'salvar/redimir'; significado genuinamente divergente del gloss. |
| `p-r-s` | extender, desplegar | ar | faris | jinete/Persia | high | Jinete/Persia no tiene puente semántico claro con 'extender/desplegar'; raíz homónima diferente. |
| `p-r-s` | extender, desplegar | ar | fars | Persia | high | Persia es nombre propio geográfico sin conexión semántica con 'extender/desplegar'. |
| `p-r-s` | extender, desplegar | ar | iftarasa | devorar, despedazar | medium | Devorar/despedazar carece de puente claro con 'extender'; posible raíz homónima convergente. |
| `p-s-q` | cortar, decidir | ar | qitāʿ | sección, sector | high | qitāʿ deriva de raíz Q-Ṭ-ʿ (قطع), no de F-Ṣ-L ni P-S-Q; raíz diferente, no es cognado. |
| `p-sh-q` | interpretar, explicar | ar | qāsama | dividir, compartir | high | Raíz Q-S-M (dividir/compartir) es diferente de P-SH-Q/F-S-R; no hay cognacía real ni puente semántico. |
| `p-sh-q` | interpretar, explicar | heb | pashaq | extender | high | Extender físicamente no tiene puente semántico claro hacia interpretar/explicar; probable raíz homónima. |
| `p-sh-q` | interpretar, explicar | heb | mifshak | articulación, coyuntura | high | Articulación/coyuntura anatómica no conecta con interpretar/explicar; deriva de la acción de extender/separar, no del gloss. |
| `q-b-l` | recibir | ar | qabl | antes | high | قَبْل 'antes' indica posición temporal/espacial frontal, sin puente semántico claro con 'recibir'; probablemente raíz homónima. |
| `q-l-l` | ser ligero, veloz; maldecir | heb | qalíl | ruidoso, sonoro | medium | El gloss es 'ligero/maldecir'; 'ruidoso/sonoro' pertenece a raíz Q-W-L (voz), no a Q-L-L semánticamente. |
| `q-r-sh` | congelar, ser frío | ar | qurshun | tiburón | medium | 'Tiburón' no tiene conexión semántica clara con 'congelar/ser frío'; probablemente raíz homónima Q-R-SH. |
| `q-r-sh` | congelar, ser frío | heb | qarnḥán | calvo | high | La raíz es Q-R-SH pero 'qarnḥán' parece derivar de Q-R-Ḥ (calvicie); no hay puente con 'congelar/frío'. |
| `r-b-a` | grande, rabí | ar | rabi' | primavera | medium | Rabi' (primavera) probablemente de raíz homónima R-B-' (cuatro/cuarto); sin puente semántico claro con 'grande/rabí'. |
| `r-d-p` | perseguir | ar | rā'id | explorador, líder | high | رَائِد deriva de raíz R-W-D (ir, explorar), no de R-D-F; es homógrafo parcial, no cognado semántico. |
| `r-d-y` | viajar, caminar | heb | rada | dominar, gobernar | medium | Dominar/gobernar no tiene puente claro con viajar; posible raíz homónima en hebreo. |
| `r-g-z` | ira, enojo | ar | rajjaza | recitar con entusiasmo | medium | Recitar con entusiasmo poético se aleja de ira; aunque derivado de agitación, el puente semántico es tenue. |
| `r-g-z` | ira, enojo | ar | rajz | poema, verso | medium | Poema/verso como género literario diverge genuinamente del campo semántico de ira/enojo sin puente claro. |
| `r-y-m` | ser alto, exaltar | ar | rāma | desear | high | Desear no tiene puente semántico claro con 'ser alto/exaltar'; probablemente raíz homónima R-W-M distinta. |
| `r-y-m` | ser alto, exaltar | ar | rūm | los bizantinos, los romanos | high | Etnónimo 'romanos/bizantinos' deriva del latín Roma, no de raíz semítica 'ser alto'; homonimia accidental. |
| `s-e-r` | hacer, visitar, cabello | ar | saʿara | encender, prender | high | Encender/prender fuego no tiene puente semántico con cabello, hacer o visitar; raíz homónima distinta. |
| `s-e-r` | hacer, visitar, cabello | ar | masʿarah | horno, hornillo | high | Horno/hornillo deriva de s-ʿ-r 'encender fuego', raíz homónima sin conexión con cabello/hacer/visitar. |
| `s-g-a` | ser muchos, crecer | ar | saja | ser tranquilo/extenso | medium | Ser tranquilo no conecta con 'ser muchos/crecer'; extenso podría derivar de crecer, pero 'calma' sugiere raíz homónima. |
| `s-g-a` | ser muchos, crecer | ar | masjá | lecho, lugar de reposo | medium | Lecho/lugar de reposo no tiene puente claro con ser muchos o crecer; probable raíz homónima. |
| `s-kh-r` | cerrar | ar | sukr | borrachera, embriaguez | high | La embriaguez no tiene puente semántico claro con 'cerrar'; probablemente raíz homónima S-K-R distinta. |
| `s-l-q` | subir, ascender | ar | mustaliḳ | que está acostado, echado | medium | Estar acostado/echado es opuesto semántico a 'subir/ascender'; no hay puente claro entre posición horizontal y ascenso. |
| `s-l-q` | subir, ascender | ar | sulūq | raza de perro, galgo | high | Nombre de raza canina (galgo de Salūq, topónimo); no tiene conexión semántica con 'subir/ascender'. |
| `s-m` | poner, colocar | ar | sammā | nombrar, designar | medium | Árabe sammā 'nombrar' deriva de S-M-W/Y 'nombre/altura', raíz distinta de S-M 'poner'; probable homofonía, no extensión semántica directa. |
| `s-m-y` | ciego | ar | sumuw'w | elevación, altura | high | سُمُوّ deriva de S-M-W (elevarse), raíz distinta de S-M-Y (ciego); sin puente semántico. |
| `s-m-y` | ciego | ar | sum'ah | reputación, fama | high | سُمْعَة deriva de S-M-ʿ (oír), raíz completamente diferente; no hay conexión con ceguera. |
| `s-p-r` | escriba, libro | ar | safara | viajar | high | Viajar no tiene puente semántico claro con escriba/libro; probablemente raíz homónima árabe S-F-R distinta. |
| `s-p-r` | escriba, libro | ar | safar | viaje | high | Viaje carece de conexión semántica con escribir o libro; es desarrollo propio de raíz árabe homónima. |
| `s-p-r` | escriba, libro | ar | asfarā | amanecer, aparecer | high | Amanecer/aparecer no guarda relación con escriba ni libro; desarrollo semántico sin puente plausible. |
| `s-p-r` | escriba, libro | ar | sufra | mantel, mesa para comer | high | Mantel/mesa para comer no tiene conexión con escribir o libro; semánticamente divergente. |
| `s-p-r` | escriba, libro | ar | musāfir | viajero | high | Viajero deriva de safara (viajar), raíz homónima sin relación semántica con escriba/libro. |
| `s-y-m` | poner, colocar | ar | samā | elevarse, ascender | high | Raíz árabe س-م-و (elevarse) es homónima pero etimológicamente distinta de la raíz siríaca ܣܝܡ (poner); no hay puente semántico. |
| `s-y-m` | poner, colocar | ar | sam'w | elevación, sublimidad | high | Derivado nominal de س-م-و (elevación); raíz diferente sin conexión semántica con 'poner, colocar'. |
| `s-y-m` | poner, colocar | ar | sumuww | altura, eminencia | high | Sustantivo de س-م-و indicando altura/eminencia; raíz árabe distinta, sin relación con el sentido de colocar. |
| `s-y-r` | esperar, tener esperanza | ar | ṣawwir | imaginar, concebir | high | ṣawwara (صَوَّرَ) deriva de raíz Ṣ-W-R 'imagen/forma', no de S-Y-R 'esperar'; raíz diferente. |
| `s-y-r` | esperar, tener esperanza | ar | ṣāʾir | que llega a ser, que se convierte en | high | ṣāʾir deriva de Ṣ-Y-R 'llegar a ser', raíz distinta de la semántica de espera/esperanza. |
| `sh-b-e` | siete, jurar | heb | shávha | estar satisfecho | medium | Aunque algunos proponen conexión etimológica (jurar = satisfacerse con el pacto), la semántica 'estar satisfecho' diverge significativamente de 'siete/jurar' sin puente claro. |
| `sh-b-kh` | alabar, gloria | ar | mashhur | famoso, célebre | high | مَشْهُور deriva de ش-ه-ر (publicar, fama), no de ش-ب-ح (alabar); raíces distintas, no hay puente semántico. |
| `sh-b-q` | dejar, perdonar | ar | sabaqa | preceder/adelantar | high | سَبَقَ 'preceder' deriva de raíz S-B-Q distinta; no hay puente semántico con 'dejar/perdonar'. |
| `sh-b-q` | dejar, perdonar | ar | sabiq | anterior/previo | high | Derivado de سَبَقَ (S-B-Q 'preceder'), raíz diferente sin conexión con 'dejar/perdonar'. |
| `sh-b-q` | dejar, perdonar | ar | tashabbaha | asemejarse, parecerse a | high | تَشَبَّهَ 'asemejarse' es de raíz Sh-B-H (semejanza), no Sh-B-Q; sin relación con 'dejar/perdonar'. |
| `sh-b-q` | dejar, perdonar | ar | tasabbaqa | adelantarse, tener prioridad | high | Forma V de S-B-Q 'preceder'; raíz distinta sin puente semántico a 'dejar/perdonar'. |
| `sh-b-th` | sábado, descansar | heb | shavit | prisionero, cautivo | high | Prisionero/cautivo pertenece a raíz homónima SH-B-H (capturar), no a SH-B-TH (descansar/sábado); sin puente semántico. |
| `sh-b-th` | sábado, descansar | heb | shevut | cautiverio, exilio | high | Cautiverio/exilio deriva de SH-B-H (capturar), raíz homónima distinta; no hay conexión con descanso o sábado. |
| `sh-e-y` | hora, tiempo | ar | istish'ār | percepción, sensación | high | Deriva de sh-'-r (sentir/percibir), raíz diferente; no hay puente semántico con 'hora/tiempo'. |
| `sh-e-y` | hora, tiempo | ar | mash'ūr | sentido, consciente | high | Pertenece a sh-'-r (percepción/consciencia), no a sh-'-y (tiempo/hora); raíces homófonas distintas. |
| `sh-kh-kh` | encontrar | heb | hishtakke'akh | olvidar | high | Olvidar es el opuesto semántico de encontrar; no hay puente metafórico claro entre ambos conceptos. |
| `sh-kh-kh` | encontrar | heb | nishkakh | olvidado | high | Olvidado es participio de olvidar, opuesto directo de encontrar; divergencia semántica genuina sin puente etimológico. |
| `sh-l-h` | desvestir, quitar | heb | shillu'aḥ | expulsión, envío | high | Shillu'aḥ deriva de SH-L-Ḥ (enviar), raíz distinta de SH-L-H (desvestir); no hay puente semántico con 'quitar ropa'. |
| `sh-l-kh` | enviar, apóstol | ar | salakha | desollar/pasar (tiempo) | high | Desollar (quitar piel) no tiene puente semántico con enviar; son raíces homónimas que convergieron fonéticamente. |
| `sh-l-y` | callar, cesar | heb | sheliYYah | placenta | medium | Placenta no tiene puente semántico claro con 'callar, cesar'; posible raíz homónima o desarrollo oscuro. |
| `sh-n-a` | cambiar, año | ar | mustahdath | nuevo, moderno | high | Raíz H-D-Th (حدث) no es S-N-W/Y; 'mustahdath' deriva de otra raíz completamente diferente, error de clasificación. |
| `sh-n-a` | cambiar, año | heb | shen'aí | enemigo | medium | Raíz Sh-N-' (odiar) es distinta de Sh-N-H (cambiar/año); 'enemigo' no tiene puente semántico claro con 'cambiar' o 'año'. |
| `sh-p-e` | desbordar, abundar | ar | shafīʿ | intercesor, mediador | high | Árabe شفع (interceder) es raíz homónima distinta de שפע (desbordar); no hay puente semántico plausible entre abundancia e intercesión. |
| `sh-p-e` | desbordar, abundar | ar | shafāʿa | intercesión, patrocinio | high | Intercesión/patrocinio deriva de raíz árabe diferente (شفع = emparejar/interceder), sin conexión con desbordar o abundar. |
| `sh-p-r` | ser bello, trompeta (shofar) | ar | safara | viajar/revelar | high | Viajar/revelar no tiene conexión semántica clara con ser bello ni con trompeta; raíz homónima distinta. |
| `sh-p-r` | ser bello, trompeta (shofar) | ar | safar | viaje | high | Viaje no se relaciona con belleza ni trompeta; pertenece a raíz S-F-R distinta (viajar). |
| `sh-p-r` | ser bello, trompeta (shofar) | ar | musaffar | amarillento | high | Amarillento no tiene puente semántico con belleza ni con trompeta; raíz Ṣ-F-R distinta (amarillo). |
| `sh-q-l` | tomar, cargar | heb | hashil | poner, colocar, dejar | medium | Forma hifil con significado 'poner/dejar' muestra divergencia semántica del campo 'tomar/cargar'; posible raíz homónima. |
| `sh-q-l` | tomar, cargar | heb | masha | carga, peso | high | Raíz נשא (N-S-') 'llevar/cargar', no Sh-Q-L; error de asignación a esta familia. |
| `sh-r` | saltar, brincar | heb | asher | que, el cual (partícula relativa) | high | Partícula relativa gramatical sin conexión semántica con 'saltar/brincar'; raíz homónima distinta. |
| `sh-r-a` | comenzar, soltar | ar | shareek | socio | high | شَرِيك deriva de raíz Sh-R-K (compartir), no de Sh-R-' (comenzar/soltar); raíz diferente, cognado erróneo. |
| `sh-r-b` | tribu, generación | ar | shariba | beber | high | Beber no tiene conexión semántica con tribu/generación; raíz homónima distinta. |
| `sh-r-b` | tribu, generación | ar | sharābun | bebida, poción | high | Bebida deriva de 'beber', no de tribu/generación; pertenece a raíz homónima. |
| `sh-r-b` | tribu, generación | ar | shurbun | acto de beber | high | Acto de beber pertenece al campo semántico de 'beber', no de tribu/generación. |
| `sh-r-b` | tribu, generación | heb | sharáv | sequía, calor ardiente | high | Sequía/calor ardiente no tiene puente semántico con tribu/generación; probablemente raíz homónima. |
| `sh-r-k` | permanecer, resto | ar | sharika | asociarse, compartir | high | Compartir/asociarse no deriva de 'permanecer/resto'; raíz árabe ش-ر-ك distinta semánticamente de la siríaca/hebrea. |
| `sh-r-k` | permanecer, resto | ar | sharik | socio, compañero | high | Socio/compañero no tiene puente semántico con 'permanecer, resto'; pertenece al campo de asociación, no de remanente. |
| `sh-r-k` | permanecer, resto | ar | shirkah | sociedad, compañía | high | Compañía/sociedad comercial no se relaciona con 'permanecer/resto'; campo semántico completamente diferente. |
| `sh-r-k` | permanecer, resto | ar | ishtaraka | participar, compartir | high | Participar/compartir no deriva de 'permanecer'; probable raíz homónima con desarrollo semántico independiente. |
| `sh-r-r` | verdad, ser firme | ar | sharra | ser malo | high | Ser malo no tiene puente semántico claro con 'verdad/ser firme'; probablemente raíz homónima árabe distinta. |
| `sh-r-r` | verdad, ser firme | ar | sharr | mal/maldad | high | Mal/maldad carece de conexión semántica con firmeza o verdad; raíz homófona pero semánticamente divergente. |
| `sh-r-r` | verdad, ser firme | ar | sharīr | malvado, perverso | high | Malvado/perverso no deriva de 'firme/verdad'; representa raíz árabe šrr 'mal' homónima de la siríaca. |
| `sh-th-a` | beber | ar | shata | llover (invierno) | high | شَتَا 'llover/invierno' deriva de raíz SH-T-W (estación invernal), homónima pero etimológicamente distinta de SH-T-Y 'beber'. |
| `sh-w-q` | calle, mercado | ar | shawq | anhelo, deseo | high | Anhelo/deseo no tiene puente semántico con calle/mercado; probablemente raíz homónima distinta. |
| `sh-w-q` | calle, mercado | ar | shawk | anhelar, desear | high | Anhelar/desear sin conexión semántica con calle/mercado; raíz homónima. |
| `sh-w-q` | calle, mercado | ar | shā'iq | anhelante, deseoso | high | Anhelante/deseoso no se relaciona con calle/mercado; deriva de raíz homónima. |
| `sh-w-q` | calle, mercado | ar | tashwīq | atracción, encanto | high | Atracción/encanto pertenece al campo semántico de deseo, no de calle/mercado. |
| `t-e-y` | errar, extraviarse | ar | tā'i' | obediente, sumiso | high | La raíz T-E-Y significa errar/transgredir; 'obediente/sumiso' es semánticamente opuesto, sin puente plausible desde extraviarse. |
| `th-b-e` | demandar, requerir | ar | tabi'a | seguir | high | Seguir/follow no tiene puente semántico claro con demandar/requerir; probablemente raíces homónimas convergentes. |
| `th-b-e` | demandar, requerir | ar | tābi' | seguidor | high | Seguidor deriva de seguir, no de demandar; sin extensión semántica plausible hacia requerir. |
| `th-l-m` | discípulo | heb | telem | surco | medium | Surco (furrow) pertenece a un campo semántico agrícola sin puente claro hacia 'discípulo'; posible raíz homónima TH-L-M. |
| `th-r-ts` | enderezar, corregir | ar | tarāḍá | acordar, convenir | high | Raíz diferente: tarāḍá viene de R-Ḍ-Y (satisfacer/consentir), no de T-R-Ṣ; homonimia aparente. |
| `th-r-ts` | enderezar, corregir | ar | tartīb | orden, arreglo | high | Tartīb deriva de R-T-B (ordenar), no de T-R-Ṣ; raíz completamente distinta, inclusión errónea. |
| `th-r-y` | dos | heb | teruts | excusa, pretexto | high | תֵּרוּץ deriva de raíz T-R-Tz (correr, apresurarse), no de TH-R-Y (dos); sin puente semántico con 'dos'. |
| `th-w-b` | volver, arrepentirse | ar | thawb | vestido/retorno | medium | El significado 'vestido/prenda' no tiene puente claro con 'volver/arrepentirse'; probablemente raíz homónima TH-W-B distinta. |
| `ts-b-a` | querer, desear | ar | saba | soplar (viento del este) | high | Soplar viento del este no tiene puente semántico con querer/desear; probablemente raíz homónima. |
| `ts-b-a` | querer, desear | ar | sa'ib | que sopla, que fluye | high | Que sopla/fluye pertenece al campo semántico de viento/fluido, sin conexión con desear/querer. |
| `ts-b-a` | querer, desear | ar | masbub | derramado, vertido | high | Derramado/vertido refiere a líquidos, sin puente semántico plausible hacia querer/desear. |
| `ts-l-a` | orar | heb | tsala | asar | high | Asar (to roast) no tiene puente semántico con orar; probablemente raíz homónima TS-L-Y distinta. |
| `ts-l-y` | orar, crucificar | heb | tsalá | asar, freir | high | Asar/freír no tiene puente semántico claro con orar o crucificar; probablemente raíz homónima TS-L-Y distinta. |
| `ts-r-y` | necesitar, ser necesario | ar | ḍarīr | ciego | high | Ciego no tiene puente semántico claro con necesitar/ser necesario; probablemente de raíz homónima ḍ-r-r (dañar). |
| `ts-r-y` | necesitar, ser necesario | ar | taḍarrur | daño, perjuicio | medium | Daño/perjuicio deriva de ḍ-r-r (causar daño), raíz distinta aunque relacionada; divergencia semántica del sentido de necesidad. |
| `y-b-l` | traer, llevar | ar | maʾwil | refugio, albergue | medium | Maʾwil 'refugio' deriva de raíz ʾ-W-L (refugiarse), no de Y-B-L (llevar); raíces distintas, homografía accidental. |
| `y-d-e` | saber, conocer | ar | wada'a | dejar/depositar | high | وَدَعَ (dejar/depositar) deriva de raíz W-D-ʻ, no de Y-D-ʻ; sin puente semántico con 'saber/conocer'. |
| `y-d-y` | conocer, saber | ar | wadda | desear, querer | high | wadda 'desear/querer' es raíz و-د-د distinta; no hay puente semántico claro con 'conocer/saber'. |
| `y-l-p` | aprender | ar | iltifāt | atención, comprensión | high | Iltifāt deriva de raíz L-F-T (voltear, prestar atención), no de Y-L-F/ʾ-L-F; raíz diferente sin conexión semántica. |
| `y-m-m` | mar, día | ar | yumnā | derecha | high | El significado 'derecha' no tiene conexión semántica evidente con 'mar' ni 'día'. |
| `y-m-m` | mar, día | ar | yamāmah | paloma | high | El significado 'paloma' no tiene puente semántico plausible con 'mar' o 'día'. |
| `y-m-m` | mar, día | heb | yamin | derecha | high | La raíz Y-M-M significa 'mar' o 'día'; 'derecha' no tiene puente semántico claro con estos significados. |
| `y-sh-e` | salvar, Jesús | ar | wasi'a | ser amplio/espacioso | high | Raíz árabe و-س-ع (amplitud) es distinta de י-ש-ע (salvar); convergencia fonética superficial, sin puente semántico real. |
| `y-sh-e` | salvar, Jesús | ar | sa'a | amplitud | high | Deriva de و-س-ع (amplitud), raíz diferente a י-ש-ע (salvar); no hay conexión etimológica ni semántica. |
| `y-sh-e` | salvar, Jesús | ar | ittasa'a | ensancharse, ampliarse | high | Forma verbal de و-س-ع (ensancharse), raíz árabe distinta; no relacionada con el concepto de salvación. |
| `y-th-b` | sentarse, habitar | ar | wathaba | saltar | high | Saltar (to jump) es opuesto semántico a sentarse/habitar; no hay puente plausible con el gloss. |
| `y-th-r` | quedar, sobrar | ar | watar | cuerda, cable | high | Cuerda/cable no tiene puente semántico claro con 'quedar, sobrar'; probablemente raíz homónima W-T-R distinta. |
| `y-th-r` | quedar, sobrar | ar | awtar | equipar con cuerdas | high | Derivado de watar (cuerda); sin conexión semántica con el sentido de 'quedar' o 'sobrar'. |
| `y-th-r` | quedar, sobrar | ar | watir | tendón, cuerda | high | Tendón/cuerda pertenece al campo semántico de W-T-R 'cuerda', no al de 'quedar, sobrar'. |
| `y-th-y` | sentarse, habitar | ar | wathaba | saltar, sentarse (arcaico) | medium | وَثَبَ tiene raíz W-TH-B, no Y-TH-Y; 'saltar' diverge de 'sentarse/habitar' y la forma arcaica 'sentarse' es cuestionable cognado. |
| `y-th-y` | sentarse, habitar | ar | jalasa | sentarse | high | جَلَسَ es raíz J-L-S, no cognado de Y-TH-Y; es sinónimo semántico pero no cognado etimológico de esta familia. |
| `z-m-n` | tiempo, invitar | ar | izdiyán | aumento, incremento | high | izdiyán deriva de Z-Y-N (adornar/aumentar), no de Z-M-N; 'aumento' no tiene puente semántico con tiempo/invitar. |
| `z-n-y` | tipo, clase | ar | zanī | fornicador, adúltero | high | El significado 'fornicador, adúltero' no tiene puente semántico plausible con 'tipo, clase'; probablemente raíz homónima Z-N-Y distinta. |
| `z-y-n` | arma | ar | zayn | adorno | medium | Adorno/belleza no tiene puente semántico claro con arma; probablemente raíces homónimas Z-Y-N convergentes. |
| `z-y-n` | arma | ar | tazayyun | adornarse | medium | Adornarse deriva de la raíz árabe de belleza, no de arma; sin puente etimológico claro. |
| `z-y-n` | arma | ar | tazyīn | decoración | medium | Decoración pertenece al campo semántico de adorno/belleza, no al de arma; raíces homónimas. |

## Veredictos con confianza baja o media (revisión humana recomendada)

| Raíz | Gloss (es) | Translit | Significado | Veredicto | Conf. | Justificación |
|---|---|---|---|---|---|---|
| `a-b-d` | perecer, destruir | abada | eternidad (cognado semántico) | outlier | medium | أَبَدَ 'eternidad' es raíz homónima distinta (ʾ-b-d II); no hay puente claro entre 'perecer' y 'eternidad'. |
| `a-m-n` | confiar, amén | omanut | arte | NO outlier | medium | Arte deriva de 'habilidad confiable/maestría'; el artesano (oman) es alguien en quien se confía por su pericia. |
| `a-th-r` | lugar, tierra | ʾāthara | preferir, elegir | outlier | medium | Preferir/elegir no tiene puente claro con lugar/tierra; probablemente raíz homónima árabe. |
| `a-y-l` | árbol, poder | ʾillah | causa, razón | NO outlier | medium | Causa/razón puede derivar de 'poder' como fuerza causal o principio activo detrás de eventos. |
| `a-z-l` | ir | ma'āzil | dificultades, problemas | NO outlier | medium | Dificultades como 'cosas que se van/pierden' o 'situaciones de las que uno debe irse' — extensión metafórica plausible de 'ir/quitar'. |
| `b-T-l` | cesar, estar ocioso | batal | héroe/nulo | outlier | medium | El sentido 'héroe' no deriva de 'cesar/ocioso'; probablemente raíz homónima fusionada. El sentido 'nulo' sí conecta. |
| `b-kh-r` | primogénito | ibtakara | inventar | NO outlier | medium | Inventar como 'ser el primero en crear algo' deriva del sentido de primacía; quien inventa es el 'primogénito' de una idea. |
| `b-r-a` | crear, hijo | barur | claro, puro | outlier | medium | Barur deriva de B-R-R (purificar/seleccionar), raíz distinta de B-R-A (crear); no hay puente semántico claro. |
| `b-r-y` | crear, hijo | barūr | claro, puro | outlier | medium | Barūr 'claro, puro' deriva de raíz B-R-R (purificar), no de B-R-' (crear) ni de relación filial; sin puente semántico claro. |
| `b-s-r` | carne | bissûr | anuncio, noticia | outlier | medium | Significado 'anuncio/noticia' no conecta claramente con 'carne'; posible raíz homónima B-Ś-R II 'anunciar'. |
| `b-s-r` | carne | bišārah | buena noticia | outlier | medium | Igual que heb:2, 'buena noticia' deriva de raíz homónima B-Š-R 'anunciar', distinta semánticamente de 'carne'. |
| `d-b-r` | guiar, conducir | midbar | desierto | NO outlier | medium | El desierto es 'lugar donde se conduce/guía' ganado; extensión locativa del concepto de guiar/pastorear rebaños. |
| `d-m-r` | sorprenderse, admirarse | damara | destruir, arruinar | outlier | medium | Destruir/arruinar no tiene puente semántico claro con sorprenderse/admirarse; probablemente raíz homónima. |
| `d-m-r` | sorprenderse, admirarse | damirah | estar destruido, arruinado | outlier | medium | Estar destruido es extensión pasiva de ar:0; misma divergencia semántica sin puente a admirarse. |
| `d-m-r` | sorprenderse, admirarse | madmúr | destruido, arruinado | outlier | medium | Participio pasivo de damara (destruir); pertenece al campo de destrucción, no de asombro. |
| `e-b-r` | pasar, cruzar | ʿibra | aguja, lección | outlier | medium | El significado 'aguja' (إِبْرَة) pertenece a otra raíz (أ-ب-ر); posible confusión por homofonía parcial. |
| `e-d-l` | reprender, culpar | taʿdīl | modificación, corrección | NO outlier | medium | Corrección/modificación puede conectarse con reprender: corregir errores es cercano a censurar faltas. |
| `e-d-r` | ayudar | 'adhara | excusar | outlier | medium | Excusar implica exonerar de culpa, no ayudar activamente; el puente semántico es tenue aunque posible vía 'defender'. |
| `e-d-r` | ayudar | 'udhr | excusa | outlier | medium | Excusa como sustantivo se aleja del sentido de ayuda activa; posible conexión vía 'justificación' pero débil. |
| `e-d-th` | iglesia, asamblea | 'āda | costumbre | outlier | medium | Costumbre/hábito deriva de raíz ʕ-W-D (volver, repetir), no de ʕ-D-T (asamblea); raíces homónimas distintas. |
| `e-g-l` | becerro, apresurarse | 'iggul | círculo, redondo | outlier | medium | El sentido 'círculo/redondo' parece derivar de raíz homónima ע-ג-ל relacionada con rodar, sin puente claro a 'becerro' o 'apresurarse'. |
| `e-l-l` | entrar | 'olal | niño pequeño | outlier | medium | No hay puente semántico claro entre 'entrar' y 'niño pequeño'; posible raíz homónima o extensión muy oscura. |
| `e-l-m` | mundo, eternidad | 'alem | ocultar, esconder | outlier | medium | ʿ-L-M 'esconder' es probablemente raíz homónima distinta de 'mundo/eternidad'; sin puente semántico claro entre ocultar y eternidad/mundo. |
| `e-l-th` | causa, razón | 'āliyl | acto, hecho, hazaña | outlier | medium | Significa 'acto, hazaña' sin conexión clara con 'causa/razón'; posible raíz homónima E-L-L (hacer). |
| `e-m-r` | habitar, morar | 'ammīr | abundante, próspero | NO outlier | medium | Próspero/abundante puede derivar de 'lugar habitado floreciente'; extensión metafórica plausible. |
| `e-m-r` | habitar, morar | ma'ămār | ensamblaje, estructura | NO outlier | medium | Estructura/ensamblaje se conecta con construir, que es extensión natural de habitar (cf. árabe 'amara). |
| `e-n-a` | responder | 'anayah | pobreza | outlier | medium | Pobreza deriva de otra raíz ע-נ-י (afligir/oprimir), no de responder; sin puente semántico claro. |
| `e-n-a` | responder | 'anatul | paciencia | outlier | medium | Paciencia (أناة) probablemente de raíz distinta أ-ن-ي; sin vínculo semántico evidente con responder. |
| `e-n-y` | responder | 'ăniyyût | modestia, humildad | outlier | medium | Humildad proviene de raíz ע-נ-ה II (afligir/humillar), distinta semánticamente de responder; posible homónimo. |
| `e-n-y` | responder | taʿānin | sufrimiento, penuria | outlier | medium | Sufrimiento/penuria deriva de عَنِيَ (sufrir), raíz homónima distinta de 'responder'; sin puente semántico claro. |
| `e-r-s` | cama, lecho | ʿarīsh | emparrado, enramada | outlier | medium | Emparrado/enramada es estructura de ramas para plantas; no hay puente claro con cama/lecho como mueble para dormir. |
| `e-w-l` | iniquidad, injusticia | ʿāʾil | necesitado, indigente | NO outlier | medium | El indigente sufre injusticia; puente semántico plausible: quien padece iniquidad queda necesitado. |
| `e-y-r` | vigilar, despertar | ʿayyara | reprender, criticar | outlier | medium | Reprender/criticar carece de conexión evidente con vigilar/despertar; posible raíz homónima ع-ي-ر. |
| `e-z-l` | hilar, perezoso | ʿazala | aislar | NO outlier | medium | Aislar puede derivar de 'hilar' (separar fibras) o conectarse con 'perezoso' (apartado, inactivo); puente semántico plausible. |
| `e-z-l` | hilar, perezoso | ʿazl | aislamiento | NO outlier | medium | Aislamiento como extensión nominal de aislar; mismo puente semántico que el verbo raíz. |
| `e-z-l` | hilar, perezoso | ʿazīl | solitario | NO outlier | medium | Solitario conecta con perezoso (persona apartada/retraída) y con hilar (acción solitaria); extensión semántica razonable. |
| `g-b-a` | elegir, escoger | jabā | recaudar, reunir | outlier | medium | Recaudar/reunir (collect/gather) carece de puente claro con elegir/escoger; probablemente raíces homónimas G-B-Y vs G-B-'. |
| `g-b-a` | elegir, escoger | jābī | recaudador, cobrador | outlier | medium | Derivado de jabā (recaudar); recaudador no tiene conexión semántica evidente con elegir/escoger. |
| `g-b-a` | elegir, escoger | majbī | recaudador de impuestos | outlier | medium | Recaudador de impuestos deriva de jabā (recaudar), sin puente semántico hacia elegir/escoger. |
| `g-n-y` | jardín | janān | corazón, interior | outlier | medium | Corazón/interior no tiene puente semántico claro con jardín; probablemente raíz homónima G-N-N 'cubrir/ocultar'. |
| `k-a-p` | roca, piedra | kūfah | ciudad en Irak | outlier | medium | Nombre propio de ciudad sin conexión semántica clara con roca/piedra; etimología disputada, sin puente evidente. |
| `k-r-s` | vientre, matriz | kursiyy | silla, trono | outlier | medium | Silla/trono no tiene puente semántico claro con vientre/matriz; probablemente raíz homónima K-R-S diferente. |
| `k-sh-l` | tropezar | kasila | ser perezoso | outlier | medium | Pereza no deriva claramente de tropezar; posible raíz homónima o desarrollo semántico muy oscuro sin puente evidente. |
| `k-sh-l` | tropezar | kas·l | pereza | outlier | medium | Sustantivo 'pereza' sin conexión semántica clara con 'tropezar'; no hay puente metafórico obvio. |
| `k-sh-l` | tropezar | ka·sil | perezoso | outlier | medium | Adjetivo 'perezoso' no muestra vínculo semántico con tropezar; probable raíz homónima en árabe. |
| `kh-d-y` | alegrarse, gozo | ḥadāṯa | novedad, modernidad | outlier | medium | Novedad/modernidad pertenece a raíz ḤDṮ (ser nuevo), no a ḤDY (alegrarse); homónimos distintos. |
| `kh-l-b` | leche | ḥelvāh | manteca | outlier | medium | Manteca/sebo refiere a grasa animal sólida, no a leche; posible confusión con raíz KH-L-V (grasa), no extensión clara de 'leche'. |
| `kh-l-l` | profanar, comenzar (halal) | halíl | esposo, amante | NO outlier | medium | Esposo/amante deriva de 'lo lícito' (حلال): la pareja legalmente permitida; extensión semántica clara del concepto de licitud. |
| `kh-l-p` | cambiar, en lugar de | takhallufu | atraso, retraso | NO outlier | medium | Atraso significa 'quedarse atrás' mientras otros avanzan/cambian; extensión de sucesión/reemplazo temporal. |
| `kh-p-y` | cubrir, lavar | ḥāfin | descalzo | NO outlier | medium | Descalzo (sin cubierta en los pies) deriva semánticamente de 'cubrir' por negación; el participio activo indica ausencia de cobertura. |
| `kh-r-n` | otro, diferente | hitḥarer | liberarse, emanciparse | outlier | medium | Liberarse/emanciparse no tiene puente claro con 'otro'; probable confusión con raíz Ḥ-R-R (libertad). |
| `kh-s-m` | amordazar, envidiar | ḥasama | zanjar, resolver | NO outlier | medium | Zanjar/resolver puede derivar de 'cortar' o 'cerrar' un asunto, extensión metafórica de amordazar/obstruir. |
| `kh-s-m` | amordazar, envidiar | ḥaṣūm | obstinado, inflexible | outlier | medium | Obstinado/inflexible no tiene puente claro con amordazar ni envidiar; posible raíz homónima. |
| `kh-w-h` | mostrar, declarar | ḥawwā' | Eva (nombre propio femenino) | NO outlier | medium | Eva se interpreta tradicionalmente como 'la que da vida/declara'; el nombre propio deriva de la raíz semítica asociada a mostrar o vivificar. |
| `kh-w-r` | mirar, blanco | hayyara | confundir, perturbar | NO outlier | medium | حَيَّرَ 'confundir' deriva de hacer que alguien mire en varias direcciones sin orientarse, extensión de 'mirar'. |
| `kh-y-l` | fuerza, poder | hawwala | transformar, cambiar | outlier | medium | Transformar/cambiar no tiene puente claro con fuerza/poder; probablemente raíz homónima Ḥ-W-L distinta. |
| `l-w-y` | Leví, acompañar | liwā' | estandarte, bandera | NO outlier | medium | Estandarte puede derivar de 'lo que acompaña/une' al grupo; símbolo que agrupa a seguidores. |
| `l-w-y` | Leví, acompañar | lāwwā' | abanderado, estandarte | NO outlier | medium | Abanderado es agente de liwā' (estandarte); si liwā' conecta con acompañar, este también lo hace. |
| `m-l-l` | hablar, palabra | mutamallil | aburrido, hastiado | outlier | medium | El significado 'aburrido, hastiado' no tiene puente semántico claro con 'hablar, palabra'; posible raíz homónima M-L-L. |
| `m-l-l` | hablar, palabra | tamallu | aburrimiento, hastío | outlier | medium | El significado 'aburrimiento, hastío' carece de conexión semántica con 'hablar, palabra'; probablemente raíz homónima. |
| `m-n-y` | contar, nombrar | munwá | intención, propósito | outlier | medium | Intención/propósito no tiene puente claro con contar/nombrar; probablemente de raíz homónima M-N-W (desear). |
| `m-r-y` | señor, amo | mar' | hombre/persona | NO outlier | medium | De 'señor/amo' a 'hombre/persona' hay puente semántico: el amo es un hombre libre, extensión metonímica común. |
| `m-r-y` | señor, amo | imra'a | mujer | NO outlier | medium | Extensión femenina de mar' (hombre); si 'hombre' deriva de 'señor', 'mujer' es contraparte morfológica natural. |
| `n-g-d` | atraer, guiar | najd | meseta, altiplano | outlier | medium | Meseta/altiplano es término geográfico sin puente claro a 'atraer/guiar'; posible raíz homónima o desarrollo semántico opaco. |
| `n-g-d` | atraer, guiar | najid | excelente, destacado | NO outlier | medium | Najid 'excelente' puede derivar de 'destacado/sobresaliente', extensión de quien guía o es atraído hacia adelante. |
| `n-kh-m` | consolar, consolación | nahama | carraspear/gemir | NO outlier | medium | Gemir/groan se conecta con expresar dolor o pena, estado que precede a recibir consuelo; puente semántico plausible. |
| `n-kh-m` | consolar, consolación | tanahnaha | carraspear | outlier | medium | Carraspear (aclarar la garganta) es acción física sin vínculo semántico claro con consolar o consolación. |
| `n-p-l` | caer | náfil | supererogatario | outlier | medium | Supererogatario (acto voluntario extra) no tiene puente semántico claro con 'caer'; posible raíz homónima N-F-L. |
| `n-s-b` | tomar | n'siyyá | tentativa, ensayo | NO outlier | medium | Tentativa/ensayo deriva de 'tomar' como acción de emprender o intentar algo; extensión semántica plausible. |
| `n-s-b` | tomar | nasīb | pariente, familiar | outlier | medium | Pariente/familiar proviene de la raíz árabe N-S-B 'linaje', homónima pero semánticamente distinta de 'tomar'. |
| `n-s-b` | tomar | mansūb | atribuido, relacionado | outlier | medium | Atribuido/relacionado pertenece al campo semántico de 'linaje/atribución', raíz homónima distinta de 'tomar'. |
| `n-sh-q` | besar | nesheq | arma/armamento | outlier | medium | Arma/armamento no tiene puente semántico claro con besar; probablemente raíz homónima N-SH-Q distinta. |
| `p-r-q` | salvar, redimir | firqa | grupo/secta | outlier | medium | Grupo/secta se deriva de 'separar' pero no conecta claramente con 'salvar/redimir'; es extensión de un sentido diferente de la raíz. |
| `p-r-q` | salvar, redimir | furqan | diferencia, separación | NO outlier | medium | Furqan en contexto coránico significa salvación/criterio divino que separa verdad de falsedad, conectando con redención. |
| `p-r-s` | extender, desplegar | iftarasa | devorar, despedazar | outlier | medium | Devorar/despedazar carece de puente claro con 'extender'; posible raíz homónima convergente. |
| `p-r-sh` | separar, distinguir | furshah | cepillo | NO outlier | medium | Cepillo tiene cerdas separadas/esparcidas; derivación instrumental plausible de la noción de separar/extender. |
| `q-l-l` | ser ligero, veloz; maldecir | qalíl | ruidoso, sonoro | outlier | medium | El gloss es 'ligero/maldecir'; 'ruidoso/sonoro' pertenece a raíz Q-W-L (voz), no a Q-L-L semánticamente. |
| `q-r-sh` | congelar, ser frío | qurshun | tiburón | outlier | medium | 'Tiburón' no tiene conexión semántica clara con 'congelar/ser frío'; probablemente raíz homónima Q-R-SH. |
| `r-b-a` | grande, rabí | rabi' | primavera | outlier | medium | Rabi' (primavera) probablemente de raíz homónima R-B-' (cuatro/cuarto); sin puente semántico claro con 'grande/rabí'. |
| `r-d-y` | viajar, caminar | rada | dominar, gobernar | outlier | medium | Dominar/gobernar no tiene puente claro con viajar; posible raíz homónima en hebreo. |
| `r-g-z` | ira, enojo | rajjaza | recitar con entusiasmo | outlier | medium | Recitar con entusiasmo poético se aleja de ira; aunque derivado de agitación, el puente semántico es tenue. |
| `r-g-z` | ira, enojo | rajz | poema, verso | outlier | medium | Poema/verso como género literario diverge genuinamente del campo semántico de ira/enojo sin puente claro. |
| `r-kh-q` | estar lejos | rahiq | néctar (vino raro/lejano) | NO outlier | medium | El néctar/vino raro se llama así por ser 'lejano' o difícil de obtener; extensión metafórica de rareza/distancia. |
| `s-e-r` | hacer, visitar, cabello | suʿarāʾ | poetas | NO outlier | medium | Shiʿr (poesía) deriva de shaʿara 'percibir/sentir'; relacionado con raíz S-ʿ-R aunque glosa no lo refleja bien. |
| `s-g-a` | ser muchos, crecer | saja | ser tranquilo/extenso | outlier | medium | Ser tranquilo no conecta con 'ser muchos/crecer'; extenso podría derivar de crecer, pero 'calma' sugiere raíz homónima. |
| `s-g-a` | ser muchos, crecer | sajjā | cubrir, extenderse | NO outlier | medium | Extenderse es desarrollo natural de crecer; lo que crece se extiende y cubre espacio. |
| `s-g-a` | ser muchos, crecer | masjá | lecho, lugar de reposo | outlier | medium | Lecho/lugar de reposo no tiene puente claro con ser muchos o crecer; probable raíz homónima. |
| `s-l-q` | subir, ascender | mustaliḳ | que está acostado, echado | outlier | medium | Estar acostado/echado es opuesto semántico a 'subir/ascender'; no hay puente claro entre posición horizontal y ascenso. |
| `s-m` | poner, colocar | sammā | nombrar, designar | outlier | medium | Árabe sammā 'nombrar' deriva de S-M-W/Y 'nombre/altura', raíz distinta de S-M 'poner'; probable homofonía, no extensión semántica directa. |
| `sh-b-e` | siete, jurar | shávha | estar satisfecho | outlier | medium | Aunque algunos proponen conexión etimológica (jurar = satisfacerse con el pacto), la semántica 'estar satisfecho' diverge significativamente de 'siete/jurar' sin puente claro. |
| `sh-l-t` | gobernar, dominar | shelet | letrero/escudo | NO outlier | medium | El escudo es símbolo de poder/autoridad del gobernante; el letrero es objeto que ejerce control sobre el espacio público. |
| `sh-l-y` | callar, cesar | sheliYYah | placenta | outlier | medium | Placenta no tiene puente semántico claro con 'callar, cesar'; posible raíz homónima o desarrollo oscuro. |
| `sh-n-a` | cambiar, año | shen'aí | enemigo | outlier | medium | Raíz Sh-N-' (odiar) es distinta de Sh-N-H (cambiar/año); 'enemigo' no tiene puente semántico claro con 'cambiar' o 'año'. |
| `sh-p-r` | ser bello, trompeta (shofar) | sur | Tiro (cuerno) | NO outlier | medium | Tiro se asocia con cuerno/trompeta en la glosa; la nota '(cuerno)' indica conexión con shofar. |
| `sh-q-l` | tomar, cargar | hashil | poner, colocar, dejar | outlier | medium | Forma hifil con significado 'poner/dejar' muestra divergencia semántica del campo 'tomar/cargar'; posible raíz homónima. |
| `sh-r-a` | comenzar, soltar | shriirut | arbitrariedad | NO outlier | medium | De 'soltar' → 'sin restricción' → 'actuar a voluntad propia' → 'arbitrariedad'; extensión semántica plausible. |
| `sh-r-y` | comenzar, habitar, soltar | mishrah | jurisdicción, autoridad | NO outlier | medium | Jurisdicción/autoridad puede derivar de 'habitar' → dominio territorial, o de 'comenzar' → fundamento de gobierno. |
| `th-l-m` | discípulo | telem | surco | outlier | medium | Surco (furrow) pertenece a un campo semántico agrícola sin puente claro hacia 'discípulo'; posible raíz homónima TH-L-M. |
| `th-r-ts` | enderezar, corregir | turs | escudo | NO outlier | medium | Escudo como 'lo firme/sólido' conecta con enderezar; objeto que mantiene recto/firme al guerrero. |
| `th-w-b` | volver, arrepentirse | thawb | vestido/retorno | outlier | medium | El significado 'vestido/prenda' no tiene puente claro con 'volver/arrepentirse'; probablemente raíz homónima TH-W-B distinta. |
| `ts-l-y` | orar, crucificar | mits'lé'a | rejilla, parrilla | NO outlier | medium | Una parrilla/rejilla conecta con crucifixión por la estructura de barras cruzadas; extensión instrumental plausible. |
| `ts-r-y` | necesitar, ser necesario | taḍarrur | daño, perjuicio | outlier | medium | Daño/perjuicio deriva de ḍ-r-r (causar daño), raíz distinta aunque relacionada; divergencia semántica del sentido de necesidad. |
| `y-b-l` | traer, llevar | maʾwil | refugio, albergue | outlier | medium | Maʾwil 'refugio' deriva de raíz ʾ-W-L (refugiarse), no de Y-B-L (llevar); raíces distintas, homografía accidental. |
| `y-th-b` | sentarse, habitar | wādib | constante, perseverante | NO outlier | medium | Constante/perseverante se deriva de permanecer sentado o establecido; extensión figurativa de habitar. |
| `y-th-y` | sentarse, habitar | wathaba | saltar, sentarse (arcaico) | outlier | medium | وَثَبَ tiene raíz W-TH-B, no Y-TH-Y; 'saltar' diverge de 'sentarse/habitar' y la forma arcaica 'sentarse' es cuestionable cognado. |
| `z-y-n` | arma | zayn | adorno | outlier | medium | Adorno/belleza no tiene puente semántico claro con arma; probablemente raíces homónimas Z-Y-N convergentes. |
| `z-y-n` | arma | zayān | daño, perjuicio | NO outlier | medium | Daño/perjuicio conecta con arma: las armas causan daño, extensión semántica natural por metonimia. |
| `z-y-n` | arma | tazayyun | adornarse | outlier | medium | Adornarse deriva de la raíz árabe de belleza, no de arma; sin puente etimológico claro. |
| `z-y-n` | arma | tazyīn | decoración | outlier | medium | Decoración pertenece al campo semántico de adorno/belleza, no al de arma; raíces homónimas. |
