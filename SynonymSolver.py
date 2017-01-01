# -*- coding: utf-8 -*-
'''
Author:         Shoujun Leo Feng
                1T9 Engsci, UofT
Last modified:  Dec. 18, 2015.
'''

import math
import random
import time
import os
os.chdir('F:\\Fsj\\Documents\\u of t\\CSC180\\p3')

# -*- coding: utf-8 -*-
'''Semantic Similarity: starter code

Author: Michael Guerzhoy. Last modified: Nov. 18, 2015.
'''

import math
import random

def norm(vec):
    ''' Return the norm of a vector semantic descriptor stored as a dictionary,
        as described in the handout for Project 3.

        vec: The semantic descriptor vectors.
    '''

    sum_of_squares = 0.0  # floating point to handle large numbers
    for x in vec:
        sum_of_squares += vec[x] * vec[x]

    return math.sqrt(sum_of_squares)


def cosine_similarity(vec1, vec2):
    ''' Calculate the cosine of the angle between two semantic descriptor
        vectors of two words.

        vec1,vec2: The semantic descriptor vectors, stored as dictionaries.
        returned value: The cosine similarity of the two vectors (words).
    '''
    norm_1=norm(vec1)
    norm_2=norm(vec2)
    #Calculate the norms of the two vectors.
    dot_product=0.0
    for word in vec1:
        if word in vec2:
            #Go through every entries that the two vectors have in common.
            dot_product+=vec1[word]*vec2[word]
            #Add the product of this indice to the total dot product.
    #Calculate the doc product of the two vectors.
    cos=dot_product/norm_2/norm_1
    #Cosine of two values is given by their dot product devided by the
    #product of their norms.
    return cos

def euclidean_similarity(vec1, vec2):
    ''' Calculate the euclidean distance between two semantic descriptor
        vectors of two words, and return its negative value

        vec1,vec2: The semantic descriptor vectors, stored as dictionaries.
        returned value: The cosine similarity of the two vectors (words).
    '''
    eucli_sum=0.0
    for word in vec1.keys() | vec2.keys():
        #Go through every entries that at least one of the two vectors have.
        eucli_sum+=(vec1.get(word,0)-vec2.get(word,0))**2
        #Add the component of their euclidian distance.
        #If one entry does not exist in one vector, the default is 0.
    return -eucli_sum #return the negative euclidean distance

def norm_euclidean_similarity(vec1, vec2):
    ''' Calculate the euclidean distance between two normalized semantic
        descriptor vectors of two words, and return its negative value.

        vec1,vec2: The semantic descriptor vectors, stored as dictionaries.
        returned value: The cosine similarity of the two vectors (words).
    '''
    norm_1=norm(vec1)
    norm_2=norm(vec2)
    #Calculate the norms of the two vectors.
    eucli_sum=0.0
    for word in vec1.keys() | vec2.keys():
        #Go through every entries that at least one of the two vectors have.
        eucli_sum+=(vec1.get(word,0)/norm_1-vec2.get(word,0)/norm_2)**2
        #Add the component of their euclidian distance.
        #If one entry does not exist in one vector, the default is 0.
    return -eucli_sum #return the negative euclidean distance

def add_coappearance(word_i,word_j,semantic_desc_dict):
    ''' Update the semantic descriptors dictionary with one more co-appearance
        of two words.

        semantic_desc_dict: The dictionary of all semantic descriptors.
        word_i,word_j: The two words that appeared in the same sentence.
        No return.
    '''
    if word_i==word_j:
        return
    #Do not count the word appears with itself.
    if word_i not in semantic_desc_dict:
        semantic_desc_dict[word_i]={}
    if word_j not in semantic_desc_dict:
        semantic_desc_dict[word_j]={}
    #If the word have never appeared, create a new vector for it.
    if word_j not in semantic_desc_dict[word_i]:
        semantic_desc_dict[word_i][word_j]=0
    if word_i not in semantic_desc_dict[word_j]:
        semantic_desc_dict[word_j][word_i]=0
    #If the two words have never appeared together before, create a new
    #entry for one word in the descriptor of the other word.
    semantic_desc_dict[word_i][word_j]+=1
    semantic_desc_dict[word_j][word_i]+=1
    #Add one more time that one of the word has appeared together with the
    #other one and update both descriptors.


def build_semantic_descriptors(sentences):
    ''' Build a dictionary of semantic descriptors from the list of sentences.

        sentences: A list of sentences, with each sentence given as a list of
        words, with all punctuations are removed and converted to lower case.
    '''
    semantic_desc_dict={}
    #Create empty dictionary.
    for sentence in sentences:
        #Go through each sentence.
        s_tmp=list(set(sentence))
        #Convert sentence list to set and back to list to avoid duplication.
        for i in range(len(s_tmp)):
            for j in range(i+1,len(s_tmp)):
                #Go through every pairs of words in the same sentence.
                add_coappearance( s_tmp[i], s_tmp[j], semantic_desc_dict)
                #Update the descriptor dictionary with the new co-appearance
                #pair
    return semantic_desc_dict

