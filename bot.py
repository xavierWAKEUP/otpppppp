from telegram import Update
from telegram.ext import Updater, CommandHandler, CallbackContext
import random
import logging
import time

# Enable logging
logging.basicConfig(format='%(asctime)s - %(name)s - %(levelname)s - %(message)s', level=logging.INFO)
logger = logging.getLogger(__name__)

# Global dictionary to store OTPs and their timestamps
otp_storage = {}

# Define your token from BotFather
TOKEN = '7365961128:AAHdDe9w3E5Xjwtg6eFhq39_SA-SkLDyGNE'

# Your Telegram user ID (replace with your actual user ID)
ALLOWED_USER_ID = 6847825791

# OTP validity period in seconds (e.g., 5 minutes)
OTP_VALIDITY_PERIOD = 300

# Function to generate OTP
def generate_otp():
    return random.randint(100000, 999999)

# Check if the user is allowed
def check_user(update: Update) -> bool:
    return update.message.from_user.id == ALLOWED_USER_ID

# Command handler to start the bot
def start(update: Update, context: CallbackContext) -> None:
    if not check_user(update):
        update.message.reply_text('Access denied.')
        return
    update.message.reply_text('Welcome! Use /getotp to receive an OTP.')

# Command handler to get OTP
def getotp(update: Update, context: CallbackContext) -> None:
    if not check_user(update):
        update.message.reply_text('Access denied.')
        return
    user_id = update.message.from_user.id
    otp = generate_otp()
    otp_storage[user_id] = (otp, time.time())  # Store OTP and current timestamp
    update.message.reply_text(f'Your OTP is {otp}. It will expire in 5 minutes.')

# Command handler to verify OTP
def verifyotp(update: Update, context: CallbackContext) -> None:
    if not check_user(update):
        update.message.reply_text('Access denied.')
        return
    user_id = update.message.from_user.id
    otp = int(context.args[0]) if context.args else None

    if user_id in otp_storage:
        stored_otp, timestamp = otp_storage[user_id]
        current_time = time.time()

        if current_time - timestamp > OTP_VALIDITY_PERIOD:
            update.message.reply_text('OTP has expired. Please request a new one.')
            del otp_storage[user_id]  # Remove expired OTP
        elif stored_otp == otp:
            update.message.reply_text('OTP verified successfully!')
            del otp_storage[user_id]  # Remove OTP after successful verification
        else:
            update.message.reply_text('Invalid OTP.')
    else:
        update.message.reply_text('No OTP found. Please request a new one.')

def main() -> None:
    # Create the Updater and pass it your bot's token
    updater = Updater(TOKEN)

    # Get the dispatcher to register handlers
    dp = updater.dispatcher

    # Register handlers
    dp.add_handler(CommandHandler('start', start))
    dp.add_handler(CommandHandler('getotp', getotp))
    dp.add_handler(CommandHandler('verifyotp', verifyotp))

    # Start the Bot
    updater.start_polling()

    # Run the bot until you send a signal to stop
    updater.idle()

if __name__ == '__main__':
    main()
