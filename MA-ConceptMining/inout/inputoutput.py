import sqlite3 as sql
import re
import csv


def read_file_by_line(file):

    """
    reads a text file line by line
    :param file: path to file
    :return: list of all lines
    """

    word_list = list()
    with open(file, mode='r', encoding='utf-8') as f:
        for line in f:
            line = line.strip()
            word_list.append(line)
    return word_list


def read_esco_csv(file, only_unigrams, synsets):
    """
    reads a csv file containing esco skills
    :param file: path to file
    :param only_unigrams: True if you only want to collect unigram skills
    :param synsets: True if you want to group skills by synsets
    :return: list of skills or list of synsets
    """

    if synsets:
        synset_list = list()
    else:
        skills = list()

    with open(file, newline='', encoding='utf-8') as csvfile:
        reader = csv.reader(csvfile, delimiter=',', quotechar='"')

        next(reader, None) # skip header

        for row in reader:
            pref_label = row[4]
            alt_labels = row[5]

            synset = set()

            if only_unigrams:
                if ' ' not in pref_label:
                    synset.add(pref_label)
            else:
                synset.add(pref_label)
            if len(alt_labels) > 0:
                label_list = alt_labels.split('\n')
                for l in label_list:
                    if only_unigrams:
                        if ' ' not in l:
                            synset.add(l)
                    else:
                        synset.add(l)

            if synsets:
                if len(synset) > 1: # process only synset with more than one member
                    synset_list.append(synset)
            else:
                skills.extend(synset)

    if synsets:
        return synset_list
    else:
        return skills


def read_ams_synsets(file, only_unigrams, synsets):
    """

    :param file:
    :param only_unigrams:
    :param synsets:
    :return:
    """

    conn = sql.connect(file)
    sql_select = """SELECT Synonyms, Orig_String FROM Categories"""
    c = conn.cursor()
    c.execute(sql_select)

    rows = c.fetchall()

    if synsets:
        synsets = set()
        for r in rows:
            syns = r[0]
            comp = r[1]

            if syns is None:
                continue

            # collect als synonyms that are single-word-expressions
            synset = set([s.lower() for s in syns.split(' | ') if ' ' not in s])
            if only_unigrams:
                if ' ' not in comp:
                    synset.add(comp.lower())
            else:
                synset.add(comp.lower())

            if len(synset) > 1:
                synsets.add(tuple(synset))

        c.close()
        return synsets
    else:
        skills = list()
        for r in rows:
            comp = r[1]
            if only_unigrams:
                if ' ' not in comp:
                    skills.append(comp.lower())
            else:
                skills.append(comp.lower())
        c.close()
        return skills


def read_jobads_content(file):
    """
    reads all jobads from given sqlite file
    :param file: path to file
    :return: list of all jobads
    """
    conn = sql.connect(file)

    sql_select = """SELECT STELLENBESCHREIBUNG FROM jobs_textkernel"""
    c = conn.cursor()
    c.execute(sql_select)

    rows = c.fetchall()

    jobs = list()

    for r in rows:
        jobs.append(r[0])

    return jobs
