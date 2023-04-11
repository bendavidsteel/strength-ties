import json
import os

import pandas as pd
import transformers
import tqdm

def get_max_label(scores):
    max_score = max(scores, key=lambda x: x['score'])
    return max_score['label'], max_score['score']

def main():
    this_dir_path = os.path.dirname(os.path.abspath(__file__))
    data_dir_path = os.path.join(this_dir_path, '..', 'data', 'cache')
    first_half_path = os.path.join(data_dir_path, 'first_half.csv')

    first_half_df = pd.read_csv(first_half_path)

    batch_size = 32
    emotion_classifier = transformers.pipeline("text-classification", model="j-hartmann/emotion-english-distilroberta-base", return_all_scores=True, batch_size=batch_size)
    sentiment_classifier = transformers.pipeline("text-classification", model="j-hartmann/sentiment-roberta-large-english-3-classes", return_all_scores=True, batch_size=batch_size)

    for i in tqdm.tqdm(range(0, len(first_half_df) + batch_size, batch_size)):
        batch_df = first_half_df[i:min(i + batch_size, len(first_half_df))]
        texts = batch_df['text'].tolist()
        emotion_scores = emotion_classifier(texts)
        sentiment_scores = sentiment_classifier(texts)
        for j, row in batch_df.iterrows():
            first_half_df.loc[j, 'emotion'] = json.dumps(emotion_scores[j - i])
            first_half_df.loc[j, 'sentiment'] = json.dumps(sentiment_scores[j - i])

    first_half_df.to_csv(os.path.join(data_dir_path, 'first_half_with_scores.csv'), index=False)

if __name__ == '__main__':
    main()