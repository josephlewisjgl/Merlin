from statswalespy.search import statswales_search
from statswalespy.download_data import statswales_get_metadata, statswales_get_dataset
import random
from mouth.vocab import HELP_MENU, GREETINGS, GOODBYES
from brain.parsing import preprocess


class MerlinBot():

    EXIT_COMMANDS = ("quit", "goodbye", "exit", "no")

    # output_message prints Merlin's response
    def output_message(self, message):
        print("Merlin: " + str(message))

    # take_response is the function containing Merlin's response logic
    def take_response(self):
        self.output_message(random.choice(GREETINGS))
        response = preprocess(input("Response: ").lower())

        while not self.exit_func(response):
            if response == 'help':
                self.output_message(HELP_MENU)
                response = preprocess(input("Response: ").lower())

            elif response.startswith('search'):
                search_terms = response.split(' ')[1:]
                self.search(search_terms)
                response = preprocess(input("Response: ").lower())

            elif response.startswith('describe'):
                self.describe(response[9:])
                response = preprocess(input("Response: ").lower())

            elif response.startswith('download'):
                self.download_data(response[9:])
                response = preprocess(input("Response: ").lower())

            elif response.startswith('get data for'):
                self.get_data(response[13:])
                response = preprocess(input("Response: ").lower())

            else:
                self.output_message("Sorry I'm not sure what you need. Could you please try asking again or refer to the "
                                    "help menu for more options by typing 'help'.")
                response = preprocess(input("Response: ").lower())

    # exit function
    def exit_func(self, user_message):
        for command in self.EXIT_COMMANDS:
            if command in user_message:
                self.output_message(random.choice(GOODBYES))
                return True

    # search function to access the SW API and search based on the search term and iterate results
    def search(self, search_text):
        results = statswales_search(search_text)
        cubes = results[['Description_ENG', 'Dataset']]
        for index, row in cubes.iterrows():
            self.output_message("Cube name: " + row['Description_ENG'] + "| Cube ID: " + row['Dataset'] + "\n")
        self.output_message("Total cubes: " + str(cubes.Dataset.count()))

        return None

    # general conversation


    # data questions
    def describe(self, cube):
        # set up variables as blank if no response from API
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

        # check if there is a description of value if not use keywords
        if len(desc_check) > 5:
            self.output_message('The cube ' + str(title) + ' was last updated on ' + str(
                last_update) + '. \nIt holds information on ' + desc + '.')

        else:
            self.output_message('The cube ' + str(title) + ' was last updated on ' + str(
                last_update) + '. \n Here are some keywords to describe it: ' + str(keywords))

        return None

    def download_data(self, cube):
        df = statswales_get_dataset(cube)
        self.output_message('Downloading the data for: ' + cube)
        path = input('Where should I save this file? Please enter the file path: ')
        file = path+cube+'.csv'
        print(file)
        df.to_csv(file)

        return None

    def get_data(self, cube):
        df = statswales_get_dataset(cube)

        # set up number of dimensions to be incremented and the col_output_input dict to store the names of the col
        # and the name to output as a user friendly name
        num_dimensions = 0
        col_output_input = {}

        self.output_message('Dimensions for this cube are:')

        for col in df:
            if 'ItemName_ENG' in col:

                user_friendly_col = col.split('_')[0]
                col_output_input[user_friendly_col]= col
                self.output_message(user_friendly_col)
                num_dimensions += 1

        self.output_message('Now we can start filtering. You can filter up to three dimensions. Please just enter one filter on each dimension for now.')
        first = input('Select the first dimension you would like to filter: ')
        dimension = col_output_input.get(first)
        self.output_message('You have chosen to filter: ' + first + 'How would you like to filter this dimension, the options are below: ')
        filter_options = df.groupby(dimension).count().reset_index()[dimension].to_list()
        for option in filter_options:
            self.output_message(option)
        filter = input('What would you like to filter this column to?')
        df = df[df[dimension] == filter]


        if num_dimensions > 1:
            second = input('Select the second dimension you would like to filter (type no to filter by only one dimension): ')
            if second != 'no':
                dimension = col_output_input.get(second)
                self.output_message(
                    'You have chosen to filter: ' + first + 'How would you like to filter this dimension, the options are below: ')
                filter_options = df.groupby(dimension).count().reset_index()[dimension].to_list()
                for option in filter_options:
                    self.output_message(option)
                filter = input('What would you like to filter this column to?')
                df = df[df[dimension] == filter]

        if num_dimensions > 2:
            third = input('Select the third dimension you would like to filter (type no to filter by only two dimensions): ')
            if third != 'no':
                dimension = col_output_input.get(third)
                self.output_message(
                    'You have chosen to filter: ' + first + 'How would you like to filter this dimension, the options are below: ')
                filter_options = df.groupby(dimension).count().reset_index()[dimension].to_list()
                for option in filter_options:
                    self.output_message(option)
                filter = input('What would you like to filter this column to?')
                df = df[df[dimension] == filter]

        self.output_message('The data you requested is: ' + str(df.Data.sum()))

        return None

if __name__ == '__main__':
    merlin = MerlinBot()


    merlin.take_response()
