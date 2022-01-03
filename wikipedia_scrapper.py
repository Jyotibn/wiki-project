import base64
import re
import requests
import os
import os.path
from selenium.webdriver.common.by import By
from nltk.corpus import stopwords
from nltk.tokenize import word_tokenize, sent_tokenize




class scrapper:

    def __init__(self, search_string, driver):
        """contains the search_string,driver,thumbnail_of_images and no of image"""
        try:
            self.search_string = search_string
            self.driver = driver



        except Exception as e:
            print("error in init() of scrapper class--" + str(e))

    def links(self):
        """for getting links in refrence"""
        try:
            links = self.driver.find_elements(By.TAG_NAME, "a.external.text")
            refrence_links = []
            for link in links:
                refrence_links.append(link.get_attribute('href'))
            print("got all the reference links")
            return refrence_links
        except Exception as e:
            print("error in links() of scrapper class--" + str(e))

    def information(self):
        """for getting the information in the page"""
        try:

            target_path = 'C:/Users/malik/PycharmProjects/wiki_project/information'
            name_of_folder = self.search_string
            folder_for_text = self.create_the_folder(target_path=target_path, name_of_folder=name_of_folder)

            info = self.driver.find_elements(By.TAG_NAME, "p")  # this will give the entire text inside the <p> tag
            str_of_text = ''
            for i in info:
                str_of_text = str_of_text + i.text + "\n"




            f = open(os.path.join(folder_for_text, 'text'), 'w', encoding='utf-8')
            f.write(str_of_text)
            f.close()
            return str_of_text
        except Exception as e:
            print("error in information() of scrapper class--" + str(e))

    def make_the_summary(self):
        """this will give the summary of the above information collected"""
        try:
            # Input text - to summarize

            text = self.information()
            text = re.sub("[\(\[].*?[\)\]]", "", text)  # to remove brackets from the text

            # Tokenizing the text
            stopWords = set(stopwords.words("english"))
            words = word_tokenize(text)

            # Creating a frequency table to keep the
            # score of each word

            freqTable = dict()
            for word in words:
                word = word.lower()
                if word in stopWords:
                    continue
                if word in freqTable:
                    freqTable[word] += 1
                else:
                    freqTable[word] = 1

            # Creating a dictionary to keep the score
            # of each sentence
            sentences = sent_tokenize(text)
            sentenceValue = dict()

            for sentence in sentences:
                for word, freq in freqTable.items():
                    if word in sentence.lower():
                        if sentence in sentenceValue:
                            sentenceValue[sentence] += freq
                        else:
                            sentenceValue[sentence] = freq

            sumValues = 0
            for sentence in sentenceValue:
                sumValues += sentenceValue[sentence]

            # Average value of a sentence from the original text

            average = int(sumValues / len(sentenceValue))

            # Storing sentences into our summary.
            summary = ''
            for sentence in sentences:
                if (sentence in sentenceValue) and (sentenceValue[sentence] > (1.2 * average)):
                    summary += " " + sentence

            target_path = 'C:/Users/malik/PycharmProjects/wiki_project/information'
            name_of_folder = self.search_string
            folder_for_summary = self.create_the_folder(target_path=target_path, name_of_folder=name_of_folder)

            f = open(os.path.join(folder_for_summary, 'summary'), 'w', encoding='utf-8')
            f.write(summary)
            f.close()
            print("summary is stored ")
            return summary
        except Exception as e:
            print("error in make_the_summary() of scrapper class--" + str(e))

    def create_the_folder(self, target_path: str, name_of_folder: str):
        """this will create the folder for image"""
        try:

            # search_string folder will be created inside image folder
            target_folder = os.path.join(target_path, '_'.join(name_of_folder.lower().split(' ')))
            if not os.path.exists(target_folder):  # checking if folder does not exist then make it
                os.makedirs(target_folder)

            return target_folder
        except Exception as e:
            print("error in create_the_folder() of scrapper class--" + str(e))

    def image_url(self):
        """this will give the url of images"""
        try:
            urls = set()
            count = 0
            images = self.driver.find_elements(By.TAG_NAME, "img")
            for img in images:

                if img.get_attribute('src') and 'https' in img.get_attribute('src'):
                    urls.add(img.get_attribute('src'))
                    count = count + 1

            print(count, " urls are found")
            return urls
        except Exception as e:
            print("error in image_url() of scrapper class--" + str(e))

    def store_images_in_folder_and_in_base64_format(self, urls):
        """this will store the images in a folder and convert the url of each image in base64 image"""
        try:
            list_base64_image = []
            count = 1
            target_path = 'C:/Users/malik/PycharmProjects/wiki_project/images'
            name_of_folder = self.search_string
            folder = self.create_the_folder(target_path=target_path, name_of_folder=name_of_folder)

            for i in urls:
                image_content = requests.get(i).content
                list_base64_image.append(base64.b64encode(image_content))
                f = open(os.path.join(folder, 'jpg' + '_' + str(count) + '.jpg'), 'wb')
                f.write(image_content)
                f.close()
                count = count + 1
            print("images are converted to base64 format")
            return list_base64_image
        except Exception as e:
            print("error in store_images_in_folder_and_in_base64_format() of scrapper class--" + str(e))












