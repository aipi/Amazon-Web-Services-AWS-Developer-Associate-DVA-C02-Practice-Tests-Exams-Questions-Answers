import random
import google.generativeai as genai
import os

os.environ["GRPC_VERBOSITY"] = "ERROR"
os.environ["GLOG_minloglevel"] = "2"

errors_file_path = "README.md"


def log_failed_answer_formatted(question, options, correct_answers):
    options_str = '\n'.join(
        option.replace('- [ ]', '- [x]') if index + 1 in correct_answers else option
        for index, option in enumerate(options)
    )
    
    formatted_entry = (
        f"\n### {question}\n\n"
        f"{options_str}\n"
    )
    
    with open(errors_file_path, "a", encoding="utf-8") as file:
        file.write(formatted_entry)


def read_questions_from_file(path):
    with open(path, "r", encoding="utf-8") as file:
        content = file.read()
    questions = content.split("###")
    formatted_questions = []
    
    for question in questions[1:]:
        lines = question.strip().split("\n")
        question_text = lines[0].strip()
        options = [line.strip().replace("[x]", "[ ]").strip() for line in lines[2:] if line.startswith("-")]
        correct_answers = [i + 1 for i, line in enumerate(lines[2:]) if "[x]" in line]
        formatted_questions.append((question_text, options, correct_answers))
    
    return formatted_questions

def filter_questions_by_keyword(questions, keyword):
    keyword = keyword.lower()
    return [
        (q[0], q[1], q[2])
        for q in questions
        if keyword in q[0].lower() or
           any(keyword in option.lower() for option in q[1])
    ]

def display_question(index, question, options):
    print(f"\nQuestion {index}: {question}\n")
    for i, option in enumerate(options, start=1):
        print(f"{i}. {option}")

def select_options(options):
    print("\nEnter the number(s) of the correct option(s), separated by commas:")
    selection = input().split(",")
    return [int(option.strip()) for option in selection if option.strip().isdigit()]

def calculate_score(user_answers, correct_answers):
    return set(user_answers) == set(correct_answers)

def get_explanation(question_text,options, correct_answers):
    prompt = (
        f"Explain briefly why the correct answer(s) to this question are: {correct_answers}. "
        f"The question is: {question_text} {options}"
    )
    genai.configure(api_key=os.environ["GEMINI_API_KEY"])
    model = genai.GenerativeModel("gemini-1.5-flash")
    response = model.generate_content(prompt)
    print(f"\n💬 Explanation: {response.text}")

def main():
    file_path = "errors.md"
    questions = read_questions_from_file(file_path)
    
    total_questions = len(questions)
    print(f"The file contains {total_questions} available questions.")
    
    print("\nDo you want to filter questions by a keyword? (y/n)")
    filter_choice = input().strip().lower()
    
    if filter_choice == "y":
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
            log_failed_answer_formatted(question, options, correct_answers)
        print("\n🤖 Do you want IA explanation? (y/n)")
        filter_choice = input().strip().lower()
        if filter_choice == 'y':
            get_explanation(question, options, correct_answers)
                

        print(f"\n{question_index}/{num_questions}")
        question_index += 1
    
    print(f"\nQuiz finished! You got {score} out of {num_questions} questions correct. Total: {score * 100/num_questions}%")

if __name__ == "__main__":
    main()
