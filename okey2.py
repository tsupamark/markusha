from telegram import Update, Message
from telegram.ext import Application, MessageHandler, filters, CommandHandler, ContextTypes

# 🔧 Настройки
BOT_TOKEN = '8098121171:AAGcumK5w_5PAn6Pk-LNafIWSiSstaJdZeA'
ADMIN_ID = 7756306224  # Замени на свой Telegram user ID

# 🟢 Команда /start
async def start(update: Update, context: ContextTypes.DEFAULT_TYPE):
    await update.message.reply_text("Привет! Напиши сюда сообщение, и администратор свяжется с тобой.")

# 📥 Обработка входящих сообщений от пользователей
async def forward_to_admin(update: Update, context: ContextTypes.DEFAULT_TYPE):
    user = update.message.from_user
    message = update.message
    text = f"📩 Сообщение от @{user.username or user.id} (ID: {user.id}):\n\n{message.text}"

    # Пересылаем админу
    forwarded = await context.bot.send_message(chat_id=ADMIN_ID, text=text)

    # Сохраняем соответствие: id сообщения -> id пользователя
    context.chat_data[forwarded.message_id] = user.id

# 🔁 Ответ администратора
async def handle_admin_reply(update: Update, context: ContextTypes.DEFAULT_TYPE):
    if update.effective_user.id != ADMIN_ID:
        return  # Только админ может отвечать

    replied_msg: Message = update.message.reply_to_message
    if not replied_msg:
        return

    original_user_id = context.chat_data.get(replied_msg.message_id)
    if not original_user_id:
        await update.message.reply_text("❗ Не удалось найти получателя.")
        return

    await context.bot.send_message(chat_id=original_user_id, text=f"📬 Ответ от администратора:\n\n{update.message.text}")

# 🚀 Запуск
def main():
    app = Application.builder().token(BOT_TOKEN).build()

    app.add_handler(CommandHandler("start", start))
    app.add_handler(MessageHandler(filters.TEXT & ~filters.COMMAND, forward_to_admin))
    app.add_handler(MessageHandler(filters.TEXT & filters.USER(ADMIN_ID), handle_admin_reply))

    print("Бот запущен...")
    app.run_polling()

if __name__ == "__main__":
    main()
