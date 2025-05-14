# 🤖 Agent模型测试框架

<div align="center">

[![Python Version](https://img.shields.io/badge/python-3.8%2B-blue.svg)](https://www.python.org/downloads/)
[![License: MIT](https://img.shields.io/badge/License-MIT-yellow.svg)](https://opensource.org/licenses/MIT)
[![Code Style](https://img.shields.io/badge/code%20style-black-000000.svg)](https://github.com/psf/black)

</div>

## 📝 项目简介

这是一个专门用于测试和评估各种Agent模型性能的综合性测试框架。该框架提供了标准化的测试流程、自动化测试脚本以及详细的性能评估指标，帮助开发者更好地理解和优化Agent模型的表现。

## ✨ 主要特性

- 🧪 完整的测试套件
  - 单元测试
  - 集成测试
  - 性能测试
- 📊 多维度评估指标
  - 准确率
  - 响应时间
  - Token使用量
  - 成本分析
- 🔄 自动化测试流程
- 📈 性能基准测试
- 📝 详细的测试报告生成

## 🏗️ 项目结构

```
.
├── README.md                 # 项目说明文档
├── requirements.txt          # Python依赖包
├── .gitignore               # Git忽略文件配置
├── tests/                    # 测试用例目录
│   ├── unit/                # 单元测试
│   │   ├── component_test.py
│   │   ├── intent_test.py
│   │   ├── offline_map_test.py
│   │   └── parameter_extraction_test.py
│   ├── integration/         # 集成测试
│   │   └── online_all_test.py
│   └── performance/         # 性能测试
├── src/                     # 源代码目录
│   ├── models_prompt/       # 模型提示词
│   │   └── prompt.py
│   ├── utils/              # 工具函数
│   └── config/             # 配置文件
├── data/                    # 测试数据目录
│   ├── component/          # 组件测试数据
│   ├── intent/             # 意图测试数据
│   ├── offline_map/        # 离线地图测试数据
│   └── parameter_extraction/ # 参数提取测试数据
├── docs/                    # 文档目录
└── scripts/                 # 实用脚本
```

## 🚀 快速开始

### 环境要求

- Python 3.8+
- pip 包管理器

### 安装步骤

1. 克隆仓库：
```bash
git clone [repository-url]
cd agent-model-test
```

2. 创建虚拟环境（推荐）：
```bash
python -m venv venv
source venv/bin/activate  # Linux/Mac
# 或
.\venv\Scripts\activate  # Windows
```

3. 安装依赖：
```bash
pip install -r requirements.txt
```

### 运行测试

1. 运行所有测试：
```bash
python scripts/run_all_tests.py
```

2. 运行特定测试：
```bash
python scripts/run_test.py --test-type [test_type] --model [model_name]
```

## 📊 测试指标说明

- **准确率**：模型回答的准确程度
- **响应时间**：模型处理请求所需时间
- **Token使用量**：模型消耗的token数量
- **成本**：API调用产生的费用

## 🤝 贡献指南

1. Fork 项目
2. 创建特性分支 (`git checkout -b feature/AmazingFeature`)
3. 提交更改 (`git commit -m 'Add some AmazingFeature'`)
4. 推送到分支 (`git push origin feature/AmazingFeature`)
5. 创建 Pull Request

## 📄 许可证

本项目采用 MIT 许可证 - 查看 [LICENSE](LICENSE) 文件了解详情

## 📞 联系方式

- 项目维护者：[您的名字]
- 邮箱：[您的邮箱]
- 项目链接：[项目URL]

## 🙏 致谢

感谢所有为本项目做出贡献的开发者！