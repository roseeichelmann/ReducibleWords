import sys

#  File: Reducible.py

#  Description: Program to find list of longest reducible words
# in English language

#  Student Name: Rose Eichelmann

#  Student UT EID: ree585

#  Course Name: CS 313E

#  Unique Number: 86610

#  Date Created: 7-15-21

#  Date Last Modified: 8-1-21

# Input: takes as input a positive integer n
# Output: returns True if n is prime and False otherwise
def is_prime ( n ):
    if (n == 1):
        return False
    limit = int (n ** 0.5) + 1
    div = 2
    while (div < limit):
        if (n % div == 0):
            return False
        div += 1
    return True


# Input: takes as input a string in lower case and the size
# of the hash table
# Output: returns the index the string will hash into
def hash_word (s, size):
    hash_idx = 0
    for j in range (len(s)):
        letter = ord (s[j]) - 96
        hash_idx = (hash_idx * 26 + letter) % size
    return hash_idx


# Input: takes as input a string in lower case and the constant
# for double hashing
# Output: returns the step size for that string
def step_size (s, const, key):
    steps = const - ( key % const )
    return steps


# Input: takes as input a string and a hash table
# Output: no output; the function enters the string in the hash table,
# it resolves collisions by double hashing
def insert_word (s, hash_table):
    # find size of table
    size = len(hash_table)
    # find index of word
    index = hash_word(s, size)
    key = 0
    # find integer key for word
    for j in range (len(s)):
        letter = ord (s[j]) - 96
        key = (key * 26 + letter)
    # find step size for key
    steps = step_size(s, 5, key)
    i = 1
    # double hash until empty spot found
    while hash_table[index] != '':
        index = (index + i * steps) % size
        i += 1
    # insert word into empty space
    hash_table[index] = s


# Input: takes as input a string and a hash table
# Output: returns True if the string is in the hash table
# and False otherwise
def find_word (s, hash_table):
    # find size of table
    size = len(hash_table)
    # find index of word
    index = hash_word(s, size)
    key = 0
    # find integer key for word
    for j in range (len(s)):
        letter = ord (s[j]) - 96
        key = (key * 26 + letter)
    # find step size
    steps = step_size(s, 5, key)
    i = 0
    # search for word using double hashing until found or spot is empty
    while hash_table[(index + i * steps) % size] != s:
        # if spot is empty word is not in table
        if hash_table[(index + i * steps) % size] == '':
            return False
        # search next spot
        i += 1
    return True


# Input: string s, a hash table, and a hash_memo
# recursively finds if the string is reducible
# Output: if the string is reducible it enters it into the hash memo
# and returns True and False otherwise
def is_reducible (s, hash_list, hash_memo):
    # return if word is reducible
    if len(s) == 1:
        return s == 'a' or s == 'o' or s == 'i'
    else:
        for letter in range(len(s)):
            # delete letter from word
            new_word = s[:letter] + s[letter + 1:]
            # if word is already in memo it is reducible
            if find_word(new_word, hash_memo):
                return True
            # if word is in hash list recursively call function with new word
            if find_word(new_word, hash_list):
                return is_reducible(new_word, hash_list, hash_memo)
            # if new word has now been reduced to a i or u it is reducible
            elif new_word == 'a' or new_word == 'o' or new_word == 'i':
                return True
        return False


# Input: string_list a list of words
# Output: returns a list of words that have the maximum length
def get_longest_words (string_list):
    # create list of longest words
    longest_words = []
    length = 0
    # loop through each word in reducible word list
    for word in string_list:
        new_length = len(word)
        # if length of word is longer than longest length
        if new_length > length:
            # empty the list
            longest_words = []
            # make current length the longest length
            length = new_length
            # append word to the list
            longest_words.append(word)
    return longest_words


def main():
    # create an empty word_list
    word_list = []

    # read words from words.txt and append to word_list
    for line in sys.stdin:
        line = line.strip()
        word_list.append (line)

    # find length of word_list
    n = len(word_list)

    # determine prime number N that is greater than twice
    # the length of the word_list
    N = n * 2 + 1
    while not is_prime(N):
        N += 1

    # create an empty hash_list
    hash_list = []

    # populate the hash_list with N blank strings
    hash_list = [''] * N

    # hash each word in word_list into hash_list
    # for collisions use double hashing
    for word in word_list:
        insert_word(word, hash_list)


    # create an empty hash_memo of size M
    # we do not know a priori how many words will be reducible
    # let us assume it is 10 percent (fairly safe) of the words
    # then M is a prime number that is slightly greater than
    # 0.2 * size of word_list
    M = int(0.2 * n) + 1
    while not is_prime(M):
        M += 1    # for collisions use double hashing
    hash_memo = [''] * (M)

    # create an empty list reducible_words
    reducible_words = []

    # for each word in the word_list recursively determine
    # if it is reducible, if it is, add it to reducible_words
    # as you recursively remove one letter at a time check
    # first if the sub-word exists in the hash_memo. if it does
    # then the word is reducible and you do not have to test
    # any further. add the word to the hash_memo.
    for word in word_list:
        # if word doesnt have 'a' 'i' or 'u' skip
        if 'a' in word or 'o' in word or 'i' in word:
            # check if reducible
            if is_reducible(word, hash_list, hash_memo):
                # append to reducible words list and hash memo
                reducible_words.append(word)
                insert_word(word, hash_memo)
    # find the largest reducible words in reducible_words
    # print the reducible words in alphabetical order
    # one word per line
    longest_words = get_longest_words(reducible_words)
    longest_words.sort()
    for word in longest_words:
        print(word)


if __name__ == "__main__":
    main()