"""
@Date:2021.3.18
@Author:Xiaoke Quan
@Company:Tenable
@Mail:xquan@tenable.com
@Version 1.0-GA
安装以下附加模块
pyTenable
xlrd
time
shutil
os
xlwt
argparse
dnspython
requests


替换主程序（ main（））第3行的X-apikey
用户template需要手动登陆页面创建
"""

import xlrd
import xlwt
import time
import requests
import sublist3r
import shutil
import os
import json


def menu():
    try:
        print('欢迎使用T.IO-WAS V2 自动化脚本')
        print('输入编号选择相应功能')
        print('1. 创建扫描目录   2. 检查扫描策略   3. 选择扫描器/扫描策略，批量上传扫描目标，建立扫描任务  4. 批量开始扫描任务  ')
        print('5. 查看扫描任务和结果  6.FQDN枚举并保存列表  7.按目录自动批量生成扫描报告  8.按目录自动批量下载扫描报告  ')
        task_root = int(input('请输入您要使用的功能编号： '))
        return task_root
    except ValueError:
        main()

def file_name_get(file_dir):
    i=0
    for root, dirs, files in os.walk(file_dir):
        file_name = files
        break
    return file_name

def creat_report_pdf(report_id):
    url = "https://cloud.tenable.com/was/v2/scans/" + report_id + "/report"
    headers = {
        "Accept": "application/json",
        "Content-Type": "application/pdf",
        "X-ApiKeys": X_Apikeys
    }
    response = requests.request("PUT", url, headers=headers)
    print(response.text)

def creat_report_csv(report_id):
    url = "https://cloud.tenable.com/was/v2/scans/" + report_id + "/report"
    headers = {
        "Accept": "application/json",
        "Content-Type": "text/csv",
        "X-ApiKeys": X_Apikeys
    }
    response = requests.request("PUT", url, headers=headers)
    print(response.text)

def get_report_pdf(report_id, report_name):
    url = "https://cloud.tenable.com/was/v2/scans/" + report_id +"/report"
    headers = {
        "Accept": "application/json",
        "Content-Type": "application/pdf",
        "X-ApiKeys": X_Apikeys
    }
    name = report_name
    name1 = name.split (sep='//')
    name2 = name1[1]
    report_real_name = name2 + ".pdf"
    response = requests.request("GET", url, headers=headers)
    with open(report_real_name, 'wb') as f:
        f.write(response.content)

def get_report_csv(report_id, report_name):
    url = "https://cloud.tenable.com/was/v2/scans/" + report_id +"/report"
    headers = {
        "Accept": "application/json",
        "Content-Type": "text/csv",
        "X-ApiKeys": X_Apikeys
    }
    name = report_name
    name1 = name.split (sep='//')
    name2 = name1[1]
    report_real_name = name2 + ".csv"
    response = requests.request("GET", url, headers=headers)
    with open(report_real_name, 'wb') as f:
        f.write(response.content)


def list_owner():
    url = "https://cloud.tenable.com/users"
    headers = {"Accept": "application/json", 'X-APIKeys': X_Apikeys}
    response = requests.request("GET", url, headers=headers)
    response.data = json.loads(response.text)
    for i in response.data['users']:
        print ('userID： ', i['uuid'],'   username： ',i['user_name'])


def list_scanner():
    url = "https://cloud.tenable.com/scanners"
    headers = {"Accept": "application/json", 'X-APIKeys': X_Apikeys}
    response = requests.request("GET", url, headers=headers)
    response.data = json.loads(response.text)
    # print(response.data['scanners'])
    for i in response.data['scanners']:
        print ('扫描器ID： ', i['id'],'   扫描器名称： ',i['name'], '   是否支持WebApp扫描： ',i['supports_webapp'])

def list_folder():
    url = "https://cloud.tenable.com/was/v2/folders"
    headers = {"Accept": "application/json", 'X-APIKeys': X_Apikeys}
    response = requests.request("GET", url, headers=headers)
    response.data = json.loads(response.text)
    for i in response.data:
        print ('目录ID： ', i['folder_id'],'   目录名称： ',i['name'])

def create_folder(x):
    url = "https://cloud.tenable.com/was/v2/folders"
    headers = {"Accept": "application/json", "Content-Type": "application/json", 'X-APIKeys': X_Apikeys}
    body = {'name':x}
    response = requests.request("POST", url, headers=headers,json=body)
    response.data = json.loads(response.text)
    print(response.data)

