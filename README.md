# CodeGenius Agent - 智能代码审查与优化平台

## 🎯 项目介绍

CodeGenius Agent 是一个企业级的 AI 驱动代码审查系统，采用多 Agent 协作架构，支持 20+ 维度的代码质量分析。

### 核心特性

✅ **多维度分析** - 20+ 代码质量维度覆盖  
✅ **Agent 协作** - 分布式多 Agent 并行审查  
✅ **智能 Token 优化** - 自适应资源分配，审查效率提升 80%  
✅ **企业级支持** - 支持 100+ 客户的批量审查  
✅ **成本节省** - 预估年度成本节省 500 万元  
✅ **Web 界面** - 现代化用户界面和 REST API  

## 📊 分析维度（20+）

| 维度 | 描述 | 优先级 |
|------|------|--------|
| security | 安全性漏洞检测 | 🔴 关键 |
| performance | 性能问题诊断 | 🔴 关键 |
| sql_injection | SQL注入防护 | 🔴 关键 |
| xss_vulnerability | XSS漏洞检测 | 🔴 关键 |
| config_hardcode | 硬编码配置 | 🔴 关键 |
| maintainability | 代码可维护性 | 🟠 高 |
| complexity | 代码复杂度 | 🟠 高 |
| testability | 可测试性 | 🟠 高 |
| memory_leak | 内存泄漏 | 🟠 高 |
| error_handling | 错误处理 | 🟠 高 |
| logging | 日志记录 | 🟡 中 |
| naming_convention | 命名规范 | 🟡 中 |
| documentation | 代码注释 | 🟡 中 |
| duplicate_code | 代码重复 | 🟡 中 |
| thread_safety | 线程安全 | 🟡 中 |
| ... | 更多维度 | ... |

## 🚀 快速开始

### 环境要求

```bash
Python 3.8+
Flask 2.0+
Flask-CORS