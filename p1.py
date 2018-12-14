import math
import matplotlib
import numpy as np
import time
matplotlib.use('TkAgg')
from collections import defaultdict
from matplotlib import pyplot as plt
from pdb import set_trace as bp


# generate and return e and p array
def generateEPArrays(conflictAdjacency):
    # init arrays with single element, 0, to begin with session number 1
    e = []
    p = []

    eIndex = 0
    pIndex = 0

    for key, value in conflictAdjacency.iteritems():
        if len(value) == 0:
            continue
        else:
            p.append(eIndex)
            for i in value:
                e.append(i) 
                eIndex += 1
    return [e, p]

def generateAdjacency(sessions, distinctConflicts):
    conflictAdjacency = {}
    conflictKeys = distinctConflicts.keys()
    # initalize lists for  all sessions
    for i in range(1, sessions + 1):
        conflictAdjacency[i] = []

    for key in conflictKeys:
        currentConflicts = distinctConflicts[key]
        for session in currentConflicts:
            conflictAdjacency[key].append(session)
            if key not in conflictAdjacency[session]:
                conflictAdjacency[session].append(key)
    return conflictAdjacency

def formatConflicts(conflicts):
    distinctConflicts = {}
    for pair in conflicts:
        element0 = pair[0]
        element1 = pair[1]
        conflictKeys = distinctConflicts.keys()
        if element0 not in conflictKeys and element1 not in conflictKeys:
            distinctConflicts[element0] = []
            targetList = distinctConflicts[element0]
            targetList.append(element1)
        elif element0 in conflictKeys and element1 not in distinctConflicts[element0]:
            targetList = distinctConflicts[element0]
            targetList.append(element1)
        elif element1 in conflictKeys and element0 not in distinctConflicts[element1]:
            targetList = distinctConflicts[element1]
            targetList.append(element0)
        elif element0 in conflictKeys and element1 in distinctConflicts[element0] or element1 in conflictKeys and element0 in distinctConflicts[element1]:
            continue
    return distinctConflicts


def calculateDistinctConflicts2(conflicts):
    indexesWithDuplicates = []
    conflictsNoDups = []
    conflictTuples = [tuple(x) for x in conflicts]
    def list_duplicates(seq):
        tally = defaultdict(list)
        for i,item in enumerate(seq):
            tally[item].append(i)
        return ((key,locs) for key,locs in tally.items() 
                                if len(locs)>1)

    for dup in sorted(list_duplicates(conflictTuples)):
        dupIndexs = dup[1]
        # push all dup indexes except for the first one
        for x in range(1, len(dupIndexs)):
            indexesWithDuplicates.append(dupIndexs[x])
    
    for idx, i in enumerate(conflicts):
        if idx not in indexesWithDuplicates:
            conflictsNoDups.append(i)
    
    distinctConflicts = formatConflicts(conflictsNoDups)

    return distinctConflicts

def calculateDistinctConflicts1(conflicts):
    distinctConflicts = formatConflicts(conflicts)
    return distinctConflicts

def calculateConflicts(schedule):
    conflictArray = []
    for key, value in schedule.iteritems():
        currentList = schedule[key]
        for i in range(0, len(currentList) - 1):
            for x in range(i, len(currentList) - 1):
                conflictArray.append([currentList[i], currentList[x+1]])
    return conflictArray

def getRandomTiered(sessions):
    num_sessions = sessions + 1
    first = np.random.randint(1, int(sessions * 0.1), int(sessions * 0.5))
    second = np.random.randint(int(sessions * 0.1) , sessions + 1, int(sessions * 0.5))
    final = np.append(first, second)
    selection = np.random.choice(final, 1)
    
    # plotting
    # data = np.random.choice(final, sessions)
    # print data
    # count, bins, ignored = plt.hist(final, int(sessions//10), facecolor='green') 
    # plt.xlabel('X~U[1,500]')
    # plt.ylabel('Count')
    # plt.title("Tiered Distribution Histogram (Bin size 50)")
    # plt.axis([1, sessions, 0, 70])
    # plt.grid(True)
    # plt.show(block=True)

    return selection


def getRandomUniform(sessions):
    selection = int(np.random.randint(1, sessions + 1, 1))

    # plotting
    # data = np.random.randint(1, 101, 2500)
    # count, bins, ignored = plt.hist(data, 50, facecolor='green') 
    # plt.xlabel('X~U[1,100]')
    # plt.ylabel('Count')
    # plt.title("Uniform Distribution Histogram (Bin size 2)")
    # plt.axis([1, 100, 0, 100])
    # plt.grid(True)
    # plt.show(block=True)

    return selection

