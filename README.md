# Detecting Adversarial Examples via Undercover Attack

## Description
This repository includes the source code of the paper "Detecting Adversarial Examples via Undercover Attack". Please cite our paper when you use this program! 😍

## Model overview
![](https://i.loli.net/2019/11/21/gVDjRvxpUkZGIbq.png)

## Requirements
python3

```
pip install -r requirements.txt
```

## Datasets

* Quora Question Pairs (QQP)
* SNLI
* MultiNLI

## Preprocess the data
After the datasets have been downloaded, you can preprocess the data.

### Preprocess the data for BERT
```
cd scripts/preprocessing
python process_quora_bert.py
python preprocess_cqadup_bert.py
python preprocess_snli_bert.py
python process_mnli_bert.py
```

### Preprocess the data for ELMo
```
cd scripts/preprocessing
python process_quora.py
python preprocess_snli.py
python preprocess_mnli.py
```

## Train
### BERT as service
If you want to train models with BERT word embedding, please use the [bert-as-service](https://github.com/hanxiao/bert-as-service), and then run the following scripts.

### Train all models
```
sh -x run.sh
```

### Train with BERT
```
python bert_quora.py >> log/quora/quora_bert.log
python bert_cqadup.py >> log/cqadup/cqadup_bert.log
python bert_snli.py >> log/snli/snli_bert.log
python bert_mnli.py >> log/mnli/mnli_bert.log
```

### Train with ELMo
```
python train_quora_elmo.py >> log/quora/quora_elmo.log
python train_snli_elmo.py >> log/snli/snli_elmo.log
python train_mnli_elmo.py >> log/mnli/mnli_elmo.log
```

## Test
After the models have been trained, you can test the models.

### Test the models with BERT

```
python test_bert_quora.py
python test_bert_cqadup.py
python test_bert_snli.py
python test_bert_mnli.py
```

### Test the models with ELMo

```
python test_elmo_quora.py
python test_elmo_snli.py
python test_elmo_mnli.py
```

## Report issues
Please let us know, if you encounter any problems.

The contact email is qifeizhou@pku.edu.cn


--> example_xx.ipynb: a quick glance of the use case of undercover attack on images and texts

--> xxx_pre_train: train models on normal examples

--> xxx_adv: undercover training, undercover attack and performance analysis

--> adversary: five attack methods are implemented in this package
    fgsm: FGSM, BIM_A, BIM_B
    jsma: JSMA, JSMA*(texts)
    cw: CW

--> data: 20 ImageNet classes are exhibited in imagenet_classes.txt

--> models: the definitions of 5-layer convolution network, PreActResNet and RNNs for IMDB


