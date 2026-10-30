"""
PyLearn — LLM-Based Python Learning System
RCSA Graduate Project — Harshitha Bommi · UCO

Run:  python3 -m streamlit run app.py
Deps: pip3 install streamlit pylint requests pandas
LLM:  ollama run phi3:mini  (optional — falls back to built-in C.O.D.E. explanations)
"""

import streamlit as st
import subprocess, tempfile, json, os, datetime, hashlib, requests
from pathlib import Path

# ─────────────────────────────────────────────────────────────────────────────
#  Config
# ─────────────────────────────────────────────────────────────────────────────
OLLAMA_URL    = "http://localhost:11434/api/generate"
MODEL_NAME    = "phi3:mini"
GROQ_URL      = "https://api.groq.com/openai/v1/chat/completions"
GROQ_MODEL = "openai/gpt-oss-20b"
DATA_FILE     = Path("data/users.json")
PROGRESS_FILE = Path("data/progress.json")
DATA_FILE.parent.mkdir(parents=True, exist_ok=True)

TOTAL_MODULES = 15   # update if adding more

# ─────────────────────────────────────────────────────────────────────────────
#  L.E.A.R.N. concept framework
#  Each module has a "learn" dict with five keys:
#    L — Label:   What is this concept and why does Python need it?
#    E — Example: A clear, runnable code snippet
#    A — Analogy: Real-world comparison that makes it click
#    R — Rule:    The single most important rule to remember
#    N — Note:    The most common beginner mistake to avoid
# ─────────────────────────────────────────────────────────────────────────────

def render_learn(learn):
    """Display a L.E.A.R.N. concept card with styled sections."""
    st.markdown("""
<div style="background:#0f172a;color:#e2e8f0;border-radius:10px;
            padding:14px 20px 6px 20px;margin-bottom:16px;font-size:0.95em;">
  <strong style="letter-spacing:3px;font-size:1.05em;">L.E.A.R.N.</strong>
  &nbsp;·&nbsp; <span style="opacity:0.75;">Label · Example · Analogy · Rule · Note</span>
</div>
""", unsafe_allow_html=True)

    icons  = {"L": ("🏷️", "Label",   "#1e3a5f", "#bfdbfe"),
              "E": ("💻", "Example", "#1e4038", "#a7f3d0"),
              "A": ("🔗", "Analogy", "#3b1f5e", "#ddd6fe"),
              "R": ("📌", "Rule",    "#4a2512", "#fed7aa"),
              "N": ("⚠️", "Note",    "#3b1e1e", "#fecaca")}

    for key in ["L", "E", "A", "R", "N"]:
        icon, label, bg, border = icons[key]
        content = learn.get(key, "")
        # code blocks inside learn sections — render as markdown inside the card
        st.markdown(
            f'<div style="background:{bg};border-left:4px solid {border};'
            f'border-radius:8px;padding:12px 16px;margin-bottom:10px;">'
            f'<strong style="color:{border};font-size:1.1em;">{icon} {key} — {label}</strong>'
            f'</div>',
            unsafe_allow_html=True
        )
        st.markdown(content)
        st.markdown("")   # breathing room

