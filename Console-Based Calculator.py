def calculate(command):
    parts = command.strip().split()

    if len(parts) == 0:
        return "⚠️ No command entered."

    operation = parts[0].lower()

    if operation == "exit":
        return "exit"

    if operation == "help":
        return """
Available Commands:
  add [num1] [num2]    → Add two numbers
  sub [num1] [num2]    → Subtract num2 from num1
  mul [num1] [num2]    → Multiply two numbers
  div [num1] [num2]    → Divide num1 by num2
  help                 → Show this help message
  exit                 → Exit the calculator
"""

    if len(parts) != 3:
        return "❌ Error: Please provide a command followed by two numbers."

    try:
        num1 = float(parts[1])
        num2 = float(parts[2])
    except ValueError:
        return "❌ Error: Invalid number format."

    if operation == "add":
        return f"✅ Result: {num1 + num2}"
    elif operation == "sub":
        return f"✅ Result: {num1 - num2}"
    elif operation == "mul":
        return f"✅ Result: {num1 * num2}"
    elif operation == "div":
        if num2 == 0:
            return "❌ Error: Division by zero."
        return f"✅ Result: {num1 / num2}"
    else:
        return "❓ Unknown command. Type 'help' to see available commands."


def main():
    print("=== Simple Command Calculator ===")
    print("Type 'help' to see available commands.\n")

    while True:
        user_input = input(">> ")
        result = calculate(user_input)
        if result == "exit":
            print("👋 Exiting. Goodbye!")
            break
        print(result)


if __name__ == "__main__":
    main()
