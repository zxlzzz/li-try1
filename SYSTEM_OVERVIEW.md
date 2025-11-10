# 医学文献检索与汇总系统 - 系统总览

## 系统简介

这是一个完整的、基于AI的医学文献检索和自动汇总系统。系统能够：

1. 从PubMed等医学数据库检索相关文献
2. 使用AI智能分析文献内容
3. 按照医学模块自动分类和汇总
4. 生成专业的Word文档报告

## 核心功能

### 1. 多数据源文献检索
- **PubMed检索**：通过NCBI E-utilities API检索高质量医学文献
- **中华医学会检索**：提供框架代码，可扩展中文医学数据源
- **文献类型过滤**：支持综述、指南、荟萃分析、临床试验等类型

### 2. AI智能内容分析
- **支持多种AI模型**：
  - OpenAI GPT-4o-mini（快速、性价比高）
  - Anthropic Claude Haiku（成本低、适合大批量）
- **智能分类**：自动将文献内容分类到四个医学模块
- **相关性评分**：对每篇文献的相关性进行0-10分评分
- **关键点提取**：自动提取文献中的关键信息点

### 3. 四模块医学分类

系统将文献内容自动分类到以下四个模块：

| 模块 | 内容 |
|------|------|
| **病因诱因** | 疾病的病因、诱发因素、风险因素等 |
| **发病机制** | 病理生理机制、分子机制、发病过程等 |
| **诊断与鉴别** | 诊断标准、检查方法、鉴别诊断等 |
| **治疗与预后** | 治疗方案、用药指导、预后评估等 |

### 4. 专业文档生成
- **Word格式输出**：生成格式规范的.docx文档
- **结构化内容**：包含概览、模块摘要、详细文献列表
- **完整参考文献**：提供所有文献的PubMed链接
- **可编辑性**：生成的文档可用Word或WPS直接编辑

## 技术架构

### 核心技术栈
```
Python 3.7+
├── Biopython (文献检索)
├── OpenAI / Anthropic (AI分析)
├── python-docx (文档生成)
├── BeautifulSoup4 (网页解析)
└── Requests (HTTP请求)
```

### 模块架构
```
医学文献检索系统
├── 检索模块 (retrievers/)
│   ├── PubMed检索器
│   └── 中华医学会检索器
├── 处理模块 (processors/)
│   └── AI内容分类器
├── 生成模块 (generators/)
│   └── Word文档生成器
└── 主程序 (main.py)
```

## 工作流程

```mermaid
graph LR
    A[输入疾病名称] --> B[PubMed检索]
    A --> C[中华医学会检索]
    B --> D[文献汇总]
    C --> D
    D --> E[AI内容分析]
    E --> F[四模块分类]
    F --> G[生成模块摘要]
    G --> H[生成Word文档]
```

### 详细步骤

1. **文献检索** (1-2分钟)
   - 根据疾病名称在PubMed检索
   - 应用文献类型过滤
   - 获取文献元数据（标题、摘要、作者等）

2. **AI分析** (2-5分钟)
   - 逐篇分析文献内容
   - 判断与各模块的相关性
   - 提取关键信息和要点
   - 计算相关性分数

3. **摘要生成** (30-60秒)
   - 对每个模块生成综合摘要
   - 整合多篇文献的核心观点
   - 保持客观性和准确性

4. **文档生成** (10-30秒)
   - 创建Word文档
   - 格式化内容
   - 添加文献链接
   - 保存到output目录

## 文件结构

```
li-try1/
├── src/                          # 源代码
│   ├── retrievers/              # 检索模块
│   │   ├── __init__.py
│   │   ├── pubmed_retriever.py  # PubMed检索器
│   │   └── cma_retriever.py     # 中华医学会检索器
│   ├── processors/              # 处理模块
│   │   ├── __init__.py
│   │   └── content_classifier.py # AI内容分类器
│   ├── generators/              # 生成模块
│   │   ├── __init__.py
│   │   └── word_generator.py    # Word文档生成器
│   └── main.py                  # 主程序入口
│
├── output/                       # 输出目录（自动创建）
│
├── requirements.txt              # Python依赖列表
├── .env.example                 # 环境变量示例
├── .gitignore                   # Git忽略文件
│
├── run.sh                       # Linux/Mac运行脚本
├── run.bat                      # Windows运行脚本
├── test_system.py               # 系统测试脚本
│
├── README.md                    # 项目说明
├── USAGE_GUIDE.md               # 使用指南
├── CHANGELOG.md                 # 更新日志
└── SYSTEM_OVERVIEW.md           # 本文档
```

## 快速开始

### 1. 安装
```bash
pip install -r requirements.txt
```

