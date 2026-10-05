# 北京大学《具身智能导论》自学教程

这是一份写给具身智能初学者的中文自学教程。通过具体例子、逐页课件翻译和基础练习，逐步理解机器人如何感知、规划和行动。

## 来源与感谢

本教程基于北京大学2025春季《具身智能导论》（Introduction to Embodied AI）课程，使用 GitHub 项目 [zhuozhiyongde/Embodied-Artificial-Intelligence-2025Spring-PKU](https://github.com/zhuozhiyongde/Embodied-Artificial-Intelligence-2025Spring-PKU) 整理的课件、笔记与作业。课程信息见[北京大学课程官网](https://pku-epic.github.io/Intro2EAI_2025/)。

感谢课程负责人**王鹤老师**及授课、助教团队，感谢原始课件、笔记、作业及引用论文、图片、数据的作者，也感谢 **zhuozhiyongde** 与源项目贡献者的整理和分享。这些开放的学习材料，是本教程的基础。原始作者署名、引用与致谢随材料保留。

本项目由 **buildwithamy** 面向初学者整理，加入了十章学习路线、13讲946页课件的完整中文翻译、概念与公式讲解、自测题和基础代码练习，以及截至2026年10月4日的技术、政策与产业动态。

## 从这里开始

- [在线阅读教程](https://buildwithamy.github.io/pku-embodied-ai-self-study/)
- [下载完整 ZIP，离线阅读](https://github.com/buildwithamy/pku-embodied-ai-self-study/archive/refs/heads/main.zip)
- [学习与运行指南](学习与运行说明.html)

第一次阅读，可以从第1章开始。先看例子和图，再逐步理解公式，最后通过自测和代码检验理解。遇到不熟悉的数学概念时，沿着章内练习补齐基础。

| 章节 | 学习内容 |
| --- | --- |
| [第1章](ch01/index.html) | 具身智能导论与入门练习 |
| [第2章](ch02/index.html) | 刚体变换与坐标系 |
| [第3章](ch03/index.html) | 四元数与运动规划入门 |
| [第4章](ch04/index.html) | 运动规划与PID控制 |
| [第5章](ch05/index.html) | 抓取原理与旋转回归 |
| [第6章](ch06/index.html) | ICP配准与抓取稳定性 |
| [第7章](ch07/index.html) | 抓取检测与生成 |
| [第8章](ch08/index.html) | 模仿学习与行为克隆 |
| [第9章](ch09/index.html) | 强化学习与Actor-Critic |
| [第10章](ch10/index.html) | 机器人任务与前沿 |

## 对照课件

[13讲原课件与中文翻译](课件与中文译解.html)按原讲次和页号组织。每张英文课件下方都有完整译文，标题、条目、表格、公式与原页对应；概念解释和教学例子放在正文中。

[术语与符号](术语与符号.html)帮助查找常见英文缩写；[技术动态](技术动态_20261004.html)把新研究、政策和产业资料接回课程基础。

## 离线阅读与基础练习

下载 ZIP 并解压后，可以直接打开 `index.html`。Windows 上也可双击 `打开教程.cmd`，通过本地服务器阅读；需要已安装 Python 3，并保持服务器窗口开启。

```bash
git clone https://github.com/buildwithamy/pku-embodied-ai-self-study.git
cd pku-embodied-ai-self-study
python -m http.server 8000 --bind 127.0.0.1
```

浏览器访问 `http://127.0.0.1:8000/`。正文、图片、公式和原始PDF都保存在本地，适合离线阅读；外部论文、视频和依赖安装需要联网。

基础代码练习使用 Python 3.12，依赖版本记录在 `requirements-cpu.txt`：

```bash
python -m pip install -r requirements-cpu.txt
python ch01/homework01/warmup.py
```

第2—9章各有 `examples.py`。先用小规模CPU练习理解算法，再按课程作业说明准备完整的训练、仿真与评估环境。原作业保留学生实现部分，方便继续练习。

## 学习用途与许可

本项目用于个人学习与交流。源项目的 GPL-3.0 许可证，以及课件、图片、作业和第三方软件原有的署名与许可随资料保留，具体见[来源、致谢与许可](来源与许可.html)。

- [来源材料的固定版本](https://github.com/zhuozhiyongde/Embodied-Artificial-Intelligence-2025Spring-PKU/tree/0d6658dd1e87efd52cf505f5b8cb291b22a962a8)
- [原课件来源与SHA256](sources/课件来源.json)
- [原始笔记来源与SHA256](sources/笔记来源.json)
- [GPL-3.0许可证](LICENSE)
- [MathJax许可证](vendor/mathjax/LICENSE)
