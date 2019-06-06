# -*—coding:utf8-*-
import requests
from bs4 import BeautifulSoup
import xlwt
import xlrd
import os
import time
from xlutils.copy import copy

# 1.获取网页信息，以文本形式返回网页内容


def getHTMLText(url):
    try:
        r = requests.get(url)
        r.raise_for_status()
        r.encoding = r.apparent_encoding
        return r.text
    except Exception as err:
        print(err)

# 2.解析页面，以列表形式返回手机号结果信息['手机号码段','卡号归属地','卡 类 型','区 号','邮 编']


def parsePhoneData(html):
    soup = BeautifulSoup(html, "html.parser")
    table = soup.find('table', attrs={'style': 'border-collapse: collapse'})
    phoneInfoList = []
# 用于存放电话信息
    for td in table.find_all('td', attrs={'class': 'tdc2'}):
        rst = td.getText()\
            .replace('\xa0', '&&')\
            .replace(' 测吉凶(新)', '')\
            .replace(' 更详细的..', '')
        if '移动' in rst:
            rst = '中国移动'
        elif '联通' in rst:
            rst = '中国联通'
        elif '电信' in rst:
            rst = '中国电信'
        phoneInfoList.append(rst)
    print(phoneInfoList)
    return phoneInfoList

# 3.将查询的信息写入Excel文件，如果Excel存在，则追加数据


def saveDataToExcel(datalist, path):
    if os.path.exists(path):
        xlsrd = xlrd.open_workbook(path, formatting_info=True)
        sheet1 = xlsrd.sheet_by_index(0)
        n = sheet1.nrows
        newWK = copy(xlsrd)
        newsheet = newWK.get_sheet(0)
        for i in range(0, 5):
            data = datalist[i]
            newsheet.write(n, i, data)
            newWK.save(path)
    else:
        # 标题栏背景色
        styleBlueBkg = xlwt.easyxf(
            'pattern: pattern solid, fore_colour pale_blue; font: bold on;')  # 80% like
        # 创建一个工作簿
        book = xlwt.Workbook(encoding='utf-8', style_compression=0)
        # 创建一张表
        sheet = book.add_sheet('手机归属地查询', cell_overwrite_ok=True)
        # 标题栏
        titleList = ('手机号码段', '卡号归属地', '卡 类 型', '区 号', '邮 编')
        # 设置第一列尺寸
        first_col = sheet.col(0)
        first_col.width = 256 * 30
        # 写入标题栏
        for i in range(0, 5):
            sheet.write(0, i, titleList[i], styleBlueBkg)
        # 写入Chat信息
        for i in range(0, 5):
            data = datalist[i]
            sheet.write(1, i, data)
        # 保存文件到指定路径
        book.save(path)

# 读取一批电话号码，存到列表中


def nums(phonenumPath, offsett):
    f = open(phonenumPath)
    phoneNums = []
    f.seek(offsett, 0)
    while True:
        phoneNum = f.readline().strip('\n')
        if phoneNum == "" or len(phoneNums) == 400:
            print(f.tell())
            f.close()
            break
        phoneNums.append(phoneNum)
    f.close()
    return phoneNums


if __name__ == '__main__':
    path = "D:/CrackPasswd/phone_section_result.xls"
    phonenumPath = "D:/CrackPasswd/phonenum.txt"
    phoneNums = []
    phoneNums = nums(phonenumPath, offsett=62690)
    for phoneNum in phoneNums:
        url = "http://www.ip138.com:8080/search.asp?mobile=" + phoneNum + "&action=mobile"
        html = getHTMLText(url)
        result = parsePhoneData(html)
        if "验证手机号有误" not in result:
            saveDataToExcel(result, path)
        time.sleep(1)
