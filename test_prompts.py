"""Test prompts manually."""

from src.niveles import _llamar_modelo

texto = """¿Alguien sabe como configurar el timeout en una conexión HTTP con Python? 
Estoy usando la librería requests y a veces se queda colgado cuando el servidor tarda más de 10 segundos."""

print("=== SENTIMIENTO ===")
r = _llamar_modelo(
    """Responde SIEMPRE asi: {"sentimiento":"valor","puntuacion":0.0,"emociones":["a"],"confianza":0.0}
Valor de sentimiento debe ser: positivo, negativo o neutral
Ejemplo para pregunta técnica: {"sentimiento":"neutral","puntuacion":0.5,"emociones":["curiosidad"],"confianza":0.8}""",
    texto,
    modelo="qwen2.5:3b"
)
print(r)
print()

print("=== ENTIDADES ===")
r = _llamar_modelo(
    """Responde SIEMPRE asi: {"personas":[],"organizaciones":[],"lugares":[],"fechas":[],"cantidades":[],"otros":[]}
Si mentionas Python, HTTP, agregar a "otros"
Ejemplo: {"personas":[],"organizaciones":["empresa X"],"lugares":[],"fechas":["hoy"],"cantidades":["10"],"otros":["Python","HTTP","timeout"]}""",
    texto,
    modelo="qwen2.5:3b"
)
print(r)
print()

print("=== INTENCION ===")
r = _llamar_modelo(
    """Responde SIEMPRE asi: {"intencion_principal":"","subcategoria":"","urgencia":"","accion_sugerida":""}
Urgencia debe ser: alta, media o baja
Intencion principal debe ser: informacion, compra, soporte, queja, sugerencia
Ejemplo pregunta técnica: {"intencion_principal":"informacion","subcategoria":"ayuda tecnica","urgencia":"media","accion_sugerida":"responder"}""",
    texto,
    modelo="qwen2.5:3b"
)
print(r)
print()

print("=== CLASIFICACION ===")
r = _llamar_modelo(
    """Responde SIEMPRE asi: {"tema":"","tipo":"","canal_adecuado":"","prioridad":3}
Tema debe ser: tecnico, facturacion, cuenta, producto, servicio_cliente, otro
Tipo debe ser: pregunta, queja, sugerencia, informacion, solicitud
Canal debe ser: email, chat, telefono, automatico
Prioridad entre 1 y 5
Ejemplo pregunta técnica: {"tema":"tecnico","tipo":"pregunta","canal_adecuado":"chat","prioridad":3}""",
    texto,
    modelo="qwen2.5:3b"
)
print(r)
print()

print("=== RESUMEN ===")
r = _llamar_modelo(
    "Responde solo con el resumen en maximo 3 frases.",
    texto,
    modelo="qwen2.5:3b"
)
print(r)