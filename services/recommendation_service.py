import pandas as pd
import tensorflow as tf
from sklearn.preprocessing import MultiLabelBinarizer

from utils.als_model import ALSModel


class RecommendationService:

    def __init__(self):
        self.films_df = pd.read_csv('films.csv')
        self.books_df = pd.read_csv('books.csv', delimiter=';', encoding='utf-8')

        self.films_df = self.preprocess_data(self.films_df, 'film')
        self.books_df = self.preprocess_data(self.books_df, 'book')

        self.als_model = ALSModel()

    def preprocess_data(self, df, collection_type):
        if collection_type == 'film':
            df['Genres'] = df['Genres'].apply(lambda x: x.split(',') if isinstance(x, str) else [])
            df = self.encode_genres(df, 'Genres')
        else:
            df['Category'] = df['Category'].apply(lambda x: x.split(',') if isinstance(x, str) else [])
            df = self.encode_genres(df, 'Category')
        return df

    def encode_genres(self, df, column):
        mlb = MultiLabelBinarizer()
        df_genres_encoded = pd.DataFrame(mlb.fit_transform(df[column]), columns=mlb.classes_, index=df.index)
        df = pd.concat([df, df_genres_encoded], axis=1)
        df.drop(columns=[column], inplace=True)
        return df

    def get_recommendations(self, collection_id, watched_ids):
        if collection_id == '2435466':
            df = self.films_df
        elif collection_id == '9875768':
            df = self.books_df
        else:
            return None, "Invalid collection ID"

        watched_items = df[df['id'].isin(watched_ids)]
        if watched_items.empty:
            return None, "No valid watched items found"

        features = df.drop(columns=['id', 'url', 'Name', 'PosterLink', 'Actors', 'Director',
                                    'Description', 'DatePublished', 'Keywords', 'ReviewAurthor',
                                    'ReviewDate', 'ReviewBody', 'duration'])

        labels = features.copy()
        self.als_model.train_model(features, labels)

        embeddings = self.als_model.generate_embeddings(features)

        watched_indices = watched_items.index.to_numpy()

        watched_indices_tensor = tf.convert_to_tensor(watched_indices, dtype=tf.int32)

        watched_embeddings = tf.gather(embeddings, watched_indices_tensor)  # Use tf.gather for indexing

        similarity_scores = self.als_model.calculate_similarity(embeddings, watched_embeddings)

        top_indices = tf.argsort(similarity_scores, axis=1, direction='DESCENDING')[:, :10]

        recommended_items = [df.iloc[idx].to_dict() for idx in
                             top_indices.numpy().flatten()]

        return recommended_items, None