def list_template():
    url = "https://cloud.tenable.com/was/v2/user-templates"
    headers = {"Accept": "application/json", 'X-APIKeys': X_Apikeys}
    response = requests.request("GET", url, headers=headers)
    response.data = json.loads(response.text)
    # print(response.data['data'])
    for i in response.data['data']:
        print('Tenable策略ID:  ',i['template_id'], '用户策略ID： ', i['user_template_id'], '  使用者ID:  ', i['owner_id'],'  策略名称： ', i['name'])

def list_tenable_template():
    url = "https://cloud.tenable.com/was/v2/templates"
    headers = {"Accept": "application/json", 'X-APIKeys': X_Apikeys}
    response = requests.request("GET", url, headers=headers)
    response.data = json.loads(response.text)
    tenable_template_id = 0
    for i in response.data['data']:
        # print ('名称',i['name'], '    描述：',i['description'], '  ID:',i['template_id'])
        if i['name'] == 'scan':
            tenable_template_id = i['template_id']

    print ('您的Tenable Web扫描模版ID是：', tenable_template_id)
    return (tenable_template_id)


def list_scans(x):
    url = "https://cloud.tenable.com/was/v2/configs/search"
    querystring = {"limit": "10000"}
    payload = {"value": x,
            "field": "folder_name",
            "operator": "match"}
    headers = {"Accept": "application/json", 'X-APIKeys': X_Apikeys}
    response = requests.request("POST", url, headers=headers, json=payload, params=querystring)
    response.data = json.loads(response.text)
    print(response.data)
    for i in response.data['data']:
        print(i)
        print('名称： ', i['name'],'   id： ', i['config_id'])

def create_scans(scan_target_name, io_folder_id, io_owner_id, io_tenable_template_id, io_template_id, io_scanner_id):
    url = "https://cloud.tenable.com/was/v2/configs"
    payload = {
        "schedule": {
            "timezone": "Asia/Shanghai",
            "starttime": "20210316T110000",
            "rrule": "FREQ=YEARLY",
            "enabled": False
            },
        "name": scan_target_name,
        "target": scan_target_name,
        "folder_id": io_folder_id,
        "owner_id": io_owner_id,
        "template_id": io_tenable_template_id,
        "user_template_id": io_template_id,
        "scanner_id": io_scanner_id
    }
    headers = {
        "Accept": "application/json",
        "Content-Type": "application/json",
        "X-ApiKeys": X_Apikeys
    }

    response = requests.request("POST", url, json=payload, headers=headers)
    response.data = json.loads(response.text)
    # print(response.data)
    print (response.data['settings']['target'], '  创建成功')

def scan_count(id):
    scan_count = 0

    url = "https://cloud.tenable.com/was/v2/configs/search"
    querystring = {"limit": "10000"}
    payload = {"value": id,
            "field": "folder_name",
            "operator": "match"}
    headers = {"Accept": "application/json", 'X-APIKeys': X_Apikeys}
    response = requests.request("POST", url, headers=headers, json=payload, params=querystring)
    response.data = json.loads(response.text)
    for i in response.data['data']:
        try:
            scan_status_list = i['last_scan']['status']
            if scan_status_list == 'running' or scan_status_list == 'pending':
                scan_count += 1
        except:
            pass

    print('正在扫描的任务数：',scan_count)
    return scan_count

def was_launch_scan_folder(folder_name):
        url = "https://cloud.tenable.com/was/v2/configs/search"
        querystring = {"limit": "10000"}
        payload = {"value": folder_name,
                "field": 'folder_name',
                "operator": "match"}
        headers = {"Accept": "application/json", 'X-APIKeys': X_Apikeys}
        response = requests.request("POST", url, headers=headers, json=payload, params=querystring)
        response.data = json.loads(response.text)
        # print('进入启动函数')
        # print(response.data)
        for (i) in response.data['data']:
            # print('名称： ', i['name'],'   id： ', i['config_id'])
            # print('进入id循环')
            try:

                if i['last_scan']['status'] == 'running':
                    print('扫描任务：',i['name'],' 扫描状态: ',i['last_scan']['status'])
                    # print('id1',i['config_id'])
                elif i['last_scan']['status'] == 'pending':
                    print('扫描任务：',i['name'],'  扫描状态：',i['last_scan']['status'])
                    # print('id2', i['config_id'])
                elif i['last_scan']['status'] is None:
                    print('扫描任务：',i['name'],'  扫描状态：','无')
                    # print('id3',i['config_id'])
                    url = "https://cloud.tenable.com/was/v2/configs/" + i['config_id'] + "/scans"
                    headers = {"Accept": "application/json", 'X-APIKeys': X_Apikeys}
                    response = requests.request("POST", url, headers=headers)
                    # print('id4',i['config_id'])
                    print(response.text)
                    break
                else:
                    url = "https://cloud.tenable.com/was/v2/configs/" + i['config_id'] + "/scans"
                    headers = {"Accept": "application/json", 'X-APIKeys': X_Apikeys}
                    response = requests.request("POST", url, headers=headers)
                    # print('id4',i['config_id'])
                    print(response.text)
                    break
            except TypeError:
                url = "https://cloud.tenable.com/was/v2/configs/" + i['config_id'] + "/scans"
                headers = {"Accept": "application/json", 'X-APIKeys': X_Apikeys}
                response = requests.request("POST", url, headers=headers)
                # print('id4',i['config_id'])
                print(response.text)
                break


