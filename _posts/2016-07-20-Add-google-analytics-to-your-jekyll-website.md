---
published: true
layout: post
title: Add google analytics to your jekyll website 
category: Tutorial
tags: 
  - jekyll
  - GithubPages
time: 2016.07.20 20:00:00
excerpt: Google Analytics is a freemium web analytics service offered by Google that tracks and reports website traffic.In this post, we are going to add goole analytics to a jekyll website.
---
<!-- lsw toc mark1. Do not remove this comment so that lsw_toc can update TOC correctly. -->

## Table of Contents
- [Introduction](#introduction)
- [Method](#method)
    - [Step One](#step-one)
    - [Step Two](#step-two)
    - [Step Three](#step-three)
    - [Step Four](#step-four)
    - [Final Step](#final-step)
- [Ending](#ending)

<!-- lsw toc mark2. Do not remove this comment so that lsw_toc can update TOC correctly. -->

## Introduction

Google Analytics is a freemium web analytics service offered by Google that tracks and reports website traffic. You can visit [here](https://en.wikipedia.org/wiki/Google_Analytics) for more information.

In this post, we are going to add goole analytics to a jekyll website. [This blog](http://linshiwei.github.io) is an example website, having contained google analytics code already.

## Method

### Step One

To add google analytics, you should visit [google analytics](https://www.google.com/intl/en_uk/analytics/#?modal_active=none) website and sign up a google account: 

![image](https://raw.githubusercontent.com/LinShiwei/linshiwei.github.io/master/images/屏幕快照 2016-07-20 09.24.04.png)

![image](https://raw.githubusercontent.com/LinShiwei/linshiwei.github.io/master/images/屏幕快照 2016-07-20 09.26.22.png)

For Chinese version, you can visit [here](https://www.google.com/intl/zh-CN/analytics/). If you have had a google account, you can log in and go to next step.


### Step Two

After you have a google account and log in google analytics website, you need to follow the guide to register for google analytics.

Choose `website` in this page:

![image](https://raw.githubusercontent.com/LinShiwei/linshiwei.github.io/master/images/屏幕快照 2016-07-20 09.28.39.png)

Fill in website name and website url. Select one industry category.

Then click `Get Tracking ID`.

Now in your google analytics page, you will get a track ID such as `UA-80935640-1` and some code for website tracking: 

![image](https://raw.githubusercontent.com/LinShiwei/linshiwei.github.io/master/images/屏幕快照 2016-07-20 09.30.07.png)

### Step Three

Copy the tracking code, create a `google-analytics.html` file in your jekyll website's `_includes` folder:

![image](https://raw.githubusercontent.com/LinShiwei/linshiwei.github.io/master/images/屏幕快照 2016-07-19 23.19.11.png)

Put the code in this `.html` file:

![image](https://raw.githubusercontent.com/LinShiwei/linshiwei.github.io/master/images/屏幕快照 2016-07-20 09.32.53.png)

### Step Four

After creating `google-analytics.html` with tracking code from google analytics website, you can open the `footer.html` file in `_include` folder and add  `include google-analytics.html` in it like the following:

![image](https://raw.githubusercontent.com/LinShiwei/linshiwei.github.io/master/images/屏幕快照 2016-07-19 23.16.44.png)

This step will simply add analytics code to all pages in your website, which helps google to analyse.

### Final Step

We have added analytics code to website step by step. Now in Terminal of your website folder,let's run:

```ruby
$ jekyll build
```

After that, you can preview your website at `http://localhost:4000` by running:

```ruby
$ jekyll serve
```

## Ending

If you use github to manage your website code, you can use github desktop to commit changes to `master`. The google analytics will work in no time. You can see the analytics report in your google analytics page.

By the way, if you want to know how to build your own blog in Github, [here](http://linshiwei.github.io/2016/Using-Jekyll-and-Github-Pages-to-build-your-own-blog-macOS) is another post for you.


