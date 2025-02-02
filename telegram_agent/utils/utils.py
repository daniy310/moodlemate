from telegram import Update
from telegram.ext import CallbackContext
from telegram_agent.mongo_handler import MongoHandler
from telegram_agent.constants import SYSTEM_PROMPT

students_handler = MongoHandler("students")
lectures_handler = MongoHandler("lectures")

def check_user_setup(update: Update, context: CallbackContext) -> bool:
    message = update.message
    user_id = message.from_user.id

    is_user = students_handler.find({"user_id": user_id})
    if not is_user:
        return False
    return True


def personalize_system_prompt(user_id) -> str:
    # Fetch user data from the students collection
    user = students_handler.find({"user_id": user_id})

    # Fetch the list of courses the user is enrolled in
    courses_list = user.get("courses_list", [])  # Default to empty list if courses_list is not found

    # Build the base system prompt with user details
    PERSONALIZED_SYSTEM_PROMPT = (SYSTEM_PROMPT +
                                  f"User's name is {user['name']} \n\n" +
                                  f"User studies at {user['university']} \n\n" +
                                  f"User's timetable is {user['timetable']} \n\n")

    # If the user has enrolled courses, fetch corresponding lectures
    if courses_list:
        # Query the lectures collection to get all lectures for the courses in the courses_list
        lectures = lectures_handler.find_many({"course_id": {"$in": courses_list}})
        print(lectures)

        # Add the list of lectures to the prompt
        lectures_info = "User is enrolled in the following courses and lectures:\n"

        for lecture in lectures:
            lectures_info += (
                f"- {lecture['course_id']}: {lecture['lecture_title']} (Lecture ID: {lecture['lecture_id']})\n {lecture['lecture_text']}")

        # Add the lecture info to the personalized system prompt
        PERSONALIZED_SYSTEM_PROMPT += lectures_info
    else:
        PERSONALIZED_SYSTEM_PROMPT += "User is not enrolled in any courses.\n"

    return PERSONALIZED_SYSTEM_PROMPT


async def reset_history(update: Update, context: CallbackContext):
    context.user_data["history"] = []
    await update.message.reply_text("🗑️ Chat history cleared.")
