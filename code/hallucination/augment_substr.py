"""
The data hallucination method we propose:
substring-based data hallucination
"""

import os, sys, argparse, re
import align
from random import choice
import random

def read_data(filename):
    with open(filename) as f:
        lines = f.readlines()
    inputs = []
    outputs = []
    tags = []
    for line in lines:
        line = line.strip().split("\t")
        if len(line) == 3:
            inputs.append(list(line[0].strip()))
            outputs.append(list(line[1].strip()))
            tags.append(line[2].strip().split(";"))
    return inputs, outputs, tags

def find_good_range(a, b):
    # print(b)
    mask = [(a[i] == b[i] and a[i] != u" ") for i in range(len(a))]

    if sum(mask) == 0:
        # return []
        # Some times the alignment is off-by-one
        b = [' '] + b
        mask = [(a[i] == b[i] and a[i] != u" ") for i in range(len(a))]

    ranges = []
    prev = False
    for i, k in enumerate(mask):
        if k and prev:
            prev = True
        elif k and not prev:
            start = i
            prev = True
        elif prev and not k:
            end = i
            ranges.append((start, end))
            prev = False
        elif not prev and not k:
            prev = False
    if prev:
        ranges.append((start, i + 1))
    ranges = [c for c in ranges if c[1] - c[0] > 2]
    # print(a)
    # print(b)
    # print(mask)
    # print(ranges)
    # print()
    return ranges, sum(mask) == 0

def augment(inputs, outputs, tags, characters):
    """
    This function is modified to augment with subsequences
    """
    temp = [(''.join(inputs[i]), ''.join(outputs[i])) for i in range(len(outputs))]
    aligned = align.Aligner(temp, align_symbol=' ').alignedpairs

    vocab = list(characters)
    try:
        vocab.remove(u" ")
    except:
        pass

    new_inputs = []
    new_outputs = []
    new_tags = []
    count_empty = 0
    count_valid = 0

    count_disjoint = 0
    for k, item in enumerate(aligned):
        #print(''.join(inputs[k]) + '\t' + ''.join(outputs[k]))
        i, o = item[0], item[1]
        # print(tags[k])
        # print(i)
        # print(o)

        # if type(i) != list or type(o) != list:
        #     print(i)
        #     print(o)
        #     print()
        good_range, empty = find_good_range(i, o)
        # print(good_range)
        # print()

        if empty:
            count_empty += 1
        else:
            count_valid += 1

        if len(good_range) > 1:
            count_disjoint += 1
            # print("longer than 1:", len(good_range))
            # print(i)
            # print(o)
            # print(good_range)
            # print()

        if good_range:
            new_i, new_o = list(i), list(o)
            # print("new i:", new_i)
            # print("new o:", new_o)
            # print()
            good_range = [good_range[0]]
            for r in good_range:
                s = r[0] # start id
                e = r[1] # end id
                # print(s, e)
                new_i_prefix, new_i_suffix = i[:s], i[e:]
                new_o_prefix, new_o_suffix = o[:s], o[e:]
                strlen = random.randint(3, 10)
                # if len(good_range) == 1:
                if random.random() > 0.8:
                    strlen = random.randint(1, 20)
                fakestr = ""
                while len(fakestr) < strlen:
                    fakestr += choice(vocab)
                new_i = new_i_prefix + list(fakestr) + new_i_suffix
                new_o = new_o_prefix + list(fakestr) + new_o_suffix
                # print(new_i)
                # print(new_o)

            new_i1 = [c for l,c in enumerate(new_i) if (c.strip() or (new_o[l]==' ' and new_i[l] == ' '))]
            new_o1 = [c for l,c in enumerate(new_o) if (c.strip() or (new_i[l]==' ' and new_o[l] == ' '))]
            # print(new_i1)
            # print(new_o1)

            new_inputs.append(new_i1)
            new_outputs.append(new_o1)
            new_tags.append(tags[k])
        else:
            new_inputs.append([])
            new_outputs.append([])
            new_tags.append([])
    # print("count emtpy:", count_empty, "count valid:", count_valid)
    # print("disjoint lemma:", count_disjoint)
    # print()
    return new_inputs, new_outputs, new_tags

def get_chars(l):
    flat_list = [char for word in l for char in word]
    return list(set(flat_list))

def get_ngrams(l):
    ngram_set = set()
    for charlist in l:
        for word in "".join(charlist).strip().split(" "):
            for item in zip(word, word[1:]): # bigram
                ngram_set.add("".join(item))
            for item in zip(word, word[1:], word[2:]): # trigram
                ngram_set.add("".join(item))
            for item in zip(word, word[1:], word[2:], word[3:]): # 4-gram
                ngram_set.add("".join(item))
    return list(ngram_set)


def main():
    parser = argparse.ArgumentParser()
    parser.add_argument("--datapath", help="path to data", default="example_data", type=str)
    parser.add_argument("--language", help="language", default="finnish", type=str)
    parser.add_argument("--examples", help="number of hallucinated examples to create (def: 100)", default=100, type=int)
    parser.add_argument("--use_dev", help="whether to use the development set (def: False)", action="store_true")
    args = parser.parse_args()

    DATA_PATH = args.datapath
    L2 = args.language
    LOW_PATH = os.path.join(DATA_PATH, L2+".trn")

    N = args.examples
    usedev = args.use_dev

    lowi, lowo, lowt = read_data(LOW_PATH)

    if usedev:
        DEV_PATH = os.path.join(DATA_PATH, L2 + ".dev")
        devi, devo, devt = read_data(DEV_PATH)
        vocab = get_ngrams(lowi + lowo + devi + devo)
    else:
        vocab = get_ngrams(lowi + lowo)
    # print(vocab)

    i, o, t = [], [], []
    while len(i) < N:
        if usedev:
            # Do augmentation also using examples from dev
            ii,oo,tt = augment(devi+lowi, devo+lowo, devt+lowt, vocab)
        else:
            # Just augment the training set
            ii,oo,tt = augment(lowi, lowo, lowt, vocab)
        ii = [c for c in ii if c]
        oo = [c for c in oo if c]
        tt = [c for c in tt if c]
        i += ii
        o += oo
        t += tt
        if len(ii) == 0:
            break

    # Wait is this needed?
    i = [c for c in i if c]
    o = [c for c in o if c]
    t = [c for c in t if c]

    with open(os.path.join(DATA_PATH,L2+".hall.substr"), 'w') as outp:
        for k in range(min(N, len(i))):
            outp.write(''.join(i[k]) + '\t' + ''.join(o[k]) + '\t' + ';'.join(t[k]) + '\n')


if __name__ == "__main__":
    main()
