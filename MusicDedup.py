import hashlib
import os
import sys
import pandas as pd
from kivy.app import App
from kivy.uix.button import Button

BASEDIR="/home/kuper/Desktop/kuper - External/music"
PICKLE_FILE='/tmp/music_hash.pickle'

def calculate():
    big_list = []
    count = 0
    for root, subdirs, files in os.walk(BASEDIR, topdown=False):
        for file in files:
            filename = (root + '/' + file)
            f_hash = hashlib.md5(open(filename, 'rb').read()).hexdigest()
            big_list.append({'root': root, 'file': file, 'file_hash': f_hash})
            count += 1

    df = pd.DataFrame(big_list)
    print('{} files hashed'.format(count))
    df.to_pickle(PICKLE_FILE)

def df_work():
    df = pd.read_pickle(PICKLE_FILE)
    gdf = (df.groupby('file_hash').count()
           .rename(columns={"file": "file_count"})
           .drop(columns={"root"}))
    print(gdf.head())
    print(df.head())
    joined_df = df.join(gdf, on='file_hash')
    joined_df = joined_df[joined_df.file_count > 1].sort_values(['file_hash'])
    print(joined_df.to_string())
    print(joined_df.count())


class MusicDedupApp(App):
    def build(self):
        return Button(text='Hello World')

if __name__ == '__main__':
    pd.set_option('display.max_colwidth', 100)
    df_work()
    MusicDedupApp().run()