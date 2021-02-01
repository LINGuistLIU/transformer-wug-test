"""
generate random strings by uniformly sampling from the set of 2-, 3- and 4-grams,
and add them to the training set
"""

import os, random

random.seed(1)

def get_char_set(fname):
    char_set = set()
    msd_set = set()
    with open(fname) as f:
        for line in f:
            line = line.strip()
            if line != "":
                lemma, form, msd = line.split("\t")
                lemma = lemma.strip().replace(" ", "_")
                form = form.strip().replace(" ", "_")
                msd = msd.strip().replace(" ", "_")
                for char in lemma:
                    char_set.add(char)
                for char in form:
                    char_set.add(char)
                msd_set.add(msd)
    return char_set, msd_set

def get_set_diff(set1, set2):
    """
    return a set of items in set1 but not in set2
    """
    uniqset = set()
    for item in set1:
        if item not in set2:
            uniqset.add(item)
    # print(uniqset)
    return uniqset

def make_random_strings_from_trainsubsequence(fname_train, fname_out):

    char_set = set()
    maxlen = 0
    minlen = 1000
    with open(fname_train) as f:
        for line in f:
            line = line.strip()
            if line != "":
                lemma, form, msd = line.split("\t")
                lemma = lemma.strip().replace(" ", "_")
                form = form.strip().replace(" ", "_")
                msd = msd.strip().replace(" ", "_")
                if len(lemma) > 1:
                    for item in zip(lemma, lemma[1:]): # bigrams
                        char_set.add("".join(item))
                if len(lemma) > 2:
                    for item in zip(lemma, lemma[1:], lemma[2:]): # trigram
                        char_set.add("".join(item))
                if len(lemma) > 3:
                    for item in zip(lemma, lemma[1:], lemma[2:], lemma[4:]): # 4-gram
                        char_set.add("".join(item))

                if len(form) > 1:
                    for item in zip(form, form[1:]): # bigrams
                        char_set.add("".join(item))
                if len(form) > 2:
                    for item in zip(form, form[1:], form[2:]): # trigram
                        char_set.add("".join(item))
                if len(form) > 3:
                    for item in zip(form, form[1:], form[2:], form[4:]): # 4-gram
                        char_set.add("".join(item))

                # for char in form:
                #     char_set.add(char)
                if len(lemma) > maxlen:
                    maxlen = len(lemma)
                if len(form) > maxlen:
                    maxlen = len(form)
                if len(lemma) < minlen:
                    minlen = len(lemma)
                if len(form) < minlen:
                    minlen = len(form)

    # print(maxlen, minlen, char_set)
    charlist = list(char_set)
    print(charlist)
    num = len(charlist) - 1
    fakecount = 0
    with open(fname_out, "w") as fw:
        while fakecount < 20000:
            length = random.randint(minlen, maxlen)
            clist = []
            while len(clist) < length:
                clist.extend(list(charlist[random.randint(0, num)]))
            # print(fakecount, clist)
            fw.write("".join(clist) + "\n")
            fakecount += 1

def make_random_strings_from_allsubsequence(fname_train, fname_dev, fname_test, fname_out):
    char_set = set()
    maxlen = 0
    minlen = 1000
    with open(fname_train) as f, open(fname_dev) as fdev, open(fname_test) as ftest:
        lines = [line for line in f] + [line for line in fdev] + [line for line in ftest]
        for line in lines:
            line = line.strip()
            if line != "":
                lemma, form, msd = line.split("\t")
                lemma = lemma.strip().replace(" ", "_")
                form = form.strip().replace(" ", "_")
                msd = msd.strip().replace(" ", "_")
                if len(lemma) > 1:
                    for item in zip(lemma, lemma[1:]):  # bigrams
                        char_set.add("".join(item))
                if len(lemma) > 2:
                    for item in zip(lemma, lemma[1:], lemma[2:]):  # trigram
                        char_set.add("".join(item))
                if len(lemma) > 3:
                    for item in zip(lemma, lemma[1:], lemma[2:], lemma[4:]):  # 4-gram
                        char_set.add("".join(item))

                if len(form) > 1:
                    for item in zip(form, form[1:]):  # bigrams
                        char_set.add("".join(item))
                if len(form) > 2:
                    for item in zip(form, form[1:], form[2:]):  # trigram
                        char_set.add("".join(item))
                if len(form) > 3:
                    for item in zip(form, form[1:], form[2:], form[4:]):  # 4-gram
                        char_set.add("".join(item))

                # for char in form:
                #     char_set.add(char)
                if len(lemma) > maxlen:
                    maxlen = len(lemma)
                if len(form) > maxlen:
                    maxlen = len(form)
                if len(lemma) < minlen:
                    minlen = len(lemma)
                if len(form) < minlen:
                    minlen = len(form)

    # print(maxlen, minlen, char_set)
    charlist = list(char_set)
    print(charlist)
    num = len(charlist) - 1
    fakecount = 0
    with open(fname_out, "w") as fw:
        while fakecount < 20000:
            length = random.randint(minlen, maxlen)
            clist = []
            while len(clist) < length:
                clist.extend(list(charlist[random.randint(0, num)]))
            # print(fakecount, clist)
            fw.write("".join(clist) + "\n")
            fakecount += 1

