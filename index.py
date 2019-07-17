import re
import os
import collections
import time
import math
import sys
#import other modules as needed

class Index:
    def __init__(self, path):
        self.path = path

    def buildIndex(self):
        #function to read documents from collection, tokenize and build the index with tokens
		# implement additional functionality to support methods 1 - 4
		#use unique document integer IDs

        # begin timer
        start = time.clock()
        # retrieve all documents from collection directory
        text_files = os.listdir(self.path)
        # text_files = ['Text-001.txt', 'Text-002.txt']
        text_dictionary = {}
        text_id = 1
        total_number_of_documents = len(text_files)

        for text_file in text_files:
            # concatenate path with file name
            text_file_path = self.path + text_file

            # retrieve contents from file
            text_contents = self.read_text_file(text_file_path)

            # convert string to list
            text_contents = self.convert_string_to_list(text_contents)

            # build dictionary
            text_dictionary = self.build_dictionary(text_id, text_contents, text_dictionary)

            text_id += 1

        # calculate the idf of each term
        self.calculate_idf(text_dictionary, total_number_of_documents)
        # end timer
        end = time.clock()
        total_time = end - start
        return text_dictionary  #, total_time

    # def exact_query(self, query_terms, k):
	# #function for exact top K retrieval (method 1)
	# #Returns at the minimum the document names of the top K documents ordered in decreasing order of similarity score
	#
	# def inexact_query_champion(self, query_terms, k):
	# #function for exact top K retrieval using champion list (method 2)
	# #Returns at the minimum the document names of the top K documents ordered in decreasing order of similarity score
	#
	# def inexact_query_index_elimination(self, query_terms, k):
	# #function for exact top K retrieval using index elimination (method 3)
	# #Returns at the minimum the document names of the top K documents ordered in decreasing order of similarity score
	#
	# def inexact_query_cluster_pruning(self, query_terms, k):
	# #function for exact top K retrieval using cluster pruning (method 4)
	# #Returns at the minimum the document names of the top K documents ordered in decreasing order of similarity score
	#
	# def print_dict(self):
    #     #function to print the terms and posting list in the index
	#
	# def print_doc_list(self):
	# # function to print the documents and their document id

    def read_text_file(self, text_file):
        f = open(text_file, "r")
        contents = f.read()
        return contents

    def convert_string_to_list(self, contents):
        # remove all punctuation and numerals, all text is lowercase
        contents = contents.lower()
        contents = re.sub(r'\d+', '', contents)

        # remove punctuation, replace with a space
        for char in "-:\n":
            contents = contents.replace(char, ' ')

        # remove quotes and apostrophes, replace with empty string
        for char in ".,?!'();$%\"":
            contents = contents.replace(char, '')
        contents = contents.replace('\n', ' ')

        # convert string to list
        contents = contents.split(' ')
        # remove empty strings
        contents = list(filter(None, contents))

        return contents

    def build_dictionary(self, text_id, word_list, text_dictionary):

        this_dict = text_dictionary
        total_words_in_document = len(word_list)

        integer = 0
        # for every word in a text
        for potential_new_word in word_list:
            # check if the word already exists in the dictionary
            if potential_new_word in this_dict:
                # if word does exist then access its value array
                for key, value in this_dict.items():
                    # if the new word being added is the same as a key value
                    if key == potential_new_word:
                        # temp list holds values of all texts that already have int values saved
                        already_saved_texts = []
                        for list in value:
                            # append text name to already_saved_texts list
                            already_saved_texts.append(list[0])
                        # set Boolean to false as a default
                        is_already_saved = False
                        # iterate though already_saved_texts looking for current text
                        for text_val in already_saved_texts:
                            # if current text exists set Boolean to true
                            if text_val == text_id:
                                is_already_saved = True

                        # if text already has values saved
                        if is_already_saved:
                            # iterate through lists
                            for list in value:
                                # position 0 in a list refers to the definition of what text it refers to
                                if list[0] == text_id:
                                    # if first value in key list is a text that already has this term then append
                                    # word int location to list
                                    list[1].append(integer)
                        # if list does not already have values saved
                        else:
                            # append text and word int location to list
                            value.append([text_id, [integer]])

            else:
                # if word does not already exist in dictionary
                # create new list containing text ID and int position in text to become value of new key
                new_list = [text_id, [integer]]
                # update dictionary to hold new key/value
                this_dict.update({potential_new_word: [new_list]})

            integer += 1

        this_dict = self.calculate_tf(this_dict, total_words_in_document, text_id)

        return this_dict

    def calculate_tf(self, this_dict, total_words_in_document, text_id):
        # for each dictionary term
        for key, value in this_dict.items():
            # for each document per term in dictionary
            for item in value:
                # if text_id is equal to the text_id of the list item
                if item[0] == text_id:
                    # measure the number of times a word appears in a doc
                    number_of_appearances_in_doc = len(item[1])
                    # divide it by the word count of the entire document
                    tf = number_of_appearances_in_doc/total_words_in_document
                    # insert into list
                    item.insert(1, tf)

        return this_dict

    def calculate_idf(self, this_dict, total_number_of_documents):

        # for each term in dictionary calculate and add the IDF
        for key, value in this_dict.items():
            # calculate IDF
            idf = math.log(total_number_of_documents/len(value))
            # add IDF to list in the first position
            value.insert(0, idf)

        return this_dict

    def create_query_sentence(self, query_terms):
        # create sentence describing the query
        sentence = ''
        for word in query_terms:
            if word == query_terms[0]:
                sentence = word
            else:
                sentence += ' AND ' + word
        return sentence

    def doc_name(self, doc):
        # get doc id dictionary
        doc_dict = self.get_doc_id_and_title_dict()
        for key, value in doc_dict.items():
            # if doc passed in to this function equals the key in the dictionary return the value
            if doc == key:
                return value

    def get_doc_id_and_title_dict(self):
        # get all text files
        text_files = os.listdir(self.path)
        # create empty list and iterator
        doc_dict = {}
        i = 1
        # cast int to string, concatenate, and append to list
        for text_file in text_files:
            doc_dict[i] = text_file
            i += 1
        return doc_dict


index = Index('collection3/')
final_index = index.buildIndex()
print(final_index)
# print('Index built in', final_index[1], 'seconds')
#
# index.and_query(['with', 'had', 'the', 'was'])
# index.and_query(['china', 'that'])
# index.and_query(['would', 'end', 'the', 'war'])
# index.and_query(['hat', 'time', 'put'])
# index.and_query(['practice', 'banker', 'program', 'operation', 'employee', 'government'])
# index.print_doc_list()