# ─────────────────────────────────────────────────────────────────────────────
#  15 Learning Modules — full Python curriculum
# ─────────────────────────────────────────────────────────────────────────────
MODULES = [
    # ── 1. Variables & Data Types ────────────────────────────────────────────
    {
        "id": "M01",
        "title": "Variables & Data Types",
        "icon": "🧱",
        "tagline": "How Python stores and labels information",
        "learn": {
            "L": (
                "A **variable** is a named container that stores a value. "
                "You create one with `=`. Python has four basic data types:\n\n"
                "| Type | Keyword | Stores |\n"
                "|------|---------|--------|\n"
                "| Integer | `int` | Whole numbers: `42`, `-7` |\n"
                "| Float | `float` | Decimals: `3.14`, `-0.5` |\n"
                "| String | `str` | Text: `\"Alice\"`, `'hello'` |\n"
                "| Boolean | `bool` | Truth: `True` or `False` |"
            ),
            "E": (
                "```python\n"
                "name    = \"Alice\"   # str  — always in quotes\n"
                "age     = 21        # int  — whole number\n"
                "gpa     = 3.85      # float — decimal\n"
                "passed  = True      # bool — capital T!\n\n"
                "print(type(age))    # <class 'int'>\n"
                "print(name, \"is\", age, \"years old\")\n"
                "```"
            ),
            "A": (
                "Think of a variable like a **labeled box**. "
                "The variable name is the label written on the box (`age`), "
                "and the value is what you put inside (`21`). "
                "Python reads the label to find the right box whenever you use it."
            ),
            "R": (
                "**Python infers the type automatically** — you never write `int age = 21`. "
                "Just assign it. But the type matters: `\"21\"` (string) and `21` (integer) "
                "are different — you can't do math on the string version."
            ),
            "N": (
                "🚫 **Common mistake:** mixing up strings and numbers.\n\n"
                "```python\nage = \"21\"          # looks right, but it's a string!\n"
                "next_year = age + 1  # TypeError: can only concatenate str to str\n\n"
                "age = 21             # ✓ integer — now math works\n"
                "next_year = age + 1  # 22\n```"
            ),
        },
        "challenge_intro": "This code tries to calculate a student's GPA and print a summary. Can you spot what types each variable should be?",
        "challenge_code": "student_name = \"Maria\"\ncredits = 45\ngpa = 3.72\nis_full_time = True\n\nprint(student_name, \"has\", credits, \"credits and a GPA of\", gpa)\nprint(\"Full-time student:\", is_full_time)\nprint(\"Type of gpa:\", type(gpa))",
        "pylint_ids": [],
    },

    # ── 2. Strings ───────────────────────────────────────────────────────────
    {
        "id": "M02",
        "title": "Strings & String Methods",
        "icon": "🔡",
        "tagline": "Working with text in Python",
        "learn": {
            "L": (
                "A **string** (`str`) is any sequence of characters inside quotes — single `'` or double `\"`. "
                "Python strings come with dozens of built-in methods for searching, formatting, and transforming text."
            ),
            "E": (
                "```python\n"
                "name = \"harshitha bommi\"\n\n"
                "# f-string — modern way to embed variables\n"
                "msg = f\"Welcome, {name.title()}!\"\n\n"
                "# Common methods\n"
                "name.upper()           # 'HARSHITHA BOMMI'\n"
                "name.strip()           # removes surrounding spaces\n"
                "name.replace(\"bommi\", \"uco\")  # 'harshitha uco'\n"
                "name.split()           # ['harshitha', 'bommi']\n"
                "len(name)              # 16 (number of characters)\n\n"
                "# Indexing\n"
                "name[0]                # 'h'  (first character)\n"
                "name[-1]               # 'i'  (last character)\n"
                "name[0:9]              # 'harshitha' (slice)\n"
                "```"
            ),
            "A": (
                "A string is like a **train of carriages**: each carriage holds one character. "
                "Index `[0]` is the first carriage, `[-1]` is the last. "
                "Methods are like tools you run the entire train through — they give you a *new* train, "
                "they don't modify the original."
            ),
            "R": (
                "**Strings are immutable.** A method always returns a *new* string — it never changes the original.\n\n"
                "```python\nname = \"alice\"\nname.upper()       # returns 'ALICE' but name is still 'alice'\n"
                "name = name.upper()  # ✓ now name is 'ALICE'\n```"
            ),
            "N": (
                "🚫 **Common mistake:** calling a method but not saving the result.\n\n"
                "```python\ntext = \"  hello  \"\n"
                "text.strip()       # result thrown away!\n"
                "print(text)        # still '  hello  '\n\n"
                "text = text.strip()  # ✓ save the result\n"
                "print(text)          # 'hello'\n```"
            ),
        },
        "challenge_intro": "This code builds a formatted student ID string. Edit it to try different string methods and see what each one does.",
        "challenge_code": "first_name = \"harshitha\"\nlast_name  = \"bommi\"\n\n# Format the name properly\nfull_name = first_name.capitalize() + \" \" + last_name.capitalize()\nstudent_id = f\"ID: {full_name.upper()[:3]}-{len(full_name):03d}\"\n\nprint(f\"Student: {full_name}\")\nprint(f\"Student ID: {student_id}\")\nprint(f\"Name has {len(full_name)} characters\")",
        "pylint_ids": [],
    },

    # ── 3. Conditionals ───────────────────────────────────────────────────────
    {
        "id": "M03",
        "title": "Conditionals (if / elif / else)",
        "icon": "🔀",
        "tagline": "Making decisions in your code",
        "learn": {
            "L": (
                "A **conditional** tells Python to run a block of code *only when* a condition is `True`. "
                "`if` checks the first condition, `elif` checks alternatives, `else` catches everything that didn't match."
            ),
            "E": (
                "```python\n"
                "score = 85\n\n"
                "if score >= 90:\n"
                "    grade = 'A'\n"
                "elif score >= 80:\n"
                "    grade = 'B'    # ← this branch runs\n"
                "elif score >= 70:\n"
                "    grade = 'C'\n"
                "else:\n"
                "    grade = 'F'\n\n"
                "# Comparison operators: ==  !=  <  >  <=  >=\n"
                "# Boolean operators:   and  or  not\n"
                "if score >= 60 and score < 90:\n"
                "    print('Passing but not an A')\n"
                "```"
            ),
            "A": (
                "Think of `if/elif/else` like a **bouncer at a concert**. "
                "The bouncer checks conditions one by one from top to bottom. "
                "The moment one condition is `True`, that person gets in and the bouncer stops checking. "
                "`else` is the default — it covers everyone who didn't match any earlier rule."
            ),
            "R": (
                "**Conditions are checked top to bottom; the first `True` one wins and the rest are skipped.** "
                "Order matters — if you put `score >= 60` before `score >= 90`, "
                "an A student would be caught by the weaker condition first and never reach the A branch."
            ),
            "N": (
                "🚫 **Common mistake:** using `=` (assignment) instead of `==` (comparison).\n\n"
                "```python\nif score = 90:   # SyntaxError — you can't assign inside if\n"
                "if score == 90:  # ✓ comparison — are they equal?\n```\n\n"
                "Also watch for **dead code** — `if True:` always runs; "
                "`else:` below it can never run. pylint flags this as `W0125`."
            ),
        },
        "challenge_intro": "This letter-grade function has a logic gap — one range of scores won't produce the right output. Can you find and fix it?",
        "challenge_code": "def letter_grade(score):\n    if score >= 90:\n        return \"A\"\n    elif score >= 80:\n        return \"B\"\n    elif score >= 70:\n        return \"C\"\n    elif score >= 60:\n        return \"D\"\n    else:\n        return \"F\"\n\nprint(letter_grade(95))   # A\nprint(letter_grade(83))   # B\nprint(letter_grade(55))   # F",
        "pylint_ids": ["W0125"],
    },

    # ── 4. for Loops ─────────────────────────────────────────────────────────
    {
        "id": "M04",
        "title": "for Loops",
        "icon": "🔄",
        "tagline": "Repeating actions over a sequence",
        "learn": {
            "L": (
                "A **`for` loop** repeats a block of code once for every item in a sequence "
                "(a list, a string, a `range`, a dictionary...). "
                "Use it whenever you know *what* you're iterating over."
            ),
            "E": (
                "```python\n"
                "# Iterate over a list\n"
                "fruits = ['apple', 'banana', 'cherry']\n"
                "for fruit in fruits:\n"
                "    print(fruit)\n\n"
                "# range() — generate numbers\n"
                "for i in range(5):        # 0, 1, 2, 3, 4\n"
                "    print(i)\n\n"
                "# enumerate() — index AND value together\n"
                "for i, name in enumerate(['Alice', 'Bob'], start=1):\n"
                "    print(f'{i}. {name}')  # 1. Alice  /  2. Bob\n\n"
                "# Accumulate a total\n"
                "total = 0\n"
                "for n in [10, 20, 30]:\n"
                "    total += n\n"
                "print(total)   # 60\n"
                "```"
            ),
            "A": (
                "A `for` loop is like a **conveyor belt in a factory**: "
                "each item comes along one at a time, the same operation is applied, "
                "and it stops automatically when the belt is empty. "
                "You don't count items yourself — Python handles that."
            ),
            "R": (
                "**The loop variable takes on each item's value in turn.** "
                "After the loop finishes, it holds the *last* value it had — "
                "but only if the loop ran at least once. "
                "If the sequence is empty, the variable is never created."
            ),
            "N": (
                "🚫 **Common mistake:** using a loop variable *after* the loop "
                "when the sequence might be empty.\n\n"
                "```python\ndata = []\n"
                "for item in data:\n"
                "    last = item        # never runs!\n"
                "print(last)           # NameError — last was never created\n\n"
                "last = None           # ✓ safe default before the loop\n"
                "for item in data:\n"
                "    last = item\n"
                "print(last)           # None (safe)\n```"
            ),
        },
        "challenge_intro": "This code calculates the class average but is missing a step inside the loop. What value needs to be accumulated?",
        "challenge_code": "scores = [88, 72, 95, 61, 84]\ntotal = 0\n\nfor score in scores:\n    total += score\n\naverage = total / len(scores)\nprint(f\"Class average: {average:.1f}\")\n\n# Bonus: also print each score with its rank\nfor i, score in enumerate(sorted(scores, reverse=True), start=1):\n    print(f\"  Rank {i}: {score}\")",
        "pylint_ids": [],
    },

    # ── 5. while Loops ────────────────────────────────────────────────────────
    {
        "id": "M05",
        "title": "while Loops",
        "icon": "⏳",
        "tagline": "Repeating until a condition changes",
        "learn": {
            "L": (
                "A **`while` loop** keeps repeating its body *as long as* a condition stays `True`. "
                "Use it when you don't know in advance how many times you'll need to repeat — "
                "for example, waiting for valid user input or a sensor reading."
            ),
            "E": (
                "```python\n"
                "# Count up to 4\n"
                "count = 0\n"
                "while count < 5:\n"
                "    print(count)\n"
                "    count += 1       # MUST change count or loop runs forever!\n\n"
                "# break — exit immediately when condition met\n"
                "while True:\n"
                "    password = input('Enter password: ')\n"
                "    if password == 'secret':\n"
                "        print('Access granted!')\n"
                "        break        # exits the infinite loop\n\n"
                "# continue — skip to next iteration\n"
                "n = 0\n"
                "while n < 10:\n"
                "    n += 1\n"
                "    if n % 2 == 0:\n"
                "        continue     # skip even numbers\n"
                "    print(n)         # prints 1, 3, 5, 7, 9\n"
                "```"
            ),
            "A": (
                "A `while` loop is like a **vending machine**: it keeps asking "
                "'was the correct amount inserted?' on every button press. "
                "As long as the answer is no, it loops. The moment the condition "
                "is met (enough coins), it stops and dispenses. "
                "If you never insert coins, it waits forever — just like an infinite loop."
            ),
            "R": (
                "**Something inside the loop must eventually make the condition `False` (or `break`).** "
                "Forgetting to update the variable the condition tests is the #1 cause of "
                "infinite loops that freeze your program."
            ),
            "N": (
                "🚫 **Common mistake:** forgetting to update the loop variable.\n\n"
                "```python\ncount = 0\nwhile count < 5:\n"
                "    print(count)    # prints 0 forever — count never changes!\n\n"
                "count = 0\nwhile count < 5:\n"
                "    print(count)\n"
                "    count += 1      # ✓ loop ends after 5 iterations\n```\n\n"
                "If your program freezes, press **Ctrl+C** to stop it."
            ),
        },
        "challenge_intro": "This countdown function should print from n down to 1, then 'Blast off!' — but something makes it count wrong. Can you fix it?",
        "challenge_code": "def countdown(n):\n    while n > 0:\n        print(n)\n        n -= 1\n    print(\"Blast off! 🚀\")\n\ncountdown(5)",
        "pylint_ids": [],
    },

    # ── 6. Functions ─────────────────────────────────────────────────────────
    {
        "id": "M06",
        "title": "Functions & Return Values",
        "icon": "⚙️",
        "tagline": "Reusable blocks that do one job well",
        "learn": {
            "L": (
                "A **function** is a named, reusable block of code. "
                "You `def`ine it once and `call` it as many times as you need. "
                "Functions take *parameters* (inputs) and use `return` to send a result back."
            ),
            "E": (
                "```python\n"
                "def greet(name, greeting='Hello'):\n"
                "    \"\"\"Return a formatted greeting string.\"\"\"\n"
                "    return f'{greeting}, {name}!'\n\n"
                "print(greet('Alice'))          # Hello, Alice!\n"
                "print(greet('Bob', 'Hi'))      # Hi, Bob!\n\n"
                "# Without return — Python gives back None silently\n"
                "def square(n):\n"
                "    n * n             # ← calculated then thrown away!\n\n"
                "def square(n):        # ← corrected\n"
                "    return n * n\n\n"
                "print(square(5))      # 25\n"
                "```"
            ),
            "A": (
                "A function is like a **recipe card**: you write the recipe once "
                "(define the function), then follow it as many times as you cook "
                "(call the function). The ingredients you add are the *arguments*, "
                "and the finished dish is the *return value*. "
                "Without `return`, the kitchen makes the food but never serves it."
            ),
            "R": (
                "**Always use `return` to send a result back.** "
                "Without it, Python returns `None` — no error, no warning, just silence. "
                "This is one of the trickiest bugs because the code runs without crashing, "
                "but the caller gets `None` where they expected a value."
            ),
            "N": (
                "🚫 **Common mistake:** calculating without returning.\n\n"
                "```python\ndef area(w, h):\n    w * h          # computed, instantly discarded\n\n"
                "result = area(5, 3)\n"
                "print(result)         # None  ← not 15!\n\n"
                "def area(w, h):\n    return w * h   # ✓\n\n"
                "print(area(5, 3))     # 15\n```"
            ),
        },
        "challenge_intro": "This function should return the area of a circle but currently returns nothing. What's the missing keyword?",
        "challenge_code": "import math\n\ndef circle_area(radius):\n    \"\"\"Return the area of a circle with the given radius.\"\"\"\n    math.pi * radius ** 2    # calculated but not returned!\n\ndef circle_circumference(radius):\n    \"\"\"Return the circumference of a circle.\"\"\"\n    return 2 * math.pi * radius\n\nr = 5\nprint(f\"Area:          {circle_area(r)}\")\nprint(f\"Circumference: {circle_circumference(r):.2f}\")",
        "pylint_ids": ["W0104"],
    },

    # ── 7. Lists ─────────────────────────────────────────────────────────────
    {
        "id": "M07",
        "title": "Lists",
        "icon": "📋",
        "tagline": "Ordered collections of items",
        "learn": {
            "L": (
                "A **list** is an *ordered*, *mutable* (changeable) collection of items. "
                "Create one with square brackets `[]`. Lists can hold any mix of types, "
                "and their position (index) starts at 0."
            ),
            "E": (
                "```python\n"
                "scores = [88, 72, 95, 61]\n\n"
                "# Indexing\n"
                "scores[0]           # 88  (first)\n"
                "scores[-1]          # 61  (last)\n"
                "scores[1:3]         # [72, 95]  (slice)\n\n"
                "# Methods\n"
                "scores.append(99)   # add to end\n"
                "scores.remove(72)   # remove first 72\n"
                "scores.sort()       # sort in-place\n"
                "len(scores)         # number of items\n\n"
                "# List comprehension\n"
                "passing = [s for s in scores if s >= 70]\n"
                "squares = [x**2 for x in range(1, 6)]  # [1,4,9,16,25]\n"
                "```"
            ),
            "A": (
                "A list is like a **numbered queue at a coffee shop**: position matters, "
                "you can add/remove people anywhere, and you always know who is first (`[0]`) "
                "and who is last (`[-1]`). You can also slice the queue — "
                "'give me customers 2 through 4' — with `[1:4]`."
            ),
            "R": (
                "**Lists are mutable — methods like `.sort()` change the original in-place.** "
                "Use `sorted(list)` if you want a sorted *copy* and need to keep the original order.\n\n"
                "```python\noriginal = [3, 1, 2]\ncopy = sorted(original)  # [1, 2, 3] — original unchanged\noriginal.sort()          # original is now [1, 2, 3] too\n```"
            ),
            "N": (
                "🚫 **Common mistake:** confusing `list.sort()` (in-place, returns `None`) "
                "with `sorted(list)` (returns a new sorted list).\n\n"
                "```python\nscores = [3, 1, 2]\nresult = scores.sort()   # None! sort() returns nothing\nprint(result)            # None  ← not what you wanted\n\n"
                "result = sorted(scores)  # ✓ returns a new sorted list\nprint(result)            # [1, 2, 3]\n```"
            ),
        },
        "challenge_intro": "This grade tracker has a bug — one list operation works incorrectly for the way Python lists work. Can you find it?",
        "challenge_code": "grades = [85, 92, 78, 90, 88]\n\n# Add a new grade\ngrades.append(95)\n\n# Find the highest and lowest\nbest  = max(grades)\nworst = min(grades)\n\n# Sort a COPY (so original stays unsorted)\nsorted_grades = sorted(grades)\n\nprint(f\"All grades:   {grades}\")\nprint(f\"Sorted:       {sorted_grades}\")\nprint(f\"Best:  {best}  |  Worst: {worst}\")\nprint(f\"Average: {sum(grades)/len(grades):.1f}\")\n\n# List comprehension: grades above 89\nhonors = [g for g in grades if g >= 90]\nprint(f\"Honors grades: {honors}\")",
        "pylint_ids": [],
    },

    # ── 8. Dictionaries ───────────────────────────────────────────────────────
    {
        "id": "M08",
        "title": "Dictionaries",
        "icon": "📖",
        "tagline": "Storing data as key-value pairs",
        "learn": {
            "L": (
                "A **dictionary** maps *keys* to *values*. "
                "Create one with curly braces `{}`. "
                "Keys are usually strings; values can be anything. "
                "Unlike lists, you look things up by name — not by position."
            ),
            "E": (
                "```python\n"
                "student = {\n"
                "    'name':  'Alice',\n"
                "    'age':   21,\n"
                "    'major': 'Computer Science'\n"
                "}\n\n"
                "# Access\n"
                "student['name']              # 'Alice'\n"
                "student.get('phone', 'N/A')  # 'N/A' — safe, no KeyError\n\n"
                "# Add / update / delete\n"
                "student['gpa'] = 3.9         # add new key\n"
                "student['age'] = 22          # update existing\n"
                "del student['major']         # remove\n\n"
                "# Loop\n"
                "for key, value in student.items():\n"
                "    print(f'{key}: {value}')\n"
                "```"
            ),
            "A": (
                "A dictionary is like a **phone book**: you look up a *name* (key) "
                "to find a *number* (value). You don't need to know which page it's on — "
                "just the name. That's fundamentally different from a list, "
                "where you need to know the *position* (index 0, 1, 2...)."
            ),
            "R": (
                "**Keys must be unique.** Assigning the same key twice overwrites the value — "
                "no warning, no error.\n\n"
                "```python\nd = {'score': 85}\nd['score'] = 90    # silent overwrite — 85 is gone\nprint(d)           # {'score': 90}\n```"
            ),
            "N": (
                "🚫 **Common mistake:** using `dict['key']` when the key might not exist.\n\n"
                "```python\nstudent = {'name': 'Alice'}\nprint(student['phone'])        # KeyError — 'phone' not in dict\n\n"
                "print(student.get('phone', 'N/A'))  # ✓ 'N/A' — safe default\n```\n\n"
                "Always use `.get(key, default)` for keys that might be absent."
            ),
        },
        "challenge_intro": "This student record system uses a dictionary. Add code to safely retrieve the student's minor (which might not exist) and to loop through and print all their information.",
        "challenge_code": "student = {\n    \"name\": \"Harshitha\",\n    \"major\": \"Computer Science\",\n    \"gpa\": 3.9,\n    \"credits\": 60\n}\n\n# Safe access — won't crash if key is missing\nminor = student.get(\"minor\", \"Undecided\")\nprint(f\"Minor: {minor}\")\n\n# Add graduation year\nstudent[\"graduation\"] = 2026\n\n# Print all student info\nprint(\"\\n--- Student Record ---\")\nfor key, value in student.items():\n    print(f\"  {key.capitalize():15} {value}\")",
        "pylint_ids": [],
    },

    # ── 9. Error Handling ────────────────────────────────────────────────────
    {
        "id": "M09",
        "title": "Error Handling (try / except)",
        "icon": "⚠️",
        "tagline": "Keeping your program running when things go wrong",
        "learn": {
            "L": (
                "**Error handling** lets you catch problems at runtime and respond gracefully "
                "instead of crashing. Python uses `try` (risky code), `except` (what to do if it fails), "
                "and `finally` (always runs — clean-up)."
            ),
            "E": (
                "```python\n"
                "try:\n"
                "    number = int(input('Enter a number: '))\n"
                "    result = 100 / number\n"
                "    print(f'Result: {result}')\n"
                "except ValueError:\n"
                "    print('That is not a valid number!')\n"
                "except ZeroDivisionError:\n"
                "    print('Cannot divide by zero!')\n"
                "finally:\n"
                "    print('Done.')   # always runs\n\n"
                "# Common exceptions\n"
                "# ValueError       — wrong value: int('abc')\n"
                "# TypeError        — wrong type: 'a' + 1\n"
                "# ZeroDivisionError— 10 / 0\n"
                "# FileNotFoundError— open missing file\n"
                "# KeyError         — dict key missing\n"
                "# IndexError       — list index out of range\n"
                "```"
            ),
            "A": (
                "Error handling is like a **safety net under a trapeze artist**. "
                "The artist (your code) tries the move (risky operation). "
                "If they fall (exception), the net (except) catches them — "
                "the show goes on instead of ending in disaster. "
                "`finally` is the stage crew that cleans up regardless."
            ),
            "R": (
                "**Catch the most specific exception you can.** "
                "`except Exception:` catches everything including bugs you didn't mean to hide. "
                "Use `except ValueError:` when you expect that exact problem — "
                "let everything else crash loudly so you notice real bugs."
            ),
            "N": (
                "🚫 **Common mistake:** catching all exceptions and swallowing errors silently.\n\n"
                "```python\ntry:\n    result = risky_function()\nexcept:              # catches EVERYTHING — even typos!\n    pass             # silent failure — you'll never know what broke\n\n"
                "try:\n    result = risky_function()\nexcept ValueError as e:  # ✓ specific and informative\n    print(f'Value error: {e}')\n```"
            ),
        },
        "challenge_intro": "This division function crashes on bad input. Add error handling so it returns a helpful message instead of crashing.",
        "challenge_code": "def safe_divide(a, b):\n    try:\n        result = a / b\n        return f\"{a} / {b} = {result:.2f}\"\n    except ZeroDivisionError:\n        return \"Error: cannot divide by zero\"\n    except TypeError:\n        return \"Error: both inputs must be numbers\"\n\nprint(safe_divide(10, 2))    # 10 / 2 = 5.00\nprint(safe_divide(10, 0))    # Error: cannot divide by zero\nprint(safe_divide(10, \"x\"))  # Error: both inputs must be numbers",
        "pylint_ids": [],
    },

    # ── 10. File I/O ─────────────────────────────────────────────────────────
    {
        "id": "M10",
        "title": "File I/O",
        "icon": "📁",
        "tagline": "Reading and writing files safely",
        "learn": {
            "L": (
                "Python reads and writes files with `open()`. Always pair it with `with` — "
                "the `with` block closes the file automatically, even if an error occurs. "
                "Mode `'r'` reads, `'w'` writes (overwrites), `'a'` appends."
            ),
            "E": (
                "```python\n"
                "# Read a file\n"
                "with open('notes.txt', 'r', encoding='utf-8') as f:\n"
                "    content = f.read()       # whole file as string\n"
                "    # OR  lines = f.readlines()  # list of lines\n\n"
                "# Write a file (creates or overwrites)\n"
                "with open('output.txt', 'w', encoding='utf-8') as f:\n"
                "    f.write('Hello, file!\\n')\n\n"
                "# Append (adds to end)\n"
                "with open('log.txt', 'a', encoding='utf-8') as f:\n"
                "    f.write('New entry\\n')\n\n"
                "# Safe read — handles missing file\n"
                "try:\n"
                "    with open('data.txt', encoding='utf-8') as f:\n"
                "        data = f.read()\n"
                "except FileNotFoundError:\n"
                "    data = ''   # safe default\n"
                "```"
            ),
            "A": (
                "Opening a file in Python is like **checking out a library book**: "
                "you go to the library (`open()`), borrow the book, read or write notes, "
                "then return it when you leave (`with` closes it automatically). "
                "Without `with`, it's like forgetting to return the book — "
                "the file stays locked until your program ends."
            ),
            "R": (
                "**Always specify `encoding='utf-8'`.** "
                "Without it, Windows defaults to `cp1252` and macOS/Linux use `utf-8` — "
                "code that works on your Mac can crash on a classmate's Windows PC "
                "with a cryptic `UnicodeDecodeError`. UTF-8 is the universal standard."
            ),
            "N": (
                "🚫 **Common mistake:** opening files without specifying encoding.\n\n"
                "```python\nwith open('notes.txt') as f:          # risky — OS-dependent encoding\n    data = f.read()\n\n"
                "with open('notes.txt', encoding='utf-8') as f:  # ✓ safe everywhere\n    data = f.read()\n```\n\n"
                "pylint flags the first version as `W1514 — unspecified-encoding`."
            ),
        },
        "challenge_intro": "This file-reading function is missing the encoding specification — a common portability bug. Fix it, and notice how the safe version handles missing files.",
        "challenge_code": "def read_file(filename):\n    \"\"\"Read a text file and return its contents.\"\"\"\n    try:\n        with open(filename, \"r\", encoding=\"utf-8\") as f:\n            return f.read()\n    except FileNotFoundError:\n        return f\"(file '{filename}' not found)\"\n\ndef write_file(filename, content):\n    \"\"\"Write content to a text file.\"\"\"\n    with open(filename, \"w\", encoding=\"utf-8\") as f:\n        f.write(content)\n    return f\"Saved to {filename}\"\n\n# Demo\nprint(read_file(\"missing.txt\"))\nprint(write_file(\"test_output.txt\", \"Hello from PyLearn!\\n\"))\nprint(read_file(\"test_output.txt\"))",
        "pylint_ids": ["W1514"],
    },

    # ── 11. Classes & OOP ────────────────────────────────────────────────────
    {
        "id": "M11",
        "title": "Classes & OOP",
        "icon": "🏛️",
        "tagline": "Building your own data types with behaviour",
        "learn": {
            "L": (
                "A **class** is a blueprint for creating *objects* — custom data types that bundle "
                "together *attributes* (data) and *methods* (behaviour). "
                "OOP (Object-Oriented Programming) is the style of organising code around these objects."
            ),
            "E": (
                "```python\n"
                "class Student:\n"
                "    def __init__(self, name, gpa):   # constructor\n"
                "        self.name = name             # attribute\n"
                "        self.gpa  = gpa\n\n"
                "    def greet(self):                 # method\n"
                "        return f'Hi, I am {self.name} with GPA {self.gpa}'\n\n"
                "    def is_honors(self):\n"
                "        return self.gpa >= 3.5\n\n"
                "# Create instances (objects)\n"
                "alice = Student('Alice', 3.8)\n"
                "print(alice.greet())       # Hi, I am Alice with GPA 3.8\n"
                "print(alice.is_honors())   # True\n\n"
                "# Inheritance\n"
                "class GradStudent(Student):\n"
                "    def __init__(self, name, gpa, thesis):\n"
                "        super().__init__(name, gpa)\n"
                "        self.thesis = thesis\n"
                "```"
            ),
            "A": (
                "A class is like an **architectural blueprint**: the blueprint describes a house "
                "(the class), but you can build many individual houses from it (the objects/instances). "
                "Each house has its own address and colour (`self.name`, `self.gpa`), "
                "but they all share the same floor plan (the methods defined in the class)."
            ),
            "R": (
                "**Every method in a class must have `self` as its first parameter.** "
                "`self` is the reference to *this specific object* — it's how the method "
                "knows which instance's data to read or change. "
                "Python passes it automatically; you never pass it when calling the method."
            ),
            "N": (
                "🚫 **Common mistake:** forgetting `self` in the method signature or `self.` when accessing attributes.\n\n"
                "```python\nclass Dog:\n    def __init__(self, name):\n        name = name       # ← stores in local variable, not self!\n\n"
                "class Dog:\n    def __init__(self, name):\n        self.name = name  # ✓ stored on the object\n\n"
                "    def speak(self):              # ← self required\n        return f'{self.name} says Woof!'\n```"
            ),
        },
        "challenge_intro": "This BankAccount class is missing a method. The withdraw method should also check that the balance never goes negative — complete it.",
        "challenge_code": "class BankAccount:\n    def __init__(self, owner, balance=0):\n        self.owner   = owner\n        self.balance = balance\n\n    def deposit(self, amount):\n        if amount > 0:\n            self.balance += amount\n            return f\"Deposited ${amount:.2f}. Balance: ${self.balance:.2f}\"\n        return \"Deposit amount must be positive.\"\n\n    def withdraw(self, amount):\n        if amount > self.balance:\n            return f\"Insufficient funds. Balance: ${self.balance:.2f}\"\n        if amount <= 0:\n            return \"Withdrawal must be positive.\"\n        self.balance -= amount\n        return f\"Withdrew ${amount:.2f}. Balance: ${self.balance:.2f}\"\n\n    def __str__(self):\n        return f\"Account({self.owner}, ${self.balance:.2f})\"\n\nacc = BankAccount(\"Alice\", 100)\nprint(acc.deposit(50))\nprint(acc.withdraw(30))\nprint(acc.withdraw(200))\nprint(acc)",
        "pylint_ids": [],
    },

    # ── 12. Modules & Imports ────────────────────────────────────────────────
    {
        "id": "M12",
        "title": "Modules & Imports",
        "icon": "📦",
        "tagline": "Using Python's standard library and your own files",
        "learn": {
            "L": (
                "A **module** is a `.py` file containing reusable functions, classes, and constants. "
                "Python ships with hundreds of built-in modules — the 'standard library'. "
                "Use `import` to bring them into your code."
            ),
            "E": (
                "```python\n"
                "import math\n"
                "print(math.pi)          # 3.14159...\n"
                "print(math.sqrt(16))    # 4.0\n\n"
                "from math import pi, sqrt   # import specific names — no prefix needed\n"
                "print(sqrt(25))             # 5.0\n\n"
                "import random\n"
                "random.randint(1, 6)        # roll a die\n"
                "random.choice(['a','b','c'])# pick one randomly\n\n"
                "from datetime import datetime\n"
                "print(datetime.now().strftime('%Y-%m-%d'))\n\n"
                "# Useful standard modules\n"
                "# math, random, os, datetime, json, re, sys, collections\n"
                "```"
            ),
            "A": (
                "The standard library is like a **toolbox that came with your house**: "
                "hundreds of specialised tools (modules) already included. "
                "`import math` is like opening the maths drawer; "
                "`from math import sqrt` is like taking out just the calculator. "
                "You don't write `sqrt` from scratch — Python already built it."
            ),
            "R": (
                "**Only import what you use.** An import you never call is dead code — "
                "pylint flags it as `W0611 (unused-import)`. "
                "Keep imports at the top of the file and remove anything you don't need."
            ),
            "N": (
                "🚫 **Common mistake:** importing a module but never using it, "
                "or importing everything with `*`.\n\n"
                "```python\nimport os        # ← never used in this file\nfrom math import *  # ← pollutes namespace with 40+ names\n\n"
                "import math      # ✓ import only what you need\nprint(math.sqrt(9))\n```"
            ),
        },
        "challenge_intro": "This script uses several standard library modules. Try modifying it to use a module you haven't tried before — check what `datetime` or `collections` can do.",
        "challenge_code": "import math\nimport random\nimport os\nfrom datetime import datetime\n\n# math examples\nprint(f\"Pi:          {math.pi:.4f}\")\nprint(f\"sqrt(144):   {math.sqrt(144):.0f}\")\nprint(f\"log10(1000): {math.log10(1000):.0f}\")\n\n# random examples\nnumbers = list(range(1, 11))\nrandom.shuffle(numbers)\nprint(f\"Shuffled:    {numbers}\")\nprint(f\"Random pick: {random.choice(numbers)}\")\n\n# datetime\nnow = datetime.now()\nprint(f\"Today:       {now.strftime('%Y-%m-%d')}\")\n\n# os\nprint(f\"Working dir: {os.getcwd()}\")",
        "pylint_ids": ["W0611"],
    },

    # ── 13. Scope & Undefined Variables ──────────────────────────────────────
    {
        "id": "M13",
        "title": "Scope & Undefined Variables",
        "icon": "🔭",
        "tagline": "Where variables live and why order matters",
        "learn": {
            "L": (
                "**Scope** is the region of code where a variable exists and can be read. "
                "Python searches for a name in this order: "
                "**L**ocal → **E**nclosing → **G**lobal → **B**uilt-in (LEGB). "
                "A `NameError` means Python searched all four and found nothing."
            ),
            "E": (
                "```python\n"
                "x = 10          # GLOBAL — visible everywhere\n\n"
                "def show():\n"
                "    y = 20      # LOCAL — only inside show()\n"
                "    print(x)    # ✓ can see global x\n"
                "    print(y)    # ✓ can see local y\n\n"
                "show()\n"
                "print(y)        # NameError! y doesn't exist here\n\n"
                "# Using before defining\n"
                "print(count)    # NameError — not defined yet\n"
                "count = 0\n\n"
                "# Loop variable risk\n"
                "data = []\n"
                "last = None     # ✓ safe default\n"
                "for item in data:\n"
                "    last = item # never runs if data is empty\n"
                "print(last)     # None — safe\n"
                "```"
            ),
            "A": (
                "Scope is like **office floors in a building**: a local variable lives only on its own floor (function). "
                "From that floor, you can see the ground floor (globals) below, "
                "but someone on the ground floor can't see up to your private office. "
                "Python always starts looking on the current floor before checking downward."
            ),
            "R": (
                "**Variables must be assigned before they are used — Python reads top-to-bottom.** "
                "A variable created inside a function or loop only exists there. "
                "Referencing it outside causes a `NameError` — not a warning, a crash."
            ),
            "N": (
                "🚫 **Common mistake #1:** typo creates a new variable instead of using the intended one.\n\n"
                "```python\nstudent_score = 95\nprint(stuednt_score)  # NameError — typo, not the same name!\n```\n\n"
                "🚫 **Common mistake #2:** relying on a loop variable after an empty loop.\n\n"
                "```python\nfor item in []:    # body never runs\n    result = item\nprint(result)      # NameError!\n\n"
                "result = None      # ✓ initialise before loop\n```"
            ),
        },
        "challenge_intro": "This code has two scope-related issues — a variable used before it's defined, and a loop variable risk. Can you spot and fix both?",
        "challenge_code": "def calculate_average(numbers):\n    total = 0\n    last_value = None   # safe default before loop\n    for n in numbers:\n        total += n\n        last_value = n\n    if not numbers:\n        return 0, None\n    return total / len(numbers), last_value\n\nscores = [88, 72, 95, 61, 84]\navg, last = calculate_average(scores)\nprint(f\"Average:    {avg:.1f}\")\nprint(f\"Last score: {last}\")\n\n# Empty list — should not crash\navg2, last2 = calculate_average([])\nprint(f\"Empty avg:  {avg2}, last: {last2}\")",
        "pylint_ids": ["E0602", "W0631"],
    },

    # ── 14. Syntax Rules ─────────────────────────────────────────────────────
    {
        "id": "M14",
        "title": "Python Syntax Rules",
        "icon": "📐",
        "tagline": "The grammar rules Python insists on",
        "learn": {
            "L": (
                "**Syntax** is the grammar of Python — the exact rules it needs to read your code. "
                "A `SyntaxError` means Python couldn't parse what you wrote. "
                "**Nothing in your file runs** until every syntax error is fixed."
            ),
            "E": (
                "```python\n"
                "# Rule 1: colon after every block header\n"
                "if x > 0:          # ← required\n"
                "    print(x)\n\n"
                "# Rule 2: consistent indentation (4 spaces standard)\n"
                "def greet():\n"
                "    print('Hello') # inside function\n"
                "print('Done')      # outside function\n\n"
                "# Rule 3: match all brackets and quotes\n"
                "data = [1, 2, 3]   # ✓\n"
                "# data = [1, 2, 3  # SyntaxError: unclosed '['\n\n"
                "# Rule 4: don't use keywords as variable names\n"
                "# for = 5          # SyntaxError\n"
                "# list = [1,2,3]   # shadows built-in — avoid\n"
                "count = 5          # ✓ use a descriptive name\n"
                "```"
            ),
            "A": (
                "Syntax is like **punctuation in English**: a missing comma changes meaning; "
                "a missing period confuses the reader. In Python, a missing colon after `if x > 0` "
                "confuses Python the same way. Unlike English, Python is exact — "
                "one missing character stops the entire program from running."
            ),
            "R": (
                "**Every block header (`if`, `for`, `while`, `def`, `class`) must end with `:`** "
                "and the body below it must be indented consistently (4 spaces is the standard). "
                "Indentation *is* the structure in Python — there are no curly braces `{}`."
            ),
            "N": (
                "🚫 **Common trick:** Python flags the *line after* the real error — "
                "because it only notices something is wrong when it hits unexpected text.\n\n"
                "```python\ndef greet()       # ← real error here (missing colon)\n"
                "    print('hi')   # ← Python reports an error on THIS line\n\n"
                "def greet():      # ✓\n    print('hi')\n```\n\n"
                "Always check the flagged line **and the one above it**."
            ),
        },
        "challenge_intro": "This code has two syntax errors preventing it from running at all. Find both before you click Analyse — then fix them.",
        "challenge_code": "def describe_score(score):\n    if score >= 90:\n        grade = \"A\"\n    elif score >= 80:\n        grade = \"B\"\n    else:\n        grade = \"C or below\"\n    return grade\n\nsubjects = [\"Math\", \"Science\", \"English\"]\nfor subject in subjects:\n    s = 85\n    result = describe_score(s)\n    print(f\"{subject}: {result}\")",
        "pylint_ids": ["E0001"],
    },

    # ── 15. Function Calls & Arguments ───────────────────────────────────────
    {
        "id": "M15",
        "title": "Function Calls & Arguments",
        "icon": "📞",
        "tagline": "Calling functions with the right inputs",
        "learn": {
            "L": (
                "When you **call** a function, you pass *arguments* that match its *parameters*. "
                "Arguments can be *positional* (matched by order) or *keyword* (matched by name). "
                "Missing a required argument raises a `TypeError`."
            ),
            "E": (
                "```python\n"
                "def introduce(name, course, year=1):\n"
                "    print(f'{name} studies {course}, year {year}')\n\n"
                "introduce('Alice', 'CS', 2)              # positional\n"
                "introduce(name='Alice', course='CS')     # keyword (year → default 1)\n"
                "introduce('Alice', year=3, course='CS')  # mix — keyword can be any order\n\n"
                "# Too few arguments\n"
                "def add(a, b):\n"
                "    return a + b\n\n"
                "add(1)   # TypeError: add() missing 1 required argument: 'b'\n\n"
                "# *args — any number of positional args\n"
                "def total(*numbers):\n"
                "    return sum(numbers)\n\n"
                "print(total(1, 2, 3, 4, 5))  # 15\n"
                "```"
            ),
            "A": (
                "Calling a function is like **ordering at a restaurant**: "
                "the menu (function signature) lists what you must order (required parameters) "
                "and what's optional with a default (optional parameters). "
                "You can't skip required items — the kitchen (Python) won't know what to make. "
                "Keyword arguments are like saying 'no onions please' — "
                "you name exactly what you're specifying."
            ),
            "R": (
                "**Required parameters (no default value) must always be provided.** "
                "Optional parameters (with `=default`) can be skipped — Python uses the default. "
                "You can never pass *fewer* arguments than required parameters."
            ),
            "N": (
                "🚫 **Common mistake:** changing a function's parameters without updating every call.\n\n"
                "```python\n# You added a required parameter:\ndef greet(name, language):   # was greet(name)\n    ...\n\n"
                "greet('Alice')  # TypeError: missing 1 required argument: 'language'\n\n"
                "# Fix: either add a default or update the call\ndef greet(name, language='English'):  # ✓ default keeps old calls working\n    ...\n```"
            ),
        },
        "challenge_intro": "This set of function calls has one that passes the wrong number of arguments. Which call will crash, and why?",
        "challenge_code": "def calculate_grade(score, total, weight=1.0):\n    \"\"\"Return weighted percentage score.\"\"\"\n    percentage = (score / total) * 100 * weight\n    return round(percentage, 1)\n\n# These should all work\nprint(calculate_grade(45, 50))              # default weight\nprint(calculate_grade(45, 50, 0.3))         # with weight\nprint(calculate_grade(score=90, total=100)) # keyword args\n\n# Bonus: *args example\ndef average(*scores):\n    \"\"\"Return the average of any number of scores.\"\"\"\n    if not scores:\n        return 0\n    return sum(scores) / len(scores)\n\nprint(f\"Average: {average(88, 72, 95, 61, 84):.1f}\")",
        "pylint_ids": ["E1120"],
    },
]

