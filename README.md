# Task Manager Telegram Bot

## Overview

A Telegram bot to help users manage their tasks efficiently. Users can add, view, edit, delete, and update the status of their tasks through simple commands and buttons.

## Features

- Add new tasks
- View all tasks
- Edit task descriptions
- Delete tasks
- Update task status
- User-friendly interface with buttons
- Command support for manual inputs

## Setup

### Prerequisites

- Python 3.x
- Django
- Django REST framework
- Telegram bot API token

### Installation

1. **Clone the repository:**

```bash
git clone https://github.com/sina4404/telegram_task_manager_with_django.git
cd task_manager_telegram_bot
```

2. **Create a virtual environment and activate it:**

```bash
python -m venv venv
source venv/bin/activate  # On Windows use `venv\Scripts\activate`
```

3. **Install the required packages:**

```bash
pip install -r requirements.txt
```

4. **Set up your Django project:**

```bash
python manage.py migrate
python manage.py runserver
```

5. **Configure your Telegram bot:**

Replace the placeholder token with your actual Telegram bot API token in the script (`telegram_bot.py`).

6. **Run the Telegram bot:**

```bash
python telegram_bot.py
```

## Usage

### Bot Commands

- `/start`: Display the Task Manager Dashboard.
- `/help`: Show help information.
- `/addtask`: Prompt to add a new task.
- `/viewtasks`: List all tasks.
- `/edittask <task_id> <new_description>`: Edit a task's description.
- `/deletetask <task_id>`: Delete a task.
- `/setstatus <task_id> <status>`: Update a task's status.

### Button Guide

- **➕ Add Task**: Create new task
- **📝 My Tasks**: List all tasks
- **✏️ Edit Task**: Modify task description
- **❌ Delete Task**: Remove a task
- **🔄 Update Status**: Change task progress
- **ℹ️ Help**: Show help message

## Contributing

Contributions are welcome! Feel free to open issues or submit pull requests.

Feel free to expand on each section or add any other relevant information. Let me know if you need further assistance! 😊
