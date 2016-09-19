//: Playground - noun: a place where people can play

import UIKit

var str = "Hello, playground"

func backward(_ s1: String, _ s2: String)-> Bool{
    return s1 > s2
}

let names = ["aaa","bbb","ccc"]

var reverseNames = names.sorted(by:backward)

extension Array{
    mutating func mySort1(clo:(_ s1: String, _ s2: String)-> Bool)-> [Element]{
        for i in 0...self.count - 1{
            for j in i...self.count - 1{
                if clo(self[i] as! String, self[j] as! String){
                    let temp = self[i]
                    self[i] = self[j]
                    self[j] = temp
                }
            }
        }
        
        return self
    }
    
    func mySort(clo:(_ s1: String, _ s2: String)-> Bool)-> [Element]{
        var tempArray = self
        for i in 0...tempArray.count - 1{
            for j in i...tempArray.count - 1{
                if clo(tempArray[i] as! String, tempArray[j] as! String){
                    let temp = tempArray[i]
                    tempArray[i] = tempArray[j]
                    tempArray[j] = temp
                }
            }
        }
        
        return tempArray
    }
}

func numSort(n1:String, n2:String)->Bool{
    return n1<n2
}

var num1 = ["a","b","c","d"]
let number1 = num1.mySort1(clo: numSort)

let num = ["a","b","c","d"]
let number = num.mySort(clo: numSort)

let numberb = num.mySort{
    (a,b)->Bool in
    return a<b
}
numberb

let numbera = num.mySort{$0<$1}
numbera
let numberc = num.mySort(clo:<)
numberc


