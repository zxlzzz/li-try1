"""
PubMed文献检索模块
使用NCBI E-utilities API进行文献检索
"""

import time
import requests
from typing import List, Dict, Optional
from Bio import Entrez
from tqdm import tqdm


class PubMedRetriever:
    """PubMed文献检索器"""

    def __init__(self, email: str, api_key: Optional[str] = None):
        """
        初始化PubMed检索器

        Args:
            email: 用户邮箱（NCBI要求）
            api_key: NCBI API密钥（可选，但建议使用以提高请求限制）
        """
        Entrez.email = email
        if api_key:
            Entrez.api_key = api_key
        self.base_delay = 0.34 if not api_key else 0.1  # 请求间隔

    def search(
        self,
        disease: str,
        max_results: int = 50,
        filter_types: Optional[List[str]] = None
    ) -> List[Dict]:
        """
        搜索指定疾病的文献

        Args:
            disease: 疾病名称
            max_results: 最大结果数量
            filter_types: 过滤文献类型，如 ['Review', 'Guideline', 'Clinical Trial']

        Returns:
            文献列表，每篇文献包含标题、摘要、作者等信息
        """
        print(f"\n正在从PubMed检索关于 '{disease}' 的文献...")

        # 构建查询字符串
        query = disease
        if filter_types:
            # 添加文献类型过滤
            type_filters = " OR ".join([f"{t}[Publication Type]" for t in filter_types])
            query = f"({disease}) AND ({type_filters})"

        try:
            # 第一步：搜索获取PMID列表
            search_handle = Entrez.esearch(
                db="pubmed",
                term=query,
                retmax=max_results,
                sort="relevance"
            )
            search_results = Entrez.read(search_handle)
            search_handle.close()

            pmid_list = search_results["IdList"]
            print(f"找到 {len(pmid_list)} 篇相关文献")

            if not pmid_list:
                return []

            # 第二步：批量获取文献详细信息
            articles = []
            batch_size = 20  # 每批次获取的文献数

            for i in tqdm(range(0, len(pmid_list), batch_size), desc="获取文献详情"):
                batch_ids = pmid_list[i:i + batch_size]
                time.sleep(self.base_delay)

                try:
                    fetch_handle = Entrez.efetch(
                        db="pubmed",
                        id=batch_ids,
                        rettype="medline",
                        retmode="xml"
                    )
                    records = Entrez.read(fetch_handle)
                    fetch_handle.close()

                    # 解析文献信息
                    for record in records['PubmedArticle']:
                        article = self._parse_article(record)
                        if article:
                            articles.append(article)

                except Exception as e:
                    print(f"获取批次 {i//batch_size + 1} 时出错: {str(e)}")
                    continue

            print(f"成功获取 {len(articles)} 篇文献详情")
            return articles

        except Exception as e:
            print(f"检索出错: {str(e)}")
            return []

    def _parse_article(self, record: Dict) -> Optional[Dict]:
        """
        解析单篇文献记录

        Args:
            record: PubMed文献记录

        Returns:
            格式化的文献信息字典
        """
        try:
            medline = record['MedlineCitation']
            article = medline['Article']

            # 提取PMID
            pmid = str(medline['PMID'])

            # 提取标题
            title = article.get('ArticleTitle', '')

            # 提取摘要
            abstract = ''
            if 'Abstract' in article and 'AbstractText' in article['Abstract']:
                abstract_parts = article['Abstract']['AbstractText']
                if isinstance(abstract_parts, list):
                    abstract = ' '.join([str(part) for part in abstract_parts])
                else:
                    abstract = str(abstract_parts)

            # 提取作者
            authors = []
            if 'AuthorList' in article:
                for author in article['AuthorList'][:5]:  # 只取前5位作者
                    if 'LastName' in author and 'Initials' in author:
                        authors.append(f"{author['LastName']} {author['Initials']}")

            # 提取发表日期
            pub_date = ''
            if 'Journal' in article and 'JournalIssue' in article['Journal']:
                issue = article['Journal']['JournalIssue']
                if 'PubDate' in issue:
                    date_parts = issue['PubDate']
                    year = date_parts.get('Year', '')
                    month = date_parts.get('Month', '')
                    pub_date = f"{year}-{month}" if month else year

            # 提取期刊名称
            journal = ''
            if 'Journal' in article and 'Title' in article['Journal']:
                journal = article['Journal']['Title']

            # 提取文献类型
            pub_types = []
            if 'PublicationTypeList' in article:
                pub_types = [str(pt) for pt in article['PublicationTypeList']]

            # 构建PubMed URL
            url = f"https://pubmed.ncbi.nlm.nih.gov/{pmid}/"

            return {
                'pmid': pmid,
                'title': title,
                'abstract': abstract,
                'authors': authors,
                'journal': journal,
                'pub_date': pub_date,
                'pub_types': pub_types,
                'url': url,
                'source': 'PubMed'
            }

        except Exception as e:
            print(f"解析文献时出错: {str(e)}")
            return None

    def get_related_articles(self, pmid: str, max_results: int = 10) -> List[str]:
        """
        获取相关文献的PMID列表

        Args:
            pmid: 原始文献的PMID
            max_results: 最大结果数

        Returns:
            相关文献的PMID列表
        """
        try:
            link_handle = Entrez.elink(
                dbfrom="pubmed",
                id=pmid,
                linkname="pubmed_pubmed",
                retmax=max_results
            )
            links = Entrez.read(link_handle)
            link_handle.close()

            if links and links[0]["LinkSetDb"]:
                return [link["Id"] for link in links[0]["LinkSetDb"][0]["Link"]]
            return []

        except Exception as e:
            print(f"获取相关文献时出错: {str(e)}")
            return []
