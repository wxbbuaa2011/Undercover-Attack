import torch.nn as nn
import torch.optim as optim
import torch.backends.cudnn as cudnn
from torch.optim import lr_scheduler
import torchvision
import torchvision.transforms as transforms
import os
from models.conv import MnistModel
from settings import *
import torch.nn.functional as F
import numpy as np
from adversary.fgsm import Attack, ShannonEntropy
from torch.autograd import Variable
from torch.nn.modules.distance import PairwiseDistance
from util.roc_plot import roc_auc, creterion_func
import adversary.cw as cw
from adversary.jsma import SaliencyMapMethod
import torch
import random
import sys

# Training
def train(epoch):
    print('\nEpoch: %d' % epoch)
    scheduler.step()
    net.train()
    correct = 0
    total = 0
    for batch_idx, (inputs, targets) in enumerate(trainloader):
        inputs, targets = inputs.to(device), targets.to(device)
        optimizer.zero_grad()
        outputs = net(inputs)
        _, predicted = outputs.max(1)
        total += targets.size(0)
        correct += predicted.eq(targets).sum().item()

        x_adv = FGSM(inputs, targets, eps=EPS_MINIST)
        adv_outputs = net(x_adv)

        loss1 = criterion(outputs, targets)
        loss2 = criterion(adv_outputs, targets)
        loss = loss1 + loss2*0.8
        loss.backward()
        optimizer.step()

    acc = correct / total
    print('train acc: %.2f%%' % (100.*acc))


