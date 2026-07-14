# AI Engineer Notes

---

# Project

## AI Outreach Agent

### Goal

Build a production-ready AI Outreach Agent using:

* Python
* OOP
* n8n
* Gemini AI
* Gmail
* APIs
* File Handling
* Error Handling

---

# Day 1

## What is a Class?

A class is a blueprint that defines the structure and behavior of an object.

### Project Example

Class:

OutreachAgent

This class represents the complete AI Outreach Agent.

---

## What is an Object?

An object is a real instance of a class.

Example:

agent = OutreachAgent(...)

Here, `agent` is the actual AI Outreach Agent.

---

## What is a Constructor?

Constructor:

**init**()

It runs automatically whenever an object is created.

Purpose:

* Initialize object
* Store initial data

Example:

sender_name

company

api_key

---

## What are Attributes?

Attributes are variables stored inside an object.

Our Project Attributes

* sender_name
* company
* api_key

These represent the identity of our AI Agent.

---

## Why do we use self?

self refers to the current object.

Example:

self.company = company

Right side:

company

↓

Input provided by user.

Left side:

self.company

↓

Saved inside the object.

---

# Real Life Analogy

Imagine hiring an employee.

Employee Name

↓

Ali

Company

↓

ABC Solutions

API Key

↓

Secret Office Key

Every employee has different information.

Similarly, every AI Agent has different attributes.

---

# n8n Mapping

Manual Trigger

↓

Create AI Agent

Set Node

↓

Object Attributes

---

# Day 2

## What is a Method?

A method is a function inside a class.

Methods define what an object can do.

---

### Our Methods

generate_email()

Future Methods

choose_prompt()

score_lead()

send_email()

validate_lead()

---

## Why Method Inside Class?

Because generating an email requires access to:

company

sender_name

api_key

All this information already exists inside the object.

Therefore, the method belongs to the class.

---

# Current Project Architecture

OutreachAgent

Attributes

* sender_name
* company
* api_key

Methods

* generate_email()

Future

* choose_prompt()
* score_lead()
* send_email()

---

# n8n Mapping

Gemini Node

↓

generate_email()

Python decides what action to perform.

Gemini performs the action.

---

# Project Structure

AI_Outreach_Agent/

app.py

↓

Entry Point

agent.py

↓

Brain

prompts.py

↓

All AI Prompts

config.py

↓

Configuration

data/

↓

Lead Storage

logs/

↓

Application Logs

README.md

↓

Project Documentation

CHANGELOG.md

↓

Project History

NOTES.md

↓

Interview Revision Notes

---

# Debugging Notes

## AttributeError

Meaning

Python could not find the requested method or attribute.

Common Reasons

* Wrong method name
* Wrong indentation
* Method outside class
* Calling a method that does not exist

How to Fix

1. Read the error.
2. Check file name.
3. Check line number.
4. Verify method exists.
5. Save file.
6. Run again.

---

# Interview Questions

Q1. What is a Class?

Answer:

A class is a blueprint used to create objects.

---

Q2. What is an Object?

Answer:

An object is an instance of a class.

---

Q3. Why use **init**()?

Answer:

To initialize object attributes automatically when the object is created.

---

Q4. What are Attributes?

Answer:

Attributes store the data of an object.

---

Q5. What are Methods?

Answer:

Methods define the actions an object can perform.

---

# Project Progress

Version 1.0

✔ Project Structure Created

✔ AI Agent Created

✔ OOP Started

✔ generate_email() Added

Next Version

* choose_prompt()
* Prompt Engineering
* Conditional Logic

# Day 3

## return

return sends a value back to the caller.

Unlike print(), it can be reused later.

Example

prompt = agent.choose_prompt("Software")

The variable prompt now stores the returned prompt.

---

## Why Separate prompts.py?

To keep the code modular.

Instead of writing hundreds of prompts inside agent.py, all prompts are stored in a dedicated file.

This improves readability and maintenance.

---

## Decision Making

if / elif / else

The AI Agent chooses different prompts for different industries.

Software → SOFTWARE_PROMPT

Healthcare → HEALTHCARE_PROMPT

Others → GENERAL_PROMPT

---

## Real Project Mapping

Industry

↓

choose_prompt()

↓

Prompt

↓

Gemini

# Day 4

## f-String

An f-string allows variables to be inserted directly into a string.

Example:

f"Hello {name}"

---

## Multi-line String

Triple quotes (""" """) are used to create strings that span multiple lines.

Useful for:

* Emails
* Prompts
* Messages

---

## Method Calling Another Method

A method can call another method using `self`.

Example:

generate_email()

↓

choose_prompt()

↓

Returns Prompt

↓

Build Email

This improves code reuse and avoids duplication.

---

## Why return instead of print?

The generated email will later be:

* Sent through Gmail
* Saved to JSON
* Stored in a database
* Logged

Therefore, the method returns the email instead of only printing it.

# Day 5 – File Handling + JSON

## File Handling

