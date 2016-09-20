---
published: true
layout: post
title: UISearchBar：使用 becomeFirstResponder 获得焦点并唤起键盘
category: Tutorial
tags: 
  - swift
  - iOS
  - UISearchBar
  - UISearchController
time: 2016.09.02 09:23:00
excerpt: 当我们使用 UISearchBar 时，常常会想当 searchBar 出现时，自动获得焦点并唤起键盘，这样就能省去用户手动点击搜索框准备输入这个步骤。但是某些情况下，使用 becomeFirstResponder 并不能实现我们的目标。
---

<!-- lsw toc mark1. Do not remove this comment so that lsw_toc can update TOC correctly. -->

## Table of Contents
- [背景](#1)
- [问题描述](#2)
- [原因分析](#3)
- [解决方法](#4)
- [结语](#5)

<!-- lsw toc mark2. Do not remove this comment so that lsw_toc can update TOC correctly. -->

## <a id="1"></a>背景

当我们使用 `UISearchBar` 时，常常会想当 `searchBar` 出现时，自动获得焦点并唤起键盘，这样就能省去用户手动点击搜索框准备输入这个步骤。
从 Apple 的官方文档中，我们知道：

>- becomeFirstResponder

>Notifies the receiver that it is about to become first responder in its window.

即对于继承自 `UIResponder` 的类，如：`UISearchBar`，使用 `becomeFirstResponder` 能够使其获得焦点，同时 `CocoaTouch` 还做了优化：获得焦点后当控件需要输入时，能够自动唤起键盘。

因此，我们只需要关注如何使 `UISearchBar` 获得焦点。但是某些情况下，使用 `becomeFirstResponder` 并不能实现我们的目标。下面我们将在实例中解决这个问题。 

## <a id="2"></a>问题描述

在目前我正在开发的**天气APP（源码请看[这里](https://github.com/LinShiwei/WeatherDemo)）**中，主界面的左侧有一个 `tableView` 用于显示不同的城市，其中有一个 `tableViewCell`，当点击它的时候，会出现另一个 `viewController` 供用户添加新的城市。

假设这个 `viewController` 为 `viewController_A`，这个类里包含了一个 tableView，和一个 `UISearchBarController`。

这样把 `tableView` 的 `tableHeaderView` 设置为 `searchController.searchBar`，就能把 `searchBar` 显示在 tableView 上。

现在的问题就是，当点击 `tableViewCell`，出现了包含 `searchBar` 的 `viewController_A` 时，并不会将焦点定位到 `searchBar` 上，当然也不会出现键盘。

我尝试了在 `viewController_A` 的 `viewDidLoad()` 里用：

```swift
searchController.active = true
searchController.searchBar.becomeFirstResponder()
```

第一行用于激活 `searchController`，第二行让 `searchBar` 获得焦点。

但是运行结果表明，只激活了 `searchController`，而没有把焦点定位到 `searchBar` 上。

## <a id="3"></a>原因分析

在官方文档里有如下描述：

>A responder object only becomes the first responder if the current responder can resign first-responder status (canResignFirstResponder) and the new responder can become first responder.

**一个 `responder` 想要成功获得焦点，必需满足，上一个 `responder` 能够放弃焦点，并且当前的 `responder` 能够获得焦点。**

因此，问题就出在之前描述的那种情况下，使用：`SearchController.searchBar.becomeFirstResponder()` 的时候，`searchBar` 并没有能力获得焦点，因此焦点设置不成功。

但是为什么 `searchBar` 这时候没有能力获得焦点呢？

因为，在 `viewDidLoad()` 的时候，`searchController` 也刚刚初始化，必需得等到 `searchController` 初始化完毕，呈现出来的时候，才能为 `searchBar` 设置焦点。

## <a id="4"></a>解决方法

为了在 `searchController` 初始化之后，再进行 `searchBar` 焦点设置，我们可以为 `viewController_A` 声明 `UISearchControllerDelegate`，并在 `didPresentSearchController` 中添加焦点设置代码，如下：

```swift
extension ViewController_A : UISearchControllerDelegate {
    func didPresentSearchController(searchController: UISearchController) {
        searchController.searchBar.becomeFirstResponder()
    }
}
```

这样就能在出现 `viewController_A` 后，自动将焦点定位到 `searchBar` 并唤起键盘。

## <a id="5"></a>结语

这其实是 `View` 和 `ViewController` 的**生命周期（cycle）**的问题，在周期的各个阶段，会触发相应的事件，可以进行相应的设置。

之前在 `viewDidLoad()` 中同时设置 `searchController.active` 和 `searchController.searchBar.becomeFirstResponder()`，由于此时 `searchBar` 是不可用的，因此对它的设置无效。必需在  `searchController` 初始化完毕才能对 `searchBar` 进行设置。因此，后来，我们在 `didPresentSearchController` 中设置 `searchBar`，就能设置成功了。