def build_semantic_descriptors_from_files(filenames):
    ''' Takes a list of filenames of strings, which contains the names of files.
        build sentences and call function build_semantic_descriptors to obtain
        a dictionary of the semantic descriptors of all the words in the files
        filenames

        sentences: A list of sentences, with each sentence given as a list of
        words. Assume all punctuations are removed and converted to lower case.

        filenames: a list of the name of different files which are to be opened
    '''
    sentences = []

    for filename in filenames:
        #seperate the sentences from the file and out the sentences in the list
        #as the string
        f = open(filename, "r", encoding="utf-8")
        text = f.read()
        text = text.lower()
        text = text.replace('?','.').replace('!','.')
        text = text.split('.')
        sentences.extend(text)

    for i in range(len(sentences)):
        #seperate the sentences into individual words and remove all possible
        # non_word symbols from the sides of the word
        sentence_tmp = sentences[i].replace(","," ").replace( "-"," ").\
        replace("-",' ').replace( ":"," ").replace( ";"," ").replace( '"',' ').\
        replace("'",' ').replace("[",' ').replace(']',' ').replace('(',' ').\
        replace(')',' ').replace('*',' ').replace('/',' ').replace('\\',' ').\
        replace('_',' ').replace('$'," ")
        sentence_tmp = sentence_tmp.split()
        sentences[i]=[]
        for word in sentence_tmp:
            if word.isalpha():
                #if there are still non-letter character in the word don't
                #include the word
                sentences[i].append(word)

    # call the build_semantic_descriptors function and return the result of that
    # function
    return build_semantic_descriptors(sentences)

def most_similar_word(word, choices, semantic_descriptors, similarity_fn):
    ''' Takes in a string word, a list of strings choices, and a dictionary
        semantic_descriptors，returns the element of choices which has the
        largest semantic similarity to word

        word: a given word with which a synonyms is to be chosen from the list
        of potential choices in the list 'choices'
        max_choice: the word in the choices list which has the most similarity
        with the 'word'
        max_similarity : the largest similarity score between the given word and
        the word in the list 'choices'
    '''
    max_choice = None
    max_similarity = None
    if word in semantic_descriptors:
        for i in range(len(choices)):
            # go through the list of choices and find the element with the
            # largest similarity to the word
            if choices[i] in semantic_descriptors:
                similarity = similarity_fn(semantic_descriptors[word],\
                semantic_descriptors[choices[i]])
                if max_similarity==None or similarity > max_similarity:
                    #if the current similarity is larger than the current max
                    # one or if this is the first comparison
                    max_similarity = similarity
                    max_choice = choices[i]
                    #update the max_choice and the max_similarity
        if max_choice==None:
            #If all words not in dictionary, pick randomly
            return random.choice(choices)
        else:
            #Return the choice with maximum similarity
            return max_choice

    else:
        # if the word is not in semantic_descriptors, there is no way to compare
        # word with other word return a random choice
        return random.choice(choices)


def run_similarity_test(filename, semantic_descriptors, similarity_fn):

    '''Takes in a string filename, returns the percentage  of questions on which
       most_similar_word() guesses the answer correctly using the semantic
       descriptors stored in semantic_descriptors, using the similarity function
       similariy_fn

        counter : the number of times the most_similar_word() gets the correct
        answer
        text: a nested list the elements of this list is the list of the words
        in the corresponding line
        choice : the selected answer from the list of choices
    '''
    counter = 0
    file = open(filename, "r", encoding="utf-8")
    text = file.read()
    text = text.strip().split('\n')
    # remove the space on the sides of the string in order to reduce the
    # potential of getting the empty lines
    # break the file into sentences because the sentences in this file is only
    # saperated by '\n'
    for i in range(len(text)):
        text[i] = text[i].split(' ')
        #put the words in saperate lines in the inner list of the text list

    for line in text:
        # obtain the most similar word
        if len(line) > 0:
            # compare the first element of the inner list which is the given
            # word with the choices which are from the third element of the
            # inner list to the end
            choice = most_similar_word(line[0],line[2:],\
            semantic_descriptors,similarity_fn)
            #compare the selected answer with the actual correct answer, if they
            # are the same, the number of times the function gets the correct
            # answer adds 1
            if choice == line[1]:
                counter += 1
    # return the percentage of the number of correctly answered questions
    return counter/len(text)*100

if __name__ == '__main__':
    import time


###the parameter is to determine the percentage of the novel text
    #for i in range (1,10):
    #   print (i*10,'%')
    t1 = time.time()
    d=build_semantic_descriptors_from_files(["pg2600.txt",'pg7178.txt'])
    success_rate=run_similarity_test\
    ("F:\\Fsj\Documents\\u of t\\CSC180\\p3\\text.txt",d,cosine_similarity)
    print('success_rate',success_rate)
    t = time.time()
    print('time is :',t- t1)
