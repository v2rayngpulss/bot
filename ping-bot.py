import telebot
import subprocess
import threading
import time

# دریافت ورودی‌ها از کاربر
TOKEN = '7658248071:AAE2svRF7rv46l7ZbWQHSYDp1sqZjr-Q8MA'
CHAT_ID_SUCCESS = '-1002586449276'  # آیدی کانال موفقیت
CHAT_ID_FAIL = '-1002608599474'     # آیدی کانال خطا
ADMINS = ['6175707321']  # آیدی ادمین‌ها

# لیست IPها
ip_list = []

# ساخت ربات
bot = telebot.TeleBot(TOKEN)

# تابع بررسی دسترسی ادمین
def is_admin(user_id):
    return str(user_id) in ADMINS

# تابع پینگ گرفتن
def ping_ip(ip):
    try:
        # پینگ کردن آی‌پی و بررسی نتیجه
        result = subprocess.run(['ping', '-n', '3', ip], stdout=subprocess.PIPE, stderr=subprocess.PIPE, text=True)
        
        # بررسی وضعیت پینگ
        if result.returncode == 0:
            bot.send_message(CHAT_ID_SUCCESS, f'✅ آی‌پی {ip} در دسترس است.')
        else:
            bot.send_message(CHAT_ID_FAIL, f'⚠️ خطا: عدم دسترسی به {ip}')
    except Exception as e:
        bot.send_message(CHAT_ID_FAIL, f'❌ خطای داخلی: {e}')

# حلقه‌ی دائمی برای پینگ گرفتن
def ping_loop():
    while True:
        if ip_list:
            for ip in ip_list:
                ping_ip(ip)
        time.sleep(5)  # هر ۵ ثانیه یک‌بار پینگ می‌گیرد

# افزودن آی‌پی
def add_ip(user_id, ip):
    if is_admin(user_id):
        if ip not in ip_list:
            ip_list.append(ip)
            return f'✅ آی‌پی {ip} اضافه شد.'
        else:
            return f'ℹ️ آی‌پی {ip} از قبل موجود است.'
    else:
        return '🚫 شما مجوز انجام این عملیات را ندارید.'

# حذف آی‌پی
def remove_ip(user_id, ip):
    if is_admin(user_id):
        if ip in ip_list:
            ip_list.remove(ip)
            return f'✅ آی‌پی {ip} حذف شد.'
        else:
            return f'ℹ️ آی‌پی {ip} یافت نشد.'
    else:
        return '🚫 شما مجوز انجام این عملیات را ندارید.'

# فرمان‌های ربات
@bot.message_handler(commands=['add_ip'])
def handle_add_ip(message):
    try:
        ip = message.text.split()[1]
        response = add_ip(message.from_user.id, ip)
        bot.reply_to(message, response)
    except IndexError:
        bot.reply_to(message, '❗ لطفاً آی‌پی را وارد کنید: /add_ip [آی‌پی]')

@bot.message_handler(commands=['remove_ip'])
def handle_remove_ip(message):
    try:
        ip = message.text.split()[1]
        response = remove_ip(message.from_user.id, ip)
        bot.reply_to(message, response)
    except IndexError:
        bot.reply_to(message, '❗ لطفاً آی‌پی را وارد کنید: /remove_ip [آی‌پی]')

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
