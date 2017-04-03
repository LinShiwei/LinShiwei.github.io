---
published: true
layout: post
title: iOS：为 App 添加内购买项目
category: Tutorial
tags: 
  - iOS
  - swift
  - In-app purchase
time: 2017.03.01 09:22:00
excerpt: 本文将用一个真实的例子，以消费型内购买项目为例，介绍内购买的流程。
---

<!-- lsw toc mark1. Do not remove this comment so that lsw_toc can update TOC correctly. -->

## Table of Contents
- [前言](#1)
- [必要的准备](#2)
- [内购买项目的用户界面](#3)
- [在 iTunesConnect 上新建内购买项目](#4)
- [完成内购买相关代码](#5)
- [内购买测试](#6)
- [结语](#7)

<!-- lsw toc mark2. Do not remove this comment so that lsw_toc can update TOC correctly. -->

## <a id="1"></a>前言
在 AppStore 里，付费应用的下载量往往比免费应用的下载量少的多。上架过应用的开发者，可能会有这样的体会：当一个应用免费的时候，每天能有几十上百次的下载，但是一旦设置为收费的时候，下载量立即暴跌，即使只设成了一元，可能好几星期都没人下载。

收费的应用不好做，与其长时间零下载，还不如设置为免费，每天看看下载量来的舒服。

但是作为一个开发者，开发免费应用的动力，显然比不上开发收费应用。应用免费了，开发的动力也少了。因此，我们可以考虑在应用里面加入内购买项目，通过免费下载吸引用户，再用内购买项目让用户按需购买，自己赚点零花钱。

本文将用一个真实的例子（已上架 AppStore：[Catch - 捕捉稍纵即逝的灵感](https://itunes.apple.com/cn/app/catch-%E6%8D%95%E6%8D%89%E7%A8%8D%E7%BA%B5%E5%8D%B3%E9%80%9D%E7%9A%84%E7%81%B5%E6%84%9F/id1193123297?mt=8)），介绍为 App 添加内购买项目的流程。

## <a id="2"></a>必要的准备

添加内购买项目之前，需要有一个付费的开发者账号，并在开发者账号的“协议、税务和银行业务”里完善银行卡等信息，否则 Apple 无法将应用的收入转给你。

你还需要准备一个已上架或者未上架的应用，应用在首次添加内购买项目时需要与新的应用版本一起提交审核。

## <a id="3"></a>内购买项目的用户界面

在添加内购买项目前，你需要在你的应用里，自己设计好商品展示的界面，Apple 只负责购买的流程。这个界面在接下去新建内购买项目时也会用到。

下图是一个实际应用的内购展示界面：

![](/images/in_app_purchase1.png)

## <a id="4"></a>在 iTunesConnect 上新建内购买项目

接下来，在 iTunesConnect 上的应用页面，选择“功能”－“App 内购买项目“，点击加号新建项目，如下图：

![](/images/in_app_purchase2.png)

之后会要求选择内购买项目的类型，这里以“消费型项目”为例。在接下来的表里填写相应的信息。产品 ID 一般以 App 的 Bundle ID 为前缀再加上自定义的产品后缀，如：com.self.purchase1。在审核信息里上传刚刚的内购商品展示界面，供审查员审核。其他信息自行填写即可。

![](/images/in_app_purchase3.png)

新建内购买项目后，在内购买项目列表里显示为“准备提交”状态。现在在准备提交的 App 版本中添加刚刚新建的内购买项目。

![](/images/in_app_purchase4.png)
 
## <a id="5"></a>完成内购买相关代码

关于内购买的代码，本文将使用一个现成的框架：[SwiftyStoreKit](https://github.com/bizz84/SwiftyStoreKit)，这样有利于理清思路。对于直接使用 StoreKit 完成整个内购买的流程，将在下一篇文章里讨论。

首先在项目里添加 SwiftyStoreKit 框架。具体添加的方法上面的链接里已有说明。
总共的代码有三部分，如下：

一、获取商品信息，用于在界面上显示：

```swift
SwiftyStoreKit.retrieveProductsInfo([productID]) {[weak self ] result in
    if let product = result.retrievedProducts.first {
        let priceString = product.localizedPrice!
        print("Product: \(product.localizedDescription), price: \(priceString)")
    }else if let invalidProductId = result.invalidProductIDs.first {
        print("Could not retrieve product info .Invalid product identifier: \(invalidProductId)")
    }else {
        print("Error: \(result.error)")
    }
}
```

商品信息包括商品的价格和名称，保存在 `SKProduct` 对象里。汇率的问题 Apple 已经帮我们处理好，商品的名称会根据我们在 iTunesConect 里填写的本地化信息自动选择，因此我们只需要直接使用 `localizedPrice` 和 `localizedTitle` 或 `localizedDescription`。

二、购买商品（当用户点击购买后）：

```swift
func purchase(_ productID: String) {
    SwiftyStoreKit.purchaseProduct(productID, atomically: true) { [weak self] result in
        if case .success(let product) = result {
        // Deliver content from server, then:
        if product.needsFinishTransaction {
            SwiftyStoreKit.finishTransaction(product.transaction)
            }
        }
        if let alert = self?.alertForPurchaseResult(result) {
            self?.showAlert(alert)
        }
    }
}
```

`productID` 就是内购买项目的 ID，如：com.self.appname.purchase1。`productID` 可以事先在程序中定义，如果想从网络上获取 `productID` 的话，只能从自己的服务器中获取，iTunesConnect 并不提供获取内购买商品列表的 API。

三、完成购买事务：

```swift
func completeIAPTransactions() {
    SwiftyStoreKit.completeTransactions(atomically: true) { products in
        for product in products {
            if product.transaction.transactionState == .purchased || product.transaction.transactionState == .restored {
                if product.needsFinishTransaction {
                // Deliver content from server, then:
                    SwiftyStoreKit.finishTransaction(product.transaction)
                }
                print("purchased: \(product.productId)")
            }
        }
    }
}
```

在 application:didFinishLaunchingWithOptions 里调用上述的函数。因为 Apple 建议在 app 载入的时候为购买事务添加一个观察者：

>Adding your app's observer at launch ensures that it will persist during all launches of your app, thus allowing your app to receive all the payment queue notifications.

SwiftyStoreKit 用 completeTransactions 函数实现了这个功能。这样，如果在载入的时候有任何进行中的事务，就可以对它们进行处理，更新 app 的状态和 UI。

## <a id="6"></a>内购买测试

完成内购买的代码后，在提交审核之前，还应该对它进行测试。Apple 为应用内购买项目提供了沙箱（sandbox）测试，让你使用虚拟的货币模拟内购过程。

a) 在 iTunesConnect 的“用户与职能”里添加沙箱技术测试员。

![](/images/in_app_purchase5.png)

b) 在 iPhone 设置里的 “iTunes Store 与 App Store” 将原来的账号注销。但是不要登陆测试员的账号。

c) 打开待测试内购买的 app，点击内购买的项目进行购买。这时候，会提示登录 App Store，使用沙箱测试员的账号登录。

![](/images/in_app_purchase6.jpeg)

d) 之后会弹出购买信息确认窗口，注意窗口内的提示信息 “Environment: Sandbox“，表示是在沙箱中测试，购买的货币是虚拟的。如果没有这一行的话，则是在真实的环境中进行交易，使用的就是真实的货币了。

![](/images/in_app_purchase7.jpeg)

![](/images/in_app_purchase8.jpeg)

## <a id="7"></a>结语

测试完成后就可以提交审核了。如果是首次添加内购买项目，记得在 app 审核页添加内购项目一起提交审核。当再次添加内购买项目，就可以独立审核内购买项目，而无需提交新的 app 版本。当然，这样做的前提是 app 能够从自己的服务器上获取内购买项目的 productID，否则 app 无法获取新内购买项目的信息。

本文是以消费性内购买项目为例，对于其他类型的内购买项目，方法大同小异，更多的信息请参考[官方文档](https://developer.apple.com/library/content/documentation/NetworkingInternet/Conceptual/StoreKitGuide/Introduction.html#//apple_ref/doc/uid/TP40008267)。

**有任何疑问的话，欢迎在下方评论区讨论。**

