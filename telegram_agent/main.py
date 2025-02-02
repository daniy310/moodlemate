import datetime
from os import utime

import openai
import os
import json
import telegram
from dotenv import load_dotenv
from telegram import Update, Message
from telegram.ext import Application, CommandHandler, MessageHandler, filters, CallbackContext, ConversationHandler
from solss_scraper import scrape_timetable
from mongo_handler import MongoHandler
from telegram_agent.utils.utils import check_user_setup, personalize_system_prompt, reset_history
from utils.utils import check_user_setup


load_dotenv()

# Initialize MongoHandler
students_handler = MongoHandler("students")

OPENAI_KEY = os.getenv("OPENAI_KEY")
BOT_TOKEN = os.getenv('BOT_TOKEN')
ENV = os.getenv("ENV")

TIMETABLE_FILE = "timetable.json"
timetable_data = []

NAME, UNIVERSITY, MOODLE_USERNAME, MOODLE_PASSWORD = range(4)


async def start(update: Update, context: CallbackContext):
    # Check if user is already set up
    if check_user_setup(update, context):
        await update.message.reply_text("Welcome back! How can I assist you today?")
        return

    # Start conversation
    await update.message.reply_text("Hello! To get started, I need to know a few details about you.")
    await update.message.reply_text("What is your full name?")
    return NAME


# Handle the name input and prompt for university
async def ask_university(update: Update, context: CallbackContext):
    user_name = update.message.text
    context.user_data["name"] = user_name

    await update.message.reply_text(f"Got it, {user_name}! Now, what is the name of your university?")
    return UNIVERSITY


# Handle the university input and prompt for Moodle username
async def ask_moodle_username(update: Update, context: CallbackContext):
    university = update.message.text
    context.user_data["university"] = university

    await update.message.reply_text(f"Great! Please provide your Moodle username.")
    return MOODLE_USERNAME


# Handle the Moodle username input and prompt for Moodle password
async def ask_moodle_password(update: Update, context: CallbackContext):
    moodle_username = update.message.text
    context.user_data["moodle_username"] = moodle_username

    await update.message.reply_text(f"Thanks! Now, please provide your Moodle password.")
    return MOODLE_PASSWORD


# Handle the Moodle password input and scrape the timetable
async def scrape_and_save_timetable(update: Update, context: CallbackContext):
    if ENV == 'dev':
        await update.message.reply_text(
            f"App is in dev mode so everyone can test it out without the SOLSS account. Instead, you will see some mock data ! \n This can easily be changed back to prod version from our ENV vars :)")
        return ConversationHandler.END

    moodle_password = update.message.text

    await update.message.reply_text(f"Thank you! Allow me one minute to connect to SOLSS and gather the relevant data..")

    # Now scrape the timetable using solss-scraper
    user_data = context.user_data
    timetable = await scrape_timetable(user_data["moodle_username"], moodle_password, update, context)

    # Save the user data in the database
    user_id = update.message.from_user.id
    student_data = {
        "name": user_data["name"],
        "university": user_data["university"],
        "moodle_username": user_data["moodle_username"],
        "timetable": timetable,
        "courses_list": timetable["courses_list"]
    }

    students_handler.save(student_data, unique_key={"user_id": user_id})

    await update.message.reply_text(f"Your profile has been set up! Your timetable has been saved. Please don't forget to delete your password from our conversation :p")
    return ConversationHandler.END

async def help_command(update: Update, context: CallbackContext):
    await update.message.reply_text("I can help you with your timetable, assignments, and lecture notes. \n Please configure your details by clicking here -> /start :)")

