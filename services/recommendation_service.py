import numpy as np
import pandas as pd
import tensorflow as tf
from sklearn.preprocessing import MultiLabelBinarizer

from repositories.recommendation_repository import RecommendationRepository
from utils.als_model import ALSModel


class RecommendationService:

    def __init__(self, db):
        self.db = db
        self.recommendation_repo = RecommendationRepository(db)

        self.films_df = pd.read_csv('films.csv')
        self.books_df = pd.read_csv('books.csv', delimiter=';', encoding='utf-8')

        # Предобработка данных
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

    def get_recommendations(self, collection_id, watched_ids, user_id):
        # Определяем коллекцию и `features` в зависимости от типа коллекции
        if collection_id == '2435466':  # ID фильмов
            df = self.films_df
            features = df.drop(columns=[
                'id', 'url', 'Name', 'PosterLink', 'Actors', 'Director',
                'Description', 'DatePublished', 'Keywords', 'ReviewAurthor',
                'ReviewDate', 'ReviewBody', 'duration'
            ])
            watched_items = df[df['id'].isin(watched_ids)]
        elif collection_id == '9875768':  # ID книг
            df = self.books_df
            features = df.drop(columns=[
                'id', 'Filename', 'PosterLink', 'Name',
                'Author', 'Category ID'
            ])
            watched_ids = list(map(str, watched_ids))
            watched_items = df[df['id'].astype(str).isin(watched_ids)]
        else:
            return None, "Invalid collection ID"

        # Проверка на наличие просмотренных элементов
        if watched_items.empty:
            return None, "No valid watched items found"

        # Получаем размерность для модели и создаем `ALSModel` с этой размерностью
        input_dim = features.shape[1]
        output_dim = input_dim  # Здесь можно изменить, если требуется другая выходная размерность
        self.als_model = ALSModel(input_dim=input_dim, output_dim=output_dim)

        # Обучаем модель
        labels = features.copy()
        self.als_model.train_model(features, labels)

        # Генерация эмбеддингов
        embeddings = self.als_model.generate_embeddings(features)
        watched_indices = watched_items.index.to_numpy()
        watched_indices_tensor = tf.convert_to_tensor(watched_indices, dtype=tf.int32)
        watched_embeddings = tf.gather(embeddings, watched_indices_tensor)

        # Расчет сходства
        similarity_scores = self.als_model.calculate_similarity(embeddings, watched_embeddings)
        top_indices = tf.argsort(similarity_scores, axis=1, direction='DESCENDING')[:, :10]
        recommended_items = [df.iloc[idx].to_dict() for idx in top_indices.numpy().flatten()]

        for item in recommended_items:
            try:
                recommendation_id = int(item['id'])
                image = item.get('PosterLink')
                title = item.get('Name')
                self.recommendation_repo.add_or_update_recommendation(
                    collection_id=int(collection_id),
                    user_id=user_id,
                    recommendation_id=recommendation_id,
                    image=image,
                    title=title
                )
            except (KeyError, ValueError) as e:
                print(f"Error saving recommendation: {e}")

        recommendations = RecommendationRepository.get_recommendations_by_user_and_collection(collection_id, user_id)

        recommendations_list = [{
            'id': recommendation.id,
            'collection_id': recommendation.collection_id,
            'user_id': recommendation.user_id,
            'recommendation_id': recommendation.recommendation_id,
            'title': recommendation.title,
            'image': recommendation.image
        } for recommendation in recommendations]

        return recommendations_list, None

    def get_items_from_collection(self, collection_id, limit=10, offset=0):
        # Определяем коллекцию, которую нужно отправить
        if collection_id == '2435466':  # ID фильмов
            df = self.films_df
        elif collection_id == '9875768':  # ID книг
            df = self.books_df
        else:
            return None, "Invalid collection ID"

        # Ограничиваем результаты по limit и offset
        items = df[['id', 'Name']].iloc[offset:offset + limit]

        # Преобразуем id в int64, чтобы избежать переполнения
        items['id'] = items['id'].apply(pd.to_numeric, errors='coerce').astype(np.int64)

        # Преобразуем данные в список словарей
        items_list = items.to_dict(orient='records')

        return items_list, None

