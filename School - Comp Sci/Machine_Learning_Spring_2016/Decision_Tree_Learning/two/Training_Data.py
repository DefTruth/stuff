import fileinput
import copy

class Training_Data:

    tokenized_data = []
    categories = {}

    def __init__(self):
        self.tokenized_data =self. get_tokenized_data()

    def get_tokenized_data(self):

        # if data has already been collected from file return it
        if self.tokenized_data != []:
            return self.tokenized_data
        # else collect the data from the file
        else:
            temp_tokenized_data = []
            data = fileinput.input()
            for line in data:
                tokens = line.split()
                temp_tokenized_data.append(tokens)
            return temp_tokenized_data

    def get_categories(self):
        assert self.categories != {}, 'error: categories have not been created from training data. call create_categories_from_training_data()'

        return self.categories

    def create_categories_from_training_data(self):

        categories = {}

        # last column before the class column
        last_category_column = self.get_index_of_class_column()

        for i in range(1, last_category_column):
            current_category = self.create_category_tuple_from_column(i)
            name = current_category[0]
            attribute_dictionary = current_category[1]
            categories[name] = attribute_dictionary

        return categories

    def create_category_tuple_from_column(self, index):

        # the name of the category
        category_name = self.get_category_name_from_column(index)

        # for every every unique attribute in this column, create a dictionary with a dictionary inside of
        # if containing all the unique class types and their counts set to zero
        # what this data structure is essentially saying is that this category has these attributes, and
        # they have not been classified as any type any number of times
        # so their count is of course initialized to zero
        attribute_dictionary = self.create_attribute_dictionary_from_column(index)

        return (category_name, attribute_dictionary)

    def create_attribute_dictionary_from_column(self, index):
        attribute_dictionary = {}
        for unique_attribute_name in self.get_unique_attribute_names_from_column(index):
            attribute_dictionary[unique_attribute_name] = {'n' : 0, 'y' : 0}
        return attribute_dictionary

    def get_category_name_from_column(self, index):
        column = self.get_column(index)
        return copy.deepcopy(column[0])

    # this is a classification problem, so this function will mine from the training data, the set of types
    # any training instance can be classified as
    def get_set_of_unique_class_types(self):
        last_column = self.get_index_of_class_column()
        return self.get_unique_attribute_names_from_column(last_column)

    def get_number_of_training_examples_of_class_type(self, type):
        num_of_specified_type = 0
        class_values = self.get_class_values_for_training_set()
        for value in class_values:
            if value == type:
                num_of_specified_type += 1
        return num_of_specified_type

    def get_proportion_to_class_type_for_training_set_dictionary(self):
        class_types = self.get_set_of_unique_class_types()

        proportion_to_class_type_for_training_set = {}
        for type in class_types:
            num_of_type = self.get_number_of_training_examples_of_class_type(type)
            proportion_to_class_type_for_training_set[type] = num_of_type
        return proportion_to_class_type_for_training_set

    # note: this is referring to the actual column data, not just the attribute data.
    # the data is still pretty raw when this function is called
    def get_unique_attribute_names_from_column(self, index):

        column = copy.deepcopy(self.get_column(index))

        #delete the category name from this data column
        del column[0]

        # add all names not seen before to the list of attr names
        # note: attribute names cannot be the same as a category name
        known_attribute_names = []
        for item in column:
            if item not  in known_attribute_names and item not in self.get_category_names():
                known_attribute_names.append(item)

        return known_attribute_names

    def get_category_names(self):
        temp_row = copy.deepcopy(self.get_row(0))
        del temp_row[0]
        del temp_row[-1]
        return temp_row

    def get_class_values_for_training_set(self):
        class_column = copy.deepcopy(self.get_column(self.get_index_of_class_column()))
        del class_column[0]
        return class_column

    def get_counter_name(self):
        temp_row = copy.deepcopy(self.get_row(0))
        return temp_row[0]

    def get_class_name(self):
        temp_row = copy.deepcopy(self.get_row(0))
        return temp_row[-1]

    def get_row(self, index):
        return self.tokenized_data[index]

    def get_column(self, index):
        temp_column = []
        for row in self.tokenized_data:
            temp_column.append(row[index])
        return temp_column

    def get_index_of_class_column(self):
        return len(self.tokenized_data[0]) - 1