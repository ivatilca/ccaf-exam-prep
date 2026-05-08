import anthropic

client = anthropic.Anthropic()

SYSTEM_HERMIONE = '''Sos Hermione: analista de hechos.
Dado un texto, identificá:
- Afirmaciones verificables vs. especulación
- Posibles inconsistencias o información faltante
- Nivel de credibilidad del contenido
Respondé en formato de reporte breve. Sé precisa y directa.'''

SYSTEM_RON = '''Sos Ron: comunicador de impacto.
Dado un texto, explicá:
- Qué significa esto para una persona común
- Por qué debería importarle
- Una sola frase que resume el punto principal
Usá lenguaje simple, sin tecnicismos.'''

SYSTEM_DUMBLEDORE = '''Sos Dumbledore: sintetizador de inteligencia.
Recibirás dos reportes sobre el mismo tema:
uno de análisis de hechos y uno de impacto en lenguaje simple.
Tu tarea: integrá ambas perspectivas en una conclusión breve
que combine rigor con claridad. Máximo 3 oraciones.'''

def hermione_analiza(texto):
    resp = client.messages.create(
        model='claude-sonnet-4-6',
        max_tokens=400,
        system=SYSTEM_HERMIONE,
        messages=[{'role':'user','content':f'Analizá este texto:\n{texto}'}]
    )
    return resp.content[0].text

def ron_explica(texto):
    resp = client.messages.create(
        model='claude-haiku-4-5-20251001',
        max_tokens=250,
        system=SYSTEM_RON,
        messages=[{'role':'user','content':f'Explicá este texto:\n{texto}'}]
    )
    return resp.content[0].text

def dumbledore_sintetiza(reporte_hermione, reporte_ron):
    prompt = f'''Reporte de Hermione (análisis de hechos):
{reporte_hermione}

Reporte de Ron (impacto en lenguaje simple):
{reporte_ron}

Integrá ambos en una conclusión final.'''
    resp = client.messages.create(
        model='claude-sonnet-4-6',
        max_tokens=300,
        system=SYSTEM_DUMBLEDORE,
        messages=[{'role':'user','content':prompt}]
    )
    return resp.content[0].text

noticia = '''
El Ministerio de Magia anunció hoy nuevas restricciones
al uso de magia en zonas no mágicas. Funcionarios indicaron
que los incidentes han aumentado un 40% este año,
aunque no presentaron datos de respaldo para esa cifra.
'''

print('La Orden del Fénix analiza...')
print()

reporte_h = hermione_analiza(noticia)
reporte_r = ron_explica(noticia)

print('=== Hermione (análisis de hechos) ===')
print(reporte_h)
print()
print('=== Ron (impacto simple) ===')
print(reporte_r)
print()

conclusion = dumbledore_sintetiza(reporte_h, reporte_r)
print('=== Dumbledore (síntesis final) ===')
print(conclusion)