Python uses `with open()` to safely read and write files.

Example:

```python
with open("data/sent_emails.json", "w") as file:
```

---

## Dictionary

A dictionary stores data in key-value pairs.

Example:

```python
email_data = {
    "company": self.company,
    "industry": industry,
    "email": email
}
```

---

## json.dump()

`json.dump()` converts a Python dictionary into JSON and writes it to a file.

Flow:

Dictionary

↓

json.dump()

↓

JSON File

---

## Project Flow

generate_email()

↓

Returns Email (String)

↓

save_email()

↓

Create Dictionary

↓

json.dump()

↓

sent_emails.json

---

## Interview Point

A `.json` extension alone does **not** make a file JSON.

A file becomes valid JSON only when properly formatted JSON data is written into it.

# Day 6 – Reading JSON Data (json.load)

## Objective

Learn how to read data from a JSON file and convert it back into a Python Dictionary.

---

## json.load()

`json.load()` reads a JSON file and converts it into a Python Dictionary.

Flow:

Dictionary

↓

json.dump()

↓

JSON File

↓

json.load()

↓

Dictionary

---

## Read Mode

```python
with open("data/sent_emails.json", "r") as file:
```

* `"r"` means **Read Mode**.
* Used when we only want to read data from a file.

---

## Loading JSON

```python
email_data = json.load(file)
```

This converts JSON into a Python Dictionary.

---

## Returning Data

```python
return email_data
```

Instead of printing inside the method, we return the dictionary so it can be reused anywhere in the project.

---

## Accessing Dictionary Values

```python
data["company"]
data["industry"]
data["sender"]
data["date"]
data["email"]
```

Each key returns its corresponding value.

---

## Important Observation

When the JSON file is opened in VS Code, newline characters appear as:

```
\n
```

After using `json.load()` and printing:

```python
print(data["email"])
```

Python automatically converts `\n` into actual line breaks.

---

## Data Types

```python
type(data)
```

Output:

```python
<class 'dict'>
```

```python
type(data["email"])
```

Output:

```python
<class 'str'>
```

---

## Real Project Mapping

generate_email()

↓

Returns String

↓

save_email()

↓

Dictionary

↓

json.dump()

↓

JSON File

↓

json.load()

↓

Dictionary

↓

Access data using keys

---

## Interview Points

* `json.dump()` → Dictionary → JSON File
* `json.load()` → JSON File → Dictionary
* JSON is used for data exchange.
* Python works with Dictionaries.
* `data["email"]` returns a String.
* `data` itself is a Dictionary.

# Day 7 – Error Handling (try-except)

## Objective

Learn how to prevent the AI Agent from crashing when an unexpected error occurs.

---

## Why Error Handling?

Without error handling, if a file is missing or invalid, the entire program crashes.

Professional software should handle errors gracefully and continue running whenever possible.

---

## try-except

Syntax:

```python
try:
    # Risky code

except:
    # Handle the error
```

Python first executes the code inside the `try` block.

If an error occurs, Python skips the remaining `try` code and executes the matching `except` block.

---

## FileNotFoundError

This error occurs when Python tries to open a file that does not exist.

Example:

```python
try:
    with open("data/sent_emails.json", "r") as file:
        email_data = json.load(file)

    return email_data

except FileNotFoundError:
    print("❌ Email file not found.")
    return None
```

---

## None

`None` represents the absence of a value.

Examples:

```python
name = "Ayesha"      # String
age = 22             # Integer
data = {}            # Dictionary
result = None        # No value
```

When the file is missing, `load_email()` returns `None`.

---

## if data

Before accessing dictionary keys, always check whether data exists.

Example:

```python
if data:
    print(data["company"])
else:
    print("No email data found.")
```

This prevents program crashes.

---

## Project Flow

JSON File Exists

↓

load_email()

↓

Dictionary

↓

if data

↓

Access Dictionary Values

---

JSON File Missing

↓

FileNotFoundError

↓

except Block

↓

Return None

↓

Display Friendly Message

---

## Real Project Mapping

User requests data

↓

Python reads JSON

↓

If successful → Continue

↓

If failed → Handle error gracefully

---

## Interview Points

* `try` contains risky code.
* `except` handles specific errors.
* `FileNotFoundError` occurs when a file is missing.
* Returning `None` indicates that no data was loaded.
* `if data:` prevents accessing keys on a `None` object.
* Error handling improves application reliability and user experience.
###############
# Day 8 – Handling Invalid JSON (JSONDecodeError)

## Objective

Learn how to handle corrupted or invalid JSON files without crashing the application.

---

## What is JSONDecodeError?

`JSONDecodeError` occurs when the file exists but its contents are not valid JSON.

Example of Invalid JSON:

```text
abcdefg
```

or

```text
Hello World
```

or

```json
{
    "company": "ABC",
```

(The closing brace is missing.)

Python cannot convert these into a Dictionary.

---

## Handling Multiple Exceptions

