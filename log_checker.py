import os
import argparse
from datetime import datetime


class File():

    def __init__(self, file_path, range, line):
        self.file = dict()
        self.file["path"] = file_path
        self.file["time"] = self.__mtime()
        if self.__is_range(range):
            read = self.__read_file(line)
            self.file["range"] = True
            self.file["content"] = read[0]
            self.file["readable"] = read[1]
            self.file["err_msg"] = read[2]

        else:
            self.file["range"] = False

    def __is_range(self, range):
        hour = datetime.now() - datetime.fromtimestamp(self.file["time"])
        hour = hour.total_seconds() / 3600

        if range == 0 or hour <= range:
            return True
        else:
            return False

    def __mtime(self):
        try:
            return os.stat(self.file["path"]).st_mtime
        except:
            return 0

    def __read_file(self, line):
        read_list = list()

        try:
            with open(self.file["path"], "r") as f:
                readable = True
                err_msg = ""
                count = 0
                read = f.readlines()
                index = len(read)
                for i in read[::-1]:
                    if line == count and line != 0:
                        break

                    else:
                        count += 1
                        read_list.append("\033[90m" + str(index) + "\033[0m " + i.strip("\n"))
                        index -= 1
        except PermissionError:
            readable = False
            err_msg = "PermissionError"

        except UnicodeDecodeError:
            readable = False
            err_msg = "UnicodeDecodeError"
        except Exception as err:
            readable = False
            err_msg = str(err)

        return [read_list, readable, err_msg]

    def __str__(self):
        rstr = ""
        if self.file["readable"]:
            rstr += "\033[01m\033[32m#### \033[0m"
        else:
            rstr += "\033[01m\033[31m#### \033[0m"
        rstr += "\033[01m" + str(datetime.fromtimestamp(self.file["time"])) + "\t" + self.file["path"] + "\033[0m\n"

        for i in self.file["content"][::-1]:
            rstr += i + "\n"
        rstr += self.file["err_msg"] + "\n"
        return rstr

    def info(self):
        return self.file


class Logs():

    def __init__(self, range, line):
        self.filter_str = ""
        self.range = range
        self.line = line
        self.err_logs = list()
        self.readable_logs = list()

        for log in self.__log_files(self.range, line):
            info = log.info()
            if info["range"]:
                if info["readable"]:
                    self.readable_logs.append(log)
                else:
                    self.err_logs.append(log)

        def sortkey(file: File):
            return file.info()["time"]

        self.err_logs = sorted(self.err_logs, key=sortkey)
        self.readable_logs = sorted(self.readable_logs, key=sortkey)

    def filter(self, f_str):
        self.filter_str = f_str
        f_log = list()
        for log in self.readable_logs:
            for line in log.info()["content"]:
                if f_str in line:

                    red_line = line.replace(f_str, "\033[31m{}\033[0m".format(f_str))
                    index = log.info()["content"].index(line)
                    log.info()["content"][index] = red_line
                    if not log in f_log:
                        f_log.append(log)

        self.readable_logs = f_log

    def __log_files(self, range, line):
        logs_path = "/var/log"
        walk = os.walk(logs_path)
        for i in walk:
            for j in i[2]:
                file_path = i[0] + "/" + j
                log = File(file_path, range, line)
                yield log

    def report(self):
        r_log = len(self.readable_logs)
        e_log = len(self.err_logs)

        for log in self.readable_logs:
            print(log)

        print("\n\033[01m### REPORT - Hour:{} | Line: {} | Filter: {} \033[0m".format(self.range, self.line,
                                                                                      self.filter_str))
        print("\033[01m\033[32m### Total Log: {} \033[0m".format(r_log + e_log))
        print("\033[01m\033[32m# Readable Log: {} \033[0m".format(r_log))

        for log in self.readable_logs:
            time = str(datetime.fromtimestamp(log.info()["time"]))
            print(time + "\t" + log.info()["path"])

        print("\n\033[01m\033[31m# Unreadable Log :{}\033[0m".format(e_log))
        for log in self.err_logs:
            time = str(datetime.fromtimestamp(log.info()["time"]))
            print(time + "\t" + log.info()["path"] + "\t" + log.info()["err_msg"])


parser = argparse.ArgumentParser(description="Log Checker: /var/log dizini altındaki logları verilen parametrelere göre filtreler")

parser.add_argument("-r", "--range", required=True, help="Saat öncesinden itibaren log'ları kontrol et", type=float)
parser.add_argument("-l", "--line", required=True, help="Log'dan getirilecek satır sayısı", type=int)
parser.add_argument("-f", "--filter", help="Getirilen satır içinde filtrelenmek istenen kelime")
args = parser.parse_args()

logs = Logs(range=args.range, line=args.line)

if args.filter is not None:
    logs.filter(str(args.filter))

logs.report()

