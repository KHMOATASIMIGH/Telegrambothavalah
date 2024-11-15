from telegram import Update
from telegram.ext import Application, CommandHandler, MessageHandler, filters, ConversationHandler, CallbackContext

# وضعیت‌های مختلف ربات
HVALA_NUMBER, HVALA, SENDERS, RECEIVERS, AMOUNT, DETAILS = range(6)

# ذخیره‌سازی ورودی‌های کاربر
user_data = {}

# شروع فرآیند دریافت اطلاعات
async def start(update: Update, context: CallbackContext):
    await update.message.reply_text("سلام! لطفاً نمبر حواله خود را وارد کنید.")
    return HVALA_NUMBER

# مرحله دریافت نمبر حواله
async def get_hvala_number(update: Update, context: CallbackContext):
    user_data[update.message.chat_id] = {'hvala_number': update.message.text}
    await update.message.reply_text("لطفاً محل حواله خودتان را بنویسید.")
    return HVALA

# مرحله دریافت حواله
async def get_hvala(update: Update, context: CallbackContext):
    user_data[update.message.chat_id]['hvala'] = update.message.text
    await update.message.reply_text("لطفاً فرستنده را وارد کنید.")
    return SENDERS

# مرحله دریافت فرستنده
async def get_senders(update: Update, context: CallbackContext):
    user_data[update.message.chat_id]['sender'] = update.message.text
    await update.message.reply_text("لطفاً گیرنده را وارد کنید.")
    return RECEIVERS

# مرحله دریافت گیرنده
async def get_receivers(update: Update, context: CallbackContext):
    user_data[update.message.chat_id]['receiver'] = update.message.text
    await update.message.reply_text("لطفاً مبلغ را وارد کنید.")
    return AMOUNT

# مرحله دریافت مبلغ
async def get_amount(update: Update, context: CallbackContext):
    user_data[update.message.chat_id]['amount'] = update.message.text
    await update.message.reply_text("لطفاً توضیحات را وارد کنید (اختیاری).")
    return DETAILS

# مرحله دریافت توضیحات
async def get_details(update: Update, context: CallbackContext):
    user_data[update.message.chat_id]['details'] = update.message.text if update.message.text else "هیچ توضیحی وارد نشده است."
    
    # ارسال پیامی با اطلاعات
    data = user_data[update.message.chat_id]
    message = f"""
    نمبر حواله: {data['hvala_number']}
    حواله به: {data['hvala']}
    فرستنده: {data['sender']}
    گیرنده: {data['receiver']}
    مبلغ: {data['amount']}
    توضیحات: {data['details']}
    """
    
    await update.message.reply_text(f"اطلاعات شما: آدرس‌ها:\n هرات، درب خوش، مارکت تجارتی معراج فیضی دوکان نمبر 52ـ52 \n غور، مارکت موتورسیکلت فروشان، دوکان سید احمد مرادی\n  به شرح زیر است:\n{message}")
    
    # بازگشت به حالت اولیه
    return ConversationHandler.END

# مرحله‌ پایان
async def cancel(update: Update, context: CallbackContext):
    await update.message.reply_text("فرآیند دریافت اطلاعات متوقف شد.")
    return ConversationHandler.END

# تنظیم ربات
def main():
    application = Application.builder().token("7707909069:AAGnOgnet-kPi9ZKsGaRr3hZeAsZUZbEqLc").build()

    conversation_handler = ConversationHandler(
        entry_points=[CommandHandler("start", start)],
        states={
            HVALA_NUMBER: [MessageHandler(filters.TEXT & ~filters.COMMAND, get_hvala_number)],
            HVALA: [MessageHandler(filters.TEXT & ~filters.COMMAND, get_hvala)],
            SENDERS: [MessageHandler(filters.TEXT & ~filters.COMMAND, get_senders)],
            RECEIVERS: [MessageHandler(filters.TEXT & ~filters.COMMAND, get_receivers)],
            AMOUNT: [MessageHandler(filters.TEXT & ~filters.COMMAND, get_amount)],
            DETAILS: [MessageHandler(filters.TEXT & ~filters.COMMAND, get_details)],
        },
        fallbacks=[CommandHandler("cancel", cancel)],
    )

    application.add_handler(conversation_handler)

    application.run_polling()

if __name__ == '__main__':
    main()