```python
try:
    with open("data/sent_emails.json", "r") as file:
        email_data = json.load(file)

    return email_data

except FileNotFoundError:
    print("❌ Email file not found.")
    return None

except json.JSONDecodeError:
    print("❌ Invalid JSON format.")
    return None
```

---

## Difference Between Errors

### FileNotFoundError

* File does not exist.
* Example:

  * `sent_emails.json` has been deleted.

### JSONDecodeError

* File exists.
* But its contents are not valid JSON.
* Example:

  * File contains `abcdefg`.

---

## Program Flow

Program Starts

↓

Open JSON File

↓

If file is missing

↓

FileNotFoundError

↓

Return None

---

Open JSON File

↓

Read JSON

↓

If JSON is invalid

↓

JSONDecodeError

↓

Return None

---

Open JSON File

↓

Valid JSON

↓

Dictionary

↓

Continue Program

---

## Why Return None?

When an error occurs, we return `None` to indicate that no valid data was loaded.

Then we safely check:

```python
if data:
```

instead of directly accessing dictionary keys.

This prevents the application from crashing.

---

## Real AI Agent Mapping

Gemini Response

↓

JSON

↓

json.load()

↓

Dictionary

↓

If JSON is invalid

↓

Handle Error

↓

Show Friendly Message

↓

Continue Running

---

## Interview Points

* `FileNotFoundError` → File is missing.
* `JSONDecodeError` → File exists but JSON is invalid.
* One application can have multiple `except` blocks.
* Returning `None` is safer than allowing the application to crash.
* Always validate data before using it.
###########
# Day 9 – Logging System

## Objective

Learn how to store the execution history of the AI Outreach Agent.

---

## What is Logging?

Logging is the process of recording important events that happen while an application is running.

Instead of only displaying messages on the console, professional applications also save them into a log file.

---

## Why do we use Logging?

Logging helps developers:

* Debug errors
* Track application activity
* Monitor application behavior
* Understand what happened after the program finishes

---

## Project Structure

AI-Outreach-Agent/

app.py

agent.py

prompts.py

data/

```
sent_emails.json
```

logs/

```
log.py

app.log
```

---

## log.py

```python
def log(message):

    with open("logs/app.log", "a") as file:

        file.write(message + "\n")
```

---

## Understanding the Code

### def log(message)

Creates a reusable function.

`message` is the text that will be saved inside the log file.

Example:

```python
log("AI Agent Started")
```

---

### with open(...)

Opens the log file safely.

Python automatically closes the file after writing.

---

### "a"

Append Mode

* Keeps previous data.
* Adds new messages at the end of the file.

Comparison:

* `"r"` → Read
* `"w"` → Write (overwrite)
* `"a"` → Append

---

### file.write()

Writes the message into the file.

```python
file.write(message + "\n")
```

`\n` moves the next message to a new line.

---

## Application Flow

Program Starts

↓

log("AI Agent Started")

↓

Generate Email

↓

log("Email Generated")

↓

Save Email

↓

log("Email Saved")

↓

Load Email

↓

log("Email Loaded")

↓

Program Finished

↓

log("Program Finished")

---

## Example app.log

AI Agent Started

Email Generated

Email Saved

Email Loaded

Program Finished

---

## Difference Between print() and log()

print()

* Displays output on the console.
* Disappears when the program ends.

log()

* Saves information permanently in app.log.
* Useful for debugging and monitoring.

---

## Interview Points

What is Logging?

Logging is the process of storing important application events into a file for debugging, monitoring, and troubleshooting.

Why use Append Mode?

Because we want to preserve previous logs instead of overwriting them.

Why create a separate log.py?

To keep logging logic separate from business logic, making the code cleaner and easier to maintain.

Real software projects use Python's built-in logging module, but understanding a custom logger first helps build strong fundamentals.
#######
# Day 10 – Professional Logging using Python Logging Module

## Objective

Replace the custom logging system with Python's built-in `logging` module.

Professional software projects use the built-in logging library instead of manually writing messages to files.

---

# Why use the logging module?

Instead of writing:

```python
with open("logs/app.log", "a") as file:
    file.write(message)
```

Python provides the `logging` module which automatically handles:

* Log Levels
* Date & Time
* File Handling
* Formatting
* Better Debugging

---

# Import

```python
import logging
```

The `logging` module is built into Python.

No installation is required.

---

# Configure Logging

```python
logging.basicConfig(
    filename="logs/app.log",
    level=logging.INFO,
    format="%(asctime)s | %(levelname)s | %(message)s"
)
```

---

## filename

```python
filename="logs/app.log"
```

Specifies where logs will be stored.

---

## level

```python
level=logging.INFO
```

Specifies the minimum log level to save.

Current project uses:

INFO

---

## format

```python
"%(asctime)s | %(levelname)s | %(message)s"
```

Automatically stores:

* Date
* Time
* Log Level
* Message

Example Output:

2026-07-02 21:15:10 | INFO | AI Agent Started

