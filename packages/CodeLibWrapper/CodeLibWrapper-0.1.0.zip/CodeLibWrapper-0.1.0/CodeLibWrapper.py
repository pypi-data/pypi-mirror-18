# -*- coding: utf-8 -*-
"""
Package: CodeLib For Data Production/API automatic testing Framework
Module: CodeLib
Dependency:
"""

# region   Import Library

import os
import sys

from API.APIReader import APIReader
from Database.SQLServerHelper import SQLServerHelper
from XMLFunction.EnvironmentConfig import EnvironmentConfig
from Network.EmailUtils import EmailUtils
from TextTools.RandomUtils import RandomUtils
from IO.SimpleFileCompare import file_compare, dir_compare

# endregion


class CodeLibWrapper:
    ROBOT_LIBRARY_SCOPE = 'GLOBAL'
    Author = "Benjamin Zhou"
    Version = "0.1.0"

    def __init__(self):
        reload(sys)
        sys.setdefaultencoding('utf8')
        pass

    # ====================框架信息===============================
    @staticmethod
    def show_about_information():
        """
        显示“关于信息”和“版本信息”
        :return: 返回作者和最后编辑的日期
        """
        basic_version = "Author: %s, Version: %s\nPython version: %s" % (
            CodeLibWrapper.Author, CodeLibWrapper.Version, sys.version)
        module_api_version = "    API Modules\n" + "        APIReader Version: %s" % APIReader.VERSION
        output = """
\n*************************************************************
Generation Information\n
%s
\n*************************************************************
Modules Version:\n
%s
"""
        return output % (basic_version, module_api_version)

    @staticmethod
    def send_email_to_admin(fromaddress, emailbody):
        """
        给这个框架的管理员发邮件，非常期待你的回馈
        :param fromaddress: 您的邮件地址，例如：Benjamin.zhou@morningstar.com
        :param emailbody: 回馈内容.例如：Bug 报告，功能需求
        :return: 邮件发送成功标志
        """
        adminaddress = ["Benjamin.Zhou@morningstar.com"]
        return EmailUtils.send_plainmail(adminaddress, fromaddress, "Robot Framework Feedback", emailbody)

    # ============= IO FileSystem==============================

    @staticmethod
    def iofilesysgetcurrentpath():
        """
        返回当前路径

        :return: path string
        """
        return os.getcwd()

    @staticmethod
    def iofilesysremovefile(filepath):
        """
        删除指定路径的文件

        :param filepath: 要删除文件的路径

        :return: 是否删除成功标志
        """
        try:
            os.remove(filepath)
            return True
        except IOError, e:
            print e
            return False

    @staticmethod
    def iofilesysgetfilelist(dirpath):
        """
        获取某指定目录下的所有文件的列表
        :param dirpath: 指定的目录
        :return:
        """
        dirpath = str(dirpath)
        if dirpath == "":
            return []
        dirpath = dirpath.replace("/", "\\")
        if dirpath[-1] != "\\":
            dirpath = dirpath + "\\"
        a = os.listdir(dirpath)
        b = [x for x in a if os.path.isfile(dirpath + x)]
        return b

    @staticmethod
    def iofilesysmakedir(dirpath):
        """
        创建指定目录
        :param dirpath:目录路径
        :return:
        """
        try:
            os.makedirs(dirpath)
            return True
        except IOError, e:
            print e
            return False

    @staticmethod
    def api_readwebservice_exoi(username, password, url):
        result = APIReader().access_exoi_api(url, username, password)
        return result

    @staticmethod
    def database_sqlserver_executescript(server, user, password, database_name, scripts):
        return SQLServerHelper(server, user, password).execute_sql_script(database_name, scripts)

    @staticmethod
    def config_get_parametervalue_by_name_and_environment(config_file_path, environment_name, parameter_name):
        """
        多环境参数配置读取。
        :param config_file_path: 参数配置文件的路径。在Windows环境下运行的RobotFramework中，需要用\\标识文件夹的分隔。例如：D:\\PythonCode\\CodeLib\\Template\\Sample_EnvironmentConfig.xml
        :param environment_name:要选取的环境变量名称
        :param parameter_name:要选取的参数名称
        :return: 返回参数值（string）
        """
        return EnvironmentConfig(config_file_path).read_environment_parameter_from_config(environment_name,
                                                                                          parameter_name)

    @staticmethod
    def utils_generate_random_string(length):
        """
        生成随机字符串
        :param length: 要生成的随机字符串长度
        :return:
        """
        return RandomUtils.genrandomstring(length)

    @staticmethod
    def send_plain_email(from_address, subject, content, to_address_list):
        result = EmailUtils.send_plainmail(to_address_list, from_address, subject, content)
        return result

    @staticmethod
    def assert_file_compare(source_file_path, target_file_path):
        return file_compare(source_file_path, target_file_path)

    @staticmethod
    def assert_dir_compare(source_dir_path, target_dir_path, output_report_path):
        dir_compare(source_dir_path, target_dir_path, output_report_path)


def main():
    print CodeLibWrapper.show_about_information()


if __name__ == '__main__':
    main()