async def timetable(update: Update, context: CallbackContext):
    if ENV != 'dev':
        if not check_user_setup(update, context):
            await update.message.reply_text("You first have to setup your details. \n Please do that by clicking here -> /start :)")
            return

    if ENV == 'dev':
        user_id = 1365379642
    else:
        user_id = update.message.from_user.id
    timetable_data = students_handler.find({"user_id": user_id})['timetable']

    if not timetable_data:
        await update.message.reply_text("❌ No timetable data available.")
        return

    response = "📅 Your Timetable :\n\n"

    for day in timetable_data:
        if len(timetable_data[day]):
            response += f"📅 {day}\n\n"
            for course in timetable_data[day]:
                response += f"<b>{course['course_id']}</b>\n\n"
                response += f"   🏫 Class Type: {course['course_type']}\n\n"
                response += f"   ⏰ Timing: {course['course_start_time']} - {course['course_end_time']}\n\n"
                response += f"   📍 Location: {course['course_location']}\n\n"
                response += "\n"

    await update.message.reply_text(response, parse_mode=telegram.constants.ParseMode.HTML)


# 🔹 Watcher for logging all messages received
async def messages_watcher(update: Update, context: CallbackContext):
    if ENV != 'dev':
        if not check_user_setup(update, context):
            await update.message.reply_text("You first have to setup your details. \n Please do that by clicking here -> /start :)")
            return

    message: Message = update.message

    if ENV == 'dev':
        user_id = 1365379642
    else:
        user_id = update.message.from_user.id

    PERSONALIZED_SYSTEM_PROMPT = personalize_system_prompt(user_id)

    # Initialize or retrieve conversation history
    if "history" not in context.user_data:
        context.user_data["history"] = []

    # Get current date and time
    now = datetime.datetime.now()
    formatted_date = now.strftime("%Y-%m-%d")  # Format: YYYY-MM-DD
    formatted_time = now.strftime("%H:%M:%S")  # Format: HH:MM:SS
    day_of_week = now.strftime("%A")  # Full weekday name (e.g., "Monday")

    user_prompt = f"{day_of_week} : {formatted_date}, {formatted_time} \n {message.text}"

    # Append user message to history
    context.user_data["history"].append({"role": "user", "content": user_prompt})

    # Construct system message
    system_message = {"role": "system", "content": PERSONALIZED_SYSTEM_PROMPT}

    # Prepare message history (Include system prompt + conversation history)
    messages = [system_message] + context.user_data["history"]

    try:
        client = openai.OpenAI(api_key=OPENAI_KEY)  # ✅ Ensure API key is used
        response = client.chat.completions.create(
            model="gpt-3.5-turbo",
            messages=messages,
            temperature=0.7
        )

        ai_reply = response.choices[0].message.content

        # Append AI response to history
        context.user_data["history"].append({"role": "assistant", "content": ai_reply})

        # Trim history if it gets too long (Keep only last 20 messages)
        if len(context.user_data["history"]) > 20:
            context.user_data["history"] = context.user_data["history"][-20:]

        # Send response to user
        await update.message.reply_text(ai_reply, parse_mode="HTML")

    except Exception as e:
        print(f"❌ OpenAI API Error: {e}")
        await update.message.reply_text("⚠️ Error generating AI response. Try again later.")


# Conversation handler to guide the user through the setup process
setup_conversation_handler = ConversationHandler(
    entry_points=[CommandHandler('start', start)],
    states={
        NAME: [MessageHandler(filters.TEXT & ~filters.COMMAND, ask_university)],
        UNIVERSITY: [MessageHandler(filters.TEXT & ~filters.COMMAND, ask_moodle_username)],
        MOODLE_USERNAME: [MessageHandler(filters.TEXT & ~filters.COMMAND, ask_moodle_password)],
        MOODLE_PASSWORD: [MessageHandler(filters.TEXT & ~filters.COMMAND, scrape_and_save_timetable)],
    },
    fallbacks=[],
)


def main():
    app = Application.builder().token(BOT_TOKEN).build()

    app.add_handler(setup_conversation_handler)

    # 🔹 Command Handlers
    app.add_handler(CommandHandler("start", start))
    app.add_handler(CommandHandler("help", help_command))
    app.add_handler(CommandHandler("timetable", timetable))
    app.add_handler(CommandHandler("reset", reset_history))

    # 🔹 Message Watcher: Logs every message received
    app.add_handler(MessageHandler(filters.TEXT & ~filters.COMMAND, messages_watcher))

    print("🤖 Bot is running...")
    app.run_polling()


if __name__ == "__main__":
    main()