---

# Helper Functions

Instead of writing:

```python
logging.info(...)
```

everywhere, we created helper functions.

```python
def log_info(message):
    logging.info(message)

def log_warning(message):
    logging.warning(message)

def log_error(message):
    logging.error(message)
```

Advantages:

* Cleaner code
* Centralized logging
* Easy future modifications

---

# Log Levels

INFO

Used for normal application events.

Example:

* Agent Started
* Email Generated
* Email Saved

---

WARNING

Used when something unexpected happens but the application can continue.

Example:

* API key missing
* Using default configuration

---

ERROR

Used when an operation fails.

Example:

* File Not Found
* Invalid JSON
* API Request Failed

---

# Difference Between Log Levels

INFO

Normal operation.

WARNING

Problem exists but application is still running.

ERROR

Operation failed.

---

# Project Structure

AI-Outreach-Agent/

logs/

```
app.log

log.py
```

---

# Flow

Application

↓

log_info()

↓

logging.info()

↓

logging Module

↓

app.log

---

# Professional Concepts Learned

* Built-in Logging
* Logging Configuration
* Log Levels
* Centralized Logging
* Helper Functions
* Loose Coupling
* Clean Architecture

---

# Interview Questions

Q1. Why use the logging module?

Answer:

Because it automatically manages timestamps, formatting, log levels and file handling. It is the standard logging solution used in professional Python applications.

---

Q2. Difference between INFO, WARNING and ERROR?

INFO

Normal application events.

WARNING

Unexpected situation but application continues.

ERROR

Operation failed due to an error.

---

# Future Topics

Later in the project we will learn:

* DEBUG
* CRITICAL
* Exception Logging
* Rotating Logs
* API Logging
* JSON Logging
* Production Logging
########
# Day 11 – Integrating AI Service Layer

## Objective

Separate AI communication from the main application by introducing a dedicated service layer.

## Concepts Learned

### 1. Service Layer

A Service Layer is responsible for handling communication with external services or APIs. Instead of letting the agent directly communicate with Gemini, a separate `GeminiService` class was created.

Benefits:

* Better code organization
* Easier maintenance
* Reusable AI communication logic
* Follows Single Responsibility Principle (SRP)

### 2. GeminiService Class

A new `GeminiService` class was introduced to manage AI-related operations.

Responsibilities:

* Receive prompts from the agent.
* Send prompts to Gemini AI.
* Return generated responses.

### 3. Agent and Service Separation

The `OutreachAgent` no longer contains AI communication logic. It delegates this responsibility to `GeminiService`.

Application Flow:

App → OutreachAgent → GeminiService → Gemini AI → Response → OutreachAgent → App

### 4. Clean Architecture

Each file now has a single responsibility.

* app.py → Runs the application
* agent.py → Business logic
* gemini_service.py → AI communication
* prompts.py → Prompt management
* config.py → Configuration
* logs → Application logging

## Key Learning

Separating business logic from external API communication makes the project easier to maintain, extend and debug. This architecture is commonly used in professional software development.
##########
# Day 12 – Environment Configuration & Gemini SDK Integration

## Objective

Prepare the project for real AI integration using secure configuration management and Google's official Gemini SDK.

## Concepts Learned

### 1. Environment Variables (.env)

Sensitive information such as API keys should never be hardcoded inside source code.

Instead, they are stored inside a `.env` file and accessed through `config.py`.

Benefits:

* Improved security
* Easier configuration management
* Environment-specific settings

### 2. Config Management

The `config.py` file was updated to centralize application settings.

Managed values include:

* Gemini API Key
* Gemini Model
* Application Name

### 3. Google Gemini SDK

Installed Google's official SDK:

* google-genai

This SDK acts as a bridge between the Python application and Gemini AI.

Application Flow:

Python Application → google-genai SDK → Gemini API → AI Response

### 4. Python Version Compatibility

The project initially used Python 3.15 Alpha, which caused dependency installation failures.

The environment was upgraded to Python 3.13 Stable for better compatibility with AI libraries.

### 5. Real AI Architecture

The project is now prepared to generate real AI responses once a valid Gemini API key is configured.

## Key Learning

The Gemini SDK does not generate AI responses itself. It simply connects the application to Google's Gemini API. A valid API key is required for authentication.
########
# Day 13 – Project Cleanup & Code Refactoring

## Objective

Improve the overall project structure by removing unnecessary code, improving readability, and following clean coding practices.

## Concepts Learned

### 1. Clean Code

Clean code is easy to read, understand, and maintain. A well-structured project reduces bugs and makes future development easier.

### 2. Removing Unused Code

The `api_key` attribute inside `OutreachAgent` became unnecessary because the `GeminiService` now reads the API key directly from `config.py`.

Instead of storing duplicate information, the project follows a single source of truth.

### 3. Separation of Responsibilities

Each component now has a clear responsibility.

