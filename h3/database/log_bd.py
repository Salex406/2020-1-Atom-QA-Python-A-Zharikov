import argparse
import os
import sys
from orm_builder import MysqlOrmLogBuilder
from mysql_orm_client import MysqlOrmConnection


if __name__ == '__main__':
    args = sys.argv[1:]
    parser = argparse.ArgumentParser()
    path = os.path.join(os.getcwd(), "nginx.log")
    parser.add_argument("-i", "--input", help="input file", default="None")
    p = parser.parse_args(args)
    if p.input != "None":
        path = p.input

    connection = MysqlOrmConnection('test', 'root', 'LOG')
    log_b = MysqlOrmLogBuilder(connection)
    log_b.create_log_db()

    with open(path, "r") as f:
        for line in f.readlines():
            line = line.split()
            ip = line[0]
            time = line[3] + line[4]
            method = line[5][1:]
            url = line[6]
            code = line[8]
            log_b.add_log(url, code, method, ip)
