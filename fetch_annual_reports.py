# -*- coding: utf-8 -*-
"""
下载年报到本地
"""
import os
import config

from SECEdgar.filings import Filing, FilingType


if __name__ == '__main__':
    REPORT_DIR = os.path.join(config.BASE_FOLDER, 'reports')

    for com_info in config.COMPANIES:
        # if com_info['name'] in ['Merck', 'BMS', 'Gilead', 'lilly']:
        #     continue

        filings = Filing(
            cik=com_info['cik'],
            filing_type=FilingType.FILING_10K)

        com_report_folder = os.path.join(REPORT_DIR, com_info['name'])
        filings.save(com_report_folder)
