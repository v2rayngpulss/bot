#!/bin/bash

# به‌روزرسانی و نصب پیش‌نیازها
echo "📦 نصب پیش‌نیازها..."
sudo apt update && sudo apt install python3 python3-pip -y

# دانلود اسکریپت پینگ بات از GitHub
echo "⬇️ دانلود اسکریپت از GitHub..."
git clone https://github.com/v2rayngpulss/bot.git || echo "📁 پوشه قبلاً وجود دارد."
cd bot || exit 1

# نصب کتابخانه‌های لازم
pip install -r requirements.txt || pip install pyTelegramBotAPI

# تنظیم توکن و آیدی کانال‌ها (مقادیر ثابت)
TOKEN="7658248071:AAE2svRF7rv46l7ZbWQHSYDp1sqZjr-Q8MA"
SUCCESS_ID="-1002586449276"  # پینگ عادی
FAIL_ID="-1002608599474"    # بد پینگ

# اجرای ربات در پس‌زمینه
echo "🚀 اجرای ربات در پس‌زمینه..."
nohup env TOKEN="$TOKEN" SUCCESS_ID="$SUCCESS_ID" FAIL_ID="$FAIL_ID" python3 ping-bot.py > bot.log 2>&1 &

echo "✅ ربات با موفقیت اجرا شد!"
echo "برای مشاهده لاگ‌ها دستور زیر را اجرا کنید:"
echo "tail -f bot/bot.log"
