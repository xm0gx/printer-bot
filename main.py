import telebot
import google.generativeai as genai
import os

# --- الإعدادات ---
# ملاحظة: يمكنك وضع التوكن مباشرة هنا أو استخدامه كمتغير بيئة (Environment Variable)
TELEGRAM_TOKEN = '8009820362:AAGxvyEweXIk4s5aTZmkhu7M5AwE3mltBFs'
GEMINI_API_KEY = 'AIzaSyDVkw61FRf-q8bfpcHgy1hRwyGpqHjZ-wk'

# إعداد الذكاء الاصطناعي - استخدام النسخة المستقرة gemini-1.5-flash
# مع إضافة منطق التحقق من الاتصال
genai.configure(api_key=GEMINI_API_KEY)
model = genai.GenerativeModel('gemini-1.5-flash')

bot = telebot.TeleBot(TELEGRAM_TOKEN)

def ai_repair_agent(error_code):
    """الوكيل الذكي لتحليل الأعطال"""
    prompt = f"""
    أنت خبير صيانة طابعات محترف في 'ورشة أور'.
    وصلك طلب لتحليل الكود التالي: {error_code}
    أجب بالترتيب التالي:
    1. Technical Analysis (English): شرح تقني دقيق للمشكلة.
    2. التشخيص والحل (بالعربية): شرح باللهجة العراقية أو العربية المبسطة، حدد القطعة (سخان، ليزر، بورد، حساس).
    3. خطوات الإصلاح: (1، 2، 3).
    
    إذا لم تكن متأكداً من الكود، اطلب من المستخدم تحديد نوع الطابعة (Canon, HP, Ricoh).
    """
    try:
        response = model.generate_content(prompt)
        return response.text
    except Exception as e:
        return f"⚠️ عذراً، هنالك مشكلة في الاتصال بخادم الذكاء الاصطناعي حالياً.\nالخطأ: {str(e)}"

@bot.message_handler(commands=['start'])
def send_welcome(message):
    welcome_text = (
        "🏢 **مرحباً بك في ورشة أور الذكية**\n"
        "━━━━━━━━━━━━━━━\n"
        "أنا وكيل صيانة مدعوم بالذكاء الاصطناعي.\n"
        "أرسل لي الماركة وكود العطل الآن.\n"
        "مثال: `Canon IR 2520 E001`"
    )
    bot.send_message(message.chat.id, welcome_text, parse_mode='Markdown')

@bot.message_handler(func=lambda message: True)
def handle_repair(message):
    query = message.text
    # إشعار المستخدم ببدء العمل
    processing_msg = bot.reply_to(message, "🤖 جاري تحليل الكود بواسطة AI Agent... انتظر لحظة")
    
    # الحصول على التشخيص من الوكيل الذكي
    result = ai_repair_agent(query)
    
    final_response = (
        f"🏢 *ورشة أور لصيانة الأجهزة*\n"
        f"━━━━━━━━━━━━━━━\n"
        f"{result}\n"
        f"━━━━━━━━━━━━━━━\n"
        f"📍 تم الفحص بواسطة نظام أور الذكي"
    )
    
    # تحديث الرسالة بالنتيجة النهائية
    try:
        bot.edit_message_text(final_response, chat_id=message.chat.id, message_id=processing_msg.message_id, parse_mode='Markdown')
    except:
        # في حال فشل التنسيق (Markdown)، نرسلها كنص عادي
        bot.send_message(message.chat.id, final_response)

# تشغيل البوت
if __name__ == "__main__":
    print("✅ بوت ورشة أور يعمل الآن...")
    bot.infinity_polling()
  
