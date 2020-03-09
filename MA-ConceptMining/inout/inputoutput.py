import sqlite3 as sql
import re
import csv


# def write_dict(dict, file):
#
#     fo = open(file, "w", encoding="utf8")
#
#     entries = sorted(dict.items(), key=lambda kv: kv[1], reverse=True)
#     for k,v in entries:
#         to_write = k + ' ' + str(v) + '\n'
#         fo.write(to_write)
#
#     fo.close()


# def write_db(job_ads, file):
#     conn = sql.connect(file)
#
#     sql_create_tabel = """ CREATE TABLE IF NOT EXISTS jobs_textkernel (
#                                 ID INTEGER PRIMARY KEY,
#                                 ZEILENNR text,
#                                 Jahrgang text,
#                                 LANG text,
#                                 STELLENBESCHREIBUNG text NOT NULL,
#                                 ORIG text
#                             ); """
#
#     c = conn.cursor()
#     c.execute(sql_create_tabel)
#
#     del_sql = 'DELETE FROM jobs_textkernel'
#
#     c.execute(del_sql)
#
#     for job in job_ads:
#         content = (job.id, job.id, '2017', str(job.lang), str(job.content), str(job.orig_content))
#         try:
#             c.execute('insert into jobs_textkernel(ID, ZEILENNR, Jahrgang, LANG, STELLENBESCHREIBUNG, ORIG) values (?,?,?,?,?,?)', content)
#         except:
#             print('id: ', job.id, ' failed')
#
#     conn.commit()
#     conn.close()


def read_file_by_line(file, only_unigrams):

    word_list = list()
    with open(file, mode='r', encoding='utf-8') as f:
        for line in f:
            line = line.strip()
            if only_unigrams:
                if ' ' not in line:
                    word_list.append(line)
            else:
                word_list.append(line)
    return word_list


def read_esco_csv(file, only_unigrams, synsets):

    if synsets:
        synset_list = list()
    else:
        skills = list()

    with open(file, newline='', encoding='utf-8') as csvfile:
        reader = csv.reader(csvfile, delimiter=',', quotechar='"')

        next(reader, None) # skip header
        rows = 0
        for row in reader:
            rows += 1
            pref_label = row[4]
            alt_labels = row[5]

            synset = set()

            if ' ' not in pref_label:
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


def read_ams(file, level, only_unigrams):

    word_list = dict()

    conn = sql.connect(file)
    if level == 1:
        sql_select = """SELECT Competence, FirstLevel FROM Categories"""
    elif level == 2:
        sql_select = """SELECT Competence, SecondLevelCategory FROM Categories"""
    else:
        sql_select = """SELECT Competence, ThirdLevelCategory FROM Categories"""
    c = conn.cursor()
    c.execute(sql_select)

    rows = c.fetchall()

    for r in rows:
        comp = r[0]
        cat = r[1]
        if only_unigrams:
            if ' ' not in comp:
                word_list[comp] = cat
        else:
            word_list[comp] = cat

    return word_list


# def read_skillmatches(file):
#     conn = sql.connect(file)
#
#     sql_select = """SELECT Zeilennr, Sentence, Comp FROM Competences"""
#     c = conn.cursor()
#     c.execute(sql_select)
#     rows = c.fetchall()
#
#     sentences = list()
#     for r in rows:
#         sentences.append((r[1], r[2], r[0]))
#
#     return sentences


def read_jobads_content(file):
    conn = sql.connect(file)

    sql_select = """SELECT STELLENBESCHREIBUNG FROM jobs_textkernel"""
    c = conn.cursor()
    c.execute(sql_select)

    rows = c.fetchall()

    jobs = list()

    for r in rows:
        jobs.append(r[0])

    return jobs


class JobAd:
    def __init__(self, id, orig_content, content, lang):
        self.id = id
        self.orig_content = orig_content
        self.content = content
        self.lang = lang


# def process_job_ad(text):
#
#     pattern = "\*REPLACEDREPLACED\*"
#     text = re.sub(pattern, '', text, flags=re.S)
#     text = text.strip()
#
#     # identifies unimportant part of job ad at the end of text
#     pattern = "\sJetzt bewerben( Ähnliche Jobs)?\s+(.*)"
#     found = re.search(pattern, text, flags=re.S)
#     if found:
#         start = found.start()
#         end = found.end()
#         length = len(text)
#
#         rel = start / length
#         if rel > 0.5: # if "Jetzt bewerben" appears in the second half
#             text = re.sub(pattern, '', text)
#
#     text = text.strip()
#     return text


# def read_skill_set(file):
#
#     skill_list = list()
#
#     with open(file, newline='', encoding='utf-8') as csvfile:
#         reader = csv.reader(csvfile, delimiter=',', quotechar='"')
#
#         next(reader, None) # skip header
#         rows = 0
#         for row in reader:
#             rows += 1
#             pref_label = row[4]
#             alt_labels = row[5]
#
#             if ' ' not in pref_label:
#                 pref_label = pref_label.lower()
#                 skill_list.append(pref_label)
#             if len(alt_labels) > 0:
#                 label_list = alt_labels.split('\n')
#                 for l in label_list:
#                     if ' ' not in l:
#                         l = l.lower()
#                         skill_list.append(l)
#
#     return skill_list


# def read_jobad_csv(file, keyword):
#     langs = set()
#     job_ads = set()
#
#     missing = 0
#
#     with open(file, newline='', encoding='utf-8') as csvfile:
#         reader = csv.reader(csvfile, delimiter=';', quotechar='"')
#
#         rows = 0
#
#         for row in reader:
#             rows += 1
#
#             id = row[0]
#
#             if id == "":
#                 continue
#             lang = row[1]
#             langs.add(lang)
#             job_ad = row[2].strip()
#
#             cleaned = process_job_ad(job_ad)
#             if len(cleaned) > 0:
#                 ad = JobAd(id, orig_content=job_ad, content=cleaned, lang=lang)
#                 job_ads.add(ad)
#             else:
#                 missing += 1
#
#     print('Anzeigen gesamt: ', rows, ' -- ',missing, ' missing')
#     return job_ads
