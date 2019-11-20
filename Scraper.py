import json

from justext import justext
from bs4 import BeautifulSoup
from os import listdir, remove
from os.path import isfile, join
from langid import classify

from Utils import get_stoplist

from Stats import compute_stats, compute_diff_stats, compute_classified_diff_stats


def clean_scrapes():
    for path in ('./JT/', './BS/', './JT_langid/', './JT_trueLg/'):
        files = [f for f in listdir(path) if isfile(join(path, f))]
        for file in files:
            remove(path + file)

        print('Cleaned scrapes at : ' + path)


def scrape_with_justext():
    print('Scraping with justext.')

    files = [f for f in listdir('./html/') if isfile(join('./html/', f))]
    for file in files:
        with open('./html/' + file, 'r', encoding='utf-8', errors='ignore') as content_file:
            paragraphs = justext(content_file.read(), get_stoplist('English'))

            with open('./JT/' + file, 'w+', encoding='utf-8') as scraped_file:
                for paragraph in paragraphs:
                    if not paragraph.is_boilerplate:
                        scraped_file.write('<p>' + paragraph.text + '</p>\n')

    print('Justext scraping done.')


def scrape_with_beautifulsoup():
    print('Scraping with beautiful soup 4.')

    files = [f for f in listdir('./html/') if isfile(join('./html/', f))]
    for file in files:
        with open('./html/' + file, 'r', encoding='utf-8', errors='ignore') as content_file:
            soup = BeautifulSoup(content_file.read(), 'html.parser')

            with open('./BS/' + file, 'w+', encoding='utf-8') as scraped_file:
                for paragraph in soup.get_text().split('\n'):
                    if paragraph:
                        scraped_file.write('<p>' + paragraph + '</p>\n')

    print('Beautiful soup 4 scraping done.')


def classify_with_langid():
    # This methods uses langid classify on the original html file instead of the one initially produced by justext.
    # Justext can't extract without language, this causes blank files

    print('Using langid to improve justext files.')

    languages = {'ru': 'Russian', 'el': 'Greek', 'en': 'English', 'pl': 'Polish', 'zh': 'Chinese'}

    files = [f for f in listdir('./html/') if isfile(join('./html/', f))]
    for file in files:
        with open('./html/' + file, 'r', encoding='utf-8', errors='ignore') as content:
            text = content.read()
            lang = classify(text)[0]

            paragraphs = justext(text, get_stoplist(languages[lang]))
            with open('./JT_langid/' + file, 'w+', encoding='utf-8') as scraped_file:
                for paragraph in paragraphs:
                    if not paragraph.is_boilerplate:
                        scraped_file.write('<p>' + paragraph.text + '</p>\n')

    print('Done.')


def classify_with_true_lang():
    print('Using true language to improve justext files.')

    with open('doc_lg.json', 'r') as f:
        files_langs = json.load(f)

    files = [f for f in listdir('./html/') if isfile(join('./html/', f))]
    for file in files:
        with open('./html/' + file, 'r', encoding='utf-8', errors='ignore') as content:

            paragraphs = justext(content.read(), get_stoplist(files_langs[file]))
            with open('./JT_trueLg/' + file, 'w+', encoding='utf-8') as scraped_file:
                for paragraph in paragraphs:
                    if not paragraph.is_boilerplate:
                        scraped_file.write('<p>' + paragraph.text + '</p>\n')

    print('Done.')


def exercice2():
    classify_with_langid()
    classify_with_true_lang()

    compute_classified_diff_stats()


def exercice1():
    clean_scrapes()

    scrape_with_justext()
    scrape_with_beautifulsoup()

    compute_stats()
    compute_diff_stats()


def main():
    exercice1()
    exercice2()


if __name__ == '__main__':
    main()
