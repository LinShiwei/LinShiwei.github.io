---
published: true
layout: post
title: Train mnist using your own images
category: Tutorial
tags: 
  - tensorflow
time: 2016.07.13 20:00:00
excerpt: In tensorflow.org there are "MNIST for beginners" and "Deep MNIST for experts" for learning. In these tutorials, the training source is from MNIST. It is awesome, containing thousands of images. But there are some situations that we want to use our own images for training...
---
## Introduction

In [tensorflow.org](http://www.tensorflow.org) there are [MNIST For ML Beginners](https://www.tensorflow.org/versions/r0.9/tutorials/mnist/beginners/index.html) and [Deep MNIST for Experts](https://www.tensorflow.org/versions/r0.9/tutorials/mnist/pros/index.html) for learning. 

In these tutorials, the training source is from [MNIST](http://yann.lecun.com/exdb/mnist/). It is awesome, containing thousands of images.

But there are some situations that we want to use our own images for training. I have searched on the Internet and could hardly find the direct way to convert images into MNIST Database format. So I just do it myself and have found another way to create my data files and train it in the tensorflow.

## Method

### Step One

You should first have some images for training. You can use your own images or use [my images](https://github.com/LinShiwei/TensorflowLearning/tree/master/trainYourOwnMnist/numberImage) for a try. 

The images like the following, should have a black background and a white number.

![image](https://raw.githubusercontent.com/LinShiwei/TensorflowLearning/master/trainYourOwnMnist/introductionImage/imageSample.png)

### Step Two

I have writed some Matlab code to convert your images into image data and create label data. These data are in binary format and have `.txt` suffix. Here shows the data format in these data file.

![image](https://raw.githubusercontent.com/LinShiwei/TensorflowLearning/master/trainYourOwnMnist/introductionImage/dataFormat.png)

After generating, these four files should like the following:

```swift
trainImage.txt
trainImageLabel.txt
testImage.txt
testImageLabel.txt
```

And then you should use [gzipCreate.py](https://github.com/LinShiwei/TensorflowLearning/blob/master/trainYourOwnMnist/gzipCreate.py) to convert these files into '.gz' files.

```swift
trainImage.txt.gz
trainImageLabel.txt.gz
testImage.txt.gz
testImageLabel.txt.gz
```

Until now, the training files are ready.(training files can be find in this repository)

### Step Three

I have done some changes to tensorflow's mnist example code. You can use `lswBeginnerMnist.py` for simple mnist training or use `lswDeepMnist.py` for deep mnist training.

## Example results

Result of [lswBeginnerMnist.py](https://github.com/LinShiwei/TensorflowLearning/blob/master/trainYourOwnMnist/lswBeginnerMnist.py) training , 29 images.

![image](https://raw.githubusercontent.com/LinShiwei/TensorflowLearning/master/trainYourOwnMnist/introductionImage/beginnerMnistTrainingResult.png)

Result of [lswDeepMnist.py](https://github.com/LinShiwei/TensorflowLearning/blob/master/trainYourOwnMnist/lswDeepMnist.py) training , 36 images.

![image](https://raw.githubusercontent.com/LinShiwei/TensorflowLearning/master/trainYourOwnMnist/introductionImage/deepMnistTrainingResult.png)


