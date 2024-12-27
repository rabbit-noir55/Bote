import os
import telebot
from yt_dlp import YoutubeDL
from telebot.types import InputMediaVideo

# Telegram bot tokenini kiriting
BOT_TOKEN = "8072140256:AAGJP8_1wlMwUKQpJkXMm8PoSGzNOQnRSSo"
bot = telebot.TeleBot(BOT_TOKEN)

# Yuklab olingan fayllarni saqlash uchun papka
DOWNLOAD_FOLDER = "downloads"

if not os.path.exists(DOWNLOAD_FOLDER):
    os.mkdir(DOWNLOAD_FOLDER)

# Video yuklash funksiyasi
def download_video(url):
    try:
        ydl_opts = {
            'format': 'best',  # Eng yaxshi sifatdagi video
            'outtmpl': os.path.join(DOWNLOAD_FOLDER, '%(title)s.%(ext)s'),  # Fayl nomini sozlash
            'quiet': True,  # Konsolda ortiqcha ma'lumot ko'rsatmaslik
        }
        with YoutubeDL(ydl_opts) as ydl:
            info = ydl.extract_info(url, download=True)
            file_path = ydl.prepare_filename(info)
        return file_path, info['title']
    except Exception as e:
        raise Exception(f"Video yuklashda xatolik: {str(e)}")

# Yuklangan faylni xavfsiz o‘chirish funksiyasi
def safe_remove(file_path):
    try:
        if os.path.exists(file_path):
            os.remove(file_path)
    except Exception as e:
        print(f"Faylni o‘chirishda xatolik: {str(e)}")

@bot.message_handler(commands=['start', 'help'])
def send_welcome(message):
    bot.reply_to(
        message,
        "Salom! Menga YouTube video yoki playlist URL yuboring. Men videoni yuklab, sizga yuboraman."
    )

@bot.message_handler(func=lambda message: True)
def handle_message(message):
    url = message.text.strip()
    
    # URL tekshirish
    if not ("youtube.com" in url or "youtu.be" in url):
        bot.reply_to(message, "Bu haqiqiy YouTube URL emas! Iltimos, to‘g‘ri link yuboring.")
        return

    bot.reply_to(message, "Videoni yuklab olishni boshlayapman. Kuting...")
    
    try:
        # Videoni yuklash
        video_path, title = download_video(url)
        bot.send_message(message.chat.id, f"Video topildi: {title}. Yuklash tugadi, yuboryapman...")
        
        # Videoni yuborish
        with open(video_path, "rb") as video:
            bot.send_video(message.chat.id, video)

        bot.send_message(message.chat.id, "Video muvaffaqiyatli yuborildi.")
    
    except Exception as e:
        bot.send_message(message.chat.id, f"Xatolik yuz berdi: {str(e)}")

    finally:
        # Faylni xavfsiz o‘chirish
        safe_remove(video_path)

# Botni ishga tushirish
try:
    bot.polling()
except Exception as e:
    print(f"Botni ishga tushirishda xatolik: {str(e)}")