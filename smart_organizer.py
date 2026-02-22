#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
智能文件分类整理工具 - Smart Organizer
作者：AI Assistant
功能：自动将指定文件夹中的文件按照五大类别进行智能分类整理
安全特性：默认为测试模式，只有添加 --execute 参数才会真正移动文件
"""

import os
import sys
import shutil
import argparse
from pathlib import Path
from datetime import datetime

# Windows 系统编码处理
if sys.platform == 'win32':
    import io
    sys.stdout = io.TextIOWrapper(sys.stdout.buffer, encoding='utf-8')


class SmartOrganizer:
    """智能文件整理器类"""

    def __init__(self, target_path, dry_run=True):
        """
        初始化整理器

        参数:
            target_path: 要整理的目标文件夹路径
            dry_run: 是否为测试模式（默认True，只显示计划不执行）
        """
        self.target_path = Path(target_path).resolve()
        self.dry_run = dry_run

        # 定义五大分类文件夹名称
        self.categories = {
            'course': '1-大学课程类',
            'coding': '2-兴趣编程类',
            'growth': '3-认知提高类',
            'entertainment': '4-娱乐休闲类',
            'work': '5-日常工作类'
        }

        # 定义需要跳过的文件类型（安全保护）
        self.skip_extensions = {
            '.exe', '.msi', '.dll', '.sys', '.ini',
            '.lnk', '.url', '.bat', '.cmd', '.com',
            '.scr', '.cpl', '.drv', '.ocx'
        }

        # 定义各类别的关键词和扩展名规则
        self.classification_rules = self._init_classification_rules()

        # 统计信息
        self.stats = {
            'total': 0,
            'skipped': 0,
            'classified': 0,
            'by_category': {cat: 0 for cat in self.categories.keys()}
        }

    def _init_classification_rules(self):
        """
        初始化文件分类规则

        返回:
            包含各类别识别规则的字典
        """
        return {
            'course': {
                'keywords': [
                    '课程', '作业', '试卷', '考试', '教材', '课件',
                    '大学', '学院', '专业', '学期', '学分', '成绩',
                    '奖学金', '助学金', '请假', '考勤', '学习指南',
                    '管理学', '经济', '计算机二级', '英语', '数学'
                ],
                'extensions': ['.ppt', '.pptx', '.pptm'],
                'priority': 2  # 优先级：数字越大越优先
            },
            'coding': {
                'keywords': [
                    'python', 'java', 'javascript', 'code', 'script',
                    '编程', '代码', '开发', 'github', 'git', 'api',
                    'algorithm', '算法', 'leetcode', 'project'
                ],
                'extensions': [
                    '.py', '.java', '.js', '.ts', '.cpp', '.c', '.h',
                    '.html', '.css', '.json', '.xml', '.sql', '.sh',
                    '.go', '.rs', '.php', '.rb', '.swift', '.kt',
                    '.ipynb', '.md'  # Jupyter notebook 和 Markdown
                ],
                'priority': 3
            },
            'growth': {
                'keywords': [
                    '生涯', '规划', '发展', '成长', '复盘', '反思',
                    '读书', '笔记', '思维导图', '总结', '心得',
                    '访谈', '实习', '实践', '证明', '报告'
                ],
                'extensions': ['.xmind', '.mm'],  # 思维导图
                'priority': 2
            },
            'entertainment': {
                'keywords': [
                    '游戏', '攻略', '电影', '音乐', '小说', '动漫',
                    '娱乐', '休闲', '视频', '照片', '图片', '壁纸',
                    '星斗', '玄女', '考验', '装备', '道具'
                ],
                'extensions': [
                    '.jpg', '.jpeg', '.png', '.gif', '.bmp', '.svg', '.webp',
                    '.mp4', '.avi', '.mkv', '.mov', '.flv', '.wmv',
                    '.mp3', '.wav', '.flac', '.aac', '.m4a',
                    '.epub', '.mobi', '.azw3', '.txt'
                ],
                'priority': 1
            },
            'work': {
                'keywords': [
                    '简历', '求职', '发票', '报销', '合同', '协议',
                    '工作', '办公', '会议', '汇报', '总结', '计划',
                    '表格', '数据', '统计', '分析', '展演', '稿子'
                ],
                'extensions': [
                    '.doc', '.docx', '.xls', '.xlsx', '.csv',
                    '.pdf'  # PDF 可能属于多个类别，优先级较低
                ],
                'priority': 1
            }
        }

    def is_safe_to_process(self, file_path):
        """
        检查文件是否安全可处理

        参数:
            file_path: 文件路径对象

        返回:
            True 表示安全可处理，False 表示应跳过
        """
        # 跳过隐藏文件
        if file_path.name.startswith('.'):
            return False

        # 跳过系统文件
        if file_path.name.lower() in ['desktop.ini', 'thumbs.db', '$recycle.bin']:
            return False

        # 跳过危险扩展名
        if file_path.suffix.lower() in self.skip_extensions:
            return False

        # 跳过 Word/Excel 临时文件（以 ~$ 开头）
        if file_path.name.startswith('~$'):
            return False

        return True

    def classify_file(self, file_path):
        """
        根据文件名和扩展名判断文件所属类别

        参数:
            file_path: 文件路径对象

        返回:
            类别键名（如 'course'），如果无法分类则返回 None
        """
        filename = file_path.name.lower()
        extension = file_path.suffix.lower()

        # 存储匹配结果：(类别, 优先级, 匹配分数)
        matches = []

        for category, rules in self.classification_rules.items():
            score = 0

            # 检查扩展名匹配（权重：10分）
            if extension in rules['extensions']:
                score += 10

            # 检查关键词匹配（每个关键词：5分）
            for keyword in rules['keywords']:
                if keyword.lower() in filename:
                    score += 5

            # 如果有匹配分数，记录下来
            if score > 0:
                matches.append((category, rules['priority'], score))

        # 如果没有任何匹配，返回 None
        if not matches:
            return None

        # 按照优先级和分数排序，选择最佳匹配
        # 排序规则：优先级高的优先，优先级相同时分数高的优先
        matches.sort(key=lambda x: (x[1], x[2]), reverse=True)

        return matches[0][0]

    def scan_directory(self):
        """
        扫描目标目录，生成文件分类计划

        返回:
            分类计划字典 {类别: [文件列表]}
        """
        plan = {cat: [] for cat in self.categories.keys()}
        plan['skipped'] = []  # 跳过的文件
        plan['unclassified'] = []  # 无法分类的文件

        print(f"\n正在扫描目录: {self.target_path}")
        print("=" * 80)

        # 遍历目录中的所有文件和文件夹
        for item in self.target_path.iterdir():
            # 跳过已存在的分类文件夹
            if item.name in self.categories.values():
                continue

            self.stats['total'] += 1

            # 检查是否安全可处理
            if not self.is_safe_to_process(item):
                plan['skipped'].append(item)
                self.stats['skipped'] += 1
                continue

            # 对文件进行分类
            if item.is_file():
                category = self.classify_file(item)
                if category:
                    plan[category].append(item)
                    self.stats['classified'] += 1
                    self.stats['by_category'][category] += 1
                else:
                    plan['unclassified'].append(item)

            # 对文件夹进行分类（基于文件夹名称）
            elif item.is_dir():
                # 创建一个虚拟文件对象用于分类判断
                virtual_file = Path(str(item) + '.folder')
                category = self.classify_file(virtual_file)
                if category:
                    plan[category].append(item)
                    self.stats['classified'] += 1
                    self.stats['by_category'][category] += 1
                else:
                    plan['unclassified'].append(item)

        return plan

    def print_plan(self, plan):
        """
        打印文件移动计划

        参数:
            plan: 分类计划字典
        """
        print("\n" + "=" * 80)
        print("📋 文件分类计划")
        print("=" * 80)

        # 打印各类别的文件
        for category, folder_name in self.categories.items():
            files = plan[category]
            if files:
                print(f"\n【{folder_name}】 - 共 {len(files)} 项")
                for file_path in files:
                    file_type = "📁" if file_path.is_dir() else "📄"
                    size = self._get_size_str(file_path)
                    print(f"  {file_type} {file_path.name} ({size})")

        # 打印无法分类的文件
        if plan['unclassified']:
            print(f"\n【⚠️  无法自动分类】 - 共 {len(plan['unclassified'])} 项")
            for file_path in plan['unclassified']:
                file_type = "📁" if file_path.is_dir() else "📄"
                print(f"  {file_type} {file_path.name}")
            print("  提示：这些文件将保持原位不移动")

        # 打印跳过的文件
        if plan['skipped']:
            print(f"\n【🛡️  安全跳过】 - 共 {len(plan['skipped'])} 项")
            for file_path in plan['skipped'][:10]:  # 最多显示10个
                print(f"  🔒 {file_path.name}")
            if len(plan['skipped']) > 10:
                print(f"  ... 还有 {len(plan['skipped']) - 10} 个文件被跳过")

        # 打印统计信息
        print("\n" + "=" * 80)
        print("📊 统计信息")
        print("=" * 80)
        print(f"总文件数: {self.stats['total']}")
        print(f"可分类: {self.stats['classified']}")
        print(f"无法分类: {len(plan['unclassified'])}")
        print(f"安全跳过: {self.stats['skipped']}")

        print("\n各类别分布:")
        for category, folder_name in self.categories.items():
            count = self.stats['by_category'][category]
            if count > 0:
                print(f"  {folder_name}: {count} 项")

    def _get_size_str(self, file_path):
        """
        获取文件大小的可读字符串

        参数:
            file_path: 文件路径对象

        返回:
            格式化的大小字符串
        """
        try:
            if file_path.is_file():
                size = file_path.stat().st_size
                for unit in ['B', 'KB', 'MB', 'GB']:
                    if size < 1024.0:
                        return f"{size:.1f} {unit}"
                    size /= 1024.0
                return f"{size:.1f} TB"
            else:
                return "文件夹"
        except:
            return "未知"

    def execute_plan(self, plan):
        """
        执行文件移动计划

        参数:
            plan: 分类计划字典
        """
        print("\n" + "=" * 80)
        print("🚀 开始执行文件移动")
        print("=" * 80)

        success_count = 0
        fail_count = 0

        # 创建分类文件夹
        for folder_name in self.categories.values():
            folder_path = self.target_path / folder_name
            if not folder_path.exists():
                folder_path.mkdir()
                print(f"✓ 创建文件夹: {folder_name}")

        print()

        # 移动文件
        for category, folder_name in self.categories.items():
            files = plan[category]
            if not files:
                continue

            print(f"【{folder_name}】")
            dest_folder = self.target_path / folder_name

            for file_path in files:
                try:
                    dest_path = dest_folder / file_path.name

                    # 如果目标位置已存在同名文件，添加时间戳
                    if dest_path.exists():
                        timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
                        stem = dest_path.stem
                        suffix = dest_path.suffix
                        dest_path = dest_folder / f"{stem}_{timestamp}{suffix}"

                    shutil.move(str(file_path), str(dest_path))
                    print(f"  ✓ {file_path.name}")
                    success_count += 1

                except Exception as e:
                    print(f"  ✗ {file_path.name} - 错误: {e}")
                    fail_count += 1

        # 打印执行结果
        print("\n" + "=" * 80)
        print("✅ 执行完成")
        print("=" * 80)
        print(f"成功: {success_count} 项")
        print(f"失败: {fail_count} 项")

        if plan['unclassified']:
            print(f"未移动: {len(plan['unclassified'])} 项（无法自动分类）")

    def run(self):
        """运行整理器主流程"""
        # 检查目标路径是否存在
        if not self.target_path.exists():
            print(f"❌ 错误：路径不存在 - {self.target_path}")
            return False

        if not self.target_path.is_dir():
            print(f"❌ 错误：不是有效的文件夹 - {self.target_path}")
            return False

        # 打印模式信息
        print("\n" + "=" * 80)
        print("🤖 智能文件分类整理工具 - Smart Organizer")
        print("=" * 80)

        if self.dry_run:
            print("⚠️  当前模式：测试演习（Dry Run）")
            print("   只显示分类计划，不会真正移动文件")
            print("   如需执行，请添加 --execute 参数")
        else:
            print("⚡ 当前模式：执行模式（Execute）")
            print("   将会真正移动文件！")

        # 扫描并生成计划
        plan = self.scan_directory()

        # 打印计划
        self.print_plan(plan)

        # 如果是执行模式，询问确认
        if not self.dry_run:
            print("\n" + "=" * 80)
            response = input("⚠️  确认要执行文件移动吗？(输入 yes 确认): ")
            if response.lower() != 'yes':
                print("❌ 已取消操作")
                return False

            # 执行移动
            self.execute_plan(plan)
        else:
            print("\n" + "=" * 80)
            print("💡 提示：这只是测试演习，没有移动任何文件")
            print("   如需真正执行，请运行：")
            print(f"   python smart_organizer.py \"{self.target_path}\" --execute")

        print("=" * 80 + "\n")
        return True


def main():
    """主函数：处理命令行参数并运行整理器"""

    # 创建命令行参数解析器
    parser = argparse.ArgumentParser(
        description='智能文件分类整理工具 - 自动将文件按类别整理到子文件夹',
        formatter_class=argparse.RawDescriptionHelpFormatter,
        epilog="""
使用示例:
  # 测试模式（只显示计划，不移动文件）
  python smart_organizer.py "C:/Users/YourName/Downloads"

  # 执行模式（真正移动文件）
  python smart_organizer.py "C:/Users/YourName/Downloads" --execute

  # 整理当前目录
  python smart_organizer.py . --execute

分类说明:
  1-大学课程类: 课件、作业、PDF教材等
  2-兴趣编程类: 代码、脚本、开发笔记等
  3-认知提高类: 读书笔记、思维导图等
  4-娱乐休闲类: 游戏、电影、音乐、图片等
  5-日常工作类: 发票、简历、表格等
        """
    )

    parser.add_argument(
        'path',
        nargs='?',
        default='.',
        help='要整理的文件夹路径（默认为当前目录）'
    )

    parser.add_argument(
        '--execute',
        action='store_true',
        help='执行模式：真正移动文件（默认为测试模式）'
    )

    # 解析参数
    args = parser.parse_args()

    # 创建整理器并运行
    organizer = SmartOrganizer(
        target_path=args.path,
        dry_run=not args.execute
    )

    organizer.run()


if __name__ == '__main__':
    main()
