import requests
import pandas as pd
from bs4 import BeautifulSoup
import time
import re

from data_loader.accent_data_loader import AccentDataLoader
from accent_dataset.audio_downloader import AudioDownloader

ROOT_URL = 'http://accent.gmu.edu/'
BROWSE_LANGUAGE_URL = 'browse_language.php?function=find&language={}'
# WAIT = 1.2
WAIT = 0.1
DEBUG = True


def get_htmls(urls):
    '''
    Retrieves html in text form from ROOT_URL
    :param urls (list): List of urls from which to retrieve html
    :return (list): list of HTML strings
    '''
    htmls = []
    for url in urls:
        if DEBUG:
            print('downloading from {}'.format(url))
        htmls.append(requests.get(url).text)
        time.sleep(WAIT)

    return (htmls)


def build_search_urls(languages):
    '''
    creates url from ROOT_URL and languages
    :param languages (list): List of languages
    :return (list): List of urls
    '''
    return ([ROOT_URL + BROWSE_LANGUAGE_URL.format(language) for language in languages])


def parse_p(p_tag):
    '''
    Extracts href property from HTML <p> tag string
    :param p_tag (str): HTML string
    :return (str): string of link
    '''
    text = p_tag.text.replace(' ', '').split(',')
    return ([ROOT_URL + p_tag.a['href'], text[0], text[1]])


def get_bio(hrefs):
    '''
    Retrieves HTML from list of hrefs and returns bio information
    :param hrefs (list): list of hrefs
    :return (DataFrame): Pandas DataFrame with bio information
    '''

    htmls = get_htmls(hrefs)
    bss = [BeautifulSoup(html, 'html.parser') for html in htmls]
    rows = []
    bio_row = []
    for bs in bss:
        rows.append([li.text for li in bs.find('ul', 'bio').find_all('li')])
    for row in rows:
        bio_row.append(parse_bio(row))

    return (pd.DataFrame(bio_row))


def parse_bio(row):
    '''
    Parse bio data from row string
    :param row (str): Unparsed bio string
    :return (list): Bio columns
    '''
    cols = []
    for col in row:
        try:
            tmp_col = re.search((r"\:(.+)", col.replace(' ', '')).group(1))
        except:
            tmp_col = col
        cols.append(tmp_col)
    return (cols)


def create_dataframe(languages):
    '''

    :param languages (str): language from which you want to get html
    :return df (DataFrame): DataFrame that contains all audio metadata from searched language
    '''
    htmls = get_htmls(build_search_urls(languages))
    bss = [BeautifulSoup(html, 'html.parser') for html in htmls]
    persons = []

    for bs in bss:
        for p in bs.find_all('p'):
            if p.a:
                persons.append(parse_p(p))

    df = pd.DataFrame(persons, columns=['href', 'language_num', 'sex'])

    bio_rows = get_bio(df['href'])

    if DEBUG:
        print('loading finished')

    df['birth_place'] = bio_rows.iloc[:, 0]
    df['native_language'] = bio_rows.iloc[:, 1]
    df['other_languages'] = bio_rows.iloc[:, 2]
    df['age_sex'] = bio_rows.iloc[:, 3]
    df['age_of_english_onset'] = bio_rows.iloc[:, 4]
    df['english_learning_method'] = bio_rows.iloc[:, 5]
    df['english_residence'] = bio_rows.iloc[:, 6]
    df['length_of_english_residence'] = bio_rows.iloc[:, 7]

    # df['birth_place'] = df['birth_place'].apply(lambda x: x[:-6].split(' ')[-2:])
    df['birth_place'] = df['birth_place'].apply(lambda x: x[:-6].split(',')[-2:][1].strip())
    # print(df['birth_place'])
    # df['birth_place'] = lambda x: x[:-6].split(' ')[2:], df['birth_place']
    df['native_language'] = df['native_language'].apply(lambda x: x.split(' ')[2])
    # print(df['native_language'])
    # df['native_language'] = lambda x: x.split(' ')[2], df['native_language']
    df['other_languages'] = df['other_languages'].apply(lambda x: x.split(' ')[2:])
    # print(df['other_languages'])
    # df['other_languages'] = lambda x: x.split(' ')[2:], df['other_languages']
    df['age_sex'], df['age'] = df['age_sex'].apply(lambda x: x.split(' ')[2:]), df['age_sex'].apply(
        lambda x: x.replace('sex:', '').split(',')[1])
    # print(df['age'])
    # df['age_sex'] = lambda x: x.split(' ')[2], df['age_sex']
    # df['age_of_english_onset'] = lambda x: float(x.split(' ')[-1]), df['age_of_english_onset']
    df['age_of_english_onset'] = df['age_of_english_onset'].apply(lambda x: float(x.split(' ')[-1]))
    # print(df['age_of_english_onset'])
    # df['english_learning_method'] = lambda x: x.split(' ')[-1], df['english_learning_method']
    df['english_learning_method'] = df['english_learning_method'].apply(lambda x: x.split(' ')[-1])
    # print(df['english_learning_method'])
    # df['english_residence'] = lambda x: x.split(' ')[2:], df['english_residence']
    df['english_residence'] = df['english_residence'].apply(lambda x: x.split(' ')[2:])
    # print(df['english_residence'])
    # df['length_of_english_residence'] = lambda x: float(x.split(' ')[-2]), df['length_of_english_residence']
    df['length_of_english_residence'] = df['length_of_english_residence'].apply(lambda x: float(x.split(' ')[-2]))
    # print(df['length_of_english_residence'])

    # df['age'] = lambda x: x.replace(' ','').split(',')[0], df['age_sex']

    return df


def scrape(destination_file,
           languages,
           target_accent,
           only_target=False,
           download=True,
           input_file=""):

    output_file = AccentDataLoader.csv_path(destination_file)

    # dont download, read data from an input file to filter
    if input_file:
        df = pd.read_csv(input_file)
    else:
        df = create_dataframe(languages=languages)

    df.drop_duplicates(subset='language_num', inplace=True)

    # make all non-english natives to a different type
    df.loc[(df.native_language != "english"), 'new_native_language'] = "other"
    df.loc[(df.native_language == "english"), 'new_native_language'] = "english"

    # if we want only people of the target accent, we drop all english speakers born in different places
    if only_target:
        df.drop(df[(df.native_language == "english") & (df.birth_place != target_accent)].index, inplace=True)
    else:
        # we convert all the non target accent people to "other"
        df.loc[(df.native_language == "english") & (df.birth_place != target_accent), 'new_native_language'] = "other"

    # Filter metadata to retrieve only files desired
    df.drop(df[(df.length_of_english_residence > 10) & (df.native_language != "english")].index, inplace=True)

    df.to_csv(output_file, index=False)

    if download:
        downloader = AudioDownloader(csv_filepath=output_file,
                                     debug=True)
        downloader.get_audio()
