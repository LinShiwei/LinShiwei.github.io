---
published: true
layout: post
title: Using Jekyll and GithubPages to build your own blog [macOS]
category: Tutorial
tags: 
  - jekyll
  - GithubPages
  - github
time: 2016.07.19 20:00:00
excerpt: GithubPages is now a easy way to build a website for you and your project. The code of your website is stored in the Github so it is convenient for you to edit and push your posts.Jekyll is a tool for building GithubPages, which is also simple and easy to understand.
---

<!-- lsw toc mark1. Do not remove this comment so that lsw_toc can update TOC correctly. -->

## Table of Contents
- [Introduction](#1)
- [Method](#2)
    - [Step One](#21)
    - [Step Two](#22)
    - [Step Three](#23)
    - [Step Four](#24)
- [Ending](#3)

<!-- lsw toc mark2. Do not remove this comment so that lsw_toc can update TOC correctly. -->

## <a id="1"></a>Introduction

[GithubPages](https://pages.github.com) is now a easy way to build a website for you and your project. The code of your website is stored in the Github so it is convenient for you to edit and push your posts.

[Jekyll](https://jekyllrb.com) is a tool for building GithubPages, which is also simple and easy to understand.

My blog, this website, is build using Jekll and GithubPages. You can get its original code from [here](https://github.com/LinShiwei/linshiwei.github.io).

Now let's strat building your own blog. The following guideline is in macOS environment.

## <a id="2"></a>Method

### <a id="21"></a>Step One

You should have an account in [Github](https://github.com) and create a new repository base on your github username. [Here](https://pages.github.com) is the guideline in GithubPages website. The name of your repository maybe `your-username.github.io`. Make sure the name is correct. Then in the repository's setting page: 

![image](https://raw.githubusercontent.com/LinShiwei/linshiwei.github.io/master/images/屏幕快照%202016-07-19%2012.31.55.png)

You can see:

![image](https://raw.githubusercontent.com/LinShiwei/linshiwei.github.io/master/images/屏幕快照%202016-07-19%2014.18.21.png)

Here you can launch automatic page generator to generate your site quickly. But in this circumstance you don't need to, because we are going to build website using jekyll.

After creating the repository, your should clone it to your mac. I suggest your using [Github Desktop](https://desktop.github.com) to do it. 

### <a id="22"></a>Step Two

In Terminal, using the following code to install jekyll:

```ruby
$ gem install jekyll
```

If your have enabled password in you mac. You may use this instead:

```ruby
$ sudo gem install jekyll
```

### <a id="23"></a>Step Three

After installing jekyll, you can download some jekyll template from [Jekyll Theme](http://jekyllthemes.org) and choose the one your like most. And copy all the files in the folder to the repository folder your create in Step One:

![image](https://raw.githubusercontent.com/LinShiwei/linshiwei.github.io/master/images/屏幕快照%202016-07-19%2013.22.32.png)

Now run Terminal in your repository folder:

```ruby
$ cd your repository folder
```

Run jekyll serve:

```ruby
$ jekyll serve
```

In this step, due to the template your choose, you may need to install some other jekyll gems. Just follow the guide in terminal.

After jekyll serve successfully, a website will run in `http://localhost:4000/` by default for developing.

### <a id="24"></a>Step Four

Until now, the blog has been built. You can commit the change to `master` of your repository and visit your blog at url such as `your-username.github.io`.

But this is not the end, it's time to add things to your blog.

Basically, to add a post to your blog, you can write a post in `Markdown` grammar and put it in the `_posts` folder in your repository:

![image](https://raw.githubusercontent.com/LinShiwei/linshiwei.github.io/master/images/屏幕快照%202016-07-19%2013.46.20.png)

For more information about the files and folders in a jekyll template, you can read documents [here](https://jekyllrb.com/docs/structure/).

## <a id="3"></a>Ending

There are lots of things you can do with the jekyll template such as adding google analytics, disqus supporting and so on. We will discuss them in the future posts. Here we just talk about the base of building a blog. It's easy only if your have done it. Hope you enjoy it.


