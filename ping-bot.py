import telebot
import subprocess
import threading
import time

# دریافت توکن و آیدی کانال‌ها از کاربر
TOKEN = input('🔑 توکن ربات را وارد کنید: ')
CHAT_ID_SUCCESS = input('📢 آیدی کانال موفقیت را وارد کنید: ')
CHAT_ID_FAIL = input('📢 آیدی کانال خطا را وارد کنید: ')

# لیست IPها برای پینگ گرفتن
ip_list = []

# ساخت ربات
bot = telebot.TeleBot(TOKEN)

# تابع پینگ گرفتن
def ping_ip(ip):
    try:
        result = subprocess.run(['ping', '-c', '3', ip], stdout=subprocess.PIPE, stderr=subprocess.PIPE)
        if result.returncode == 0:
            bot.send_message(CHAT_ID_SUCCESS, f'✅ آی‌پی {ip} در دسترس است.')
        else:
            bot.send_message(CHAT_ID_FAIL, f'⚠️ خطا: عدم دسترسی به {ip}')
    except Exception as e:
        bot.send_message(CHAT_ID_FAIL, f'❌ خطای داخلی: {e}')

# اجرای دائمی پینگ
def ping_loop():
    while True:
        for ip in ip_list:
            ping_ip(ip)
        time.sleep(60)  # هر 60 ثانیه یک بار پینگ می‌گیرد

# فرمان برای افزودن IP
@bot.message_handler(commands=['add_ip'])
def add_ip(message):
    try:
        ip = message.text.split()[1]
        if ip not in ip_list:
            ip_list.append(ip)
            bot.reply_to(message, f'✅ آی‌پی {ip} اضافه شد.')
        else:
            bot.reply_to(message, f'ℹ️ آی‌پی {ip} از قبل موجود است.')
    except IndexError:
        bot.reply_to(message, '❗ لطفاً آی‌پی را وارد کنید: /add_ip [آی‌پی]')

# فرمان برای حذف IP
@bot.message_handler(commands=['remove_ip'])
def remove_ip(message):
    try:
        ip = message.text.split()[1]
        if ip in ip_list:
            ip_list.remove(ip)
            bot.reply_to(message, f'✅ آی‌پی {ip} حذف شد.')
        else:
            bot.reply_to(message, f'ℹ️ آی‌پی {ip} یافت نشد.')
    except IndexError:
        bot.reply_to(message, '❗ لطفاً آی‌پی را وارد کنید: /remove_ip [آی‌پی]')

# فرمان برای نمایش IPها
@bot.message_handler(commands=['list_ip'])
def list_ip(message):
    if ip_list:
        bot.reply_to(message, '📋 لیست آی‌پی‌ها:\n' + '\n'.join(ip_list))
    else:
        bot.reply_to(message, 'ℹ️ لیست آی‌پی‌ها خالی است.')

# اجرای پینگ در رشته جداگانه
ping_thread = threading.Thread(target=ping_loop)
ping_thread.daemon = True
ping_thread.start()

# اجرای ربات
bot.polling()