* app.py → Runs the application.
* agent.py → Business logic.
* gemini_service.py → Communicates with Gemini AI.
* config.py → Stores application configuration.
* prompts.py → Stores prompt templates.
* logs/ → Stores application logs.

### 4. Improving Readability

Methods were grouped logically.

Recommended order:

1. Constructor
2. Prompt Selection
3. Email Generation
4. Save Email
5. Load Email

This makes navigation easier for developers.

### 5. Error Handling

Additional exception handling was added to improve stability while saving and loading files.

### 6. Future Refactoring

The `choose_prompt()` method can later be simplified using a dictionary lookup instead of multiple `if-elif` statements.

Example:

PROMPTS = {
"Software": SOFTWARE_PROMPT,
"Healthcare": HEALTHCARE_PROMPT,
}

This approach improves scalability and readability.

## Key Learning

Writing code is only the first step.

Professional developers continuously improve code quality by refactoring, removing duplication, and keeping responsibilities separate.

##########
# Day 14 – Prompt Engineering & Code Refactoring

## Objective

Improve the quality of AI-generated outreach emails by using prompt engineering techniques and refactor the project structure for better maintainability.

---

## Topics Covered

### 1. Prompt Engineering

Prompt engineering is the process of writing clear and detailed instructions for an AI model so it produces accurate and high-quality responses.

Instead of sending a simple prompt, we now provide:

* Company Name
* Sender Name
* Industry
* Writing Instructions
* Base Prompt

This gives the AI proper context before generating an email.

---

### 2. Personalized Prompt

The prompt now dynamically includes:

* Company Name
* Sender Name
* Industry

This allows the AI to generate more personalized emails instead of generic responses.

---

### 3. Prompt Rules

We instructed Gemini to:

* Generate only one email.
* Avoid placeholders such as `[Company Name]`.
* Use a professional tone.
* Keep the email concise.
* Include a subject line.
* End with the sender's name.
* Return only the final email.

---

### 4. Prompt Templates

Industry-specific prompts remain inside `prompts.py`.

Examples:

* Software
* Healthcare
* General

The agent simply selects the correct prompt and adds dynamic information before sending it to Gemini.

---

### 5. Dictionary-Based Prompt Selection

Instead of multiple `if-elif` statements, prompt selection now uses a dictionary.

Benefits:

* Cleaner code
* Easier to maintain
* Easy to add new industries

---

### 6. Dynamic Date

The email date is now generated automatically using Python's `datetime` module instead of using a hardcoded date.

---

### 7. Clean Project Structure

Current responsibilities:

* `app.py` → Starts the application
* `agent.py` → Business logic
* `gemini_service.py` → Gemini API communication
* `config.py` → Configuration
* `prompts.py` → Prompt templates
* `logs/` → Logging
* `data/` → Saved emails

---

## Key Learning

Prompt Engineering is one of the most important skills in AI development.

The quality of an AI application's output depends heavily on the quality of the prompt provided.

Good prompts produce better AI responses.
########
# Day 15 – Professional Code Quality

## Objective

Improve the AI Outreach Agent by making the code safer, more readable, and closer to production-quality Python.

---

# Topics Covered

## 1. Response Validation

AI responses should never be trusted blindly.

Instead of directly returning the generated email, we first validate the response.

If Gemini returns an empty response (`None`), the application:

* Logs the error
* Stops the workflow safely
* Prevents invalid data from being saved

This improves application reliability.

---

## 2. Type Hints

Type hints describe the expected input and output of functions.

Example:

```python
def generate_email(self, industry: str) -> str | None:
```

Benefits:

* Better code readability
* IDE auto-completion
* Easier debugging
* Easier collaboration with other developers

---

## 3. Docstrings

Each function now contains a short description explaining its purpose.

Example:

```python
"""
Generate a personalized outreach email
using Gemini AI.
"""
```

Benefits:

* Self-documenting code
* Easier maintenance
* Better project documentation

---

## 4. Better Logging

Logging is added to important steps instead of logging only errors.

Examples:

* Email generation started
* Email generated successfully
* Email saved
* Email loaded

Benefits:

* Easier debugging
* Better monitoring
* Professional workflow tracking

---

## 5. Cleaner Code

The project now follows a cleaner architecture.

Responsibilities are separated across different files.

* app.py → Starts the application
* agent.py → Business logic
* gemini_service.py → Gemini API communication
* prompts.py → Prompt templates
* config.py → Configuration
* logs → Logging
* data → JSON storage

---

# Key Learning

Professional software development is not only about writing code that works.

It is also about writing code that is:

* Readable
* Maintainable
* Scalable
* Reliable
* Easy for other developers to understand

Today's improvements focused on software quality rather than adding new features.
#########
# Day 16 – AI Outreach Agent Personalization

## Objective

Transform the AI Outreach Agent from a generic email generator into a personalized outreach assistant by providing recipient-specific information and allowing users to control the writing style.

---

# Topics Covered

## 1. Recipient Personalization

The AI agent now receives information about the recipient.

New attributes:

