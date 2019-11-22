# Detecting Adversarial Examples via Undercover Attack

## Description
This repository includes the source code of the paper "Detecting Adversarial Examples via Undercover Attack". Please cite our paper when you use this program! 😍

## Model overview
![](https://i.loli.net/2019/11/22/STtspcuDf6PVUqb.png)

a quick glance of the use case of undercover attack on images and texts:
example_images.ipynb and example_texts.ipynb

![](https://i.loli.net/2019/11/22/R4jFAODNUegpLvs.png)

benign example criterion:  1.1444092e-05;
 
adversarial example criterion:  2.758562

split criterion in our experiment is 1.2505696; 1.1444092e-05 < 1.2505696 --> example1 is judged as a normal example; 2.757648 > 1.2505696 --> example2 is judged as a adversarial example;


--------------------

original sentiment: 1, changed words num: 2

original sentence:  touching well directed autobiography of a talented young director producer . a love story with rabin s assassination in the background . worth seeing !

adv sentence:       touching well directed autobiography of a talented young director producer . a love story with rabin s assassination in the not . worth from !

original criterion loss: -0.00 -- adversarial criterion loss: 0.62

--------------------

original sentiment: 0, changed words num: 2

original sentence:  comment this movie is impossible . is terrible very improbable bad interpretation e direction . not look !

adv sentence:       comment this movie is impossible . is terrible very improbable bad but e direction . it look !

original criterion loss: 0.00 -- adversarial criterion loss: 0.43



--> xxx_pre_train: train models on normal examples

--> xxx_adv: undercover training, undercover attack and performance analysis

--> adversary: five attack methods are implemented in this package
    fgsm: FGSM, BIM
    jsma: JSMA, JSMA*(texts)
    cw: CW
    boundary attack is implemented by Foolbox

--> models: the definitions of 5-layer convolution network, PreActResNet and RNNs for IMDB, ESIM for Quora

## Report issues
Please let us know, if you encounter any problems.

The contact email is qifeizhou@pku.edu.cn


