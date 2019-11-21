# Detecting Adversarial Examples via Undercover Attack

## Description
This repository includes the source code of the paper "Detecting Adversarial Examples via Undercover Attack". Please cite our paper when you use this program! 😍

## Report issues
Please let us know, if you encounter any problems.

The contact email is qifeizhou@pku.edu.cn


--> example_images.ipynb and example_texts.ipynb: a quick glance of the use case of undercover attack on images and texts

--> xxx_pre_train: train models on normal examples

--> xxx_adv: undercover training, undercover attack and performance analysis

--> adversary: five attack methods are implemented in this package
    fgsm: FGSM, BIM
    jsma: JSMA, JSMA*(texts)
    cw: CW
    boundary attack is implemented by Foolbox

--> models: the definitions of 5-layer convolution network, PreActResNet and RNNs for IMDB


