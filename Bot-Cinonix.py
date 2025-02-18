import logging
from telegram import Update
from telegram.ext import Application, CommandHandler, MessageHandler, filters, ContextTypes
from fastapi import FastAPI, Request
from fastapi.responses import JSONResponse
import os

TOKEN = os.getenv("BOT_TOKEN")  # Obtiene el token desde las variables de entorno
WEBHOOK_URL = os.getenv("WEBHOOK_URL")  # URL del webhook en Vercel

app = FastAPI()

# Configuración de logging
logging.basicConfig(level=logging.INFO)

RESPUESTAS = {
    ('pago', 'precio', 'costo', '19.99'): (
        "🎬 ¡Disfruta películas y series para toda la vida por un único pago de **19.99 €**! 💶\n\n"
        "✅ Acceso **vitalicio**, sin mensualidades.\n"
        "📲 Disponible desde **Telegram** o en nuestra **app oficial**.\n"
        "🪙 Aceptamos pagos en criptomonedas y euros.\n\n"
        "🔗 **Compra ahora**: [Clic aquí](https://cinonix.vercel.app/)\n\n"
        "📌 **Desde Telegram**: Usa el botón de acceso en la web."
    ),
}

# Configurar el bot
application = Application.builder().token(TOKEN).build()
application.add_handler(CommandHandler('start', lambda update, context: update.message.reply_text(
    "👋 ¡Hola! Soy el asistente de **Cinonix** 🎬\n\n"
    "📺 **Mira películas y series para siempre** por solo **19.99 €** 💶\n"
    "📲 **Desde Telegram** o descargando nuestra **app**.\n\n"
    "💡 Pregunta sobre:\n"
    "• Pagos 💳\n"
    "• Acceso 🔑\n"
    "• Problemas técnicos ⚠️\n"
    "• Soporte 🛠️\n\n"
    "🛒 **Compra aquí**: [Clic aquí](https://cinonix.vercel.app/)"
)))

application.add_handler(MessageHandler(filters.TEXT, lambda update, context: update.message.reply_text(
    RESPUESTAS.get(tuple(word for word in update.message.text.lower().split()), "❌ No entendí tu consulta\nUsa /help para ver temas disponibles")
)))

# Webhook handler
@app.post("/api/webhook")
async def webhook(request: Request):
    json_body = await request.json()
    update = Update.de_json(json_body, application.bot)
    await application.process_update(update)
    return JSONResponse(content={"status": "ok"})

# Ruta para configurar el webhook
@app.get("/set-webhook")
async def set_webhook():
    url = f"{WEBHOOK_URL}/api/webhook"
    response = await application.bot.set_webhook(url)
    return JSONResponse(content={"webhook_set": response})