MODULE_MAP = {m["id"]: m for m in MODULES}

# ─────────────────────────────────────────────────────────────────────────────
#  Beginner-friendly names for pylint codes  (hides technical IDs from UI)
# ─────────────────────────────────────────────────────────────────────────────
FRIENDLY_NAMES = {
    "E0001": "Syntax Error",
    "E0101": "Return Outside Function",
    "E0102": "Duplicate Definition",
    "E0103": "Break/Continue Outside Loop",
    "E0104": "Return Outside Function",
    "E0105": "Yield Outside Function",
    "E0107": "Nonexistent Operator",
    "E0108": "Duplicate Argument",
    "E0110": "Abstract Class Instantiated",
    "E0112": "More Than One Star Expression",
    "E0601": "Variable Used Before Assignment",
    "E0602": "Undefined Variable",
    "E0603": "Undefined Name in __all__",
    "E0611": "Name Not Found in Module",
    "E1101": "Module Has No Such Member",
    "E1120": "Missing Required Argument",
    "E1121": "Too Many Arguments",
    "E1123": "Unexpected Keyword Argument",
    "E1124": "Argument Passed Twice",
    "E1125": "Missing Keyword Argument",
    "W0104": "Pointless Statement",
    "W0105": "Pointless String",
    "W0107": "Unnecessary Pass",
    "W0108": "Unnecessary Lambda",
    "W0120": "Else Without Break",
    "W0122": "Use of exec()",
    "W0123": "Use of eval()",
    "W0125": "Constant Condition in If",
    "W0401": "Wildcard Import",
    "W0611": "Unused Import",
    "W0612": "Unused Variable",
    "W0631": "Variable Used Before Loop Assignment",
    "W1514": "Missing Encoding in open()",
}

def friendly(mid):
    """Return a plain-English label for a pylint message-id."""
    return FRIENDLY_NAMES.get(mid, "Code Issue")

# ─────────────────────────────────────────────────────────────────────────────
#  C.O.D.E. explanations — per pylint message-id (rule-based fallback)
# ─────────────────────────────────────────────────────────────────────────────
CODE_EXPLANATIONS = {
    "E0001": (
        "**C — Cause**\n"
        "Python hit something it couldn't read — usually a missing colon, "
        "mismatched parenthesis, or wrong indentation.\n\n"
        "**O — Output**\n"
        "`SyntaxError: invalid syntax` — Python refuses to run *any* of your "
        "code until this is fixed.\n\n"
        "**D — Demo**\n"
        "```python\ndef greet()       # ← missing colon after the parenthesis\n"
        "    print('hi')   # Python never even gets here\n```\n\n"
        "**E — Edit**\n"
        "```python\ndef greet():      # ← add the colon ✓\n    print('hi')\n```\n"
        "*Tip: check the flagged line and the one just above it.*"
    ),
    "E0602": (
        "**C — Cause**\n"
        "You used a variable that Python has never seen before — it has no value yet.\n\n"
        "**O — Output**\n"
        "`NameError: name 'message' is not defined` — Python stops immediately.\n\n"
        "**D — Demo**\n"
        "```python\nprint(message)   # ← Python has no idea what 'message' is\n```\n\n"
        "**E — Edit**\n"
        "```python\nmessage = 'Hello!'   # ← define it first\nprint(message)       # now Python knows ✓\n```"
    ),
    "W0631": (
        "**C — Cause**\n"
        "A variable created inside a loop might never exist if the loop body never runs.\n\n"
        "**O — Output**\n"
        "`NameError: name 'i' is not defined` — happens when the list or range is empty.\n\n"
        "**D — Demo**\n"
        "```python\nfor i in range(0):   # empty range — loop body never runs\n    pass\nprint(i)             # ← i was never created!\n```\n\n"
        "**E — Edit**\n"
        "```python\ni = None             # ← safe default before the loop\nfor i in range(0):\n    pass\nprint(i)             # prints None safely ✓\n```"
    ),
    "W0104": (
        "**C — Cause**\n"
        "You calculated something but never saved or returned the result — Python discarded it.\n\n"
        "**O — Output**\n"
        "No crash, but the function returns `None` instead of the value you expected.\n\n"
        "**D — Demo**\n"
        "```python\ndef square(n):\n    n * n            # ← result computed then thrown away\n\nprint(square(5))   # prints: None\n```\n\n"
        "**E — Edit**\n"
        "```python\ndef square(n):\n    return n * n   # ← send the result back ✓\n\nprint(square(5))   # prints: 25\n```"
    ),
    "W1514": (
        "**C — Cause**\n"
        "You opened a file without specifying which character encoding to use.\n\n"
        "**O — Output**\n"
        "Works on your machine but may crash with `UnicodeDecodeError` on a different OS.\n\n"
        "**D — Demo**\n"
        "```python\nwith open('notes.txt') as f:   # encoding depends on the OS\n    data = f.read()              # risky on Windows / Linux\n```\n\n"
        "**E — Edit**\n"
        "```python\nwith open('notes.txt', encoding='utf-8') as f:   # ← always specify ✓\n    data = f.read()\n```"
    ),
    "W0125": (
        "**C — Cause**\n"
        "Your `if` condition is always True or always False — one branch can never execute.\n\n"
        "**O — Output**\n"
        "No crash, but part of your code is unreachable — a sign of a logic mistake.\n\n"
        "**D — Demo**\n"
        "```python\nif True:                 # always True — else is dead code\n    print('runs')\nelse:\n    print('never runs')  # ← unreachable!\n```\n\n"
        "**E — Edit**\n"
        "```python\ndebug = False            # use a real variable\nif debug:\n    print('debug mode')\nelse:\n    print('normal mode') # both branches reachable ✓\n```"
    ),
    "E1120": (
        "**C — Cause**\n"
        "You called a function but didn't provide all the values it requires.\n\n"
        "**O — Output**\n"
        "`TypeError: greet() missing 1 required positional argument: 'age'`\n\n"
        "**D — Demo**\n"
        "```python\ndef greet(name, age):\n    print(f'{name} is {age}')\n\ngreet('Alice')   # ← missing second argument!\n```\n\n"
        "**E — Edit**\n"
        "```python\ngreet('Alice', 20)   # ← pass ALL required arguments ✓\n```"
    ),
    "W0611": (
        "**C — Cause**\n"
        "You imported a module or name that you never actually used in the code.\n\n"
        "**O — Output**\n"
        "No crash — it's a warning. But it wastes memory and confuses readers.\n\n"
        "**D — Demo**\n"
        "```python\nimport os       # ← imported but never used\nimport math\nprint(math.pi)  # only math is used\n```\n\n"
        "**E — Edit**\n"
        "```python\nimport math     # ← remove unused imports ✓\nprint(math.pi)\n```"
    ),
    "W0612": (
        "**C — Cause**\n"
        "You assigned a value to a variable but never used that variable afterward.\n\n"
        "**O — Output**\n"
        "No crash — but the assignment is wasted work and may hide a bug.\n\n"
        "**D — Demo**\n"
        "```python\nresult = some_function()   # ← result assigned...\nprint('Done')              # ← ...but result never used!\n```\n\n"
        "**E — Edit**\n"
        "Either use `result`, or if intentionally ignoring the return value: `_ = some_function()`"
    ),
}

# Per-module generic C.O.D.E. feedback when pylint finds nothing wrong
MODULE_CLEAN_FEEDBACK = {
    "M01": (
        "**C — Cause**\nYou correctly assigned variables using appropriate data types. "
        "Python read every name and value without confusion.\n\n"
        "**O — Output**\nPython runs your code exactly as intended — each variable holds the right type "
        "and `type()` reports correctly.\n\n"
        "**D — Demo**\nYour own code is the demo here — each `=` assignment you wrote is correct syntax.\n\n"
        "**E — Edit**\nChallenge: try `type(42 + 3.0)` and `type(True + 1)` — what types does Python produce? 🎉"
    ),
    "M02": (
        "**C — Cause**\nYou used string operations and methods correctly. Python could read and process every string.\n\n"
        "**O — Output**\nAll string operations produced the expected text — no `AttributeError` or `TypeError`.\n\n"
        "**D — Demo**\nYour f-string formatting is a great example of clean, readable Python.\n\n"
        "**E — Edit**\nTry adding `.title()`, `.zfill(5)`, or `\":\".join([...])` to explore more string power. 🎉"
    ),
    "M03": (
        "**C — Cause**\nYour conditional logic uses real boolean expressions — no constant conditions.\n\n"
        "**O — Output**\nPython evaluates each branch correctly; no branch is dead code.\n\n"
        "**D — Demo**\nYour `elif` chain is a clean example of a complete decision tree.\n\n"
        "**E — Edit**\nTry adding a `not` operator or a compound `and`/`or` condition to deepen your understanding. 🎉"
    ),
    "M04": (
        "**C — Cause**\nYour `for` loop correctly iterates over the sequence and accumulates results.\n\n"
        "**O — Output**\nPython processes every item and the final result is correct.\n\n"
        "**D — Demo**\nYour use of `enumerate()` or `range()` shows good loop technique.\n\n"
        "**E — Edit**\nChallenge: rewrite your loop as a list comprehension — can you make it one line? 🎉"
    ),
    "M05": (
        "**C — Cause**\nYour `while` loop has a correct terminating condition — it won't run forever.\n\n"
        "**O — Output**\nThe loop runs the expected number of times and exits cleanly.\n\n"
        "**D — Demo**\nYour loop body correctly changes the condition variable on every iteration.\n\n"
        "**E — Edit**\nTry adding a `break` inside a `while True:` loop — a common real-world pattern. 🎉"
    ),
    "M06": (
        "**C — Cause**\nYour function correctly uses `return` to send a value back to the caller.\n\n"
        "**O — Output**\nThe caller receives the computed result instead of `None`.\n\n"
        "**D — Demo**\nYour `return` statement is exactly where it needs to be — after the calculation.\n\n"
        "**E — Edit**\nAdd a docstring and a default parameter to make your function more robust. 🎉"
    ),
    "M07": (
        "**C — Cause**\nYour list operations use correct syntax and the right methods for each task.\n\n"
        "**O — Output**\nPython modifies and queries the list as expected — no `IndexError` or `AttributeError`.\n\n"
        "**D — Demo**\nYour list comprehension (if you wrote one) is a great Pythonic idiom.\n\n"
        "**E — Edit**\nTry `zip()` to pair two lists together, or `filter()` with a lambda. 🎉"
    ),
    "M08": (
        "**C — Cause**\nYour dictionary uses `.get()` for safe key access and `.items()` to iterate.\n\n"
        "**O — Output**\nNo `KeyError` — the dictionary responds correctly to every operation.\n\n"
        "**D — Demo**\nUsing `.get(key, default)` is a best practice — it never crashes on a missing key.\n\n"
        "**E — Edit**\nTry a dictionary comprehension: `{k: v*2 for k, v in d.items()}` 🎉"
    ),
    "M09": (
        "**C — Cause**\nYour `try/except` block catches specific exceptions — exactly the right approach.\n\n"
        "**O — Output**\nInstead of crashing, the program returns a helpful error message.\n\n"
        "**D — Demo**\nCatching `ZeroDivisionError` and `TypeError` separately makes error messages precise.\n\n"
        "**E — Edit**\nAdd a `finally` block that always prints 'Operation complete.' regardless of outcome. 🎉"
    ),
    "M10": (
        "**C — Cause**\nYou correctly specified `encoding='utf-8'` — your file code works on any OS.\n\n"
        "**O — Output**\nThe file is read and written safely, with no encoding surprises.\n\n"
        "**D — Demo**\nThe `with open(...) as f:` pattern is best practice — it closes the file automatically.\n\n"
        "**E — Edit**\nTry reading a CSV file line-by-line with `f.readlines()` and splitting on commas. 🎉"
    ),
    "M11": (
        "**C — Cause**\nYour class correctly uses `__init__`, `self`, and method definitions.\n\n"
        "**O — Output**\nObjects are created and methods behave as expected.\n\n"
        "**D — Demo**\nYour `__str__` method makes the object print nicely — a key OOP best practice.\n\n"
        "**E — Edit**\nAdd a `@property` decorator or create a subclass that inherits from your class. 🎉"
    ),
    "M12": (
        "**C — Cause**\nYour imports are all used — no dead import weight in your code.\n\n"
        "**O — Output**\nAll imported names resolve correctly and the module functions work as expected.\n\n"
        "**D — Demo**\nUsing `from datetime import datetime` (importing just what you need) is clean style.\n\n"
        "**E — Edit**\nExplore `collections.Counter` — count item frequencies in one line. 🎉"
    ),
    "M13": (
        "**C — Cause**\nAll variables are defined before use, and loop variables have safe defaults.\n\n"
        "**O — Output**\nNo `NameError` — Python finds every variable when it needs it.\n\n"
        "**D — Demo**\nInitialising `last_value = None` before the loop is the correct defensive pattern.\n\n"
        "**E — Edit**\nTry intentionally triggering a `NameError` to see what the message looks like. 🎉"
    ),
    "M14": (
        "**C — Cause**\nYour syntax is perfect — colons, indentation, brackets, and quotes all match.\n\n"
        "**O — Output**\nPython parsed and ran your entire file without a `SyntaxError`.\n\n"
        "**D — Demo**\nYour consistent 4-space indentation is exactly the Python style standard (PEP 8).\n\n"
        "**E — Edit**\nTry deliberately removing a colon and see where Python flags the error vs. where the real mistake is. 🎉"
    ),
    "M15": (
        "**C — Cause**\nAll function calls supply the correct number and type of arguments.\n\n"
        "**O — Output**\nNo `TypeError: missing argument` — every call matches its function's signature.\n\n"
        "**D — Demo**\nUsing keyword arguments like `calculate_grade(score=90, total=100)` makes calls self-documenting.\n\n"
        "**E — Edit**\nDefine a function with `*args` and `**kwargs` — call it with 10 different arguments. 🎉"
    ),
}

