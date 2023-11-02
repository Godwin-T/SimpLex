import os
import gzip
import shutil
import requests
from nltk import word_tokenize

nltk.download("punkt")
nltk.download("averaged_perceptron_tagger")

def generate_dictionary_unigrams(path):
    """
    Generates a unigram dictionary file containig each word from the corpus given as path

    The structure of the generated file is: word number_of_appearences number_of_sencences_in_which_it_appears
    The name of the generated file is dictionary_unigrams

    Parameters:
    path (string): The path to the corpus file
    """
    f = open(path, "r")

    count = 1
    dictionary = {}
    for line in f:
        print(count, end='\r')
        tokens = word_tokenize(line)
        tokens = list(filter(lambda x: any(c.isalpha() for c in x), tokens))
        tokens = list(map(lambda x: x.lower(), tokens))
        seen = []
        for token in tokens:
            if token in dictionary:
                dictionary[token][0] += 1
                if token not in seen:
                    dictionary[token][1] += 1
                    seen.append(token)
            else:
                dictionary[token] = [1, 1]
        count += 1

    res = open("./datasets/dictionary_unigrams", "w")
    for token in dictionary:
        res.write(token + " " + str(dictionary[token][0]) + " " + str(dictionary[token][1]) + "\n")
    print("Unigram dictionary generation complete")

def download_file(url, save_path):
    if not os.path.exists(save_path):
        print(save_path)
        response = requests.get(url)
        if response.status_code == 200:
            with open(save_path, 'wb') as file:
                file.write(response.content)
            print(f"File downloaded and saved to {save_path}")
        else:
            print("Failed to download the file")
    else:
        print('File exists in directory')

def unzip_file(gz_file, extracted_file_path):

    if not os.path.exists(extracted_file_path):
        with gzip.open(gz_file, 'rb') as f_in, open(extracted_file_path, 'wb') as f_out:
            shutil.copyfileobj(f_in, f_out)

        print(f"File '{gz_file}' has been extracted to '{extracted_file_path}'.")
    else:
        print('File exists')

extract_path = './datasets/new/news.2007.en.shuffled.deduped.txt'
file_url = 'https://data.statmt.org/news-crawl/en/news.2007.en.shuffled.deduped.gz'
gz_file_location = './datasets/new/news.2007.en.shuffled.deduped.gz'

if __name__=='__main__':
    download_file(file_url, gz_file_location)
    unzip_file(gz_file_location, extract_path)
    generate_dictionary_unigrams(extract_path)