### 2. 配置
```bash
cp .env.example .env
# 编辑.env文件，填入API密钥
```

### 3. 运行
```bash
python src/main.py --disease "diabetes" --skip-cma
```

### 4. 查看结果
生成的Word文档在 `output/` 目录中。

## 使用场景

### 场景1：临床医生快速了解疾病
医生需要快速了解某个疾病的最新研究进展：
```bash
python src/main.py --disease "heart failure" --max-results 30 --skip-cma
```
系统会在5-10分钟内生成一份包含最新文献的综合报告。

### 场景2：医学生撰写综述
医学生需要为某个疾病撰写文献综述：
```bash
python src/main.py --disease "alzheimer disease" --max-results 100
```
系统会检索100篇文献并按模块分类，极大提高效率。

### 场景3：研究人员文献调研
研究人员需要系统性了解某个疾病的发病机制：
```bash
python src/main.py --disease "rheumatoid arthritis" --filter-types Review Meta-Analysis
```
系统会重点检索综述和荟萃分析，提供高质量的文献汇总。

### 场景4：临床指南编写
需要收集某个疾病的临床指南和诊疗规范：
```bash
python src/main.py --disease "diabetes mellitus" --filter-types Guideline
```
系统会专门检索临床指南类文献。

## 性能指标

### 检索性能
- PubMed检索速度：约10-20篇/分钟（无API密钥）
- PubMed检索速度：约30-50篇/分钟（有API密钥）
- 文献解析成功率：>95%

### AI分析性能
- 单篇文献分析时间：2-5秒
- 30篇文献总分析时间：2-5分钟
- 分类准确率：基于AI模型性能

### 成本估算（30篇文献）
- OpenAI GPT-4o-mini：$0.07-0.15
- Anthropic Claude Haiku：$0.03-0.08

## 系统优势

### 1. 自动化程度高
- 一键完成从检索到文档生成
- 无需手动分类和整理
- 大幅提高工作效率

### 2. AI驱动的智能分析
- 准确理解文献内容
- 智能提取关键信息
- 合理评估相关性

### 3. 专业的医学分类
- 符合医学逻辑的四模块分类
- 便于临床和科研使用
- 结构化呈现信息

### 4. 高质量的输出
- 专业格式的Word文档
- 包含完整参考文献
- 可直接编辑和使用

### 5. 灵活的配置
- 支持多种AI模型
- 可调整检索数量和类型
- 可扩展新的数据源

## 系统限制

### 1. API依赖
- 需要OpenAI或Anthropic API密钥
- AI分析会产生API调用费用
- 需要网络连接

### 2. 中文文献支持
- PubMed中中文文献较少
- 中华医学会检索需额外配置
- 建议使用英文检索

### 3. 文献数量限制
- 检索数量越多，处理时间越长
- 成本随文献数量线性增长
- 建议控制在30-100篇

### 4. AI分析准确性
- 依赖AI模型的性能
- 可能存在理解偏差
- 建议人工审核重要内容

## 扩展性

系统具有良好的扩展性，可以：

### 1. 添加新的数据源
在 `src/retrievers/` 中创建新的检索器类，实现统一接口。

### 2. 自定义分类模块
修改 `ContentClassifier.MODULES` 定义自己的分类体系。

### 3. 调整文档格式
修改 `WordGenerator` 中的样式和布局。

### 4. 集成其他AI模型
在 `ContentClassifier` 中添加新的AI提供商支持。

### 5. 添加Web界面
基于Flask/Django创建Web前端。

## 未来规划

- [ ] 添加文献缓存功能
- [ ] 实现并行AI分析
- [ ] 支持PDF导出
- [ ] 添加Web界面
- [ ] 支持批量处理
- [ ] 完善中文数据源
- [ ] 添加文献网络分析
- [ ] 支持协作功能

## 技术支持

### 文档
- [README.md](README.md) - 项目介绍和安装指南
- [USAGE_GUIDE.md](USAGE_GUIDE.md) - 详细使用说明
- [CHANGELOG.md](CHANGELOG.md) - 版本更新历史

### 测试
运行系统测试：
```bash
python test_system.py
```

### 帮助
查看命令行帮助：
```bash
python src/main.py --help
```

## 贡献指南

欢迎贡献代码、报告问题或提出建议：

1. Fork本项目
2. 创建特性分支
3. 提交更改
4. 推送到分支
5. 创建Pull Request

## 许可证

本项目仅供学习和研究使用。

## 免责声明

本系统生成的内容仅供参考，不构成医学建议。所有临床决策应遵循专业医学指导和临床实践。

---

**系统版本**: 1.0.0
**最后更新**: 2024
**开发语言**: Python 3.7+
**许可**: 学习研究使用
