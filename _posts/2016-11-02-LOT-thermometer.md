---
published: true
layout: post
title: LOT|物联网 温度传感器 
category: Tutorial
tags: 
  - LOT
  - Arduino
time: 2016.11.02 09:22:00
excerpt: 前段时间从网上买了一个体重计，它自带了无线上网的功能，能够同步体重测量数据到网上。想到物联网已经有这么多产品了，于是就打算自己做一个物联网温度传感器。
---

# 前言

做一个物联网的设备，不管是体重计还是温度传感器等等，首先要清楚物体是怎么联网的。

其中一种方式是通过 Wi-Fi 模块进行连接。配备有 Wi-Fi 模块的设备，能够搜索附近的无线热点，通过 Wi-Fi 用户名和密码连接 Wi-Fi。但是如何让设备知道所要连接的 Wi-Fi 和密码呢？

具体的方法可以参考这里：[智能家居第一步： WiFi 设备怎么连上网](http://www.jianshu.com/p/a852d5ca6a44)。

由于我们要完成的是一个物联网温度传感器，我们选择一种相对简单、直接的方法：我们在程序里面直接设定好所要连接的 Wi-Fi 和密码，这样就能让传感器联网了。下面将会介绍具体的做法。

# 物联网温度传感器

物联网温度传感器分为两大部分。一是**传感器**，用于采集和发送温度数据；二是**远程服务器**，用于收集温度数据和根据请求返回温度数据。

## 传感器

对于传感器部分，需要一下材料：

1. ESP8266开发板（附带 Wi-Fi 模块和电源模块）;
2. DS18B20（温度传感器）;
3. 连接线（USB线、导线）、电脑;

### ESP8266

ESP8266是一个小型的 Wi-Fi 模块，能够建立 Wi-Fi 热点和连接 Wi-Fi 热点，并且能够配置 Web Client 或 Web Server 。它在我们这个温度传感器中的作用就是，作为一个 Web Client ，在通过 Wi-Fi 联网后，实时向远程服务器发送本地的（温度）数据。

ESP8266有很多个型号，从 ESP-01 到 ESP-12F 。ESP-01 是最初的版本，它上面可用的 GPIO 引脚较少，而 ESP-12F 具有全部 GPIO 引脚。由于 ESP8266 的额定电压是 3.3V，而 USB 的电压是 5V ，因此如果要单独使用 ESP8266 的话，就需要外接电源转化模块。

我们选用的是 **ESP-12E NodeMCU 开发板**：

![image](/images/ESP8266_mcu.png)

开发板上集成了电源模块，因此我们可以直接用 USB 给开发板供电，来使用 ESP8266，而不需要额外的电源模块。

开发板上附带有 CP2102（高度集成的 USB-UART 桥接器）因此我们只需要用一根 USB 线连接开发板与电脑，就能实现供电和下载程序。CP2102 在 Mac 和 PC 有相应的驱动程序，安装好驱动程序后，连接电脑，电脑就能识别出它的串口号。在接下去的烧写固件和下载程序都需要用到这个串口。

将开发板连上电脑后，接下去我们将烧写固件，并下载程序到 ESP8266 里。

#### 烧写固件，调试开发板

一、烧写固件

烧写固件（firmware）需要用到 [ESP8266Flasher](https://github.com/nodemcu/nodemcu-flasher)。

首先，从 [nodemcu-firmware](https://github.com/nodemcu/nodemcu-firmware) 选择合适的固件，如：`nodemcu_float_0.9.6-dev_20150704.bin` 。

然后打开 ESP8266，在 "Config" 页面选择需要烧写的固件：

![image](/images/ESP8266_flashConfig.png)

在 "Advanced" 页面设置好波特率，如：115200，一般这一页不需要修改。设置完成后，在 "Operation" 页面选择串口，点击 "Flash" 进行烧写。

![image](/images/ESP8266_flashOperation.png)
![image](/images/ESP8266_flashFlashing.png)

二、调试开发板

烧写完成后，我们需要验证固件是否烧写成功。关闭烧写程序，重新连接开发板与计算机，打开调试软件，推荐使用 Tera Term。

![image](/images/ESP8266_teratermConfig.png)

初次打开 TeraTerm 需进行简单配置，在 "Serial" 选择相应的串口，点击 "OK" 进入主界面，此时输入：

```lua
print("hello world")
```

得到相应如下：

![image](/images/ESP8266_teratermTest.png)

至此，烧写的固件已经运行在开发板中，下一步可以进行程序的编写和下载。

#### 用 Arduino 编程

> 在 Mac 和 PC 上都可以用 Arduino 为 ESP8166 编程。

一、配置 Arduino ESP8266 开发平台

ESP8266 里的程序是支持 Lua 语言的。但是直接写 Lua 程序，然后通过其他的软件把程序下载到开发板上，这个过程并不容易。因为相应的开发软件并不好用，比如 ESPlorer，luatool，Lualoader。因此，我们选用 Arduino 来进行编程。一是因为 Arduino 用的比较多，比较专业，二是因为 Arduino 软件做的比较精致，上手相对容易一些。

Arduino 是开源软件，下载安装完成后，在"Presences"->"Additional Board Manager URLs" 里填入 `http://arduino.esp8266.com/stable/package_esp8266com_index.json`

然后从 "Tools"->"Board"->"Boards Manager" 打开 Boards Manager。搜索并安装 ESP8266 开发平台。安装完成后，记得在 "Tools"->"Board" 菜单里选择和你开发板型号一致的开发平台。

对于 Arduino ESP8266 开发平台的配置还有疑问的话，可以参考 [esp8266/Arduino](https://github.com/esp8266/Arduino)。

二、下载测试程序

连接开发板与电脑，在 Arduino 里选择相应的串口。将以下程序下载到开发板中，记得修改程序中 Wi-Fi 的名称和密码：

```c++
// Import required libraries
#include "ESP8266WiFi.h"
// WiFi parameters
const char* ssid = "YourWifiName";
const char* password = "WifiPassword";
void setup(void)
{
// Start Serial
Serial.begin(9600);
Serial.print("Connecting");
// Connect to WiFi
WiFi.begin(ssid, password);
while (WiFi.status() != WL_CONNECTED) {
delay(500);
Serial.print(".");
}
Serial.println("");
Serial.println("WiFi connected");
// Print the IP address
Serial.println(WiFi.localIP());
}
void loop() {
}
```

下载完成后，程序会自动运行。打开 "Tools"->"Serial Monitor" 查看串口的状态。在串口监视器上，会显示 Wi-Fi 的连接情况，一旦连接成功，就会打印出 IP 地址。

到这一步，我们已经完成了开发板的调试和程序下载。接下去我们将把 DS18B20 与 ESP8266 结合，实时发送温度数据到远程服务器。

### DS18B20

DS18B20是常用的温度传感器，具有体积小，硬件开销低，抗干扰能力强，精度高的特点。

DS18B20 有三个管脚：GND、DQ、VDD。GND 接地，VDD 接 +3.3V，温度数据只靠 DQ 引脚传输。

我们选用的是带有上拉电阻的 DS18B20 模块，这样就不必自己外接上拉电阻。

![image](/images/ESP8266_ds18b20.png)

连线方式：

1. NodeMCU 开发板 3v3 -> DS18B20 VDD 
2. NodeMCU 开发板 D1  -> DS18B20 DQ
3. NodeMCU 开发板 GND -> DS18B20 GND

为了读取传感器上的温度数据，还需要在 Arduino 上安装 DallasTemperature 库。在 "Sketch" -> "Include Library" -> "Manage Libraries.." 中搜索 DallasTemperature 并安装。

## 远程服务器

### 方案一：ThingSpeak

物联网服务器可以选用现成的、也可以自己设计搭建。
提供物联网服务的有 [ThingSpeak](https://thingspeak.com)，它提供了多种强大的物联网 API ，能够满足各种需求。这里我们简单介绍一下使用 Thingspeak 的物联网方案。

首先需要在 ThingSpeak 上注册帐号，获取帐号的 API key。然后使用下面的程序（需要修改 API key 以及 Wi-Fi 名称和密码）：

```c++
#include <OneWire.h>
#include <ESP8266WiFi.h>
#include <ESP8266WebServer.h>
#include <DallasTemperature.h>

#define ONE_WIRE_BUS D1

const char* host = "api.thingspeak.com"; // Your domain
String ApiKey = "EWWXFA64H1U55QFZ";
String path = "/update?key=" + ApiKey + "&field1=";

OneWire oneWire(ONE_WIRE_BUS);
DallasTemperature DS18B20(&oneWire);

const char* ssid = "YourWifiName";
const char* pass = "WifiPassword";

char temperatureString[6];

void setup(void){
  Serial.begin(9600);
  Serial.println("");

  WiFi.begin(ssid, pass);
  // Wait for connection
  while (WiFi.status() != WL_CONNECTED) {
    delay(100);
    Serial.print(".");
  }

  Serial.println("");
  Serial.print("Connected to ");
  Serial.println(ssid);
  Serial.print("IP address: ");
  Serial.println(WiFi.localIP());

  DS18B20.begin();

}

float getTemperature() {
  float temp;
  do {
    DS18B20.requestTemperatures();
    temp = DS18B20.getTempCByIndex(0);
    delay(100);
  } while (temp == 85.0 || temp == (-127.0));
  return temp;
}

void loop() {

  float temperature = getTemperature();

  dtostrf(temperature, 2, 2, temperatureString);
  // send temperature to the serial console
  Serial.println(temperatureString);

  WiFiClient client;
  const int httpPort = 80;
  if (!client.connect(host, httpPort)) {
    Serial.println("connection failed");
    return;
  }

  client.print(String("GET ") + path + temperatureString + " HTTP/1.1\r\n" +
               "Host: " + host + "\r\n" +
               "Connection: keep-alive\r\n\r\n");
  delay(500);

}
```

程序下载到开发板后，运行时，就会自动读取传感器的温度并上传到 ThingSpeak 上。通过 ThingSpeak 上数据读取的 API，就能在任何一台联网的设备上获得传感器的实时温度数据。

### 方案二：自己搭建服务端

ThingSpeak 是现成的物联网服务，不使用它的话，我们如何自己搭建自己的物联网服务端呢？

物联网温度传感器的服务端主要由一下几个部分构成：

1. 服务器主机
2. 服务器程序
3. 后台数据库

一、服务器主机

对与主机的选择，我们选用的是云主机，在淘宝上就可以购买到，选择动态 IP 的云主机即可。

二、服务器程序

服务器程序可以使用 PHP 编写，[这里](https://github.com/LinShiwei/LswApacheServer)是我编写的温度传感器服务器程序。程序中的 host 默认是 `localhost`，可供本地调试使用，当配合云主机使用时，需要改成云主机的地址。

如果是在 Mac 上调试服务器程序，推荐使用 MAMP。

三、后台数据库

只有主机和程序还不够，还需要配置好后台服务器。淘宝上购买的云主机一般都配有 MySQL 数据库。在数据库中添加名为 `temperature` 的表。然后在表中添加以下字段：

![image](/images/ESP8266_database.png)

结合服务器程序，就能根据接收的请求，进行数据的存储与读取。

搭建完自己的服务端后，需要对上面的 Arduino 程序稍作修改，如下（需要修改 host 为自己的服务器地址或域名）：

```c++
#include <OneWire.h>
#include <ESP8266WiFi.h>
#include <ESP8266WebServer.h>
#include <DallasTemperature.h>

#define ONE_WIRE_BUS D1

const char* host = "YourDomain.com"; // Your domain
String key = "lsw";
String path = "/temperature.php?key=" + key + "&query=set&value=";

OneWire oneWire(ONE_WIRE_BUS);
DallasTemperature DS18B20(&oneWire);

const char* ssid = "test";
const char* pass = "149149149";

char temperatureString[6];

void setup(void){
  Serial.begin(9600);
  Serial.println("");
 
 boolean result = WiFi.softAP("ESPsoftAP_01", "lsw-soft-AP",1,true);
 WiFi.softAPdisconnect(true); 
  if(result == true){
    Serial.println("Ready");
  }else{
    Serial.println("Failed!");
  }
    
  WiFi.begin(ssid, pass);
  // Wait for connection
  while (WiFi.status() != WL_CONNECTED) {
    delay(100);
    Serial.print(".");
  }

  Serial.println("");
  Serial.print("Connected to ");
  Serial.println(ssid);
  Serial.print("IP address: ");
  Serial.println(WiFi.localIP());

  DS18B20.begin();

}

float getTemperature() {
  float temp;
  do {
    DS18B20.requestTemperatures();
    temp = DS18B20.getTempCByIndex(0);
    delay(100);
  } while (temp == 85.0 || temp == (-127.0));
  return temp;
}

void loop() {

  float temperature = getTemperature();

  dtostrf(temperature, 2, 2, temperatureString);
  // send temperature to the serial console
  Serial.println(temperatureString);

  WiFiClient client;
  const int httpPort = 80;
  if (!client.connect(host, httpPort)) {
    Serial.println("connection failed");
    return;
  }

  client.print(String("GET ") + path + temperatureString + " HTTP/1.1\r\n" +
               "Host: " + host + "\r\n" +
               "Connection: keep-alive\r\n\r\n");
  delay(500);

}
```

将程序下载到开发板中运行，就能实时发送温度数据到服务器上了。

**有任何疑问的话，欢迎在下方评论区讨论。**

