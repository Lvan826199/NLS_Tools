import os

#获取apk的包名
import time

class Pull_apk():

    def __init__(self,package_name):
        self.get_package_name = package_name

    def pull_select_apk(self):

        # get_package_name = "com.android.settings"
        # get_package_name = "com.android.theme.icon_pack.circular.android"
        # get_package_name = "com.google.android.networkstack.permissionconfig"

        #获取apk所在的路径
        apk_path_cmdshow = os.popen(f"adb shell pm path {self.get_package_name}").read()
        apk_path = apk_path_cmdshow.split(":")[1].strip()
        apk_name = apk_path.split("/")[-1]

        "adb pull /product/priv-app/Settings/Settings.apk  ./resources/all_apk_files"
        windows_apk_path = "./resources/all_apk_files"
        #尝试提取到windows系统，如果提取不了，则复制到设备的sdcard目录中，再提取到Windows
        try:
            msg = os.popen(f'adb pull {apk_path} {windows_apk_path} ').read()
            print("----------------")
            if "1 file pulled" in msg:
                print("apk复制成功")
            else:
                #复制到sdcard目录下
                os.system(f'adb shell cp {apk_path}  /sdcard/')
                time.sleep(3)
                os.system(f'adb pull /sdcard/{apk_name} {windows_apk_path}')
                print("else分支，apk复制成功")
        except Exception as e :
            print(e)
        return apk_name



