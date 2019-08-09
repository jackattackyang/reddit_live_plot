import praw
import time
import csv
import pandas as pd
import altair as alt

class redditpost():
    def __init__(self, submission_id, csv_dir='data/'):
        self.submission_id = submission_id
        self.csv_file = csv_dir + self.submission_id +'.csv'
        
        self.reddit = praw.Reddit(client_id, client_secret,user_agent)

    def get_data(self):
        self.post = self.reddit.submission(submission_id=self.submission_id)
        return [self.post.title, self.post.title.score, self.post.created_utc]

    def to_csv(self):
        with open(self.csv_file, 'a') as f:
            writer = csv.writer(f)
            writer.writerows(self.get_data())

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
            self.save_alt_html
            time.sleep(5)