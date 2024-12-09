import random

def read_questions_from_file(path):
    with open(path, "r", encoding="utf-8") as file:
        content = file.read()
    questions = content.split("###")
    formatted_questions = []
    
    for question in questions[1:]:
        lines = question.strip().split("\n")
        question_text = lines[0].strip()
        options = [line.strip().replace("[x]", "[ ]").strip() for line in lines[2:] if line.startswith("-")]
        correct_answers = [i for i, line in enumerate(lines[2:], start=1) if "[x]" in line]  # Start indexing at 1
        formatted_questions.append((question_text, options, correct_answers))
    
    return formatted_questions

def display_question(question, options):
    print(f"\n{question}\n")
    for i, option in enumerate(options, start=1):  # Display options starting from 1
        print(f"{i}. {option}")

def select_options(options):
    print("\nEnter the number(s) of the correct option(s), separated by commas:")
    selection = input().split(",")
    return [int(option.strip()) for option in selection if option.strip().isdigit()]

def calculate_score(user_answers, correct_answers):
    return set(user_answers) == set(correct_answers)

def main():
    file_path = "README.md"
    questions = read_questions_from_file(file_path)
    
    total_questions = len(questions)
    print(f"The file contains {total_questions} available questions.")
    
    while True:
        try:
            num_questions = int(input("How many questions would you like to answer? "))
            if 1 <= num_questions <= total_questions:
                break
            print(f"Please choose a number between 1 and {total_questions}.")
        except ValueError:
            print("Invalid input. Please enter an integer.")
    
    selected_questions = random.sample(range(total_questions), num_questions)
    score = 0
    
    for index in selected_questions:
        question, options, correct_answers = questions[index]
        display_question(question, options)
        
        user_answers = select_options(options)
        is_correct = calculate_score(user_answers, correct_answers)
        
        if is_correct:
            print("\n✔️ Correct answer!")
            score += 1
        else:
            print("\n❌ Wrong answer!")
            print(f"The correct answer(s): {', '.join(map(str, correct_answers))}")
    
    print(f"\nQuiz finished! You got {score} out of {num_questions} questions correct.")

if __name__ == "__main__":
    main()
