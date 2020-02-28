# -*- coding: utf-8 -*-

import os

BASE_FOLDER = os.path.dirname(__file__)

IGNORE_WORDS = [
    'revenues',
    'Revenues',
    'Revenue',
    'Other',
    'Product',
    'product',
    'Total',
    'total',
    'Livestock',
    'United States',
    'Europe',
    'World',
    'revenue'
]

COMPANIES = [
    {
        'name': 'Merck',
        'cn_name': '默沙东',
        'cik': '0000310158',
        'company_code': 'MRK',
        'drug_data_titles': [
            'Sales of the Company’s products were as follows:'
        ],
        'year_col_patterns': [
            r'(\d{4})',
            r'Total\.(\d{4})'
        ],
        'ignore_words': IGNORE_WORDS
    },
    {
        'name': 'BMS',
        'cn_name': 'BMS',
        'cik': '0000014272',
        'company_code': 'BMS',
        'drug_data_titles': [
            'Total revenues of key products were as follows:',
            'Product revenues were as follows:',
            'Product revenues and the composition of total revenues were as follows:',
            'The following table summarizes the disaggregation of revenue by product and region:'
        ],
        'year_col_patterns':[
                r'(\d{4})\.Year'
                # r'(\d{4})\.Year Ended December 31,'
        ],
        'ignore_words': IGNORE_WORDS
    },
    {
        'name': 'Gilead',
        'cn_name': '吉利德科学',
        'cik': '0000882095',
        'company_code': 'GILD',
        'drug_data_titles': [
            'The following table summarizes the period-over-period changes in our product sales:',
            'The following table summarizes the period over period changes in our product sales:',
            # 'The following table lists aggregate product sales for our major products (in thousands):'
        ],
        'year_col_patterns': [
            r'(\d{4})',
        ],
        'ignore_words': IGNORE_WORDS,
        'year_in_thousand': [
            2013,
            2012,
            2011
        ]
    },
    {
        'name': 'lilly',
        'cn_name': '礼来',
        'cik': '0000059478',
        'company_code': 'LLY',
        'drug_data_titles': [
            r'The following table summarizes our revenue activity in \d{4} compared with \d{4}:',
        ],
        'year_col_patterns': [
            r'(\d{4})',
            r'Total.Year Ended.December 31, (\d{4})'
        ],
        'ignore_words': IGNORE_WORDS
    },
    {
        'name': 'amgen',
        'cn_name': '安进',
        'cik': '0000318154',
        'company_code': 'AMGN',
        'drug_data_titles': [
            r'Worldwide product sales were as follows \(dollar amounts in millions\):',
        ],
        'year_col_patterns': [
            r'(\d{4})',
        ],
        'ignore_words': IGNORE_WORDS
    },
    {
        'name': 'regeneron',
        'cn_name': '再生元',
        'cik': '0000872589',
        'company_code': 'REGN',
        'drug_data_titles': [
            r'Net Product Sales of Regeneron-Discovered Products',
        ],
        'year_col_patterns': [
            r'(\d{4})'
        ],
        'ignore_words': IGNORE_WORDS
    },
    # {
    #     'name': 'ABBV',     # table 格式不匹配
    #     'cn_name': '艾伯维',
    #     'cik': '0001551152',
    #     'company_code': 'ABBV',
    #     'drug_data_titles': [
    #         'The following tables detail AbbVie\'s worldwide net revenues:',
    #     ],
    #     'year_col_patterns': [
    #         r'(\d{4})',
    #     ],
    #     'ignore_words': IGNORE_WORDS
    # },
    # {
    #     'name': 'Pfizer',     # table 格式不匹配
    #     'cn_name': '辉瑞',
    #     'cik': '',
    #     'company_code': 'PFE',
    #     'drug_data_titles': [
    #         'Net Product Sales of Regeneron-Discovered Products',
    #     ],
    #     'year_col_patterns': [
    #         r'Total.(\d{4})'
    #     ],
    #     'ignore_words': IGNORE_WORDS
    # },
    {
        'name': 'BioMarin',
        'cn_name': '拜玛林制药',
        'cik': '1048477',
        'company_code': 'BMRN',
        'drug_data_titles': [
            'Net Product Revenues related to our major commercial products consisted of the following:',
            'A summary of our various commercial products, including key metrics',
            'Net product revenues consisted of the following (in millions):'
        ],
        'year_col_patterns': [
            r'(\d{4})'
        ],
        'ignore_words': IGNORE_WORDS
    },
]