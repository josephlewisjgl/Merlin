import re
from collections import Counter
import spacy
from nltk import pos_tag
from nltk.tokenize import word_tokenize
from nltk.corpus import stopwords
from ears.comparison_phrases import COMMANDS
import regex

word2vec = spacy.load('en_core_web_sm')


stop_words = set(stopwords.words("english"))


def preprocess(input_sentence):
    input_sentence = input_sentence.lower()
    input_sentence = re.sub(r'[^\w\s]', '', input_sentence)
    tokens = word_tokenize(input_sentence)
    input_sentence = [i for i in tokens if not i in stop_words]
    return input_sentence


def compare_overlap(user_message, possible_response):
    similar_words = 0
    for token in user_message:
        if token in possible_response:
            similar_words += 1
    return similar_words

def highest_score(command_scores):
    scores = list(command_scores.values())
    commands = list(command_scores.keys())
    return commands[scores.index(max(scores))]

def find_intent(response):
    scores = {}
    for command in COMMANDS:
        score = compare_overlap(response, command)
        scores[command] = score
    chosen_command = highest_score(scores)
    print(scores)
    print(chosen_command)
    return chosen_command[0]

def extract_nouns(tagged_message):
    message_nouns = list()
    for token in tagged_message:
        if token[1].startswith("N"):
            message_nouns.append(token[0])
    return message_nouns


def compute_similarity(tokens, category):
    output_list = list()
    for token in tokens:
        output_list.append([token.text, category.text, token.similarity(category)])
    return output_list

def find_cube_ref(response):
    cube_regex = re.compile('[a-zA-z]{4}[0-9]{4}')
    matches = []
    for token in response:
        matches.append(re.findall(cube_regex, token))

    cubes = []

    for cube in matches:
        if len(cube)>0:
            cubes.append(cube)

    return cubes

