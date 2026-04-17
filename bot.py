import os
import sys
import asyncio
import logging
from datetime import datetime, timedelta, timezone # timedelta နဲ့ timezone ထပ်ထည့်ထားတယ်
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

        # --- မြန်မာစံတော်ချိန် (GMT+6:30) သတ်မှတ်ခြင်း ---
        mm_tz = timezone(timedelta(hours=6, minutes=30))
        # လက်ရှိအချိန်ကို မြန်မာစံတော်ချိန်နဲ့ ယူမယ်၊ ပြီးရင် နှိုင်းယှဉ်ရလွယ်အောင် timezone info ကို ပြန်ဖြုတ်မယ်
        now = datetime.now(mm_tz).replace(tzinfo=None)

        if now >= thingyan_date:
            response = "💦 ရေလောင်းမယ်နော်... သင်္ကြန်ရောက်ပြီဟေ့! 💦"
        else:
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

# User က "ကဲမယ်" လို့ စာရိုက်ရင်လည်း အလုပ်လုပ်အောင်
async def check_text(update: Update, context: ContextTypes.DEFAULT_TYPE) -> None:
    if update.message.text == "ကဲမယ်":
        await thingyan_countdown(update, context)

if __name__ == '__main__':
    if sys.platform == 'win32':
        asyncio.set_event_loop_policy(asyncio.WindowsSelectorEventLoopPolicy())
        
    load_dotenv()
    # Token ထဲမှာ \n တွေပါလာရင် ဖြတ်ပစ်ဖို့ .strip() သုံးထားပါတယ်
    token = os.getenv("TELEGRAM_TOKEN").strip() if os.getenv("TELEGRAM_TOKEN") else None
    
    if not token:
        logging.error("TELEGRAM_TOKEN is not set correctly.")
        sys.exit(1)

    app = ApplicationBuilder().token(token).build()

    app.add_handler(CommandHandler("start", thingyan_countdown))
    app.add_handler(CommandHandler("dance", thingyan_countdown)) 
    app.add_handler(MessageHandler(filters.TEXT & ~filters.COMMAND, check_text))

    print("Bot is polling with Myanmar Timezone fix...")
    app.run_polling()