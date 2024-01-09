import tensorflow as tf

def data_loader(train_df, val_df, test_df):
        # Create ImageDataGenerator
    train_generator = tf.keras.preprocessing.image.ImageDataGenerator(
        rescale=1./255,
        validation_split=0.2
    )
    test_generator = tf.keras.preprocessing.image.ImageDataGenerator(
        rescale=1./255
    )
    batch_size = 64
    size=(224, 224)
    # Change iamges to dataframe
    train_images = train_generator.flow_from_dataframe(
        dataframe=train_df,
        directory=None,
        x_col='Filepath',
        y_col=list(train_df.columns[1:]),
        weight_col=None,
        target_size=size,
        color_mode='rgb',
        classes=None,
        class_mode='raw',
        # color_mode='grayscale',
        batch_size=batch_size,
        shuffle=True,
        seed=42,
        save_to_dir=None,
        save_prefix='',
        save_format='png',
        subset='training',
        interpolation='nearest',
        validate_filenames=True,
    )

    val_images = train_generator.flow_from_dataframe(
        dataframe=val_df,
        directory=None,
        x_col='Filepath',
        # y_col='Age',
        y_col=list(train_df.columns[1:]),
        weight_col=None,
        target_size=size,
        color_mode='rgb',
        classes=None,
        class_mode='raw',
        # class_mode='categorical',
        # color_mode='grayscale',
        batch_size=batch_size,
        shuffle=True,
        seed=42,
        save_to_dir=None,
        save_prefix='',
        save_format='png',
        subset='validation',
        interpolation='nearest',
        validate_filenames=True,
    )
    test_images = test_generator.flow_from_dataframe(
        dataframe=test_df,
        directory=None,
        x_col='Filepath',
        # y_col='Age',
        y_col=list(train_df.columns[1:]),
        weight_col=None,
        target_size=size,
        color_mode='rgb',
        classes=None,
        class_mode='raw',
        # class_mode='categorical',
        # color_mode='grayscale',
        batch_size=batch_size,
        shuffle=False,
        save_to_dir=None,
        save_prefix='',
        save_format='png',
        interpolation='nearest',
        validate_filenames=True,
    )
    return train_images, val_images, test_images