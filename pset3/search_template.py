###################################
##########  PROBLEM 3-4 ###########
###################################


from rolling_hash import rolling_hash

def roll_forward(rolling_hash_obj, next_letter):
    """
    "Roll the hash forward" by discarding the oldest input character and
    appending next_letter to the input. Return the new hash, and save it in rolling_hash_obj.hash_val as well

    Parameters
    ----------
    rolling_hash_obj : rolling_hash
        Instance of rolling_hash
    next_letter : char
        New letter to append to input.

    Returns
    -------
    hsh : int
        Hash of updated input.
    """

    # Pop a letter from the left and get the mapped value of the popped letter
    # use popleft
    poppedLetter = rolling_hash_obj.sliding_window.popleft()
    poppedLetterVal = rolling_hash_obj.alphabet_map[poppedLetter]

    # Push a letter to the right.
    rolling_hash_obj.sliding_window.append(next_letter)

    # Set the hash_val in the rolling hash object
    #   Hint: rolling_hash_obj.a_to_k_minus_1 may be useful

    #follow the formula from the pset instructions
    rolling_hash_obj.hash_val = ((rolling_hash_obj.hash_val - poppedLetterVal * rolling_hash_obj.a_to_k_minus_1) * rolling_hash_obj.a + rolling_hash_obj.alphabet_map[next_letter]) % rolling_hash_obj.m
    return rolling_hash_obj.hash_val


def exact_search(rolling_hash_obj, pattern, document):
    """
    Search for string pattern in document. Return the position of the first match,
    or None if no match.

    Parameters
    ----------
    rolling_hash_obj : rolling_hash
        Instance of rolling_hash, with parameters guaranteed to be already filled in based on the inputs we will test: the hash length (k) and alphabet (alphabet) are already set
        You will need to create atleast one additional instance of rolling_hash_obj
    pattern : str
        String to search in document.
    document : str
        Document to search.

    Returns
    -------
    pos : int or None
        (zero-indexed) Position of first approximate match of S in T, or None if no match.
    """

    # may be helpful for you
    n = len(document)
    k = len(pattern)

    ## DO NOT MODIFY ##
    rolling_hash_obj.set_roll_forward_fn(roll_forward)
    rolling_hash_obj.init_hash(document[:k])
    ## END OF DO NOT MODIFY ##

    # we already have the rolling hash object for the document configured

    # init a new rolling hash with the pattern we are searching: this is the hash we will compare against
    compareHashObject = rolling_hash(k)
    compareHashVal = compareHashObject.init_hash(pattern)

    #continue rolling the document hash forward until we reach an index n-k
    for i in range(n-k):

        currentHashVal = rolling_hash_obj.hash_val

        #if the hashes match, do a char by char comparison to make sure
        if currentHashVal==compareHashVal:

            #if there is a match, return the index i
            if document[i:i+k] == pattern:
                return i

            else:
                pass

        #if there wasn't a match, roll the hash forward and continue
        #index k+1 is always one index higher than the last index in our sliding window
        rolling_hash_obj.roll_forward(document[k+i])

    #if nothing was found, there is no match, so return None
    return None