* Recipient Name
* Recipient Company
* Recipient Position

These details are included in the prompt so the generated email feels more personalized instead of generic.

Example:

```text
Recipient Name: John
Recipient Company: Microsoft
Recipient Position: HR Manager
```

---

## 2. Writing Tone

Users can specify the tone of the email.

Examples:

* Professional
* Friendly
* Formal
* Confident

The selected tone is passed to Gemini through the prompt.

---

## 3. Email Length

Users can choose the desired email length.

Options:

* Short
* Medium
* Long

The AI adjusts the generated email according to the selected length.

---

## 4. Improved Prompt Engineering

The prompt now contains:

* Sender information
* Company information
* Recipient details
* Industry
* Writing tone
* Email length
* Clear instructions for Gemini

This provides better context and produces higher-quality emails.

---

## 5. JSON Enhancement

The saved JSON structure now stores more information, such as:

* Recipient Name
* Recipient Company
* Recipient Position
* Tone
* Email Length

This makes the project more scalable for future analytics and reporting.

---

## 6. Console Output

The terminal output is made cleaner and easier to read, improving the overall user experience during testing.

---

# Key Learning

A powerful AI system is not built only by changing the model.

The quality of the output depends heavily on the quality of the input (Prompt Engineering).

The more relevant context we provide, the better the AI performs.

---

# Day 16 Outcome

By the end of Day 16, the AI Outreach Agent can generate personalized outreach emails using:

* Sender information
* Company information
* Recipient information
* Industry
* Tone
* Email length

The project is moving closer to a production-ready AI application.
############
# Day 17 Notes – AI Outreach Agent

## Topics Covered

### 1. Lead Model Refactoring

* Created a separate `Lead` class to store recipient information.
* Moved recipient-related data out of `OutreachAgent`.
* Learned the importance of keeping data in a single place.

**Lead Attributes**

* name
* company
* position
* industry

---

### 2. Single Source of Truth (SSOT)

Previously, recipient information existed in two places:

* `OutreachAgent`
* `Lead`

This caused duplicate data and made maintenance difficult.

After refactoring, recipient information is stored only inside the `Lead` object, making the code cleaner and easier to maintain.

---

### 3. Subject Generator

Implemented a separate AI method:

* `generate_subject()`

Purpose:

* Generate only the email subject.
* Keep subject generation separate from email generation.

This improves modularity and makes future updates easier.

---

### 4. Dynamic Prompt Personalization

Updated `choose_prompt()` to use:

* `lead.name`
* `lead.company`
* `lead.position`
* `lead.industry`

instead of hardcoded recipient values.

The prompt also includes:

* Sender name
* Company name
* Writing tone
* Email length

---

### 5. Constructor Refactoring

Simplified `OutreachAgent`.

Removed:

* recipient_name
* recipient_company
* recipient_position

Current responsibilities of `OutreachAgent`:

* sender_name
* company
* tone
* email_length
* GeminiService

Recipient information is now managed entirely by the `Lead` object.

---

### 6. JSON Structure Improvement

Updated the email saving logic to support:

* Sender
* Recipient
* Subject
* Email
* Industry
* Tone
* Email Length
* Date

This makes saved email records more complete and easier to reuse.

---

### 7. Code Architecture

Current application flow:

App.py

↓

Lead

↓

OutreachAgent

↓

Prompt Builder

↓

GeminiService

↓

Gemini API

↓

Generated Email

↓

JSON File

---

## Concepts Learned

* Refactoring
* Lead Model
* Object-Oriented Design
* Separation of Concerns
* Single Source of Truth (SSOT)
* Dynamic Prompt Engineering
* AI Subject Generation
* Cleaner Project Architecture

---

## Pending Improvement

Gemini is still generating a subject inside the email.

Next step:
Update the email prompt to explicitly instruct Gemini **not** to include a subject line, since subject generation is already handled separately.
#####################

# 📅 Day 18 – AI Outreach Agent

## 🎯 Objective

Convert the AI Outreach Agent from generating a single email to generating personalized emails for multiple leads using a CSV file.

---

# ✅ Completed Tasks

### 1. Refactored Agent to Use Lead Object

* Removed hardcoded recipient information.
* Updated all functions to accept a `Lead` object instead of individual values.

Functions updated:

* `generate_email()`
* `generate_subject()`
* `choose_prompt()`
* `save_email()`

---

### 2. Implemented CSV Loader

Created a new service:

`services/csv_service.py`

Responsibilities:

* Read `leads.csv`
* Convert each row into a `Lead` object
* Return a list of leads

---

### 3. Bulk Email Generation

Updated `app.py` to process multiple leads.

Workflow:

Load CSV

↓

Loop through leads

↓

Generate Subject

↓

Generate Email

↓

Save Email

---

### 4. Prompt Refactoring

Updated `choose_prompt()` to dynamically use:

* Recipient Name
* Company
* Position
* Industry
* Tone
* Email Length

instead of hardcoded values.

