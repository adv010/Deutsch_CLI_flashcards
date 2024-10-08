import pandas as pd
import random
import numpy as np
import time
import sys

def load_vocabulary(filepath):
    """Loads the vocabulary from an Excel file and fills missing example sentences."""
    vocabulary = pd.read_excel(filepath, index_col=None)
    if vocabulary['Example_Sentence'].isnull().any():
        vocabulary['Example_Sentence'] = vocabulary['Example_Sentence'].ffill()
    return vocabulary

def get_random_options(vocabulary, correct_index, column_name, num_options=3):
    """Gets random options for the flashcard, excluding the correct answer."""
    indices = np.setdiff1d(np.arange(len(vocabulary)), correct_index)  # Exclude correct answer
    sampled_indices = np.random.choice(indices, size=num_options, replace=False)
    options = list(vocabulary.iloc[sampled_indices][column_name])
    return options

def display_mcq(question, correct_answer, options):
    """Displays the multiple choice question and evaluates the answer."""
    print(question)
    for idx, option in enumerate(options):
        print(f"({idx+1}) {option}")
    
    answer = int(input("Enter the correct option (1/2/3/4): "))
    
    if options[answer - 1] == correct_answer:
        print("That is correct!")
    else:
        print(f"Sorry, the correct answer is {correct_answer}")

def show_example_sentence(row):
    """Displays an example sentence and optionally its translation."""
    print(f"Example sentence: {row['Example_Sentence']}")
    if pd.notnull(row['Example_Sentence_Translation']):
        show_translation = input("Would you like to see the translation? (yes/no): ").lower()
        if show_translation == 'yes':
            print(row['Example_Sentence_Translation'])
    print("-" * 50)

def ask_german_mcq(vocabulary, row, index):
    """Ask the user to match the German word to its English translation."""
    german_word = str(row['German']).replace("\n", "/ ")
    correct_answer = str(row['English']).replace("\n", "/ ")
    
    options = get_random_options(vocabulary, index, 'English')
    options.append(correct_answer)
    random.shuffle(options)
    
    question = f"What is the meaning of {german_word}?"
    display_mcq(question, correct_answer, options)

def ask_english_mcq(vocabulary, row, index):
    """Ask the user to match the English word to its German translation."""
    english_word = str(row['English']).replace("\n", "/ ")
    correct_answer = str(row['German']).replace("\n", "/ ")
    
    options = get_random_options(vocabulary, index, 'German')
    options.append(correct_answer)
    random.shuffle(options)
    
    question = f"What is the German word for {english_word}?"
    display_mcq(question, correct_answer, options)

def present_flashcard(vocabulary, question_type):
    """Presents a flashcard in the form of a multiple-choice question."""
    index = random.randint(0, len(vocabulary) - 1)
    row = vocabulary.iloc[index]
    
    if question_type == 'german_mcq':
        ask_german_mcq(vocabulary, row, index)
    elif question_type == 'english_mcq':
        ask_english_mcq(vocabulary, row, index)

    show_example_sentence(row)

def start_flashcards(vocabulary):
    """Runs the flashcard session."""
    question_types = ['german_mcq', 'english_mcq']
    
    try:
        while True:
            question_type = random.choice(question_types)
            present_flashcard(vocabulary, question_type)
            time.sleep(2)  # Add delay between questions
    except KeyboardInterrupt:
        print("\n\n***** THANKS FOR PLAYING! ******")
        sys.exit(0)

if __name__ == "__main__":
    filepath = "./Vocabular.xlsx"
    vocabulary_df = load_vocabulary(filepath)
    start_flashcards(vocabulary_df)
