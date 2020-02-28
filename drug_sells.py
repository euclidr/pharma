# -*- coding: utf-8 -*-

import config
import json
import os
import re

from collections import defaultdict
from typing import List
from os.path import join
from table import extract_tables, Table
from submission_text import SubmissionText


def config_of_company(company: str) -> dict:
    for conf in config.COMPANIES:
        if conf['name'] == company:
            return conf

class DrugTable(object):

    @classmethod
    def search_drug_table(cls, company: str, tables: List[Table]) -> Table:
        conf = config_of_company(company)
        titles = conf['drug_data_titles']
        for table in tables:
            if not table.is_valid:
                continue
            for title in titles:
                if re.search(title, table.title):
                    return table
                if re.search(title, table.all_text()):
                    return table

def is_float(str):
    try:
        float(str)
        return True
    except Exception:
        return False


def clean_stat(stat, ignore_words):
    """清理数据，去掉非药物，或者无数据的"""
    result = {}
    for k, v in stat.items():
        fit = True
        for w in ignore_words:
            if w in k:
                fit = False
                break

        v = v.replace('$', '')
        v = v.replace(',', '')
        v = v.strip()

        if is_float(v) and fit:
            # 忽略括号中的名字
            k = re.sub(r'\(.*\)', '', k)
            k = k.replace('\u00a0', ' ')
            k = k.replace('*', '')
            k = k.replace('  ', ' ')
            k = k.replace('global', '')
            k = k.strip()
            result[k] = v

    return result


if __name__ == '__main__':
    drug_tables = {}
    drug_stats = defaultdict(dict)
    for conf in config.COMPANIES:
        company = conf['name']

        # if company != 'regeneron':
        #     continue

        folder = join(config.BASE_FOLDER, 'reports', company)
        for root, _, filenames in os.walk(folder):
            for filename in filenames:
                print(filename)
                st = SubmissionText(
                    conf['cik'],
                    conf['name'],
                    join(root, filename)
                )
                file_10k = st.get_file_10k()
                if not file_10k:
                    print(conf['name'], filename, 'is missing 10-K doc')
                    continue

                year = st.year

                file_10k.save_in_folder(join(config.BASE_FOLDER, 'tmp', company, year))

                tables = extract_tables(file_10k.text)

                # print(company, year, tables)
                # for table in tables:
                #     print(table.all_text()[:120])

                drug_table = DrugTable.search_drug_table(company, tables)
                if drug_table:
                    key = '{}_{}'.format(company, year)
                    drug_tables[key] = drug_table

                    for pattern in conf['year_col_patterns']:
                        stat = drug_table.extract_data(pattern)
                        stat = clean_stat(stat, conf['ignore_words'])
                        drug_stats[company].update(stat)

    for key, stat in drug_tables.items():
        print('---------------------------------')
        print('report: ', key)
        stat.peek()
        print('---------------------------------')

    with open('result.json', 'w') as fw:
        fw.write(json.dumps(drug_stats, indent=4))


    # for root, _, files in os.walk(config.BASE_FOLDER):
    #     print(root)
    #     print('--------')
    #     print(folders)
    #     print('--------')
    #     print(files)
