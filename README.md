# 医学文献检索与汇总系统

一个基于AI的智能医学文献检索和自动汇总系统，能够从PubMed和中华医学会等数据源检索文献，并按照病因诱因、发病机制、诊断与鉴别、治疗与预后四个模块自动分类汇总，最终生成结构化的Word文档。

## 功能特点

✨ **多数据源检索**
- PubMed文献数据库（通过NCBI E-utilities API）
- 中华医学会期刊（框架已提供，需配置访问权限）

🤖 **AI智能分析**
- 支持OpenAI GPT和Anthropic Claude两种AI模型
- 自动对文献内容进行分类和相关性评分
- 生成各模块的综合摘要

📋 **模块化分类**
- **病因诱因**: 疾病的病因、诱发因素、风险因素
- **发病机制**: 病理生理机制、分子机制
- **诊断与鉴别**: 诊断标准、检查方法、鉴别诊断
- **治疗与预后**: 治疗方案、用药指导、预后评估

📄 **专业文档生成**
- 自动生成格式化的Word文档
- 包含文献概览、模块摘要和详细文献列表
- 提供完整的参考文献链接

## 系统架构

```
li-try1/
├── src/
│   ├── retrievers/          # 文献检索模块
│   │   ├── pubmed_retriever.py
│   │   └── cma_retriever.py
│   ├── processors/          # 内容处理模块
│   │   └── content_classifier.py
│   ├── generators/          # 文档生成模块
│   │   └── word_generator.py
│   └── main.py             # 主程序入口
├── output/                  # 输出目录
├── requirements.txt         # Python依赖
├── .env.example            # 环境变量示例
├── run.sh                  # Linux/Mac运行脚本
├── run.bat                 # Windows运行脚本
└── README.md
```

## 安装指南

### 1. 环境要求

- Python 3.7 或更高版本
- pip 包管理器

### 2. 克隆项目

```bash
git clone <repository-url>
cd li-try1
```

### 3. 创建虚拟环境（推荐）

```bash
# Linux/Mac
python3 -m venv venv
source venv/bin/activate

# Windows
python -m venv venv
venv\Scripts\activate
```

### 4. 安装依赖

```bash
pip install -r requirements.txt
```

### 5. 配置环境变量

复制 `.env.example` 为 `.env` 并配置API密钥：

```bash
cp .env.example .env
```

编辑 `.env` 文件：

```ini
# OpenAI API密钥（推荐用于内容分析）
OPENAI_API_KEY=sk-your-openai-api-key

# 或使用 Anthropic Claude API
ANTHROPIC_API_KEY=your-anthropic-api-key

# PubMed配置（必填）
NCBI_EMAIL=your_email@example.com
NCBI_API_KEY=your-ncbi-api-key  # 可选，但建议配置
```

### 6. 获取API密钥

