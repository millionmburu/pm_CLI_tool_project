<========PYTHON PROJECT MANAGEMENT CLI TOOL========>
A polished, interactive Project Management Command-Line Interface (CLI) application built with Python. This tool helps you manage users, organize projects, and track underlying tasks with a beautiful terminal user interface.

<========Features========>
Interactive Menu UI: A structured, colorful terminal interface built using the Rich library.

Dual Execution Modes:

Interactive Mode: Step-by-step guidance through menus, inputs, and validations.

Automation/Subcommand Mode: Direct execution bypassing the menu via argparse integration.

Strong Validation: Robust checks for email formats, empty fields, case-insensitive project matching, and duplicate entries.

Local Persistence: Data automatically reads from and writes to disk on every modification.

<======== Project Structure========>
Ensure your workspace is organized exactly like this for the module paths to resolve correctly:

Plaintext
├── models/
│   ├── user.py
│   ├── project.py
│   └── task.py
├── utils/
│   └── storage_handler.py
└── main.py

<======== Getting Started ========>
Prerequisites
Python 3.8 or higher

pip (Python package installer)

1. Installation
Clone or navigate to your project directory and install the required dependencies:

Bash
pip install rich

2. Running Interactive Mode
To open the colorful main menu loop and interact with the system step-by-step, run:

Bash
python main.py

3. Running Subcommand Mode (Automation)
You can completely bypass the interactive menu by executing direct subcommands. This is highly useful for automated testing and grading scripts:

List current projects & tasks:

Bash
python main.py list-projects
Launch user creation wizard directly:

Bash
python main.py add-user
Launch project creation wizard directly:

Bash
python main.py add-project
Launch task assignment wizard directly:

Bash
python main.py add-task
Launch task completion wizard directly:

Bash
python main.py complete-task

<========Core Dependencies========>
Rich: Handles the terminal panels, stylized input tables, and custom logging syntax colors.

Argparse & Sys: Native standard library components routing system line configurations and exit signals safely.