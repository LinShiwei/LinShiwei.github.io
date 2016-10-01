---
published: true
layout: post
title: Swift 3.0 ：UnsafePointer 
category: Experience
tags: 
  - swift
  - iOS
  - UnsafePointer
time: 2016.10.01 09:22:00
excerpt: 在用 Swift 进行 iOS 开发时，有时会需要调用一些 C++ 的 API，如：使用 OpenCV 。这时候经常需要使用指针，对内存进行访问和处理。在 3.0 版本之前，Swift 的指针 API 比较晦涩难懂，使用指针 API 时经常是只知其然而不知其所以然。但在 Swift 3.0 里，这部分内容有了重大的改善，变的更有条理更清晰了。
---

<!-- lsw toc mark1. Do not remove this comment so that lsw_toc can update TOC correctly. -->

## Table of Contents
- [前言](#1)
- [Unsafe 结构体](#2)
        - [1. Raw](#211)
        - [2. Mutable](#212)
        - [3. Buffer](#213)

<!-- lsw toc mark2. Do not remove this comment so that lsw_toc can update TOC correctly. -->

## <a id="1"></a>前言

在用 Swift 进行 iOS 开发时，有时会需要调用一些 C++ 的 API，如：使用 OpenCV 。这时候经常需要使用指针，对内存进行访问和处理。

Swift 是支持指针的。在 3.0 版本之前，Swift 的指针 API 比较晦涩难懂，使用指针 API 时经常是只知其然而不知其所以然。但在 Swift 3.0 里，这部分内容有了重大的改善，变的更有条理更清晰了。

## <a id="2"></a>Unsafe 结构体

在 Swift 3.0 里，定义了如下有关指针的结构体：

- UnsafePointer
- UnsafeRawPointer
- UnsafeMutablePointer
- UnsafeMutableRawPointer
- UnsafeBufferPointer
- UnsafeMutableBufferPointer
- UnsafeBufferPointerIterator

它们都以 Unsafe 开头，表示使用这些结构体是很不安全的，使用时要谨慎。对于上面几个结构体，这里做出如下说明：

#### <a id="211"></a>1. Raw
名称中含有 Raw 的表示指针指向的内存并没有被分配具体的数据类型。名称中不含 Raw 的表示指针指向的内存是有数据类型的。

```swift
let ptr = UnsafeMutablePointer<Int>.allocate(capacity: 1)
// 表示 ptr 指向一个内存地址，从这个地址开始，存放了一个 Int 类型的数据。

let rawPtr = UnsafeMutableRawPointer(bitPattern: 0x608000008FD0)
// 表示 rawPtr 指向一个内存地址，从这个地址开始存放的数据类型未知。
```

UnsafePointer 和 UnsafeRawPointer 的互相转化：

```swift
let ptr = UnsafePointer<Int>(bitPattern: 10)
let rawPtr = UnsafeRawPointer(aaa)
let ptrAgain = rawPtr.assumingMemoryBound(to: Int.self)
```

#### <a id="212"></a>2. Mutable
名称中带有 Mutable 的对应 Swift 中的 var ，不带 Mutable 的对应 let ，描述的是内存中的数据是否可变。例子如下：

```swift
let a = UnsafeMutablePointer<Int>.allocate(capacity: 1)
a.pointee = 40
a.pointee = 50
print(a.pointee)// 输出：50\n

let b = UnsafePointer<Int>(bitPattern: 0x608000008FD0)!
b.pointee = 20 // Error: Cannot assign to property:'pointee' is a get-only property
```

#### <a id="213"></a>3. Buffer
名称中含有 Buffer 的是用来沟通 Swift 的数组和指针。

```swift
let size = 10
let array = UnsafeMutablePointer<Int>.allocate(capacity: size)
for idx in 0..<10 {
    array.advanced(by: idx).pointee = idx
}
let buffer = UnsafeBufferPointer(start: array, count: size)
buffer.forEach({
    print("\($0)" // 输出 0～9
)})
array.deallocate(capacity: size)
```

不仅可以用指针访问数组，还可以从数组获取指针：

```swift
let array = [1, 2, 3, 4, 5, 6]
array.withUnsafeBufferPointer({ ptr in
    ptr.forEach({ print("\($0)") }) // 1, 2, 3... 
})
```

**更多的 Unsafe API 请参考官方文档。**

