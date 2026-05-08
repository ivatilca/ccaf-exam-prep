import anthropic
import json

client = anthropic.Anthropic()

# ── AGENTE 1: J. JONAH JAMESON ───────────────────────────────────────
# Usamos Haiku — tarea creativa simple, necesitamos velocidad
jameson = client.messages.create(
    model="claude-haiku-4-5-20251001",
    max_tokens=120,
    system="""Sos J. Jonah Jameson, editor del Daily Bugle. Temperamental,
    dramático, convencido de que Spider-Man es una amenaza pública.
    No importa lo que Spider-Man haya hecho — siempre encontrás el ángulo negativo.
    Respondés SOLO con el titular. Nada más.""",
    messages=[{
        "role": "user",
        "content": "Spider-Man detuvo un robo a mano armada en Manhattan."
    }]
)

titular = jameson.content[0].text
print(f"Titular de Jameson:\n{titular}\n")

# ── AGENTE 2: ANALISTA DE MEDIOS ─────────────────────────────────────
# Usamos Sonnet — análisis más profundo necesita más capacidad de razonamiento
analista = client.messages.create(
    model="claude-sonnet-4-6",
    max_tokens=400,
    system="""Sos un analista de medios especializado en sesgo periodístico.
    Evaluás titulares de noticias y devolvés un análisis objetivo.
    Respondés SOLO con JSON válido, sin texto adicional, con este formato exacto:
    {
      "sesgo": {"nivel": "alto|medio|bajo", "tipo": "..."},
      "sensacionalismo": {"score": 1-10, "justificacion": "..."},
      "precision_factual": {"es_preciso": true/false, "problema": "..."},
      "reescritura_neutral": "..."
    }""",
    messages=[{
        "role": "user",
        "content": f"Analizá este titular: {titular}"
    }]
)

# Parseamos el JSON — con manejo de error
try:
    informe = json.loads(analista.content[0].text)
    print("Análisis del titular:")
    print(json.dumps(informe, indent=2, ensure_ascii=False))
except json.JSONDecodeError:
    print("El analista no devolvió JSON válido. Output crudo:")
    print(analista.content[0].text)
