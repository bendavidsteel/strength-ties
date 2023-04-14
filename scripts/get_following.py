import datetime
import os

import matplotlib.pyplot as plt
import numpy as np
import pandas as pd

def main():
    this_dir_path = os.path.dirname(os.path.abspath(__file__))
    data_dir_path = os.path.join(this_dir_path, '..', 'data')
    cache_path = os.path.join(data_dir_path, 'cache')

    first_half_path = os.path.join(cache_path, 'full_users.csv')
    user_comments_df = pd.read_csv(first_half_path)

    users_df = user_comments_df[['uniqueId', 'followingCount', 'followerCount', 'videoCount', 'diggCount', 'verified', 'createtime_user']].drop_duplicates()
    users_df['bverified'] = users_df['verified'].apply(lambda x: 1 if x else 0)
    users_df['createtime_user'] = pd.to_datetime(users_df['createtime_user'])
    users_df['age_in_months'] = ((pd.to_datetime('today', utc=True) - users_df['createtime_user']) / np.timedelta64(1, 'M')).astype(int)

    # graph distribution of user following
    fig, axes = plt.subplots(nrows=1, ncols=1)
    axes.hist(users_df['followingCount'], bins=100)
    axes.set_yscale('log')
    axes.set_xlabel('Following Count')
    axes.set_ylabel('Frequency')
    axes.set_title('Distribution of User Following Counts')

    outputs_dir_path = os.path.join(data_dir_path, 'outputs')
    plt.savefig(os.path.join(outputs_dir_path, 'user_following.png'))

    users_df.to_csv(os.path.join(outputs_dir_path, 'full_users_following.csv'), index=False)

if __name__ == '__main__':
    main()