#!/usr/bin/env python3
"""
系统测试脚本 - 用于验证各模块是否正常工作
"""

import os
import sys

def test_imports():
    """测试所有模块是否可以正常导入"""
    print("测试模块导入...")
    try:
        from src.retrievers import PubMedRetriever, CMARetriever
        from src.processors import ContentClassifier
        from src.generators import WordGenerator
        print("✓ 所有模块导入成功")
        return True
    except Exception as e:
        print(f"✗ 模块导入失败: {str(e)}")
        return False

def test_dependencies():
    """测试依赖包是否已安装"""
    print("\n测试依赖包...")
    required_packages = [
        'biopython',
        'requests',
        'docx',
        'openai',
        'anthropic',
        'bs4',
        'lxml',
        'dotenv',
        'tqdm'
    ]

    missing = []
    for package in required_packages:
        try:
            __import__(package)
            print(f"✓ {package}")
        except ImportError:
            print(f"✗ {package} - 未安装")
            missing.append(package)

    if missing:
        print(f"\n缺少以下依赖包: {', '.join(missing)}")
        print("请运行: pip install -r requirements.txt")
        return False
    else:
        print("\n✓ 所有依赖包已安装")
        return True

def test_env_config():
    """测试环境配置"""
    print("\n测试环境配置...")

    from dotenv import load_dotenv
    load_dotenv()

    required_vars = ['NCBI_EMAIL']
    optional_vars = [
        'OPENAI_API_KEY',
        'ANTHROPIC_API_KEY',
        'NCBI_API_KEY'
    ]

    all_good = True

    # 检查必填变量
    for var in required_vars:
        value = os.getenv(var)
        if value:
            print(f"✓ {var} - 已配置")
        else:
            print(f"✗ {var} - 未配置（必填）")
            all_good = False

    # 检查可选变量
    has_ai_key = False
    for var in optional_vars:
        value = os.getenv(var)
        if value:
            print(f"✓ {var} - 已配置")
            if 'API_KEY' in var and 'NCBI' not in var:
                has_ai_key = True
        else:
            print(f"○ {var} - 未配置（可选）")

    if not has_ai_key:
        print("\n⚠ 警告: 未配置任何AI API密钥（OPENAI_API_KEY或ANTHROPIC_API_KEY）")
        print("系统需要AI API密钥才能进行文献分析")
        all_good = False

    if all_good:
        print("\n✓ 环境配置完整")
    else:
        print("\n⚠ 环境配置不完整，请查看上述提示")

    return all_good

def test_directory_structure():
    """测试目录结构"""
    print("\n测试目录结构...")

    required_dirs = [
        'src',
        'src/retrievers',
        'src/processors',
        'src/generators',
        'output'
    ]

    all_exist = True
    for dir_path in required_dirs:
        if os.path.exists(dir_path):
            print(f"✓ {dir_path}/")
        else:
            print(f"✗ {dir_path}/ - 不存在")
            all_exist = False

    if all_exist:
        print("\n✓ 目录结构完整")
    else:
        print("\n⚠ 目录结构不完整")

    return all_exist

def test_pubmed_connection():
    """测试PubMed连接"""
    print("\n测试PubMed API连接...")

    try:
        from Bio import Entrez
        import os
        from dotenv import load_dotenv

        load_dotenv()
        email = os.getenv('NCBI_EMAIL', 'test@example.com')

        Entrez.email = email

        # 尝试一个简单的搜索
        handle = Entrez.esearch(db="pubmed", term="diabetes", retmax=1)
        result = Entrez.read(handle)
        handle.close()

        if result['Count'] != '0':
            print(f"✓ PubMed API连接成功（找到 {result['Count']} 篇相关文献）")
            return True
        else:
            print("○ PubMed API连接成功，但未找到测试结果")
            return True

    except Exception as e:
        print(f"✗ PubMed API连接失败: {str(e)}")
        return False

def main():
    """运行所有测试"""
    print("=" * 60)
    print("医学文献检索系统 - 系统测试")
    print("=" * 60)

    tests = [
        ("依赖包", test_dependencies),
        ("模块导入", test_imports),
        ("目录结构", test_directory_structure),
        ("环境配置", test_env_config),
        ("PubMed连接", test_pubmed_connection),
    ]

    results = {}
    for test_name, test_func in tests:
        try:
            results[test_name] = test_func()
        except Exception as e:
            print(f"\n✗ {test_name} 测试出错: {str(e)}")
            results[test_name] = False

    # 总结
    print("\n" + "=" * 60)
    print("测试总结")
    print("=" * 60)

    passed = sum(1 for r in results.values() if r)
    total = len(results)

    for test_name, result in results.items():
        status = "✓ 通过" if result else "✗ 失败"
        print(f"{test_name}: {status}")

    print(f"\n通过: {passed}/{total}")

    if passed == total:
        print("\n🎉 所有测试通过！系统已准备就绪。")
        print("\n快速开始:")
        print('  python src/main.py --disease "diabetes" --skip-cma')
    else:
        print("\n⚠ 部分测试失败，请检查上述错误信息。")
        print("\n常见解决方案:")
        print("  1. 安装依赖: pip install -r requirements.txt")
        print("  2. 配置环境: cp .env.example .env 并编辑")
        print("  3. 检查网络连接")

    print("=" * 60)

    return passed == total

if __name__ == '__main__':
    success = main()
    sys.exit(0 if success else 1)
