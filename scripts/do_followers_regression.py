import os

import pandas as pd
import patsy

import statsmodels.api as sm

def main():
    this_dir_path = os.path.dirname(os.path.abspath(__file__))
    data_dir_path = os.path.join(this_dir_path, '..', 'data', 'outputs')
    second_half_scores_path = os.path.join(data_dir_path, 'full_users_scores_agg.csv')
    first_half_users_path = os.path.join(data_dir_path, 'full_users_following.csv')

    second_half_scores_df = pd.read_csv(second_half_scores_path)
    first_half_users_df = pd.read_csv(first_half_users_path)

    merged_df = pd.merge(first_half_users_df, second_half_scores_df, left_on='uniqueId', right_on='author_name', how='inner')

    independent_variables = ['followingCount', 'followerCount', 'videoCount', 'diggCount', 'bverified', 'age_in_months']
    dependent_variables = ['negative_sentiment', 'negative_emotion', 'negative_score']
    for dependent_variable in dependent_variables:
        formula = f"{dependent_variable} ~ {' + '.join(independent_variables)}"
        y, X = patsy.dmatrices(formula, data=merged_df, return_type='dataframe')
        mod = sm.OLS(y, X)
        res = mod.fit()
        print(res.summary())

        fig = sm.graphics.plot_partregress_grid(res)
        fig.tight_layout(pad=1.0)
        fig.savefig(os.path.join(data_dir_path, f'followers_regression_{dependent_variable}.png'))

if __name__ == '__main__':
    main()