---

### 5. Subject Generator

Added a dedicated AI subject generator.

Implemented:

* `generate_subject()`

Subject generation is now separated from email generation.

---

### 6. JSON Saving Improvements

Updated `save_email()`.

Now stores:

* Sender
* Company
* Recipient
* Position
* Industry
* Tone
* Email Length
* Subject
* Email
* Date

---

### 7. TXT Export Service

Created:

`services/txt_service.py`

Purpose:

Export generated emails as text files inside the `exports/` folder.

---

# 🐞 Problems Solved

### CSV Import Error

Resolved module import issue for `CSVService`.

---

### Lead Variable Error

Moved email generation inside the loop.

---

### Duplicate Subject

Updated prompt instructions so Gemini does not generate another subject inside the email body.

---

### Gemini Quota Exhausted

Discovered that project logic was correct.

The issue was caused by the free Gemini API quota limit.

---

# 📚 Concepts Learned

* Service Layer Architecture
* CSV Processing
* Lead Object Integration
* Bulk Processing
* Prompt Refactoring
* JSON Handling
* Modular Project Structure

---

# 📁 Current Project Structure

AI-Outreach-Agent/

* app.py
* agent.py
* gemini_service.py
* prompts.py

models/

* lead.py

services/

* csv_service.py
* txt_service.py

data/

* leads.csv
* sent_emails.json

exports/

logs/

---

# 📝 Day 18 Changelog

## Added

* CSVService
* TXTService
* Bulk email generation
* Lead object integration
* Subject generation

## Improved

* Dynamic prompts
* Agent architecture
* JSON saving
* Project folder structure

## Fixed

* CSV loading issues
* Lead object errors
* Duplicate subject generation
* Multiple debugging issues

---

# ✅ Current Progress

Completed:

* AI Email Generator
* AI Subject Generator
* Lead Model
* CSV Loader
* Bulk Processing
* JSON Saving
* TXT Export Service

Pending:

* SMTP Integration
* HTML Email Support
* README
* GitHub Deployment
* Streamlit UI
* Portfolio Preparation

---

# 🎯 Day 18 Summary

Today the project evolved from a simple AI email generator into a bulk outreach system capable of processing multiple leads from a CSV file. The architecture became more modular through the introduction of dedicated services, making the project easier to maintain, extend, and prepare for real-world use.
###########

# Day 19 – Streamlit Dashboard (Version 2 Started)

## Completed

* Created `dashboard.py`
* Installed Streamlit
* Built the first dashboard interface
* Configured page title and layout
* Displayed project status on the web interface

## Learning

* Introduction to Streamlit
* Creating a web interface using Python
* Using `st.title()`, `st.write()`, `st.subheader()`, and `st.success()`
* Difference between terminal applications and GUI applications

## Project Progress

### Version 1 ✅

* AI Email Generation
* AI Subject Generation
* CSV Import
* JSON Storage
* TXT Export
* SMTP Integration
* GitHub Deployment

### Version 2 🚀

* Streamlit Dashboard (Started)

## Next Task

* Add CSV Upload functionality to the dashboard.
#########################
# Day 20 – Streamlit Dashboard (Version 2)

## Objective

Transform the AI Outreach Agent from a terminal-based application into a modern web application using Streamlit.

---

## Features Completed

### 1. Streamlit Dashboard Setup

- Installed Streamlit
- Created `dashboard.py`
- Configured page settings
- Added project title and layout

---

### 2. Campaign Settings Sidebar

Added a sidebar containing:

- Sender Name
- Company Name
- Tone Selection
- Email Length Selection
- CSV Upload

Purpose:
Provide users with campaign configuration before generating emails.

---

### 3. CSV Upload Integration

Implemented CSV upload using:

```python
st.sidebar.file_uploader()
```

Created a new CSVService function:

```python
load_uploaded_leads(uploaded_file)
```

Purpose:

- Read uploaded CSV directly from Streamlit
- Avoid saving temporary files
- Reuse existing Lead model

---

### 4. Lead Preview Table

Displayed uploaded leads inside the dashboard using:

```python
st.dataframe()
```

Information displayed:

- Name
- Company
- Position
- Industry
- Email

Purpose:

Allow users to verify uploaded data before AI processing.

---

### 5. Generate Emails Button

Added:

```python
st.button("🚀 Generate Emails")
```

Current functionality:

Displays a placeholder message indicating AI generation will be connected in the next phase.

---

### 6. Dashboard Refactoring

Reorganized dashboard into professional sections:

- Imports
- Page Configuration
- Sidebar
- CSV Upload
- Lead Preview
- Action Button
- Footer

Purpose:

Improve readability, maintainability, and scalability.

---

## Concepts Learned

- Streamlit Layout
- Sidebar Components
- File Upload Handling
- CSV Parsing from Uploaded Files
- DataFrame Rendering
- Separation of UI and Business Logic
- Professional Dashboard Structure

---

## Architecture

Dashboard