def test(epoch, methods='fgsm', update=False, random_method=False, confidence=0.5):
    global best_acc
    net.eval()
    correct = 0
    total = 0
    total_right = 0
    total_attack_sucess = 0
    benign_fgsm_correct = 0
    adv_fgsm_correct = 0
    attack_correct = 0
    benign_fgsm_loss = None
    adv_fgsm_loss = None
    l2sum = 0

    for batch_idx, (inputs, targets) in enumerate(testloader):
        inputs, targets = inputs.to(device), targets.to(device)
        outputs = net(inputs)
        _, predicted = outputs.max(1)
        correct += predicted.eq(targets).sum().item()
        selected = (predicted == targets).cpu().numpy().astype(bool)
        total += inputs.size(0)
        temp_batch = selected.sum()

        inputs = torch.from_numpy(inputs.cpu().numpy()[selected]).to(device)
        targets = torch.from_numpy(targets.cpu().numpy()[selected]).to(device)
        predicted = torch.from_numpy(predicted.cpu().numpy()[selected]).to(device)
        outputs = torch.from_numpy(outputs.detach().cpu().numpy()[selected]).to(device)
        total_right += inputs.size(0)

        # benign fgsm
        benign_fgsm = FGSM(inputs, predicted, eps=EPS_MINIST)
        benign_fgsm_outputs = net(benign_fgsm)
        _, benign_fgsm_predicted = benign_fgsm_outputs.max(1)
        temp1 = criterion_none(benign_fgsm_outputs, predicted).detach().cpu().numpy()
        # temp1 = criterion_none(benign_fgsm_outputs, predicted).detach().cpu().numpy() - \
        #         criterion_none(outputs, predicted).detach().cpu().numpy()
        # temp1 = ShannonEntropy(benign_fgsm_outputs, F.softmax(outputs, dim=-1)).detach().cpu().numpy()

        if random_method:
            tag = random.randint(0, 4)
            if tag == 0:
                methods = 'fgsm'
            elif tag == 1:
                methods = 'bim_a'
            elif tag == 2:
                methods = 'bim_b'
            elif methods == 3:
                methods = 'jsma'
            else:
                methods = 'cw'

        # attack begin
        if methods == 'fgsm':
            x_adv = FGSM(inputs, predicted, eps=EPS_MINIST*2, alpha=1 / 255, iteration=1)
        elif methods == 'bim_a':
            x_adv = FGSM(inputs, predicted, eps=EPS_MINIST*2, alpha=1 / 255, iteration=50, bim_a=True, confidence=confidence)
        elif methods == 'bim_b':
            x_adv = FGSM(inputs, predicted, eps=EPS_MINIST*2, alpha=1 / 255, iteration=50)
        elif methods == 'jsma':
            x_adv = jsma_attack.generate(inputs, y=predicted, confidence=confidence)
        else:
            x_adv = cw_attack(net, inputs, predicted, to_numpy=False)

        l2sum += l2dist.forward(x_adv.reshape(temp_batch, -1), inputs.reshape(temp_batch, -1)).sum().detach().cpu().numpy()
        adv_outputs = net(x_adv)
        _, adv_predicted = adv_outputs.max(1)
        attack_correct += adv_predicted.eq(predicted).sum().item()
        selected = (adv_predicted != targets).cpu().numpy().astype(bool)

        # adv_fgsm
        adv_fgsm = FGSM(x_adv, adv_predicted, eps=EPS_MINIST)
        adv_fgsm_outputs = net(adv_fgsm)
        _, adv_fgsm_predicted = adv_fgsm_outputs.max(1)
        temp2 = criterion_none(adv_fgsm_outputs, adv_predicted).detach().cpu().numpy()
        # temp2 = criterion_none(adv_fgsm_outputs, adv_predicted).detach().cpu().numpy() - \
        #         criterion_none(adv_outputs, adv_predicted).detach().cpu().numpy()
        # temp2 = ShannonEntropy(adv_fgsm_outputs, F.softmax(adv_outputs, dim=-1)).detach().cpu().numpy()


        # select the examples which is attacked successfully
        temp1 = temp1[selected].reshape(1, -1)
        temp2 = temp2[selected].reshape(1, -1)
        if batch_idx != 0:
            benign_fgsm_loss = np.column_stack((benign_fgsm_loss, temp1))
            adv_fgsm_loss = np.column_stack((adv_fgsm_loss, temp2))
        else:
            benign_fgsm_loss = temp1
            adv_fgsm_loss = temp2
        # if batch_idx == 20:
        #     break

        total_attack_sucess += len(temp1[0])
        benign_fgsm_correct += np.equal(benign_fgsm_predicted.cpu().numpy()[selected],(predicted.cpu().numpy()[selected])).sum()
        adv_fgsm_correct += np.equal(adv_fgsm_predicted.cpu().numpy()[selected],(adv_predicted.cpu().numpy()[selected])).sum()

    acc = correct/total
    attack_acc = attack_correct / total_right
    benign_fgsm_acc = benign_fgsm_correct/ total_attack_sucess
    adv_fgsm_acc = adv_fgsm_correct / total_attack_sucess
    print('-'*20,total,total_right)
    print('valid acc: %.2f%%' % (100.*acc))
    print('attact acc: %.2f%% L2 perturbation: %.2f' % (100.*attack_acc, l2sum/total_right))
    print('fgsm attack benign: %.2f%% adversary: %.2f%%' % (100.*benign_fgsm_acc, 100.*adv_fgsm_acc))
    benign_fgsm_loss = benign_fgsm_loss.reshape(-1)
    adv_fgsm_loss = adv_fgsm_loss.reshape(-1)

    losses = np.concatenate((benign_fgsm_loss, adv_fgsm_loss), axis=0)
    labels = np.concatenate((np.zeros_like(benign_fgsm_loss), np.ones_like(adv_fgsm_loss)), axis=0)
    auc_score = roc_auc(labels, losses)
    print(np.mean(benign_fgsm_loss), np.mean(adv_fgsm_loss))
    print('split criterion', np.median(losses))
    print('[ROC_AUC] score: %.2f%%' % (100.*auc_score))
    aucs.append(auc_score)
    sys.stdout.flush()

    # plot losses
    creterion_func(benign_fgsm_loss, adv_fgsm_loss)


    # Save checkpoint.
    if auc_score >= best_acc and update:
        print('update resnet ckpt!')
        state = {
            'net': net.state_dict(),
            'auc_score': auc_score,
            'epoch': epoch,
        }
        if not os.path.isdir('checkpoint'):
            os.mkdir('checkpoint')
        torch.save(state, MNIST_CKPT)
        best_acc = auc_score

