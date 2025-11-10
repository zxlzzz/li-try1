#!/usr/bin/env python3
"""
医学文献检索与汇总系统 - 主程序
"""

import os
import sys
import argparse
from dotenv import load_dotenv

from retrievers import PubMedRetriever, CMARetriever
from processors import ContentClassifier
from generators import WordGenerator


def main():
    """主函数"""
    # 加载环境变量
    load_dotenv()

    # 解析命令行参数
    parser = argparse.ArgumentParser(
        description='医学文献检索与汇总系统',
        formatter_class=argparse.RawDescriptionHelpFormatter,
        epilog="""
使用示例:
  python src/main.py --disease "糖尿病" --max-results 30
  python src/main.py --disease "高血压" --ai-provider anthropic
  python src/main.py --disease "冠心病" --email your@email.com

注意:
  1. 需要在 .env 文件中配置 API 密钥
  2. PubMed 检索需要提供邮箱地址
  3. 默认使用 OpenAI API，可选择 Anthropic Claude
        """
    )

    parser.add_argument(
        '--disease',
        type=str,
        required=True,
        help='要检索的疾病名称（必填）'
    )

    parser.add_argument(
        '--max-results',
        type=int,
        default=30,
        help='每个数据源的最大检索结果数（默认: 30）'
    )

    parser.add_argument(
        '--email',
        type=str,
        default=os.getenv('NCBI_EMAIL'),
        help='用于PubMed检索的邮箱地址（必填）'
    )

    parser.add_argument(
        '--ncbi-api-key',
        type=str,
        default=os.getenv('NCBI_API_KEY'),
        help='NCBI API密钥（可选，建议使用以提高检索速度）'
    )

    parser.add_argument(
        '--ai-provider',
        type=str,
        choices=['openai', 'anthropic'],
        default='openai',
        help='AI服务提供商（默认: openai）'
    )

    parser.add_argument(
        '--ai-api-key',
        type=str,
        help='AI API密钥（如未提供，将从环境变量读取）'
    )

    parser.add_argument(
        '--output',
        type=str,
        help='输出文件路径（默认: output/疾病名_文献汇总_时间戳.docx）'
    )

    parser.add_argument(
        '--skip-cma',
        action='store_true',
        help='跳过中华医学会文献检索（中华医学会检索目前为示例实现）'
    )

    parser.add_argument(
        '--filter-types',
        type=str,
        nargs='+',
        default=['Review', 'Guideline', 'Meta-Analysis', 'Clinical Trial'],
        help='PubMed文献类型过滤（默认: Review Guideline Meta-Analysis Clinical Trial）'
    )

    args = parser.parse_args()

    # 验证必填参数
    if not args.email:
        print("错误: 必须提供邮箱地址（--email 或在 .env 中设置 NCBI_EMAIL）")
        sys.exit(1)

    # 显示配置信息
    print("=" * 60)
    print("医学文献检索与汇总系统")
    print("=" * 60)
    print(f"疾病名称: {args.disease}")
    print(f"最大结果数: {args.max_results}")
    print(f"AI提供商: {args.ai_provider}")
    print(f"文献类型过滤: {', '.join(args.filter_types)}")
    print("=" * 60)

    try:
        # 步骤1: 文献检索
        print("\n【步骤1/4】 文献检索")
        print("-" * 60)

        all_articles = []

        # PubMed检索
        print("\n>>> 检索 PubMed 数据库")
        pubmed = PubMedRetriever(
            email=args.email,
            api_key=args.ncbi_api_key
        )
        pubmed_articles = pubmed.search(
            disease=args.disease,
            max_results=args.max_results,
            filter_types=args.filter_types
        )
        all_articles.extend(pubmed_articles)
        print(f"✓ PubMed: 获得 {len(pubmed_articles)} 篇文献")

        # 中华医学会检索
        if not args.skip_cma:
            print("\n>>> 检索 中华医学会 数据库")
            cma = CMARetriever()
            cma_articles = cma.search(
                disease=args.disease,
                max_results=args.max_results // 2
            )
            all_articles.extend(cma_articles)
            print(f"✓ 中华医学会: 获得 {len(cma_articles)} 篇文献")
        else:
            print("\n>>> 跳过中华医学会检索")

        if not all_articles:
            print("\n错误: 未找到任何相关文献")
            sys.exit(1)

        print(f"\n✓ 文献检索完成，共获得 {len(all_articles)} 篇文献")

        # 步骤2: AI内容分类
        print("\n【步骤2/4】 AI内容分析与分类")
        print("-" * 60)

        classifier = ContentClassifier(
            ai_provider=args.ai_provider,
            api_key=args.ai_api_key
        )

        classified_content = classifier.classify_articles(
            articles=all_articles,
            disease=args.disease
        )

        print("\n✓ 内容分类完成")

        # 步骤3: 生成模块摘要
        print("\n【步骤3/4】 生成各模块综合摘要")
        print("-" * 60)

        module_summaries = {}
        for module_key, module_info in ContentClassifier.MODULES.items():
            module_name = module_info['name']
            content = classified_content.get(module_key, [])

            if content:
                print(f">>> 正在生成 {module_name} 模块摘要...")
                summary = classifier.generate_module_summary(
                    module_content=content,
                    module_name=module_name,
                    disease=args.disease
                )
                module_summaries[module_key] = summary
                print(f"✓ {module_name} 摘要完成")
            else:
                module_summaries[module_key] = ''
                print(f"○ {module_name} 无相关内容")

        print("\n✓ 模块摘要生成完成")

        # 步骤4: 生成Word文档
        print("\n【步骤4/4】 生成Word文档")
        print("-" * 60)

        generator = WordGenerator()
        output_path = generator.generate(
            disease=args.disease,
            classified_content=classified_content,
            module_summaries=module_summaries,
            output_path=args.output
        )

        print("\n" + "=" * 60)
        print("✓ 任务完成！")
        print("=" * 60)
        print(f"输出文件: {os.path.abspath(output_path)}")
        print("=" * 60)

    except KeyboardInterrupt:
        print("\n\n任务已取消")
        sys.exit(1)
    except Exception as e:
        print(f"\n\n错误: {str(e)}")
        import traceback
        traceback.print_exc()
        sys.exit(1)


if __name__ == '__main__':
    main()
