---
published: true
layout: post
title: iOS 10：本地消息推送指南
category: Tutorial
tags: 
  - iOS
  - Swift
time: 2016.12.23 09:22:00
excerpt: 
---

# 前言

Apple 应用的消息推送分为本地消息推送（Local Notification）和远程消息推送（Remote Notification）。当有新的消息时，可以通过本地或远程推送告知用户，即使 App 并未运行。

本地消息推送不需要联网，由系统统一管理 App 推送的消息，App 只需与系统交互即可。本地消息推送适用于 iOS、tvOS 和 watchOS。

远程消息推送需要连接网络，通过 App 或者后台服务器与 Apple Push Notification（APN） 通信，再由 APN 将消息推送到终端上。远程消息推送除了支持 iOS、tvOS 和 watchOS，还支持 macOS。

本文将大体介绍消息推送的相关内容，并重点介绍实现本地消息推送的流程。实现本地消息推送的步骤请看**“本地消息推送”**这部分。

# iOS 消息推送的基础知识

## 推送方式

尽管消息推送方式分为本地和远程，但是他们展现给用户的方式是一样的，因为它们默认使用的是系统提供的外观。主要的推送方式有：

- 通知、横幅
- 应用图标标记
- 带有声音的通知、横幅或标记

## 推送流程

> App must be configured at launch time to support local and remote notification.

首先，我们需要在 `applicationDidFinishLaunching:` 之前声明支持消息推送的方式。如果想在 App 运行后某个时间再进行声明的话，在此之前要避免推送消息。因为在声明支持消息推送之前，发送任何消息都是无效的。

当配置了消息推送的方式后，需要请求授权：`requestAuthorizationWithOptions:completionHandler:`，第一次调用该方法时，系统会提示用户 App 需要推送消息，等待用户确认。系统自动保存用户的授权结果，当以后调用该方法时，就不会在出现提示了。

获得推送消息权限后，就需要考虑以下几个问题：

一、设定 Category。当 App 推送的消息很多，需要进行分类时，就需要设定 Category。

```
let generalCategory = UNNotificationCategory(identifier: "GENERAL",actions: [],intentIdentifiers: [],options: .customDismissAction)
 // Register the category.
let center = UNUserNotificationCenter.current()
center.setNotificationCategories([generalCategory])
```

设定消息的 Category 后，就可以添加自定义的行为（action），这样用户就可以在不打开 App 的情况下，对消息进行简单的操作。如果不为消息分配 Category，那么消息就会以默认的形式推送，不带有任何附加的行为。

二、为 Category 添加自定义的行为。每个 Category 最多可以包含四个自定义的行为。

```
let generalCategory = UNNotificationCategory(identifier: "GENERAL",actions: [],intentIdentifiers: [],options: .customDismissAction)
 
// Create the custom actions for the TIMER_EXPIRED category.
let snoozeAction = UNNotificationAction(identifier: "SNOOZE_ACTION",title: "Snooze", options: UNNotificationActionOptions(rawValue: 0))
let stopAction = UNNotificationAction(identifier: "STOP_ACTION",title: "Stop",options: .foreground)
 
let expiredCategory = UNNotificationCategory(identifier: "TIMER_EXPIRED", actions: [snoozeAction, stopAction],intentIdentifiers: [], options: UNNotificationCategoryOptions(rawValue: 0))
 
// Register the notification categories.
let center = UNUserNotificationCenter.current()
center.setNotificationCategories([generalCategory, expiredCategory])
```

三、配置通知声音。

四、管理推送设置。由于用户可以在设置里自由的打开或关闭 App 推送功能，在程序中，需要判断推送功能是否可用：`getNotificationSettingsWithCompletionHandler: `。

五、管理推送消息。我们可以给用户推送消息，也可以管理已经推送或将要推送的消息。当一条消息已经不具备时效性，那么我们就应该把它从通知栏中消除。使用：`removeDeliveredNotificationsWithIdentifiers:` 或 `removePendingNotificationsWithIdentifiers:`。

**有任何疑问的话，欢迎在下方评论区讨论。**

