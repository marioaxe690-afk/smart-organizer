# 🗂️ Smart Organizer - 智能文件分类整理工具

一个优雅的 Python 桌面文件自动化整理脚本，能够智能识别文件类型并自动分类到对应文件夹。

## ✨ 特性

- 🎯 **智能分类**：基于文件名关键词和扩展名的双重识别机制
- 🛡️ **安全可靠**：默认测试模���，跳过系统文件和危险文件类型
- 📊 **详细报告**：提供完整的扫描统计和分类计划预览
- ⚡ **高效处理**：支持文件和文件夹的批量整理
- 🔄 **智能重命名**：自动处理同名文件冲突（添加时间戳）

## 📁 分类体系

工具会自动将文件整理到以下五大类别：

| 类别 | 文件夹名称 | 包含内容 |
|------|-----------|---------|
| 📚 大学课程 | `1-大学课程类` | 课件、作业、试卷、教材、PPT 等 |
| 💻 兴趣编程 | `2-兴趣编程类` | 代码文件、脚本、开发笔记、GitHub 项目等 |
| 🧠 认知提高 | `3-认知提高类` | 读书笔记、思维导图、总结报告等 |
| 🎮 娱乐休闲 | `4-娱乐休闲类` | 游戏、电影、音乐、图片、小说等 |
| 💼 日常工作 | `5-日常工作类` | 简历、发票、合同、表格、办公文档等 |

## 🚀 快速开始

### 环境要求

- Python 3.6+
- 无需额外依赖库（仅使用标准库）

### 安装

```bash
git clone https://github.com/marioaxe690-afk/smart-organizer.git
cd smart-organizer
```

### 使用方法

#### 1. 测试模式（推荐首次使用）

只显示分类计划，不会真正移动文件：

```bash
# 整理当前目录
python smart_organizer.py .

# 整理指定目录
python smart_organizer.py "C:/Users/YourName/Desktop"
```

#### 2. 执行模式

真正移动文件（会要求二次确认）：

```bash
# 整理当前目录
python smart_organizer.py . --execute

# 整理指定目录
python smart_organizer.py "C:/Users/YourName/Desktop" --execute
```

## 📖 使用示例

### 示例 1：整理桌面

```bash
python smart_organizer.py "C:/Users/YourName/Desktop" --execute
```

**输出示例：**

```
🤖 智能文件分类整理工具 - Smart Organizer
================================================================================
⚡ 当前模式：执行模式（Execute）
   将会真正移动文件！

正在扫描目录: C:\Users\YourName\Desktop
================================================================================

📋 文件分类计划
================================================================================

【2-兴趣编程类】 - 共 3 项
  📄 smart_organizer.py (15.2 KB)
  📁 GitHub
  📄 algorithm_notes.md (8.5 KB)

【4-娱乐休闲类】 - 共 2 项
  📄 wallpaper.jpg (2.3 MB)
  📄 music.mp3 (4.1 MB)

📊 统计信息
================================================================================
总文件数: 5
可分类: 5
无法分类: 0
安全跳过: 0
```

### 示例 2：测试模式预览

```bash
python smart_organizer.py "D:/Downloads"
```

会显示完整的分类计划，但不会移动任何文件。

## 🔧 分类规则

### 识别机制

工具使用**双重识别机制**：

1. **扩展名匹配**（权重：10 分）
2. **关键词匹配**（每个关键词：5 分）

最终按照**优先级**和**匹配分数**选择最佳分类。

### 支持的文件类型

#### 编程类
`.py` `.java` `.js` `.ts` `.cpp` `.c` `.html` `.css` `.json` `.md` 等

#### 文档类
`.doc` `.docx` `.pdf` `.xls` `.xlsx` `.ppt` `.pptx` 等

#### 媒体类
`.jpg` `.png` `.mp4` `.mp3` `.avi` `.mkv` 等

#### 其他
`.xmind` `.mm` `.epub` `.txt` 等

### 安全保护

以下文件类型会被**自动跳过**，确保系统安全：

- 可执行文件：`.exe` `.msi` `.dll` `.sys`
- 系统文件：`.ini` `.lnk` `.bat` `.cmd`
- 隐藏文件：以 `.` 开头的文件
- 临时文件：以 `~$` 开头的 Office 临时文件

## ⚙️ 自定义配置

如需修改分类规则，可以编辑 `smart_organizer.py` 中的 `_init_classification_rules()` 方法：

```python
def _init_classification_rules(self):
    return {
        'your_category': {
            'keywords': ['关键词1', '关键词2'],
            'extensions': ['.ext1', '.ext2'],
            'priority': 2
        }
    }
```

同时需要在 `categories` 字典中添加对应的文件夹名称。

## 🛡️ 安全特性

1. **默认测试模式**：首次运行不会移动文件
2. **二次确认**：执行模式需要输入 `yes` 确认
3. **智能跳过**：自动识别并跳过系统文件
4. **冲突处理**：同名文件自动添加时间戳
5. **错误处理**：移动失败不会影响其他文件

## 📝 命令行参数

```
usage: smart_organizer.py [-h] [--execute] [path]

positional arguments:
  path        要整理的文件夹路径（默认为当前目录）

optional arguments:
  -h, --help  显示帮助信息
  --execute   执行模式：真正移动文件（默认为测试模式）
```

## 🤝 贡献

欢迎提交 Issue 和 Pull Request！

### 开发建议

1. Fork 本仓库
2. 创建特性分支 (`git checkout -b feature/AmazingFeature`)
3. 提交更改 (`git commit -m 'Add some AmazingFeature'`)
4. 推送到分支 (`git push origin feature/AmazingFeature`)
5. 开启 Pull Request

## 📄 许可证

本项目采用 MIT 许可证 - 详见 [LICENSE](LICENSE) 文件

## 🙏 致谢

感谢所有为这个项目做出贡献的开发者！

## 📮 联系方式

如有问题或建议，欢迎通过以下方式联系：

- GitHub Issues: [提交问题](https://github.com/marioaxe690-afk/smart-organizer/issues)
- Email: [你的邮箱]

---

⭐ 如果这个项目对你有帮助，请给个 Star 支持一下！
