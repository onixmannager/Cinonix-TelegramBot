import logging
from telegram import Update
from telegram.ext import Application, CommandHandler, MessageHandler, filters, ContextTypes

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
    
    ('cripto', 'criptomonedas', 'bitcoin'): (
        "🪙 **Aceptamos pagos en criptomonedas**:\n\n"
        "• Bitcoin (BTC)\n"
        "• Ethereum (ETH)\n"
        "• Litecoin (LTC)\n\n"
        "El monto a pagar es **19.99 €**, convertido a la cripto en el momento del pago.\n\n"
        "🔗 **Paga aquí**: [Clic aquí](https://cinonix.vercel.app/)"
    ),
    
    ('link', 'pagina', 'web', 'landing'): (
        "🌍 **Nuestra página oficial**:\n"
        "🔗 [Cinonix](https://cinonix.vercel.app/)\n\n"
        "📲 **Desde ahí puedes**:\n"
        "• Realizar el pago\n"
        "• Descargar la app\n"
        "• Acceder desde Telegram\n"
        "• Ver tutoriales\n"
        "• Contactar soporte"
    ),
    
    ('problema', 'error', 'fallo', 'soporte'): (
        "🚨 **¿Tienes problemas?**\n\n"
        "1️⃣ Revisa tu conexión a Internet.\n"
        "2️⃣ Borra la caché de tu navegador.\n"
        "3️⃣ Prueba en modo incógnito.\n\n"
        "📩 **Soporte técnico**: soporte@cinonix.com"
    ),
    
    ('acceso', 'login', 'entrar'): (
        "🔑 **Cómo acceder**:\n\n"
        "1️⃣ Completa el pago.\n"
        "2️⃣ Recibirás un email de confirmación.\n"
        "3️⃣ Sigue las instrucciones del email.\n"
        "4️⃣ Accede desde **Telegram** o la **app**.\n\n"
        "🔗 **Ir a la web**: [Cinonix](https://cinonix.vercel.app/)"
    ),
    
    ('refund', 'reembolso', 'devolución'): (
        "🔙 **Política de reembolsos**:\n\n"
        "• Devoluciones dentro de los primeros **3 días**.\n"
        "• Contactar a **soporte@cinonix.com**.\n"
        "• El proceso tarda **24-48 horas**.\n"
        "• **Solo válido para la primera compra**."
    )
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

async def help(update: Update, context: ContextTypes.DEFAULT_TYPE):
    await update.message.reply_text(
        "🔍 **Comandos disponibles**:\n"
        "/start - Iniciar el bot\n"
        "/help - Ver esta ayuda\n\n"
        "ℹ️ **Puedes preguntar sobre**:\n"
        "✔️ Formas de pago (cripto/€)\n"
        "✔️ Problemas técnicos\n"
        "✔️ Acceso al servicio\n"
        "✔️ Política de reembolsos\n"
        "✔️ Enlace a la web oficial"
    )

# Manejar mensajes
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

# Manejar errores
async def error(update: Update, context: ContextTypes.DEFAULT_TYPE):
    logging.error(f'Update {update} caused error {context.error}')

# Configurar el bot
def main():
    application = Application.builder().token('7853341824:AAEyF41qfBAJnafm_8jI6U3ZPblmg3kZAOs').build()  # Reemplazar con tu token
    
    # Handlers
    application.add_handler(CommandHandler('start', start))
    application.add_handler(CommandHandler('help', help))
    application.add_handler(MessageHandler(filters.TEXT, handle_message))
    
    # Error handler
    application.add_error_handler(error)
    
    # Iniciar bot
    application.run_polling()

if __name__ == '__main__':
    main()
