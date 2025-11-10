# 使用指南

## 快速上手

### 第一步：安装配置

1. **安装Python依赖**
```bash
pip install -r requirements.txt
```

2. **配置API密钥**
```bash
cp .env.example .env
# 编辑 .env 文件，填入你的API密钥
```

需要配置的密钥：
- `OPENAI_API_KEY` 或 `ANTHROPIC_API_KEY`（必须配置其中一个）
- `NCBI_EMAIL`（必填，你的邮箱地址）
- `NCBI_API_KEY`（可选，但建议配置）

### 第二步：运行示例

最简单的使用方式：

```bash
python src/main.py --disease "diabetes" --email "your@email.com" --skip-cma
```

这将：
- 从PubMed检索关于"diabetes"（糖尿病）的文献
- 跳过中华医学会检索（因为需要额外配置）
- 使用AI分析文献内容
- 生成Word文档到 `output/` 目录

### 第三步：查看结果

生成的Word文档位于 `output/` 目录，文件名格式为：
```
[疾病名称]_文献汇总_[时间戳].docx
```

## 常见使用场景

### 场景1：快速了解某个疾病

```bash
python src/main.py \
  --disease "hypertension" \
  --max-results 20 \
  --skip-cma
```

这会检索20篇关于高血压的高质量文献（综述、指南等）。

### 场景2：深度研究某个疾病

```bash
python src/main.py \
  --disease "type 2 diabetes" \
  --max-results 100 \
  --filter-types Review Guideline Meta-Analysis
```

这会检索100篇文献，只包括综述、指南和荟萃分析。

### 场景3：使用中文疾病名称

```bash
python src/main.py \
  --disease "糖尿病" \
  --skip-cma
```

PubMed也支持中文搜索，但建议使用英文以获得更好的结果。

### 场景4：使用Anthropic Claude（成本更低）

```bash
python src/main.py \
  --disease "asthma" \
  --ai-provider anthropic \
  --skip-cma
```

Claude Haiku模型比GPT-4更便宜，适合大批量处理。

## 输出文档说明

生成的Word文档包含以下内容：

### 1. 文献概览
- 检索到的文献总数
- 各模块的文献数量分布

### 2. 四个核心模块

每个模块包含：

**病因诱因**
- 综合摘要：总结该疾病的主要病因和风险因素
- 相关文献：列出具体文献及其关键发现

**发病机制**
- 综合摘要：阐述疾病的病理生理过程
- 相关文献：详细的机制研究

**诊断与鉴别**
- 综合摘要：诊断标准和方法
- 相关文献：诊断相关的研究和指南

**治疗与预后**
- 综合摘要：治疗方案和预后评估
- 相关文献：治疗相关的临床研究

### 3. 完整参考文献列表

所有引用文献的完整列表，包括：
- 标题
- 作者
- 期刊
- 发表日期
- PubMed链接（可点击访问原文）

## 参数详解

### 必填参数

- `--disease`: 疾病名称，建议使用英文
- `--email`: 你的邮箱地址（NCBI要求）

### 常用可选参数

- `--max-results`: 检索文献数量（默认30）
  - 推荐范围：20-100
  - 数量越多，AI分析时间和成本越高

- `--skip-cma`: 跳过中华医学会检索
  - 建议添加此参数（除非你已配置中文数据源）

- `--ai-provider`: 选择AI服务
  - `openai`: 默认，使用GPT-4o-mini
  - `anthropic`: 使用Claude Haiku，成本更低

### 高级参数

- `--filter-types`: 过滤文献类型
  ```bash
  --filter-types Review Guideline  # 只要综述和指南
  --filter-types "Clinical Trial"  # 只要临床试验
  ```

- `--output`: 自定义输出路径
  ```bash
  --output "reports/my_report.docx"
  ```

