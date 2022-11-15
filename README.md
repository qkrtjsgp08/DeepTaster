## Prerequisite
We use foolbox, adversarial attack tool

```python
$ pip install foolbox
$ wget http://cs231n.stanford.edu/tiny-imagenet-200.zip
$ unzip -qq 'tiny-imagenet-200.zip'
```
## Files
Files
attack: attack

Reference:

[1] Ruff et al. "Deep One-Class Classification", Deep OCC ICML 2018

## To run 

#### DFT images Generation
```python
$ python dftgeneration.py --model model_path --type all --output save_image_directory
```

generate dft images


#### Detection classifier generation
```python
$ python detection_classifier+generation.py --train train_data_path --val validataion_data_path --saveautoencoder save_autoencoder_directory --output save_classifier_directory
```



#### Attack

## Example
You can generate TRACK-IP for imagenet dataset protection using open source models by following below commands.

DFT image generation for victim models
Note that output_directory must have subdirectory temp, test, train, val
```python
$ pip install foolbox
$ python dftgeneration.py --model Imagenet --architecture Resnet101 --type all --output output_directory
$ python dftgeneration.py --model Imagenet --architecture Vgg16 --type all --output output_directory
$ python dftgeneration.py --model Imagenet --architecture Densenet161 --type all --output output_directory
```
Detection classifier generation
