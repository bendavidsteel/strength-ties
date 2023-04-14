import json
import os

import pandas as pd

def get_negative_sentiment_score(scores):
    for score in scores:
        if score['label'] == 'negative':
            return score['score']
    return None

def get_negative_emotion_score(scores):
    max_negative_emotion_score = 0
    for score in scores:
        if score['label'] == 'anger' or score['label'] == 'fear' or score['label'] == 'disgust':
            if score['score'] > max_negative_emotion_score:
                max_negative_emotion_score = score['score']
    return max_negative_emotion_score

def main():
    this_dir_path = os.path.dirname(os.path.abspath(__file__))
    data_dir_path = os.path.join(this_dir_path, '..', 'data')
    cache_dir_path = os.path.join(data_dir_path, 'cache')
    scores_path = os.path.join(cache_dir_path, 'full_users_with_scores.csv')
    scores_df = pd.read_csv(scores_path)

    scores_df['sentiment'] = scores_df['sentiment'].apply(json.loads)
    scores_df['emotion'] = scores_df['emotion'].apply(json.loads)

    scores_df['negative_sentiment'] = scores_df['sentiment'].apply(get_negative_sentiment_score)
    scores_df['negative_emotion'] = scores_df['emotion'].apply(get_negative_emotion_score)

    output_dir_path = os.path.join(data_dir_path, 'outputs')
    user_scores_df = scores_df[['author_name', 'negative_sentiment', 'negative_emotion']] \
        .groupby('author_name').agg({'negative_sentiment': 'mean', 'negative_emotion': 'mean'}).reset_index()
    user_scores_df['negative_score'] = user_scores_df['negative_sentiment'] + user_scores_df['negative_emotion']
    user_scores_df.to_csv(os.path.join(output_dir_path, 'full_users_scores_agg.csv'), index=False)

if __name__ == '__main__':
    main()