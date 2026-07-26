# Dynamic Workflow - ERPNext高级审批工作流引擎

[![License: AGPL-3.0](https://img.shields.io/badge/License-AGPL%203.0-blue.svg)](https://www.gnu.org/licenses/agpl-3.0)
![Python 3.10+](https://img.shields.io/badge/Python-3.10%2B-green)
![ERPNext v16](https://img.shields.io/badge/ERPNext-v16-red)

Dynamic Workflow 是一个为 ERPNext V16 设计的高级工作流管理应用，提供灵活的审批矩阵、动态节点配置、以及完整的审批追踪功能。

## 📚 文档导航

> 🎯 **新用户？** 从[快速开始](#快速开始)或[快速参考](./QUICKSTART.md)开始！

| 文档 | 说明 |
|-----|------|
| 📖 [快速参考](./QUICKSTART.md) | 5分钟快速上手指南 |
| 📖 [安装指南](./docs/installation.md) | 详细的安装步骤和问题排查 |
| 📖 [文档类型说明](./docs/doctype_guide.md) | 核心数据模型和字段详解 |
| 📖 [API 文档](./docs/api.md) | 完整的 REST API 参考 |
| 📖 [最佳实践](./docs/best_practices.md) | 配置原则、性能优化和故障排查 |
| 📖 [架构设计](./docs/architecture.md) | 系统架构、数据流和扩展指南 |
| 📖 [贡献指南](./CONTRIBUTING.md) | 如何参与项目开发 |
| 📖 [更新日志](./CHANGELOG.md) | 版本历史和功能改进 |

---

## 📋 核心功能

### 1. **灵活的审批矩阵** 
- ✅ 按部门、角色、金额等多维度配置审批权限
- ✅ 支持多层级审批规则引擎
- ✅ 动态审批权限计算
- ✅ 优先级管理

### 2. **审批组织结构**
- ✅ 部门和团队的审批层级配置
- ✅ 灵活的汇报关系设置
- ✅ 多级审批链支持
- ✅ 组织结构自动同步

### 3. **审批权委托**
- ✅ 临时审批权转移
- ✅ 按日期范围的委托
- ✅ 自动过期管理
- ✅ 支持多人委托

### 4. **审批转办与加签**
- ✅ 审批过程中的转办
- ✅ 前加签和后加签支持
- ✅ 灵活的权限转移
- ✅ 完整的操作记录

### 5. **审批超时升级**
- ✅ 可配置的超时时间
- ✅ 多种升级动作 (自动通过/转移/通知)
- ✅ 定期催办提醒
- ✅ 升级规则引擎

### 6. **业务动作自动化**
- ✅ 审批完成后的自动操作
- ✅ 字段更新、API 调用、脚本执行
- ✅ 条件触发机制
- ✅ 错误处理和重试

### 7. **审批追踪和审计**
- ✅ 完整的审批历史记录
- ✅ 可视化审批流程时间线
- ✅ 详细的操作日志
- ✅ 合规审计支持

### 8. **多渠道通知**
- ✅ 邮件通知
- ✅ 企业微信集成 (可选)
- ✅ 短信通知支持 (可选)
- ✅ 自定义通知模板

### 9. **RESTful API & WebHook**
- ✅ 完整的 API 接口
- ✅ WebHook 事件支持
- ✅ 第三方系统对接
- ✅ 详细的 API 文档

---

## 🎯 支持的单据类型

- 📦 **物料需求计划** (Material Request)
- 📦 **采购订单** (Purchase Order)
- 📦 **销售订单** (Sales Order)
- 📦 **其他** *(可扩展)*

---

## 🛠 技术栈

| 组件 | 要求 |
|-----|------|
| 框架 | ERPNext v16 / Frappe v16 |
| Python | 3.10+ |
| 数据库 | MariaDB 10.3+ 或 PostgreSQL 12+ |
| 前端 | Frappe UI 框架 |
| 缓存 | Redis 4.0+ |

---

## 📦 安装指南

### 快速安装 (5分钟)

```bash
cd ~/frappe-bench
bench get-app https://github.com/fwr567/dynamic_workflow
bench install-app dynamic_workflow --site site.local
bench migrate --site site.local
bench restart
```

### 详细安装步骤

请参考 **[完整安装指南](./docs/installation.md)** 了解：
- 系统要求检查
- 步骤式安装说明
- 初始配置指南
- 常见问题解决
- 升级和卸载说明

---

## 🚀 快速开始

### 1. 创建第一个审批流 (10分钟)

```bash
# 1. 进入 ERPNext
# 2. 搜索 "Dynamic Workflow"
# 3. 进入应用
# 4. 点击 "工作流配置" → 新建
# 5. 选择单据类型和审批矩阵
# 6. 保存
```

### 2. 创建审批矩阵 (15分钟)

参考 **[快速参考](./QUICKSTART.md#3-创建审批矩阵-15分钟)** 了解详细步骤。

### 3. 配置通知 (可选)

- 邮件通知：在系统设置中配置 SMTP
- 企业微信：在应用设置中配置 WebHook

更多详情见 **[安装指南 - 通知配置](./docs/installation.md#配置-6-配置通知)**

---

## 💡 常见场景

### 场景1：按金额分级审批

需求：不同金额由不同级别审批

**参考**: [最佳实践 - 常见场景1](./docs/best_practices.md#场景1电商平台订单审批)

### 场景2：多部门并联审批

需求：多个部门同时审批，都同意才能通过

**参考**: [最佳实践 - 常见场景2](./docs/best_practices.md#场景2多部门协同审批)

### 场景3：权限委托

需求：出差时，权限临时委托给他人

**参考**: [快速参考 - 场景3](./QUICKSTART.md#场景3权限委托)

---

## 📊 数据模型

### 核心单据类型

| 单据 | 说明 |
|------|------|
| Approval Matrix | 审批矩阵规则定义 |
| Approval Matrix Rule | 审批矩阵具体规则 |
| Dynamic Workflow Config | 工作流启用配置 |
| Dynamic Node Template | 审批节点模板 |
| Approval Delegation | 审批权委托 |
| Approval Log | 审批日志追踪 |
| Workflow Timeout Escalation | 超时升级规则 |
| Business Action | 审批后业务动作 |
| Node Approval Step | 节点审批步骤 |
| Approval Chain Step | 审批链步骤 |

更多细节请参考 **[文档类型说明](./docs/doctype_guide.md)**

---

## 🔌 API 接口

### 获取待审批单据

```bash
curl -X GET "http://localhost:8000/api/method/dynamic_workflow.api.approval.get_pending_approvals?user=user@company.com"
```

### 提交审批

```bash
curl -X POST "http://localhost:8000/api/method/dynamic_workflow.api.approval.approve_document" \
  -d "doctype=Purchase Order" \
  -d "docname=PO-001" \
  -d "comments=已审批"
```

更多 API 示例请参考 **[完整 API 文档](./docs/api.md)**

---

## 🔧 常见问题

| 问题 | 答案 |
|-----|------|
| 如何查看待审批单据？ | 搜索 "待审批" 或访问 Dynamic Workflow 应用 |
| 如何跳过某个步骤？ | 在工作流配置中将步骤标记为 "可选" |
| 超时了怎么办？ | 系统自动发送催办邮件；48小时未处理会自动升级 |
| 能否添加新文档类型？ | 可以，参考 [架构设计 - 扩展指南](./docs/architecture.md#扩展指南) |

更多问题请参考 **[快速参考 - FAQ](./QUICKSTART.md#🔧-常见问题速查)** 或 [GitHub Discussions](https://github.com/fwr567/dynamic_workflow/discussions)

---

## 🔐 权限管理

### 默认角色

| 角色 | 权限 |
|-----|------|
| System Manager | 管理所有工作流配置 |
| Workflow Manager | 配置审批矩阵和规则 |
| Document Approver | 审批和处理文档 |
| Department Head | 部门级审批权 |

参考 **[安装指南 - 权限控制](./docs/installation.md#配置-1-创建审批管理员角色)** 了解详细配置

---

## 📈 性能

### 系统容量

| 指标 | 标准值 |
|-----|-------|
| 日审批单据数 | 1000+ |
| 审批日志查询 | <500ms |
| 矩阵规则计算 | <200ms |
| 并发审批用户 | 100+ |

### 优化建议

参考 **[最佳实践 - 性能优化](./docs/best_practices.md#性能优化建议)** 了解如何优化系统性能

---

## 🆘 获得帮助

### 寻求支持

1. **📖 文档** - 大多数问题都能在 [文档导航](#文档导航) 中找到答案
2. **��� Issue** - 在 [GitHub Issues](https://github.com/fwr567/dynamic_workflow/issues) 中搜索问题
3. **💬 讨论** - 在 [Discussions](https://github.com/fwr567/dynamic_workflow/discussions) 中提问
4. **📧 邮件** - 联系 fengweirui567@163.com

### 报告 Bug

1. 记录错误信息和操作步骤
2. [创建 Issue](https://github.com/fwr567/dynamic_workflow/issues/new)
3. 包含尽可能多的细节信息

---

## 🤝 贡献指南

欢迎提交 Pull Request 改进项目！

**贡献前请阅读 [CONTRIBUTING.md](./CONTRIBUTING.md)**

快速流程：
1. Fork 本仓库
2. 创建特性分支 (`git checkout -b feature/AmazingFeature`)
3. 提交更改 (`git commit -m 'feat: add amazing feature'`)
4. 推送到分支 (`git push origin feature/AmazingFeature`)
5. 开启 Pull Request

---

## 📄 许可证

本项目采用 **AGPL-3.0** 许可证 - 详见 [LICENSE](LICENSE) 文件。

---

## 👤 作者

- **fwr567** - 项目维护者
- 📧 邮箱: [fengweirui567@163.com](mailto:fengweirui567@163.com)
- 🔗 GitHub: [@fwr567](https://github.com/fwr567)

---

## 🙏 致谢

感谢 ERPNext 和 Frappe 社区的支持和贡献！

---

## 📊 项目统计

- ⭐ Stars: ![GitHub stars](https://img.shields.io/github/stars/fwr567/dynamic_workflow?style=social)
- 🍴 Forks: ![GitHub forks](https://img.shields.io/github/forks/fwr567/dynamic_workflow?style=social)
- 👁️ Watchers: ![GitHub watchers](https://img.shields.io/github/watchers/fwr567/dynamic_workflow?style=social)

---

## 🎯 下一步

✅ **已安装？** → 查看 [快速参考](./QUICKSTART.md)  
✅ **想要深入？** → 阅读 [最佳实践](./docs/best_practices.md)  
✅ **需要集成？** → 参考 [API 文档](./docs/api.md)  
✅ **想要贡献？** → 查看 [贡献指南](./CONTRIBUTING.md)

---

**最后更新**: 2026-07-26  
**当前版本**: 1.0.0  
**维护状态**: ✅ 积极维护
