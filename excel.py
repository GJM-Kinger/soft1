# @将数据列表写到excel中
# @Author: gou
# @Time: 2020/10/14 15:28
# @version: 1.0
# !/usr/bin/env python
# coding=utf-8

import xlwt


# 将数据写入新文件
def data_write(datas):
    f = xlwt.Workbook()
    sheet1 = f.add_sheet(u'sheet1', cell_overwrite_ok=True)  # 创建sheet

    # 将数据写入第 i 行，第 j 列
    i = 0
    for data in datas:
        for j in range(len(data)):
            sheet1.write(i, j, data[j])
        i = i + 1
    f.save("E:\testFile\name.xlsx")  # 保存文件


if __name__ == '__main__':
    data_write(['10', '20'])