- `--ncbi-api-key`: NCBI API密钥
  - 配置后可提高检索速度10倍
  - 在 [NCBI Account](https://www.ncbi.nlm.nih.gov/account/) 获取

## 成本估算

### AI API成本（以30篇文献为例）

**OpenAI GPT-4o-mini**
- 分类30篇文献：约 $0.05-0.10
- 生成4个模块摘要：约 $0.02-0.05
- 总计：约 $0.07-0.15

**Anthropic Claude Haiku**
- 分类30篇文献：约 $0.02-0.05
- 生成4个模块摘要：约 $0.01-0.03
- 总计：约 $0.03-0.08

注意：
- 实际成本取决于文献长度和摘要详细程度
- 检索更多文献会成比例增加成本

### 时间估算

- 检索30篇文献：1-2分钟
- AI分析30篇文献：2-5分钟
- 生成文档：10-30秒
- 总计：约5-10分钟

## 最佳实践

### 1. 疾病名称选择

✅ 推荐：
- 使用英文标准医学术语
- 例如："diabetes mellitus", "hypertension", "coronary artery disease"

❌ 不推荐：
- 使用缩写（如"DM"、"HTN"）
- 使用过于宽泛的词（如"cancer"）

### 2. 文献数量选择

- **快速了解**：20-30篇
- **深入研究**：50-100篇
- **专题综述**：100+篇

注意：数量越多，成本越高，处理时间越长。

### 3. 文献类型选择

根据需求选择：
- **临床指南**：`--filter-types Guideline`
- **综述文章**：`--filter-types Review Meta-Analysis`
- **最新研究**：`--filter-types "Clinical Trial"`
- **综合信息**：`--filter-types Review Guideline Meta-Analysis Clinical Trial`（默认）

### 4. 节省成本的技巧

1. 先用小数量测试（如 `--max-results 10`）
2. 使用 Anthropic Claude（成本更低）
3. 使用NCBI API密钥（加快检索，减少等待时间）
4. 缓存检索结果，避免重复检索

## 常见问题

### Q1: 如何获取API密钥？

**OpenAI**:
1. 访问 https://platform.openai.com/
2. 注册并充值账户
3. 在 API Keys 页面创建密钥

**Anthropic**:
1. 访问 https://console.anthropic.com/
2. 注册账户
3. 获取API密钥

**NCBI** (可选):
1. 访问 https://www.ncbi.nlm.nih.gov/account/
2. 注册账户
3. 在设置中生成API密钥

### Q2: 为什么建议使用 --skip-cma？

因为中华医学会文献检索需要：
- CNKI或万方数据的访问权限
- 额外的配置和开发
- 可能遇到反爬虫限制

当前版本主要依赖PubMed，已经包含大量高质量文献。

### Q3: 可以检索中文文献吗？

可以，但：
- PubMed中的中文文献较少
- 建议使用英文疾病名称获得更多结果
- 如需大量中文文献，建议配置CNKI或万方数据接口

### Q4: 生成的文档可以编辑吗？

可以！生成的Word文档是标准的.docx格式，可以用Microsoft Word或WPS等软件打开编辑。

### Q5: 如何处理网络问题？

如果遇到网络问题：
1. 检查是否能访问 https://eutils.ncbi.nlm.nih.gov/
2. 检查是否能访问AI服务API
3. 如有代理需求，在代码中配置代理设置
4. 尝试减少 `--max-results` 数量

### Q6: 文献质量如何保证？

系统默认过滤高质量文献类型：
- Review（综述）：经过系统性总结
- Guideline（指南）：权威机构发布
- Meta-Analysis（荟萃分析）：基于多项研究
- Clinical Trial（临床试验）：实证研究

### Q7: 可以批量处理多个疾病吗？

可以写一个简单的脚本：

```bash
#!/bin/bash
diseases=("diabetes" "hypertension" "asthma")
for disease in "${diseases[@]}"; do
    python src/main.py --disease "$disease" --skip-cma
done
```

## 技术支持

如遇到问题：

1. 查看README.md的"故障排除"部分
2. 检查Python和依赖版本是否正确
3. 查看错误信息并搜索解决方案
4. 提交GitHub Issue

## 更新日志

查看项目的版本更新历史，了解新功能和改进。

---

祝你使用愉快！如有任何问题，欢迎反馈。
