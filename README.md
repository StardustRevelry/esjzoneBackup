# esjzoneBackup
备份esjzone上的小说

## 更新

1.8版本完善了站内链接检测逻辑，修复了有些链接跳过的bug。增加了下玩一本书无需退出，直接下载下一本的功能

更新
8-15 10:07

更新了闪退bug，增加了稳定性。

简化了使用，现在只要命令行直接运行save_the_whole_book.py就可以使用了。

![image](https://user-images.githubusercontent.com/65816600/129440723-dc54e5e2-dffe-41fc-be4f-9920f6ae8621.png)
## 使用方法：
### 单章节保存方法：
提醒：单章节保存应该只会在整书保存时部分章节保存失败时使用

下载single_chapter.py

url中填入对应章节的url 例：https://www.esjzone.cc/forum/----/----.html

file_path中填本地保存的地址（会自动创建文件夹）

！！！一定要把最后一行save_text前面的#去掉

### 整本书保存方法：
两个文件都要下载，因为会调用single_chapter里的函数

url中填入整合页面的url 例：https://www.esjzone.cc/detail/----.html

file_path中填本地保存的地址（会自动创建文件夹）

更新：start后面填从第几章开始下载

## 其他注意事项
关于繁简转换：在做了，已经新建文件夹了（笑）

有任何问题，b站私信我
https://space.bilibili.com/85266132