# ─────────────────────────────────────────────────────────────────────────────
#  Data helpers
# ─────────────────────────────────────────────────────────────────────────────
def load_users():
    if DATA_FILE.exists():
        try: return json.loads(DATA_FILE.read_text())
        except: return {}
    return {}

def save_users(u):
    DATA_FILE.write_text(json.dumps(u, indent=2))

def hash_pw(pw):
    return hashlib.sha256(pw.encode()).hexdigest()

def load_progress():
    if PROGRESS_FILE.exists():
        try: return json.loads(PROGRESS_FILE.read_text())
        except: return {}
    return {}

def save_progress(p):
    PROGRESS_FILE.write_text(json.dumps(p, indent=2))

def get_user_progress(username):
    return load_progress().get(username, {})

def mark_module(username, module_id, understood):
    p = load_progress()
    if username not in p:
        p[username] = {}
    p[username][module_id] = {
        "understood": understood,
        "completed_at": datetime.datetime.now().isoformat(timespec="seconds"),
    }
    save_progress(p)

# ─────────────────────────────────────────────────────────────────────────────
#  pylint analysis — broad checks for general code quality
# ─────────────────────────────────────────────────────────────────────────────
PYLINT_ENABLES = (
    "E0001,E0101,E0102,E0103,E0104,E0105,E0107,E0108,E0110,"
    "E0112,E0601,E0602,E0603,E0611,E0632,E0633,"
    "W0104,W0105,W0107,W0108,W0120,W0122,W0123,W0125,"
    "W0401,W0611,W0612,W0631,W1514,"
    "E1101,E1120,E1121,E1123,E1124,E1125"
)

def analyze_code(code):
    with tempfile.NamedTemporaryFile(
            suffix=".py", mode="w", delete=False, encoding="utf-8") as f:
        f.write(code)
        tmp = f.name
    try:
        result = subprocess.run(
            ["pylint", "--output-format=json", "--disable=all",
             f"--enable={PYLINT_ENABLES}", tmp],
            capture_output=True, text=True, timeout=20,
        )
        raw = result.stdout.strip()
        return json.loads(raw) if raw else []
    except (json.JSONDecodeError, subprocess.TimeoutExpired):
        return []
    except FileNotFoundError:
        st.error("pylint not found — install it: `pip3 install pylint`")
        return []
    finally:
        os.unlink(tmp)

# ─────────────────────────────────────────────────────────────────────────────
#  LLM prompt — learning-focused, C.O.D.E. format
# ─────────────────────────────────────────────────────────────────────────────
def build_prompt(code, errors, profile, module_title):
    level      = profile.get("level", "beginner")
    topics     = profile.get("topics", "basic Python")
    confidence = profile.get("confidence", 2)
    tone = {
        "complete beginner": "Use very simple language, avoid jargon, use analogies.",
        "some experience":   "Be clear and friendly. Basic Python terms are fine.",
        "intermediate":      "Be concise. Standard Python terminology is fine.",
    }.get(level, "Be clear and friendly.")
    if confidence <= 2:
        tone += " The student finds error messages confusing — explain gently."

    error_text = "\n".join(
        f"  Line {e['line']}: [{e.get('message-id','')}] {e['message']}"
        for e in errors
    ) or "  None — the code looks clean!"

    return f"""You are a Python tutor teaching a {level} programmer about: {module_title}.
The student already knows: {topics}.
{tone}

Their code attempt:
```python
{code.strip()}
```

Analysis results:
{error_text}

Respond using the C.O.D.E. learning framework for EACH issue found:

**C — Cause**
What concept or mistake triggered this? (one simple sentence)

**O — Output**
What does Python actually produce — the exact error or wrong result?

**D — Demo**
A tiny broken snippet (2–4 lines) showing exactly where it goes wrong.

**E — Edit**
The corrected version with a note on what changed and WHY it works now.

If no issues found: C = what they understood correctly about {module_title},
O = what Python does with their clean code, D = highlight a line from their code
that shows good thinking, E = one concept to explore next in this topic area.
Be encouraging — learning takes practice. Never say "fix" when there is nothing broken.
"""

# ─────────────────────────────────────────────────────────────────────────────
#  LLM call — tries Groq (online, free) first, then Ollama (local), then None
#  NOTE: errors from Groq are now surfaced via st.error() instead of being
#  silently swallowed, so you can see exactly why a call failed.
# ─────────────────────────────────────────────────────────────────────────────
def get_llm_feedback(prompt):
    # 1. Groq cloud API (free — get key at console.groq.com)
    groq_key = st.session_state.get("groq_api_key", "").strip()
    if groq_key:
        try:
            resp = requests.post(
                GROQ_URL,
                headers={"Authorization": f"Bearer {groq_key}",
                         "Content-Type": "application/json"},
                json={
                    "model": GROQ_MODEL,
                    "messages": [{"role": "user", "content": prompt}],
                    "temperature": 0.4,
                    "max_tokens": 800,
                },
                timeout=30,
            )
            if resp.ok:
                content = resp.json()["choices"][0]["message"]["content"].strip()
                if content:
                    st.session_state["llm_source"] = "groq"
                    return content
            else:
                # Surface the real HTTP error instead of failing silently
                st.error(f"Groq API error {resp.status_code}: {resp.text}")
        except Exception as e:
            # Surface network/timeout/parsing errors instead of failing silently
            st.error(f"Groq request failed: {e}")

    # 2. Local Ollama fallback
    try:
        resp = requests.post(
            OLLAMA_URL,
            json={"model": MODEL_NAME, "prompt": prompt, "stream": False},
            timeout=90,
        )
        if resp.ok:
            content = resp.json().get("response", "").strip()
            if content:
                st.session_state["llm_source"] = "ollama"
                return content
    except Exception:
        pass

    st.session_state["llm_source"] = None
    return None

# ─────────────────────────────────────────────────────────────────────────────
#  Rule-based C.O.D.E. feedback (no Ollama)
# ─────────────────────────────────────────────────────────────────────────────
def code_feedback(errors, profile, module_id=""):
    if not errors:
        clean = MODULE_CLEAN_FEEDBACK.get(module_id, (
            "✅ **Your code is clean.**\n\n"
            "**C — Cause**\nYou applied the concept correctly.\n\n"
            "**O — Output**\nPython runs your code exactly as intended.\n\n"
            "**D — Demo**\nYour submitted code is already a good example.\n\n"
            "**E — Edit**\nChallenge yourself: extend this code with a new idea. 🎉"
        ))
        return "✅ **Excellent! Your code is clean.**\n\n---\n" + clean

    level = profile.get("level", "beginner")
    out   = [f"**C.O.D.E. Learning Feedback** — for a *{level}* programmer:\n"]
    seen  = set()
    for e in errors[:5]:
        mid  = e.get("message-id", "")
        line = e.get("line", "?")
        msg  = e.get("message", "")
        out.append(f"---\n### 📍 Line {line} — {friendly(mid)}\n")
        if mid in CODE_EXPLANATIONS and mid not in seen:
            out.append(CODE_EXPLANATIONS[mid])
            seen.add(mid)
        else:
            out.append(
                "**C — Cause**\nPylint flagged something unexpected here.\n\n"
                "**O — Output**\nThis may cause a crash or unexpected behaviour at runtime.\n\n"
                "**D — Demo**\nLook at the pylint message above — it points to the exact line.\n\n"
                "**E — Edit**\nReview that line for a typo, wrong indentation, or logic mistake."
            )
    return "\n\n".join(out)

# ─────────────────────────────────────────────────────────────────────────────
#  Page setup
# ─────────────────────────────────────────────────────────────────────────────
st.set_page_config(page_title="PyLearn", page_icon="🐍", layout="wide")
st.markdown("""
<style>
[data-testid="stSidebar"] { background: #0f172a; }
[data-testid="stSidebar"] * { color: #e2e8f0 !important; }
.module-card {
    background: #f8fafc; border: 1px solid #e2e8f0;
    border-radius: 12px; padding: 18px 20px; margin-bottom: 12px;
}
.stButton>button { border-radius: 8px; font-weight: 600; }
</style>
""", unsafe_allow_html=True)

# Session defaults
for k, v in [
    ("logged_in",  False), ("username",  ""),
    ("page",       "login"), ("profile",  {}),
    ("current_module", None), ("ollama_ok", None),
]:
    if k not in st.session_state:
        st.session_state[k] = v

# ─────────────────────────────────────────────────────────────────────────────
#  SIDEBAR
# ─────────────────────────────────────────────────────────────────────────────
if st.session_state.logged_in:
    progress = get_user_progress(st.session_state.username)
    done     = len(progress)
    with st.sidebar:
        st.markdown(f"## 👤 {st.session_state.username}")
        st.progress(done / TOTAL_MODULES,
                    text=f"{done}/{TOTAL_MODULES} modules completed")
        p = st.session_state.profile
        if p:
            st.caption(f"🎓 {p.get('level','').title()}")
        st.divider()
        if st.button("🏠 Learning Dashboard", use_container_width=True):
            st.session_state.page = "dashboard"; st.rerun()
        if st.button("✏️ Free Practice",       use_container_width=True):
            st.session_state.page = "practice"; st.rerun()
        if st.button("📊 My Progress",         use_container_width=True):
            st.session_state.page = "progress_page"; st.rerun()
        if st.button("ℹ️ About PyLearn",       use_container_width=True):
            st.session_state.page = "about"; st.rerun()
        if st.button("🚪 Logout",              use_container_width=True):
            for k in ["logged_in","username","profile","current_module","ollama_ok"]:
                if k == "logged_in": st.session_state[k] = False
                elif k in ["current_module","ollama_ok"]: st.session_state[k] = None
                elif k == "username": st.session_state[k] = ""
                else: st.session_state[k] = {}
            st.session_state.page = "login"; st.rerun()
        st.divider()
        # ── AI backend selector ──────────────────────────────────────────
        with st.expander("🤖 AI Settings", expanded=False):
            st.markdown("**Groq (free, online)**")
            groq_key_input = st.text_input(
                "Groq API Key",
                value=st.session_state.get("groq_api_key", ""),
                type="password",
                placeholder="gsk_...",
                help="Free at console.groq.com → API Keys",
                key="groq_key_widget",
            )
            if groq_key_input != st.session_state.get("groq_api_key", ""):
                st.session_state["groq_api_key"] = groq_key_input
                st.session_state["llm_source"]   = None
                st.rerun()
            st.caption("Or run Ollama locally: `ollama run phi3:mini`")

        # Status badge
        src = st.session_state.get("llm_source")
        if src == "groq":
            st.success("🟢 Groq AI connected")
        elif src == "ollama":
            st.success("🟢 Ollama connected")
        elif st.session_state.get("groq_api_key"):
            st.info("🔑 Groq key saved — AI ready")
        else:
            st.warning("🔴 No AI — using built-in C.O.D.E.")

# ═════════════════════════════════════════════════════════════════════════════
#  LOGIN / REGISTER
# ═════════════════════════════════════════════════════════════════════════════
if not st.session_state.logged_in:
    st.markdown("## 🐍 PyLearn")
    st.markdown(
        "**Learn Python by doing — 15 guided modules covering the full language, "
        "real code analysis, and structured C.O.D.E. feedback.**"
    )
    st.markdown("---")
    t1, t2 = st.tabs(["🔑 Login", "✨ Create Account"])
    with t1:
        with st.form("lf"):
            u  = st.text_input("Username")
            pw = st.text_input("Password", type="password")
            if st.form_submit_button("Login →", use_container_width=True):
                users = load_users()
                if u in users and users[u]["password"] == hash_pw(pw):
                    st.session_state.logged_in = True
                    st.session_state.username  = u
                    st.session_state.profile   = users[u].get("profile", {})
                    st.session_state.page      = "dashboard"
                    st.rerun()
                else:
                    st.error("Incorrect username or password.")
    with t2:
        with st.form("rf"):
            nu = st.text_input("Choose a username")
            np = st.text_input("Password (min 6 chars)", type="password")
            if st.form_submit_button("Create Account →", use_container_width=True):
                users = load_users()
                if nu in users:        st.error("Username already taken.")
                elif len(nu) < 3:      st.error("Username must be at least 3 characters.")
                elif len(np) < 6:      st.error("Password must be at least 6 characters.")
                else:
                    users[nu] = {
                        "password": hash_pw(np), "profile": {},
                        "created": datetime.datetime.now().isoformat(),
                    }
                    save_users(users)
                    st.session_state.logged_in = True
                    st.session_state.username  = nu
                    st.session_state.profile   = {}
                    st.session_state.page      = "onboarding"
                    st.rerun()

# ═════════════════════════════════════════════════════════════════════════════
#  ONBOARDING
# ═════════════════════════════════════════════════════════════════════════════
elif st.session_state.page == "onboarding":
    st.markdown("## 👋 Welcome to PyLearn!")
    st.markdown(
        "Answer 3 quick questions so the system can personalise your "
        "learning experience across all 15 Python modules."
    )
    st.markdown("---")
    with st.form("of"):
        lr = st.radio(
            "**Q1 — Your Python experience:**",
            ["Complete beginner (< 1 month)",
             "Some experience (1–6 months)",
             "Intermediate (6 months+)"]
        )
        topics = st.multiselect(
            "**Q2 — Topics you've already covered:**",
            ["Variables & Data Types", "Strings", "Conditionals (if/else)",
             "for Loops", "while Loops", "Functions", "Lists",
             "Dictionaries", "Error Handling", "File I/O",
             "Classes & OOP", "Modules & Imports"],
            default=["Variables & Data Types"]
        )
        conf = st.slider(
            "**Q3 — How comfortable are you reading Python error messages?**",
            1, 5, 2, help="1 = very confused  ·  5 = totally comfortable"
        )
        if st.form_submit_button("Start Learning →", use_container_width=True):
            lmap = {
                "Complete beginner (< 1 month)": "complete beginner",
                "Some experience (1–6 months)":  "some experience",
                "Intermediate (6 months+)":       "intermediate",
            }
            profile = {
                "level":      lmap[lr],
                "topics":     ", ".join(topics) or "basic Python",
                "confidence": conf,
            }
            users = load_users()
            users[st.session_state.username]["profile"] = profile
            save_users(users)
            st.session_state.profile = profile
            st.session_state.page    = "dashboard"
            st.rerun()

# ═════════════════════════════════════════════════════════════════════════════
#  LEARNING DASHBOARD
# ═════════════════════════════════════════════════════════════════════════════
elif st.session_state.page == "dashboard":
    progress = get_user_progress(st.session_state.username)
    done     = len(progress)

    st.markdown("## 🐍 PyLearn — Learning Dashboard")
    st.markdown(
        "Work through all 15 modules to learn the full Python language. "
        "Each module has a concept lesson and a real coding challenge with C.O.D.E. feedback."
    )
    st.progress(done / TOTAL_MODULES,
                text=f"**{done} of {TOTAL_MODULES} modules completed**")
    st.markdown("---")

    # Group modules into sections for readability
    sections = [
        ("🌱 Foundations",        MODULES[0:5]),
        ("🔧 Core Building Blocks", MODULES[5:9]),
        ("📚 Advanced Topics",     MODULES[9:12]),
        ("🎯 Precision & Safety",  MODULES[12:15]),
    ]

    for section_title, section_modules in sections:
        st.markdown(f"### {section_title}")
        for mod in section_modules:
            completed  = mod["id"] in progress
            understood = progress.get(mod["id"], {}).get("understood", None)
            badge      = "✅" if (completed and understood) else (
                         "🔁" if (completed and not understood) else "⬜")
            col1, col2 = st.columns([5, 1])
            with col1:
                st.markdown(f"**{badge} {mod['icon']} {mod['title']}**")
                st.caption(mod["tagline"])
                if completed:
                    label = "Understood ✓" if understood else "Needs more practice"
                    ts    = progress[mod["id"]]["completed_at"][:10]
                    st.caption(f"Status: {label} · {ts}")
            with col2:
                btn_label = "Review" if completed else "Start"
                if st.button(btn_label, key=f"mod_{mod['id']}", use_container_width=True):
                    st.session_state.current_module = mod["id"]
                    st.session_state.page = "lesson"
                    st.rerun()
            st.markdown("---")