#### OpenAI API密钥
1. 访问 [OpenAI Platform](https://platform.openai.com/)
2. 注册/登录账号
3. 进入 [API Keys](https://platform.openai.com/api-keys) 页面
4. 创建新的API密钥

#### Anthropic API密钥（可选）
1. 访问 [Anthropic Console](https://console.anthropic.com/)
2. 注册/登录账号
3. 获取API密钥

#### NCBI API密钥（可选但推荐）
1. 访问 [NCBI Account](https://www.ncbi.nlm.nih.gov/account/)
2. 注册/登录账号
3. 在设置中生成API密钥
4. 配置后可提高PubMed检索速度（从每秒3次提升到每秒10次）

## 使用方法

### 快速开始

#### Linux/Mac

```bash
chmod +x run.sh
./run.sh 糖尿病
```

#### Windows

```bash
run.bat 糖尿病
```

### 命令行使用

```bash
python src/main.py --disease "疾病名称" [选项]
```

### 参数说明

| 参数 | 说明 | 必填 | 默认值 |
|------|------|------|--------|
| `--disease` | 要检索的疾病名称 | 是 | 无 |
| `--max-results` | 每个数据源的最大检索结果数 | 否 | 30 |
| `--email` | PubMed检索用的邮箱地址 | 是* | 从.env读取 |
| `--ncbi-api-key` | NCBI API密钥 | 否 | 从.env读取 |
| `--ai-provider` | AI服务提供商 (openai/anthropic) | 否 | openai |
| `--ai-api-key` | AI API密钥 | 否 | 从.env读取 |
| `--output` | 输出文件路径 | 否 | 自动生成 |
| `--skip-cma` | 跳过中华医学会检索 | 否 | false |
| `--filter-types` | PubMed文献类型过滤 | 否 | Review Guideline Meta-Analysis Clinical Trial |

*必填参数可以通过命令行或.env文件提供

### 使用示例

#### 1. 基本使用

```bash
python src/main.py --disease "糖尿病" --email "your@email.com"
```

#### 2. 增加检索结果数量

```bash
python src/main.py --disease "高血压" --max-results 50
```

#### 3. 使用Anthropic Claude API

```bash
python src/main.py --disease "冠心病" --ai-provider anthropic
```

#### 4. 指定输出路径

```bash
python src/main.py --disease "哮喘" --output "reports/asthma.docx"
```

#### 5. 自定义文献类型过滤

```bash
python src/main.py --disease "肺癌" --filter-types Review Guideline
```

#### 6. 仅检索PubMed（跳过中华医学会）

```bash
python src/main.py --disease "糖尿病" --skip-cma
```

## 工作流程

1. **文献检索阶段**
   - 从PubMed检索相关文献（支持类型过滤）
   - 从中华医学会检索中文文献（需配置）
   - 获取文献标题、摘要、作者、期刊等信息

2. **AI分析阶段**
   - 使用AI模型分析每篇文献
   - 判断文献与各模块的相关性
   - 提取关键信息和要点
   - 评估相关性分数

3. **摘要生成阶段**
   - 对每个模块的文献进行综合分析
   - 生成模块级别的综合摘要
   - 整合多篇文献的核心观点

4. **文档生成阶段**
   - 创建结构化的Word文档
   - 按模块组织文献内容
   - 添加文献链接和参考信息
   - 生成完整的参考文献列表

## 输出文档结构

生成的Word文档包含以下部分：

```
📄 [疾病名称]文献检索与汇总报告
├── 📊 文献概览
│   ├── 检索文献总数
│   └── 各模块文献数量统计
│
├── 📖 病因诱因
│   ├── 综合摘要
│   └── 相关文献详情
│
├── 📖 发病机制
│   ├── 综合摘要
│   └── 相关文献详情
│
├── 📖 诊断与鉴别
│   ├── 综合摘要
│   └── 相关文献详情
│
├── 📖 治疗与预后
│   ├── 综合摘要
│   └── 相关文献详情
│
└── 📚 完整参考文献列表
    ├── PubMed文献
    └── 中华医学会文献
```

每篇文献包含：
- 标题
- 作者信息
- 期刊名称和发表日期
- 文献链接（可点击访问）
- 相关性摘要
- 关键要点列表

## 注意事项

### PubMed检索

1. **邮箱地址**: NCBI要求所有API请求都要提供邮箱地址
2. **API密钥**: 虽然不是必需的，但强烈建议配置以提高检索速度
3. **请求限制**:
   - 无API密钥: 每秒最多3次请求
   - 有API密钥: 每秒最多10次请求
4. **文献类型**: 默认检索Review（综述）、Guideline（指南）、Meta-Analysis（荟萃分析）和Clinical Trial（临床试验）

### AI服务

1. **成本**: AI分析会产生API调用费用，请注意控制检索数量
2. **模型选择**:
   - OpenAI GPT-4o-mini: 性价比高，速度快
   - Anthropic Claude Haiku: 成本低，适合大批量处理
3. **API配额**: 确保你的API账户有足够的配额

### 中华医学会检索

当前版本提供的中华医学会检索为框架代码，实际使用需要：
1. 配置CNKI（中国知网）或万方数据的访问权限
2. 根据实际网站结构调整爬虫代码
3. 处理可能的反爬虫机制

建议使用 `--skip-cma` 参数跳过此部分，仅使用PubMed检索。

### 网络问题

- 确保网络可以访问PubMed API (https://eutils.ncbi.nlm.nih.gov/)
- 确保网络可以访问AI服务API
- 如有代理需求，请在代码中配置代理设置

## 故障排除

### 问题1: ModuleNotFoundError

```
解决方法: 确保已安装所有依赖
pip install -r requirements.txt
```

### 问题2: API密钥错误

```
解决方法: 检查.env文件中的API密钥是否正确配置
```

### 问题3: 未找到文献

```
可能原因:
1. 疾病名称拼写错误
2. 网络连接问题
3. PubMed API服务不可用

解决方法:
- 检查疾病名称
- 尝试使用英文疾病名称
- 检查网络连接
```

### 问题4: AI分析失败

```
可能原因:
1. API密钥无效
2. API配额用尽
3. 网络问题

解决方法:
- 检查API密钥
- 查看API账户余额
- 切换AI提供商
```

## 开发指南

### 添加新的文献数据源

1. 在 `src/retrievers/` 目录创建新的检索器类
2. 实现 `search()` 方法返回标准格式的文献列表
3. 在 `src/main.py` 中集成新的检索器

### 自定义分类模块

编辑 `src/processors/content_classifier.py` 中的 `MODULES` 字典：

```python
MODULES = {
    'your_module': {
        'name': '模块名称',
        'description': '模块描述'
    },
    # ... 其他模块
}
```

### 修改文档样式

编辑 `src/generators/word_generator.py` 中的文档生成逻辑，可以自定义：
- 字体样式
- 段落格式
- 表格样式
- 页面布局

## 性能优化建议

1. **批量处理**: 对于大量文献，考虑分批处理以避免超时
2. **缓存结果**: 可以保存检索结果避免重复检索
3. **并行处理**: AI分析可以实现并行处理以提高速度
4. **使用更快的模型**: 对于大批量处理，选择Haiku或GPT-4o-mini

## 版本历史

### v1.0.0 (2024)
- 初始版本发布
- 支持PubMed文献检索
- 支持OpenAI和Anthropic AI分析
- 自动生成Word文档
- 四模块分类系统

## 许可证

本项目仅供学习和研究使用。

## 贡献

欢迎提交Issue和Pull Request！

## 联系方式

如有问题或建议，请通过以下方式联系：
- 提交 GitHub Issue
- 发送邮件至项目维护者

## 致谢

- NCBI E-utilities API
- OpenAI / Anthropic
- Biopython
- python-docx

---

**免责声明**: 本系统生成的内容仅供参考，不构成医学建议。临床决策请遵循专业医学指导。
