import time

import xlrd
import xlwt

from utils.logger import log
from common.dir_config import LOGDIR


class DiffExcelFile():
    def __init__(self, wb_name="Excel_Workbook.xlsx", sheet_name="Sheet1"):
        self.workbook = xlwt.Workbook()
        self.wb_name = wb_name
        self.sheet_name = sheet_name
        self.worksheet = self.workbook.add_sheet(self.sheet_name)

    def write_excel(self, row, col, content, style='pattern: pattern solid, fore_colour yellow; font: bold on'):
        style = xlwt.easyxf(style)
        self.worksheet.write(row, col, label=content, style=style)
        self.save_excel()

    def save_excel(self):
        self.workbook.save(self.wb_name)


def write_file(filename, content):
    if not isinstance(content, str):
        content = str(content)

    with open(filename, 'a', encoding='utf-8') as file:
        time_now = time.strftime("%Y-%m-%d", time.localtime())
        file.write(time_now + ':Измененные интерфейсы и параметры ==>' + content + '\n')


def read_excel(file_path, sheet_name="Sheet1"):
    datas = []
    xlsx_file = {}
    wb = xlrd.open_workbook(file_path)
    sheet_name_list = wb.sheet_names()

    if sheet_name in sheet_name_list:
        sheet_name = wb.sheet_by_name(sheet_name)
        for rows in range(0, sheet_name.nrows):
            orign_list = sheet_name.row_values(rows)
            xlsx_file[rows] = orign_list
    else:
        log.info("{}Имя дочерней таблицы не существует в файле {}！".format(sheet_name, file_path))

    for row in range(1, len(xlsx_file)):
        data = dict(zip(xlsx_file[0], xlsx_file[row]))
        datas.append(data)

    return datas


def diff_excel(src_file, des_file, check="caseid,url,params"):
    fail = 0
    res1 = read_excel(src_file)
    res2 = read_excel(des_file)

    lis1 = check.split(",")
    index = lis1[0]
    check1 = lis1[1]
    check2 = lis1[2]

    data = []
    for i in range(len(res2)):
        data.append([res2[i][check1], res2[i][check2]])

    datas = []
    for r1 in range(len(res1)):
        case = [res1[r1][check1], res1[r1][check2]]
        if case not in data:
            log.info("New / changed data：{}".format(case))
            fail += 1
            case_id = str(res1[r1][index])
            content = "".join([case_id, str(case)])
            datas.append(content)
            write_file(LOGDIR + "diff_data.log", content)

    for i in range(len(datas)):
        DiffExcelFile.write_excel(i + 1, 0, datas[i])