def main():
    global X_Apikeys
    X_Apikeys = "accessKey=4a16f1a1d313bc62b82d9731ad891ffde24014a8e80f087199e5dc0f4cc84e22;secretKey=cf9c644d227c60acbf1da3ad032cbee9f0f03c29278438ee8568092d3c145322"
    task_root = menu()
    print(task_root)

    if task_root == 9:
        creat_report()
        get_report()
        main()
    if task_root == 1:
        task_folder_1=1
        try:
            while task_folder_1 != 0:
                print('这是您当前所有的扫描目录')
                list_folder()
                task_folder_1 = input('请输入您要创建的目录名称：(不要和现有目录重名,输入exit退出） ')
                if task_folder_1 == 'exit':
                    main()

                else:
                    create_folder(task_folder_1)
                    print('目录{}创建成功！'.format(task_folder_1))
                    main()
        except:
            print('名称输入错误！请不要输入相同的目录名！')
            main()


    if task_root == 2:
        print('这是您当前所有的用户扫描策略')
        list_template()
        main()

    if task_root == 3:
        print('您的扫描工作目录如下： ')
        list_folder()
        try:
            io_folder_id = input('请选择您的扫描目录，输入目录ID： ')
        except ValueError:
            main()
        print('您选择的目录是 ',io_folder_id)

        print('您现有的IO扫描器列表如下： （off代表不可用，managed代表只能用于主机扫描，managed_webapp代表只能用于web扫描)')
        list_scanner()
        try:
            io_scanner_id = input('请输入您要使用的扫描器ID： ')
        except ValueError:
            main()
        print('您选择的扫描器ID是：',io_scanner_id)

        print('您的用户扫描策略如下： ')
        list_tenable_template()
        list_template()
        try:
            io_policy_id = input('请选择您的用户扫描策略，输入策略ID： ')
        except ValueError:
            main()
        print('您选择的扫描策略是：', io_policy_id)

        list_owner()
        try:
            io_owner_id = input('请选择您的扫描Owner，输入策OwnerID： ')
        except ValueError:
            main()
        io_tenable_template_id = list_tenable_template()
        print('您选择的扫描Owner是：', io_owner_id)
        print('在批量倒入之前，请复查您选择的环境及扫描参数：  ')
        print('扫描目录ID：', io_folder_id)
        print('扫描引擎ID：', io_scanner_id)
        print('用户扫描策略ID：', io_policy_id)
        print('扫描OwnerID：', io_owner_id)
        print('Tenable扫描策略ID：', io_tenable_template_id)

        print('您当前目录中的域名表格文件如下：')
        file_name_output = file_name_get(os.getcwd())
        for i in file_name_output:
            file_ext = i[-4:]
            # print(i)
            if file_ext == '.xls':
                print(i)

        try:
            io_job_import = input('输入域名表格文件(.xlsx)的完整路径(例如"/path/file.xls"，如果在当前目录中，可以直接输入文件名)并回车开始导入。（输入0或直接回车返回主菜单）  ')
        except ValueError:
            main()
        if io_job_import != 0:
            file_name=io_job_import
            print('您选择导入的文件是： ',file_name)
            print('请耐心等待扫描任务导入')
            try:
                target_wookbook = xlrd.open_workbook(file_name)
            except FileNotFoundError:
                print('找不到您的域名表格文件！')
                print()
                main()
            target_table = target_wookbook.sheet_by_index(0)
            task_ids = set()
            for i in range(0, target_table.nrows):
                target = target_table.cell(i, 0).value
                print(target)
                scan_target_name = target
                print('导入任务： ', '名称： ', scan_target_name, '扫描目标：', scan_target_name, )
                create_scans(scan_target_name,io_folder_id,io_owner_id,io_tenable_template_id,io_policy_id,io_scanner_id)
            print('成功导入所有网址，扫描任务如下： ')
            # for scan in tio.scans.list(io_folder_id):
            #     scan_id = scan['id']
            #     scan_name = scan['name']
            #     scan_status = scan['status']
            #     print(scan_name,scan_status)

        if io_job_import == 0:
            print('退出菜单')
        main()
    if task_root == 4:
        print('这是您的扫描目录ID')
        list_folder()
        try:
            io_folder_id_l = input('请输入您要扫描的目录名称： ')
        except ValueError:
            main()
        was_launch_scan_folder(io_folder_id_l)
        count = scan_count(io_folder_id_l)
        # print('计数器',count)
        while count:
            if count == 0:
                break
            elif count > 0 and count < 4:
                was_launch_scan_folder(io_folder_id_l)
                count = scan_count(io_folder_id_l)
            elif count >= 4:
                print('并发扫描已经达到4个，请等待！')
                time.sleep(60)
                count = scan_count(io_folder_id_l)
        print('任务完成，感谢使用!')
        menu()

    if task_root == 5:
        print('您的扫描目录如下： ')
        list_folder()
        try:
            check_folder_id = input('请选择您的扫描目录，输入目录名称： ')
        except ValueError:
            main()
        print('您选择的目录ID是 ',check_folder_id)

        print('扫描任务列表如下：')
        list_scans(check_folder_id)


    if task_root == 6:
        #print('您的扫描工作目录如下： ')
        worm_url_input = input('请输入您要爬的域名： ')
        worm_url_file_name = input('请输入您要存储的表格文件名： ')
        print('域名爬虫正在工作中，请等待...')
        worm_url_details = sublist3r.main(worm_url_input, 40, 'fqdn.txt', ports='80,443', silent=True, verbose=True,
                                    enable_bruteforce=False, engines='passivedns,ssl,virustotal,netcraft,ask,baidu,bing')
        # print(worm_url_details)
        xlsx_name = worm_url_file_name + '.xlsx'
        # workbook = xlwt.Workbook(encoding='utf-8')
        # row1 = 0
        # print('正在生成表格，请稍等！')
        # worksheet = workbook.add_sheet('fqdn')
        # for fqdn in worm_url_details:
        #     url_details = 'https://'+fqdn
        #     worksheet.write(row1,0,url_details)
        #     row1 += 1
        # workbook.save(xlsx_name)
        source = 'fqdn.xlsx'
        target = xlsx_name
        try:
            shutil.copy(source, target)
            print('表格成功生成！文件名为： ', xlsx_name)
        except IOError as e:
            print("找不到文件. %s" % e)
        except:
            print("错误返回", sys.exc_info())

    if task_root == 7:
        list_folder()
        try:
            check_folder_id = input('请选择您要生成报告的目录，输入目录名称： ')
            check_file_type = input('请选择您要生成报告的类型 （csv/pdf）： ')
        except ValueError:
            main()

        url = "https://cloud.tenable.com/was/v2/configs/search"
        querystring = {"limit": "10000"}
        payload = {"value": check_folder_id,
                   "field": "folder_name",
                   "operator": "match"}
        headers = {"Accept": "application/json", 'X-APIKeys': X_Apikeys}
        response = requests.request("POST", url, headers=headers, json=payload, params=querystring)
        response.data = json.loads(response.text)
        # print(response.data)
        for i in response.data['data']:
            # print(i)
            try:
                print('名称： ', i['name'], '   扫描id： ', i['last_scan']['scan_id'])
                if check_file_type == 'csv':
                    creat_report_csv(i['last_scan']['scan_id'])
                elif check_file_type == 'pdf':
                    creat_report_pdf(i['last_scan']['scan_id'])
            except TypeError:
                pass
        main()

    if task_root == 8:
        list_folder()
        try:
            check_folder_id = input('请选择您要下载报告的目录，输入目录名称： ')
            get_file_type = input('请选择您要生成报告的类型 （csv/pdf）： ')
        except ValueError:
            main()

        url = "https://cloud.tenable.com/was/v2/configs/search"
        querystring = {"limit": "10000"}
        payload = {"value": check_folder_id,
                   "field": "folder_name",
                   "operator": "match"}
        headers = {"Accept": "application/json", 'X-APIKeys': X_Apikeys}
        response = requests.request("POST", url, headers=headers, json=payload, params=querystring)
        response.data = json.loads(response.text)
        # print(response.data)
        for i in response.data['data']:
            # print(i)
            try:
                print('名称： ', i['name'], '   扫描id： ', i['last_scan']['scan_id'])
                if get_file_type == 'csv':
                    get_report_csv(i['last_scan']['scan_id'], i['name'])
                elif get_file_type == 'pdf':
                    get_report_pdf(i['last_scan']['scan_id'], i['name'])
            except TypeError:
                pass
        main()

if __name__ =='__main__':
    main()