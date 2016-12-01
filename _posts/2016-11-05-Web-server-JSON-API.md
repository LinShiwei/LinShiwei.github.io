---
published: true
layout: post
title: PHP: 构建 JSON 数据接口的 Web 服务器
category: Tutorial
tags: 
  - PHP
  - JSON
  - Web server
time: 2016.11.05 09:22:00
excerpt: 在应用开发的过程中，涉及网络，常常就需要通过一些 HTTP 请求从网上获取数据。很多网络服务器（Web server）提供了 URL 类型的 API，通过访问特定的 URL，就能从服务器返回数据。本文将用一个简单的例子，介绍这种服务器程序的构建。
---

# 前言

在网上，有很多服务商提供了数据的API（Application Programming Interface），这些 API 可以是 URL 形式的，如下：

http://api.openweathermap.org/data/2.5/weather?q=London,uk&appid=b1b15e88fa797225412429c1c50c122a1

在浏览器访问上面这个链接，服务器就会返回数据。返回的数据类型有很多种，如：JSON，XML等。

本文旨在通过一个例子简要介绍这种服务器程序的构建，最终完成一个服务器程序，实现通过 URL 与服务器通信，服务器返回 JSON 格式的数据。

# 问题及需求分析

## API 

观察上面的 URL，我们可以发现它可以分为两个部分。

一是主机地址：`http://api.openweathermap.org/data/2.5/weather`。

二是参数：`q=London,uk&appid=b1b15e88fa797225412429c1c50c122a1`。

主机地址和参数之间用 `?` 隔开。参数又可以分为多个独立的参数。在这个 URL 中，共包含了两个参数，分别是 `q` 和 `appid`，等号后面是参数的值。

我们要做的是一个**物联网温度传感器的后台服务器**，即根据不同的 URL，返回温度数据或储存温度数据。

假设我们的 API 如下：

```
获取最近的一个温度数据 API：
http://localhost:8888/temperature.php?key=lsw&query=get
返回示例（JSON）：
成功：{"status":true,"date":"2016-11-17 19:13:09","value":32.63}
失败：{"status”:false,”message”:”*"}
备注：”value” 的数据类型是 double

上传一个温度数据 API：
http://localhost:8888/temperature.php?key=lsw&query=set&value=27.1
返回示例（JSON）：
成功：{"status":true,"message":"setting success"}
失败：{"status”:false,”message”:”*"}
```

URL 中的 temperature.php 就是我们即将编写的网页文件。key 和 query 是两个参数，在 query=set 时，还应带有 value 参数。返回的数据类型是 JSON，以 status 标志操作是否成功，以及附带有信息或数据。

## JSON 数据

