import os

import matplotlib.pyplot as plt
import pandas as pd

def main():
    this_dir_path = os.path.dirname(os.path.abspath(__file__))
    data_dir_path = os.path.join(this_dir_path, '..', 'data', 'cache')
    second_half_path = os.path.join(data_dir_path, 'second_half.csv')

    second_half_df = pd.read_csv(second_half_path)
    
    second_half_df['mention_count'] = second_half_df['mentions'].apply(lambda x: len(x.split(',')))
    user_mentions = second_half_df[['author_id', 'mention_count']].groupby('author_id').sum()
    user_mentions = user_mentions.reset_index()

    # graph distribution of user mentions
    plt.hist(user_mentions['mention_count'], bins=100)
    plt.yscale('log')
    plt.title('Distribution of User Mentions')
    plt.xlabel('Number of Mentions')
    plt.ylabel('Frequency')

    plt.savefig(os.path.join(data_dir_path, 'user_mentions.png'))

    user_mentions.to_csv(os.path.join(data_dir_path, 'user_mentions.csv'), index=False)

if __name__ == '__main__':
    main()