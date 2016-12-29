---
published: true
layout: post
title: iOS：KVO 心得
category: Tutorial
tags: 
  - iOS
  - swift
  - KVO
  - objective-c
time: 2016.12.29 09:22:00
excerpt: 在 Apple 的应用开发里 KVO（Key-value observing）提供了一个途径，使对象（观察者）能够观察其他对象（被观察者）的属性，当被观察者的属性发生变化时，观察者就会被告知该变化。KVO 能够很方便地完成不同对象之间的通信，尤其是当对象之间的关系很复杂的时候。
---

# 前言

在 Apple 的应用开发里 KVO（Key-value observing）提供了一个途径，使对象（观察者）能够观察其他对象（被观察者）的属性，当被观察者的属性发生变化时，观察者就会被告知该变化。

> 观察者：Observer，the observing object；被观察者：the observed object




**有任何疑问的话，欢迎在下方评论区讨论。**

