# -*- coding: UTF-8 -*-
import datetime
import os
import re
import shutil
import time

import langid
import xlrd
import xlwt
from xlutils.copy import copy
from apktool.decompilation import Decompilation
from pull_apk_into_windows import Pull_apk


class CompareAllCharts():

    def __init__(self):
        # 转换为langid可识别的国家代码
        self.lang = {'ar': 'ar', 'bg': 'bg', 'cs': 'cs', 'da': 'da', 'de': 'de', 'el': 'el', 'en': 'en', 'es-rUS': 'es',
                     'et': 'et', 'fi': 'fi', 'fr': 'fr', 'hi': 'hi', 'hr': 'hr', 'hu': 'hu', 'in': 'id', 'it': 'it',
                     'iw': 'he',
                     'ja': 'ja', 'ko': 'ko', 'lt': 'lt', 'lv': 'lv', 'ms': 'ms', 'nb': 'nb', 'nl': 'nl', 'pl': 'pl',
                     'pt-rBR': 'pt', 'pt-rPT': 'pt', 'pt': 'pt','ro': 'ro', 'ru': 'ru', 'sk': 'sk', 'sl': 'sl', 'sr': 'sr',
                     'sv': 'sv',
                     'th': 'th', 'tl': 'tl', 'tr': 'tr', 'uk': 'uk', 'ur': 'ur', 'vi': 'vi', 'zh-rCN': 'zh',
                     'zh-rTW': 'zh',
                     'zh-rHK': 'zh'}
        #创建当前轮次的文件夹，以当前时间命名，一轮一个文件夹
        now_time = datetime.datetime.now().strftime('%Y-%m-%d-%H-%M-%S')
        make_result_dir = os.popen(f'cd result && mkdir {now_time} && cd {now_time} && chdir').read()
        self.result_folder = make_result_dir.strip()



    # 读取xml文件中<string></string>中间部分的内容，并存储在一个列表中
    def xml_re_string(self, filepath):
        '''
        return : 返回xml中所有string的列表
        '''
        # re_string = re.compile(r'>.*?<')
        # re_string= re.compile(r'(?<=>).*?(?=<)')
        re_string = re.compile(r'(?<=">).*?(?=</string)')

        string_final = []
        with open(filepath, 'r', encoding='utf-8') as xmlfile:
            string_list = re_string.findall(xmlfile.read())

        for i in string_list:
            if i != '':
                string_final.append(i)
        return string_final

    # 将excel列内容储存为list
    def exceltolist(self, excelpath, colx):
        data = xlrd.open_workbook(excelpath)
        table1 = data.sheets()[0]
        return table1.col_values(colx, start_rowx=0, end_rowx=None)

    # 设置excel字体style
    def setStyle(self, height, color, name='Arial'):
        style = xlwt.XFStyle()  # 初始化样式
        font = xlwt.Font()  # 为样式创建字体
        # 字体类型：比如宋体、仿宋也可以是汉仪瘦金书繁
        font.name = name
        # 设置字体颜色
        font.colour_index = color
        # 字体大小
        font.height = height
        # 定义格式
        style.font = font
        return style

    # 创建文件夹
    def do_mkdir(self, path):
        # 判断路径是否存在
        # 存在     True
        # 不存在   False
        isExists = os.path.exists(path)
        # 判断结果
        if not isExists:
            # 如果不存在则创建目录
            # 创建目录操作函数
            os.makedirs(path)
            print(path + ' 创建成功')
            return True
        else:
            # 如果目录存在则不创建，并提示目录已存在
            print(path + ' 目录已存在')
            return False

    # xls追加写入内容
    def write_excel_xls_append(self, path,style = False,height=200,color=0,value=None):
        if style == False:
            style = self.setStyle(200,0)
        else:
            style = self.setStyle(height,color)
        # 判断文件是否存在
        if not os.path.exists(path):
            # 创建一个workbook 设置编码
            workbook = xlwt.Workbook(encoding='utf-8')
            # 创建一个worksheet
            worksheet = workbook.add_sheet('result')
            worksheet.col(0).width = 100 * 100  # Set the column width
            worksheet.col(1).width = 100 * 50
            worksheet.col(2).width = 100 * 50
            worksheet.col(3).width = 120 * 100
            # 写入excel
            # 参数对应 行, 列, 值
            worksheet.write(0, 0, 'xml抓取字符', self.setStyle(200, 2))
            worksheet.write(0, 1, '判断语言', self.setStyle(200, 2))
            worksheet.write(0, 2, '语言相似度', self.setStyle(200, 2))
            worksheet.write(0, 3, '所属包名', self.setStyle(200, 2))
            workbook.save(path)
        if value != None:
            index = len(value)  # 获取需要写入数据的行数
            workbook = xlrd.open_workbook(path, formatting_info=True)  # 打开工作簿
            sheets = workbook.sheet_names()  # 获取工作簿中的所有表格
            worksheet = workbook.sheet_by_name(sheets[0])  # 获取工作簿中所有表格中的的第一个表格
            rows_old = worksheet.nrows  # 获取表格中已存在的数据的行数
            new_workbook = copy(workbook)  # 将xlrd对象拷贝转化为xlwt对象
            new_worksheet = new_workbook.get_sheet(0)  # 获取转化后工作簿中的第一个表格
            for i in range(0, index):
                for j in range(0, len(value[i])):
                    new_worksheet.write(i + rows_old, j, value[i][j], style)  # 追加写入数据，注意是从i+rows_old行开始写入
            new_workbook.save(path)  # 保存工作簿
            print("xls格式表格【追加】写入数据成功！")


    # 不需要把研发的字符写进去表格，因为没法进行一个个对比，也没必要写
    # 字符就单独保存在一个列表里面，取出xml文件中的字符，然后循环对比
    def get_standard_excel_msg(self, standard_scale_excel):
        '''
        return : 返回不带引号的列表字符(后期需要更改为字典，提高查找效率)
        '''
        self.xl = xlrd.open_workbook('{}'.format(standard_scale_excel))
        self.table = self.xl.sheet_by_index(0)
        # 读取表格第一列除去第一行的值
        self.fristcol = self.table.col_values(0)
        fristcol_list = []

        for i in range(0, len(self.fristcol)):
            # 把字符两头的引号去掉
            if self.fristcol[i].startswith('"') and self.fristcol[i].endswith('"'):
                str1 = self.fristcol[i].strip('"')
                fristcol_list.append(str1)
            else:
                fristcol_list.append(self.fristcol[i])
        # print("当前表第一列的值为:{}".format(fristcol_list))
        return fristcol_list

    #获取哪些勾选了需要提取的apk名字
    def get_select_apk(self):
        xl = xlrd.open_workbook("./setting/select_apk_package.xlsx")
        table = xl.sheet_by_index(0)
        # 读取表格第一列除去第一行的值
        fristcol = table.col_values(0)
        fristcol_list = []
        fristcol_list.append(table.cell(1, 0).value)  # 把第二行第一列的值加进去

        for i in range(2, len(fristcol)):
            # 把除去第一行的第一列的0和1强转为int类型的数值，并且加入到列表里面
            fristcol_list.append(int(fristcol[i]))
        # print("当前表第一列的值为:{}".format(fristcol_list))
        # 获取fristcol_list中为1的下标,同时用一个列表存储这些下标
        indexlist = []

        for i in range(len(fristcol_list)):
            if fristcol_list[i] == 1:  # 如果为1，那就是需要运行这一行的代码，此时获取下标，就相当于是获取第几行
                indexlist.append(i+1)  # i就是下标
        # print("当前表中select是1的行数为：{}".format(indexlist))
        packagelist = []
        for i in indexlist:
            # 获取对应select为1的package（第3列）
            package_name = table.cell(i, 2).value
            packagelist.append(package_name)  # 获取select为1的package
        print("当前表中select为1对应的包名为：{}".format(packagelist))

        return packagelist






    # 返回目标文件夹中所有的子文件夹
    def get_xmldirs(self):
        # path = os.path.join(os.getcwd(),"temp")
        path = "temp"
        dirpaths = []
        for root, dirs, files in os.walk(path):
            # root 表示当前正在访问的文件夹路径
            # dirs 表示该文件夹下的子目录名list
            # files 表示该文件夹下的文件list
            for dir in dirs:
                if "values" in str(dir):
                    path = os.path.join(root, dir,"strings.xml")
                    dirpaths.append(path)
                    # print(path)
        return dirpaths

    # 获取研发的所有表格以及名字，返回一个列表
    def get_RD_excel(self):
        path = "./resources/RD_excel"
        for root, dirs, files in os.walk(path):
            # root 表示当前正在访问的文件夹路径
            # dirs 表示该文件夹下的子目录名list
            # files 表示该文件夹下的文件list
            return files


    #获取所有的excel的language_id，返回一个列表
    def get_all_language_id(self):
        all_language_id_list = []
        RD_excel_list = self.get_RD_excel()
        for RD_excel_name in RD_excel_list:
            language_id = RD_excel_name.split("_")[0]
            all_language_id_list.append(language_id)
        return all_language_id_list

    #把excel的名字和excel的language_id组合成一个字典，language_id为键，excel_name为值
    def excel_id(self):
        files = self.get_RD_excel()
        all_language_id_list = self.get_all_language_id()
        excel_id = dict(zip( all_language_id_list,files))
        return excel_id

    # 删除目录下文件以及文件夹
    def del_files(self,path):

        filelist = os.listdir(path)  # 列出该目录下的所有文件名
        for f in filelist:
            filepath =  os.path.join(path, f)  # 将文件名映射成绝对路径
            if os.path.isfile(filepath):  # 判断该文件是否为文件或者文件夹
                os.remove(filepath)  # 若为文件，则直接删除os.path.isdir(filepath)
                print(str(filepath) + " removed!")
            elif os.path.isdir(filepath):
                shutil.rmtree(filepath, True)  # 若为文件夹，则删除该文件夹及文件夹内所有文件
                print("dir " + str(filepath) + " removed!")
                # shutil.rmtree(path, True)  # 最后删除img总文件夹


    # string对比以及结果写入excel
    def classify(self):
        '''
             xml_path : 平板中xml文件的路径
             standard_scale_excel_path：研发给的表格的路径
             resultexcel_name：表格结果的名字
             language_id：本来的语言
             '''

        #获取所有选择的apk的package
        packagelist = self.get_select_apk()
        for package_name in packagelist:

            #进行提取apk
            apk_name = Pull_apk(package_name).pull_select_apk()

            #提取完apk,把temp里面的内容清掉，加快反编译
            self.del_files("./temp")

            #进行反编译apk
            Decompilation(apk_name).get_values()

            print('*************************************************************')
            excel_id_dict = self.excel_id()
            for language_id,excel_file in excel_id_dict.items():

                excel_file_path = "./resources/RD_excel/" + excel_file

            # 判断目标结果excel文件是否存在，若无创建新文件
                result_path = os.path.join(os.getcwd(), f'{self.result_folder}\\{language_id}.xls')


                print("结果保存路径：{}".format(result_path))

                self.write_excel_xls_append(path=result_path)

                fail_list = []
                pass_sum = 0
                fail_sum = 0
                not_exist = 0
                # 我这里需要写一个方法
                # 把文件夹中所有的文件名加进去一个列表里面，再从列表里面取出以values开头的文件夹名字
                # 最后要从values-（语言）取出里面的string.xml
                # (语言需要有一个列表)
                # re_name = re.compile(r'.*\\{1,2}(\(\d+\) .*?).xml')
                strings_path_list = self.get_xmldirs()
                xml_folder_name = str("values-" + language_id)
                print(xml_folder_name)
                xml_path = None
                for i in strings_path_list:
                    folder_name = i.split('\\')[2]
                    if xml_folder_name == folder_name:
                        print("目录为：",i)
                        xml_path =i


                if xml_path != None:
                    # 取得xml文件中文字的列表
                    xml_list = self.xml_re_string(xml_path)
                    print("xml_string的长度：",len(xml_list))
                    # 取得标准表格中的字符
                    standard_list = self.get_standard_excel_msg(excel_file_path)
                    print("标准表格的行数：",len(standard_list))

                    content = []

                    # 这里只写一个只对比一次的xml，暂时不写所有文件夹下的xml
                    for xml_string in xml_list:
                        if xml_string in standard_list:
                            pass_sum += 1
                        else:
                            not_exist += 1
                            # 需要判断当前的语言是啥，自己后期写入
                            language_read = langid.classify(xml_string)[0]
                            # print("language_read",language_read)
                            # print("language_id",language_id)

                            if language_read == self.lang[language_id]:
                                match_rate = str('%.2f' % (float(langid.classify(xml_string)[1]) * 100)) + '%'
                                # print("-----------------------")
                                # content.append([xml_string, language_read, match_rate])
                                # print("列表：",content)
                            else:
                                pass
                                match_rate = 'FAIL'
                                # fail_list.append(xml_string)
                                fail_sum += 1
                            # 把不存在标准表格中的写入到表格中
                            content.append([xml_string, language_read, match_rate,package_name])

                    self.write_excel_xls_append(path=result_path, value=content)
                    summary = time.strftime("%Y-%m-%d %H:%M:%S", time.localtime()) + '    ' + 'pass:' + str(
                        pass_sum) + '    ' + 'not_exist:'  + str(not_exist) + '   '+'其中fail:' + str(fail_sum)

                    self.write_excel_xls_append(path=result_path,value=[[summary]],style=True,height=300,color=2)
                    print(summary)
                    print('result file save in ' + result_path)

                else:
                    print("xml_path出问题了")


if __name__ == '__main__':
    run = CompareAllCharts()
    run.classify()
