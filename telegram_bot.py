from telegram import Update, ReplyKeyboardMarkup
from telegram.ext import Application, CommandHandler, ContextTypes, MessageHandler, filters
import requests

# ========== API Configuration ==========
API_BASE_URL = "http://127.0.0.1:8000/api/tasks/"

# ========== Helper Functions ==========
def send_api_request(method, url, json_data=None):
    """Helper function to send API requests."""
    try:
        response = requests.request(method, url, json=json_data)
        response.raise_for_status()
        return response
    except requests.exceptions.RequestException as e:
        print(f"API Error: {e}")
        return None

# ========== Command Handlers ==========
async def start(update: Update, context: ContextTypes.DEFAULT_TYPE):
    """Display the Task Manager Dashboard."""
    keyboard = [
        ["➕ Add Task", "📝 My Tasks"],
        ["✏️ Edit Task", "❌ Delete Task"],
        ["🔄 Update Status", "ℹ️ Help"]
    ]
    
    await update.message.reply_text(
        "📊 Task Manager Dashboard\n\n"
        "Choose an action:",
        reply_markup=ReplyKeyboardMarkup(
            keyboard, 
            resize_keyboard=True,
            input_field_placeholder="Select an action..."
        )
    )

async def help_command(update: Update, context: ContextTypes.DEFAULT_TYPE):
    """Display help information."""
    help_text = (
        "🤖 Task Manager Bot Help\n\n"
        "Button Guide:\n"
        "➕ Add Task - Create new task\n"
        "📝 My Tasks - List all tasks\n"
        "✏️ Edit Task - Modify task description\n"
        "❌ Delete Task - Remove a task\n"
        "🔄 Update Status - Change task progress\n"
        "ℹ️ Help - Show this message\n\n"
        "Manual Commands Still Work:\n"
        "/addtask, /edittask, /viewtasks, etc."
    )
    await update.message.reply_text(help_text)

async def add_task(update: Update, context: ContextTypes.DEFAULT_TYPE):
    """Prompt the user to enter a task description."""
    context.user_data['awaiting_task_description'] = True
    await update.message.reply_text("Type your task description:")

async def view_tasks(update: Update, context: ContextTypes.DEFAULT_TYPE):
    """Fetch and display the user's tasks."""
    user_id = update.message.from_user.id
    response = send_api_request("GET", f"{API_BASE_URL}?user_id={user_id}")
    
    if response and response.status_code == 200:
        tasks = response.json()
        if tasks:
            task_list = "\n".join([f"📝 {task['id']}: {task['description']} (Status: {task['status']})" 
                                 for task in tasks])
            await update.message.reply_text(f"📋 Your tasks:\n{task_list}")
        else:
            await update.message.reply_text("📭 You have no tasks.")
    else:
        await update.message.reply_text("❌ Failed to fetch tasks. Please try again.")

async def process_add_task(update: Update, context: ContextTypes.DEFAULT_TYPE):
    """Add a new task based on user input."""
    task_description = update.message.text
    user_id = update.message.from_user.id
    
    response = send_api_request("POST", API_BASE_URL, json_data={"user_id": user_id, "description": task_description, "status": "TODO"})
    
    if response and response.status_code == 201:
        await update.message.reply_text("✅ Task added successfully!")
    else:
        await update.message.reply_text("❌ Failed to add task. Please try again.")
    context.user_data.pop('awaiting_task_description', None)

async def process_edit_task(update: Update, context: ContextTypes.DEFAULT_TYPE):
    """Edit an existing task."""
    try:
        task_data = update.message.text.split(maxsplit=1)
        if len(task_data) != 2:
            await update.message.reply_text("⚠️ Invalid format. Use: `<Task ID> <New Description>`\nExample: `1 Buy groceries`")
            return

        task_id, new_description = task_data
        user_id = update.message.from_user.id

        response = send_api_request("PATCH", f"{API_BASE_URL}{task_id}/", json_data={"description": new_description, "user_id": user_id})

        if response and response.status_code == 200:
            await update.message.reply_text("✅ Task updated successfully!")
        else:
            await update.message.reply_text("❌ Failed to update task. Please try again.")

    except Exception as e:
        await update.message.reply_text(f"⚠️ Error processing task update: {e}")
    finally:
        context.user_data.pop('awaiting_edit', None)

