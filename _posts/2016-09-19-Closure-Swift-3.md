---
published: true
layout: post
title: Swift 3.0 ：理解 Closure 
tags: 
  - swift
  - iOS
time: 2016.09.19 19:22:00
excerpt: Closure 是一个函数块，在 Swift 3.0 的官方文档里有详细的说明。从 Swift 2.3 到 Swift 3.0 ，Closure 也有了一些变化。本文主要通过一些例子，谈谈自己的理解。
---

## 前言

Closure 是一个函数块，在 [Swift 3.0 的官方文档](https://developer.apple.com/library/content/documentation/Swift/Conceptual/Swift_Programming_Language/Closures.html#//apple_ref/doc/uid/TP40014097-CH11-ID94)里有详细的说明。从 Swift 2.3 到 Swift 3.0 ，Closure 也有了一些变化。本文主要通过一些例子，谈谈自己的理解。

## Closure 的表达形式

Closure 其实就是一段函数。当一个函数的使用范围比较小，没有必要为它进行明确的冗长的声明，这时候，就可以用 Closure 来实现这个函数的功能，使代码更加紧凑，清晰。

### 排序函数

在官方文档里，通过 `sorted(by:)` 函数来描述 Closure 的运作过程，一个 closure 作为 `sorted(by:)` 的参数传入，最终达到利用这个 closure 排序进行的目的。但是 `sorted(by:)` 函数具体的实现并没有给出，因此，对于初学者来说，并不清楚 `sorted(by:)` 函数对 closure 做了什么。在这里就通过自己的一个例子来说明，Closure 到底是怎么运作的。

下面为 `Array` 类自定义了一个排序函数，这个函数以一个函数（或者 closure ）为参数，最终返回一组元素。参数列表里的函数需要有两个参数，并返回 `Bool` 值。

```swift
extension Array{
    func mySort(clo:(_ s1: String, _ s2: String)-> Bool)-> [Element]{
        var tempArray = self
        for i in 0...tempArray.count - 1{
            for j in i...tempArray.count - 1{
                if closure(tempArray[i] as! String, tempArray[j] as! String){
                    let temp = tempArray[i]
                    tempArray[i] = tempArray[j]
                    tempArray[j] = temp
                }
            }
        }
        
        return tempArray
    }
}
```

上面这段代码大致模拟了 closure 在函数里的使用过程。在这个函数中，通过调用参数表里的 clo 函数，利用 clo 函数返回的值对数组元素进行操作，最后返回一组元素。

在函数外，我们可以明确地定义一个比较函数：

```swift
func numSort(n1:String, n2:String)->Bool{
    return n1<n2
}
```

这样我们就能把这个比较函数 `numSort:` 传入排序函数 `mySort(clo:)` ：

```swift
let num = ["a","b","c","d"]
let number = num.mySort(clo: numSort)
// number is equal to ["d", "c", "b", "a"].
```

在上面这段代码中，`mySort(clo:)` 函数被传入了一个函数作为参数。因此，在完成这个排序功能时，需要额外定义一个比较函数，然后作为参数传入。对与比较函数这样短小的函数，额外的定义显得有些繁琐，不够简练，因此 Swift 提供了 Closure 来简化这个过程：

```swift
let numberb = num1.mySort{
    (a,b)->Bool in
    return a<b
}
// numberb is equal to number above.
```

上面这段代码利用了一个简单的 closure 替换了之前的比较函数，同样实现了排序的功能。在这种情况下，就不需要额外定义比较函数了。

> 需要注意的是，当 closure 作为函数的最后一个参数时，在调用函数时，可以省去小括号，并把 closure 写在外面。官方文档里称之为 `Trailing Closures` 。

上面的例子展示了从函数到 closure 的替换，对于 closure 的表达还能进行简化，直到：

```swift
let numberc = num.mySort(clo:<)
// numberc is equal to number and numberb above.
```

具体的简化过程及解释请参考官方文档。

## @autoclosure 和 @escaping

`@autoclosure` 和 `@escaping` 可以用来标记 closure 参数的类型。

> **New in Xcode 8 beta – Swift and Apple LLVM Compilers: Swift Language**
>
> The @noescape and @autoclosure attributes must now be written before the parameter type instead of before the parameter name. [SE-0049]

> **Swift 3: closure parameters attributes are now applied to the parameter type, and not the parameter itself**

注意，这里指的是标记参数的类型，在 Swift 3 之前，它们是用来标记参数的。

用 `@autoclosure` 标记 clousre 参数的类型后，在函数调用的时候就可以去掉 closure 的花括号，把 closure 以其返回值的形式传入函数中，以下是不带 `@autoclosure` 和带 `@autoclosure` 的参数类型及其使用：

```swift
// customersInLine is ["Alex", "Ewa", "Barry", "Daniella"]
func serve(customer customerProvider: () -> String) {
    print("Now serving \(customerProvider())!")
}
serve(customer: { customersInLine.remove(at: 0) } )
// Prints "Now serving Alex!”

// 摘录来自: Apple Inc. “The Swift Programming Language (Swift 3)”。 iBooks. 
```

```swift
// customersInLine is ["Ewa", "Barry", "Daniella"]
func serve(customer customerProvider: @autoclosure () -> String) {
    print("Now serving \(customerProvider())!")
}
serve(customer: customersInLine.remove(at: 0))
// Prints "Now serving Ewa!”

// 摘录来自: Apple Inc. “The Swift Programming Language (Swift 3)”。 iBooks. 
```

`@escaping` 标记在 Swift 3 之前是没有的，在 Swift 2.3 中，只有 `@noescaping` 。

>**New in Xcode 8 beta 6 - Swift Compiler: Swift Language**
>
>Closure parameters are non-escaping by default, rather than explicitly being annotated with @noescape. Use @escaping to indicate that a closure parameter may escape. @autoclosure(escaping) is now written as  @autoclosure @escaping. The annotations @noescape and  @autoclosure(escaping) are deprecated. (SE-0103)

也就是说，现在 closure 作为函数的参数，默认是 @noescaping 类型的。

`@escaping` 标记表示 closure 可以在函数运行结束后再执行，而 `@noescaping` 标记表示 closure 必须在函数运行结束前执行。一个常见的例子是常见的 completion handle ，它们在函数运行完成后才执行：

```swift
class func animate(withDuration duration: TimeInterval, animations: () -> Void, completion: ((Bool) -> Void)? = nil)
```

需要注意的是，当 closure 的类型用 `@escaping` 标记之后，在 closure 内使用类的属性或方法时，需要用 `self` 标明。

```swift
func someFunctionWithNonescapingClosure(closure: () -> Void) {
    closure()
}
 
class SomeClass {
    var x = 10
    func doSomething() {
        someFunctionWithEscapingClosure { self.x = 100 }
        someFunctionWithNonescapingClosure { x = 200 }
    }
}

// 摘录来自: Apple Inc. “The Swift Programming Language (Swift 3)”。 iBooks. 
```

## Closure playground

关于 Closure ，[这里](https://github.com/LinShiwei/linshiwei.github.io/tree/master/lsw_codesource)有一个 Swift playground ，里面有一些例子可以参考。

