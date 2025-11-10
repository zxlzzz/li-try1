"""
文献内容分类器
使用AI模型将文献内容分类到不同的医学模块
"""

import os
import json
from typing import List, Dict, Optional
from openai import OpenAI
from anthropic import Anthropic


class ContentClassifier:
    """文献内容分类器，使用AI进行智能分类和汇总"""

    # 医学内容模块定义
    MODULES = {
        'etiology': {
            'name': '病因诱因',
            'description': '疾病的病因、诱发因素、风险因素等'
        },
        'pathogenesis': {
            'name': '发病机制',
            'description': '疾病的病理生理机制、分子机制等'
        },
        'diagnosis': {
            'name': '诊断与鉴别',
            'description': '诊断标准、检查方法、鉴别诊断等'
        },
        'treatment': {
            'name': '治疗与预后',
            'description': '治疗方案、用药指导、预后评估等'
        }
    }

    def __init__(self, ai_provider: str = 'openai', api_key: Optional[str] = None):
        """
        初始化分类器

        Args:
            ai_provider: AI提供商，'openai' 或 'anthropic'
            api_key: API密钥
        """
        self.ai_provider = ai_provider.lower()

        if not api_key:
            if self.ai_provider == 'openai':
                api_key = os.getenv('OPENAI_API_KEY')
            else:
                api_key = os.getenv('ANTHROPIC_API_KEY')

        if not api_key:
            raise ValueError(f"请设置 {self.ai_provider.upper()}_API_KEY 环境变量")

        if self.ai_provider == 'openai':
            self.client = OpenAI(api_key=api_key)
            self.model = 'gpt-4o-mini'  # 使用性价比高的模型
        else:
            self.client = Anthropic(api_key=api_key)
            self.model = 'claude-3-5-haiku-20241022'  # 使用快速模型

    def classify_articles(
        self,
        articles: List[Dict],
        disease: str
    ) -> Dict[str, List[Dict]]:
        """
        对文献进行分类和汇总

        Args:
            articles: 文献列表
            disease: 疾病名称

        Returns:
            按模块分类的文献内容
        """
        print(f"\n开始使用AI分析 {len(articles)} 篇文献...")

        classified_content = {
            'etiology': [],
            'pathogenesis': [],
            'diagnosis': [],
            'treatment': []
        }

        # 逐篇文章分析
        from tqdm import tqdm
        for article in tqdm(articles, desc="分析文献"):
            try:
                classification = self._classify_single_article(article, disease)
                if classification:
                    # 将分类结果添加到相应模块
                    for module, content in classification.items():
                        if content and content.get('relevant', False):
                            classified_content[module].append({
                                'article': article,
                                'summary': content.get('summary', ''),
                                'key_points': content.get('key_points', []),
                                'relevance_score': content.get('relevance_score', 0)
                            })
            except Exception as e:
                print(f"分析文献时出错 ({article.get('title', 'Unknown')}): {str(e)}")
                continue

        # 对每个模块的内容进行排序（按相关性）
        for module in classified_content:
            classified_content[module].sort(
                key=lambda x: x.get('relevance_score', 0),
                reverse=True
            )

        print(f"分类完成！各模块文献数量：")
        for module, content in classified_content.items():
            module_name = self.MODULES[module]['name']
            print(f"  {module_name}: {len(content)} 篇")

        return classified_content

    def _classify_single_article(
        self,
        article: Dict,
        disease: str
    ) -> Optional[Dict]:
        """
        分析单篇文献并分类到各模块

        Args:
            article: 文献信息
            disease: 疾病名称

        Returns:
            各模块的分类结果
        """
        # 构建提示词
        prompt = self._build_classification_prompt(article, disease)

        try:
            if self.ai_provider == 'openai':
                response = self.client.chat.completions.create(
                    model=self.model,
                    messages=[
                        {
                            "role": "system",
                            "content": "你是一名专业的医学文献分析专家，擅长提取和分类医学文献中的关键信息。"
                        },
                        {
                            "role": "user",
                            "content": prompt
                        }
                    ],
                    temperature=0.3,
                    response_format={"type": "json_object"}
                )
                result = response.choices[0].message.content
            else:  # anthropic
                response = self.client.messages.create(
                    model=self.model,
                    max_tokens=2000,
                    temperature=0.3,
                    messages=[
                        {
                            "role": "user",
                            "content": prompt
                        }
                    ]
                )
                result = response.content[0].text

            # 解析JSON结果
            classification = json.loads(result)
            return classification

        except Exception as e:
            print(f"AI分类出错: {str(e)}")
            return None

    def _build_classification_prompt(self, article: Dict, disease: str) -> str:
        """构建分类提示词"""
        return f"""
请分析以下关于"{disease}"的医学文献，并将其内容分类到以下四个模块中：

1. **病因诱因** (etiology): 疾病的病因、诱发因素、风险因素
2. **发病机制** (pathogenesis): 病理生理机制、分子机制
3. **诊断与鉴别** (diagnosis): 诊断标准、检查方法、鉴别诊断
4. **治疗与预后** (treatment): 治疗方案、用药指导、预后评估

文献信息：
标题: {article.get('title', 'N/A')}
摘要: {article.get('abstract', 'N/A')[:1500]}  # 限制长度
来源: {article.get('source', 'N/A')}
类型: {', '.join(article.get('pub_types', []))}

请以JSON格式返回分析结果，格式如下：
{{
    "etiology": {{
        "relevant": true/false,
        "summary": "该模块的内容摘要（1-2句话）",
        "key_points": ["关键点1", "关键点2"],
        "relevance_score": 0-10的相关性评分
    }},
    "pathogenesis": {{
        "relevant": true/false,
        "summary": "...",
        "key_points": [],
        "relevance_score": 0-10
    }},
    "diagnosis": {{
        "relevant": true/false,
        "summary": "...",
        "key_points": [],
        "relevance_score": 0-10
    }},
    "treatment": {{
        "relevant": true/false,
        "summary": "...",
        "key_points": [],
        "relevance_score": 0-10
    }}
}}

注意：
1. 如果文献内容与某个模块无关，将relevant设为false
2. relevance_score表示文献对该模块的相关性（0-10分）
3. key_points应该是具体的、可操作的信息点
4. 保持专业性和准确性
"""

    def generate_module_summary(
        self,
        module_content: List[Dict],
        module_name: str,
        disease: str
    ) -> str:
        """
        为特定模块生成综合摘要

        Args:
            module_content: 模块的文献内容列表
            module_name: 模块名称
            disease: 疾病名称

        Returns:
            模块综合摘要
        """
        if not module_content:
            return f"暂无关于{disease}的{module_name}相关文献。"

        # 收集所有关键点
        all_summaries = []
        all_key_points = []

        for item in module_content[:10]:  # 最多使用前10篇最相关的文献
            if item.get('summary'):
                all_summaries.append(item['summary'])
            if item.get('key_points'):
                all_key_points.extend(item['key_points'])

        # 构建综合摘要提示
        prompt = f"""
请基于以下关于"{disease}"的{module_name}相关文献摘要和关键点，生成一份综合性总结。

文献摘要：
{chr(10).join([f"- {s}" for s in all_summaries[:20]])}

关键点：
{chr(10).join([f"- {p}" for p in all_key_points[:30]])}

要求：
1. 生成一段300-500字的综合摘要
2. 整合所有文献的核心信息
3. 避免重复，突出重点
4. 使用专业但易懂的语言
5. 保持客观性和准确性

请直接返回摘要文本，不要包含其他格式。
"""

        try:
            if self.ai_provider == 'openai':
                response = self.client.chat.completions.create(
                    model=self.model,
                    messages=[
                        {
                            "role": "system",
                            "content": "你是一名专业的医学文献综述专家。"
                        },
                        {
                            "role": "user",
                            "content": prompt
                        }
                    ],
                    temperature=0.5
                )
                summary = response.choices[0].message.content
            else:  # anthropic
                response = self.client.messages.create(
                    model=self.model,
                    max_tokens=1500,
                    temperature=0.5,
                    messages=[
                        {
                            "role": "user",
                            "content": prompt
                        }
                    ]
                )
                summary = response.content[0].text

            return summary.strip()

        except Exception as e:
            print(f"生成综合摘要时出错: {str(e)}")
            return f"综合{len(module_content)}篇相关文献的内容。"
