from telegram import Update, InlineKeyboardButton, InlineKeyboardMarkup
from telegram.ext import Updater, CommandHandler, CallbackContext, CallbackQueryHandler
from apscheduler.schedulers.background import BackgroundScheduler
from sqlalchemy.orm import sessionmaker
from database import engine, Event, User

TOKEN = "7707609145:AAFU1fVID8Dbc4LCEgNKFQO7xhCApbSTOGo"
Session = sessionmaker(bind=engine)
scheduler = BackgroundScheduler()

# ---------------------- Команды для студентов ----------------------
def start(update: Update, context: CallbackContext):
    user_id = update.effective_chat.id
    session = Session()
    if not session.query(User).get(user_id):
        session.add(User(chat_id=user_id))
        session.commit()
    update.message.reply_text(
        "Добро пожаловать в агрегатор мероприятий КемГУ! 🎓\n"
        "Используйте /events для просмотра мероприятий."
    )

def show_events(update: Update, context: CallbackContext):
    buttons = [
        [InlineKeyboardButton("Фильтры", callback_data="open_filters")],
        [InlineKeyboardButton("Календарь", callback_data="open_calendar")]
    ]
    update.message.reply_text(
        "Выберите действие:",
        reply_markup=InlineKeyboardMarkup(buttons)
    )

# ---------------------- Фильтрация мероприятий ----------------------
def handle_filters(update: Update, context: CallbackContext):
    query = update.callback_query
    if query.data == "open_filters":
        buttons = [
            [InlineKeyboardButton("По дате", callback_data="filter_date")],
            [InlineKeyboardButton("По категории", callback_data="filter_category")],
            [InlineKeyboardButton("По месту", callback_data="filter_location")]
        ]
        query.edit_message_text("Выберите фильтр:", reply_markup=InlineKeyboardMarkup(buttons))

# ---------------------- Интерфейс администратора ----------------------
def admin_login(update: Update, context: CallbackContext):
    if context.args and context.args[0] == "mnjjkyr123$##":
        user_id = update.effective_chat.id
        session = Session()
        user = session.query(User).get(user_id)
        user.is_admin = True
        session.commit()
        update.message.reply_text("✅ Вы получили права администратора!")

def add_event(update: Update, context: CallbackContext):
    # Реализация пошагового добавления мероприятия
    pass

# ---------------------- Уведомления ----------------------
def send_notifications():
    session = Session()
    events = session.query(Event).filter(Event.date >= datetime.now()).all()
    for user in session.query(User):
        for event in events:
            context.bot.send_message(
                chat_id=user.chat_id,
                text=f"🔔 Напоминание: {event.title} состоится {event.date}!"
            )

scheduler.add_job(send_notifications, 'interval', hours=24)
scheduler.start()

# ---------------------- Запуск бота ----------------------
def main():
    updater = Updater(TOKEN)
    dp = updater.dispatcher

    dp.add_handler(CommandHandler("start", start))
    dp.add_handler(CommandHandler("events", show_events))
    dp.add_handler(CommandHandler("admin", admin_login))
    dp.add_handler(CallbackQueryHandler(handle_filters))

    updater.start_polling()
    updater.idle()

if name == "main":
    main()