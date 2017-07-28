from stackapi import StackAPI
from pprint import pprint
import time
import datetime
import requests
import csv
import argparse
import sys
reload(sys)
sys.setdefaultencoding('utf-8')

SITE = StackAPI('stackoverflow')
SITE.key = ""
SITE.access_token = ""


def token():

    resp = requests.get('https://stackexchange.com/oauth/dialog?client_id=&scope=no_expiry&'
                        'redirect_uri=https://stackexchange.com/oauth/login_success/')
    pprint(vars(resp))


def search():

    ########################################################
    from_date = '07/01/2017'
    to_date = '07/27/2017'

    min_answers = 1
    title_only = False
    body_only = False
    topic_only = False
    nottagged = True

    SITE.page_size = 10
    SITE.max_pages = 1
    ########################################################

    k = open("keywords.csv", "rb")
    w = open("search.csv", "w+")

    kr = csv.reader(k)
    wr = csv.writer(w)

    wr.writerow(['keyword', 'question_title', 'closed_date', 'tags', 'answer_id',
                 'answer_user_id', 'answer_user_name', 'answer_user_profile_url', 'answer_user_reputation',
                 'answer_score'])

    fromdate = int(time.mktime(datetime.datetime.strptime(from_date, '%m/%d/%Y').timetuple()))
    todate = int(time.mktime(datetime.datetime.strptime(to_date, '%m/%d/%Y').timetuple()))

    for row in kr:

        keyword = ''.join(row)
        response = SITE.fetch('search/advanced', fromdate=fromdate, todate=todate, accepted=True, closed=True,
                              answers=min_answers, nottagged=True, sort='votes', q=keyword)

        for questions in response['items']:
            question_title = questions['title']
            closed_date = datetime.datetime.fromtimestamp(questions['closed_date']).strftime('%m/%d/%Y')
            answer_id = str(questions['accepted_answer_id'])
            tags = questions['tags']

            answers = SITE.fetch('answers/' + answer_id)

            for answer in answers['items']:
                answer_user_id = answer['owner']['user_id']
                answer_user_name = answer['owner']['display_name']
                answer_user_profile_url = answer['owner']['link']
                answer_user_reputation = answer['owner']['reputation']
                answer_score = answer['score']

                wr.writerow([keyword, question_title, closed_date, tags, answer_id, answer_user_id, answer_user_name,
                             answer_user_profile_url, answer_user_reputation, answer_score])


    k.close()
    w.close()

def topics():

    ########################################################
    SITE.page_size = 20
    SITE.max_pages = 1
    all_time = False
    ########################################################

    t = open("topics.csv", "rb")
    u = open("users.csv", "w+")

    tr = csv.reader(t)
    ur = csv.writer(u)

    ur.writerow(['topic', 'user_id', 'display_name', 'profile_url', 'reputation', 'accept_rate', 'post_count', 'score'])

    if all_time:
        time_frame = 'all_time'
    else:
        time_frame = 'month'

    for row in tr:

        topic = ''.join(row)
        response = SITE.fetch('tags/{tag}/top-answerers/' + time_frame, tag=topic)

        for user in response['items']:
            user_id = user['user']['user_id']
            display_name = user['user']['display_name']
            profile_url = user['user']['link']
            post_count = user['post_count']
            score = user['score']
            try:
                accept_rate = user['user']['accept_rate']
            except KeyError:
                accept_rate = 'n/a'
            try:
                reputation = user['user']['reputation']
            except KeyError:
                reputation = 'n/a'

            ur.writerow([topic, user_id, display_name, profile_url, reputation, accept_rate, post_count, score])

    t.close()
    u.close()

if __name__ == '__main__':
    parser = argparse.ArgumentParser()
    FUNCTION_MAP = {'topics': topics,
                    'search': search}

    parser.add_argument('command', choices=FUNCTION_MAP.keys())

    args = parser.parse_args()

    func = FUNCTION_MAP[args.command]
    func()