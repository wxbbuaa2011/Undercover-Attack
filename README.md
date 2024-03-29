# Detecting Adversarial Examples via Undercover Attack

## Description
This repository includes the source code of the paper "Detecting Adversarial Examples via Undercover Attack". Please cite our paper when you use this program! 😍

## Model overview
![](https://i.loli.net/2019/11/22/STtspcuDf6PVUqb.png)

## Quick glance
A quick glance of the use case of undercover attack on images and texts:

```
example_images.ipynb
example_texts.ipynb
```

### Image case
![](https://i.loli.net/2019/11/22/R4jFAODNUegpLvs.png)

benign example criterion:  1.1444092e-05;
 
adversarial example criterion:  2.758562

split criterion in our experiment is 1.2505696; 

1.1444092e-05 < 1.2505696 --> example1 is judged as a normal example; 

2.757648 > 1.2505696 --> example2 is judged as a adversarial example.

### Text case 1
original sentiment: 1, changed words num: 2

original sentence:  touching well directed autobiography of a talented young director producer . a love story with rabin s assassination in the background . worth seeing !

adv sentence: touching well directed autobiography of a talented young director producer . a love story with rabin s assassination in the not . worth from !

original criterion loss: -0.00

adversarial criterion loss: 0.62

### Text case 2
original sentiment: 0, changed words num: 2

original sentence:  comment this movie is impossible . is terrible very improbable bad interpretation e direction . not look !

adv sentence: comment this movie is impossible . is terrible very improbable bad but e direction . it look !

original criterion loss: 0.00

adversarial criterion loss: 0.43

## Adversary
Five attack methods are implemented in this package.

1. FGSM: FGSM, BIM
2. JSMA: JSMA, JSMA*(texts)
3. CW: CW
4. Boundary Attack (Implemented by Foolbox)

## Models
### IMDB

1. The definitions of 5-layer convolution network
2. PreActResNet 
3. RNNs

### Quora
ESIM
   
## Train
### Train models on normal examples

```
python cifar10_pre_train.py
python mnist_pre_train.py
python movie_pre_train.py
python quora_pre_train.py
```

### Undercover training, undercover attack and performance analysis

```
python cifar10_adv.py
python mnist_adv.py
python movie_adv.py
```

## Report issues
Please let us know, if you encounter any problems.

The contact email is qifeizhou@pku.edu.cn


