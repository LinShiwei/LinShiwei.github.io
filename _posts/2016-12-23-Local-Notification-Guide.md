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



**有任何疑问的话，欢迎在下方评论区讨论。**

