#coding=utf-8

import os
#1.提取设备中的framework-res.apk进行反编译
#adb pull /system/framework/framework-res.apk
import time
class Decompilation():

    def __init__(self,apk_name):
        self.apk_name = apk_name
        print("framework-res提取")

    def get_values(self):
        # framework_showpath = os.popen("cd .. && cd resources && cd framework-res && chdir").read()
        framework_showpath = os.popen("cd resources && cd framework-res && chdir").read()
        framework_path = framework_showpath.strip()
        print(framework_path)
        apktool_file = os.listdir("./apktool")
        print("apktool_file",apktool_file)
        # framework_res = os.listdir("../resources/framework-res")
        framework_res = os.listdir("./resources/framework-res")

        if ("framework-res.apk" in apktool_file) and ("1.apk" in framework_res):
            print("已存在")
        else:
            try:
                # os.popen("adb pull /system/framework/framework-res.apk .")
                os.popen("cd apktool && adb pull /system/framework/framework-res.apk .")
                time.sleep(5)
            except Exception as e:
                print(f'{e},提取设备framework-res失败，请联系开发人员！')

            #2.把framework-res.apk解析到对应文件夹
            # os.popen('apktool_2.5.0 if -p D:\Y_Script\\rubbish_draft\\all_app_charater\\NLS_Tools\\resources\\framework-res  framework-res.apk')
            # os.system(f'apktool_2.5.0 if -p {framework_path}  framework-res.apk')
            os.system(f'cd apktool && apktool_2.5.0 if -p {framework_path}  framework-res.apk')


        #3.反编译apk
        #把对应文件夹下面的apk反编译到主目录下的temp文件夹里面
        #每次编译都会覆盖掉temp下面的所有内容
        # window_apk_path = '../resources/all_apk_files/IconPackCircularAndroidOverlay.apk'
        apk_name = self.apk_name
        # window_apk_path = '../resources/all_apk_files/Settings.apk'
        window_apk_path = f'../resources/all_apk_files/{apk_name}'
        # save_path = '../temp/'
        save_path = '../temp/'
        time.sleep(3)
        # os.popen(f'apktool_2.5.0.bat d -p {framework_path} -f {window_apk_path} -o {save_path}')
        msg = os.system(f'cd ./apktool && apktool_2.5.0.bat d -p {framework_path} -f {window_apk_path} -o {save_path}')
        #如果执行成功，输出为0，否则执行失败
        if msg == 0:
            print("当前apk反编译完成，开始进行xml遍历提取")

        else:
            print(f'当前apk反编译失败,{apk_name},请联系开发人员！')








