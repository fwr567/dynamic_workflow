# Dynamic Workflow - ERPNext高级审批工作流引擎

[![License: AGPL-3.0](https://img.shields.io/badge/License-AGPL%203.0-blue.svg)](https://www.gnu.org/licenses/agpl-3.0)
![Python 3.10+](https://img.shields.io/badge/Python-3.10%2B-green)
![ERPNext v16](https://img.shields.io/badge/ERPNext-v16-red)

Dynamic Workflow 是一个为 ERPNext V16 设计的高级工作流管理应用，提供灵活的审批矩阵、动态节点配置、以及完整的审批追踪功能。

## 📋 核心功能

### 1. **审批矩阵管理** 
- 按部门、角色、金额等多维度配置审批权限
- 支持灵活的审批规则引擎
- 实时审批权限计算

### 2. **审批组织结构**
- 组织部门/团队的审批层级配置
- 灵活的汇报关系设置
- 多级审批链配置

### 3. **审批模板**
- 预定义审批流程模板
- 快速流程部署
- 模板版本管理

### 4. **审批���托**
- 临时审批权转移
- 指定时间范围内有效
- 自动同步与过期管理

### 5. **审批转办**
- 当前审批人可转办至他人
- 记录转办历史
- 支持多次转办

### 6. **审批加签**
- 审批过程中添加加签人
- 支持前加签和后加签
- 灵活的加签规则

### 7. **审批回退**
- 支持退回至指定审批节点
- 记录回退原因
- 自动重新流转

### 8. **审批轨迹**
- 完整的审批历史记录
- 可视化审批流程图
- 详细的操作日志

### 9. **审批附件**
- 支持上传审批相关附件
- 版本控制
- 权限管理

### 10. **审批意见模板**
- 常用审批意见预定义
- 快速选择和使用
- 自定义意见库

### 11. **审批催办**
- 逾期审批提醒
- 多渠道通知（邮件、企业微信等）
- 可配置催办规则

### 12. **审批超时**
- 自动超时升级
- 自动转办至管理员
- 超时规则配置

### 13. **审批代理**
- 设置代理审批人
- 代理权限范围限制
- 代理有效期管理

### 14. **审批事件**
- 审批流程事件触发
- Webhook支持
- 自定义事件处理

## 🎯 支持的单据类型

- **物料需求计划 (Material Request)**
- **采购订单 (Purchase Order)**
- **销售订单 (Sales Order)**
- *(可扩展至其他单据类型)*

## 🛠 技术栈

- **框架**: ERPNext v16 / Frappe
- **语言**: Python 3.10+
- **数据库**: MariaDB / PostgreSQL
- **前端**: Frappe UI 框架

## 📦 安装指南

### 前置条件
- ERPNext v16 已安装
- Frappe Bench 环境已配置
- Python 3.10 或更高版本

### 安装步骤

1. **克隆应用到 Bench 应用目录**
```bash
cd ~/frappe-bench
git clone https://github.com/fwr567/dynamic_workflow apps/dynamic_workflow
```

2. **安装应用**
```bash
bench get-app dynamic_workflow
bench install-app dynamic_workflow
```

3. **执行数据库迁移**
```bash
bench migrate
```

4. **重启 Bench**
```bash
bench restart
```

5. **在浏览器中访问**
```
http://localhost:8000
```

然后在 Awesome Bar 中搜索 "Dynamic Workflow" 进入应用。

## 🚀 快速开始

### 1. 配置审批矩阵

访问 **Dynamic Workflow > 审批矩阵** 新建规则：

```
文档类型: 采购订单
条件: 金额 > 10000
审批人: 采购部经理
优先级: 1
```

### 2. 设置审批模板

创建审批模板以快速应用到不同单据类型：

```
模板名称: 标准采购审批流
步骤1: 部门主管审批
步骤2: 采购部审��
步骤3: 财务部审批
```

### 3. 配置触发单据

在 **Dynamic Workflow Config** 中启用需要工作流的单据类型。

### 4. 启动审批流程

创建采购订单时，系统将自动触发对应的审批流程。

## 📊 数据模型

### 核心单据类型

| 单据 | 说明 |
|------|------|
| Approval Matrix | 审批矩阵规则定义 |
| Approval Matrix Rule | 审批矩阵具体规则 |
| Dynamic Workflow Config | 工作流配置 |
| Dynamic Node Template | 审批节点模板 |
| Approval Delegation | 审批权委托 |
| Approval Log | 审批日志追踪 |
| Workflow Timeout Escalation | 超时升级规则 |
| Business Action | 审批后业务动作 |
| Node Approval Step | 节点审批步骤 |
| Approval Chain Step | 审批链步骤 |

## 🔌 API 接口

### 获取审批矩阵

```python
from dynamic_workflow.api.approval_matrix import get_approval_matrix

matrix = get_approval_matrix(
    doctype="Purchase Order",
    approval_amount=50000,
    department="采购部"
)
```

### 获取审批流程

```python
from dynamic_workflow.api.workflow_engine import get_workflow_chain

chain = get_workflow_chain(
    doctype="Sales Order",
    document_name="SO-001"
)
```

### 记录审批日志

```python
from dynamic_workflow.dynamic_workflow.approval_engine import log_approval

log_approval(
    doctype="Purchase Order",
    document_name="PO-001",
    approver="user@company.com",
    action="Approved",
    comments="已核准"
)
```

## ⚙️ 配置选项

### 环境变量

在 `hooks.py` 中可配置：

```python
# 是否启用微信集成
ENABLE_WECHAT_NOTIFICATION = True

# 是否启用邮件通知
ENABLE_EMAIL_NOTIFICATION = True

# 超时升级间隔 (小时)
TIMEOUT_ESCALATION_INTERVAL = 24
```

## 🔐 权限控制

- **审批矩阵管理**: 需要系统管理员角色
- **工作流配置**: 需要工作流管理员角色
- **审批操作**: 基于审批矩阵规则动态分配

## 📱 微信集成 *(可选)*

配置企业微信机器人以获取审批通知：

1. 在企业微信中创建机器人
2. 在 Dynamic Workflow 设置中配置 Webhook URL
3. 启用微信通知选项

## 🐛 常见问题

### Q: 如何添加新的单据类型支持？
A: 编辑 `dynamic_workflow/hooks.py`，在 `doc_events` 字典中添加新的单据类型及其事件处理函数。

### Q: 审批流程如何与业务流程联动？
A: 在 **Business Action** 中定义审批完成后的业务动作（如自动转为已确认状态）。

### Q: 如何导出审批报表？
A: 在 **Approval Log** 列表视图中使用"导出"功能，支持 Excel/CSV 格式。

### Q: 如何处理紧急审批？
A: 使用"加签"功能快速添加高级审批人，或使用"审批代理"功能临时委托权限。

## 📚 文档与资源

- [ERPNext 官方文档](https://docs.erpnext.com)
- [Frappe 框架文档](https://frappeframework.com)
- [工作流最佳实践](./docs/best-practices.md) *(待补充)*

## 🤝 贡献指南

欢迎提交 Pull Request 来改进这个项目！

1. Fork 本仓库
2. 创建特性分支 (`git checkout -b feature/AmazingFeature`)
3. 提交更改 (`git commit -m 'Add AmazingFeature'`)
4. 推送到分支 (`git push origin feature/AmazingFeature`)
5. 开启 Pull Request

## 📄 许可证

本项目采用 AGPL-3.0 许可证 - 详见 [LICENSE](LICENSE) 文件。

## 👤 作者

- **fwr567** - 项目维护者
- 联系邮箱: [fengweirui567@163.com](mailto:fengweirui567@163.com)

## 🙏 致谢

感谢 ERPNext 和 Frappe 社区的支持和贡献！

---

**最后更新**: 2026-07-26  
**当前版本**: 1.0.0
