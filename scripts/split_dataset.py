import os

from pytok import utils

def main():
    this_dir = os.path.dirname(os.path.abspath(__file__))
    other_data_dir = os.path.join(this_dir, '..', '..', 'polar-seeds', 'data')
    data_dir = os.path.join(this_dir, '..', 'data')
    all_comments_path = os.path.join(other_data_dir, 'cache', 'related_comments.csv')

    comment_df = utils.get_comment_df(all_comments_path)
    english_comments_df = comment_df[comment_df['comment_language'] == 'en']

    english_comments_df = english_comments_df.sort_values(by='createtime')
    split = 0.5

    first_half_df = english_comments_df[:int(len(english_comments_df) * split)]
    second_half_df = english_comments_df[int(len(english_comments_df) * split):]

    cache_dir = os.path.join(data_dir, 'cache')
    if not os.path.exists(cache_dir):
        os.makedirs(cache_dir)

    first_half_df.to_csv(os.path.join(cache_dir, 'first_half.csv'), index=False)
    second_half_df.to_csv(os.path.join(cache_dir, 'second_half.csv'), index=False)

if __name__ == '__main__':
    main()