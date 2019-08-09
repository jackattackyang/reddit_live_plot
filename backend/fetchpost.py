import yaml

import praw
import time
import csv
import pandas as pd
import altair as alt

conf = yaml.load(open('application.yml'))
client_id = conf['client']['id']
client_secret = conf['client']['secret']
user_agent = conf['user_agent']

class redditpost():
    def __init__(self, submission_id, csv_dir='data/'):
        self.submission_id = submission_id
        self.csv_file = csv_dir + self.submission_id +'.csv'
        
        self.reddit = praw.Reddit(client_id=client_id, client_secret=client_secret,user_agent=user_agent)

    def get_data(self):
        self.post = self.reddit.submission(id=self.submission_id)
        return [self.post.title, self.post.upvote_ratio, self.post.score, time.time()]

    def to_csv(self):
        with open(self.csv_file, 'a') as f:
            writer = csv.writer(f)
            writer.writerows([self.get_data()])

    def save_alt_html(self):
        df = pd.read_csv(self.csv_file, names=['title', 'upvote_ratio', 'upvotes', 'time'])
        df['time'] = pd.to_datetime(df['time'], unit='s')
        chart = alt.Chart(df).mark_line().encode(
            x = 'time',
            y = 'upvote_ratio')
        chart.save('chart.html')

    def auto_data(self):
        while True:
            self.to_csv()
            self.save_alt_html()
            time.sleep(5)