def _format_test_dev(fname, fname_in, fname_out):
    with open(fname) as f, open(fname_in, "w") as fwin, open(fname_out, "w") as fwout:
        for line in f:
            line = line.strip()
            if line != "":
                lemma, form, msd = line.split("\t")
                lemma = lemma.strip().replace(" ", "_")
                form = form.strip().replace(" ", "_")
                msd = msd.strip().replace(" ", "_")

                input = list(lemma) + msd.split(";")
                output = list(form)

                fwin.write(" ".join(input) + "\n")
                fwout.write(" ".join(output) + "\n")

def format_data(fname_train, fname_dev, fname_test, fname_randstr, outdir, lang, augsize):
    os.makedirs(outdir, exist_ok=True)
    ftrain_in = os.path.join(outdir, "train." + lang + ".input")
    ftrain_out = os.path.join(outdir, "train." + lang + ".output")

    fdev_in = os.path.join(outdir, "dev." + lang + ".input")
    fdev_out = os.path.join(outdir, "dev." + lang + ".output")

    ftest_in = os.path.join(outdir, "test." + lang + ".input")
    ftest_out = os.path.join(outdir, "test." + lang + ".output")

    _format_test_dev(fname_dev, fdev_in, fdev_out)
    _format_test_dev(fname_test, ftest_in, ftest_out)

    with open(fname_train) as ftrain, open(fname_randstr) as frandstr, open(ftrain_in, "w") as fwin, open(ftrain_out, "w") as fwout:
        for line in ftrain:
            line = line.strip()
            if line != "":
                lemma, form, msd = line.split("\t")
                lemma = lemma.strip().replace(" ", "_")
                form = form.strip().replace(" ", "_")
                msd = msd.strip().replace(" ", "_")

                input = list(lemma) + msd.split(";")
                output = list(form)

                fwin.write(" ".join(input) + "\n")
                fwout.write(" ".join(output) + "\n")
        count = 0
        for line in frandstr:
            if count < augsize:
                line = line.strip()
                input = list(line) + ["COPY"]
                output = list(line)
                fwin.write(" ".join(input) + "\n")
                fwout.write(" ".join(output) + "\n")
                count += 1
            else:
                break



def main_random_string_with_training_subsequence():
    """
    generate random strings from 2, 3, 4 subsequences from the training set.
    """
    rootdir = "PATH_TO_DIRECTORY_WHERE_DATA_IS_STORED"
    datadir = os.path.join(rootdir, "2018-languages/wug_test_full_tables")
    langlist = ["czech", "finnish", "german", "russian", "spanish", "turkish"]

    outdir = os.path.join(rootdir, "full_table_experiment/randstr_from_trainsubsequence")

    for lang in langlist:
        print(lang)
        fname_train = os.path.join(datadir, lang +".train")

        outdir_now = os.path.join(outdir, lang)
        os.makedirs(outdir_now, exist_ok=True)

        fname_out = os.path.join(outdir_now, lang+".randstr.trainsubsequence")
        make_random_strings_from_trainsubsequence(fname_train, fname_out)


