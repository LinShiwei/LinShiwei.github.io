---
published: true
layout: post
title: iOS：KVO 指南
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

在 iOS 开发中，常常需要在不同的对象、不同的视图（View）或不同的视图控制器（ViewController）之间通信，传递数据。主要的实现方法有：

- 直接通过 superView 或 subView 传递数据，或者在类中添加其他对象的引用。方法直接但效率低、容易使代码混乱，难以处理复杂的关系。
- 通过自带的或自定义的 delegate 协议通信。效率较高，能完成复杂的通信及执行复杂的操作，代码结构较好，但是代码量比较大。
- 使用 KVO（Key-value observing）。能够穿越复杂的关系网，直接观察其他对象的属性，获取信息，根据所观察对象的变化进行响应，代码量少。

这些方法各有优劣，在不同的情况下选用合适的方法是最好的。因此掌握这些方法，才能更好地应对各种开发难题。KVO 是本文关注的重点。

# KVO 简介

在 Apple 的应用开发里 KVO 提供了一个途径，使对象（观察者）能够观察其他对象（被观察者）的属性，当被观察者的属性发生变化时，观察者就会被告知该变化。这其实就对应**设计模式**中的观察者模式。

> 观察者：Observer，the observing object；被观察者：the observed object
 
## 前提条件

在实现 KVO 之前，需要确保被观察的对象是支持 KVO 的。通常继承自 NSObject 的对象都会自动支持 KVO。对于非继承自 NSObject 的类，也可以[手动实现 KVO 支持](https://developer.apple.com/library/content/documentation/Cocoa/Conceptual/KeyValueObserving/Articles/KVOCompliance.html#//apple_ref/doc/uid/20002178-BAJEAIEE)。

## 适用场景

KVO 能很方便地实现模型（Model）和控制器（Controller）之间的通信。主要的应用场景有：

[图]

KVO 能够实现一对多、多对多、多对一的观察。也就是说，KVO 没有限制观察者和被观察者的数量。当同时观察多个对象时，不但对象本身发生改变时会告知观察者，而且被观察对象发生替换、删除或插入等操作时也会告知观察者。

# 实现 KVO：注册观察者和观察者方法

## 基本流程

1. 添加观察者：`addObserver:forKeyPath:options:context: `；
2. 实现观察响应方法：`observeValueForKeyPath:ofObject:change:context: `；
3. 在观察者 deallocted 之前移除观察者： `removeObserver:forKeyPath:` ；

### 添加观察者

> observedObject.addObserver:forKeyPath:options:context:

注意：

- 调用该函数的 observedObject 是被观察者，参数 addObserver 后面的是观察者；
- forKeyPath 参数是 String 类型的，代表 observedObject 的属性，私有属性也可以观察，但是在 Swift 中需要把被观察对象的属性用 `dynamic` 标记，如：

```swift
class ObservedObjectClass: NSObject {
//在 Swift 中要用 dynamic 标记被观察的属性
    dynamic private var observedProperty = ""
    ...
}
```

- options：可以选择获取的数据包含哪些内容，获取的数据是以字典的形式传递的。
    - NSKeyValueObservingOptionOld: 获取变化前的数据
    - NSKeyValueObservingOptionNew: 获取变化后的数据
    - NSKeyValueObservingOptionInitial: 获取设置观察者时被观察者的初始数据，即在 addObserver 函数调用完成前，被观察者的数据。
    - NSKeyValueObservingOptionPrior: 在变化前发送消息

- context：可选的参数，会随着观察消息传递，用于区分接收该消息的观察者。一般情况下，只需通过 keyPath 就可以判断接收消息的观察者。但是当父类子类都观察了同一个 keyPath 时，仅靠 keyPath 就无法判断消息该传给子类，还是传给父类。
- addObserver 并不会维持对观察者、被观察者和 Context 的强引用。如果需要的话，要自行维持对它们的强引用。

### 观察响应方法：

> 所有的观察者都必须实现观察响应方法：
> observeValueForKeyPath:ofObject:change:context:

- change 是一个字典，包含了一系列键－值。
    - NSKeyValueChangeKindKey: 变化的类型
    - NSKeyValueChangeOldKey: 变化前的值
    - NSKeyValueChangeNewKey: 变化后的值
    - NSKeyValueChangeIndexesKey: 在所有变化中的坐标

- NSKeyValueChangeKindKey 又包含了：
    - NSKeyValueChangeSetting
    - NSKeyValueChangeInsertion
    - NSKeyValueChangeRemoval
    - NSKeyValueChangeReplacement
   
- 如果接收到的观察者消息于当前的 Context 不符，就需要把消息传给 父类，直到寻找到对应的 Context。
- 如果一个消息传到了 NSObject 仍然没有找到它的观察者，那么就会抛出异常：NSInternalInconsistencyException。

### 移除观察者

当一个对象不再需要观察另一个对象时，就需要移除观察。

> observedObject.removeObserver:forKeyPath:context: 

这个方法和添加观察者的方法是对应的。

移除观察者需要注意以下几点：

- 一个对象如果没有注册成为观察者，那么当调用 removeObserver 移除它时，就会抛出异常。所以想要安全地移除观察者，可以使用 do、try、catch 来调用 removeObserver。
- 观察者不会在 dealloc 的时候自动移除。因此最晚必须在观察者 dealloc 时移除它。
- 系统没有自带的方法用于判断一个对象是否注册为观察者，因此尽量在初始化的时候注册观察者，在 dealloc 时移除。

# 总结

KVO 能够在复杂的关系网中直接观察某个对象，合理的使用 KVO 能够简化代码。但是 KVO 也有很多坑，稍有不慎就会抛出异常或者无法建立观察。在实践中，还是应该选择合适的方法来完成对象间的通信，熟练应对各种情况。 
  
**有任何疑问的话，欢迎在下方评论区讨论。**

