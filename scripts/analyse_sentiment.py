import json
import os

import pandas as pd

def get_top_label(scores):
    return max(scores, key=lambda x: x['score'])['label']

def get_top_score(scores):
    return max(scores, key=lambda x: x['score'])['score']

def main():
    this_dir_path = os.path.dirname(os.path.abspath(__file__))
    data_dir_path = os.path.join(this_dir_path, '..', 'data', 'cache')
    first_half_path = os.path.join(data_dir_path, 'first_half_with_scores.csv')
    scores_df = pd.read_csv(first_half_path)

    scores_df['emotion'] = scores_df['emotion'].apply(json.loads)
    scores_df['sentiment'] = scores_df['sentiment'].apply(json.loads)

    scores_df['emotion_label'] = scores_df['emotion'].apply(get_top_label)
    scores_df['sentiment_label'] = scores_df['sentiment'].apply(get_top_label)

    scores_df['emotion_score'] = scores_df['emotion'].apply(get_top_score)
    scores_df['sentiment_score'] = scores_df['sentiment'].apply(get_top_score)

    print(scores_df['emotion_label'].value_counts())
    print(scores_df['sentiment_label'].value_counts())

    # get some samples
    scores_sample = scores_df[['text', 'emotion_label', 'emotion_score', 'sentiment_label', 'sentiment_score']].sample(100)
    scores_sample.to_csv(os.path.join(data_dir_path, 'first_half_samples.csv'), index=False)

if __name__ == '__main__':
    main()