# ═════════════════════════════════════════════════════════════════════════════
#  LESSON PAGE
# ═════════════════════════════════════════════════════════════════════════════
elif st.session_state.page == "lesson":
    mod = MODULE_MAP.get(st.session_state.current_module)
    if not mod:
        st.session_state.page = "dashboard"; st.rerun()

    progress  = get_user_progress(st.session_state.username)
    completed = mod["id"] in progress

    if st.button("← Back to Dashboard"):
        st.session_state.page = "dashboard"; st.rerun()

    st.markdown(f"## {mod['icon']} {mod['title']}")
    st.markdown(f"*{mod['tagline']}*")
    st.markdown("---")

    tab_learn, tab_challenge = st.tabs(["📖 Learn the Concept", "💻 Try the Challenge"])

    with tab_learn:
        render_learn(mod["learn"])

        # ── Q&A box — ask if still confused ─────────────────────────────────
        st.markdown("---")
        st.markdown("### 🙋 Still have questions?")
        st.caption(
            "Type your question below — the system will explain it further "
            "using the same L.E.A.R.N. framework."
        )
        qa_key = f"qa_{mod['id']}"
        user_question = st.text_area(
            "Your question about this concept:",
            placeholder=f"e.g. 'I don't understand how {mod['title'].split()[0].lower()} works with loops' "
                        f"or 'What's the difference between X and Y?'",
            height=80,
            key=qa_key,
        )
        if st.button("💬 Get Clarification", key=f"qa_btn_{mod['id']}",
                     use_container_width=True):
            if user_question.strip():
                with st.spinner("Thinking through your question…"):
                    qa_prompt = (
                        f"A student is learning Python, specifically about: **{mod['title']}**.\n"
                        f"They have just read this explanation:\n"
                        f"L — Label:   {mod['learn'].get('L','')[:300]}\n"
                        f"R — Rule:    {mod['learn'].get('R','')[:300]}\n\n"
                        f"Their question is: \"{user_question.strip()}\"\n\n"
                        f"Answer their question clearly and concisely using the L.E.A.R.N. format:\n"
                        f"**L — Label**: Re-state or reframe the specific concept they asked about\n"
                        f"**E — Example**: A short code snippet that directly answers their question\n"
                        f"**A — Analogy**: A fresh analogy or different angle if the first one didn't click\n"
                        f"**R — Rule**: The key rule or insight that resolves their confusion\n"
                        f"**N — Note**: One thing to watch out for related to their question\n\n"
                        f"Keep each section to 2–4 sentences. Be warm and encouraging."
                    )
                    answer = get_llm_feedback(qa_prompt)
                if answer:
                    st.session_state.ollama_ok = True
                    st.markdown("---")
                    st.markdown("#### 💡 Clarification")
                    st.markdown(answer)
                else:
                    st.session_state.ollama_ok = False
                    st.markdown("---")
                    st.markdown("#### 💡 Clarification (Built-in)")
                    # Rule-based Q&A fallback — works without Ollama
                    q_lower = user_question.lower()
                    learn   = mod["learn"]
                    # Decide which sections are most relevant to the question
                    sections = []
                    if any(w in q_lower for w in ["example", "show", "how", "what does", "demo", "code"]):
                        sections.append(("💻 Example", learn.get("E", "")))
                    if any(w in q_lower for w in ["rule", "always", "never", "must", "should", "syntax"]):
                        sections.append(("📌 Rule", learn.get("R", "")))
                    if any(w in q_lower for w in ["why", "analogy", "like", "compare", "real"]):
                        sections.append(("🔗 Analogy", learn.get("A", "")))
                    if any(w in q_lower for w in ["mistake", "error", "wrong", "common", "avoid", "watch"]):
                        sections.append(("⚠️ Note", learn.get("N", "")))
                    # Default: show Example + Note (most useful for confusion)
                    if not sections:
                        sections = [
                            ("💻 Example", learn.get("E", "")),
                            ("⚠️ Note",    learn.get("N", "")),
                        ]
                    st.markdown(
                        f"*You asked: \"{user_question.strip()}\"*\n\n"
                        f"Here are the most relevant parts of the **{mod['title']}** lesson:"
                    )
                    for sec_title, sec_content in sections:
                        st.markdown(f"**{sec_title}**")
                        st.markdown(sec_content)
                        st.markdown("")
                    st.caption(
                        "🤖 For live AI answers: add a free Groq key in **AI Settings** "
                        "(sidebar), or run Ollama locally: `ollama run phi3:mini`"
                    )
            else:
                st.warning("Please type a question first.")

    with tab_challenge:
        st.markdown(f"**{mod['challenge_intro']}**")
        st.markdown("Edit the code, then click **Analyse** to get C.O.D.E. feedback:")

        code        = st.text_area(
            "Code:", value=mod["challenge_code"], height=200, key=f"code_{mod['id']}"
        )
        analyse_btn = st.button(
            "🔍 Analyse with C.O.D.E.", type="primary", use_container_width=True
        )

        if analyse_btn and code.strip():
            with st.spinner("Analysing…"):
                errors = analyze_code(code)

            st.markdown("---")
            if errors:
                st.warning(f"**{len(errors)} learning moment(s) found:**")
                for e in errors:
                    st.markdown(
                        f"- Line {e['line']} — **{friendly(e.get('message-id',''))}**"
                    )
            else:
                st.success("✅ Your code is clean!")

            st.markdown("---")
            st.markdown("### 🤖 C.O.D.E. Feedback")
            st.caption("**C**ause · **O**utput · **D**emo · **E**dit")

            with st.spinner("Generating learning feedback…"):
                prompt   = build_prompt(code, errors, st.session_state.profile, mod["title"])
                feedback = get_llm_feedback(prompt)

            if feedback is None:
                st.session_state.ollama_ok = False
                st.info(
                    "💡 *Using built-in C.O.D.E. explanations. "
                    "Add a free **Groq API key** in the sidebar AI Settings for live AI feedback "
                    "(no install needed), or run `ollama run phi3:mini` locally.*"
                )
                feedback = code_feedback(errors, st.session_state.profile, mod["id"])
            else:
                st.session_state.ollama_ok = True

            st.markdown(feedback)

            # ── Did you understand? ──────────────────────────────────────────
            st.markdown("---")
            st.markdown("**How did this go for you?**")
            c1, c2 = st.columns(2)
            with c1:
                if st.button("✅ I understood this!", use_container_width=True):
                    mark_module(st.session_state.username, mod["id"], True)
                    st.rerun()
            with c2:
                if st.button("🔁 I need more practice", use_container_width=True):
                    mark_module(st.session_state.username, mod["id"], False)
                    st.rerun()

        if completed:
            rec   = progress[mod["id"]]
            label = "✅ Understood" if rec["understood"] else "🔁 Needs more practice"
            st.info(f"You previously marked this: **{label}** on {rec['completed_at'][:10]}")

        # ── Next module navigation ───────────────────────────────────────────
        idx = next((i for i, m in enumerate(MODULES) if m["id"] == mod["id"]), None)
        if idx is not None and idx < len(MODULES) - 1:
            next_mod = MODULES[idx + 1]
            if st.button(
                f"Next: {next_mod['icon']} {next_mod['title']} →",
                use_container_width=True,
            ):
                st.session_state.current_module = next_mod["id"]
                st.session_state.page = "lesson"
                st.rerun()

# ═════════════════════════════════════════════════════════════════════════════
#  ABOUT / CONTRIBUTIONS
# ═════════════════════════════════════════════════════════════════════════════
elif st.session_state.page == "about":
    if st.button("← Back to Dashboard"):
        st.session_state.page = "dashboard"; st.rerun()

    st.markdown("## ℹ️ About PyLearn")
    st.markdown("---")

    # ── Project identity ────────────────────────────────────────────────────
    st.markdown("""
**PyLearn — LLM-Based Intelligent Code Review System for Beginner Python Learners**

*RCSA Graduate Research Project · University of Central Oklahoma*
*Researcher: Harshitha Bommi · hbommi@uco.edu*
    """)
    st.markdown("---")

    # ── Researcher's original contributions ─────────────────────────────────
    st.markdown("### 🎓 Researcher Contributions")
    st.markdown(
        "The following design decisions, frameworks, and system components were "
        "conceived and implemented by **Harshitha Bommi** as part of this graduate research project:"
    )

    contributions = [
        ("🔬 Research Concept & Problem Definition",
         "Identified the gap in existing code-review tools that provide error messages "
         "but no pedagogical explanation. Framed the research question: *Can an LLM-based system "
         "provide structured, beginner-friendly code feedback that improves learning outcomes?*"),

        ("📐 L.E.A.R.N. Framework (Original Design)",
         "Designed the **L.E.A.R.N.** instructional framework (Label · Example · Analogy · Rule · Note) "
         "to structure concept lessons. Each letter maps to a distinct pedagogical function: "
         "Label grounds the concept, Example demonstrates it in code, Analogy bridges to real-world intuition, "
         "Rule captures the core principle, and Note prevents the most common beginner error."),

        ("💡 C.O.D.E. Feedback Framework (Original Design)",
         "Designed the **C.O.D.E.** feedback acronym (Cause · Output · Demo · Edit) as the "
         "structured response format delivered to students after code analysis. "
         "This reframes error messages as learning moments rather than failures, "
         "and ensures every piece of feedback is actionable."),

        ("🗺️ Python Curriculum Architecture",
         "Designed the 15-module progressive Python curriculum, organising topics into four "
         "learning tiers: Foundations → Core Building Blocks → Advanced Topics → Precision & Safety. "
         "Each module includes a concept lesson, a targeted coding challenge, and adaptive feedback."),

        ("🤖 Adaptive Feedback System",
         "Designed the hybrid feedback pipeline: (1) pylint static analysis identifies code issues, "
         "(2) the LLM (Phi-3-mini via Ollama) generates personalised C.O.D.E. feedback based on the "
         "student's learner profile, and (3) a rule-based fallback ensures the system works "
         "even without a running LLM."),

        ("👤 Learner Profile & Personalisation",
         "Designed the onboarding questionnaire and learner profile system — capturing experience level, "
         "topics covered, and confidence with error messages — to personalise LLM prompt generation "
         "so that a beginner and an intermediate student receive appropriately calibrated feedback."),

        ("🙋 In-Lesson Q&A System",
         "Designed the contextual Q&A feature below each L.E.A.R.N. concept lesson, "
         "where students type free-form questions and receive elaborations in the same "
         "L.E.A.R.N. structured format, powered by the LLM with module context injected into the prompt."),

        ("📊 Progress & Self-Assessment Tracking",
         "Designed the 'I understood this / I need more practice' self-assessment model "
         "as an alternative to score-based evaluation, aligning with metacognitive learning theory. "
         "Progress is persisted per user and visualised on the dashboard and progress page."),
    ]

    for title, desc in contributions:
        with st.expander(title):
            st.markdown(desc)

    st.markdown("---")

    # ── Technology stack ────────────────────────────────────────────────────
    st.markdown("### 🛠️ Technology Stack")
    col1, col2 = st.columns(2)
    with col1:
        st.markdown("""
**Frontend / UI**
- Streamlit (Python web framework)

**Code Analysis**
- pylint (static analysis, JSON output mode)
- Python `subprocess` module

**AI / LLM**
- Phi-3-mini via Ollama (local LLM)
- Rule-based C.O.D.E. fallback (no internet required)
        """)
    with col2:
        st.markdown("""
**Data Storage**
- JSON flat-file storage (users & progress)
- Designed for MongoDB migration (see HOW_TO_RUN.txt)

**Language**
- Python 3.9+ compatible

**Research Framework**
- L.E.A.R.N. (concept instruction)
- C.O.D.E. (code feedback)
        """)

    st.markdown("---")
    st.caption(
        "PyLearn prototype · RCSA Graduate Project · UCO · 2024–2025 · "
        "Harshitha Bommi · hbommi@uco.edu"
    )

# ═════════════════════════════════════════════════════════════════════════════
#  FREE PRACTICE
# ═════════════════════════════════════════════════════════════════════════════
elif st.session_state.page == "practice":
    st.markdown("## ✏️ Free Practice")
    st.markdown(
        "Paste any Python code — get C.O.D.E. feedback without a guided lesson. "
        "Great for your own projects or homework."
    )
    st.markdown("---")

    code = st.text_area(
        "Your Python code:", height=280,
        placeholder="# Paste your Python code here…"
    )
    if st.button("🔍 Analyse", type="primary", use_container_width=True):
        if code.strip():
            with st.spinner("Analysing…"):
                errors = analyze_code(code)
            if errors:
                st.warning(f"**{len(errors)} learning moment(s) found:**")
                for e in errors:
                    st.markdown(
                        f"- Line {e['line']} — **{friendly(e.get('message-id',''))}**"
                    )
            else:
                st.success("✅ No issues found!")
            st.markdown("---")
            st.markdown("### 🤖 C.O.D.E. Feedback")
            st.caption("**C**ause · **O**utput · **D**emo · **E**dit")
            with st.spinner("Generating feedback…"):
                prompt   = build_prompt(code, errors, st.session_state.profile, "General Python")
                feedback = get_llm_feedback(prompt)
            if feedback is None:
                st.session_state.ollama_ok = False
                feedback = code_feedback(errors, st.session_state.profile)
            else:
                st.session_state.ollama_ok = True
            st.markdown(feedback)
        else:
            st.warning("Please enter some code first.")

# ═════════════════════════════════════════════════════════════════════════════
#  PROGRESS PAGE
# ═════════════════════════════════════════════════════════════════════════════
elif st.session_state.page == "progress_page":
    st.markdown("## 📊 My Learning Progress")
    progress = get_user_progress(st.session_state.username)
    profile  = st.session_state.profile

    done       = len(progress)
    understood = sum(1 for v in progress.values() if v.get("understood"))
    needs_more = done - understood

    c1, c2, c3, c4 = st.columns(4)
    c1.metric("Modules Completed",     f"{done}/{TOTAL_MODULES}")
    c2.metric("Understood ✅",          understood)
    c3.metric("Need More Practice 🔁", needs_more)
    c4.metric("Remaining ⬜",           TOTAL_MODULES - done)

    st.markdown("---")
    sections = [
        ("🌱 Foundations",         MODULES[0:5]),
        ("🔧 Core Building Blocks", MODULES[5:9]),
        ("📚 Advanced Topics",      MODULES[9:12]),
        ("🎯 Precision & Safety",   MODULES[12:15]),
    ]
    for section_title, section_mods in sections:
        st.markdown(f"### {section_title}")
        for mod in section_mods:
            rec = progress.get(mod["id"])
            if rec:
                label = "✅ Understood" if rec["understood"] else "🔁 Needs more practice"
                st.markdown(
                    f"**{mod['icon']} {mod['title']}** — {label} "
                    f"*(completed {rec['completed_at'][:10]})*"
                )
            else:
                st.markdown(f"**{mod['icon']} {mod['title']}** — ⬜ Not started yet")

    st.markdown("---")
    if profile:
        st.markdown(f"**Your level:** {profile.get('level','').title()}")
        st.markdown(f"**Topics covered:** {profile.get('topics','—')}")
        st.markdown(f"**Confidence with errors:** {profile.get('confidence','?')}/5")
    if st.button("✏️ Update my profile"):
        st.session_state.page = "onboarding"; st.rerun()
# ═════════════════════════════════════════════════════════════════════════════
#  ✨ NEW FEATURES — Ask PyLearn · Learn Any Topic · Ask-first Home page
# ═════════════════════════════════════════════════════════════════════════════
import re

# ─────────────────────────────────────────────────────────────────────────────
#  Knowledge base + retrieval — powers "Ask PyLearn"
#  A student asks a question → the app looks it up here FIRST (instant, vetted
#  answers drawn from all 15 lessons + common "X vs Y" questions).
#  Only if nothing matches well does it fall back to the LLM.
# ─────────────────────────────────────────────────────────────────────────────
STOPWORDS = set("""a an the is are was were be been am do does did to of in on at by
and or but it its this that these those i you we they my your our me can could should
would will how what whats why when where which who please explain tell about understand
help get got use using used like make want know mean means has have had not no yes also
just really very much some any there their them then than so as python
 don doesn didn isn aren wasn won couldn shouldn wouldn""".split())

COMPARE_WORDS = {"difference", "differences", "different", "differ", "differs",
                 "versus", "vs", "between", "compare", "comparison", "contrast"}

SYNONYMS = {
    "def": "function", "func": "function", "fn": "function",
    "dict": "dictionary", "oop": "class", "object": "class",
    "iterate": "loop", "iteration": "loop", "iterating": "loop",
    "exception": "error", "bug": "error", "crash": "error", "traceback": "error",
    "str": "string", "int": "integer", "bool": "boolean",
    "if": "conditional", "elif": "conditional", "else": "conditional",
    "var": "variable", "array": "list", "arr": "list", "kwarg": "arg",
}

def _norm(text):
    t = text.lower()
    t = re.sub(r"do[\s\-]*while", " dowhile ", t)
    t = re.sub(r"[!<>]=", " cmpop ", t)
    t = t.replace("==", " equalcompare ")
    t = t.replace("=", " assignop ")
    return t

def _stem(w):
    if w.endswith("sses"):
        return w[:-2]
    if len(w) > 4 and w.endswith("ies"):
        return w[:-3] + "y"
    if len(w) > 3 and w.endswith("s") and not w.endswith("ss"):
        return w[:-1]
    return w

def tokenize(text):
    out = []
    for w in re.findall(r"[a-z0-9_]+", _norm(text)):
        if w in STOPWORDS or w in COMPARE_WORDS or len(w) < 2:
            continue
        w = _stem(w)
        out.append(SYNONYMS.get(w, w))
    return out

# ── Hand-written answers to the questions beginners ask most ─────────────────
EXTRA_QA = [
    dict(id="while_vs_dowhile", topic="while vs do-while loops", module="M05", kind="compare",
         q="What is the difference between a while loop and a do-while loop?",
         kw="while do-while dowhile loop repeat condition",
         a="""**`while` vs `do-while`**

| | `while` | `do-while` |
|---|---|---|
| Checks the condition | **before** each run | **after** each run |
| Body runs at least once? | No — may run **zero** times | **Yes** — always at least once |
| Exists in Python? | ✅ Yes | ❌ No (it's in C, Java, JavaScript…) |

**Python has no do-while** — but you can copy it with `while True` + `break`:

```````python
while True:
    answer = input("Play again? (y/n) ")   # always runs once
    if answer == "n":
        break                              # the "after" check
```````

**Rule of thumb:** need the body to run at least once (menus, input checks)? Use the `while True` + `break` pattern. Otherwise use a normal `while`."""),

    dict(id="function_vs_class", topic="function vs class", module="M11", kind="compare",
         q="What is the difference between a function and a class?",
         kw="function class method object def self attribute oop",
         a="""**Function vs class**

- A **function** is a reusable block of code that does *one job*: inputs in, result out.
- A **class** is a blueprint that bundles **data** (attributes) and **functions** (methods) together into objects.

```````python
# Function — just does a job
def area(width, height):
    return width * height

# Class — holds data AND behaviour together
class Rectangle:
    def __init__(self, width, height):
        self.width = width
        self.height = height

    def area(self):
        return self.width * self.height

print(area(3, 4))               # 12
print(Rectangle(3, 4).area())   # 12
```````

**Rule of thumb:** one task → write a function. Something with its own data that does several related things (a student, a bank account) → write a class."""),

    dict(id="function_vs_loop", topic="function vs loop", module="M06", kind="compare",
         q="What is the difference between a function and a loop?",
         kw="function loop def for while repeat reuse",
         a="""**Function vs loop**

- A **loop** *repeats* code (`for` / `while`): "do this again and again."
- A **function** *packages* code under a name so you can *reuse* it: "do this whenever I call it."

They work together — a function can contain a loop, and a loop can call a function:

```````python
def total(numbers):          # function: a reusable job
    result = 0
    for n in numbers:        # loop: repeat for every item
        result += n
    return result

print(total([10, 20, 30]))   # 60
print(total([1, 2, 3]))      # 6  ← same function, reused
```````

**Rule of thumb:** repeating *within* one run → loop. Reusing the same logic in *different places* → function."""),

    dict(id="for_vs_while", topic="for vs while loops", module="M04", kind="compare",
         q="What is the difference between a for loop and a while loop?",
         kw="for while loop iterate range repeat",
         a="""**`for` vs `while`**

- Use **`for`** when you know *what* you're looping over (a list, a range, a string).
- Use **`while`** when you repeat *until a condition changes* and don't know how many times.

```````python
for fruit in ["apple", "banana"]:   # known items → for
    print(fruit)

attempts = 0
while attempts < 3:                 # unknown count → while
    attempts += 1
```````

**Watch out:** a `while` loop must change something each time, or it runs forever. A `for` loop stops by itself."""),

    dict(id="list_vs_dict", topic="list vs dictionary", module="M08", kind="compare",
         q="What is the difference between a list and a dictionary?",
         kw="list dictionary dict index key value",
         a="""**List vs dictionary**

| | List | Dictionary |
|---|---|---|
| Look things up by | **position** (`items[0]`) | **key** (`student["name"]`) |
| Written with | `[ ]` | `{ }` |
| Best for | ordered items: scores, names | labelled data: a student record |

```````python
scores = [88, 72, 95]
print(scores[0])               # 88  ← by position

student = {"name": "Alice", "age": 21}
print(student["name"])         # Alice  ← by key
```````

**Rule of thumb:** a plain sequence of similar things → list. Things that each need a *name/label* → dictionary."""),

    dict(id="assign_vs_equals", topic="= vs ==", module="M03", kind="compare",
         q="What is the difference between = and ==?",
         kw="= == assignment comparison equal equals if",
         a="""**`=` vs `==`**

- **`=`** *assigns* a value: "put 5 into x."
- **`==`** *compares* two values: "is x equal to 5?" — it gives `True` or `False`.

```````python
x = 5          # assignment — stores 5 in x
print(x == 5)  # comparison — prints True
print(x == 9)  # prints False

if x == 5:     # ✓ use == inside an if
    print("five!")
# if x = 5:    # ✗ SyntaxError — you can't assign inside an if
``````"""),

    dict(id="print_vs_return", topic="print vs return", module="M06", kind="compare",
         q="What is the difference between print and return?",
         kw="print return function output value none",
         a="""**`print` vs `return`**

- **`print()`** *shows* something on the screen for a human to read. The value is then gone.
- **`return`** *hands a value back* to the code that called the function, so it can be used again.

`````python
def add_print(a, b):
    print(a + b)       # shows 7, but gives back None

def add_return(a, b):
    return a + b       # gives back 7

x = add_print(3, 4)    # prints 7, but x is None
y = add_return(3, 4)   # y is 7
print(y * 2)           # 14 ← we can keep using it
`````

**Rule of thumb:** functions that *calculate* something should `return` it; use `print` only to display results."""),

    dict(id="param_vs_arg", topic="parameter vs argument", module="M15", kind="compare",
         q="What is the difference between a parameter and an argument?",
         kw="parameter argument function call def",
         a="""**Parameter vs argument**

- A **parameter** is the *name* in the function definition (`def greet(name):` → `name`).
- An **argument** is the *actual value* you pass when you call it (`greet("Alice")` → `"Alice"`).

`````python
def greet(name):       # name    = parameter
    return f"Hi, {name}!"

greet("Alice")         # "Alice" = argument
`````

Think of it this way: parameters are the **blanks on a form**, arguments are what you **fill in**."""),

    dict(id="break_vs_continue", topic="break vs continue", module="M05", kind="compare",
         q="What is the difference between break and continue?",
         kw="break continue loop skip exit stop",
         a="""**`break` vs `continue`**

- **`break`** *exits the whole loop* immediately.
- **`continue`** *skips the rest of this round* and jumps to the next one.

`````python
for n in range(1, 6):
    if n == 3:
        continue       # skip 3 only
    print(n)           # 1 2 4 5

for n in range(1, 6):
    if n == 3:
        break          # stop everything at 3
    print(n)           # 1 2
````"""),

    dict(id="common_errors", topic="Common Python error messages", module="M09", kind="faq",
         q="What do common Python error messages mean?",
         kw="nameerror typeerror valueerror keyerror indexerror indentationerror syntaxerror zerodivisionerror error message",
         a="""**What the common errors mean**

| Error | Plain English | Example |
|---|---|---|
| `SyntaxError` | Python can't read your code (missing `:`, bracket…) | `if x > 0` |
| `IndentationError` | Wrong spacing at the start of a line | body not indented |
| `NameError` | You used a name Python doesn't know | typo, or used before defining |
| `TypeError` | Wrong kind of value for the operation | `"5" + 1` |
| `ValueError` | Right type, but unusable value | `int("abc")` |
| `KeyError` | Dictionary key doesn't exist | `d["missing"]` |
| `IndexError` | List position doesn't exist | `[1, 2][5]` |
| `ZeroDivisionError` | Divided by zero | `10 / 0` |

Read the **last line** of the error first — it names the problem — then the line number above it."""),

    dict(id="input_string", topic="input() always returns a string", module="M01", kind="faq",
         q="Why does input() give me a string and how do I get a number?",
         kw="input string convert int float number user type",
         a="""**Why `input()` always gives a string**

`input()` returns **text**, even if the user types a number. Convert it before doing math:

```python
age = input("Age? ")              # user types 21 → age is "21" (a string)
next_year = int(age) + 1          # ✓ int() converts it → 22

price = float(input("Price? "))   # float() for decimals
```

If the text can't be converted (like `"abc"`), Python raises a `ValueError` — wrap it in `try/except` to handle that."""),
]

# Extra search words per lesson, so questions find the right module
MODULE_KEYWORDS = {
    "M01": "variable data type integer float string boolean assign value",
    "M02": "string text f-string method upper lower split slice index replace",
    "M03": "if elif else condition decision boolean comparison branch",
    "M04": "for loop range enumerate iterate sequence repeat",
    "M05": "while loop break continue infinite repeat condition",
    "M06": "function def return parameter call reuse",
    "M07": "list append sort sorted index slice remove",
    "M08": "dictionary dict key value get items lookup",
    "M09": "try except finally exception error handling valueerror zerodivisionerror",
    "M10": "file open read write with encoding utf-8 text file",
    "M11": "class object self init method attribute inheritance oop",
    "M12": "module import library math random datetime standard library",
    "M13": "scope local global nameerror undefined variable",
    "M14": "syntax colon indentation syntaxerror bracket quote parse",
    "M15": "argument parameter call positional keyword args typeerror missing",
}

# ── Extra lessons beyond the 15 core modules (work fully offline) ────────────
EXTRA_TOPICS = [
    {
        "id": "T01", "title": "Tuples", "icon": "📦",
        "tagline": "Ordered collections that can't be changed",
        "kw": "tuple immutable unpack parentheses fixed",
        "learn": {
            "L": ("A **tuple** is an ordered collection like a list, but it is **immutable** — "
                  "once created, it can't be changed. Create one with parentheses `()`."),
            "E": ("```python\n"
                  "point = (3, 4)\n"
                  "print(point[0])        # 3  (indexing works like a list)\n\n"
                  "x, y = point           # unpacking\n"
                  "print(x, y)            # 3 4\n\n"
                  "colors = (\"red\", \"green\", \"blue\")\n"
                  "for c in colors:\n"
                  "    print(c)\n\n"
                  "single = (5,)          # a one-item tuple needs a trailing comma\n"
                  "```"),
            "A": ("A tuple is like a **sealed envelope**: you can read what's inside and pass it around, "
                  "but you can't swap the contents. A list is a whiteboard you can keep erasing."),
            "R": ("**Tuples can't be changed.** Trying `point[0] = 10` raises a `TypeError`. "
                  "Use a tuple for data that shouldn't change (coordinates, RGB colours) "
                  "and a list for data that will."),
            "N": ("🚫 **Common mistake:** forgetting the trailing comma in a one-item tuple.\n\n"
                  "```python\n"
                  "not_a_tuple = (5)      # just the number 5 in brackets!\n"
                  "a_tuple = (5,)         # ✓ the comma makes it a tuple\n"
                  "print(type(not_a_tuple), type(a_tuple))\n"
                  "```"),
        },
        "code": ("point = (3, 4)\nx, y = point\nprint(f\"x={x}, y={y}\")\n"
                 "print(type((5)), type((5,)))\n# Try: point[0] = 10   <- what error do you get?\n"),
    },
    {
        "id": "T02", "title": "Sets", "icon": "🧮",
        "tagline": "Collections of unique items",
        "kw": "set unique duplicate union intersection membership",
        "learn": {
            "L": ("A **set** is an unordered collection of **unique** items. "
                  "Create one with `{}` around values, or `set()` for an empty set. "
                  "Use sets to remove duplicates and to test membership quickly."),
            "E": ("```python\n"
                  "nums = {1, 2, 2, 3, 3, 3}\n"
                  "print(nums)                  # {1, 2, 3}  — duplicates gone\n\n"
                  "nums.add(4)\n"
                  "nums.discard(1)\n\n"
                  "a = {1, 2, 3}\n"
                  "b = {3, 4, 5}\n"
                  "print(a | b)    # union        {1, 2, 3, 4, 5}\n"
                  "print(a & b)    # intersection {3}\n"
                  "print(a - b)    # difference   {1, 2}\n\n"
                  "print(2 in a)   # True — fast membership test\n"
                  "unique = list(set([1, 1, 2, 2, 3]))   # remove duplicates from a list\n"
                  "```"),
            "A": ("A set is like a **guest list**: each name appears once, and there's no seating order. "
                  "Checking \"is Alice on the list?\" is instant."),
            "R": ("**Sets have no order and no duplicates**, so you can't use an index like `s[0]`. "
                  "Use `in` to check membership and a `for` loop to go through the items."),
            "N": ("🚫 **Common mistake:** `{}` creates an empty **dictionary**, not an empty set.\n\n"
                  "```python\n"
                  "empty = {}          # ✗ this is a dict\n"
                  "empty = set()       # ✓ an empty set\n"
                  "print(type({}), type(set()))\n"
                  "```"),
        },
        "code": ("names = [\"Ana\", \"Ben\", \"Ana\", \"Cara\", \"Ben\"]\nunique = set(names)\n"
                 "print(unique)\nprint(len(unique), \"unique names\")\nprint(\"Ana\" in unique)\n"),
    },
    {
        "id": "T03", "title": "List Comprehensions", "icon": "⚡",
        "tagline": "Build a list in one readable line",
        "kw": "list comprehension comprehensions filter transform one-line",
        "learn": {
            "L": ("A **list comprehension** builds a new list in one line by transforming or filtering "
                  "items from another sequence. Pattern: "
                  "`[expression for item in sequence if condition]`."),
            "E": ("```python\n"
                  "nums = [1, 2, 3, 4, 5, 6]\n\n"
                  "squares = [n ** 2 for n in nums]            # [1, 4, 9, 16, 25, 36]\n"
                  "evens   = [n for n in nums if n % 2 == 0]   # [2, 4, 6]\n\n"
                  "# The longer for-loop version of squares:\n"
                  "squares2 = []\n"
                  "for n in nums:\n"
                  "    squares2.append(n ** 2)\n\n"
                  "words = [\"apple\", \"kiwi\", \"banana\"]\n"
                  "lengths = [len(w) for w in words]           # [5, 4, 6]\n"
                  "```"),
            "A": ("Think of an **assembly line in one step**: items go in on the left, each is "
                  "(optionally) checked by a filter and reshaped, and a finished list comes out."),
            "R": ("**Read it left to right:** \"give me *expression* for each *item* in *sequence* "
                  "(if *condition*)\". If it gets long or tricky, use a normal `for` loop — "
                  "clarity beats cleverness."),
            "N": ("🚫 **Common mistake:** putting the `if` in the wrong place. "
                  "A filter goes at the **end**; an `if/else` goes at the **front**.\n\n"
                  "```python\n"
                  "nums = [1, 2, 3, 4]\n"
                  "[n for n in nums if n > 2]                    # filter  → [3, 4]\n"
                  "[\"big\" if n > 2 else \"small\" for n in nums]    # if/else → front\n"
                  "```"),
        },
        "code": ("scores = [88, 72, 95, 61, 84]\npassing = [s for s in scores if s >= 70]\n"
                 "curved = [s + 5 for s in scores]\nprint(passing)\nprint(curved)\n"),
    },
    {
        "id": "T05", "title": "Recursion", "icon": "🪆",
        "tagline": "A function that calls itself",
        "kw": "recursion recursive base case factorial function calls itself",
        "learn": {
            "L": ("**Recursion** is when a function calls *itself* to solve a smaller version of the same "
                  "problem. Every recursive function needs a **base case** (when to stop) and a "
                  "**recursive case** (the call on a smaller problem)."),
            "E": ("```python\n"
                  "def factorial(n):\n"
                  "    if n == 0:                    # base case — stop here\n"
                  "        return 1\n"
                  "    return n * factorial(n - 1)   # recursive case — smaller problem\n\n"
                  "print(factorial(5))   # 120  (5 * 4 * 3 * 2 * 1)\n\n"
                  "def countdown(n):\n"
                  "    if n == 0:\n"
                  "        print(\"Go!\")\n"
                  "        return\n"
                  "    print(n)\n"
                  "    countdown(n - 1)\n\n"
                  "countdown(3)          # 3, 2, 1, Go!\n"
                  "```"),
            "A": ("Recursion is like **Russian nesting dolls**: to reach the smallest doll you open one, "
                  "and inside is a smaller version of the same problem — until you hit the tiny doll "
                  "that doesn't open (the base case)."),
            "R": ("**Write the base case first**, and make sure every call moves *closer* to it. "
                  "Without a base case the function calls itself forever and Python stops it with a "
                  "`RecursionError`."),
            "N": ("🚫 **Common mistake:** forgetting the base case.\n\n"
                  "```python\n"
                  "def bad(n):\n"
                  "    return n * bad(n - 1)   # ✗ never stops → RecursionError\n\n"
                  "def good(n):\n"
                  "    if n <= 1:              # ✓ base case\n"
                  "        return 1\n"
                  "    return n * good(n - 1)\n"
                  "```"),
        },
        "code": ("def sum_to(n):\n    if n == 0:\n        return 0\n    return n + sum_to(n - 1)\n\n"
                 "print(sum_to(4))   # 4 + 3 + 2 + 1 = 10\n"),
    },
]

TOPIC_MAP = {**MODULE_MAP, **{t["id"]: t for t in EXTRA_TOPICS}}


def _module_answer(m):
    L = m["learn"]
    return (f"**{m['icon']} {m['title']}** — {m['tagline']}\n\n"
            f"{L['L']}\n\n**Example**\n\n{L['E']}\n\n**Analogy**\n\n{L['A']}\n\n"
            f"**Key rule**\n\n{L['R']}\n\n**Watch out**\n\n{L['N']}")

def _index(e):
    e["_topic"] = set(tokenize(e["topic"]))
    e["_kw"]   = set(tokenize(e["topic"] + " " + e["kw"]))
    e["_q"]    = set(tokenize(e["question"]))
    e["_body"] = set(tokenize(e["answer"]))
    return e

def build_kb(modules):
    kb = []
    for m in modules:
        kb.append(_index(dict(
            id=m["id"], topic=m["title"], module=m["id"], kind="concept",
            question=f"What is {m['title']}? {m['tagline']}",
            kw=MODULE_KEYWORDS.get(m["id"], ""), answer=_module_answer(m))))
    for t in EXTRA_TOPICS:
        kb.append(_index(dict(
            id=t["id"], topic=t["title"], module=t["id"], kind="concept",
            question=f"What is {t['title']}? {t['tagline']}", kw=t["kw"],
            answer=_module_answer(t))))
    for x in EXTRA_QA:
        kb.append(_index(dict(
            id=x["id"], topic=x["topic"], module=x["module"], kind=x["kind"],
            question=x["q"], kw=x["kw"], answer=x["a"])))
    return kb

KB = build_kb(MODULES)

def search_kb(query, module_id=None, limit=3):
    """Return [(score, coverage, entry), ...] best first."""
    is_compare = bool(set(re.findall(r"[a-z]+", query.lower())) & COMPARE_WORDS)
    qt = list(dict.fromkeys(tokenize(query)))
    if not qt:
        return []
    scored = []
    for e in KB:
        score, hits = 0.0, 0
        for t in qt:
            if t in e["_kw"]:
                score += 3; hits += 1
            elif t in e["_q"]:
                score += 2; hits += 1
            elif t in e["_body"]:
                score += 1
        if score == 0:
            continue
        score += sum(1 for t in qt if t in e["_topic"])      # prefer the entry whose title matches
        if e["kind"] == "compare":
            score = score + 1.5 * hits if is_compare else score * 0.8
        if module_id and e["module"] == module_id:
            score += 1.5
        scored.append((score, hits / len(qt), e))
    scored.sort(key=lambda x: x[0], reverse=True)
    return scored[:limit]

# ─────────────────────────────────────────────────────────────────────────────
#  LLM call with a token limit (Groq first, then Ollama)
# ─────────────────────────────────────────────────────────────────────────────
def _llm(prompt, max_tokens=800):
    key = st.session_state.get("groq_api_key", "").strip()
    if key:
        try:
            r = requests.post(
                GROQ_URL,
                headers={"Authorization": f"Bearer {key}", "Content-Type": "application/json"},
                json={"model": GROQ_MODEL, "messages": [{"role": "user", "content": prompt}],
                      "temperature": 0.4, "max_tokens": max_tokens},
                timeout=30,
            )
            if r.ok:
                text = r.json()["choices"][0]["message"]["content"].strip()
                if text:
                    st.session_state["llm_source"] = "groq"
                    return text
            else:
                st.error(f"Groq API error {r.status_code}: {r.text}")
        except Exception as e:
            st.error(f"Groq request failed: {e}")
    try:
        r = requests.post(OLLAMA_URL, json={"model": MODEL_NAME, "prompt": prompt, "stream": False},
                          timeout=90)
        if r.ok:
            text = r.json().get("response", "").strip()
            if text:
                st.session_state["llm_source"] = "ollama"
                return text
    except Exception:
        pass
    st.session_state["llm_source"] = None
    return None

# ─────────────────────────────────────────────────────────────────────────────
#  "Ask PyLearn" — answer engine + reusable UI
#  Order of attack:  1) knowledge base (instant, vetted)  2) LLM (any question)
#                    3) closest lessons (if no AI is available)
# ─────────────────────────────────────────────────────────────────────────────
def build_qa_prompt(question, entries, profile, module=None):
    level = profile.get("level", "beginner")
    tone = {
        "complete beginner": "Use very simple language, avoid jargon, use an everyday analogy.",
        "some experience":   "Be clear and friendly. Basic Python terms are fine.",
        "intermediate":      "Be concise. Standard Python terminology is fine.",
    }.get(level, "Be clear and friendly.")
    where = f"The student is currently on the lesson: {module['title']}.\n" if module else ""
    if entries:
        material = "\n\n".join(f"[{e['topic']}]\n{e['answer'][:900]}" for e in entries)
        source = f"Lesson material to base your answer on:\n{material}\n\n"
    else:
        source = ""
    return (
        f"You are a friendly Python tutor for a {level} programmer. {tone}\n"
        f"{where}Student question: \"{question}\"\n\n{source}"
        "Answer the question directly in under 180 words. Include one short, correct Python "
        "code example if it helps, and end with a one-line 'Try it:' suggestion. "
        "If the question is not about Python or programming, politely say you can only help with Python."
    )

def answer_question(question, module=None):
    """Find the best answer for a student's question. Returns a result dict."""
    module_id = module["id"] if module else None
    hits      = search_kb(question, module_id)
    n_tokens  = len(set(tokenize(question)))
    need      = 3 if n_tokens <= 1 else 6
    confident = bool(hits) and hits[0][0] >= need and hits[0][1] >= 0.5

    refs = []
    for score, _, e in hits:
        if score >= 2 and e["module"] and e["module"] not in refs:
            refs.append(e["module"])

    result = {"question": question, "answer": "", "source": "related",
              "refs": refs[:3], "llm": None}

    # 1) Knowledge base — instant, consistent, no API call
    if confident:
        result.update(answer=hits[0][2]["answer"], source="kb")
        return result

    # 2) LLM — grounded in the closest lesson material
    context = [e for score, _, e in hits[:2] if score >= 3]
    ai = _llm(build_qa_prompt(question, context, st.session_state.get("profile", {}), module))
    if ai:
        result.update(answer=ai, source="ai", llm=st.session_state.get("llm_source"))
        return result

    # 3) No AI available — point to the closest lessons
    return result

def render_answer(res, key):
    st.markdown("---")
    st.caption(f"You asked: “{res['question']}”")
    if res["source"] == "kb":
        st.markdown("#### 📚 Answer from the PyLearn knowledge base")
        st.markdown(res["answer"])
    elif res["source"] == "ai":
        who = "Groq" if res.get("llm") == "groq" else "Ollama"
        st.markdown(f"#### 🤖 AI answer ({who})")
        st.markdown(res["answer"])
    else:
        st.markdown("#### 🔍 I couldn't find an exact answer")
        st.info(
            "That question isn't in the lessons yet. Add a free **Groq API key** in "
            "**AI Settings** (sidebar) and I can answer any Python question."
            + (" Meanwhile, these lessons are the closest match:" if res["refs"] else "")
        )
    if res["refs"]:
        st.markdown("**📖 Related lessons**")
        cols = st.columns(len(res["refs"]))
        for col, mid in zip(cols, res["refs"]):
            m = TOPIC_MAP[mid]
            if col.button(f"{m['icon']} {m['title']}", key=f"rel_{key}_{mid}",
                          use_container_width=True):
                go_to_topic(mid)
    if res["source"] == "ai":
        if st.button("📘 Teach me this as a full lesson", key=f"teach_{key}",
                     use_container_width=True):
            st.session_state["topic_pending"] = res["question"]
            st.session_state.page = "topics"
            st.rerun()

def ask_box(key, module=None, placeholder="e.g. What's the difference between a function and a class?"):
    """A question box that fetches the answer automatically (press Enter or click)."""
    with st.form(f"ask_form_{key}"):
        q   = st.text_input("Ask any Python question", placeholder=placeholder, key=f"ask_q_{key}")
        sub = st.form_submit_button("🔎 Get answer", use_container_width=True)
    if sub:
        if q.strip():
            with st.spinner("Looking that up…"):
                st.session_state[f"ask_res_{key}"] = answer_question(q.strip(), module)
        else:
            st.warning("Please type a question first.")
    res = st.session_state.get(f"ask_res_{key}")
    if res:
        render_answer(res, key)

