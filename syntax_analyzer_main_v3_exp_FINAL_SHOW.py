import tkinter as tk
from tkinter import messagebox
import re
from enchant import Dict


KEYWORDS = [
    "auto", "break", "case", "char", "const", "continue", "default", "do",
    "double", "else", "enum", "extern", "float", "for", "goto", "if",
    "int", "long", "register", "return", "short", "signed", "sizeof", "static",
    "struct", "switch", "typedef", "union", "unsigned", "void", "volatile", "while",
    "cout", "cin", "endl"
]

# Initialize the spell checker
dictionary = Dict("en_US")

# Function to check for possible spelling mistakes in keywords
def check_spelling(keyword):
    if not dictionary.check(keyword):
        suggestions = dictionary.suggest(keyword)
        valid_suggestions = [suggestion for suggestion in suggestions if suggestion in KEYWORDS]
        return valid_suggestions
    return []

# Function to analyze syntax
def analyze_syntax():
    code = code_text.get("1.0", tk.END)
    syntax_errors, detected_keywords = [], []

    # Remove comments from code
    code = re.sub(r"//.*$", "", code, flags=re.MULTILINE)
    code = re.sub(r"/\.?\*/", "", code, flags=re.DOTALL)

    # Split code into lines
    lines = code.split("\n")

    # Track the number of open and closing braces
    open_braces = 0
    closing_braces = 0

    # Analyze each line
    for i, line in enumerate(lines):
        line_number = i + 1

        # Remove leading/trailing whitespaces
        line = line.strip()

        # Check for empty line or comment
        if not line or line.startswith("//"):
            continue

        # Check for semicolon at the end
        if not line.endswith(";") and "{" not in line and "}" not in line and not line.endswith(")") and not line.startswith("#include"):
            syntax_errors.append(f"Missing semicolon at line {line_number}")

        # Check for correct closing of braces
        open_braces += line.count("{")
        closing_braces += line.count("}")

        # Check for function declaration
        if "(" in line and ")" in line and "{" in line and not line.endswith(")"):
            function_name = line[:line.index("(")].strip()
            detected_keywords.append(function_name)

        # Check for keywords and spelling errors
        words = re.findall(r"\b\w+\b", line)
        for word in words:
            if word in KEYWORDS:
                detected_keywords.append(word)
            else:
                suggestions = check_spelling(word)
                if suggestions:
                    detected_keywords.extend(suggestions)

    # Check for incorrect usage of C++ keywords
    incorrect_keywords = set(detected_keywords) - set(KEYWORDS)

    # Check for missing closing braces
    if open_braces > closing_braces:
        syntax_errors.append("Missing closing brace")

    # Display syntax errors and detected keywords
    output_text.config(state=tk.NORMAL)
    output_text.delete("1.0", tk.END)

    if syntax_errors:
        output_text.insert(tk.END, "Syntax errors:\n", "syntax_error")
        for error in syntax_errors:
            output_text.insert(tk.END, f"- {error}\n", "syntax_error")
    else:
        output_text.insert(tk.END, "No syntax errors found\n", "no_error")

    output_text.insert(tk.END, "\nDetected keywords:\n")
    for keyword in detected_keywords:
        if keyword in KEYWORDS:
            output_text.insert(tk.END, f"- {keyword}\n", "keyword")
        else:
            output_text.insert(tk.END, f"- {keyword}\n", "misspelled_keyword")

    # Configure tags for text formatting
    output_text.tag_config("syntax_error", foreground="red")
    output_text.tag_config("keyword", foreground="green")
    output_text.tag_config("misspelled_keyword", foreground="blue")
    output_text.tag_config("no_error", foreground="green")

    # Disable text editing in the output text area
    output_text.config(state=tk.DISABLED)

# Create the main window
window = tk.Tk()
window.title("C++ Syntax Analyzer")
window.geometry("800x600")

# Set the window background color to grey
window.config(bg="#e0e0e0")

# Create a frame for the blue bar
blue_bar_frame = tk.Frame(window, bg="#2196f3", height=60)
blue_bar_frame.pack(fill=tk.X)

# Create a label for the blue bar
blue_bar_label = tk.Label(blue_bar_frame, text="C++ Syntax Analyzer", font=("Arial", 18), fg="white", bg="#2196f3")
blue_bar_label.pack(pady=10)

# Create a label for code input
code_label = tk.Label(window, text="Enter C++ code:", font=("Arial", 14), bg="#e0e0e0")
code_label.pack(pady=10)

# Create a text area for code input
code_text = tk.Text(window, height=10, font=("Arial", 12))
code_text.pack()

# Create a button to analyze syntax
analyze_button = tk.Button(window, text="Analyze Syntax", font=("Arial", 14), command=analyze_syntax)
analyze_button.pack(pady=10)

# Create a label for output
output_label = tk.Label(window, text="Syntax Analysis:", font=("Arial", 14), bg="#e0e0e0")
output_label.pack(pady=10)

# Create a text area for output
output_text = tk.Text(window, height=10, font=("Arial", 12), state=tk.DISABLED)
output_text.pack()

# Create a messagebox intro
messagebox.showinfo("C++ Syntax Analyzer", "Welcome to the C++ Syntax Analyzer!\n\nThis program analyzes the syntax of C++ code and identifies any potential errors or misspelled keywords.\n\nTo use the analyzer, enter your C++ code in the text area and click the 'Analyze Syntax' button.\n\nThe program will display any syntax errors and highlight the detected keywords.\n\nEnjoy analyzing your C++ code!")

# Run the main event loop
window.mainloop()

