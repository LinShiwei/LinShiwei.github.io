---
published: true
layout: post
title: 为未勾选“ Using CoreData ”的项目添加 CoreData 支持
category: Tutorial
tags: 
  - swift
  - iOS
  - CoreData
time: 2016.09.09 12:22:00
excerpt: CoreData 作为一个官方的数据存储框架，具有很高的性能。新建项目时，勾选 Using CoreData 能够让 Xcode 自动配置 CoreData 框架，但有时侯会忘记勾选这个选项，这时候就需要自己配置 CoreData 了。
---

<!-- lsw toc mark1. Do not remove this comment so that lsw_toc can update TOC correctly. -->

## Table of Contents
- [前言](#1)
- [手动配置 CoreData](#2)
    - [添加 CoreData 框架](#21)
    - [添加 CoreData 模型文件](#22)
    - [添加 CoreData 配置代码](#23)
    - [使用 CoreData](#24)

<!-- lsw toc mark2. Do not remove this comment so that lsw_toc can update TOC correctly. -->

## <a id="1"></a>前言

[CoreData](https://developer.apple.com/library/watchos/documentation/Cocoa/Conceptual/CoreData/index.html) 作为一个官方的数据存储框架，具有很高的性能。在应用开发中，涉及到大量数据时，常常会使用它作为数据存储。
在 Xcode 中，新建项目时，有一个“ Using CoreData ”选项。勾选这个选项后，Xcode 会在建立项目时自动为你配置好 CoreData 的使用环境，非常方便。
但是当建立项目时未勾选“ Using CoreData ”，想在已有的项目中使用 CoreData ，就需要自己手动配置。本文主要介绍了手动配置 CoreData 的方法。

## <a id="2"></a>手动配置 CoreData

### <a id="21"></a>添加 CoreData 框架

在项目属性页 General 里的 Linked Frameworks and Libraries 中添加 CoreData.framework 。

### <a id="22"></a>添加 CoreData 模型文件

在 Xcode 左侧的导航栏的项目文件夹上点击右键，选择“ New File... ”，在弹出的对话框中选择“ iOS -> Core Data -> Data Model ”添加一个 CoreData 模型文件，在这个文件里可以添加自定义的模型对象。

### <a id="23"></a>添加 CoreData 配置代码

在 AppDelegate.swift 中，import UIKit 下面导入 CoreData ：

```swift
import CoreData
```

最后一个大括号前面添加以下 CoreData 配置代码，注意要把代码中的 `YourDataModelName` 替换成刚刚新建的模型文件名：

```swift
// MARK: - Core Data stack
    
    lazy var applicationDocumentsDirectory: NSURL = {
        // The directory the application uses to store the Core Data store file. This code uses a directory named "lsw.self.MyGraphics" in the application's documents Application Support directory.
        let urls = NSFileManager.defaultManager().URLsForDirectory(.DocumentDirectory, inDomains: .UserDomainMask)
        return urls[urls.count-1]
    }()
    
    lazy var managedObjectModel: NSManagedObjectModel = {
        // The managed object model for the application. This property is not optional. It is a fatal error for the application not to be able to find and load its model.
        let modelURL = NSBundle.mainBundle().URLForResource("YourDataModelName", withExtension: "momd")!
        return NSManagedObjectModel(contentsOfURL: modelURL)!
    }()
    
    lazy var persistentStoreCoordinator: NSPersistentStoreCoordinator = {
        // The persistent store coordinator for the application. This implementation creates and returns a coordinator, having added the store for the application to it. This property is optional since there are legitimate error conditions that could cause the creation of the store to fail.
        // Create the coordinator and store
        let coordinator = NSPersistentStoreCoordinator(managedObjectModel: self.managedObjectModel)
        let url = self.applicationDocumentsDirectory.URLByAppendingPathComponent("SingleViewCoreData.sqlite")
        var failureReason = "There was an error creating or loading the application's saved data."
        do {
            try coordinator.addPersistentStoreWithType(NSSQLiteStoreType, configuration: nil, URL: url, options: nil)
        } catch {
            // Report any error we got.
            var dict = [String: AnyObject]()
            dict[NSLocalizedDescriptionKey] = "Failed to initialize the application's saved data"
            dict[NSLocalizedFailureReasonErrorKey] = failureReason
            
            dict[NSUnderlyingErrorKey] = error as NSError
            let wrappedError = NSError(domain: "YOUR_ERROR_DOMAIN", code: 9999, userInfo: dict)
            // Replace this with code to handle the error appropriately.
            // abort() causes the application to generate a crash log and terminate. You should not use this function in a shipping application, although it may be useful during development.
            NSLog("Unresolved error \(wrappedError), \(wrappedError.userInfo)")
            abort()
        }
        
        return coordinator
    }()
    
    lazy var managedObjectContext: NSManagedObjectContext = {
        // Returns the managed object context for the application (which is already bound to the persistent store coordinator for the application.) This property is optional since there are legitimate error conditions that could cause the creation of the context to fail.
        let coordinator = self.persistentStoreCoordinator
        var managedObjectContext = NSManagedObjectContext(concurrencyType: .MainQueueConcurrencyType)
        managedObjectContext.persistentStoreCoordinator = coordinator
        return managedObjectContext
    }()
    
    // MARK: - Core Data Saving support
    
    func saveContext () {
        if managedObjectContext.hasChanges {
            do {
                try managedObjectContext.save()
            } catch {
                // Replace this implementation with code to handle the error appropriately.
                // abort() causes the application to generate a crash log and terminate. You should not use this function in a shipping application, although it may be useful during development.
                let nserror = error as NSError
                NSLog("Unresolved error \(nserror), \(nserror.userInfo)")
                abort()
            }
        }
    }

```

### <a id="24"></a>使用 CoreData

进行以上配置后，就可以在项目文件中使用 CoreData 了，记得在文件开头 import CoreData ：

```swift
import CoreData
```

Enjoy yourself~


