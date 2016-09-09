---
published: true
layout: post
title: iOS ：自定义 searchController 和 searchBar
category: Tutorial
tags: 
  - swift
  - iOS
  - UISearchBar
  - UISearchController
time: 2016.09.07 13:19:00
excerpt: 在 iOS app 中，搜索功能非常常见，UISearchBar 为开发者提供了基本的 UI ，它具有默认的外观，并已经配置了一些现成的函数和委托（delegate）。但是这个默认的 searchBar 是只读的，并不能更改它的外观。那我们该怎样自定义 searchBar 呢？
---

## 背景

在 iOS app 中，搜索功能非常常见，如：各类网络视频 APP ，字典类 APP ，以及我最近正在做的[天气 APP](https://github.com/LinShiwei/WeatherDemo)。CocoaTouch 自带的 `UISearchController`，包含了一个 `searchBar: UISearchBar` 为开发者提供了基本的 UI ，它具有默认的外观，并已经配置了一些现成的函数和委托（delegate）。
但是这个默认的 searchBar 是只读的，并不能更改它的外观。那我们该怎样自定义 searchBar 呢？

## 教程：自定义 searchBar 和 searchController

在官方文档中 `UISearchController` 这一部分有下面一句话：

> To use a custom subclass of UISearchBar, subclass UISearchController and implement this property to return your custom search bar.

这句话说明了，想要有自定义 searchBar 的话，应该 有一个 `UISearchController` 子类（如：CustomSearchController）和 `UISearchBar` 子类（如：CustomSearchBar），并在 CustomSearchController 中声明一个 CustomSearchBar 的属性。

 **详细的教程和步骤请参考[这里](http://www.appcoda.com/custom-search-bar-tutorial/)。**

## 核心思路

详细的步骤上面的链接已经给出，但是教程篇幅较长，内容很多。光看教程很容易只知其然而不知其所以然。下面我大致介绍一下，整个自定义过程的**核心思路**。

- **核心思路**如下：

1. 创建一个 CustomSearchBar 类继承自 `UISearchBar` 。
 - 在 drawRect(rect:CGRect) 中更改外观。
 - 重写初始化函数 `init(frame: CGRect)` 或者自定义初始化函数，记得设定 `frame` 属性。

2. 创建一个 CustomSearchController 类继承自 `UISearchController` 。
 - 在类里声明一个属性：

```swift
 customSearchBar: CustomSearchBar!
```
 
 - 在定义初始化函数，并在初始化函数中调用 CustomSearchBar 的初始化函数。

3. 由于是自定义的 searchBar ，不支持原有的一些 delegate 协议。因此需要自己声明 delegate 协议。
 - 声明 CustomSearchControllerDelegate 协议，如：
 
```swift
protocol CustomSearchControllerDelegate {
    func didChangeSearchTextInSearchBar(searchBar:CustomSearchBar, searchText:String)
} 
```
 
 - 在 CustomSearchController 类中声明一个属性：
 
```swift
 customDelegate: CustomSearchControllerDelegate?
```
 
 - 在包含 CustomSearchController 的上一级 viewController 中支持并实现这个协议。
 
```swift
 extension ViewController: CustomSearchControllerDelegate
```
 
 - 把 customDelegate 设为这个 viewController，即让这个 viewController 作为 customSearchController 的代理。 

4. 让 CustomSearchController 支持 `UISearchBarDelegate` 。
  
```swift
 extension CustomSearchController: UISearchBarDelegate
```

 - 设 customSearchBar.delegate 为 CustomSearchController。
 - 在 CustomSearchController 中实现 `UISearchBarDelegate` ，在具体的实现中可以通过 customDelegate 调用 CustomSearchControllerDelegate 中的函数，如：
  
```swift
extension CustomSearchController : UISearchBarDelegate{
    func searchBar(searchBar: UISearchBar, textDidChange searchText: String) {
        guard let bar = searchBar as? CustomSearchBar else {return}
        searchDelegate?.didChangeSearchTextInSearchBar(bar, searchText: searchText)
    }
}  
```

这就是整个自定义 searchBar 和 searchController 的流程，在自定义外观的同时，还应该记得定义自己的 delegate ，否则定义的 searchBar 就没法使用了。


