import csv

from os import listdir, remove
from os.path import isfile, join, exists
from statistics import mean, stdev


def remove_csv():
    if exists('./stats.csv') and isfile('./stats.csv'):
        remove('./stats.csv')


def write_to_csv(data):
    with open('./stats.csv', 'w+') as csvfile:
        csvwriter = csv.writer(csvfile, delimiter=';', quotechar='|', quoting=csv.QUOTE_MINIMAL)
        csvwriter.writerow(['Type', 'Nombre lignes', 'Nombre caracteres', 'Moyenne lignes', 'Moyenne caracteres', 'Ecart-type lignes', 'Ecart-type caracteres', 'Moyenne de difference (carac)', 'Ecart-type de difference (carac)'])

        for row in data:
            csvwriter.writerow(row)


def read_values(path: str) -> tuple:
    print('Gettings lines and chars from path : ' + path)

    files_tuple = list(), list()

    files = [f for f in listdir(path) if isfile(join(path, f))]
    files.sort()  # To make sure the list order is the same on every call
    for file in files:
        lines = 0
        chars = 0

        with open(path + file, 'r', encoding='utf-8') as content_file:
            for line in content_file.readlines():
                lines += 1
                for char in line:
                    chars += 1

        files_tuple[0].append(lines)
        files_tuple[1].append(chars)

    return files_tuple


def compute_stats():
    remove_csv()

    data = list()

    justext = read_values('./JT/')
    beautifulsoup = read_values('./BS/')
    clean = read_values('./clean/')
    justext_langid = read_values('./JT_langid/')
    justext_truelg = read_values('./JT_trueLg/')

    justext_diff = list()
    beautifulsoup_diff = list()
    justext_langid_diff = list()
    justext_truelg_diff = list()

    for i in range(len(clean[1])):
        justext_diff.append(abs(justext[1][i] - clean[1][i]))
        beautifulsoup_diff.append(abs(beautifulsoup[1][i] - clean[1][i]))
        justext_langid_diff.append(abs(justext_langid[1][i] - clean[1][i]))
        justext_truelg_diff.append(abs(justext_truelg[1][i] - clean[1][i]))

    # Compute average lines and chars from clean files
    clean_lines = sum(clean[0])
    clean_chars = sum(clean[1])
    clean_lines_avg = mean(clean[0])
    clean_chars_avg = mean(clean[1])
    clean_lines_stdev = stdev(clean[0])
    clean_chars_stdev = stdev(clean[1])

    data.append(['CLEAN', str(clean_lines), str(clean_chars), str(clean_lines_avg), str(clean_chars_avg),
                  str(clean_lines_stdev), str(clean_chars_stdev)])

    # Compute average lines and chars from justext
    justext_lines = sum(justext[0])
    justext_chars = sum(justext[1])
    justext_lines_avg = mean(justext[0])
    justext_chars_avg = mean(justext[1])
    justext_lines_stdev = stdev(justext[0])
    justext_chars_stdev = stdev(justext[1])
    justext_avg = mean(justext_diff)
    justext_stdev = stdev(justext_diff)

    data.append(['JUSTEXT', str(justext_lines), str(justext_chars), str(justext_lines_avg), str(justext_chars_avg),
                  str(justext_lines_stdev), str(justext_chars_stdev), str(justext_avg), str(justext_stdev)])

    # Compute average lines and chars from justext with langid
    justext_langid_lines = sum(justext_langid[0])
    justext_langid_chars = sum(justext_langid[1])
    justext_langid_lines_avg = mean(justext_langid[0])
    justext_langid_chars_avg = mean(justext_langid[1])
    justext_langid_lines_stdev = stdev(justext_langid[0])
    justext_langid_chars_stdev = stdev(justext_langid[1])
    justext_langid_diff_avg = mean(justext_langid_diff)
    justext_langid_diff_stdev = stdev(justext_langid_diff)

    data.append(['JUSTEXT-LANGID', str(justext_langid_lines), str(justext_langid_chars), str(justext_langid_lines_avg),
                  str(justext_langid_chars_avg), str(justext_langid_lines_stdev), str(justext_langid_chars_stdev),
                  str(justext_langid_diff_avg), str(justext_langid_diff_stdev)])

    # Compute average lines and chars from justext with true lang
    justext_truelg_lines = sum(justext_truelg[0])
    justext_truelg_chars = sum(justext_truelg[1])
    justext_truelg_lines_avg = mean(justext_truelg[0])
    justext_truelg_chars_avg = mean(justext_truelg[1])
    justext_truelg_lines_stdev = stdev(justext_truelg[0])
    justext_truelg_chars_stdev = stdev(justext_truelg[1])
    justext_truelg_diff_avg = mean(justext_truelg_diff)
    justext_truelg_diff_stdev = stdev(justext_truelg_diff)

    data.append(['JUSTEXT-TRUELG', str(justext_truelg_lines), str(justext_truelg_chars), str(justext_truelg_lines_avg),
                  str(justext_truelg_chars_avg), str(justext_truelg_lines_stdev), str(justext_truelg_chars_stdev),
                  str(justext_truelg_diff_avg), str(justext_truelg_diff_stdev)])

    # Compute average lines and chars from bf4
    bf4_lines = sum(beautifulsoup[0])
    bf4_chars = sum(beautifulsoup[1])
    bf4_lines_avg = mean(beautifulsoup[0])
    bf4_chars_avg = mean(beautifulsoup[1])
    bf4_lines_stdev = stdev(beautifulsoup[0])
    bf4_chars_stdev = stdev(beautifulsoup[1])
    beautifulsoup_avg = mean(beautifulsoup_diff)
    beautifulsoup_stdev = stdev(beautifulsoup_diff)

    data.append(['BEAUTIFUL_SOUP', str(bf4_lines), str(bf4_chars), str(bf4_lines_avg), str(bf4_chars_avg),
                  str(bf4_lines_stdev), str(bf4_chars_stdev), str(beautifulsoup_avg), str(beautifulsoup_stdev)])

    write_to_csv(data)


if __name__ == '__main__':
    compute_stats()