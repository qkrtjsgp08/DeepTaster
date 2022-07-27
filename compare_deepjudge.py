# -*- coding: utf-8 -*-
"""Compare_deepJudge.ipynb

Automatically generated by Colaboratory.

Original file is located at
    https://colab.research.google.com/drive/1FwGREKyRhdHhVnPhIEVaus-NyK0jCpy9
"""

!pip install onnx

#!git clone https://github.com/Testing4AI/DeepJudge.git

!git clone https://github.com/onnx/onnx-tensorflow.git

!apt install --allow-change-held-packages libcudnn8=8.1.0.77-1+cuda11.2

# Commented out IPython magic to ensure Python compatibility.
# %cd onnx-tensorflow
!pip install -e .

import torch
import torch.nn as nn
import torch.nn.functional as F
import torch.optim as optim
from torchvision import datasets, transforms
from torch.autograd import Variable
import onnx
from onnx_tf.backend import prepare
import tensorflow as tf

# mount drive
from google.colab import drive
drive.mount('/content/drive')



import torch 
model=torch.load("/content/drive/MyDrive/Watermark_dnn/CIFAR_model_224input/resnet18.pt")

print(model)

model = nn.Sequential(*list(model.children())[:5])
#print(model)

device = torch.device("cuda:0" if torch.cuda.is_available() else "cpu")
dummy_input = Variable(torch.randn(1, 3, 32, 32)).to(device)
torch.onnx.export(model, dummy_input, "/content/drive/MyDrive/Watermark_dnn/onnxmodel/densenet.onnx")

model = onnx.load('/content/drive/MyDrive/Watermark_dnn/onnxmodel/densenet.onnx')
tf_rep = prepare(model)

# import numpy as np
# from IPython.display import display
# from PIL import Image
# tf_rep.export_graph('/content/drive/MyDrive/Watermark_dnn/tensormodel/save_test.h5')

# Commented out IPython magic to ensure Python compatibility.
# %cd /content/drive/MyDrive/Watermark_dnn/DeepJudge1/DeepJudge

!python seed_selection.py --model /content/drive/MyDrive/Watermark_dnn/CIFAR_model_224input/resnet18.pt --num 11

!python whitebox_generation.py --model /content/drive/MyDrive/Watermark_dnn/CIFAR_model_224input/resnet18.pt --seeds /content/drive/MyDrive/Watermark_dnn/DeepJudge1/DeepJudge/seeds/resnet_10seed.npz --layer 9



!python whitebox_evaluation.py --model /content/drive/MyDrive/Watermark_dnn/CIFAR_model_224input/resnet18.pt --suspect /content/drive/MyDrive/Watermark_dnn/cifar_dataset_experiment/transfer_office_freezing/freeze_70/models/resnet_200.pt --tests /content/drive/MyDrive/Watermark_dnn/DeepJudge1/DeepJudge/testcases

def seedSelection(model, x, y, num=1000, order='max'):
    #model.run(x)
    print(model.run(x))
    true_idx = np.where(np.argmax(model.run(x), axis=1) == np.argmax(y, axis=1))[0]
    x, y = x[true_idx], y[true_idx]
    ginis = np.sum(np.square(model(x).numpy()), axis=1)
    if order == 'max':
        ranks = np.argsort(-ginis)
    else:
        ranks = np.argsort(ginis)
    return x[ranks[:num]], y[ranks[:num]]



model=torch.load("/content/drive/MyDrive/Watermark_dnn/CIFAR_model_224input/resnet18.pt")
model = nn.Sequential(*list(model.children())[:0])
device = torch.device("cuda:0" if torch.cuda.is_available() else "cpu")
dummy_input = Variable(torch.randn(1, 3, 32, 32)).to(device)
torch.onnx.export(model, dummy_input, "/content/drive/MyDrive/Watermark_dnn/onnxmodel/densenet.onnx")
model = onnx.load('/content/drive/MyDrive/Watermark_dnn/onnxmodel/densenet.onnx')
tf_rep = prepare(model)

import numpy as np
from IPython.display import display
from PIL import Image
import tensorflow as tf
cifar10 = tf.keras.datasets.cifar10

(training_images, training_labels), (test_images, test_labels) = cifar10.load_data()
y_test = tf.keras.utils.to_categorical(test_labels, 10)
test_images =test_images.reshape(10000, 3, 32, 32)
x_test = test_images / 255.0
#x_test_data=tf.expand_dims(x_test[0], axis=0)
x_test_data=tf.cast(x_test, tf.float32)
#true_idx = np.where(np.argmax(tf_rep.run(x_test_data)[0], axis=1) == np.argmax(y_test, axis=1))[0]
#print(x_test_data.shape[1:])
#print(len(tf_rep.run(x_test_data)[0][0]))
#print(tf_rep.run(x_test_data)[0][0])
#print(tf_rep.run(x_test_data)[0])
print(tf_rep.run(x_test_data)[0].shape)
#seeds_x, seeds_y = seedSelection(tf_rep, x_test_data, y_test, num=opt.num, order=opt.order)

print(tf_rep.get_output_node_names())

