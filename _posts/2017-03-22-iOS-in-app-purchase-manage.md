---
published: true
layout: post
title: iOS：动态管理 App 内购买项目
category: Tutorial
tags: 
  - iOS
  - swift
  - In-app purchase
time: 2017.03.22 09:22:00
excerpt: 本文介绍如何实现动态添加和删除 App 内购买项目，而无需更新 App。
---

## 前言

在[iOS：为 App 添加内购买项目](http://linshiwei.site/tutorial/2017/03/01/iOS-in-app-purchase)一文里，我们介绍了为 App 添加内购买项目的方法。对于一般的情况，文中的方法已经够用。但是如果想在不上传新 App 版本的前提下，添加或删除 App 中的内购买项目，就需要做一些额外的工作。

## 思路

实现动态管理 App 内购买项目的整体思路如下：

1. 搭建后台服务器，为 App 提供内购买产品 ID；
2. 在 iTunes Connect 中添加或删除内购买项目，并在服务器数据库中同步。
3. 在 App 中添加从服务器获取数据的代码。

### 1、后台服务器

后台服务器能够根据 http 请求，返回相应的数据。关于搭建后台服务器的方法，请看这篇文章：[文章](http://linshiwei.site/tutorial/2016/11/05/Web-server-JSON-API)。

假定服务器返回的是 JSON 格式的数据，如下：

```p
{"status":true,"IDSuffix":[{"id":"purchase1"},{"id":"purchase2"}]}
```

其中的 purchase1 和 purchase2 就是内购买项目的产品 ID 后缀。
从服务器获取到产品 ID 后缀后，然后在 App 程序中与 App Bundle ID 拼接得到：com.appname.self.purchase1 和 com.appname.self.purchase2。这两个 ID 就是产品 ID，必须和 iTunes Connect 上添加的内购买产品 ID 一致。这样就能通过服务器获取到当前的产品，用于更新内购买项目。

### 2、添加或删除内购买项目

由于 Apple 并没有提供官方的接口，用于从 iTunes Connect 上获取内购买项目列表，因此我们应该手动在 iTunes Connect 上添加或删除内购买项目，并同时在服务器的数据库中更新当前可用的内购买产品 ID 后缀。

这样我们从自己的服务器获取数据时，就能得到最新的内购买项目列表。

### 3、获取内购买数据

在 App 程序内部，我们需要让 App 发出 http 请求，从服务器获取内购买项目的数据。如果服务器支持 https，则可以直接用 https 请求。

下面的代码使用单例模式，实现了从服务器获取并返回内购产品 ID 后缀的功能。

```
import Foundation
import Alamofire
import SwiftyJSON

internal class WebServerManager {
    private let serverAPIAddress = "http://YourServerDataAPIAddress"
    static let shared = WebServerManager()
    private init(){
    }
    
    internal func getDataFromServer(_ completion: @escaping (Bool,[String]?)->Void){
        let url = URL(string:serverAPIAddress)!
        Alamofire.request(url).responseJSON{ response in
            if let anyValue = response.result.value{
                let json = JSON(anyValue)
                if json["status"].boolValue == true , let idSuffix = json["IDSuffix"].array {
                    var suffixs = [String]()
                    for item in idSuffix{
                        if let suffix = item["id"].string{
                            suffixs.append(suffix)
                        }else{
                            print("data from server invalid")
                        }
                    }
                    completion(true,suffixs)
                }else{
                    completion(false,nil)
                    print("json data format invalid")
                }
            }else{
                DispatchQueue.main.async {
                    completion(false,nil)
                    print("fail to fetch data")
                }
            }
        }
    }
}
```

可以通过调用 getDataFromServer 方法，获取产品 ID 后缀，之后拼接得到产品 ID 后，使用 StoreKit 的 API 从 Apple 服务器获取内购买项目的数据。

这就实现了从服务器获取当前可用的内购买产品 ID（后缀），动态更新应用内购买项目。为 App 添加内购买项目的方法请看[这里](http://linshiwei.site/tutorial/2017/03/01/iOS-in-app-purchase)。


**有任何疑问的话，欢迎在下方评论区讨论。**

