import os

from pytok import utils

def main():
    this_dir = os.path.dirname(os.path.abspath(__file__))
    data_dir = os.path.join(this_dir, '..', 'data')
    all_comments_path = os.path.join(data_dir, 'cache', 'related_comments.csv')

    cache_dir = os.path.join(data_dir, 'cache')
    if not os.path.exists(cache_dir):
        os.makedirs(cache_dir)

    comment_df = utils.get_comment_df(all_comments_path)
    english_comments_df = comment_df[comment_df['comment_language'] == 'en']

    all_users_path = os.path.join(data_dir, 'cache', 'all_users.csv')
    user_df = utils.get_user_df(all_users_path)

    user_comments_df = english_comments_df.merge(user_df, left_on='author_name', right_on='uniqueId', how='left', suffixes=('', '_user'))

    user_comments_df = user_comments_df[user_comments_df['followingCount'].notna()]
    user_comments_df.to_csv(os.path.join(cache_dir, 'full_users.csv'), index=False)

    english_comments_df = english_comments_df.sort_values(by='createtime')

    split = 0.5
    first_half_df = english_comments_df[:int(len(english_comments_df) * split)]
    second_half_df = english_comments_df[int(len(english_comments_df) * split):]

    first_half_df.to_csv(os.path.join(cache_dir, 'first_half.csv'), index=False)
    second_half_df.to_csv(os.path.join(cache_dir, 'second_half.csv'), index=False)

if __name__ == '__main__':
    main()