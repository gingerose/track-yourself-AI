import tensorflow as tf

from loger import Logger2


class ALSModel:

    def __init__(self, input_dim, output_dim):
        self.model = tf.keras.Sequential([
            tf.keras.layers.Dense(256, activation='relu', input_shape=(input_dim,)),
            tf.keras.layers.BatchNormalization(),
            tf.keras.layers.Dropout(0.3),
            tf.keras.layers.Dense(128, activation='relu'),
            tf.keras.layers.BatchNormalization(),
            tf.keras.layers.Dense(64, activation='relu'),
            tf.keras.layers.Dense(output_dim, activation='relu')
        ])
        self.model.compile(optimizer='adam', loss='mse', metrics=['accuracy'])

    def train_model(self, features, labels, epochs=5, batch_size=100):
        history = self.model.fit(
            features, labels,
            epochs=epochs,
            batch_size=batch_size,
            validation_split=0.2,
            verbose=0,
            callbacks=[Logger2]
        )

        return history

    @tf.function
    def generate_embeddings(self, features):
        features = tf.cast(features, dtype=tf.float32)
        return self.model(features)

    @tf.function
    def calculate_similarity(self, embeddings, watched_embeddings):
        embeddings_normalized = tf.nn.l2_normalize(embeddings, axis=1)
        watched_embeddings_normalized = tf.nn.l2_normalize(watched_embeddings, axis=1)
        similarity_scores = tf.matmul(watched_embeddings_normalized, embeddings_normalized, transpose_b=True)
        return similarity_scores
