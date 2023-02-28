
"""
Generate DFT images
"""

import torchvision.models as models
import torch
import torch.optim as optim
import torch.nn.functional as F
import torchvision
import torchvision.datasets as datasets
import torchvision.transforms as transforms
from torchvision.transforms import ToTensor 
from torch import nn
from keras.datasets import cifar100
import tensorflow as tf
import matplotlib.pyplot as plt
import cv2
import numpy as np
import os
import foolbox as fb
import argparse

parser = argparse.ArgumentParser(description='DFT image generation')
parser.add_argument('--model',type=str, help='model path')
parser.add_argument('--architecture', default='Resnet18', type=str, help='model architecture: Resnet18, Vgg16, Densenet161, Alexnet')
parser.add_argument('--label', type=str, help='model label')
#parser.add_argument('--dataset', default='cifar100', type=str, help='dataset for DFT image ganeration')
parser.add_argument('--type', default='all', type=str, help='type of DFT images: all/test/val/train')
parser.add_argument('--output', default='./DFTimages', type=str, help='DFT images saved dir')


if __name__ == '__main__':

    opt = parser.parse_args()
    device = torch.device("cuda:0" if torch.cuda.is_available() else "cpu")
    #Load model
    #Load Pretrained imagenet model
    if opt.model == 'Imagenet':
        torch.__version__
        torch.cuda.is_available()
        if opt.architecture == 'Resnet18':
            model=models.resnet101(pretrained=True)
        elif opt.architecture == 'Densenet161':
            model=models.densenet161(pretrained=True)
        elif opt.architecture == 'Alexnet':
            model=models.Alexnet(pretrained=True)
        elif opt.architecture == 'Vgg16':
            model=models.vgg16(pretrained=True)
    else:
        model=torch.load(opt.model)
        model = model.to(device)
    model.eval()

    if not os.path.exists(opt.output):
        os.mkdir(opt.output)
    #load dataset

    (X_train, y_train), (X_test1, y_test1) = cifar100.load_data()
    X_test1=X_test1.reshape(10000,3,32,32)
    y_test1=tf.keras.utils.to_categorical(y_test1)
    X_test1=X_test1/255
    X_test1=X_test1.astype(np.float32)

    #adversarial attack generation
    bounds = (-1, 100)
    fmodel = fb.PyTorchModel(model, bounds=bounds)
    fmodel = fmodel.transform_bounds((-1, 100))
    
    
    
        #DFT image generation
    if opt.type=='test' or opt.type=='all':
        for k in range(9):
            X_test=torch.from_numpy(X_test1[0+32*k:32+32*k]).float().to(device)
            X_test=F.interpolate(X_test, size=(224, 224), mode='bicubic', align_corners=False)
            y_test=[]
            for j in range(32):
                y_test.append(torch.argmax(model(X_test)[j]))
            y_test=torch.tensor(y_test).to(device)
            # y_test=np.argmax(y_test1, axis=1)
            # y_test=torch.from_numpy(y_test[0+32*k:32+32*k]).to(device)
            attack = fb.attacks.FGSM()
            epsilon=0.03
            attackname="FGSM"
            filepath=opt.output+'/temp'
            filepath_test = opt.output + '/test'
            filepath2=opt.output+'/test/'+opt.label

            if not os.path.exists(filepath):
                os.mkdir(filepath)
            if not os.path.exists(filepath_test):
                os.mkdir(filepath_test)
            if not os.path.exists(filepath2):
                os.mkdir(filepath2)    
            raw, clipped, is_adv = attack(fmodel,X_test,y_test, epsilons=epsilon)
            for i in range(32):
                plt.figure(num=None, figsize=(4,3), dpi=150)
                plt.figure(figsize = (2,2))
                plt.imshow((clipped[i]-X_test[i]).cpu().permute(1,2,0));
                plt.axis('off')
                plt.savefig(filepath+'/per'+str(i+32*k)+'.jpg', dpi=150,bbox_inches='tight', pad_inches=0)
            for i in range(32):
                img_c1=cv2.imread(os.path.join(filepath,'per'+str(i+32*k)+'.jpg'), 0)
                img_c2 = np.fft.fft2(img_c1)
                img_c3 = np.fft.fftshift(img_c2)
                cv2.imwrite(os.path.join(filepath2,opt.architecture+'test'+str(i+32*k)+'.jpg'),20*np.log(1+np.abs(img_c3)))

    if opt.type=='val' or opt.type=='all':
        for k in range(9,18):
            X_test=torch.from_numpy(X_test1[0+32*k:32+32*k]).float().to(device)
            X_test=F.interpolate(X_test, size=(224, 224), mode='bicubic', align_corners=False)
            y_test=[]
            for j in range(32):
                y_test.append(torch.argmax(model(X_test)[j]))
            y_test=torch.tensor(y_test).to(device)
            # y_test=np.argmax(y_test1, axis=1)
            # y_test=torch.from_numpy(y_test[0+32*k:32+32*k]).to(device)
            attack = fb.attacks.FGSM()
            epsilon=0.03
            attackname="FGSM"
            filepath=opt.output+'/temp'
            filepath_val=opt.output+'/val'
            filepath2=opt.output+'/val/'+opt.label

            if not os.path.exists(filepath):
                os.mkdir(filepath)
            if not os.path.exists(filepath_val):
                os.mkdir(filepath_val)
            if not os.path.exists(filepath2):
                os.mkdir(filepath2)
            raw, clipped, is_adv = attack(fmodel,X_test,y_test, epsilons=epsilon)
            for i in range(32):
                plt.figure(num=None, figsize=(4,3), dpi=150)
                plt.figure(figsize = (2,2))
                plt.imshow((clipped[i]-X_test[i]).cpu().permute(1,2,0));
                plt.axis('off')
                plt.savefig(filepath+'/per'+str(i+32*k)+'.jpg', dpi=150,bbox_inches='tight', pad_inches=0)
            for i in range(32):
                img_c1=cv2.imread(os.path.join(filepath,'per'+str(i+32*k)+'.jpg'), 0)
                img_c2 = np.fft.fft2(img_c1)
                img_c3 = np.fft.fftshift(img_c2)
                cv2.imwrite(os.path.join(filepath2,opt.architecture+'val'+str(i+32*k)+'.jpg'),20*np.log(1+np.abs(img_c3)))
    if opt.type=='train' or opt.type=='all':
        for k in range(18,68):
            X_test=torch.from_numpy(X_test1[0+32*k:32+32*k]).float().to(device)
            X_test=F.interpolate(X_test, size=(224, 224), mode='bicubic', align_corners=False)
            y_test=[]
            for j in range(32):
                y_test.append(torch.argmax(model(X_test)[j]))
            y_test=torch.tensor(y_test).to(device)
            # y_test=np.argmax(y_test1, axis=1)
            # y_test=torch.from_numpy(y_test[0+32*k:32+32*k]).to(device)
            attack = fb.attacks.FGSM()
            epsilon=0.03
            attackname="FGSM"
            filepath=opt.output+'/temp'
            filepath_train=opt.output+'/train'
            filepath2=opt.output+'/train/'+opt.label
            if not os.path.exists(filepath):
                os.mkdir(filepath)
            if not os.path.exists(filepath_train):
                os.mkdir(filepath_train)
            if not os.path.exists(filepath2):
                os.mkdir(filepath2)
            raw, clipped, is_adv = attack(fmodel,X_test,y_test, epsilons=epsilon)
            for i in range(32):
                plt.figure(num=None, figsize=(4,3), dpi=150)
                plt.figure(figsize = (2,2))
                plt.imshow((clipped[i]-X_test[i]).cpu().permute(1,2,0));
                plt.axis('off')
                plt.savefig(filepath+'/per'+str(i+32*k)+'.jpg', dpi=150,bbox_inches='tight', pad_inches=0)
            for i in range(32):
                img_c1=cv2.imread(os.path.join(filepath,'per'+str(i+32*k)+'.jpg'), 0)
                img_c2 = np.fft.fft2(img_c1)
                img_c3 = np.fft.fftshift(img_c2)
                cv2.imwrite(os.path.join(filepath2,opt.architecture+'train'+str(i+32*k)+'.jpg'),20*np.log(1+np.abs(img_c3)))   
