# 与蛇共舞，我的智能小蛇

#### 作品介绍

参加贪吃蛇魔改大赛作品，基于pgzero1.2中example的snake作品，结合百度AI人工智能平台中人体关键点分析，小蛇吃苹果，我来做运动，我与小蛇共舞。通过手的围绕身体进行转动，控制小蛇的运动方向。

#### 作品截图
![页面预览](https://gitee.com/shiranfei/Adapted-game-ai_snake/raw/master/pic/pic.jpg)

#### 作品效果

作品B站演示视频：https://www.bilibili.com/video/BV1iK4y1e7d1/


#### 软件架构
1.  贪吃蛇程序采用pgzero1.2中example的snake例程，

    pgzero1.2链接：https://github.com/lordmauve/pgzero

    pgzero的使用官方文档：https://pygame-zero.readthedocs.io/en/stable/

2.  百度AI人工智能平台人体关键点分析，使用史然飞的《中学生都能玩的人工智能》中对百度AI进一步封装库。

    参考链接：https://gitee.com/shiranfei/open_course_for_AI.git

    《中学生都能玩的人工智能》是史然飞（就是我啊）基于树莓派和百度AI定制的人工智能实验课，可以体验当前深度学习能完成的事情和其效果，基于开发平台的API，省略了模型建立和调参的复杂过程，可以快速、的制作智能产品，智能化我们的生活。

3.  程序由三大块组成：使用摄像头分析我们的姿态程序、标准贪吃蛇程序、音乐播放程序

    (1) 使用摄像头分析我们姿态的程序，读取摄像头的图片，然后发给百度AI进行分析，返回人体姿态，通过姿态信息里手臂、头部和肩膀的关系，得到方向控制键：上下左右，然后通过socke发送给标准贪吃蛇程序socket:127.0.0.1:20163。通过测试，发现在树莓派和PC上，百度AI的分析速度基本为2帧/秒。

    (2) 标准贪吃蛇程序，在pgzero1.2的snake基础上，新建了一个进程，完成从127.0.0.1:20163中读取人体姿态分析后的方向控制键，然后更新小蛇的运动方向。

    (3) 播放音乐程序，这个程序是后加的，发现当前在标准贪吃蛇程序中，调用music模块播放音乐有问题,当前未找出问题，所有采用折中方式，新建一个进程专门播放音乐。

4.  2020-07-19,当前版本程序，完成摄像头捕捉人体姿态，通过人体姿态完成对小蛇的控制，同时可以播放音乐

    后续待添加功能：

    (1)解决pgzero中运行music长时间播放异常的问题

    (2)添加滑动手臂，更换播放音乐的效果。

    (3)添加通过语音控制开始游戏和结束游戏。

    (4)项目退出问题，当前程序已后台运行，要退出需要手动kill 项目相关进程号，所以当前退出需要重新启动树莓派

#### 安装教程

1.  基于树莓派4B的安装教程

    (1) 安装系统镜像，镜像下载：

        链接：https://pan.baidu.com/s/14KYZl21Hyf3sjjcWxa5_bg、提取码：dbe5

        系统的详细安装视频：https://www.bilibili.com/video/BV1Q54y1i72T

    (2) fork本项目，点击桌面的终端，打开终端，在/home/pi中输入：

        git clone https://gitee.com/shiranfei/Adapted-game-ai_snake.git，即可获取项目

        进入/home/pi/Adapted-game-ai_snake目录下，输入：sh run_snake.sh，即可开始本项目的体验。

2.  基于PC机的安装教程

    (1) 我的PC机为ubuntu20.04(64位)，安装Anaconda3-2020.02-Linux-x86_64.sh

        在anaconda3中，安装opencv、pgzero、thonny、baidu-aip

        ubuntu系统中安装mplayer工具

    (2) fork本项目，点击桌面的终端，打开终端，在自己的目录下中输入：

        git clone https://gitee.com/shiranfei/Adapted-game-ai_snake.git，即可获取项目

        进入Adapted-game-ai_snake目录下，输入：sh run_snake.sh，即可开始本项目的体验。

#### 使用说明

1.  新建百度AI的人体分析应用，获取人体分析:AppID、API Key、Secret Key三个关键参数，更改camera_get_direct.py中的对应参数，例如我的参数为：

    "" 与蛇共舞的人体关键点分析，需要更改为自己的api接口 """

    pic_APP_ID = '21414508'

    pic_API_KEY = 'l5XEnXQePmookhlAM9ORkD8O'

    pic_SECRET_KEY = 'hwEuXHLja7U03Zfj1FkI08sNkLiy56QY'

    将程序中对应的参数，更换为您的即可。可以提高分析速度，如果好多人同时使用我的API体验时，百度API的分析速度会下降好多。

2.  运行程序，在树莓派和基于ubuntu的PC上，输入:sh run_snake.sh即可开始体验本项目

3.  控制小蛇变方向

    (1)小蛇向上走，双手合并，举过头顶，即可控制小蛇向上走

    (2)小蛇向左走，双手合并，在左肩的左边，即可控制小蛇向左转

    (3)小蛇向右走，双手合并，在右肩的右边，即可控制小蛇向右转

    (4)小蛇向下走，双手合并，在在肩部的下边，即可控制小蛇向下走

#### 参与贡献

1.  Fork 本仓库
2.  新建 develop分支
3.  提交代码
4.  新建 Pull Request

#### 码云特技

1.  使用 Readme\_XXX.md 来支持不同的语言，例如 Readme\_en.md, Readme\_zh.md
2.  码云官方博客 [blog.gitee.com](https://blog.gitee.com)
3.  你可以 [https://gitee.com/explore](https://gitee.com/explore) 这个地址来了解码云上的优秀开源项目
4.  [GVP](https://gitee.com/gvp) 全称是码云最有价值开源项目，是码云综合评定出的优秀开源项目
5.  码云官方提供的使用手册 [https://gitee.com/help](https://gitee.com/help)
6.  码云封面人物是一档用来展示码云会员风采的栏目 [https://gitee.com/gitee-stars/](https://gitee.com/gitee-stars/)
