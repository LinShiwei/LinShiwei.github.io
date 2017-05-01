---
published: false
layout: post
title: iOS：XML 解析入门示例
category: Tutorial
tags: 
  - iOS
  - Objective-C
  - XML
time: 2017.04.14 09:22:00
excerpt: 本文介绍 XML 的基础知识，并用 NSXMLParser 和 NSXMLParserDelegate 实现了一个简单 XML 解析实例，用于为刚接触 iOS XML 解析的开发者提供快速上手的资料。
---

## 前言：关于 XML

XML（Extensible Markup Language），中文名：可拓展标记语言，它定义了数据和文档的编码规范，是编码后的文件既便于人类阅读，又能让机器识别。

### XML 和 HTML

刚接触 XML，可能会把它和 HTML 混在一起。

HTML（Hypertext Markup Language）是超文本标记语言，它关注于如何呈现数据，是用来展示数据的。

XML 关注数据是什么，用于携带数据传输。XML 里面的 tag 并不是预定义的，而是编码人员根据需要自行定义。

### 与 XML 相关的缩写

- DOM：Document Object Model，是 W3C 提出的一个模型，用于描述 XML 和 HTML 的对象，并且定义了一些接口，用于获取和操作对象；
- SAX：Simple API for XML，是基于事件驱动的 XML 解析；
- DTD：Document Type Definition，定义 XML 文件的结构，包含合法的元素和属性，可以在 XML 内部或外部定义。

## XML 解析方法



**有任何疑问的话，欢迎在下方评论区讨论。**

