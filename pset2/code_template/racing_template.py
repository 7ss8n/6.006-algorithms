"""Main solution file for F1 Kart Racing."""

import heapq as h
from operator import itemgetter


def compare(a, b):
    """
    Return True if a is smaller than b, or False, otherwise.

    Arguments:
        a (Fraction): The first fraction.
        b (Fraction): The second fraction.

    Return:
        bool: A boolean that is True if a < b, or False, otherwise.
    """
    # Implement this method for part (b).
    num_a_scaled = a.num*b.den
    num_b_scaled = b.num*a.den
    return num_a_scaled < num_b_scaled


class Fraction(object):
    """Class for fractions."""

    def __init__(self, num, den):
        """Construct a new fraction."""
        self.num = num
        self.den = den

    def __lt__(self, other):
        """Return True if self < other, or False otherwise."""
        return compare(self, other)

    def __str__(self):
        """Return textual representation of the fraction."""
        return str(self.num) + "/" + str(self.den)

    def __repr__(self):
        return str(float(self.num)/self.den)


def losetime(p_s, v_s, p_f, v_f, L):
    """
    Return the moment in time when (p_f, v_f) is going to take over (p_s, v_s).

    Arguments:
        p_s (int): The starting position of the slower kart.
        v_s (int): The velocity of the slower kart.
        p_f (int): The starting position of the faster kart.
        v_f (int): The velocity of the faster kart.
        L (int): The length of the track.

    Preconditions:
        (1) 0 <= p_s, p_f < L;
        (2) v_s < v_f
        (3) p_f != p_s

    Return:
        Fraction: The time when the faster kart (p_f, v_f) is going to take
            over the slower kart (p_s, v_s).
    """
    # Implement this method for part (c).
    if p_s > p_f:
        losetime = Fraction(p_s-p_f, v_f-v_s)
    else:
        losetime = Fraction((L-p_f)+p_s, v_f-v_s)
    return losetime


def remove(i, ahead, behind):
    """
    Update the (ahead, behind) data structure by removing competitor i.

    Note that this method does not return anything.

    Arguments:
        i (int): The id of the competitor.
        ahead (dict): A dictionary where the competitor ahead of competitor j
            is given by ahead[j].
        behind (dict): A dictionary where the competitor behind competitor j
            is given by behind[j].

    Preconditions:
        (1) i is present in both dictionaries.
        (2) for every competitor i present in either ahead or behind, we have
            i = ahead[behind[i]], as well as i = behind[ahead[i]]

    Return: Nothing.
    """
    # Implement this method for part (d).
    behind_i = behind[i]
    ahead_i = ahead[i]

    #remove the elements that are not possible any more
    del ahead[i]
    del ahead[behind_i]
    del behind[ahead_i]
    del behind[i]


    #the player behind i will now be behind the player ahead of i
    behind[ahead_i] = behind_i

    #the player ahead of i will now be ahead of the player behind i
    ahead[behind_i] = ahead_i
    return ((i,ahead_i),(behind_i,ahead_i))

def buildDictionaries(position):
    """
    Takes in a list of positions for players i=0 to i=N-1
    Returns: the ahead and behind dictionaries (ahead, behind).
    Runs in O(nlgn) time
    """
    ahead = {}
    behind = {}

    position_tuples = [(j,position[j]) for j in range(len(position))]

    #sort the position list
    sorted_position = sorted(position_tuples, key = itemgetter(1))

    #now build the ahead and behind dictionary
    for i in range(len(sorted_position)):
        ahead[sorted_position[i][0]] = sorted_position[(i+1) % len(position)][0] #the mod makes the list wrap around to the front
        behind[sorted_position[i][0]] = sorted_position[i-1][0] #at index 0, the behind index is -1, which is correct
    return (ahead, behind)


def rank(N, L, velocity, position):
    """
    Compute the rank (as defined in the problem statement) of competitor 0.

    Arguments:
        N (int): The number of competitors.
        L (int): The length of the track.
        velocity (list[int]): The velocities of all competitors, where the
            velocity of competitor i (0 <= i < N) is given by velocity[i].
        position (list[int]): The starting positions of all competitors, where
            the starting position of competitor i (0 <= i < N) is given by
            position[i].

    Preconditions:
        (1) len(velocity) = len(position) = N
        (2) all elements of velocity are distinct, and non-negative
        (3) all elements of position are distinct, and non-negative

    Return: The rank of competitor 0, which is a number between 1 and N,
        inclusive.
    """
    # Implement this method for part (f).

    #build the ahead and behind dictionaries
    ahead, behind = buildDictionaries(position)

    #for each pair of players in ahead, compute the losetime for the player in front
    #if the player in front is moving faster, don't add this to the array of losetimes
    #(losetime, (a,b))

    losetimes = []
    for playerA,playerB in ahead.items():
        if velocity[playerA] <= velocity[playerB]: #this means that playerA can never pass playerB
            continue
        else: #player A can pass player B at some time
            #compute when playerA will pass player B
            l_time = losetime(position[playerB], velocity[playerB], position[playerA], velocity[playerA], L)
            losetimes.append((l_time,(playerA,playerB)))

    #transform the losetimes list into a heap
    h.heapify(losetimes)

    #events stores tuples of the form (Losetime, (PlayerA, PlayerB))
    #where Losetime is the time it takes for playerA to pass playerB
    #events will be added to this list in chronological order
    events = []

    #if an event is invalidated, store it in the event_impossible dict as True
    event_impossible = {}

    while len(losetimes) >= 1:
        min_losetime = h.heappop(losetimes) #has structure (Fraction, (a,b)) where a passes b

        try: #see if the event is known to be impossible due to the game state
            test = event_impossible[min_losetime[1]]
        except: #if not, then the event can happen and should be added to events
            events.append(min_losetime)

        #remove the player that was passed, update ahead and behind dicts
        #also store the event that will need to be removed from the heap
        #and the event that needs to be added to the heap

        try:
            rm_event, add_event = remove(min_losetime[1][1], ahead, behind)

            #add the event that must be removed to the event_impossible dictionary
            event_impossible[rm_event] = True

            #add the new case if it is possible (behind player can overtake front player)
            p1 = add_event[0]
            p2 = add_event[1]

            if velocity[p1] > velocity[p2]:
                l_time = losetime(position[p2], velocity[p2], position[p1], velocity[p1], L)
                element_to_add = (l_time, (p1,p2)) #this element is to be added to the heap

                #add the new possible event to the heap
                h.heappush(losetimes, element_to_add)

        except:
            pass

    #get the rank of competitor zero
    for i in range(len(events)):
        if events[i][1][1] == 0: #if the event is Player 0 being passed
            return N-i
    
    #if competitor zero was never passed, he/she/ze/zir must have won!
    return 1



        












