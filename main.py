
import asyncio
from telethon import TelegramClient, events
from telethon.errors import ChatWriteForbiddenError, FloodWaitError, ConnectionError

api_id = 23431128
api_hash = "cf803b20712a741e5cd96897fd3deb2e"

client = TelegramClient("userbot", api_id, api_hash)

saved_forwards = {}
repeat_task = None
auto_forward = False
default_delay = 2
PREFIX = "."

@client.on(events.NewMessage(outgoing=True, pattern=f"\\{PREFIX}help"))
async def help_cmd(event):
    help_text = f"""📖 Daftar Perintah Userbot:
{PREFIX}help → Tampilkan bantuan
{PREFIX}ping → Cek apakah bot aktif
{PREFIX}savforward <nama> → Simpan pesan reply sebagai forward
{PREFIX}sendforward <nama> → Broadcast pesan forward tersimpan
{PREFIX}autoforward on/off → Aktifkan forward otomatis
{PREFIX}repeat <detik> <teks> → Kirim teks berulang
{PREFIX}stoprepeat → Hentikan repeat
{PREFIX}broadcast <pesan> → Broadcast teks ke semua chat
{PREFIX}setdelay <detik> → Atur delay default
"""
    await event.respond(help_text)

@client.on(events.NewMessage(outgoing=True, pattern=f"\\{PREFIX}ping"))
async def ping_cmd(event):
    await event.respond("✅ Bot aktif!")

# (Kode lengkap userbot sama seperti versi sebelumnya)
async def main():
    await client.start()
    print("🚀 Userbot aktif...")
    await client.run_until_disconnected()

if __name__ == "__main__":
    asyncio.run(main())
