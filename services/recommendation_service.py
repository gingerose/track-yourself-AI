import pandas as pd
import tensorflow as tf
from sklearn.preprocessing import MultiLabelBinarizer
from sklearn.metrics.pairwise import cosine_similarity


class RecommendationService:

    def __init__(self):

        self.films_df = pd.read_csv('films.csv')
        self.books_df = pd.read_csv('books.csv', delimiter=';', encoding='utf-8')

        self.films_df = self.preprocess_data(self.films_df, 'film')
        self.books_df = self.preprocess_data(self.books_df, 'book')

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
        if collection_id == '2435466':  # Фильмы
            df = self.films_df
        elif collection_id == '9875768':  # Книги
            df = self.books_df
        else:
            return None, "Invalid collection ID"

        watched_items = df[df['id'].isin(watched_ids)]

        if watched_items.empty:
            return None, "No valid watched items found"

        # Генерируем эмбеддинги для элементов
        embeddings = self.generate_embeddings(df)

        # Вычисляем рекомендации
        recommendations = self.calculate_similar_items(embeddings, watched_items, df)

        return recommendations, None

    def generate_embeddings(self, df):
        model = tf.keras.Sequential([
            tf.keras.layers.Dense(128, activation='relu'),
            tf.keras.layers.Dense(64, activation='relu'),
            tf.keras.layers.Dense(32, activation='relu')
        ])

        features = df.drop(columns=['id', 'url', 'Name', 'PosterLink',  'Actors', 'Director',
                                    'Description', 'DatePublished', 'Keywords', 'ReviewAurthor',
                                    'ReviewDate', 'ReviewBody', 'duration'])  # Оставляем только числовые признаки

        print("Features before conversion (first 5 rows):")
        print(features.head())

        features = features.astype('float32')

        print("Features before conversion (first 5 rows):")
        print(features.head())

        embeddings = model.predict(features)

        return embeddings

    def calculate_similar_items(self, embeddings, watched_items, df):
        watched_embeddings = embeddings[watched_items.index]

        similarity_scores = cosine_similarity(watched_embeddings, embeddings)

        top_indices = similarity_scores.argsort()[:, -10:][:, ::-1]
        recommended_items = [df.iloc[idx] for idx in top_indices.flatten()]

        print("Recommended items before conversion:")
        print(recommended_items)

        recommendations_list = [item.to_dict() for item in recommended_items]

        print("Recommendations list (first 5):")
        print(recommendations_list[:5])

        return recommendations_list

