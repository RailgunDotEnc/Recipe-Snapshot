#!/usr/bin/env python
# coding: utf-8

# In[1]:


get_ipython().system(' pip install transformers datasets')


# In[2]:


get_ipython().system('pip install transformers datasets evaluate')


# In[3]:


from datasets import load_dataset


# In[4]:


from huggingface_hub import notebook_login

notebook_login()


# In[5]:


food = load_dataset("imagefolder", data_dir="/Users/adesai/Desktop/Recipe/dataset")


# In[6]:


food


# In[7]:


labels = food["train"].features["label"].names
label2id, id2label = dict(), dict()
for i, label in enumerate(labels):
    label2id[label] = str(i)
    id2label[str(i)] = label


# In[8]:


from transformers import AutoImageProcessor

checkpoint = "google/vit-base-patch16-224-in21k"
image_processor = AutoImageProcessor.from_pretrained(checkpoint)


# In[9]:


from tensorflow import keras
from tensorflow.keras import layers

size = (image_processor.size["height"], image_processor.size["width"])

train_data_augmentation = keras.Sequential(
    [
        layers.RandomCrop(size[0], size[1]),
        layers.Rescaling(scale=1.0 / 127.5, offset=-1),
        layers.RandomFlip("horizontal"),
        layers.RandomRotation(factor=0.02),
        layers.RandomZoom(height_factor=0.2, width_factor=0.2),
    ],
    name="train_data_augmentation",
)

val_data_augmentation = keras.Sequential(
    [
        layers.CenterCrop(size[0], size[1]),
        layers.Rescaling(scale=1.0 / 127.5, offset=-1),
    ],
    name="val_data_augmentation",
)


# In[10]:


import numpy as np
import tensorflow as tf
from PIL import Image


def convert_to_tf_tensor(image: Image):
    np_image = np.array(image)
    tf_image = tf.convert_to_tensor(np_image)
    # `expand_dims()` is used to add a batch dimension since
    # the TF augmentation layers operates on batched inputs.
    return tf.expand_dims(tf_image, 0)


def preprocess_train(example_batch):
    """Apply train_transforms across a batch."""
    images = [
        train_data_augmentation(convert_to_tf_tensor(image.convert("RGB"))) for image in example_batch["image"]
    ]
    example_batch["pixel_values"] = [tf.transpose(tf.squeeze(image)) for image in images]
    return example_batch


def preprocess_val(example_batch):
    """Apply val_transforms across a batch."""
    images = [
        val_data_augmentation(convert_to_tf_tensor(image.convert("RGB"))) for image in example_batch["image"]
    ]
    example_batch["pixel_values"] = [tf.transpose(tf.squeeze(image)) for image in images]
    return example_batch


# In[11]:


food["train"].set_transform(preprocess_train)
food["test"].set_transform(preprocess_val)


# In[12]:


from transformers import DefaultDataCollator

data_collator = DefaultDataCollator(return_tensors="tf")


# In[13]:


import evaluate

accuracy = evaluate.load("accuracy")


# In[14]:


import numpy as np


def compute_metrics(eval_pred):
    predictions, labels = eval_pred
    predictions = np.argmax(predictions, axis=1)
    return accuracy.compute(predictions=predictions, references=labels)


# In[15]:


from transformers import create_optimizer

batch_size = 16
num_epochs = 5
num_train_steps = len(food["train"]) * num_epochs
learning_rate = 3e-5
weight_decay_rate = 0.01

optimizer, lr_schedule = create_optimizer(
    init_lr=learning_rate,
    num_train_steps=num_train_steps,
    weight_decay_rate=weight_decay_rate,
    num_warmup_steps=0,
)


# In[16]:


from transformers import TFAutoModelForImageClassification

model = TFAutoModelForImageClassification.from_pretrained(
    checkpoint,
    id2label=id2label,
    label2id=label2id,
)


# In[17]:


# converting our train dataset to tf.data.Dataset
tf_train_dataset = food["train"].to_tf_dataset(
    columns=["pixel_values"], label_cols=["label"], shuffle=True, batch_size=batch_size, collate_fn=data_collator
)

# converting our test dataset to tf.data.Dataset
tf_eval_dataset = food["test"].to_tf_dataset(
    columns=["pixel_values"], label_cols=["label"], shuffle=True, batch_size=batch_size, collate_fn=data_collator
)


# In[18]:


from tensorflow.keras.losses import SparseCategoricalCrossentropy

loss = tf.keras.losses.SparseCategoricalCrossentropy(from_logits=True)
model.compile(optimizer=optimizer, loss=loss)


# In[19]:


import os
print(os.getcwd())


# In[20]:


from transformers.keras_callbacks import KerasMetricCallback, PushToHubCallback

metric_callback = KerasMetricCallback(metric_fn=compute_metrics, eval_dataset=tf_eval_dataset)
save_callback = keras.callbacks.ModelCheckpoint(
    'checkpoint/',
    save_weights_only = False,
    monitor = 'accuracy',
    save_best_only = False
)
callbacks = [metric_callback, save_callback]


# In[21]:


model.fit(tf_train_dataset, validation_data=tf_eval_dataset, epochs=num_epochs, callbacks=callbacks)


# In[40]:


ds = load_dataset("imagefolder", data_dir="/Users/adesai/Desktop/Recipe/dataset", split="test")
image = ds["image"][6]


# In[41]:


ds


# In[42]:


image


# In[35]:


img = Image.open("/Users/adesai/Desktop/Recipe/test.jpg")
image = img


# In[36]:


image


# In[43]:


image = val_data_augmentation(convert_to_tf_tensor(image.convert("RGB")))
image = tf.transpose(tf.squeeze(image))
image = tf.expand_dims(image, 0)


# In[44]:


prediction = model(image)
predicted_class_idx = tf.argmax(prediction.logits, axis=-1).numpy()[0]
predicted_class = id2label[str(predicted_class_idx)]

print(f"The predicted class is {predicted_class}")


# In[30]:


tf.saved_model.save(model, 'saved/')


# In[33]:


loaded_model = tf.saved_model.load('/Users/adesai/Desktop/Recipe/saved')


# In[34]:


prediction = loaded_model(image)
predicted_class_idx = tf.argmax(prediction.logits, axis=-1).numpy()[0]
predicted_class = id2label[str(predicted_class_idx)]

print(f"The predicted class is {predicted_class}")


# In[38]:


model.summary()


# In[39]:


model.save('/Users/adesai/Desktop/Recipe/testing')


# In[ ]:




