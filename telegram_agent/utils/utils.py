from telegram import Update
from telegram.ext import CallbackContext
from telegram_agent.mongo_handler import MongoHandler
from telegram_agent.constants import SYSTEM_PROMPT

students_handler = MongoHandler("students")

def check_user_setup(update: Update, context: CallbackContext) -> bool:
    message = update.message
    user_id = message.from_user.id

    is_user = students_handler.find({"user_id": user_id})
    if not is_user:
        return False
    return True

def personalize_system_prompt(user_id) -> str:
    user = students_handler.find({"user_id": user_id})
    PERSONALIZED_SYSTEM_PROMPT = (SYSTEM_PROMPT +
                                  f"User's name is {user['name']} \n\n" +
                                  f"User studies at {user['university']} \n\n" +
                                  f"User's timetable is {user['timetable']} \n\n")
    return PERSONALIZED_SYSTEM_PROMPT

async def reset_history(update: Update, context: CallbackContext):
    context.user_data["history"] = []
    await update.message.reply_text("🗑️ Chat history cleared.")
