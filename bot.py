cat <<EOF > bot.py
import telebot
import google.generativeai as genai
import PIL.Image
import os

TG_TOKEN = "8616125372:AAFPRxzh90kRSyFEgKeSi2mzFjhz1FWXgMs"
GOOGLE_API_KEY = "AIzaSyBI-y4bWb1bwUiYqy69omEup1q4DxklukE"

genai.configure(api_key=GOOGLE_API_KEY)
model = genai.GenerativeModel('gemini-1.5-flash')
bot = telebot.TeleBot(TG_TOKEN)

@bot.message_handler(content_types=['text', 'photo'])
def handle_message(message):
    try:
        if message.content_type == 'text':
            response = model.generate_content(message.text)
            bot.reply_to(message, response.text)
        elif message.content_type == 'photo':
            file_info = bot.get_file(message.photo[-1].file_id)
            downloaded_file = bot.download_file(file_info.file_path)
            with open("temp.jpg", "wb") as f:
                f.write(downloaded_file)
            img = PIL.Image.open("temp.jpg")
            caption = message.caption if message.caption else "Что на фото?"
            response = model.generate_content([caption, img])
            bot.reply_to(message, response.text)
    except Exception as e:
        bot.reply_to(message, f"Ошибка: {str(e)}")

if __name__ == "__main__":
    print("Бот запущен...")
    bot.polling(none_stop=True)
EOF
