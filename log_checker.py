# -*- coding: UTF-8 -*-

import os, getopt, sys
from datetime import datetime

class Color():
    @staticmethod
    def bold(str):
        return "\033[01m"+str + "\033[0m"

    @staticmethod
    def green(str):
        return "\033[32m"+str + "\033[0m"

    @staticmethod
    def lightgrey(str):
        return  "\033[37m"+str + "\033[0m"

    @staticmethod
    def red(str):
        return "\033[31m" + str + "\033[0m"


class File():

    def __init__(self, file_path):
        self.__file_path = file_path
        self.__line_count = 1
        self.__rstr = "\n"
        try:

            self._f_time = self.__m_time(self.__file_path)
            self.__rstr += "\033[01m\033[32m#####\033[0m\033[01m {} : {} \033[0m \n".format(datetime.fromtimestamp(self._f_time), self.__file_path)

        except Exception as err:
            self._f_time = 0
            self.__rstr += "\033[31m#####\033[0m\033[01m{} \033[0m \n".format(err)


    def line_limit(self, limit):
        self.__line_count = abs(limit)

    def __m_time(self,file_path):
        return os.stat(self.__file_path).st_mtime


    def __str__(self):
        line_list = self.__read_log()
        for i in line_list[::-1]:
            self.__rstr += "\033[90m" + str(i[0]) + " \033[0m" +  str(i[1])

        return self.__rstr

    def __read_log(self):
        read_list = list()

        try:
            with open(self.__file_path, "r") as file:
                count = 0
                read = file.readlines()
                for i in read[::-1]:
                    if self.__line_count == count:
                        break

                    else:
                        count += 1
                        read_list.append((read.index(i) + 1, i))

        except Exception as err:
            read_list.append(("\033[31m!\033[0m", err))


        return read_list

    def is_range(self, r_hour=24):
        hour = datetime.now() - datetime.fromtimestamp(self._f_time)
        hour = hour.total_seconds() / 3600

        if self._f_time == 0 or hour <= r_hour:
            return True
        else:
            return False



def log_files(read_line):
    logs_path = "/var/log"
    walk = os.walk(logs_path)

    for i in walk:
        for j in i[2]:
            file_path = i[0] + "/" + j
            log = File(file_path)
            log.line_limit(read_line)
            yield log


count = 0
for i in log_files(5):
    if i.is_range(0.5):
        count +=1
        print(i)


print("\n\033[01m\033[32mRapor: \033[0m/var/log 'da {} saat içinde loglama yapılmış olabilecek toplam {} dosya bulundu \n".format(5,count))

