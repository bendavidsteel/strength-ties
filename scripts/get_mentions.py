import os

import matplotlib.pyplot as plt
import pandas as pd

def str_to_list(stri):
    if ',' not in stri:
        return []
    return [word.strip()[1:-1] for word in stri[1:-1].split(',')]

def main():
    this_dir_path = os.path.dirname(os.path.abspath(__file__))
    data_dir_path = os.path.join(this_dir_path, '..', 'data')
    cache_dir_path = os.path.join(data_dir_path, 'cache')
    second_half_path = os.path.join(cache_dir_path, 'second_half.csv')

    second_half_df = pd.read_csv(second_half_path)
    
    second_half_df['mentions'] = second_half_df['mentions'].apply(str_to_list)
    second_half_df['mention_count'] = second_half_df['mentions'].apply(len)
    second_half_df['unique_mentions'] = second_half_df['mentions'].apply(lambda x: len(set(x)))
    second_half_df['mean_mentions'] = second_half_df['mention_count'] / second_half_df['unique_mentions']
    user_mentions = second_half_df[['author_id', 'mention_count', 'unique_mentions', 'mean_mentions']].groupby('author_id').sum()
    user_mentions = user_mentions.reset_index()

    # graph distribution of user mentions
    fig, axes = plt.subplots(nrows=1, ncols=3)
    for i, col in enumerate(['mention_count', 'unique_mentions', 'mean_mentions']):
        axes[i].hist(user_mentions[col], bins=100)
        axes[i].set_yscale('log')
        axes[i].set_xlabel(col.replace('_', ' ').capitalize())
        axes[i].set_ylabel('count')

    outputs_dir_path = os.path.join(data_dir_path, 'outputs')
    plt.savefig(os.path.join(outputs_dir_path, 'user_mentions.png'))

    user_mentions.to_csv(os.path.join(outputs_dir_path, 'user_mentions.csv'), index=False)

if __name__ == '__main__':
    main()