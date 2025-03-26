#!/bin/bash

# نصب پیش‌نیازها
echo "📦 نصب پیش‌نیازها..."
sudo apt update && sudo apt install python3 python3-pip python3-venv git -y

# دانلود اسکریپت پینگ بات از GitHub
echo "⬇️ دانلود اسکریپت از GitHub..."
git clone https://github.com/v2rayngpulss/bot.git || echo "📁 پوشه قبلاً وجود دارد."
cd bot || exit 1

# ساخت محیط مجازی
echo "🧑‍💻 ایجاد محیط مجازی..."
python3 -m venv botenv

# فعال‌سازی محیط مجازی
source botenv/bin/activate

# نصب کتابخانه‌ها
echo "📚 نصب کتابخانه‌ها..."
pip install pyTelegramBotAPI

# اجرای ربات
echo "🚀 اجرای ربات..."
nohup python3 ping-bot.py > bot.log 2>&1 &

echo "✅ ربات با موفقیت اجرا شد!"
echo "برای مشاهده لاگ‌ها دستور زیر را اجرا کنید:"
echo "tail -f bot.log"