def FGSM(x, y_true, eps=1/255, alpha=1/255, iteration=1, bim_a=False, confidence=0.5):
    net.eval()
    x = Variable(x.to(device), requires_grad=True)
    y_true = Variable(y_true.to(device), requires_grad=False)

    if iteration == 1:
        x_adv = bim_attack.fgsm(x, y_true, False, eps)
    else:
        if bim_a:
            x_adv = bim_attack.i_fgsm_a(x, y_true, False, eps, alpha, iteration, confidence=confidence)
        else:
            x_adv = bim_attack.i_fgsm(x, y_true, False, eps, alpha, iteration)

    return x_adv


if __name__ == '__main__':
    best_acc = 0  # best test accuracy
    start_epoch = 0  # start from epoch 0 or last checkpoint epoch

    # Data
    print('==> Preparing data..')
    transform_train = transforms.Compose([
        transforms.RandomHorizontalFlip(),
        transforms.ToTensor(),
    ])

    transform_test = transforms.Compose([
        transforms.ToTensor(),
    ])

    trainset = torchvision.datasets.MNIST(root='./data', train=True, download=True, transform=transform_train)
    trainloader = torch.utils.data.DataLoader(trainset, batch_size=BATCH_SIZE_MNIST, shuffle=True,
                                              num_workers=NUM_WORKERS)

    testset = torchvision.datasets.MNIST(root='./data', train=False, download=True, transform=transform_test)
    testloader = torch.utils.data.DataLoader(testset, batch_size=BATCH_SIZE_MNIST_TEST, shuffle=False,
                                             num_workers=NUM_WORKERS)

    # Model
    print('==> Building model..')
    net = MnistModel()
    net = net.to(device)

    if device == 'cuda':
        net = torch.nn.DataParallel(net)
        cudnn.benchmark = True

    # Load checkpoint.
    print('==> Resuming from checkpoint..')
    assert os.path.isdir('checkpoint'), 'Error: no checkpoint directory found!'
    checkpoint = torch.load(MNIST_CKPT)
    net.load_state_dict(checkpoint['net'])
    start_epoch = checkpoint['epoch']
    print(start_epoch)
    try:
        best_acc = checkpoint['auc_score']
        if best_acc > 90:
            best_acc = best_acc / 100
        print('best_auc: %.2f%%' % (100. * best_acc))
    except:
        pass

    l2dist = PairwiseDistance(2)
    criterion_none = nn.CrossEntropyLoss(reduction='none')
    criterion = nn.CrossEntropyLoss()
    optimizer = optim.SGD(net.parameters(), lr=LEARNING_RATE, momentum=0.9, weight_decay=5e-4)
    scheduler = lr_scheduler.StepLR(optimizer, step_size=SCHEDULER_STEP_SIZE, gamma=0.1)
    # attacks
    bim_attack = Attack(net, F.cross_entropy)
    cw_attack = cw.L2Adversary(targeted=False,
                               confidence=0.5,
                               search_steps=10,
                               box=(0, 1),
                               optimizer_lr=0.001)
    jsma_params = {'theta': 1, 'gamma': 0.1,
                   'clip_min': 0., 'clip_max': 1.,
                   'nb_classes': 10}
    jsma_attack = SaliencyMapMethod(net, **jsma_params)


    aucs = []
    for epoch in range(start_epoch, start_epoch+NUM_EPOCHS):
        # fgsm, bim_a, bim_b, jsma, cw
        # train(epoch)
        # test(epoch, methods='fgsm', update=True)
        methods = 'fgsm'
        print('MNIST ', methods)
        # confidences = np.arange(50, 100, 4) / 100
        confidences = [0.5]

        print(confidences)
        for i in confidences:
            print('==========',i)
            cw_attack = cw.L2Adversary(targeted=False,
                                       confidence=i,
                                       search_steps=10,
                                       box=(0, 1),
                                       optimizer_lr=0.001)
            test(epoch, methods=methods, update=False, random_method=False, confidence=i)
        print(aucs)
        break