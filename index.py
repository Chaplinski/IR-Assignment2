import re
import os
import collections
import time
import math
import sys
#import other modules as needed

class Index:
    def __init__(self, path, index, query, total_number_of_documents, stop_words):
        self.path = path
        self.index = index
        self.query = query
        self.total_number_of_documents = total_number_of_documents
        self.stop_words = stop_words

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
        self.total_number_of_documents = len(text_files)
        # list of stop words
        stop_words_list = self.stop_words

        for text_file in text_files:
            # concatenate path with file name
            text_file_path = self.path + text_file

            # retrieve contents from file
            text_contents = self.read_text_file(text_file_path)

            # convert string to list
            text_contents = self.convert_string_to_list(text_contents)

            # build dictionary
            text_dictionary = self.build_dictionary(text_id, text_contents, text_dictionary, stop_words_list)

            text_id += 1

        # calculate the idf of each term
        self.calculate_idf(text_dictionary, self.total_number_of_documents)
        # end timer
        end = time.clock()
        total_time = end - start
        self.index= text_dictionary
        # return text_dictionary  #, total_time

    def exact_query(self, query_terms, k):
	# #function for exact top K retrieval (method 1)
	# #Returns at the minimum the document names of the top K documents ordered in decreasing order of similarity score
        print('query: ', query_terms)
        print('top k: ', k)
        print('index: ', self.index)

        query_tf_idf_dict = {}
        index_tf_idf_dict = {}
        # for each word in the query
        for word, list in query_terms.items():
            # if that word is not a stop word
            if word not in self.stop_words:
                # get tf-idf of this query term
                query_term_tf_idf = list[0] * list[1]
                query_tf_idf_dict[word] = query_term_tf_idf
                # print('list:', list, 'tf-idf:', query_term_tf_idf)
                # if the word appears in self.index
                if word in self.index:
                    # get idf from the dictionary
                    dictionary_idf = self.index[word][0]
                    print(word, 'is in the index and its idf value is:', dictionary_idf)

                    for doc_id_list in self.index[word]:
                        # skip the first list item since it is the idf
                        if doc_id_list != self.index[word][0]:

                            doc_id = doc_id_list[0]
                            word_tf = doc_id_list[1]
                            doc_word_tf_idf = word_tf * dictionary_idf
                            if index_tf_idf_dict[doc_id] in index_tf_idf_dict:
                                index_tf_idf_dict[doc_id] = {}
                                index_tf_idf_dict[doc_id][word] = doc_word_tf_idf
                                print('doc id is:', doc_id, 'and tf-idf is:', doc_word_tf_idf)
                                # sys.exit()
        print(index_tf_idf_dict)


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

    def build_dictionary(self, text_id, word_list, text_dictionary, stop_words):

        this_dict = text_dictionary
        total_words_in_document = len(word_list)

        integer = 0
        # for every word in a text
        for potential_new_word in word_list:
            # make sure stop word is not in list
            if potential_new_word not in stop_words:
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
                    tf = number_of_appearances_in_doc
                    # print(tf)
                    # calculate w
                    w = (1 + math.log10(tf))
                    # print('word:', key)
                    # print('doc appearances: ', number_of_appearances_in_doc)
                    # print('doc words total: ', total_words_in_document)
                    # print('tf: ', tf)
                    # print('w:', w)
                    # sys.exit()
                    # print(w)
                    # sys.exit()
                    # insert into list
                    item.insert(1, w)

        return this_dict

    def calculate_idf(self, this_dict, total_number_of_documents):

        # for each term in dictionary calculate and add the IDF
        for key, value in this_dict.items():
            # calculate IDF
            idf = math.log10(total_number_of_documents/len(value))
            # print(this_dict)
            # sys.exit()
            # add IDF to list in the first position
            value.insert(0, idf)

        return this_dict

    def get_stop_words(self):
        f = open('stop-list/stop-list.txt', "r")
        contents = f.read()
        contents = self.convert_string_to_list(contents)
        self.stop_words = contents

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

    # get query and store terms as a list
    def ask_for_query(self, final_index):
        self.query = input("Enter your query: ")
        self.query = self.convert_string_to_list(self.query)
        # create dictionary to keep track of word occurrences in query
        this_dict = {}
        # for each word in query
        for item in self.query:
            # if the word is not in the dictionary add it with a value of 1 occurrence
            if item not in this_dict:
                this_dict.update({item: 1})
            else:
                number_of_occurrences = this_dict.get(item)
                number_of_occurrences += 1
                this_dict.update({item: number_of_occurrences})

        total_words_in_query = len(self.query)
        # print(total_words_in_query)
        # for each word in the query, calculate the tf-idf
        for key, value in this_dict.items():
            # calculate tf
            number_of_appearances_in_query = value
            # divide it by the word count of the entire query
            tf = number_of_appearances_in_query
            # calculate w
            w = (1 + math.log10(tf))

            idf = ''
            # get idf that is already stored in inverted index
            if key in final_index:
                idf = final_index[key][0]

            # store w and idf as value for word key in this dict
            this_dict[key] = [w, idf]

        return this_dict

    def show_query(self):
       print('')
       # print(self.query)


# instantiate the object
index = Index('collection3/', '', '', '', '')
# build the index, which is stored as self.index
index.buildIndex()
# get the stop words list
# index.get_stop_words()
# ask for a query and store it as query
query = index.ask_for_query(index.index)
# function for exact top K retrieval (method 1)
index.exact_query(query, 10)

# stop_words = index.get_stop_words()
# print(final_index)
# print('Index built in', final_index[1], 'seconds')
#
# index.and_query(['with', 'had', 'the', 'was'])
# index.and_query(['china', 'that'])
# index.and_query(['would', 'end', 'the', 'war'])
# index.and_query(['hat', 'time', 'put'])
# index.and_query(['practice', 'banker', 'program', 'operation', 'employee', 'government'])
# index.print_doc_list()
