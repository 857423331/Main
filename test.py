# Litm
# 时间：2021/6/27 11:46 下午
# Imports the Google Cloud client library
import csv
import os
import time
from multiprocessing import Pool

import json
from aliyunsdkcore.client import AcsClient
from aliyunsdkcore.request import CommonRequest

os.environ["GOOGLE_APPLICATION_CREDENTIALS"] = "/Users/lim/Downloads/crafty-shade-318122-e90d1d29a871.json"
from google.cloud import language_v1

core = 12

# Instantiates a client
client = language_v1.LanguageServiceClient()

word_list = []


def analize_google(texts):
    save_text = []
    save_score = []
    save_magnitude = []
    time1 = time.time()
    for text in texts:
        document = language_v1.Document(content=(text), type_=language_v1.Document.Type.PLAIN_TEXT)
        # Detects the sentiment of the text
        sentiment = client.analyze_sentiment(request={'document': document}).document_sentiment
        save_text.append(text)
        print("Text: {}".format(text))
        save_score.append(sentiment.score)
        save_magnitude.append(sentiment.magnitude)
        print("Sentiment: {}, {}".format(sentiment.score, sentiment.magnitude))

    time2 = time.time()
    print(time2 - time1)

    with open('/Users/lim/Desktop/MSC_project/data/out_google_Echo_Dot_(3).csv', 'a+', newline='',
              Ωencoding='utf-8') as csv_file:

        writer = csv.writer(csv_file)

        for i in range(len(save_text)):
            if float(save_score[i]) <= -1 / 3 and float(save_score[i]) >= -1:
                writer.writerow([save_text[i], save_score[i], "Negative"])
                with open('/Users/lim/Desktop/MSC_project/data/out_google_Echo_Dot_(3)_Negative.csv',
                          'a+', newline='', encoding='utf-8') as csv_file_Negative:
                    writer_Negative = csv.writer(csv_file_Negative)
                    writer_Negative.writerow([save_text[i]])

            elif float(save_score[i]) > -1 / 3 and float(save_score[i]) < 1 / 3:
                writer.writerow([save_text[i], save_score[i], "Neutral"])
                with open('/Users/lim/Desktop/MSC_project/data/out_google_Echo_Dot_(3)_Neutral.csv',
                          'a+', newline='', encoding='utf-8') as csv_file_Neutral:
                    writer_Neutral = csv.writer(csv_file_Neutral)
                    writer_Neutral.writerow([save_text[i]])
            elif float(save_score[i]) >= 1 / 3 and float(save_score[i]) <= 1:
                writer.writerow([save_text[i], save_score[i], "Positive"])
                with open('/Users/lim/Desktop/MSC_project/data/out_google_Echo_Dot_(3)_Positive.csv',
                          'a+', newline='', encoding='utf-8') as csv_file_Positive:
                    writer_Positive = csv.writer(csv_file_Positive)
                    writer_Positive.writerow([save_text[i]])

    time3 = time.time()
    print(time3 - time2)


def analize_ali(texts):
    client = AcsClient(
        "LTAI5tEpFacoG9YmoQpN9j9a",
        "varxb2ExFeaqYQ5To6I79OugfMNzWp",
        "cn-hangzhou"
    )
    save_text = []
    save_score = []
    time1 = time.time()
    for text in texts:
        try:
            request = CommonRequest()
            # domain和version是固定值
            request.set_domain('alinlp.cn-hangzhou.aliyuncs.com')
            request.set_version('2020-06-29')
            # action name可以在API文档里查到
            request.set_action_name('GetSaSeaEcom')
            # 需要add哪些param可以在API文档里查到
            request.add_query_param('ServiceCode', 'alinlp')
            if len(text) > 500:
                request.add_query_param('Text', text[0:500])
                save_text.append(text)
            else:
                request.add_query_param('Text', text)
                save_text.append(text)
            request.add_query_param('Language', 'en')
            response = client.do_action_with_exception(request)
            resp_obj = json.loads(response)
            if json.loads(resp_obj["Data"])['result']["output"][0] == 0.0:
                print(text)
                print("-" + str(json.loads(resp_obj["Data"])['result']["output"][1]))
                save_score.append("-" + str(json.loads(resp_obj["Data"])['result']["output"][1]))
            else:
                print(text)
                print(str(json.loads(resp_obj["Data"])['result']["output"][1]))
                save_score.append(str(json.loads(resp_obj["Data"])['result']["output"][1]))
        except:
            print("Error:" + text + "!" * 10)
    time2 = time.time()
    print(time2 - time1)
    with open('/Users/lim/Desktop/MSC_project/data/out_ali_Echo_Dot_(3).csv', 'a+', newline='',
              encoding='utf-8') as csv_file:
        writer = csv.writer(csv_file)
        for i in range(len(save_text)):
            if float(save_score[i]) <= -1 / 3 and float(save_score[i]) >= -1:
                writer.writerow([save_text[i], save_score[i], "Negative"])
                with open('/Users/lim/Desktop/MSC_project/data/out_ali_Echo_Dot_(3)_Negative.csv', 'a+', newline='',
                          encoding='utf-8') as csv_file_Negative:
                    writer_Negative = csv.writer(csv_file_Negative)
                    writer_Negative.writerow([save_text[i]])
            elif float(save_score[i]) > -1 / 3 and float(save_score[i]) < 1 / 3:
                writer.writerow([save_text[i], save_score[i], "Neutral"])
                with open('/Users/lim/Desktop/MSC_project/data/out_ali_Echo_Dot_(3)_Neutral.csv', 'a+', newline='',
                          encoding='utf-8') as csv_file_Neutral:
                    writer_Neutral = csv.writer(csv_file_Neutral)
                    writer_Neutral.writerow([save_text[i]])
            elif float(save_score[i]) >= 1 / 3 and float(save_score[i]) <= 1:
                writer.writerow([save_text[i], save_score[i], "Positive"])
                with open('/Users/lim/Desktop/MSC_project/data/out_ali_Echo_Dot_(3)_Positive.csv', 'a+', newline='',
                          encoding='utf-8') as csv_file_Positive:
                    writer_Positive = csv.writer(csv_file_Positive)
                    writer_Positive.writerow([save_text[i]])

    time3 = time.time()
    print(time3 - time2)


if __name__ == '__main__':
    with open('''/Users/lim/Desktop/MSC_project/data/Amazon_Echo_3_Reviews.csv''', 'r+', encoding='utf-8') as csv_file:
        readerline = csv.reader(csv_file)
        count = 0
        for text in readerline:
            if count == 0:
                count = 1
                continue
            word_list.append(text[2])
        csv_file.close()

    len_list = [0, 567, 1134, 1701, 2268, 2835, 3402, 3969, 4536, 5103, 5670, 6237, 6808]

    p = Pool(1)
    time1 = time.time()
    print(len(word_list))
    analize_google(word_list)
    analize_ali(word_list)
    for i in range(0, core):
        fore = int(len_list[i])
        rear = int(len_list[i + 1])
        # p.apply_async(analize_ali, args=(word_list[fore:rear],))
        # p.apply_async(analize_google, args=(word_list[fore:rear],))
        # time.sleep(30)

    print('Waiting for all subprocesses done...')
    p.close()
    p.join()
    print('All subprocesses done.')
