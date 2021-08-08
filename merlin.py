from statswalespy.search import statswales_search
from statswalespy.download_data import statswales_get_metadata
import random
import pandas as pd


class MerlinBot():
    # CONVERSATION
    HELP_TEXT = "Type help to find out what I can do! Type exit to close me."

    HELP_MENU = "I can do lots of cool stuff: \n 1. Type search and one or more key word(s) and I can find a data " \
                "source for your query." \

    GREETINGS = [
        "Hello there! My name is MerlinBot and I'm here to help. " + HELP_TEXT,
        "What's up my name is MerlinBot did you have any questions? " + HELP_TEXT,
        "Nice to meet you I am MerlinBot how can I help you today? " + HELP_TEXT
    ]

    # output_message prints Merlin's response
    def output_message(self, message):
        print("Merlin: " + str(message))

    # take_response is the function containing Merlin's response logic
    def take_response(self):
        response = input("Response: ").lower()
        if response == 'help':
            self.output_message(self.HELP_MENU)

        elif response.startswith('search'):
            search_terms = response.split(' ')[1:]
            self.search(search_terms)

        elif response == 'exit':
            self.output_message('Goodbye!')
            exit()

        elif response.startswith('describe'):
            self.describe(response[9:])

        else:
            self.output_message("Sorry I'm not sure what you need. Could you please try asking again or refer to the "
                                "help menu for more options by typing 'help'.")

    # search function to access the SW API and search based on the search term and iterate results
    def search(self, search_text):
        results = statswales_search(search_text)
        cubes = results[['Description_ENG', 'Dataset']]
        for index, row in cubes.iterrows():
            self.output_message("Cube name: " + row['Description_ENG'] + "| Cube ID: " + row['Dataset'] + "\n")
        self.output_message("Total cubes: " + str(cubes.Dataset.count()))

    # general conversation


    # data questions
    def describe(self, cube):

        title = ''
        last_update = ''
        desc = ''
        keywords = ''

        try:
            md = statswales_get_metadata(cube)
            title = md[(md['Tag_ENG'] == 'Title')]['Description_ENG'].reset_index()['Description_ENG'][0]
            last_update = md[(md['Tag_ENG'] == 'Last update')]['Description_ENG'].reset_index()['Description_ENG'][0]
            desc = md[(md['Tag_ENG'] == 'General description')]['Description_ENG'].reset_index()['Description_ENG'][0]
            keywords = md[(md['Tag_ENG'] == 'Keywords')]['Description_ENG'].reset_index()['Description_ENG'][0]

        except:
             self.output_message('Error finding cube description.')

        desc_check = desc.split(' ')

        if len(desc_check) > 5:
            self.output_message('The cube ' + str(title) + ' was last updated on ' + str(
                last_update) + '. \nIt holds information on ' + desc + '.')

        else:
            self.output_message('The cube ' + str(title) + ' was last updated on ' + str(
                last_update) + '. \n Here are some keywords to describe it: ' + str(keywords))

        return None

if __name__ == '__main__':
    merlin = MerlinBot()

    merlin.output_message(random.choice(merlin.GREETINGS))
    while True:
        merlin.take_response()