# ─────────────────────────────────────────────────────────────────────────────
#  "Learn Any Topic" — students pick ANY topic and get a full L.E.A.R.N. lesson
#  1) known topic (15 core lessons + extra lessons)  2) AI-generated lesson
#  3) closest lessons (if no AI is available)
# ─────────────────────────────────────────────────────────────────────────────
TOPIC_FILLER = {"learn", "teach", "topic", "lesson", "tutorial", "basic",
                "introduction", "intro", "course", "study", "show"}

def find_topic(query):
    """Return the id of the lesson that best matches the topic, or None."""
    qt = [t for t in dict.fromkeys(tokenize(query)) if t not in TOPIC_FILLER]
    if not qt:
        return None
    need = 3 if len(qt) == 1 else 6
    best = None
    for e in KB:
        if e["kind"] != "concept":
            continue
        score, hits = 0, 0
        for t in qt:
            if t in e["_kw"]:
                score += 3; hits += 1
            elif t in e["_q"]:
                score += 2; hits += 1
            elif t in e["_body"]:
                score += 1
        score += sum(1 for t in qt if t in e["_topic"])
        if score >= need and hits / len(qt) >= 0.5 and (best is None or score > best[0]):
            best = (score, e["id"])
    return best[1] if best else None

def build_topic_prompt(topic, profile):
    level = profile.get("level", "beginner")
    tone = {
        "complete beginner": "Use very simple language, avoid jargon.",
        "some experience":   "Be clear and friendly. Basic Python terms are fine.",
        "intermediate":      "Be concise. Standard Python terminology is fine.",
    }.get(level, "Be clear and friendly.")
    return (
        f"You are a Python tutor. Teach the topic \"{topic}\" to a {level} programmer "
        f"using the L.E.A.R.N. framework. {tone}\n\n"
        "Use EXACTLY these section headings, each on its own line, in this order, "
        "with nothing before the first heading:\n"
        "## L\n(Label: what it is and why Python needs it — 2 or 3 sentences)\n"
        "## E\n(Example: a short, correct, runnable Python code block in ```python fences, with comments)\n"
        "## A\n(Analogy: an everyday real-world comparison — 2 or 3 sentences)\n"
        "## R\n(Rule: the single most important rule to remember)\n"
        "## N\n(Note: the most common beginner mistake, with a tiny wrong/right code snippet)\n"
        "## CODE\n(One short runnable practice snippet in a ```python block for the student to edit)\n\n"
        "If the topic is not about Python or programming, reply with only: NOT_PYTHON"
    )

def parse_lesson(text):
    """Split an AI lesson into ({L,E,A,R,N}, practice_code). (None, None) if malformed."""
    parts = re.split(r"(?m)^[ \t]*(?:#{1,4}|\*\*)[ \t]*(L|E|A|R|N|CODE)\b[^\n]*\n?", text)
    secs = {}
    for i in range(1, len(parts) - 1, 2):
        secs[parts[i]] = parts[i + 1].strip()
    if not all(secs.get(k) for k in "LEARN"):
        return None, None
    code = None
    m = re.search(r"```(?:python)?\n(.*?)```", secs.get("CODE", ""), re.S)
    if m:
        code = m.group(1).strip() + "\n"
    return {k: secs[k] for k in "LEARN"}, code

def resolve_topic(query):
    """Decide what to show for a topic and store it in session_state['topic_view']."""
    known = find_topic(query)
    if known:
        st.session_state["topic_view"] = {"kind": "known", "id": known}
        return
    text = _llm(build_topic_prompt(query, st.session_state.get("profile", {})),
                max_tokens=1200)
    if not text:
        st.session_state["topic_view"] = {"kind": "none", "query": query}
    elif "NOT_PYTHON" in text:
        st.session_state["topic_view"] = {"kind": "offtopic", "query": query}
    else:
        learn, code = parse_lesson(text)
        st.session_state["topic_view"] = {
            "kind": "ai", "query": query, "title": query.strip().capitalize(),
            "learn": learn, "code": code, "raw": text,
            "llm": st.session_state.get("llm_source"),
        }

def go_to_topic(mid):
    """Open a lesson: core modules open the full lesson page, extras open the topic page."""
    if mid in MODULE_MAP:
        st.session_state.current_module = mid
        st.session_state.page = "lesson"
    else:
        st.session_state["topic_view"] = {"kind": "known", "id": mid}
        st.session_state.page = "topics"
    st.rerun()

def render_topic_view(view):
    st.markdown("---")
    kind = view["kind"]

    if kind == "known":
        obj = TOPIC_MAP[view["id"]]
        st.markdown(f"## {obj['icon']} {obj['title']}")
        st.markdown(f"*{obj['tagline']}*")
        render_learn(obj["learn"])
        if view["id"] in MODULE_MAP:
            st.info("This topic is part of the core curriculum, so it has a coding challenge "
                    "with C.O.D.E. feedback.")
            if st.button("💻 Open the full lesson & challenge →", key="topic_open_full",
                         use_container_width=True):
                go_to_topic(view["id"])
        else:
            _practice_block(obj.get("code"))

    elif kind == "ai":
        who = "Groq" if view.get("llm") == "groq" else "Ollama"
        st.markdown(f"## 🎓 {view['title']}")
        st.caption(f"🤖 Lesson generated by AI ({who}) in the L.E.A.R.N. format")
        if view.get("learn"):
            render_learn(view["learn"])
            _practice_block(view.get("code"))
        else:
            st.markdown(view["raw"])

    elif kind == "offtopic":
        st.warning(f"“{view['query']}” doesn't look like a Python topic. "
                   "Try something like *recursion*, *tuples* or *file handling*.")

    else:  # none — no AI available and no matching lesson
        st.markdown(f"## 🔍 No lesson for “{view['query']}” yet")
        st.info("That topic isn't built in. Add a free **Groq API key** in **AI Settings** "
                "(sidebar) and PyLearn can teach you **any** Python topic. "
                "These lessons are the closest match:")
        shown = []
        for score, _, e in search_kb(view["query"], None, limit=6):
            if e["kind"] == "concept" and score >= 2 and e["id"] not in shown:
                shown.append(e["id"])
        for mid in shown[:3]:
            t = TOPIC_MAP[mid]
            if st.button(f"{t['icon']} {t['title']}", key=f"near_{mid}", use_container_width=True):
                go_to_topic(mid)

def _practice_block(code):
    if not code:
        return
    st.markdown("### 💻 Try it yourself")
    st.code(code, language="python")
    st.caption("Click the copy icon on the code, then paste it into ✏️ Free Practice for C.O.D.E. feedback.")
    if st.button("✏️ Open Free Practice", key="topic_practice", use_container_width=True):
        st.session_state.page = "practice"
        st.rerun()

# ─────────────────────────────────────────────────────────────────────────────
#  Home page helpers
# ─────────────────────────────────────────────────────────────────────────────
def render_module_list(progress, prefix):
    """The 15 modules grouped into sections (used by the dashboard and the home expander)."""
    sections = [
        ("🌱 Foundations",          MODULES[0:5]),
        ("🔧 Core Building Blocks", MODULES[5:9]),
        ("📚 Advanced Topics",      MODULES[9:12]),
        ("🎯 Precision & Safety",   MODULES[12:15]),
    ]
    for section_title, section_modules in sections:
        st.markdown(f"### {section_title}")
        for mod in section_modules:
            completed  = mod["id"] in progress
            understood = progress.get(mod["id"], {}).get("understood", None)
            badge = "✅" if (completed and understood) else ("🔁" if completed else "⬜")
            col1, col2 = st.columns([5, 1])
            with col1:
                st.markdown(f"**{badge} {mod['icon']} {mod['title']}**")
                st.caption(mod["tagline"])
                if completed:
                    label = "Understood ✓" if understood else "Needs more practice"
                    st.caption(f"Status: {label} · {progress[mod['id']]['completed_at'][:10]}")
            with col2:
                if st.button("Review" if completed else "Start",
                             key=f"{prefix}_{mod['id']}", use_container_width=True):
                    st.session_state.current_module = mod["id"]
                    st.session_state.page = "lesson"
                    st.rerun()
            st.markdown("---")

def _ask_example(key, question):
    """Button callback: fetch the answer for an example question."""
    st.session_state[f"ask_res_{key}"] = answer_question(question)


    # ═════════════════════════════════════════════════════════════════════════════
#  🩹 PATCH — focused answers for "what is X?" questions
# ═════════════════════════════════════════════════════════════════════════════
EXTRA_QA.append(dict(id="global_local", topic="local and global variables", module="M13", kind="faq",
    q="What are global and local variables?",
    kw="global local variable scope function inside outside",
    a="""**Global vs local variables**

- A **global variable** is created *outside* every function, so any function can read it.
- A **local variable** is created *inside* a function. It only exists there and disappears when the function ends.

```python
count = 10            # global — visible everywhere

def show():
    message = "hi"    # local — only exists inside show()
    print(count)      # ✓ can read the global
    print(message)    # ✓ can use its own local

show()
print(count)          # ✓ 10
print(message)        # ✗ NameError — message only lived inside show()
```

To **change** a global inside a function, use the `global` keyword:

```python
total = 0

def add_one():
    global total      # "I mean the global total"
    total += 1

add_one()
print(total)          # 1
```

**Rule of thumb:** prefer passing values in as parameters and returning results, instead of changing globals."""))

EXTRA_QA.append(dict(id="self_meaning", topic="self in classes", module="M11", kind="faq",
    q="What does self mean in a class?",
    kw="self init method class object attribute this",
    a="""**What does `self` mean?**

`self` is the object a method is working on — "this particular one". Python passes it in automatically, so you write it in the method definition but never when you call the method.

```python
class Dog:
    def __init__(self, name):
        self.name = name          # store the name on THIS dog

    def speak(self):
        return f"{self.name} says Woof!"

rex = Dog("Rex")
print(rex.speak())                # Rex says Woof!  (Python passed rex as self)
```

**Rule of thumb:** every method in a class starts with `self`, and attributes are saved with `self.name = ...`."""))

EXTRA_QA.append(dict(id="none_meaning", topic="None", module="M06", kind="faq",
    q="What is None in Python?",
    kw="none null nothing return value empty",
    a="""**What is `None`?**

`None` is Python's way of saying "nothing here yet". It is a real value, not an error — and it's what a function gives back when it has no `return`.

```python
def say_hi():
    print("hi")        # no return statement

result = say_hi()      # prints hi
print(result)          # None

name = None            # "no value yet"
if name is None:
    print("name is not set")
```

**Rule of thumb:** check for it with `is None` (not `== None`)."""))

KB = build_kb(MODULES)      # rebuild so the new answers are searchable

def answer_question(question, module=None):
    """Find the best answer: precise built-in answer → AI (exact question) → matching lesson."""
    module_id = module["id"] if module else None
    hits      = search_kb(question, module_id)
    n_tokens  = len(set(tokenize(question)))
    need      = 3 if n_tokens <= 1 else 6
    confident = bool(hits) and hits[0][0] >= need and hits[0][1] >= 0.5
    kind      = hits[0][2]["kind"] if hits else None

    refs = []
    for score, _, e in hits:
        if score >= 2 and e["module"] and e["module"] not in refs:
            refs.append(e["module"])

    result = {"question": question, "answer": "", "source": "related",
              "refs": refs[:3], "llm": None, "kind": kind}

    # 1) A precise built-in answer (X-vs-Y or FAQ) — instant, no API call
    if confident and kind in ("compare", "faq"):
        result.update(answer=hits[0][2]["answer"], source="kb")
        return result

    # 2) The AI answers the exact question, using the closest lesson as its source
    has_key = bool(st.session_state.get("groq_api_key", "").strip())
    if has_key or not confident:
        context = [e for score, _, e in hits[:2] if score >= 3]
        ai = _llm(build_qa_prompt(question, context, st.session_state.get("profile", {}), module))
        if ai:
            result.update(answer=ai, source="ai", llm=st.session_state.get("llm_source"))
            return result

    # 3) Only a whole lesson matched and no AI is available — show that lesson
    if confident:
        result.update(answer=hits[0][2]["answer"], source="kb")
    return result

def render_answer(res, key):
    st.markdown("---")
    st.caption(f"You asked: “{res['question']}”")
    if res["source"] == "kb" and res.get("kind") == "concept":
        st.markdown("#### 📖 The lesson that covers your question")
        st.info("PyLearn doesn't have a one-line answer for this yet, so here is the lesson "
                "that explains it. Add a free **Groq API key** in **AI Settings** (sidebar) "
                "to get a direct answer to your exact question.")
        st.markdown(res["answer"])
    elif res["source"] == "kb":
        st.markdown("#### 📚 Answer from the PyLearn knowledge base")
        st.markdown(res["answer"])
    elif res["source"] == "ai":
        who = "Groq" if res.get("llm") == "groq" else "Ollama"
        st.markdown(f"#### 🤖 AI answer ({who})")
        st.markdown(res["answer"])
    else:
        st.markdown("#### 🔍 I couldn't find an exact answer")
        st.info(
            "That question isn't in the lessons yet. Add a free **Groq API key** in "
            "**AI Settings** (sidebar) and I can answer any Python question."
            + (" Meanwhile, these lessons are the closest match:" if res["refs"] else "")
        )
    if res["refs"]:
        st.markdown("**📖 Related lessons**")
        cols = st.columns(len(res["refs"]))
        for col, mid in zip(cols, res["refs"]):
            m = TOPIC_MAP[mid]
            if col.button(f"{m['icon']} {m['title']}", key=f"rel_{key}_{mid}",
                          use_container_width=True):
                go_to_topic(mid)
    if res["source"] == "ai":
        if st.button("📘 Teach me this as a full lesson", key=f"teach_{key}",
                     use_container_width=True):
            st.session_state["topic_pending"] = res["question"]
            st.session_state.page = "topics"
            st.rerun()
