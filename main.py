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

def get_operation_input(prompt, valid_operations):
    while True:
        operation = input(prompt)
        if operation in valid_operations:
            return operation
        else:
            print("Ogiltigt räknesätt valt. Försök igen.")

def generate_question(operation, table_or_divisor):
    if operation not in ['*', '/', '%']:
        raise ValueError("Invalid operation")

    factor_or_dividend = random.randint(1, 12)
    if operation == '*':
        return f"{factor_or_dividend} * {table_or_divisor}", factor_or_dividend * table_or_divisor
    elif operation == '/':
        return f"{factor_or_dividend * table_or_divisor} // {table_or_divisor}", factor_or_dividend
    elif operation == '%':
        return f"{factor_or_dividend} % {table_or_divisor}", factor_or_dividend % table_or_divisor

def choose_door(num_doors):
    zombie_door = random.randint(1, num_doors)
    user_choice = get_integer_input(f"Välj en dörr (1-{num_doors}): ", 1, num_doors)
    if user_choice == zombie_door:
        print(f"Du förlorade. Zombiesarna var bakom dörr {zombie_door}.")
        return False
    else:
        print(f"Säker! Zombiesarna var bakom dörr {zombie_door}.")
        return True

def setup_game_conditions(won_last_game, previous_conditions):
    if won_last_game or previous_conditions['num_questions'] is None:
        num_questions = get_integer_input("Välj antal frågor (12 - 39): ", 12, 39)
        operation = get_operation_input("Välj räknesätt (*, /, %, slump): ", ['*', '/', '%', 'slump'])
    else:
        num_questions = previous_conditions['num_questions']
        operation = previous_conditions['operation']

    if operation != 'slump':
        if won_last_game or previous_conditions['table_or_divisor'] is None:
            if operation == '*':
                table_or_divisor = get_integer_input("Välj en tabell (2 - 12): ", 2, 12)
            elif operation in ['/', '%']:
                table_or_divisor = get_integer_input("Välj en divisor (2 - 5): ", 2, 5)
        else:
            table_or_divisor = previous_conditions['table_or_divisor']
    else:
        table_or_divisor = None

    return num_questions, operation, table_or_divisor

# Initialize game variables
previous_conditions = {'num_questions': None, 'operation': None, 'table_or_divisor': None}
user_won_last_game = False

continue_game = True
while continue_game:
    correct_answers = 0
    questions_asked = 0
    asked_questions = {}

    num_questions, operation, table_or_divisor = setup_game_conditions(user_won_last_game, previous_conditions)

    previous_conditions['num_questions'] = num_questions
    previous_conditions['operation'] = operation
    previous_conditions['table_or_divisor'] = table_or_divisor

    user_won_last_game = False  # Reset flag

    while questions_asked < num_questions:
        # Inre loop för att hantera varje fråga
        question_loop = True
        while question_loop:
            current_operation = operation if operation != 'slump' else random.choice(['*', '/', '%'])
            current_table_or_divisor = random.randint(2, 12 if current_operation == '*' else 5) if operation == 'slump' else table_or_divisor
            
            try:
                question, answer = generate_question(current_operation, current_table_or_divisor)
            except ValueError:
                print("Invalid operation, please restart the game.")
                break

            times_asked = asked_questions.get(question, 0)

            if num_questions <= 13 and times_asked == 0:
                break
            elif 14 <= num_questions <= 26 and times_asked < 2:
                break
            elif 27 <= num_questions <= 39 and times_asked < 3:
                break

        asked_questions[question] = asked_questions.get(question, 0) + 1

        print(f"Du har besvarat {questions_asked} frågor korrekt av {num_questions} möjliga.")

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

        print(f"Du har nu {correct_answers} korrekta svar och {num_questions - questions_asked} frågor kvar.")

        if questions_asked == num_questions:
            print("Grattis! Du har vunnit!")
            user_won_last_game = True

    play_again = input("Vill du spela igen? (ja/nej): ").lower()
    if play_again != 'ja':
        continue_game = False