async def process_delete_task(update: Update, context: ContextTypes.DEFAULT_TYPE):
    """Delete a task."""
    try:
        task_id = update.message.text.strip()
        user_id = update.message.from_user.id

        response = send_api_request("DELETE", f"{API_BASE_URL}{task_id}/", json_data={"user_id": user_id})

        if response and response.status_code == 204:
            await update.message.reply_text("🗑️ Task deleted successfully!")
        else:
            await update.message.reply_text("❌ Failed to delete task. Ensure the ID is correct.")

    except Exception as e:
        await update.message.reply_text(f"⚠️ Error processing task deletion: {e}")
    finally:
        context.user_data.pop('awaiting_delete', None)

async def process_delete_task(update: Update, context: ContextTypes.DEFAULT_TYPE):
    """Delete a task."""
    try:
        task_id = update.message.text.strip()
        user_id = update.message.from_user.id

        response = send_api_request("DELETE", f"{API_BASE_URL}{task_id}/", json_data={"user_id": user_id})

        if response and response.status_code == 204:
            await update.message.reply_text("🗑️ Task deleted successfully!")
        else:
            await update.message.reply_text("❌ Failed to delete task. Ensure the ID is correct.")

    except Exception as e:
        await update.message.reply_text(f"⚠️ Error processing task deletion: {e}")
    finally:
        context.user_data.pop('awaiting_delete', None)

async def process_set_status(update: Update, context: ContextTypes.DEFAULT_TYPE):
    """Update the status of a task."""
    try:
        task_data = update.message.text.split(maxsplit=1)
        if len(task_data) != 2:
            await update.message.reply_text("⚠️ Invalid format. Use: `<Task ID> <Status>`\nExample: `1 IN_PROGRESS`")
            return

        task_id, status = task_data
        user_id = update.message.from_user.id

        response = send_api_request("PATCH", f"{API_BASE_URL}{task_id}/", json_data={"status": status, "user_id": user_id})

        if response and response.status_code == 200:
            await update.message.reply_text("✅ Task status updated successfully!")
        else:
            await update.message.reply_text("❌ Failed to update task status. Please try again.")

    except Exception as e:
        await update.message.reply_text(f"⚠️ Error processing status update: {e}")
    finally:
        context.user_data.pop('awaiting_status', None)

# ========== Message Handler for Button Clicks ==========
async def handle_message(update: Update, context: ContextTypes.DEFAULT_TYPE):
    """Handle button clicks and free-form text input."""
    text = update.message.text
    user_id = update.message.from_user.id
    
    # Map button texts to commands
    button_actions = {
        "➕ Add Task": "addtask",
        "📝 My Tasks": "viewtasks",
        "✏️ Edit Task": "edittask",
        "❌ Delete Task": "deletetask",
        "🔄 Update Status": "setstatus",
        "ℹ️ Help": "help"
    }
    
    if text in button_actions:
        command = button_actions[text]
        # Handle different button actions
        if command == "addtask":
            await add_task(update, context)
        elif command == "viewtasks":
            await view_tasks(update, context)
        elif command == "edittask":
            context.user_data['awaiting_edit'] = True
            await update.message.reply_text("Send task ID and new description:\nExample: 1 Buy milk")
        elif command == "deletetask":
            context.user_data['awaiting_delete'] = True
            await update.message.reply_text("Send task ID to delete:\nExample: 1")
        elif command == "setstatus":
            context.user_data['awaiting_status'] = True
            await update.message.reply_text("Send task ID and status (TODO/IN_PROGRESS/DONE):\nExample: 1 IN_PROGRESS")
        elif command == "help":
            await help_command(update, context)
    else:
        # Handle free-form text input
        if context.user_data.get('awaiting_task_description'):
            await process_add_task(update, context)
        elif context.user_data.get('awaiting_edit'):
            await process_edit_task(update, context)
        elif context.user_data.get('awaiting_delete'):
            await process_delete_task(update, context)
        elif context.user_data.get('awaiting_status'):
            await process_set_status(update, context)
        else:
            await update.message.reply_text("I didn't understand that. Please use the buttons or type /help.")

# ========== Main Function ==========
def main():
    """Start the bot."""
    application = Application.builder().token("Your_Token").build()
    
    # Command handlers
    application.add_handler(CommandHandler("start", start))
    application.add_handler(CommandHandler("help", help_command))
    
    # Button click handler
    application.add_handler(MessageHandler(filters.TEXT & ~filters.COMMAND, handle_message))
    
    # Existing command handlers
    application.add_handler(CommandHandler("addtask", add_task))
    application.add_handler(CommandHandler("viewtasks", view_tasks))
    application.add_handler(CommandHandler("edittask", process_edit_task))
    application.add_handler(CommandHandler("deletetask", process_delete_task))
    application.add_handler(CommandHandler("setstatus", process_set_status))

    application.run_polling()

if __name__ == "__main__":
    main()