↓

Campaign Settings

↓

CSV Upload

↓

Lead Objects

↓

Lead Preview

↓

Generate Button

↓

AI Processing (Upcoming)

---

## Next Goals

- Connect Dashboard with OutreachAgent
- Generate AI Subjects
- Generate AI Emails
- Display Generated Emails
- Progress Bar
- Download JSON
- Download TXT
- SMTP Integration

#############
# Day 21 – Dashboard & OutreachAgent Integration

## Objective

Connect the Streamlit dashboard with the `OutreachAgent` while maintaining a clean and scalable architecture.

---

## Features Completed

### 1. Dashboard Connected with Backend

Imported:

```python
from agent import OutreachAgent
```

Purpose:

Allow the Streamlit dashboard to communicate with the AI backend instead of keeping business logic inside the UI.

---

### 2. Generate Emails Button Updated

Replaced the placeholder message with actual backend initialization.

Created:

```python
agent = OutreachAgent(
    sender_name=sender,
    company=company,
    tone=tone,
    email_length=email_length,
)
```

Purpose:

Create an AI agent using the campaign settings entered by the user.

---

### 3. Agent Configuration Display

Displayed the current campaign configuration inside the dashboard using:

```python
st.json(...)
```

Information shown:

* Sender Name
* Company
* Tone
* Email Length

Purpose:

Allow users to verify campaign settings before AI email generation.

---

## Concepts Learned

* Frontend and Backend Separation
* Object Initialization from UI Inputs
* Streamlit JSON Display
* Clean Dashboard Architecture
* Professional Software Development Workflow

---

## Current Dashboard Workflow

Dashboard

↓

Campaign Settings

↓

CSV Upload

↓

Lead Preview

↓

Generate Emails Button

↓

OutreachAgent Initialization

↓

Ready for AI Processing

---

## Architecture

dashboard.py

↓

OutreachAgent

↓

Gemini Service (Upcoming)

↓

TXT Service

↓

SMTP Service

---

## Progress

### Version 1 ✅

* CSV Import
* Gemini Subject Generation
* Gemini Email Generation
* JSON Export
* TXT Export
* SMTP Integration
* GitHub Deployment

### Version 2 🚀

* Streamlit Dashboard
* Campaign Settings Sidebar
* CSV Upload
* Lead Preview
* Generate Emails Button
* Dashboard Connected with OutreachAgent

---

## Next Goals

* Generate AI Subject from Dashboard
* Generate AI Email from Dashboard
* Display Generated Emails
* Progress Bar
* Download Generated Emails
* Campaign Summary
* Dashboard-based SMTP Sending
* Analytics & Reports

---

## Learning Outcome

Today marked the transition from a static dashboard to a functional frontend connected with the application's backend. The project now follows a cleaner software architecture where the dashboard handles user interaction and the `OutreachAgent` manages business logic, making the application easier to maintain and extend.
#################
# Day 22 — CSV Upload Module Completed

## Objective
Implement a complete CSV Upload workflow for the AI Outreach Agent and stabilize the dashboard.

## Tasks Completed

### Dashboard Refactoring
- Cleaned and reorganized dashboard.py
- Removed duplicate logic
- Improved code readability
- Structured dashboard into logical sections

### CSV Upload
- Integrated Streamlit File Uploader
- Connected uploaded file with CSVService
- Successfully loaded uploaded CSV files

### CSV Service
- Completely rebuilt csv_service.py
- Replaced csv.DictReader with Pandas
- Added helper method for DataFrame to Lead conversion
- Added required column validation
- Improved overall code quality

### Lead Preview
- Displayed uploaded leads inside Streamlit
- Added total lead count
- Created responsive preview table

### Bug Fixes
- Fixed UploadedFile handling
- Fixed bytes/string CSV parsing issue
- Fixed duplicate dashboard execution
- Stabilized CSV Upload workflow
- Successfully resolved CSV loading issue

## Concepts Learned
- Streamlit UploadedFile
- Pandas DataFrame
- CSV Processing
- Object-Oriented Programming
- Service Layer Architecture
- Exception Handling
- Clean Code Principles

## Current Project Status

Completed
- Gemini Integration
- Prompt Engineering
- Lead Model
- Campaign Settings
- Dashboard UI
- CSV Upload
- CSV Processing
- Lead Preview

Pending
- AI Email Generation
- Export Generated Emails
- Campaign Analytics
- Professional Dashboard UI
- Download Reports

## Outcome
Successfully implemented a stable CSV Upload Module capable of:
- Uploading CSV files
- Reading lead information
- Converting rows into Lead objects
- Displaying lead previews
- Preparing leads for AI email generation

## Challenges Faced
- CSV parsing issues
- UploadedFile handling
- Duplicate dashboard logic
- Streamlit execution flow
- Dashboard cleanup and restructuring

## Result
CSV Upload Module Completed Successfully ✅
Dashboard Stabilized ✅
Lead Preview Working Successfully ✅

