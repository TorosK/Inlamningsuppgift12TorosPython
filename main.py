import random

def get_integer_input(prompt, min_value, max_value):
    while True:
        try:
            value = int(input(prompt))
            if min_value <= value <= max_value:
                return value
            else:
                print(f"Värdet måste vara mellan {min_value} och {max_value}.")
        except ValueError:
            print("Ogiltig inmatning. Ange ett heltal.")

def generate_question(operation, table_or_divisor):
    factor_or_dividend = random.randint(1, 12)
    if operation == '*':
        return f"{factor_or_dividend} * {table_or_divisor}", factor_or_dividend * table_or_divisor
    elif operation == '/':
        return f"{factor_or_dividend * table_or_divisor} // {table_or_divisor}", factor_or_dividend
    elif operation == '%':
        return f"{factor_or_dividend} % {table_or_divisor}", factor_or_dividend % table_or_divisor

while True:
    num_questions = get_integer_input("Välj antal frågor (12 - 39): ", 12, 39)
    operation = input("Välj räknesätt (*, /, %, slump): ")

    if operation not in ['*', '/', '%', 'slump']:
        print("Ogiltigt räknesätt valt. Försök igen.")
        continue

    if operation == '*':
        table_or_divisor = get_integer_input("Välj en tabell (2-12): ", 2, 12)
    elif operation in ['/', '%']:
        table_or_divisor = get_integer_input("Välj en divisor (2-5): ", 2, 5)

    questions_asked = 0
    correct_answers = 0
    used_questions = {}

    while questions_asked < num_questions:
        
        # Här slumpar vi räknesätt och table_or_divisor för varje fråga om räknesättet är 'slump'
        if operation == 'slump':
            current_operation = random.choice(['*', '/', '%'])
            current_table_or_divisor = random.randint(2, 12 if current_operation == '*' else 5)
        else:
            current_operation = operation
            current_table_or_divisor = table_or_divisor

        question, answer = generate_question(current_operation, current_table_or_divisor)

        max_occurrences = 1
        if 14 <= num_questions <= 26:
            max_occurrences = 2
        elif 27 <= num_questions <= 39:
            max_occurrences = 3

        if question in used_questions and used_questions[question] >= max_occurrences:
            continue

        user_answer = get_integer_input(f"Fråga {questions_asked + 1}: {question} = ", 0, 1000)

        if user_answer == answer:
            correct_answers += 1
            print(f"Korrekt! Du har {correct_answers} korrekta svar.")
        else:
            print(f"Fel svar. Du förlorade. Rätt svar var {answer}.")
            break

        used_questions[question] = used_questions.get(question, 0) + 1
        questions_asked += 1

        if questions_asked == num_questions:
            print("Grattis! Du har vunnit!")
            break

    play_again = input("Vill du spela igen? (ja/nej): ").lower()
    if play_again != 'ja':
        break
