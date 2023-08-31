# ACSAC23 Artifact for DeepTaster Submission

## Title
DeepTaster: Adversarial Perturbation-Based Fingerprinting to Identify Proprietary Dataset Use in Deep Neural Networks

## Overview
This research artifact aims to provide the source code of DEEPTASTER, a DNN IP tracking tool that can identify unauthorized proprietary dataset use in deep neural networks. DEEPTASTER works by generating adversarial DFT images from a suspect model and then using a detection classifier to identify the dataset on which the suspect model was trained.

The source code of DEEPTASTER consists of three parts: 1) DFT image generation: This step generates adversarial DFT images from a suspect model, 2) Detection classifier training: This step trains a detection classifier to identify the dataset a suspect model was trained on, and 3) Evaluation of suspect models: This step evaluates the performance of DEEPTASTER by testing it on a variety of suspect models.

## Build Environment
We tested with the following versions of software:
1. Ubuntu 16.04
2. Python 3.7.10

## Prerequisite
To run DEEPTASTER, you will need the following:
1. Jupyter Notebook
2. Python 3.7
3. Other software listed in the requirements.txt file (include foolbox [foolbox](https://github.com/bethgelab/foolbox) )
4. A CUDA-enabled GPU in Linux OS


## How To Run 

### Generate Classifier

#### Step 0: Target model Generation
Training victim/suspect models need GPU and lots of time. You can freely use pre-trained models in [Google Drive](https://drive.google.com/drive/folders/1Onxx5L77a16Vr3p10mvhWZ14VigqlkUm) by **simply running *download_models.ipynb***.

Otherwise, you can download models.zip from the [Google Drive](https://drive.google.com/drive/folders/1Onxx5L77a16Vr3p10mvhWZ14VigqlkUm), unzip that file, and put them into the *models* folder.

#### Step 1: DFT images Generation

Run *DFTimageGeneration.ipynb*

#### Step 2: Detection classifier generation

Run *DetectionClassifierGeneration.ipynb*

#### Step 3: Evaluation Classifier

Run *Evaluation.ipynb*



### Attack Model Generation

#### Fine-tuning attack

Run *Fine-tuning.ipynb*

Fine-tune victim Resnet18 model and store attacked models at *models/attack_model*

## Code File Organization

| File                         	| Functionality                                                       	|
| ---------------- | ------------------------------------------------------------ |
| requirements.txt                      | Python software requirements. 	|
| DFTimageGeneration.ipynb               | Generate adversarial DFT images of models in *models* folder 	|
| DetectionClassifierGeneration.ipynb  	| Generate detection_classifier using a set of adversarial DFT images. 	|
| Evaluation.ipynb                	     | Evaluate suspect models using DeepTaster. 	|
| ./utils/deepsvdd.py                	          | Functions for DeepSVDD [1]. 	|
| ./utils/train.py                	          | Train models. 	|




[1] Ruff et al., "Deep One-Class Classification," Deep OCC ICML 2018

