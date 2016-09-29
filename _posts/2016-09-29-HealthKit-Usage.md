---
published: true
layout: post
title: HealthKit 配置及使用 
category: Tutorial
tags: 
  - swift
  - iOS
  - HealthKit
time: 2016.09.29 15:22:00
excerpt: 随着人们对健康生活的日益关注，运动、健康类的 APP 也越来越多。使用 HealthKit 是这类 APP 获取数据的来源之一。因此，开发者有必要熟悉 HealthKit 。
---

## 前言

HealthKit 储存了 iPhone 和 iWatch 上的健康数据，对于开发者而言，能够很方便地获取相关数据，同时它还具有完善的隐私保护机制，使用户能够对每一项数据进行授权。

[这里](https://github.com/LinShiwei/HealthyDay)是一个使用 HealthKit 的跑步类 APP ，HealthKit 配置及使用过程与下面的描述一致，可供参考。

## 配置 HealthKit

通过一下几个步骤，就能够完成 HealthKit 的配置。

1. 在 Xcode 的项目配置页面，选择项目的 target ，在 Capabilities 页面打开 HealthKit 。
2. 在 target 的 `info.plist` 里添加两个 HealthKit 的 key 值，分别是：`Privacy - Health Share Usage Description` 和 `Privacy - Health Update Usage Description` 。用于在授权界面进行描述，给用户提供信息。
3. 在需要使用 HealthKit 的文件里：

```swift
import HealthKit
```

4. 声明一个且只有一个 HealthStore 实例：

```swift
let healthStore = HKHealthStore()
```

5. 使用 HealthStore 的实例方法，请求用户授权：

```swift
func requestAuthorization(toShare typesToShare: Set<HKSampleType>?, read typesToRead: Set<HKObjectType>?, completion: (Bool, Error?) -> Void)
```

当调用这个方法后，会自动弹出授权界面，等待用户操作。之前在 `info.plist` 里设置的 key 值会显示在这个页面上。

当用户授权后就可以开始获取数据。APP 并不能知道用户已授权或是禁止授权。不管授权结果如何，获取数据的过程都能够进行，只不过当禁止授权时，获取到的数据为空。

## 数据获取

1. 声明 HKSampleQuery 实例
    - 声明一个 HKSampleQuery 实例，需要包含 HKSampleType 、NSPredicate 、limit 、NSSortDescriptor 和 resultsHandler。它们分别对应需要获取的数据类型、过滤条件、数据数量、排序方式以及结果的处理。

```swift
init(sampleType: HKSampleType, predicate: NSPredicate?, limit: Int, sortDescriptors: [NSSortDescriptor]?, resultsHandler: (HKSampleQuery, [HKSample]?, Error?) -> Void)
```

2. 有了 HKSampleQuery 实例后，如：sampleQuery ，使用 healthStore 获取数据：

```swift
healthStore.execute(sampleQuery)
``` 

## 与 Core Motion 比较

HealthKit 和 Core Motion 都可以用来获取运动数据。但它们的侧重点不同，应根据 APP 的需求，选择合适的框架。

- HealthKit
    - 除了运动数据，还可以获取健康数据，并且能够储存近乎无限的数据。
    - 可以用来连接外设
    - 获取数据的速度比 Core Motion 慢
- CoreMotion
    - 只能获取和保存一周以内的运动数据。
    - 获取数据的速度快
    - 不能连接外设