>**[JSON](http://baike.baidu.com/link?url=vAIdH3CjSpssVA3Xh3KoBWFTjfdNwGcL9eD7QspsbyDdLPMq76QYBM0I61VUj2aomAJlJyFqoXRo8HVG6qwl-K)**(JavaScript Object Notation) 是一种轻量级的数据交换格式。它基于ECMAScript的一个子集。 JSON采用完全独立于语言的文本格式，但是也使用了类似于C语言家族的习惯（包括C、C++、C#、Java、JavaScript、Perl、Python等）。这些特性使JSON成为理想的数据交换语言。 易于人阅读和编写，同时也易于机器解析和生成(一般用于提升网络传输速率)。

JSON 数据是可以带有数据类型的，如上面返回示例中的 value 是一个 double 类型的数据。

# 实现
## 本地服务器开发环境：MAMP

[MAMP](https://www.mamp.info/en/) 是经典本地服务器环境的 Mac OS 软件。MAMP 这几个首字母代表苹果的 Mac OS 系统上的 Macintosh、Apache、MySQL 和 PHP。在 Windows 系统上也有相应的开发环境，WAMP。这里以 MAMP 为例进行说明。

MAMP 分免费版和专业版，我们目前只需要用到免费版。安装完成后运行，点击 Start Servers 就可以运行本地的服务器。默认的本地服务器地址是：`http://localhost:8888`。

在 MAMP 的 Preferences.. -> Web Server -> Document Foot 可以定位到服务器源文件目录。服务器的程序就保存在这个目录里。


## 后台数据库 MySQL

为了存储数据，服务器需要有一个数据库，并实现与数据库之间的通信。首先我们用 MAMP 运行本地的服务器，在打开的导航网页中打开数据库的管理页面。

![MySQL](/images/JSONWebServer_mysql.png)

新建一个名为 `temperatureData` 的数据库，再新建一个数据表 `temperature`，并添加如下字段：

![数据表](/images/JSONWebServer_table.png)

这样就完成了数据库的配置，目前只需要储存温度信心，因此只配置这几个条目。

## 服务器程序

有了数据库，接下来就要写服务器程序了。服务器程序需要完成以下几个部分的内容：

1. 连接数据库，与数据库通信，实现数据的读取与存储。
2. 获取 URL 中的参数，根据不同的参数和参数值执行相应的操作。
3. 封装要返回的信息，以 JSON 形式返回。

具体的程序如下，在关键的地方以注释的方式进行说明。

```php
<?php
    //函数：用于把数据封装为 JSON 格式
    function echoJSON($withStatus,$andMessage){
        $data = array('status' => $withStatus, 'message' => $andMessage);
        $jsonstring = json_encode($data);
        header('Content-Type: application/json');
        echo $jsonstring;
    }
    // 配置数据库
    $user = 'root';
    $password = 'root';
    $db = 'temperatureData';
    $host = 'localhost';
    $port = 8889;
    $link = mysqli_init();
    $success = mysqli_real_connect(
                                   $link,
                                   $host,
                                   $user,
                                   $password,
                                   $db,
                                   $port
                                   );
    $privateKey = "lsw";
    if($success){
    //与数据库连接成功后，获取 URL 中的参数值，根据参数执行相应的程序。如：$_GET["key"] 用于获取 URL 中 "key" 的参数值。
        $key = $_GET["key"];
        if($key == $privateKey){
            $query = $_GET["query"];
            switch ($query){
                case "get":
                    $result = mysqli_query($link,"SELECT * FROM `Temperature`");
                    $row = mysqli_fetch_array($result);
                    
                    $data = array('status' => true, 'date' => $row["Date"], 'value' => (double)$row["Value"]);
                    $jsonstring = json_encode($data);
                    header('Content-Type: application/json');
                    echo $jsonstring;
                    break;
                case "set":
                    $value = $_GET["value"];
                    $valueDouble = (double)$value;
                    if($valueDouble){
                        mysqli_query($link,"DELETE FROM `Temperature` WHERE 1");
                        mysqli_query($link,"INSERT INTO `Temperature`(`Date`, `Value`) VALUES (CURRENT_TIMESTAMP,$valueDouble);");
                        $data = array('status' => true, 'message' => 'setting success');
                        $jsonstring = json_encode($data);
                        header('Content-Type: application/json');
                        echo $jsonstring;
                    }else{
                        echoJSON(false,"invalid value");
                    }
                    break;
                default:
                    echoJSON(false,"unsupported query");
            }
        }else{
            echoJSON(false,"invalid key");
        }
    }else{
        echoJSON(false,"Connect Error: " . mysqli_connect_error());
    }
    // 关闭数据库连接。
    mysqli_close($link);
?>
```

在服务器目录里新建一个 `temperature.php` 文件，将上述程序复制到文件中保存。用 MAMP 运行服务器，下面将检验我们服务器的配置情况。

在浏览器中访问：http://localhost:8888/temperature.php?key=lsw&query=get 就能获取数据库中的温度信息。如果数据库中还没有温度信息，则会返回如下结果：

```php
{"status":true,"date":null,"value":0}
```

在浏览器中显示如下：

![JSON](/images/JSONWebServer_json.png)

完整的程序请看[这里](https://github.com/LinShiwei/LswApacheServer/blob/master/temperature.php)。

关于如何使用这个 Web 服务器完成物联网温度传感器，请参考：[LOT|物联网 温度传感器](http://linshiwei.site/tutorial/2016/11/02/LOT-thermometer)。

**有任何疑问的话，欢迎在下方评论区讨论。**

