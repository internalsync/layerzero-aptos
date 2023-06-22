# -*- coding: utf-8 -*-
import csv
# from openpyxl import load_workbook


class FileReader:
    def __init__(self, file_name):
        self.file_name = file_name

    def load(self) -> list:
        raise NotImplemented()

    def check(self, res) -> list:
        return res


class CsvFileReader(FileReader):
    def load(self) -> list:
        return self.load_csv()

    def load_csv(self) -> list:
        res = []
        with open(self.file_name) as f:
            dialect = csv.Sniffer().sniff(f.readline(), delimiters=";,")
            f.seek(0)
            reader = csv.DictReader(f, dialect=dialect)
            for row in reader:
                res.append(row)
        return self.check(res)


# class XlsxFileReader(FileReader):
#     def load(self) -> list:
#         return self.load_xlsx()
#
#     def load_xlsx(self) -> list:
#         workbook = load_workbook(self.file_name)
#         sheet = workbook.worksheets[0]
#         columns = [cell.value for cell in sheet[1]]
#         res = []
#         for row in sheet.iter_rows(min_row=2, values_only=True):
#             res.append(dict(zip(columns, row)))
#         return self.check(res)
#
#
# class UniversalFileReader(XlsxFileReader, CsvFileReader, FileReader):
#     def load(self) -> list:
#         if self.file_name.endswith('.xlsx'):
#             return self.load_xlsx()
#         else:
#             return self.load_csv()
