from statswalespy.search import statswales_search
import random
import pandas as pd


class MerlinBot():
    # CONVERSATION
    HELP_TEXT = "Type help to find out what I can do! Type exit to close me."

    HELP_MENU = "I can do lots of cool stuff: \n 1. Type search and a key word and I can find a data source for your query."

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
            self.search(response[7:])

        elif response == 'exit':
            self.output_message('Goodbye!')
            exit()

        else:
            self.output_message("Sorry I'm not sure what you need. Could you please try asking again or refer to the help menu for more options by typing 'help'.")

    # search function to access the SW API and search based on the search term and iterate results
    def search(self, search_text):
        results = statswales_search(search_text)
        cubes = results[['Description_ENG', 'Dataset']]
        for index, row in cubes.iterrows():
            self.output_message("Cube name: " + row['Description_ENG'] + "| Cube ID: " + row['Dataset'] + "\n")
        self.output_message("Total cubes: " + str(cubes.Dataset.count()))

    # general conversation


    # data questions

if __name__ == '__main__':
    merlin = MerlinBot()

    merlin.output_message(random.choice(merlin.GREETINGS))
    while True:
        merlin.take_response()