def main_format_data():
    """
    generate random strings from characters in train, dev and test.
    """
    rootdir = "PATH_TO_DIRECTORY_WHERE_DATA_IS_STORED"
    datadir = os.path.join(rootdir, "wug_test_full_tables")
    dev_test_dir = os.path.join(rootdir, "conll2018/task1")
    langlist = ["czech", "finnish", "german", "russian", "spanish", "turkish"]

    lang2dir = {"czech": "all",
                "finnish": "all",
                "german": "surprise",
                "russian": "surprise",
                "spanish": "all",
                "turkish": "all"}

    trainchar_dir = os.path.join(rootdir, "full_table_experiment/randstr_from_trainsubsequence")

    out_traincharADD = os.path.join(rootdir, "full_table_experiment/data_full_table_randstr_from_trainsubsequence2k")

    for lang in langlist:
        print(lang)
        fname_train = os.path.join(datadir, lang + ".train")
        fname_dev = os.path.join(dev_test_dir, lang2dir[lang], lang + "-dev")
        fname_test = os.path.join(dev_test_dir, lang2dir[lang], lang + "-test")

        fname_randstr_trainchar = os.path.join(trainchar_dir, lang, lang+".randstr.trainsubsequence")

        out_traincharADD_now = os.path.join(out_traincharADD, lang)
        os.makedirs(out_traincharADD_now, exist_ok=True)
        format_data(fname_train, fname_dev, fname_test, fname_randstr_trainchar, out_traincharADD_now, lang, augsize=2000)


def main_random_string_with_training_subsequence_niger_congo5fold():
    """
    generate random strings from 2-, 3-, 4-grams from the training set.
    """
    rootdir = "PATH_TO_DIRECTORY_WHERE_DATA_IS_STORED"
    datadir = os.path.join(rootdir, "niger-congo_languages/wug_test_full_tables")
    langlist = ["aka", "gaa", "lin", "nya", "sot", "swa"]

    outdir = os.path.join(rootdir, "full_table_experiment/niger_congo_5fold/randstr_from_trainsubsequence")

    for fold in [str(i) for i in range(1, 6)]:
        datadir_fold = datadir + fold
        for lang in langlist:
            langfold = lang + fold
            print(fold, lang)
            fname_train = os.path.join(datadir_fold, langfold, "train." + langfold)

            outdir_now = os.path.join(outdir, langfold)
            os.makedirs(outdir_now, exist_ok=True)
            fname_out = os.path.join(outdir_now, langfold + ".randstr.trainsubsequence")
            make_random_strings_from_trainsubsequence(fname_train, fname_out)


def main_format_data_niger_congo5fold():
    """
    generate random strings from characters in train, dev and test.
    """
    rootdir = "PATH_TO_DIRECTORY_WHERE_DATA_IS_STORED"
    datadir = os.path.join(rootdir, "niger-congo_languages/niger_congo_data")
    langlist = ["aka", "gaa", "lin", "nya", "sot", "swa"]

    trainchar_dir = os.path.join(rootdir, "full_table_experiment/niger_congo_5fold/randstr_from_trainsubsequence")

    for fold in [str(i) for i in range(1, 6)]:
        # -----------2k-----------------
        out_traincharADD = os.path.join(rootdir,
                                        "full_table_experiment/niger_congo_5fold/data_niger_congo_randstr_from_trainsubsequence2k")
        for lang in langlist:
            print(lang)
            langfold = lang + fold
            fname_train = os.path.join(datadir + fold, langfold, "train." + langfold)
            fname_dev = os.path.join(datadir + fold, langfold, "dev." + langfold)
            fname_test = os.path.join(datadir + fold, langfold, "test." + langfold)

            fname_randstr_trainchar = os.path.join(trainchar_dir, langfold, langfold + ".randstr.trainsubsequence")

            out_traincharADD_now = os.path.join(out_traincharADD, langfold)
            os.makedirs(out_traincharADD_now, exist_ok=True)
            format_data(fname_train, fname_dev, fname_test, fname_randstr_trainchar, out_traincharADD_now, langfold,
                        augsize=2000)


if __name__ == "__main__":
    # main_random_string_with_training_subsequence()
    # main_format_data()

    main_random_string_with_training_subsequence_niger_congo5fold()
    main_format_data_niger_congo5fold()