def getRandomSkewed(sessions):
    a = int(np.random.randint(1, sessions + 1, 1))
    b = int(np.random.randint(1, sessions + 1, 1))
    c = abs(a-b)
    selection = c

    # plotting
    # a = np.random.randint(1, 101, 2500)
    # b = np.random.randint(1, 101, 2500)
    # c = abs(a-b)
    # count, bins, ignored = plt.hist(c, 50, facecolor='green') 
    # plt.xlabel('X~U[1,100]')
    # plt.ylabel('Count')
    # plt.title("Skewed Distribution Histogram (Bin size 2)")
    # plt.axis([1, 100, 0, 100])
    # plt.grid(True)
    # plt.show(block=True)

    return selection

def getCustom(sessions):
    selection = int(np.random.randint(1, sessions + 1, 1))

    # plotting
    # a = np.random.randint(1, 101, 2500)
    # x = np.sqrt(a) * 10
    # count, bins, ignored = plt.hist(x, 50, facecolor='green') 
    # plt.xlabel('X~U[1,100]')
    # plt.ylabel('Count')
    # plt.title("Custom Distribution Histogram (Bin size 2)")
    # plt.axis([1, 100, 0, 100])
    # plt.grid(True)
    # plt.show(block=True)

    return selection

def generateSchedule(sessions, attendees, maxSessions, distribution, attendeeDict):
    print 'Generating schedule...'
    if distribution == 'uniform':
        # I referenced the following url for uniform distribution code
        # https://stackoverflow.com/questions/22744577/plotting-basic-uniform-distribution-on-python
        print 'Generating uniform distribution...'
        # loop over the keys in the dict
        for key, value in attendeeDict.iteritems():
            # start with index 0
            currentIndex = 0
            # for each session space for the attendee...
            for s in attendeeDict[key]:
                # if there is a default space in the array...
                if None in attendeeDict[key]:
                    # select a session
                    selection = getRandomUniform(sessions)
                    # while the selected session in already in the list...
                    while selection in attendeeDict[key]:
                        # make a new selection.
                        selection = getRandomUniform(sessions)
                        # break when the selected session is not already in the list
                        if selection not in attendeeDict[key]:
                            break
                    # add the session to the attendees list
                    attendeeDict[key][currentIndex] = selection
                    # move to the next session space
                    currentIndex += 1
                else:
                    print 'ERROR - Uniform dist index error'
                    exit()
        return attendeeDict
    elif distribution == 'tiered':
        print 'Generating tiered distribution...'
        # TODO
        print 'Generating tiered distribution...'
        # loop over the keys in the dict
        for key, value in attendeeDict.iteritems():
            # start with index 0
            currentIndex = 0
            # for each session space for the attendee...
            for s in attendeeDict[key]:
                # if there is a default space in the array...
                if None in attendeeDict[key]:
                    # select a session
                    selection = getRandomTiered(sessions)
                    # while the selected session in already in the list...
                    while selection in attendeeDict[key] or selection == 0:
                        # make a new selection.
                        selection = getRandomTiered(sessions)
                        # break when the selected session is not already in the list
                        # NOTE: This while loop takes a LONG TIME when sessions == maxSessions
                        if selection not in attendeeDict[key] and selection != 0:
                            break
                    # add the session to the attendees list
                    attendeeDict[key][currentIndex] = selection
                    # move to the next session space
                    currentIndex += 1
                else:
                    print 'ERROR - Tiered dist index error'
                    exit()
        return attendeeDict
    elif distribution == 'skewed':
        # I reference the following url for skewed distribution code
        # https://gamedev.stackexchange.com/questions/116832/random-number-in-a-range-biased-toward-the-low-end-of-the-range
        print 'Generating skewed distribution...'
        # loop over the keys in the dict
        for key, value in attendeeDict.iteritems():
            # start with index 0
            currentIndex = 0
            # for each session space for the attendee...
            for s in attendeeDict[key]:
                # if there is a default space in the array...
                if None in attendeeDict[key]:
                    # select a session
                    selection = getRandomSkewed(sessions)
                    # while the selected session in already in the list...
                    while selection in attendeeDict[key] or selection == 0:
                        # make a new selection.
                        selection = getRandomSkewed(sessions)
                        # break when the selected session is not already in the list
                        # NOTE: This while loop takes a LONG TIME when sessions == maxSessions
                        if selection not in attendeeDict[key] and selection != 0:
                            break
                    # add the session to the attendees list
                    attendeeDict[key][currentIndex] = selection
                    # move to the next session space
                    currentIndex += 1
                else:
                    print 'ERROR - Skewed dist index error'
                    exit()
        return attendeeDict
    elif distribution == 'custom':
        # I referenced the following url for normal distribution code
        # https://docs.scipy.org/doc/numpy-1.13.0/reference/generated/numpy.random.normal.html
        print 'Generating custom distribution...'
        #loop over the keys in the dict
        for key, value in attendeeDict.iteritems():
            # start with index 0
            currentIndex = 0
            # for each session space for the attendee...
            for s in attendeeDict[key]:
                # if there is a default space in the array...
                if None in attendeeDict[key]:
                    # select a session
                    selection = getCustom(sessions)
                    # while the selected session in already in the list...
                    while selection in attendeeDict[key] or selection == 0:
                        # make a new selection.
                        selection = getCustom(sessions)
                        # break when the selected session is not already in the list
                        if selection not in attendeeDict[key] and selection != 0:
                            break
                    # add the session to the attendees list
                    attendeeDict[key][currentIndex] = selection
                    # move to the next session space
                    currentIndex += 1
                else:
                    print 'ERROR - Normal dist index error'
                    exit()
        print 'Done generating schedule'
        return attendeeDict
  
