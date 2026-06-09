# Dynamic Workflow 3.0

## 高级工作流引擎 - 为 ERPNext V16 增强的审批流系统

### 核心特性

#### 第一层：审批矩阵（Approval Matrix）
- 基于多维度条件的动态审批规则
- 支持金额范围、部门、业务线、项目类型、供应商等级
- 自定义 Python 条件表达式
- 串联/并联审批链配置

#### 第二层：组织关系引擎（Organization Relationship Engine）
- **灵活的审批者分配模式**：
  - 直属主管
  - 部门负责人
  - 条线负责人
  - 项目经理
  - 成本中心负责人
  - 指定角色
  - 自定义脚本

#### 第三层：动态节点（Dynamic Nodes）
- 运行时动态插入审批节点
- 基于文档属性的条件判断
- 不是预定义流程，而是真正的动态生成

#### 第四层：审批动作插件（Approval Actions Plugin）
11 种审批动作支持：
- 同意 (Approve)
- 拒绝 (Reject)
- 退回 (Return)
- 转办 (Forward)
- 加签 (Countersign)
- 会签 (Cosign)
- 委托 (Delegate)
- 催办 (Reminder)
- 抄送 (CC)
- 终止 (Terminate)
- 撤回 (Recall)

#### 第五层：业务动作引擎（Business Action Engine）
审批通过后自动执行：
- 创建采购订单
- 创建付款申请
- 生成会计凭证
- 发送邮件/企业微信
- 调用第三方 API
- 执行自定义脚本

### 增强功能

#### 审批记录中心（Workflow Timeline）
- 完整的审批记录跟踪
- 支持评论、附件、图片
- PDF 预览
- 审批时长统计

#### 审批代理（Approval Delegation）
- 支持按日期范围委托
- 指定文档类型或部门
- 自动生效
- 代理期限管理

#### 超时升级（Timeout Escalation）
- 24小时：发送催办
- 48小时：升级至上级主管
- 可配置的超时规则
- 自动化升级流程

#### 企业微信集成（WeChat Integration）
- 审批通知推送
- 在微信中直接审批
- 无需登录 ERP
- 支持回调处理

#### 审批分析（Approval Analytics）
- 平均审批时长
- 部门排名
- 审批瓶颈识别
- 退回率分析

### 安装使用

```bash
# 1. 克隆仓库到 apps 目录
cd ~/frappe-bench/apps
git clone https://github.com/fwr567/dynamic_workflow.git

# 2. 安装应用
cd ~/frappe-bench
bench --site your-site install-app dynamic_workflow

# 3. 迁移数据库
bench --site your-site migrate

# 4. 重启
bench restart
```

### 文件结构

```
dynamic_workflow/
├── README.md
├── setup.py
├── requirements.txt
├── dynamic_workflow/
│   ├── __init__.py
│   ├── hooks.py
│   ├── desktop.py
│   ├── modules.txt
│   ├── config/
│   │   └── desktop.py
│   ├── workflow_core/
│   │   ├── __init__.py
│   │   ├── approval_engine.py          # 核心审批引擎
│   │   ├── organization_engine.py      # 组织关系引擎
│   │   ├── dynamic_nodes.py            # 动态节点
│   │   ├── approval_actions.py         # 审批动作
│   │   ├── business_engine.py          # 业务动作引擎
│   │   ├── timeout_escalation.py       # 超时升级
│   │   ├── delegation.py               # 审批代理
│   │   └── doctype/
│   │       ├── approval_matrix/
│   │       ├── approval_delegation/
│   │       ├── dynamic_workflow_config/
│   │       ├── approval_log/
│   │       ├── workflow_timeout_escalation/
│   │       └── ...
│   ├── integrations/
│   │   ├── __init__.py
│   │   └── wechat_integration.py        # 企业微信集成
│   ├── api/
│   │   ├── __init__.py
│   │   ├── approval_api.py              # API 接口
│   │   ├── purchase_order_integration.py
│   │   └── ...
│   ├── reports/
│   │   ├── __init__.py
│   │   └── workflow_analytics_report.py # 审批分析报表
│   ├── public/
│   │   ├── js/
│   │   │   ├── approval_dialog.js
│   │   │   └── workflow_timeline.js
│   │   └── css/
│   │       └── workflow.css
│   └── templates/
│       └── emails/
│           ├── workflow_reminder.html
│           └── workflow_escalation.html
└── tests/
    └── __init__.py
```

### 快速开始

#### 1. 创建审批矩阵

1. 进入 Desk → Dynamic Workflow → Approval Matrix
2. 创建新的审批矩阵
3. 配置规则：
   - 金额：0 - 50,000
   - 审批链：部门负责人

#### 2. 创建动态工作流配置

1. 进入 Dynamic Workflow Config
2. 选择文档类型（如 Purchase Request）
3. 关联审批矩阵
4. 启用超时升级和企业微信集成

#### 3. 配置业务动作

在审批通过时自动执行操作：
- 创建采购订单
- 发送邮件通知
- 调用第三方 API

### API 接口

#### 提交审批

```python
frappe.call({
    'method': 'dynamic_workflow.api.approval_api.submit_approval',
    'args': {
        'document_type': 'Purchase Request',
        'document_name': 'PR-001',
        'action': 'Approve',
        'comments': '同意',
        'attachments': ['file1', 'file2']
    },
    'callback': function(r) { ... }
});
```

#### 获取审批记录

```python
frappe.call({
    'method': 'dynamic_workflow.api.approval_api.get_approval_logs',
    'args': {
        'document_type': 'Purchase Request',
        'document_name': 'PR-001'
    },
    'callback': function(r) { ... }
});
```

### 企业微信集成配置

1. 创建 WeChat Config 单据
2. 填入企业微信配置：
   - Corp ID
   - Corp Secret
   - Agent ID
3. 启用审批消息推送

### 许可证

GNU General Public License v3

### 支持

如有问题或建议，请提交 Issue 或 Pull Request
