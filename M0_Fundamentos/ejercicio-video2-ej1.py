import anthropic

# El cliente toma la API key de la variable de entorno ANTHROPIC_API_KEY
# client = anthropic.Anthropic()

# response = client.messages.create(
#     model="claude-haiku-4-5-20251001",  # modelo rápido — tarea simple
#     max_tokens=150,
#     messages=[
#         {
#             "role": "user",
#             "content": "Spider-Man acaba de salvar a 30 personas de un incendio. Escribí un titular para el Daily Bugle."
#        }
#     ]
# )

# print(response.content[0].text)

response = client.messages.create(
    model="claude-haiku-4-5-20251001",
    max_tokens=150,
    system="""Sos J. Jonah Jameson, editor jefe del Daily Bugle de Nueva York.
    Sos temperamental, dramático, y estás convencido de que Spider-Man es
    una amenaza pública, un vigilante irresponsable y un peligro para la ciudad.
    No importa lo que Spider-Man haya hecho — siempre encontrás el ángulo negativo.
    Tus titulares son sensacionalistas, exagerados y completamente sesgados.
    Respondés SOLO con el titular. Sin explicaciones. Sin contexto. Solo el titular.""",
    messages=[
        {
            "role": "user",
            "content": "Spider-Man acaba de salvar a 30 personas de un incendio."
        }
    ]
)

print(response.content[0].text)
