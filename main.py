import smtplib
from email.message import EmailMessage
from telegram import Update
from telegram.ext import Application, CommandHandler, MessageHandler, filters, ContextTypes

# Replace the placeholder values below with your own credentials and server details.
BOT_TOKEN = "YOUR_TELEGRAM_BOT_TOKEN"  # e.g. "123456789:ABCDEF..."
SMTP_SERVER = "YOUR_SMTP_SERVER"         # e.g. "smtp.example.com"
SMTP_PORT = 465                          # Use your SMTP port (465 for SSL by default)
EMAIL_ADDRESS = "YOUR_EMAIL_ADDRESS"       # e.g. "you@example.com"
EMAIL_PASSWORD = "YOUR_EMAIL_PASSWORD"     # e.g. "your_email_password_here"

async def start(update: Update, context: ContextTypes.DEFAULT_TYPE):
    await update.message.reply_text("Hello! Send me an email address to verify it with a test email.")

async def send_test_email(to_email: str) -> bool:
    msg = EmailMessage()
    msg['Subject'] = 'Email Verification - Valid Or Not'
    msg['From'] = EMAIL_ADDRESS
    msg['To'] = to_email
    msg.set_content(
        "Congratulations!🎉\n\n"
        "If you are reading this your email address is working.\n"
        "-------------------\n"
        "This is not spam or a solicitation. This email was sent to your email address because you, or someone else, requested a test email to be sent to this address."
    )

    try:
        with smtplib.SMTP_SSL(SMTP_SERVER, SMTP_PORT) as server:
            server.login(EMAIL_ADDRESS, EMAIL_PASSWORD)
            server.send_message(msg)
        return True
    except Exception as e:
        # Optionally log the exception e for debugging purposes
        return False

async def handle_email(update: Update, context: ContextTypes.DEFAULT_TYPE):
    user_email = update.message.text.strip()
    if "@" in user_email and "." in user_email:
        await update.message.reply_text(f"Verifying email: {user_email}")
        if await send_test_email(user_email):
            await update.message.reply_text("✅ Test email sent successfully! Please check your inbox.")
        else:
            await update.message.reply_text("❌ Failed to send email. Please try again.")
    else:
        await update.message.reply_text("⚠️ Please enter a valid email address.")

def main():
    app = Application.builder().token(BOT_TOKEN).build()
    app.add_handler(CommandHandler("start", start))
    app.add_handler(MessageHandler(filters.TEXT & ~filters.COMMAND, handle_email))
    app.run_polling()

if __name__ == '__main__':
    main()
