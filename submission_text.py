# -*- coding: utf-8 -*-
"""
解析年报 submission_text 文件
"""

import re
import os

from os.path import join
from typing import List


class SECFile(object):

    def __init__(self,
            filename,
            text,
            file_type,
            sequence=0,
            description=''):
        self.filename = filename
        self.text = text
        self.file_type = file_type
        self.sequence = sequence
        self.description = description

    def save_in_folder(self, folder):
        if not os.path.exists(folder):
            os.makedirs(folder)
        path = join(folder, self.filename)
        with open(path, 'w') as f:
            f.write(self.text)


class SubmissionText(object):

    MK_SEC_DOCUMENT_BEGIN = '<SEC-DOCUMENT>'
    MK_SEC_HEADER_BEGIN = '<SEC-HEADER>'
    MK_SEC_HEADER_END = '</SEC-HEADER>'
    MK_DOCUMENT_BEGIN = '<DOCUMENT>'
    MK_DOCUMENT_END = '</DOCUMENT>'
    MK_TEXT_BEGIN = '<TEXT>'
    MK_TEXT_END = '</TEXT>'

    def __init__(self, cik, name, file_path):
        self.cik = cik
        self.name = name
        self.file_path = file_path

        self.child_files = []  # type: List[SECFile]
        self.submission_header = []  # type: List[str]

        self.parse()

    def parse(self):
        lines = []
        with open(self.file_path) as file:
            lines = [line for line in file]

        line_idx = 0
        while line_idx < len(lines):
            line = lines[line_idx]

            if line.startswith(self.MK_SEC_DOCUMENT_BEGIN):
                line_idx = self.parse_sec_document(lines, line_idx)
            elif line.startswith(self.MK_SEC_HEADER_BEGIN):
                line_idx = self.parse_sec_header(lines, line_idx)
            elif line.startswith(self.MK_DOCUMENT_BEGIN):
                line_idx = self.parse_document(lines, line_idx)
            else:
                line_idx += 1

    @property
    def conformed_period(self):
        for line in self.submission_header.split('\n'):
            if 'CONFORMED PERIOD OF REPORT' in line:
                return line.split(':')[1].strip()

    @property
    def year(self):
        period = self.conformed_period
        print(self.conformed_period)
        if period:
            return period[:4]

    def print_child_files(self):
        for child_file in self.child_files:
            print('{} - {}'.format(
                child_file.filename,
                child_file.file_type
            ))

    def get_file_10k(self):
        for child_file in self.child_files:
            if child_file.file_type == '10-K':
                return child_file

    def parse_sec_document(self, lines, line_idx):
        assert lines[line_idx].startswith(self.MK_SEC_DOCUMENT_BEGIN)

        line = lines[line_idx]
        sec_doc_info = line[len(self.MK_SEC_DOCUMENT_BEGIN):]
        segments = sec_doc_info.split(':')
        segments = [s.strip() for s in segments]

        self.submission_text_file_name = segments[0]

        if len(segments) > 1:
            self.submission_date_int = int(segments[1])

        return line_idx + 1

    def parse_sec_header(self, lines, line_idx):
        assert lines[line_idx].startswith(self.MK_SEC_HEADER_BEGIN)

        first_line = lines[line_idx]
        contents = first_line[len(self.MK_SEC_HEADER_BEGIN):]
        line_idx += 1
        while not lines[line_idx].startswith(self.MK_SEC_HEADER_END):
            contents += lines[line_idx]
            line_idx += 1

        self.submission_header = contents

        return line_idx

    def parse_document(self, lines, line_idx):
        assert lines[line_idx].startswith(self.MK_DOCUMENT_BEGIN)

        line_idx += 1

        info = {}
        file_type = None
        sequence = 0
        filename = None
        description = ''
        text = ''

        while not lines[line_idx].startswith(self.MK_DOCUMENT_END):
            line = lines[line_idx]
            if line.startswith('<TYPE>'):
                file_type = self._strip_markup(line)
                line_idx += 1
            elif line.startswith('<SEQUENCE>'):
                sequence = self._strip_markup(line)
                line_idx += 1
            elif line.startswith('<FILENAME>'):
                filename = self._strip_markup(line)
                line_idx += 1
            elif line.startswith('<DESCRIPTION>'):
                description = self._strip_markup(line)
                line_idx += 1
            elif line.startswith(self.MK_TEXT_BEGIN):
                text, line_idx = self.extract_document_text(lines, line_idx)
            else:
                line_idx += 1

        child_file = SECFile(filename=filename, text=text, file_type=file_type,
                               sequence=sequence, description=description)

        self.child_files.append(child_file)

        return line_idx + 1

    def _strip_markup(self, line):
        content = re.sub('<[^<]+?>', '', line)
        return content.strip()

    def extract_document_text(self, lines, line_idx):
        assert lines[line_idx].startswith(self.MK_TEXT_BEGIN)

        text = ''
        line_idx += 1
        while not lines[line_idx].startswith(self.MK_TEXT_END):
            text += lines[line_idx]
            line_idx += 1

        return text, line_idx + 1


if __name__ == '__main__':
    parser = SubmissionText('reports/Merck/0000310158/10-k/0000310158-19-000014.txt')
    parser.print_child_files()

