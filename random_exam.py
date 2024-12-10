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
        correct_answers = [i + 1 for i, line in enumerate(lines[2:]) if "[x]" in line]  # Ajusta índice das respostas
        formatted_questions.append((question_text, options, correct_answers))
    
    return formatted_questions

def filter_questions_by_keyword(questions, keyword):
    keyword = keyword.lower()
    return [
        (q[0], q[1], q[2])  # Mantém formato das perguntas
        for q in questions
        if keyword in q[0].lower() or  # Verifica no enunciado
           any(keyword in option.lower() for option in q[1])  # Verifica nas opções
    ]

def display_question(index, question, options):
    print(f"\nQuestion {index}: {question}\n")
    for i, option in enumerate(options, start=1):  # Exibe opções numeradas
        print(f"{i}. {option}")

def select_options(options):
    print("\nEnter the number(s) of the correct option(s), separated by commas:")
    selection = input().split(",")
    return [int(option.strip()) for option in selection if option.strip().isdigit()]

def calculate_score(user_answers, correct_answers):
    return set(user_answers) == set(correct_answers)

def main():
    file_path = "README.md"  # Nome do arquivo contendo as questões
    questions = read_questions_from_file(file_path)
    
    total_questions = len(questions)
    print(f"The file contains {total_questions} available questions.")
    
    print("\nDo you want to filter questions by a keyword? (yes/no)")
    filter_choice = input().strip().lower()
    
    if filter_choice == "yes":
        keyword = input("Enter the keyword to filter questions: ").strip()
        filtered_questions = filter_questions_by_keyword(questions, keyword)
        total_filtered = len(filtered_questions)
        print(f"\nFound {total_filtered} question(s) containing the keyword '{keyword}'.")
        if total_filtered == 0:
            print("No questions match the keyword. Exiting.")
            return
        questions = filtered_questions
    
    while True:
        try:
            num_questions = int(input(f"How many questions would you like to answer? (1-{len(questions)}): "))
            if 1 <= num_questions <= len(questions):
                break
            print(f"Please choose a number between 1 and {len(questions)}.")
        except ValueError:
            print("Invalid input. Please enter an integer.")
    
    selected_questions = random.sample(range(len(questions)), num_questions)
    score = 0
    question_index = 1
    for index in selected_questions:
        question, options, correct_answers = questions[index]
        display_question(question_index, question, options)
        
        user_answers = select_options(options)
        is_correct = calculate_score(user_answers, correct_answers)
        
        if is_correct:
            print("\n✅ Correct answer!")
            score += 1
        else:
            print("\n❌ Wrong answer!")
            print(f"The correct answer(s): {', '.join(map(str, correct_answers))}")

        print(f"\n{question_index}/{num_questions}")
        question_index += 1
    
    print(f"\nQuiz finished! You got {score} out of {num_questions} questions correct. Total: {score * 100/num_questions}%")

if __name__ == "__main__":
    main()
