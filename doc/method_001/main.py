import os
import sys
import logging
import hashlib
import numpy
from random import randint

from itertools import groupby, chain

logger = logging.getLogger(__name__)
LOGGING_FORMAT = '[%(levelname)s] [%(asctime)s] %(funcName)s(): %(message)s'
logging.basicConfig(level=logging.INFO, format=LOGGING_FORMAT)

def FindRepeatedSubstring(data): 
    n = len(data)
    LCSRe = numpy.zeros((n+1,n+1), dtype=int)
    output = set()
    matches = set()

    for i in range(1, n + 1): 
        for j in range(i + 1, n + 1): 
            if (data[i - 1] == data[j - 1] and
                LCSRe[i - 1][j - 1] < (j - i)): 
                LCSRe[i][j] = LCSRe[i - 1][j - 1] + 1

                if(LCSRe[i][j] > 0):
                    _len = LCSRe[i][j]
                    if (_len, i) not in matches:
                        output.add(data[i - _len:i])
                    matches.add((_len, i))
            else: 
                LCSRe[i][j] = 0

    return output

def count_consecutive(main_vector, base_vector):
    label = -1
    main_vector = replace_subvector_02(main_vector, list(base_vector), label)
    return len(list(filter(lambda x: x == label, main_vector)))

def replace_subvector_02(data, base_vector, label):
    output = []
    u = 0
    for i in range(len(data)):
        if data[i] != base_vector[u]:
            u = 0

        if data[i] == base_vector[u]:
            u += 1 
            if u == len(base_vector):
                output.append(label)
                u = 0
            continue
        u = 0

        tmp = []
        output.append(data[i])

    return output

def find_base_vectors(main_vector):
    selected_vectors = FindRepeatedSubstring(tuple(main_vector))

    _max = []
    for v in selected_vectors:
        mc = count_consecutive(main_vector, v)
        if mc > 0:
            _max.append([mc, v])

    logger.debug('[+] Could find %d base vectors with consecutive matches.', len(_max))

    if not _max:
        return []

    _max.sort(key=lambda x: x[0], reverse=True)
    logger.debug('[+] First vector has %d elements and %d occurences', len(_max[0][1]), _max[0][0])

    main_vectors = [x[1] for x in _max]
    return main_vectors

def replace_subvector(data, base_vector, label):
    output = []
    tmp = []
    u = 0
    for i in range(len(data)):
        if data[i][0] != base_vector[u]:
            u = 0

        if data[i][0] == base_vector[u]:
            u += 1 
            tmp.append(data[i][1])
            if u == len(base_vector):
                output.append([label, tmp])
                tmp = []
                u = 0
            continue
        u = 0
        tmp = []
        output.append(data[i])

    return output

# Finds biggest repeated subvector and replace it with a token
def __transform_001(data):
    indexes = [ c[0] for c in data ]
    base_vectors = find_base_vectors(indexes)

    if len(base_vectors) <= 1:
        return data, False

    for base_vector in base_vectors:
        label = (sum(base_vector) + randint(1, 20)) * len(data)
        data = replace_subvector(data, base_vector, label)

    return data, True

def __update_repeated(element, e):
    if type(element) is not list:
        element['repeated'] += e['repeated']
        return element

    for i in range(len(element)):
        element[i] = __update_repeated(element[i], e[i])

    return element

# Removes repeated consecutive elements in a vector
def __transform_002(data):
    output = []
    last_element = [-1, None]
    for d in data:
        if last_element[0] == d[0]:
            output[-1][1] = __update_repeated(last_element[1], d[1])
            continue

        output.append(d)
        last_element = d

    return output

def __checksum(call):
    h = hashlib.md5(call.encode('utf-8'))
    return h.hexdigest()

def __expand_element(e):
    if type(e) is not list:
        return [e]

    output = []
    for x in e:
        output += __expand_element(x)

    return output

def __compress_calls(data=[]):
    # Collect calls and create indexes
    calls = []
    unique_checksums = []
    for c in data:
        csum = __checksum(c)
        if csum not in unique_checksums:
            unique_checksums.append(csum)
        calls.append([unique_checksums.index(csum), {'label': c, 'repeated': 1} ])

    logger.debug('[+] Starting transformations ... ')
    while True:
        # Transformation 001
        (calls, has_changes) = __transform_001(calls)
        if not has_changes:
            break
        # Transformation 002
        calls = __transform_002(calls)

    logger.debug('[+] Amount of API calls after transformations: %d', len(calls))
    logger.debug('[+] Expanding list ... ')

    calls_expanded = []
    for c in calls:
        calls_expanded += __expand_element(c[1])

    return calls_expanded

def main(argv):
    calls = [
        'call_0', 'call_1', 'call_2', 'call_2', 'call_2', 'call_2', \
        'call_0', 'call_1', 'call_2', 'call_2', 'call_2', 'call_2'
    ]

    print(calls)
    compressed_calls = __compress_calls(calls)
    print(compressed_calls)

if __name__ == "__main__": 
    sys.exit(main(sys.argv))
