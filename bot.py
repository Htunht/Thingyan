import os
import sys
import asyncio
import logging
from datetime import datetime
from dotenv import load_dotenv
from telegram import Update
from telegram.ext import ApplicationBuilder, CommandHandler, ContextTypes, MessageHandler, filters

# Logging setup
logging.basicConfig(
    format='%(asctime)s - %(name)s - %(levelname)s - %(message)s',
    level=logging.INFO
)

# သင်္ကြန် Countdown Logic
async def thingyan_countdown(update: Update, context: ContextTypes.DEFAULT_TYPE) -> None:
    try:
        # ၂၀၂၇ သင်္ကြန်ကျမည့်ရက် (April 13, 2027)
        thingyan_date = datetime(2027, 4, 13, 0, 0, 0)
        now = datetime.now()

        if now >= thingyan_date:
            # သင်္ကြန်အချိန်ရောက်သွားလျှင်
            response = "💦 ရေလောင်းမယ်နော်... သင်္ကြန်ရောက်ပြီဟေ့! 💦"
        else:
            # အချိန်တွက်ချက်ခြင်း
            diff = thingyan_date - now
            days = diff.days
            hours, remainder = divmod(diff.seconds, 3600)
            minutes, seconds = divmod(remainder, 60)
            
            response = (
                f"🍻 ၂၀၂၇ သင်္ကြန်ကျရန်\n"
                f"📅 **{days}** ရက်၊ **{hours}** နာရီ၊ **{minutes}** မိနစ်၊ **{seconds}** စက္ကန့် သာ လိုပါတော့သည်!"
            )

        await update.message.reply_text(response, parse_mode='Markdown')

    except Exception as e:
        logging.error(f"Error in countdown: {e}")
        await update.message.reply_text("ခေတ္တခဏ အမှားအယွင်းဖြစ်နေပါတယ်ဗျာ။")

# User က "ကဲမယ်" လို့ စာရိုက်ရင်လည်း အလုပ်လုပ်အောင် (Optional)
async def check_text(update: Update, context: ContextTypes.DEFAULT_TYPE) -> None:
    if update.message.text == "ကဲမယ်":
        await thingyan_countdown(update, context)

if __name__ == '__main__':
    if sys.platform == 'win32':
        asyncio.set_event_loop_policy(asyncio.WindowsSelectorEventLoopPolicy())
        
    # .env ဖိုင်ထဲမှ Data များကို ခေါ်ယူခြင်း
    load_dotenv()
    token = os.getenv("TELEGRAM_TOKEN")
    
    if not token:
        logging.error("TELEGRAM_TOKEN is not set in the .env file.")
        sys.exit(1)

    app = ApplicationBuilder().token(token).build()

    # --- Command ပြင်ဆင်ထားသည့်နေရာ ---
    # /start ရိုက်ရင် ပြမယ်
    app.add_handler(CommandHandler("start", thingyan_countdown))
    
    # /dance လို့ ရိုက်ရင် (သို့မဟုတ် Menu က နှိပ်ရင်) ပြမယ်
    app.add_handler(CommandHandler("dance", thingyan_countdown)) 
    
    # "ကဲမယ်" လို့ စာရိုက်ရင် ပြမယ်
    app.add_handler(MessageHandler(filters.TEXT & ~filters.COMMAND, check_text))

    print("Bot is polling... /dance Command အဆင်သင့်ဖြစ်ပါပြီ။")
    app.run_polling()