def main():
    # get input values from the command line
    sessions = raw_input('Enter the number of sessions (integer): ')
    attendees = raw_input('Enter the number of attendees (integer): ')
    maxSessions = raw_input('Enter the number of sessions per attendee (integer): ') 
    distribution = raw_input('Choose a distribution: uniform | tiered | skewed | custom: ')
    conflictMethod = raw_input('Choose a method to remove conflicts: 1 | 2: ')

    # validate command line input
    try:
        sessions = int(sessions)
    except ValueError as e:
        print 'ERROR - Number of sessions must be an integer'
        exit()
    
    try:
        attendees = int(attendees)
    except ValueError as e:
        print 'ERROR - Number of attendees must be an integer'
        exit()

    try:
        maxSessions = int(maxSessions)
    except ValueError as e:
        print 'ERROR - Max number of sessions must be an integer'
        exit()
    
    try:
        distribution = distribution.lower().replace(' ', '')
    except error as e:
        print 'ERROR - Unknown error in distribution format'
        exit()

    if distribution != 'uniform' and distribution != 'tiered' and distribution != 'skewed' and distribution != 'custom':
        print 'ERROR - Invalid distribution type'
        exit()

    if conflictMethod != '1' and conflictMethod != '2':
        print 'ERROR - invalid input for conflict method' 
    
    # adjust max sessions for skewed an custom distributions
    if distribution == 'skewed' or distribution == 'custom':
        maxSessions = int(0.1 * maxSessions)
        if maxSessions < 1:
            maxSessions = 1

    # create dictionary of lists to hold the sessions for each attendee
    attendeeDict = {}
    for i in range (0, attendees):
        attendeeDict[i + 1] = [None] * maxSessions

    # pass validated inputs to schedule generation function
    schedule = generateSchedule(sessions, attendees, maxSessions, distribution, attendeeDict)

    # enumerate all conflicts
    conflicts = calculateConflicts(schedule)

    # remove duplicate conflicts
    if conflictMethod == '1':
        distinctConflicts = calculateDistinctConflicts1(conflicts)
    elif conflictMethod == '2':
        distinctConflicts = calculateDistinctConflicts2(conflicts)

    # generate adjacency list
    conflictAdjacency = generateAdjacency(sessions,distinctConflicts)

    # generate E and P array
    EParrays = generateEPArrays(conflictAdjacency)

    print { "sessions(N)": sessions, 
    "distinctConflicts(M)": distinctConflicts, 
    "conflicts(T)": conflicts, 
    "attendees(S)": attendees, 
    "maxSessions": maxSessions,
    "distribution": distribution,
    "eArray": EParrays[0],
    "pArray": EParrays[1]}

# test if script is being run directly
if __name__ == '__main__':
    main ()