---
published: true
layout: post
title: Localization：本地化 iOS 应用
category: Tutorial
tags: 
  - iOS
  - Xcode
time: 2016.12.13 09:22:00
excerpt: 本地化是将一个 App 的语言文字转换成多种语言的过程，如：原来只支持一种语言的 App，经过本地化后，能够支持多种语言。本地化有助于让更多人使用你的 App，让 App 国际化。
---

<!-- lsw toc mark1. Do not remove this comment so that lsw_toc can update TOC correctly. -->

## Table of Contents
- [前言](#1)
- [本地化](#2)
    - [Storyboard](#21)
    - [Info.plist](#22)
    - [代码中的本地化（少量）](#23)

<!-- lsw toc mark2. Do not remove this comment so that lsw_toc can update TOC correctly. -->

# <a id="1"></a>前言

本地化是将一个 App 的语言文字转换成多种语言的过程，如：原来只支持一种语言的 App，经过本地化后，能够支持多种语言。

本地化不只是单纯的翻译，它还包括以下内容：

- 日期和时间格式。不同地区的日期时间格式不一样。
- 文字的排版。如：有的语言是从右至左的阅读顺序。
- 界面排版优化。同样的词汇在不同语言下长短不一，在 App 界面上显示效果不一样，需要用 Auto Layout 进行适配。
- 代码的适配。当程序中需要根据语言文字进行分类、排序、搜索、解析等操作时，不同的语言需要有不同的处理方案。
- ......

由于本地化涵盖了大量的内容，完整的文档请参考：[Internationalization and Localization Guide](https://developer.apple.com/library/content/documentation/MacOSX/Conceptual/BPInternational/Introduction/Introduction.html#//apple_ref/doc/uid/10000171i-CH1-SW1)。

**本文针对的情况是：**

- 轻量级的本地化。需要本地化的内容较少，主要存在于：
 
1. Storyboard（Main，LaunchScreen）等 UI 元素中；
2. Info.plist 文件中；
3. 代码里（较少）。

接下去将针对这三个方面进行讨论。

# <a id="2"></a>本地化

## <a id="21"></a>Storyboard

本地化的第一步：勾选 `Use Base Internationalization`。如下图，在项目的 Info 页面底部：

![](/images/Localizing_1.png)

然后在 Localizations 列表里添加需要本地化的语言。Xcode 项目的开发语言是 English，在这里添加的是 Chinese(Simplified)。添加时会提示勾选需要本地化的文件，可以勾选 Main.storyboard 和 LaunchScreen.storyboard。

![](/images/Localizing_2.png)

之后在导航栏里可以发现 Main.storyboard 和 LaunchScreen.storyboard 里分别包含了两个文件：

![](/images/Localizing_3.png)

Main.strings 里包含了从 Main.storyboard 中提取出的可本地化的元素，是一系列的键-值对和注释。在这个文件中，把需要本地化的内容进行翻译即可，如下：

![](/images/Localizing_4.png)

本地化 storyboard 中的内容后，可以在 Assistant Editor 中预览本地化效果（打开 Assistant Editor 后，选择 Preview，在右下角可以选择模拟的语言，还可以使用自带的伪代码调试界面）：

![](/images/Localizing_5.png)

## <a id="22"></a>Info.plist

Info.plist 中常常会包含有对 App 进行描述的文字。对于 Info.plist 的本地化，**不要点击 `Localize...`**(Xcode8)：

![](/images/Localizing_6.png)

而应该在项目中 `New File...`，新建一个 InfoPlist.strings 文件，并在 File Inspector 的 Localization 里选择本地化语言：

![](/images/Localizing_7.png)

之后在该文件中对需要本地化的 Info.plist 条目进行配置，如修改 App 的名称：

```a
CFBundleDisplayName = "TextEdit";
```

或者修改其他的键值：

![](/images/Localizing_8.png)

这样在 App 运行时，会根据系统选择的语言读取相应 Info.plist 里的配置。

## <a id="23"></a>代码中的本地化（少量）

当代码中仅有少量内容需要本地化时，可以使用下面代码获取当前系统的语言，再根据不同语言使用相应的代码：

Objective-C：

```Objective-C
NSString *languageID = [[NSBundle mainBundle] preferredLocalizations].firstObject;
```

Swift：

```swift
let languageID = Bundle.main.preferredLocalizations.first
```

使用以上方法基本上可以完成普通 App 的本地化，重度本地化请参考官方文档 [Internationalization and Localization Guide](https://developer.apple.com/library/content/documentation/MacOSX/Conceptual/BPInternational/Introduction/Introduction.html#//apple_ref/doc/uid/10000171i-CH1-SW1)。

**附上一个已实现中英文本地化的 App 源码：[ColorPicker](https://github.com/LinShiwei/ColorPicker)**，已上架 AppStore：[链接](https://itunes.apple.com/cn/app/colorpicker-pick-color-easily/id1183292373?mt=8)。

**有任何疑问的话，欢迎在下方评论区讨论。**

