import argparse
import os
import sys
import pandas


if __name__ == '__main__':
    args = sys.argv[1:]
    parser = argparse.ArgumentParser()
    path = os.path.join(os.getcwd(), "nginx.log")
    parser.add_argument("-i", "--input", help="input file", default="None")
    p = parser.parse_args(args)
    if p.input != "None":
        path = p.input
    pandas.set_option('display.max_columns', 6)
    with open(path, "r") as f:
        df = pandas.read_csv(f,
                             sep=r'\s(?=(?:[^"]*"[^"]*")*[^"]*$)(?![^\[]*\])',
                             engine='python',
                             usecols=[0, 3, 4, 5, 6],
                             names=['ip', 'time', 'request', 'status', 'size'],
                             na_values='-',
                             header=None
                             )
        f.seek(0)
        str = f.read()
    df.style.hide_index()
    cl_err = (df["status"] >= 400) & (df["status"] < 500)
    redir = (df["status"] >= 300) & (df["status"] < 400)
    df_cl_err_s = df[cl_err].sort_values(by=['size'], ascending=False)
    redir_s = df[redir].sort_values(by=['size'], ascending=False)
    df_sorted = df.sort_values(by=['size'], ascending=False)

    get = str.count("GET")
    post = str.count("POST")
    head = str.count("HEAD")
    put = str.count("PUT")
    delete = str.count("DELETE")
    connect = str.count("CONNECT")
    options = str.count("OPTIONS")
    trace = str.count("TRACE")
    patch = str.count("PATCH")
    n_req = len(str.splitlines())
    with open("results_p.txt", "w") as f:
        f.write(f"Число запросов: {n_req}\n")
        f.write(f"GET: {get}\n")
        f.write(f"POST: {post}\n")
        f.write(f"HEAD: {head}\n")
        f.write(f"PUT: {put}\n")
        f.write(f"DELETE: {delete}\n")
        f.write(f"CONNECT: {connect}\n")
        f.write(f"OPTIONS: {options}\n")
        f.write(f"TRACE: {trace}\n")
        f.write(f"PATCH: {patch}\n")
        f.write("Топ 10 запросов ПО размеру:\n")
        f.write(df.head(10).to_string(index=False) + "\n")
        f.write("Топ 10 запросов с клиентской ошибкой:\n")
        f.write(df_cl_err_s.head(10).to_string(index=False) + "\n")
        f.write("Топ 10 запросов с редиректами:\n")
        f.write(redir_s.head(10).to_string(index=False) + "\n")
