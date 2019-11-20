from cleaneval_tool import *
from os.path import isfile, join
import json
import statistics
import re


def init_file_lang():
    file = open("doc_lg.json", "r")
    data = json.loads(file.read())
    file.close()
    return data


def get_files_by_lang(lang, data, tool):
    files = []
    for k in data.keys():
        path = "./" + tool + "/"
        if data[k] == lang and isfile(join(path, k)):
            files.append(k)
    return files


def compute_stat_2(files, pathTool, stats_by_file):
    stats = {"fscore": [], "precision": [], "recall": []}
    for file in files:
        result = evaluate_file(pathTool+"/"+file, "clean/"+file)
        stats["fscore"].append(result["f-score"])
        stats["precision"].append(result["precision"])
        stats["recall"].append(result["recall"])
        stats_by_file[file] = {"fscore": [result["f-score"]], "precision": [result["precision"]], "recall": [result["recall"]]}

    return {"fscore": statistics.mean(stats["fscore"]), "precision": statistics.mean(stats["precision"]), "recall": statistics.mean(stats["recall"])}


def regroup_stats_by_source(stats_by_file):
    stats_by_sources = {}
    for k in stats_by_file:
        source = get_source(k)
        if source in stats_by_sources:
            stats_by_sources[source]["fscore"].append(stats_by_file[k]["fscore"][0])
            stats_by_sources[source]["precision"].append(stats_by_file[k]["precision"][0])
            stats_by_sources[source]["recall"].append(stats_by_file[k]["recall"][0])
        else:
            stats_by_sources[source] = stats_by_file[k]
    return stats_by_sources


def get_source(str_with_source):
    return re.findall(r'_(.+?)_', str_with_source)[0]


def main():
    # Load file lang map
    mapFile = init_file_lang()

    # Computing stats
    tools = ["JT", "JT_langid", "JT_trueLg", "BS", "UF"]  # add others tool directories
    stats_by_file = {}
    for tool in tools:
        print("=========== " + tool + " ===========")
        print("========================"+len(tool)*"=")
        langs = ["English", "Russian", "Greek", "Polish", "Chinese"]  # add others languages
        total_stats = {"fscore": [], "precision": [], "recall": []}
        for lang in langs:
            # Get stats from files by lang
            files = get_files_by_lang(lang, mapFile, tool)
            stats = compute_stat_2(files, tool, stats_by_file)

            # Increment total stats
            total_stats["fscore"].append(stats["fscore"])
            total_stats["precision"].append(stats["precision"])
            total_stats["recall"].append(stats["recall"])

            # Print lang stat
            print("--------" + lang + "--------")
            print("F-Score mean: " + str(stats["fscore"]))
            print("Precision mean: " + str(stats["precision"]))
            print("Recall mean: " + str(stats["recall"]))

        # Print total stat
        print("--------TOTAL " + tool + "--------")
        print("F-Score total mean: " + str(statistics.mean(total_stats["fscore"])))
        print("Precision total mean: " + str(statistics.mean(total_stats["precision"])))
        print("Recall total mean: " + str(statistics.mean(total_stats["recall"])))

    # Save stats by source in a csv file
    file_score_source = open("scoreSource.csv", "w+")
    file_score_source.write("Source;F-Score;Precision;Recall\n")
    stats_by_sources = regroup_stats_by_source(stats_by_file)
    for source in stats_by_sources:
        fscore = str(statistics.mean(stats_by_sources[source]["fscore"]))
        precision = str(statistics.mean(stats_by_sources[source]["precision"]))
        recall = str(statistics.mean(stats_by_sources[source]["recall"]))
        file_score_source.write(source + ";" + fscore + ";" + precision + ";" + recall + "\n")

    file_score_source.close()


if __name__ == "__main__":
    main()
