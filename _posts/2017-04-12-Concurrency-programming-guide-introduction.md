---
published: true
layout: post
title: Apple：并发编程总览
category: Introduction
tags: 
  - iOS
  - Objective-C
  - NSOperation
  - GCD
  - KVO
  - macOS
time: 2017.04.12 09:22:00
excerpt: 本文参考 Apple 官方文档，从总体上介绍并发编程的相关内容，涉及 NSOperation 和 GCD。
---

<!-- lsw toc mark1. Do not remove this comment so that lsw_toc can update TOC correctly. -->

## Table of Contents
- [前言](#1)
- [GCD 与 Operation Queues](#2)
    - [Dispatch Queues](#21)
    - [Dispatch Sources](#22)
    - [Operation Queues](#23)
- [异步设计技术](#3)
    - [确定 App 要执行的任务](#31)
    - [弄清楚任务的执行步骤](#32)
    - [确定 Queue 的类型](#33)
    - [小技巧](#34)
- [其它并发技术](#4)
    - [OpenCL](#41)
    - [何时使用线程（Threads）](#42)

<!-- lsw toc mark2. Do not remove this comment so that lsw_toc can update TOC correctly. -->

## <a id="1"></a>前言

并发（Concurrency）指的是多个事件同时发生。当 App 有多个任务要完成时，把其中一部分放在其他线程（Thread）里能充分利用 CPU 资源。

对于早期的计算机，单位时间处理的任务量取决于 CPU 的时钟频率。但是随着技术的发展，单核 CPU 的时钟频率提升逐渐达到瓶颈。因此 CPU 开始采用多核心的设计，来提高性能。

让一个 App 使用多核心的传统方法是创建多个线程，但是手动操作和管理线程，难度很大，并且很难保证性能，如：线程的数目要适当，并且随着系统运行的状态进行调整。

为此 Apple 提供了以下几种负责处理多核、多线程的解决方案：

1. Grand Central Dispatch（GCD）；
2. Operation Queues；
3. OpenCL 等；

## <a id="2"></a>GCD 与 Operation Queues

首先我们对比一下 GCD 与 Operation Queues。

GCD 基于 C 语言，它提供了简洁的并发编程 API。

Operation Queues，在 Cocoa 里对应 NSOperation 和 NSOperationQuque，是 Objective-C 类。它实现了类似于 GCD 的功能。

Operation Queues 最先引入，但是到了 OS 10.6 和 iOS 4，NSOperationQueue 的内部代码就使用 GCD 实现了。也就是说，在最新的 OS X 和 iOS 系统里，NSOperation 其实就是使用了 GCD，但它并不是简单的调用 GCD，它还实现了一些复杂的方法。

### <a id="21"></a>Dispatch Queues

GCD 包含 Dispatch Queues 和 Dispatch Sources。

Dispatch Queues 的执行方式有两种：

1. Concurrent（并发，可以同时开始多个任务）；
2. Serial（串行，一个任务完成后才开始下一个任务）；

它们都是先入先出（FIFO），需要把执行的代码放到函数或 Block 里。

### <a id="22"></a>Dispatch Sources

Dispatch Sources 基于 C 语言，用于异步处理特殊类型的系统事件。当事件发生时，dispatch source 会封装一些系统事件的信息，通过函数或 Block 提交到 dispatch queue 里。几种系统事件的类型如下：

- Timers
- Signal handlers
- Descriptor-related events
- Process-related events
- Mach port events
- Custom events that you trigger

### <a id="23"></a>Operation Queues

Dispatch Queue 总是以 FIFO 的顺序执行，而 Operation Queue 可以通过设置参数，实现对执行顺序的控制。如：可以设定当一个任务完成后，才能执行下一个任务；可以构建复杂的执行图（Graph）。

提交给 Operation Queue 的任务是一个 NSOperation 的实例。NSOperation 本身是一个抽象的类，NSInvocationOperation 和 NSBlockOperation 继承自 NSOperation。因此，我们可以使用  NSInvocationOperation 和 NSBlockOperation 或使用自己创建的 NSOperation 子类来创建任务。

还有，由于 NSOperation 继承自 NSObject，且其对象会发出 KVO 消息。所以可以通过 KVO 来检测 Operation 的执行情况。

## <a id="3"></a>异步设计技术

使用 Concurrency 能充分利用多核心，让主线程关注于用户的操作，而把其他任务交给另外的线程。但是这会极大增加代码的复杂度，并且加大维护难度，因此要做出权衡。

### <a id="31"></a>确定 App 要执行的任务

进行异步设计，首先确定 App 要完成的任务，按优先级列出，并考虑它们之间的关系。

### <a id="32"></a>弄清楚任务的执行步骤

考虑任务的每一步（Unit），分析是否能通过多线程优化，以及能得到多大的性能提升。在不熟悉 NSThread（更底层的线程操作类） 的情况下，使用 queue 可能会比使用 NSThread 效果更好。

### <a id="33"></a>确定 Queue 的类型

把任务分成各个步骤（Unit）后，把它们放到 Block 或 Operation Object 里，确定它们的执行顺序。

1. 若使用 Block，考虑添加到 Serial dispatch queue 或 Concurrency dispatch queue。
2. 若使用 Operation Objects，queue 的选择相比 operation object 的设置就不那么重要了。主要设置好各个 object 之间的关系。

### <a id="34"></a>小技巧

1. 考虑直接在进行的任务中求值，而不用回到主线程获取数值。由于线程的切换会有额外的开销，应避免频繁切换线程；
2. 尽早确定顺序执行的任务（serial tasks）；
3. 避免使用锁（lock）；
4. 尽量使用系统框架。

## <a id="4"></a>其它并发技术

### <a id="41"></a>OpenCL

[OpenCL](https://developer.apple.com/library/content/documentation/Performance/Conceptual/OpenCL_MacProgGuide/Introduction/Introduction.html#//apple_ref/doc/uid/TP40008312)（Open Computing Language）是 OS X 上的一个并发技术，用于使用 GPU 进行数值计算。如：利用 GPU 对一张图片中的每个像素点进行处理，计算出处理后的数值。

需要注意的是，使用 OpenCL 是有一定额外开销的，把数据传入 GPU 和从 GPU 获取结果数据都需要时间，因此不能滥用 OpenCL。

### <a id="42"></a>何时使用线程（Threads）

虽然 Operation Queues 和 Dispatch Queues 在处理并发任务上很适用，但是它们并不是万能的。根据实际的情况，有时需要手动创建线程，这样能对线程有更精确的控制。关于线程的使用，请参考 [Threading Programming Guide](https://developer.apple.com/library/content/documentation/Cocoa/Conceptual/Multithreading/Introduction/Introduction.html#//apple_ref/doc/uid/10000057i)。

**参考：[Concurrency Programming Guide](https://developer.apple.com/library/content/documentation/General/Conceptual/ConcurrencyProgrammingGuide/Introduction/Introduction.html#//apple_ref/doc/uid/TP40008091-CH1-SW1)**。

**有任何疑问的话，欢迎在下方评论区讨论。**

