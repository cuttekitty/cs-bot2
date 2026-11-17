import telebot
from telebot.types import BotCommand
import a2s

BOT_TOKEN = "8868023526:AAEFf4lPjpjaW_Ty7gO_cJrd1PgWOF1K4OQ"
SERVER_IP = "91.211.118.26"
SERVER_PORT = 27015

bot = telebot.TeleBot(BOT_TOKEN)

# Регистрируем кнопку меню возле скрепки
def setup_bot_commands():
    commands = [
        BotCommand("server", "🎮 Онлайн та статистика сервера"),
        BotCommand("status", "🗺 Карта та гравці"),
        BotCommand("start", "🔄 Перезапустити бота")
    ]
    bot.set_my_commands(commands)

def get_server_stats():
    address = (SERVER_IP, SERVER_PORT)
    try:
        info = a2s.info(address, timeout=4.0)
        players = a2s.players(address, timeout=4.0)
    except Exception as e:
        return f"⚠️ Не вдалося отримати дані з сервера:\n<code>{e}</code>"

    sorted_players = sorted(players, key=lambda p: p.score, reverse=True)

    text_lines = [
        f"🎮 <b>{info.server_name}</b>",
        f"🌐 <b>IP:</b> <code>{SERVER_IP}:{SERVER_PORT}</code>",
        f"🗺 <b>Карта:</b> <code>{info.map_name}</code>",
        f"👥 <b>Гравці:</b> {info.player_count}/{info.max_players}",
        ""
    ]

    medals = ["🥇", "🥈", "🥉"]

    for idx, p in enumerate(sorted_players):
        name = p.name.strip() if p.name else "Завантаження..."
        icon = medals[idx] if idx < 3 else "🎮"
        text_lines.append(f"{icon} <b>{name}</b> — {p.score} вбивств")

    if not sorted_players:
        text_lines.append("<i>На сервері зараз порожньо</i>")

    return "\n".join(text_lines)

@bot.message_handler(commands=['start', 'server', 'status', 'online'])
def handle_commands(message):
    status_text = get_server_stats()
    bot.send_message(message.chat.id, status_text, parse_mode="HTML")

@bot.message_handler(func=lambda msg: True)
def handle_all_messages(message):
    bot.reply_to(message, "Натисни кнопку «Меню» біля скріпки або напиши /server!")

# Устанавливаем команды и запускаем
setup_bot_commands()
print(">>> БОТ ПРАЦЮЄ З КНОПКОЮ МЕНЮ!")
bot.infinity_polling(timeout=10, long_polling_timeout=5)