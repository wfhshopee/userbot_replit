import asyncio
import os
import sqlite3
from telegram import Update
from telegram.ext import Application, CommandHandler, ContextTypes

# === Database ===
conn = sqlite3.connect("botdata.db", check_same_thread=False)
cur = conn.cursor()
cur.execute("CREATE TABLE IF NOT EXISTS users (chat_id INTEGER PRIMARY KEY)")
conn.commit()

delay = 3
autobc_on = False
saved_message = None

# === Fungsi bantu ===
def add_user(chat_id):
    cur.execute("INSERT OR IGNORE INTO users (chat_id) VALUES (?)", (chat_id,))
    conn.commit()

def get_users():
    cur.execute("SELECT chat_id FROM users")
    return [row[0] for row in cur.fetchall()]

# === Command ===
async def start(update: Update, context: ContextTypes.DEFAULT_TYPE):
    add_user(update.effective_chat.id)
    await update.message.reply_text("✅ Kamu sudah terdaftar untuk broadcast.")

async def autobc_add(update: Update, context: ContextTypes.DEFAULT_TYPE):
    global saved_message
    if update.message.reply_to_message:
        saved_message = update.message.reply_to_message
        await update.message.reply_text("✅ Pesan berhasil ditambahkan ke daftar broadcast.")
    else:
        await update.message.reply_text("❌ Harus reply ke pesan yang mau disimpan.")

async def autobc_delay(update: Update, context: ContextTypes.DEFAULT_TYPE):
    global delay
    try:
        delay = int(context.args[0])
        await update.message.reply_text(f"⏱ Delay diatur ke {delay} detik.")
    except:
        await update.message.reply_text("❌ Format salah. Contoh: .autobc_delay 5")

async def autobc_on_cmd(update: Update, context: ContextTypes.DEFAULT_TYPE):
    global autobc_on
    autobc_on = True
    await update.message.reply_text("🚀 Auto Broadcast dimulai...")

    if saved_message:
        users = get_users()
        success, failed = 0, 0
        for uid in users:
            try:
                await saved_message.copy(chat_id=uid)
                success += 1
            except:
                failed += 1
            await asyncio.sleep(delay)
        await update.message.reply_text(f"📢 Broadcast selesai!\n✅ {success} sukses\n❌ {failed} gagal")
    else:
        await update.message.reply_text("⚠️ Belum ada pesan untuk broadcast.")

async def autobc_off_cmd(update: Update, context: ContextTypes.DEFAULT_TYPE):
    global autobc_on
    autobc_on = False
    await update.message.reply_text("⛔ Auto Broadcast dimatikan.")

async def autobc_status(update: Update, context: ContextTypes.DEFAULT_TYPE):
    users = get_users()
    total_users = len(users)
    await update.message.reply_text(
        f"📊 Status Broadcast\n"
        f"AutoBC: {'✅ ON' if autobc_on else '❌ OFF'}\n"
        f"Delay: {delay} detik\n"
        f"User/Grup terdaftar: {total_users}\n"
        f"Pesan tersimpan: {'✅ Ada' if saved_message else '❌ Tidak ada'}"
    )

# === Main ===
if __name__ == "__main__":
    TOKEN = os.getenv("BOT_TOKEN")  # simpan token di environment variable
    app = Application.builder().token(TOKEN).build()

    app.add_handler(CommandHandler("start", start))
    app.add_handler(CommandHandler("autobc_add", autobc_add))
    app.add_handler(CommandHandler("autobc_delay", autobc_delay))
    app.add_handler(CommandHandler("autobc_on", autobc_on_cmd))
    app.add_handler(CommandHandler("autobc_off", autobc_off_cmd))
    app.add_handler(CommandHandler("autobc_status", autobc_status))

    print("🤖 Bot berjalan 24 jam...")
    app.run_polling()
