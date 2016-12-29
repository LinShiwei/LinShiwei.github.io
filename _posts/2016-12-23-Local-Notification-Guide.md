---
published: true
layout: post
title: iOS 10：本地消息推送指南
category: Tutorial
tags: 
  - iOS
  - swift
  - UserNotifications
time: 2016.12.23 09:22:00
excerpt: Apple 应用的消息推送分为本地消息推送（Local Notification）和远程消息推送（Remote Notification）。当有新的消息时，可以通过本地或远程推送告知用户，即使 App 并未运行。
---

<!-- lsw toc mark1. Do not remove this comment so that lsw_toc can update TOC correctly. -->

## Table of Contents
- [前言](#1)
- [iOS 消息推送的基础知识](#2)
    - [推送方式](#21)
    - [管理消息推送](#22)
- [本地消息推送实现](#3)

<!-- lsw toc mark2. Do not remove this comment so that lsw_toc can update TOC correctly. -->

# <a id="1"></a>前言

Apple 应用的消息推送分为本地消息推送（Local Notification）和远程消息推送（Remote Notification）。当有新的消息时，可以通过本地或远程推送告知用户，即使 App 并未运行。

本地消息推送不需要联网，由系统统一管理 App 推送的消息，App 只需与系统交互即可。本地消息推送适用于 iOS、tvOS 和 watchOS。

远程消息推送需要连接网络，通过 App 或者后台服务器与 Apple Push Notification（APN） 通信，再由 APN 将消息推送到终端上。远程消息推送除了支持 iOS、tvOS 和 watchOS，还支持 macOS。

本文将大体介绍消息推送的相关内容，并实现基本的本地消息推送。

# <a id="2"></a>iOS 消息推送的基础知识

## <a id="21"></a>推送方式

尽管消息推送方式分为本地和远程，但是他们展现给用户的方式是一样的，因为它们默认使用的是系统提供的外观。主要的推送方式有：

- 通知、横幅
- 应用图标标记
- 带有声音的通知、横幅或标记

## <a id="22"></a>管理消息推送

> App must be configured at launch time to support local and remote notification.

首先，我们需要在 `applicationDidFinishLaunching:` 之前声明支持消息推送的方式。如果想在 App 运行后某个时间再进行声明的话，在此之前要避免推送消息。因为在声明支持消息推送之前，发送任何消息都是无效的。

当配置了消息推送的方式后，需要请求授权：`requestAuthorizationWithOptions:completionHandler:`，第一次调用该方法时，系统会提示用户 App 需要推送消息，等待用户确认。系统自动保存用户的授权结果，当以后调用该方法时，就不会在出现提示了。

获得推送消息权限后，就需要考虑以下几个问题：

一、设定 Category。当 App 推送的消息很多，需要进行分类时，就需要设定 Category。

```swift
let generalCategory = UNNotificationCategory(identifier: "GENERAL",actions: [],intentIdentifiers: [],options: .customDismissAction)
 // Register the category.
let center = UNUserNotificationCenter.current()
center.setNotificationCategories([generalCategory])
```

设定消息的 Category 后，就可以添加自定义的行为（action），这样用户就可以在不打开 App 的情况下，对消息进行简单的操作。如果不为消息分配 Category，那么消息就会以默认的形式推送，不带有任何附加的行为。

二、为 Category 添加自定义的行为。每个 Category 最多可以包含四个自定义的行为。

```swift
let generalCategory = UNNotificationCategory(identifier: "GENERAL",actions: [],intentIdentifiers: [],options: .customDismissAction)
 
// Create the custom actions for the TIMER_EXPIRED category.
let snoozeAction = UNNotificationAction(identifier: "SNOOZE_ACTION",title: "Snooze", options: UNNotificationActionOptions(rawValue: 0))
let stopAction = UNNotificationAction(identifier: "STOP_ACTION",title: "Stop",options: .foreground)
 
let expiredCategory = UNNotificationCategory(identifier: "TIMER_EXPIRED", actions: [snoozeAction, stopAction],intentIdentifiers: [], options: UNNotificationCategoryOptions(rawValue: 0))
 
// Register the notification categories.
let center = UNUserNotificationCenter.current()
center.setNotificationCategories([generalCategory, expiredCategory])
```

三、配置通知声音。本地和远程推送都可以自定义声音。自定义声音的音频编码形式可以是以下几种：

- Linear PCM
- MA(IMA/ADPCM)
- uLaw
- aLaw

而音频文件应该为 `.aiff`、`.wav` 或 `.caf` 文件。音频时长必须小于 30s，否则系统会使用默认的声音。Mac 里自带了 afconvert 音频格式转换工具。如在终端中输入如下代码，可以将 16-bit linear PCM 编码的 `Submarine.aiff` 文件转化为 IMA4 编码的 `.caf` 文件：

```ruby
afconvert /System/Library/Sounds/Submarine.aiff ~/Desktop/sub.caf -d ima4 -f caff -v
```

四、管理推送设置。由于用户可以在设置里自由的打开或关闭 App 推送功能，在程序中，需要判断推送功能是否可用：`getNotificationSettingsWithCompletionHandler: `。

五、管理推送消息。我们可以给用户推送消息，也可以管理已经推送或将要推送的消息。当一条消息已经不具备时效性，那么我们就应该把它从通知栏中消除。使用：`removeDeliveredNotificationsWithIdentifiers:` 或 `removePendingNotificationsWithIdentifiers:`。

# <a id="3"></a>本地消息推送实现

下面的代码是实现了一个负责推送消息的对象，它包含了**请求推送**和**创建推送消息**的方法。

```swift
import UIKit
import UserNotifications

internal class LocalNotificationManager: NSObject {
    static let shared = LocalNotificationManager()
    private let notificationCenter = UNUserNotificationCenter.current()
    private override init(){
        super.init()        
    }
    //用于请求推送权限
    internal func requestAuthorization(){
        notificationCenter.requestAuthorization(options: [.alert, .sound]){ (granted, error) in
            if(granted&&error == nil){
                
            }else{
                
            }
        }
    }
    //用于创建推送消息（创建的消息将在调用函数后十秒发出）
    internal func createNewNotification(){     
        let content = UNMutableNotificationContent()
        content.title = NSString.localizedUserNotificationString(forKey: "Alarm", arguments: nil)
        content.body = NSString.localizedUserNotificationString(forKey: "WakeUp", arguments: nil)
        let trigger = UNTimeIntervalNotificationTrigger(timeInterval: 10, repeats: false)
        let request = UNNotificationRequest(identifier: "MyNotification", content: content, trigger: trigger)
        
        notificationCenter.add(request){(error) in
            if let _ = error {
                assertionFailure()
            }
        }
    }
}
```

有了上面管理消息推送的对象，实现简单的本地消息推送只需要以下两步：

一、在 AppDelegate.swift 里的 `application:willFinishLaunchingWithOptions:` 调用  `requestAuthorization` 请求授权：

```swift
func application(_ application: UIApplication, willFinishLaunchingWithOptions launchOptions: [UIApplicationLaunchOptionsKey : Any]? = nil) -> Bool {
        LocalNotificationManager.shared.requestAuthorization()  
        return true
}
```

二、在要推送消息的地方调用：

```swift
LocalNotificationManager.shared.createNewNotification()
```

这样就能收到推送的消息。
当 App 在后台运行时，消息会以横幅的形式出现。
当 App 在前台运行时，消息会直接传递给 App，默认状态下不出现横幅。想在前台运行时也出现横幅，可以实现 UNUserNotificationCenterDelegate 代理方法，在 completionHandler 里添加需要的推送形式：

```swift
func userNotificationCenter(_ center: UNUserNotificationCenter, willPresent notification: UNNotification, withCompletionHandler completionHandler: @escaping (UNNotificationPresentationOptions) -> Void) {
        completionHandler(UNNotificationPresentationOptions.alert)
}
```

**有任何疑问的话，欢迎在下方评论区讨论。**

