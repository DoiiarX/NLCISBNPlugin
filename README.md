# 🏠中国国家图书馆ISBN Calibre Metadata 源插件

该项目是一个用于 [Calibre](https://calibre-ebook.com/) 电子书管理软件的元数据源插件，旨在从[中国国家图书馆](http://opac.nlc.cn/F)获取图书信息，特别是基于ISBN。此插件允许用户轻松地将图书信息添加到其Calibre库中，包括书名、作者、出版日期、中图分类号等重要信息。

**(交流反馈QQ群：491088665)**


<p align="center">
	<a href="https://github.com/DoiiarX/NLCISBNPlugin/stargazers" target="_blank"><img src="https://img.shields.io/github/stars/DoiiarX/NLCISBNPlugin.svg"></a>
	<a href="https://github.com/DoiiarX/NLCISBNPlugin/network/members" target="_blank"><img src="https://img.shields.io/github/forks/DoiiarX/NLCISBNPlugin.svg"></a>
</p>
<p align="center">
	<a href="https://github.com/DoiiarX" target="_blank"><img src="https://img.shields.io/badge/Author-DoiiarX-NLCISBNPlugin.svg"></a>
	<a href="https://github.com/DoiiarX/NLCISBNPlugin/issues" target="_blank"><img src="https://img.shields.io/github/issues/DoiiarX/NLCISBNPlugin.svg"></a>
	<a href="https://github.com/DoiiarX/NLCISBNPlugin/issues?q=is%3Aissue+is%3Aclosed" target="_blank"><img src="https://img.shields.io/github/issues-closed/DoiiarX/NLCISBNPlugin.svg"></a>
	<a href="https://github.com/DoiiarX/NLCISBNPlugin/pulls" target="_blank"><img src="https://img.shields.io/github/issues-pr/DoiiarX/NLCISBNPlugin.svg"></a>
	<a href="https://github.com/DoiiarX/NLCISBNPlugin/pulls?q=is%3Apr+is%3Aclosed" target="_blank"><img src="https://img.shields.io/github/issues-pr-closed/DoiiarX/NLCISBNPlugin.svg"></a>
	<a href="https://github.com/DoiiarX/NLCISBNPlugin" target="_blank"><img src="https://img.shields.io/github/last-commit/DoiiarX/NLCISBNPlugin.svg"></a>
	<a href="https://img.shields.io/github/contributors/DoiiarX/NLCISBNPlugin"><img src="https://img.shields.io/github/contributors/DoiiarX/NLCISBNPlugin" alt="贡献者"></a>
</p>
<p align="center">
	<a href="https://github.com/DoiiarX/NLCISBNPlugin/releases" target="_blank"><img src="https://img.shields.io/github/release-pre/DoiiarX/NLCISBNPlugin"></a>
	<a href="https://img.shields.io/github/repo-size/DoiiarX/NLCISBNPlugin"><img src="https://img.shields.io/github/repo-size/DoiiarX/NLCISBNPlugin" alt="文件大小"></a>
	<a href="https://github.com/DoiiarX/NLCISBNPlugin/releases" target="_blank"><img src="https://img.shields.io/github/downloads/DoiiarX/NLCISBNPlugin/total"></a>
	<a href="https://deepscan.io/dashboard#view=project&tid=22929&pid=26210&bid=830826"><img src="https://deepscan.io/api/teams/22929/projects/26210/branches/830826/badge/grade.svg" alt="DeepScan grade"></a>
	
</p>



## 🔍功能特点

- **自动元数据检索**：通过ISBN，自动从中国国家图书馆获取图书元数据。
- **支持中图分类号**：目前唯一能获取中图分类号的Calibre插件。
- **通过标题模糊搜索ISBN号**：通过标题，自动从中国国家图书馆获取ISBN号。
- **自定义并发数**：用户可自定义的并发数。
- **自定义结果上限**：用户可自定义模糊搜索时，返回结果的上限。

## 🌟返回结果示例
![image](https://github.com/DoiiarX/NLCISBNPlugin/assets/25550075/e6906459-0457-4c8c-a872-d7eda2d8beff)

**返回项目包括：**
- 书名
- 标签
- 作者
- 简介
- 出版社

其中，标签由**分类**、**图书馆分类号**、**出版年份**组成

## ✅待办事项

以下是我们计划在未来添加到插件中的功能：

- [ ] **更好的标题处理**：更好的标题处理。
- [ ] **更好的并发优化**：更好的并发优化，减少被封IP的几率并且增加获取效率。
- [ ] **模糊搜索**：根据isbn搜索isbn相同的多本书籍。

## ❤ 赞助 Donation
如果你觉得本项目对你有帮助，请考虑赞助本项目，以激励我投入更多的时间进行维护与开发。

If you find this project helpful, please consider supporting the project going forward. Your support is greatly appreciated.


![Donation](https://github.com/DoiiarX/NLCISBNPlugin/assets/25550075/fe7815a3-d209-4871-938d-dca7af7f67cb)

**你的`star`或者`赞助`是我长期维护此项目的动力所在，由衷感谢每一位支持者，“每一次你花的钱都是在为你想要的世界投票”。 
另外，将本项目推荐给更多的人，也是一种支持的方式，用的人越多更新的动力越足。**

## 👤游客访问
<p align="center"> 
   <img alingn="center" src="https://profile-counter.glitch.me/NLCISBNPlugin/count.svg"  alt="NLCISBNPlugin"/>
</p>

## 🔧安装

1. 在 [Calibre官方网站](https://calibre-ebook.com/) 上下载并安装Calibre。

2. 下载最新版本的 `NLCISBNPlugin` 插件文件。

3. 打开Calibre软件，点击 "首选项" > "插件"。

4. 在插件界面中，点击 "加载插件从文件中" 按钮，选择之前下载的插件zip文件。

5. 安装完成后，启用该插件。

## 📘使用

1. 打开Calibre软件。

2. 选择您想要更新元数据的电子书。

3. 右键单击所选电子书，然后选择 "编辑元数据"。

4. 在 "元数据编辑器" 窗口中，点击 "下载元数据"。

5. 插件将自动从中国国家图书馆检索并填充图书信息。

6. 确认信息无误后，点击 "确定" 保存更新的元数据。

## ⚠️可能遇到的麻烦
1. [无法安装插件。报错 It does not contain a top-level init.py file](https://github.com/DoiiarX/NLCISBNPlugin/issues/1)
2. [当单一isbn对应多本书籍时，无法下载元数据](https://github.com/DoiiarX/NLCISBNPlugin/issues/4)

## 🤝贡献

如果您发现任何问题或想要改进这个插件，欢迎贡献您的代码。请按照以下步骤进行：

1. Fork 该仓库。

2. 创建一个新的分支，以进行您的改进。

3. 提交您的更改并创建一个拉取请求（Pull Request）。

4. 我们将会审查您的代码并与您合作以将改进合并到主分支。

## 📜许可证

这个项目基于 [Apache 许可证 2.0](LICENSE) 开源，因此您可以自由使用、修改和分发它。

## 💬 感谢

感谢您对中国国家图书馆ISBN Calibre Metadata 源插件的兴趣和支持！如果您有任何问题或建议，欢迎在 GitHub 上的问题部分提出。

## 📊Star History

[![Star History Chart](https://api.star-history.com/svg?repos=DoiiarX/NLCISBNPlugin&type=Date)](https://star-history.com/#DoiiarX/NLCISBNPlugin&Date)

