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

尽管消息推送方式分为本地和远程，但是他们展现给用户的方式是一样的，因为它们默认使用的是系统提供的外观。主要的推送方式有：

- 通知、横幅
- 应用图标标记
- 带有声音的通知、横幅或标记




**有任何疑问的话，欢迎在下方评论区讨论。**

