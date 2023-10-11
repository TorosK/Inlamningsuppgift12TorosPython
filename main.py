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
    else:
        return None

def choose_door(num_doors):
    zombie_door = random.randint(1, num_doors)
    user_choice = get_integer_input(f"Välj en dörr (1-{num_doors}): ", 1, num_doors)
    if user_choice == zombie_door:
        print(f"Du förlorade. Zombiesarna var bakom dörr {zombie_door}.")
        return False
    else:
        print(f"Säker! Zombiesarna var bakom dörr {zombie_door}.")
        return True

while True:
    num_questions = get_integer_input("Välj antal frågor (12 - 39): ", 12, 39)
    operation = input("Välj räknesätt (*, /, %, slump): ")

    if operation != 'slump':
        if operation == '*':
            table_or_divisor = get_integer_input("Välj en tabell (2-12): ", 2, 12)
        elif operation in ['/', '%']:
            table_or_divisor = get_integer_input("Välj en divisor (2-5): ", 2, 5)

    questions_asked = 0
    correct_answers = 0

    while questions_asked < num_questions:
        current_operation = operation if operation != 'slump' else random.choice(['*', '/', '%'])
        current_table_or_divisor = random.randint(2, 12 if current_operation == '*' else 5) if operation == 'slump' else table_or_divisor

        question, answer = generate_question(current_operation, current_table_or_divisor)

        if question is None:
            continue

        user_answer = get_integer_input(f"Fråga {questions_asked + 1}: {question} = ", 0, 1000)

        if user_answer == answer:
            print(f"Korrekt! Du har {correct_answers + 1} korrekta svar.")
            if questions_asked < num_questions - 1:
                if not choose_door(num_questions - questions_asked):
                    break
            correct_answers += 1
        else:
            print(f"Fel svar. Du förlorade. Rätt svar var {answer}.")
            break

        questions_asked += 1

        if questions_asked == num_questions:
            print("Grattis! Du har vunnit!")
            break

    play_again = input("Vill du spela igen? (ja/nej): ").lower()
    if play_again != 'ja':
        break