# ═════════════════════════════════════════════════════════════════════════════
#  🩹 PATCH 2 — every answer in the L.E.A.R.N. format (Label · Example · Analogy · Rule · Note)
# ═════════════════════════════════════════════════════════════════════════════
EXTRA_QA = [
    dict(id="while_vs_dowhile", topic="while vs do-while loops", module="M05", kind="compare",
         q="What is the difference between a while loop and a do-while loop?",
         kw="while do-while dowhile loop repeat condition",
         learn={
"L": """A **`while` loop** checks its condition *before* each run, so the body may run **zero times**. A **`do-while` loop** (in C, Java, JavaScript) checks *after* each run, so it always runs **at least once**. **Python has no do-while.**""",
"E": """```python
# while — checks first
count = 5
while count < 3:
    print("never runs")      # the condition is False from the start

# do-while style in Python: while True + break
while True:
    answer = input("Play again? (y/n) ")   # always runs once
    if answer == "n":
        break                              # the "after" check
```````````````""",
"A": """A `while` loop is a **bouncer checking tickets at the door** — no ticket, you never get in. A do-while is a **café that hands you a free sample first**, then asks if you want more.""",
"R": """Need the body to run **at least once** (menus, input checks)? Use `while True` + `break`. Otherwise use a normal `while`.""",
"N": """🚫 **Common mistake:** looking for a `do-while` keyword in Python. It doesn't exist — writing `do { ... } while (...)` gives a `SyntaxError`."""}),

    dict(id="function_vs_class", topic="function vs class", module="M11", kind="compare",
         q="What is the difference between a function and a class?",
         kw="function class method object def self attribute oop",
         learn={
"L": """A **function** is a reusable block of code that does *one job* (inputs in, result out). A **class** is a blueprint that bundles **data** (attributes) and **functions** (methods) together into objects.""",
"E": """```python
# Function — just does a job
def area(width, height):
    return width * height

# Class — holds data AND behaviour together
class Rectangle:
    def __init__(self, width, height):
        self.width = width
        self.height = height

    def area(self):
        return self.width * self.height

print(area(3, 4))               # 12
print(Rectangle(3, 4).area())   # 12
``````````````""",
"A": """A function is a **recipe card**: follow the steps, get a dish. A class is a **blueprint for a kitchen**: it describes the equipment (data) *and* what each piece can do (methods), and you can build many kitchens from it.""",
"R": """One task → write a function. Something with its own data that does several related things (a student, a bank account) → write a class.""",
"N": """🚫 **Common mistake:** writing a class for something a simple function could do. If there's no data to remember, a function is enough."""}),

    dict(id="function_vs_loop", topic="function vs loop", module="M06", kind="compare",
         q="What is the difference between a function and a loop?",
         kw="function loop def for while repeat reuse",
         learn={
"L": """A **loop** *repeats* code (`for` / `while`). A **function** *packages* code under a name so you can *reuse* it. They work together: a function can contain a loop, and a loop can call a function.""",
"E": """```python
def total(numbers):          # function: a reusable job
    result = 0
    for n in numbers:        # loop: repeat for every item
        result += n
    return result

print(total([10, 20, 30]))   # 60
print(total([1, 2, 3]))      # 6  ← same function, reused
`````````````""",
"A": """A loop is a **washing-machine cycle**: it repeats the same steps until it's done. A function is the **button labelled "Wash"**: one name you can press from anywhere.""",
"R": """Repeating *within* one run → loop. Reusing the same logic in *different places* → function.""",
"N": """🚫 **Common mistake:** copy-pasting the same loop in several places. Put it inside a function and call that instead."""}),

    dict(id="for_vs_while", topic="for vs while loops", module="M04", kind="compare",
         q="What is the difference between a for loop and a while loop?",
         kw="for while loop iterate range repeat",
         learn={
"L": """Use a **`for` loop** when you know *what* you're looping over (a list, a range, a string). Use a **`while` loop** when you repeat *until a condition changes* and don't know how many times.""",
"E": """```python
for fruit in ["apple", "banana"]:   # known items → for
    print(fruit)

attempts = 0
while attempts < 3:                 # unknown count → while
    attempts += 1
````````````""",
"A": """`for` is **delivering mail down a street**: you stop after the last house. `while` is **knocking until someone answers**: you don't know how many tries it will take.""",
"R": """Known items or a known count → `for`. Unknown count, repeat until something changes → `while`.""",
"N": """🚫 **Common mistake:** forgetting to change the variable in a `while` loop, so it runs forever. (Press **Ctrl+C** to stop it.)"""}),

    dict(id="list_vs_dict", topic="list vs dictionary", module="M08", kind="compare",
         q="What is the difference between a list and a dictionary?",
         kw="list dictionary dict index key value",
         learn={
"L": """A **list** stores items in order and you look them up by **position** (`items[0]`). A **dictionary** stores **key → value** pairs and you look things up by **key** (`student["name"]`).""",
"E": """```python
scores = [88, 72, 95]
print(scores[0])               # 88  ← by position

student = {"name": "Alice", "age": 21}
print(student["name"])         # Alice  ← by key
```````````""",
"A": """A list is a **numbered queue**: position matters. A dictionary is a **phone book**: you look up a name, not a page number.""",
"R": """A plain sequence of similar things → list. Things that each need a name or label → dictionary.""",
"N": """🚫 **Common mistake:** using `student["phone"]` when the key might not exist. Use `student.get("phone", "N/A")` to avoid a `KeyError`."""}),

    dict(id="assign_vs_equals", topic="= vs ==", module="M03", kind="compare",
         q="What is the difference between = and ==?",
         kw="= == assignment comparison equal equals if",
         learn={
"L": """**`=`** *assigns* a value ("put 5 into x"). **`==`** *compares* two values ("is x equal to 5?") and gives `True` or `False`.""",
"E": """```python
x = 5          # assignment — stores 5 in x
print(x == 5)  # comparison — prints True
print(x == 9)  # prints False

if x == 5:     # ✓ use == inside an if
    print("five!")
``````````""",
"A": """`=` is **writing a name on a box and putting something inside**. `==` is **asking "are these two boxes holding the same thing?"**""",
"R": """Use `==` in `if` and `while` conditions. Use `=` only to store a value.""",
"N": """🚫 **Common mistake:** writing `if x = 5:` — that's a `SyntaxError`. You almost always want `if x == 5:`."""}),

    dict(id="print_vs_return", topic="print vs return", module="M06", kind="compare",
         q="What is the difference between print and return?",
         kw="print return function output value none",
         learn={
"L": """**`print()`** *shows* something on the screen for a human to read — then the value is gone. **`return`** *hands a value back* to the code that called the function, so it can be used again.""",
"E": """```python
def add_print(a, b):
    print(a + b)       # shows 7, but gives back None

def add_return(a, b):
    return a + b       # gives back 7

x = add_print(3, 4)    # prints 7, but x is None
y = add_return(3, 4)   # y is 7
print(y * 2)           # 14 ← we can keep using it
`````````""",
"A": """`print` is **reading a number out loud**: everyone hears it, but nobody can use it afterwards. `return` is **handing someone the number written on a card**: they can keep it and use it.""",
"R": """Functions that *calculate* something should `return` it. Use `print` only to display results.""",
"N": """🚫 **Common mistake:** printing inside a function and then expecting a value back — you get `None`."""}),

    dict(id="param_vs_arg", topic="parameter vs argument", module="M15", kind="compare",
         q="What is the difference between a parameter and an argument?",
         kw="parameter argument function call def",
         learn={
"L": """A **parameter** is the *name* in the function definition (`def greet(name):` → `name`). An **argument** is the *actual value* you pass when you call it (`greet("Alice")` → `"Alice"`).""",
"E": """```python
def greet(name):       # name    = parameter
    return f"Hi, {name}!"

greet("Alice")         # "Alice" = argument
````````""",
"A": """Parameters are the **blanks on a form**. Arguments are what you **write in the blanks**.""",
"R": """Parameters belong to the `def` line; arguments belong to the call. A parameter with no default must always get an argument.""",
"N": """🚫 **Common mistake:** calling `greet()` with nothing inside the brackets when `name` is required — `TypeError: missing 1 required positional argument`."""}),

    dict(id="break_vs_continue", topic="break vs continue", module="M05", kind="compare",
         q="What is the difference between break and continue?",
         kw="break continue loop skip exit stop",
         learn={
"L": """**`break`** *exits the whole loop* immediately. **`continue`** *skips the rest of this round* and jumps to the next one.""",
"E": """```python
for n in range(1, 6):
    if n == 3:
        continue       # skip 3 only
    print(n)           # 1 2 4 5

for n in range(1, 6):
    if n == 3:
        break          # stop everything at 3
    print(n)           # 1 2
```````""",
"A": """`continue` is **skipping one song** in a playlist. `break` is **turning the music off**.""",
"R": """`continue` → go to the next round of the same loop. `break` → leave the loop completely.""",
"N": """🚫 **Common mistake:** using `continue` in a `while` loop *before* updating the counter. The loop never moves on and runs forever."""}),

    dict(id="common_errors", topic="Common Python error messages", module="M09", kind="faq",
         q="What do common Python error messages mean?",
         kw="nameerror typeerror valueerror keyerror indexerror indentationerror syntaxerror zerodivisionerror error message",
         learn={
"L": """Python reports problems as **named errors**. The name tells you *what kind* of problem it is, and the line number tells you *where* it happened.""",
"E": """| Error | Plain English | Example |
|---|---|---|
| `SyntaxError` | Python can't read your code (missing `:`, bracket…) | `if x > 0` |
| `IndentationError` | Wrong spacing at the start of a line | body not indented |
| `NameError` | You used a name Python doesn't know | typo, or used before defining |
| `TypeError` | Wrong kind of value for the operation | `"5" + 1` |
| `ValueError` | Right type, but unusable value | `int("abc")` |
| `KeyError` | Dictionary key doesn't exist | `d["missing"]` |
| `IndexError` | List position doesn't exist | `[1, 2][5]` |
| `ZeroDivisionError` | Divided by zero | `10 / 0` |""",
"A": """An error message is like a **warning light on a car dashboard**: it doesn't fix anything, but it tells you which part to check.""",
"R": """Read the **last line** of the error first (it names the problem), then the line number just above it.""",
"N": """🚫 **Common mistake:** panicking at the long traceback. Ignore most of it — the last line and the line number are what matter."""}),

    dict(id="input_string", topic="input() always returns a string", module="M01", kind="faq",
         q="Why does input() give me a string and how do I get a number?",
         kw="input string convert int float number user type",
         learn={
"L": """`input()` always returns **text** (a string), even when the user types a number. To do math, convert it with `int()` or `float()`.""",
"E": """```python
age = input("Age? ")              # user types 21 → age is "21" (a string)
next_year = int(age) + 1          # ✓ int() converts it → 22

price = float(input("Price? "))   # float() for decimals
``````""",
"A": """`input()` is like a **handwritten note**: even if it says `21`, it's ink on paper, not a number you can add up until you read it *as* a number.""",
"R": """Always convert: `int(input(...))` for whole numbers, `float(input(...))` for decimals.""",
"N": """🚫 **Common mistake:** `age + 1` while `age` is still text → `TypeError`. And `int("abc")` raises a `ValueError`, so wrap user input in `try/except`."""}),

    dict(id="global_local", topic="local and global variables", module="M13", kind="faq",
         q="What are global and local variables?",
         kw="global local variable scope function inside outside",
         learn={
"L": """A **global variable** is created *outside* every function, so any function can read it. A **local variable** is created *inside* a function — it only exists there and disappears when the function ends.""",
"E": """```python
count = 10            # global — visible everywhere

def show():
    message = "hi"    # local — only exists inside show()
    print(count)      # ✓ can read the global
    print(message)    # ✓ can use its own local

show()
print(count)          # ✓ 10
print(message)        # ✗ NameError — message only lived inside show()

total = 0
def add_one():
    global total      # needed to CHANGE a global
    total += 1
`````""",
"A": """Scope is like **office floors**: a local variable lives only on its own floor (the function). Everyone can see the lobby (globals), but nobody outside can see into your private office.""",
"R": """A function can **read** a global, but to **change** one it must say `global name` first. Better still: pass values in as parameters and `return` results.""",
"N": """🚫 **Common mistake:** creating `message` inside a function and printing it outside — `NameError`, because it only lived inside the function."""}),

    dict(id="self_meaning", topic="self in classes", module="M11", kind="faq",
         q="What does self mean in a class?",
         kw="self init method class object attribute this",
         learn={
"L": """`self` is **the object a method is working on** — "this particular one". Python passes it in automatically, so you write it in the method definition but never when you call the method.""",
"E": """```python
class Dog:
    def __init__(self, name):
        self.name = name          # store the name on THIS dog

    def speak(self):
        return f"{self.name} says Woof!"

rex = Dog("Rex")
print(rex.speak())                # Rex says Woof!  (Python passed rex as self)
````""",
"A": """`self` is like writing **"my"** on your own mug: `self.name` means "*my* name", not anyone else's.""",
"R": """Every method in a class starts with `self`, and attributes are saved with `self.name = ...`.""",
"N": """🚫 **Common mistake:** writing `name = name` in `__init__` instead of `self.name = name` — the value is thrown away when the method ends."""}),

    dict(id="none_meaning", topic="None", module="M06", kind="faq",
         q="What is None in Python?",
         kw="none null nothing return value empty",
         learn={
"L": """`None` is Python's way of saying **"nothing here yet"**. It is a real value, not an error — and it's what a function gives back when it has no `return`.""",
"E": """```python
def say_hi():
    print("hi")        # no return statement

result = say_hi()      # prints hi
print(result)          # None

name = None            # "no value yet"
if name is None:
    print("name is not set")
```""",
"A": """`None` is an **empty parking space**: the space exists, there's just no car in it yet.""",
"R": """Check for it with `is None` (not `== None`).""",
"N": """🚫 **Common mistake:** forgetting `return` in a function, then being surprised the result is `None`."""}),
]

def _learn_text(learn):
    return "\n\n".join(learn[k] for k in "LEARN")

def _index(e):
    e["answer"] = _learn_text(e["learn"])
    e["_topic"] = set(tokenize(e["topic"]))
    e["_kw"]    = set(tokenize(e["topic"] + " " + e["kw"]))
    e["_q"]     = set(tokenize(e["question"]))
    e["_body"]  = set(tokenize(e["answer"]))
    return e

def build_kb(modules):
    kb = []
    for m in modules:
        kb.append(_index(dict(
            id=m["id"], topic=m["title"], module=m["id"], kind="concept",
            question=f"What is {m['title']}? {m['tagline']}",
            kw=MODULE_KEYWORDS.get(m["id"], ""), learn=m["learn"])))
    for t in EXTRA_TOPICS:
        kb.append(_index(dict(
            id=t["id"], topic=t["title"], module=t["id"], kind="concept",
            question=f"What is {t['title']}? {t['tagline']}", kw=t["kw"], learn=t["learn"])))
    for x in EXTRA_QA:
        kb.append(_index(dict(
            id=x["id"], topic=x["topic"], module=x["module"], kind=x["kind"],
            question=x["q"], kw=x["kw"], learn=x["learn"])))
    return kb

KB = build_kb(MODULES)      # rebuild so every answer is L.E.A.R.N.

def build_qa_prompt(question, entries, profile, module=None):
    level = profile.get("level", "beginner")
    tone = {
        "complete beginner": "Use very simple language, avoid jargon.",
        "some experience":   "Be clear and friendly. Basic Python terms are fine.",
        "intermediate":      "Be concise. Standard Python terminology is fine.",
    }.get(level, "Be clear and friendly.")
    where = f"The student is currently on the lesson: {module['title']}.\n" if module else ""
    source = ""
    if entries:
        material = "\n\n".join(f"[{e['topic']}]\n{e['answer'][:900]}" for e in entries)
        source = f"Lesson material you can use:\n{material}\n\n"
    return (
        f"You are a friendly Python tutor for a {level} programmer. {tone}\n"
        f"{where}Student question: \"{question}\"\n\n{source}"
        "Answer THIS exact question using the L.E.A.R.N. framework. Use EXACTLY these headings, "
        "each on its own line, in this order, with nothing before the first heading:\n"
        "## L\n(Label: a direct answer to the question — 2 or 3 sentences)\n"
        "## E\n(Example: a short, correct Python code block in ```python fences, with comments)\n"
        "## A\n(Analogy: an everyday real-world comparison — 1 or 2 sentences)\n"
        "## R\n(Rule: the one most important rule to remember)\n"
        "## N\n(Note: the most common beginner mistake)\n"
        "Keep the whole answer under 220 words. "
        "If the question is not about Python or programming, reply with only: NOT_PYTHON"
    )

def answer_question(question, module=None):
    """Best answer, always in L.E.A.R.N.: precise built-in → AI (exact question) → matching lesson."""
    module_id = module["id"] if module else None
    hits      = search_kb(question, module_id)
    n_tokens  = len(set(tokenize(question)))
    need      = 3 if n_tokens <= 1 else 6
    confident = bool(hits) and hits[0][0] >= need and hits[0][1] >= 0.5
    top       = hits[0][2] if hits else None
    kind      = top["kind"] if top else None

    refs = []
    for score, _, e in hits:
        if score >= 2 and e["module"] and e["module"] not in refs:
            refs.append(e["module"])

    result = {"question": question, "answer": "", "learn": None, "source": "related",
              "refs": refs[:3], "llm": None, "kind": kind}

    def from_builtin():
        result.update(answer=top["answer"], learn=top["learn"], source="kb")
        return result

    # 1) A precise built-in answer (X-vs-Y or FAQ) — instant, no API call
    if confident and kind in ("compare", "faq"):
        return from_builtin()

    # 2) The AI answers the exact question in L.E.A.R.N., using the closest lesson as its source
    has_key = bool(st.session_state.get("groq_api_key", "").strip())
    if has_key or not confident:
        context = [e for score, _, e in hits[:2] if score >= 3]
        ai = _llm(build_qa_prompt(question, context, st.session_state.get("profile", {}), module))
        if ai:
            if "NOT_PYTHON" in ai:
                result.update(source="offtopic")
                return result
            learn, _ = parse_lesson(ai)
            result.update(answer=ai, learn=learn, source="ai", llm=st.session_state.get("llm_source"))
            return result

    # 3) Only a whole lesson matched and no AI is available — show that lesson
    if confident:
        return from_builtin()
    return result

def render_answer(res, key):
    st.markdown("---")
    st.caption(f"You asked: “{res['question']}”")
    src = res["source"]
    if src == "kb" and res.get("kind") == "concept":
        st.markdown("#### 📖 The lesson that covers your question")
        st.info("PyLearn doesn't have a one-line answer for this yet, so here is the lesson "
                "that explains it. Add a free **Groq API key** in **AI Settings** (sidebar) "
                "to get a direct answer to your exact question.")
    elif src == "kb":
        st.markdown("#### 📚 Answer from the PyLearn knowledge base")
    elif src == "ai":
        who = "Groq" if res.get("llm") == "groq" else "Ollama"
        st.markdown(f"#### 🤖 AI answer ({who})")
    elif src == "offtopic":
        st.warning("That doesn't look like a Python question. Try asking about a Python concept, "
                   "for example *“What is a list?”*")
    else:
        st.markdown("#### 🔍 I couldn't find an exact answer")
        st.info(
            "That question isn't in the lessons yet. Add a free **Groq API key** in "
            "**AI Settings** (sidebar) and I can answer any Python question."
            + (" Meanwhile, these lessons are the closest match:" if res["refs"] else "")
        )
    if src in ("kb", "ai"):
        if res.get("learn"):
            render_learn(res["learn"])          # the same L.E.A.R.N. cards as the lessons
        else:
            st.markdown(res["answer"])
    if res["refs"]:
        st.markdown("**📖 Related lessons**")
        cols = st.columns(len(res["refs"]))
        for col, mid in zip(cols, res["refs"]):
            m = TOPIC_MAP[mid]
            if col.button(f"{m['icon']} {m['title']}", key=f"rel_{key}_{mid}",
                          use_container_width=True):
                go_to_topic(mid)
    if src == "ai":
        if st.button("📘 Teach me this as a full lesson", key=f"teach_{key}",
                     use_container_width=True):
            st.session_state["topic_pending"] = res["question"]
            st.session_state.page = "topics"
            st.rerun()

# ═════════════════════════════════════════════════════════════════════════════
#  NEW PAGES: Home (ask-first), Ask PyLearn, Learn Any Topic
# ═════════════════════════════════════════════════════════════════════════════
# After login, land on Home (once per login)
if not st.session_state.logged_in:
    st.session_state["_landed"] = False
elif st.session_state.page == "dashboard" and not st.session_state.get("_landed"):
    st.session_state["_landed"] = True
    st.session_state.page = "home"
    st.rerun()

# Navigation buttons for the new pages (moved to the top of the sidebar with CSS)
if st.session_state.logged_in:
    st.markdown("<style>.st-key-pl_nav { order: -1; }</style>", unsafe_allow_html=True)
    with st.sidebar:
        with st.container(key="pl_nav"):
            if st.button("🏠 Home", key="nav_home", use_container_width=True):
                st.session_state.page = "home"; st.rerun()
            if st.button("💬 Ask PyLearn", key="nav_ask", use_container_width=True):
                st.session_state.page = "ask"; st.rerun()
            if st.button("🎯 Learn Any Topic", key="nav_topics", use_container_width=True):
                st.session_state.page = "topics"; st.rerun()
            st.divider()

if st.session_state.logged_in and st.session_state.page == "home":
    progress = get_user_progress(st.session_state.username)
    done     = len(progress)

    st.markdown(f"## 👋 Hi {st.session_state.username}! What do you want to learn today?")
    st.markdown("Ask any Python question and PyLearn **finds the answer for you**.")

    ask_box("home", placeholder="e.g. What's the difference between a function and a class?")

    st.caption("Not sure what to ask? Try one of these:")
    examples = [
        "What's the difference between while and do-while loops?",
        "Why do I get a NameError?",
        "What's the difference between a list and a dictionary?",
        "What is recursion?",
    ]
    cols = st.columns(2)
    for i, ex in enumerate(examples):
        cols[i % 2].button(ex, key=f"home_ex_{i}", use_container_width=True,
                           on_click=_ask_example, args=("home", ex))

    st.markdown("---")
    c1, c2 = st.columns(2)
    if c1.button("🎯 Learn any topic", key="home_topics", use_container_width=True):
        st.session_state.page = "topics"; st.rerun()
    if c2.button("✏️ Free practice", key="home_practice", use_container_width=True):
        st.session_state.page = "practice"; st.rerun()

    # The learning dashboard stays closed until the student clicks it
    with st.expander(f"📚 Learning Dashboard — {done}/{TOTAL_MODULES} modules completed (click to open)",
                     expanded=False):
        st.progress(done / TOTAL_MODULES,
                    text=f"**{done} of {TOTAL_MODULES} modules completed**")
        render_module_list(progress, "homemod")

if st.session_state.logged_in and st.session_state.page == "ask":
    st.markdown("## 💬 Ask PyLearn")
    st.markdown("Ask any Python question and PyLearn **finds the answer for you** — "
                "no need to search through the lessons.")
    st.caption("It checks the lesson knowledge base first (instant), then asks the AI if needed.")

    st.markdown("**Try one of these:**")
    examples = [
        "What's the difference between a function and a class?",
        "What's the difference between while and do-while loops?",
        "Why do I get a NameError?",
        "What's the difference between a list and a dictionary?",
    ]
    cols = st.columns(2)
    for i, ex in enumerate(examples):
        cols[i % 2].button(ex, key=f"ask_ex_{i}", use_container_width=True,
                           on_click=_ask_example, args=("page", ex))
    ask_box("page")

if st.session_state.logged_in and st.session_state.page == "topics":
    st.markdown("## 🎯 Learn Any Topic")
    st.markdown("Choose **any** Python topic you want to learn, in any order. "
                "Type it below or pick one — PyLearn builds the lesson for you.")

    pending = st.session_state.pop("topic_pending", None)
    if pending:
        with st.spinner(f"Preparing a lesson on “{pending}”…"):
            resolve_topic(pending)

    with st.form("topic_form"):
        tq = st.text_input("What do you want to learn?", key="topic_q",
                           placeholder="e.g. recursion, tuples, lambda, list comprehensions…")
        go = st.form_submit_button("📘 Teach me", use_container_width=True)
    if go:
        if tq.strip():
            with st.spinner(f"Preparing a lesson on “{tq.strip()}”…"):
                resolve_topic(tq.strip())
        else:
            st.warning("Please type a topic first.")

    st.markdown("**✨ Popular topics beyond the core 15**")
    cols = st.columns(3)
    for i, t in enumerate(EXTRA_TOPICS):
        if cols[i % 3].button(f"{t['icon']} {t['title']}", key=f"pop_{t['id']}",
                              use_container_width=True):
            st.session_state["topic_view"] = {"kind": "known", "id": t["id"]}

    with st.expander("📚 Core curriculum — 15 lessons, open any one in any order"):
        cols = st.columns(3)
        for i, m in enumerate(MODULES):
            if cols[i % 3].button(f"{m['icon']} {m['title']}", key=f"core_{m['id']}",
                                  use_container_width=True):
                st.session_state["topic_view"] = {"kind": "known", "id": m["id"]}

    view = st.session_state.get("topic_view")
    if view:
        render_topic_view(view)
        st.markdown("---")
        st.markdown("**Questions about this topic?**")
        ask_box("topic")