原本由于原作者许久未更新版本了，因此我做了一点临时修改，目前最新版本0.8.10

0.8.1：修复了#1 sqlite3在windows下使用绝对路径的问题。这个修改已经被回滚。

0.8.4：修复了pip安装的报错。

0.8.7：修复了pip安装的报错，增加描述文件。

不过最近原作者的pypi上版本更新到0.8.1了，我合并了他的版本后发现我这边没什么特别要修改的了，因此pip安装的原版和我的修改版差别不大了，Windows路径的问题我已经回滚了，因为发现是用法的问题。

之前联系了作者没有响应，因此我自己也在pypi上创建了一个新的库，pypi地址：

    https://pypi.python.org/pypi/robotframework-databaseslibrary

github地址：

    https://github.com/qitaos/Robotframework-Database-Library/

github请在release页面下载最新的版本。

软件版权仍然属于原作者，我只是在原有database后面加了个s，方便大家用pip安装。

安装方法：

    pip install robotframework-databaseslibrary

Installation :

    pip install robotframework-databaseslibrary

原作者的databaselibrary地址： https://pypi.python.org/pypi/robotframework-databaseslibrary

Database Library contains utilities meant for Robot Framework’s usage. This can allow you to query your database after an action has been made to verify the results. This is compatible* with any Database API Specification 2.0 module.

