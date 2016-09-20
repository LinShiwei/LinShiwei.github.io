---
published: true
layout: post
title: 让现有的Swift项目支持Carthage 
category: Tutorial
tags: 
  - github
  - Carthage
  - swift
time: 2016.07.30 20:00:00
excerpt: Carthage作为Cocoa的依赖管理器，相比于CocoaPods，对项目的改变更少。我们可以很方便地管理第三方依赖，但是该如何让自己写的框架支持Carthage，供其他人使用呢？本文将主要介绍为已有的项目添加Carthage支持。
---
<!-- lsw toc mark1. Do not remove this comment so that lsw_toc can update TOC correctly. -->

## Table of Contents
- [Introduction](#introduction)
- [前提条件](#前提条件)
- [第一步：为项目新建Target](#第一步：为项目新建target)
- [第二步：选择framework包含的文件](#第二步：选择framework包含的文件)
- [第三步：分享target](#第三步：分享target)
- [第四步：生成framework](#第四步：生成framework)
- [第五步：测试framework](#第五步：测试framework)
- [最后一步：生成release](#最后一步：生成release)

<!-- lsw toc mark2. Do not remove this comment so that lsw_toc can update TOC correctly. -->

## Introduction

Carthage作为Cocoa的依赖管理器，相比于CocoaPods，对项目的改变更少。Carthage的安装可以参考[这里](https://github.com/Carthage/Carthage)。
我们可以很方便地管理第三方依赖，但是该如何让自己写的框架支持Carthage，供其他人使用呢？**本文将主要介绍为已有的项目添加Carthage支持。**

## 前提条件
如果是第一次写框架(framework)，要记得将需要暴露给用户的接口(interface)用`public`修饰，因为各个类和变量的默认修饰符是`internal`，如果直接生成`.framework`的话，是没办法使用这些类和变量的。

## 第一步：为项目新建Target
原有的项目已经有一个target了，要生成framework的话，就需要在新建一个framework的target。如下图：

![image](/images/carthageSupport13.png)

在`Framework & Library`里选择`Cocoa Touch Framework`：

![image](/images/carthageSupport12.png)

设置好framework的名称：

![image](/images/carthageSupport11.png)

## 第二步：选择framework包含的文件
在项目的target中选中刚刚新建的framework target，在`Build Phases`里，确保添加了需要编译到framework里面的文件：

![image](/images/carthageSupport10.png)

## 第三步：分享target
在左上角停止按钮旁，点击target，选择`Manage Schemes`，勾选要分享的Scheme：

![image](/images/carthageSupport9.png)

![image](/images/carthageSupport8.png)

## 第四步：生成framework
在项目的根目录里打开终端，运行

```ruby
$ carthage build --no-skip-current
```
运行后，会在下面的目录里生成framework：

```
Carthage/Build/iOS/
```

## 第五步：测试framework
这一步只是为了检验framework是否可用，虽然不做也是可以的，但是以防万一还是测试一下吧。
新建一个test项目，把刚刚生成的`.framework`拖到test项目左边的navigation栏里：

![image](/images/carthageSupport7.png)

![image](/images/carthageSupport6.png)

这时候如果运行出错的话，别紧张：

![image](/images/carthageSupport5.png)

需要在`Build Phases`里新建一个`New copy file phase`并添加framework：

![image](/images/carthageSupport4.png)

之后就可以测试framework了，可以写一些代码，看看framework里的东西能不能用。

## 最后一步：生成release
到Github网页上，在项目的release页面，新建一个release，并给这个release一个版本号，如v1.0：

![image](/images/carthageSupport3.png)

![image](/images/carthageSupport2.png)

填写版本号，Release title，Describe this release，点击Publish release就行：

![image](/images/carthageSupport1.png)

这样就可以通过Carghage来导入framework了。例如，在项目根目录新建一个`cartfile`文件，在里面写入

```ruby
github "LinShiwei/ImageSlider"
```
再在项目根目录的终端里运行：

```ruby
$ carthage update
```
Carghage就会自动下载framework到项目目录下。具体的添加过程可以看这里：[用Carthage为项目添加第三方依赖]()。

**感谢您的阅读，有任何疑问可以在下方的评论区问我，欢迎访问我的[github](https://github.com/LinShiwei)。**


