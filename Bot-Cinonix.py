import logging
from telegram import Update
from telegram.ext import Application, CommandHandler, MessageHandler, filters, ContextTypes
from fastapi import FastAPI, Request
from fastapi.responses import JSONResponse

app = FastAPI()

# Configuración básica de logging
logging.basicConfig(
    format='%(asctime)s - %(name)s - %(levelname)s - %(message)s',
    level=logging.INFO
)

RESPUESTAS = {
    ('pago', 'precio', 'costo', '19.99'): (
        "🎬 ¡Disfruta películas y series para toda la vida por un único pago de **19.99 €**! 💶\n\n"
        "✅ Acceso **vitalicio**, sin mensualidades.\n"
        "📲 Disponible desde **Telegram** o en nuestra **app oficial**.\n"
        "🪙 Aceptamos pagos en criptomonedas y euros.\n\n"
        "🔗 **Compra ahora**: [Clic aquí](https://cinonix.vercel.app/)\n\n"
        "📌 **Desde Telegram**: Usa el botón de acceso en la web."
    ),
    # ... tus otras respuestas
}

async def start(update: Update, context: ContextTypes.DEFAULT_TYPE):
    await update.message.reply_text(
        "👋 ¡Hola! Soy el asistente de **Cinonix** 🎬\n\n"
        "📺 **Mira películas y series para siempre** por solo **19.99 €** 💶\n"
        "📲 **Desde Telegram** o descargando nuestra **app**.\n\n"
        "💡 Pregunta sobre:\n"
        "• Pagos 💳\n"
        "• Acceso 🔑\n"
        "• Problemas técnicos ⚠️\n"
        "• Soporte 🛠️\n\n"
        "🛒 **Compra aquí**: [Clic aquí](https://cinonix.vercel.app/)"
    )

async def handle_message(update: Update, context: ContextTypes.DEFAULT_TYPE):
    text = update.message.text.lower()
    response = None
    
    for keywords, answer in RESPUESTAS.items():
        if any(keyword in text for keyword in keywords):
            response = answer
            break
            
    if not response:
        response = "❌ No entendí tu consulta\nUsa /help para ver temas disponibles"
    
    await update.message.reply_text(response)

# Webhook handler
@app.post("/webhook")
async def webhook(request: Request):
    json_body = await request.json()
    update = Update.de_json(json_body, application.bot)
    await application.process_update(update)
    return JSONResponse(content={"status": "ok"})

# Configurar el bot
def main():
    global application
    application = Application.builder().token('YOUR_BOT_TOKEN').build()  # Reemplazar con tu token
    # Handlers
    application.add_handler(CommandHandler('start', start))
    application.add_handler(MessageHandler(filters.TEXT, handle_message))
    
    # Iniciar el bot de Telegram
    application.run_polling(drop_pending_updates=True, allowed_updates=Update.ALL_TYPES)

if __name__ == '__main__':
    main()
