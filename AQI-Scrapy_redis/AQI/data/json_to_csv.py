# coding=utf-8
import json
# Python内置的csv文件读写模块
import csv


def json_to_csv():
    # 读取json文件的对象
    json_file = open("aqi.json", "r")
    # 写入csv文件的对象
    csv_file = open("json_to_csv.csv", "w")
    # 把json文件的字符串内容转为对应的python数据类型
    item_list = json.load(json_file)
    # 创建一个csv文件写入对象，可以将数据写入到指定的csv文件中
    csv_writer = csv.writer(csv_file)
    # 表头数据部分， 一维列表
    table_title = item_list[0].keys()
    # 表数据部分，多行数据，二维列表
    data_list = [item.values() for item in item_list]

    # 写一行数据，参数是一个一维列表
    csv_writer.writerow(table_title)
    # 一次性写多行数据，参数是一个二维嵌套列表
    csv_writer.writerows(data_list)

    csv_file.close()
    json_file.close()


def read_csv():
    csv_file = open("json_to_csv.csv", "r")
    csv_reader = csv.reader(csv_file)
    # 迭代读取每一行
    for line in csv_reader:
        print(line)
    csv_file.close()

if __name__ == '__main__':
    json_to_csv()



