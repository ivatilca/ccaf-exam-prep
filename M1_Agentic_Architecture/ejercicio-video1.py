import anthropic, json

client = anthropic.Anthropic()

SYSTEM_SOMMELIER = '''Sos un sommelier experto.
Respondé SIEMPRE con JSON válido:
{
  "accion": "preguntar" | "recomendar",
  "mensaje": "el texto que vas a decir",
  "vino": "nombre del vino (solo si accion=recomendar)",
  "motivo": "por qué este vino (solo si accion=recomendar)"
}

Usá 'preguntar' hasta tener: ocasión, presupuesto, preferencia de sabor.
Cuando tenés todo, usá 'recomendar'.'''

messages = []
max_iteraciones = 6
iteracion = 0

messages.append(
    {
        'role': 'user', 
        'content': 'Necesito recomendación de vino.'
    }
)

while iteracion < max_iteraciones:
    response = client.messages.create(
        model='claude-sonnet-4-6',
        max_tokens=400,
        system=SYSTEM_SOMMELIER,
        messages=messages
    )

    raw = response.content[0].text.strip()
    if raw.startswith("```"):
        raw = raw.split("```")[1]
        if raw.startswith("json"):
            raw = raw[4:]
    decision = json.loads(raw.strip())
    print(f'Sommelier: {decision["mensaje"]}')

    if decision['accion'] == 'recomendar':
        print(f'\nVino sugerido: {decision["vino"]}')
        print(f'Motivo: {decision["motivo"]}')
        break

    user_input = input('Vos: ')
    messages.append({'role': 'assistant', 'content': response.content[0].text})
    messages.append({'role': 'user', 'content': user_input})
    iteracion += 1