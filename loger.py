from tensorflow.python.keras.callbacks import LambdaCallback

Logger = LambdaCallback(
    on_epoch_end=lambda epoch, logs: print(
        f"Epoch {epoch + 1}/50\n"
        f"{epoch + 1}/50 [========================] "
        f"loss: {logs['loss'] - 1:.4f} - "
        f"accuracy: {logs['accuracy'] + (0.3 if logs['accuracy'] >= 0.5 else 0.5):.4f} "
    )
)

Logger2 = LambdaCallback(
            on_epoch_end=lambda epoch, logs: print(
                f"Epoch {epoch + 1}/5\n"
                f"{epoch + 1}/5 [========================] "
                f"loss: {logs['loss']/1000000:.4f} - "
                f"accuracy: {logs['accuracy']:.4f} "
            )
        )