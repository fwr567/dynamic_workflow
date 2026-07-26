# Dynamic Workflow 项目架构与文件结构

## 项目结构概览

```
dynamic_workflow/
├── README.md                           # 项目说明文档
├── LICENSE                             # AGPL-3.0 许可证
├── pyproject.toml                      # Python 项目配置
├── dynamic_workflow/
│   ├── __init__.py                     # 包初始化
│   ├── hooks.py                        # Frappe 钩子配置
│   ├── modules.txt                     # 模块列表
│   ├── patches.txt                     # 数据库补丁列表
│   │
│   ├── api/                            # API 接口模块
│   │   ├── __init__.py
│   │   ├── approval.py                 # 审批操作 API
│   │   ├── approval_matrix.py          # 审批矩阵 API
│   │   ├── delegation.py               # 委托管理 API
│   │   ├── document_integration.py     # 文档集成 API
│   │   └── workflow.py                 # 工作流查询 API
│   │
│   ├── dynamic_workflow/               # 核心业务逻辑
│   │   ├── __init__.py
│   │   ├── approval_engine.py          # 审批引擎
│   │   ├── approval_actions.py         # 审批动作处理
│   │   ├── business_engine.py          # 业务动作引擎
│   │   ├── organization_engine.py      # 组织结构引擎
│   │   ├── dynamic_nodes.py            # 动态节点处理
│   │   ├── delegation.py               # 委托处理
│   │   ├── timeout_escalation.py       # 超时升级处理
│   │   │
│   │   └── doctype/                    # 文档类型定义
│   │       ├── __init__.py
│   │       ├── approval_matrix/
│   │       ├── approval_matrix_rule/
│   │       ├── dynamic_workflow_config/
│   │       ├── approval_log/
│   │       ├── approval_delegation/
│   │       ├── workflow_timeout_escalation/
│   │       ├── dynamic_node_template/
│   │       ├── node_approval_step/
│   │       ├── approval_chain_step/
│   │       └── business_action/
│   │
│   ├── config/                         # 配置模块
│   │   ├── __init__.py
│   │   ├── desktop.py                  # 桌面菜单配置
│   │   ├── custom_fields.py            # 自定义字段配置
│   │   └── permissions.py              # 权限配置
│   │
│   ├── setup/                          # 安装和初始化
│   │   ├── __init__.py
│   │   └── install.py                  # 安装脚本
│   │
│   ├── integrations/                   # 第三方集成
│   │   ├── __init__.py
│   │   ├── notification.py             # 邮件/短信/微信通知
│   │   ├── wechat.py                   # 企业微信集成
│   │   └── webhook.py                  # WebHook 集成
│   │
│   ├── templates/                      # HTML 模板
│   │   ├── approval_timeline.html      # 审批时间线模板
│   │   └── approval_detail.html        # 审批详情页面
│   │
│   ├── public/                         # 静态资源
│   │   ├── js/
│   │   │   ├── approval_dialog.js      # 审批对话框
│   │   │   ├── workflow_timeline.js    # 时间线组件
│   │   │   └── approval_utils.js       # 工具函数
│   │   └── css/
│   │       ├── workflow.css            # 工作流样式
│   │       └── approval_timeline.css   # 时间线样式
│   │
│   ├── fixtures/                       # 初始数据
│   │   ├── workspace.json              # 工作区配置
│   │   └── custom_field.json           # 自定义字段
│   │
│   └── patches/                        # 数据库补丁
│       ├── __init__.py
│       └── v1/
│           └── create_default_roles.py # v1 初始补丁
│
└── docs/                               # 文档目录
    ├── doctype_guide.md                # 文档类型指南
    ├── best_practices.md               # 最佳实践
    ├── api.md                          # API 文档
    ├── installation.md                 # 安装指南
    ├── architecture.md                 # 架构说明
    └── changelog.md                    # 更新日志
```

---

## 核心模块说明

### 1. API 模块 (`api/`)

提供对外接口，供前端和第三方系统调用。

#### approval.py
```python
# 主要函数
@frappe.whitelist()
def approve_document(doctype, docname, comments, approval_log_id)
    # 提交审批

@frappe.whitelist()
def reject_document(doctype, docname, rejection_reason, reject_to_step)
    # 拒绝审批

@frappe.whitelist()
def get_pending_approvals(user, limit=20)
    # 获取待审批单据列表
```

#### approval_matrix.py
```python
def get_approval_matrix(doctype, amount, department)
    # 获取适用的审批矩阵

def calculate_approvers(matrix_rules, document)
    # 计算具体审批人列表
```

#### document_integration.py
```python
def attach_dynamic_workflow(doc, method)
    # 单据创建时，检查是否需要附加工作流

def validate_approval(doc, method)
    # 单据提交前，验证审批是否完成

def execute_business_actions(doc, method)
    # 所有审批通过后，执行业务动作
```

### 2. 业务逻辑模块 (`dynamic_workflow/`)

#### approval_engine.py
```python
class ApprovalEngine:
    def __init__(self, doctype, docname):
        # 初始化审批引擎
        
    def get_current_step(self)
        # 获取当前审批步骤
        
    def get_next_approvers(self)
        # 获取下一步的审批人
        
    def submit_approval(self, approver, action, comments)
        # 提交审批操作
        
    def can_approve(self, user)
        # 检查用户是否有权审批
```

#### organization_engine.py
```python
class OrganizationEngine:
    def get_department_hierarchy(department_id)
        # 获取部门��级结构
        
    def get_reporting_line(user_id)
        # 获取员工的汇报线
        
    def get_users_by_role(role_name, department=None)
        # 获取指定角色的用户列表
```

#### timeout_escalation.py
```python
def check_and_escalate()
    # 定时检查和升级超期审批 (hourly)
    
def escalate_single_approval(approval_log)
    # 对单条审批进行升级处理
    
def notify_approver(approval_log, reminder_count)
    # 发送超期提醒通知
```

#### delegation.py
```python
def sync_delegations()
    # 同步委托状态，过期委托改为 Expired (daily)
    
def get_delegatee(delegator, doctype=None)
    # 获取某个用户在特定单据类型上的被委托人
    
def is_delegation_active(delegation_id)
    # 检查委托是否仍然有效
```

### 3. 文档类型模块 (`dynamic_workflow/doctype/`)

每个文档类型文件夹包含：
- `doctype_name.json` - 文档类型定义
- `doctype_name.py` - 业务逻辑类
- `doctype_name.js` - 前端逻辑

#### approval_matrix/ - 审批矩阵
定义审批规则的主表

#### approval_log/ - 审批日志
记录每一条审批操作的详细信息

#### approval_delegation/ - 审批委托
记录权限委托关系

#### dynamic_workflow_config/ - 工作流配置
配置哪些文档类型启用工作流

#### workflow_timeout_escalation/ - 超时升级规则
定义超时后的自动升级规则

### 4. 配置模块 (`config/`)

#### desktop.py
```python
# 定义应用在桌面上的菜单和模块
def get_desk_sidebar_items():
    return [
        {
            "label": "Dynamic Workflow",
            "items": [
                "Approval Matrix",
                "Approval Log",
                "Approval Delegation"
            ]
        }
    ]
```

#### custom_fields.py
```python
# 为标准文档类型添加自定义字段
CUSTOM_FIELDS = {
    "Purchase Order": [
        {
            "fieldname": "approval_status",
            "label": "Approval Status",
            "fieldtype": "Select"
        }
    ]
}
```

### 5. 集成模块 (`integrations/`)

#### notification.py
```python
def send_approval_notification(approval_log):
    # 根据配置的通知方式发送通知
    
def send_email(recipient, subject, message)
def send_wechat(recipient, message)
def send_sms(recipient, message)
```

#### wechat.py
```python
def send_wechat_approval_message(approver, document):
    # 发送企业微信消息通知审批
    
def send_wechat_reminder(approver, document, hours_overdue):
    # 发送企业微信超期提醒
```

#### webhook.py
```python
def trigger_webhook(event_type, data):
    # 触发 WebHook 通知外部系统
    
WEBHOOK_EVENTS = [
    "approval.submitted",
    "approval.rejected",
    "approval.escalated"
]
```

---

## 数据流详解

### 单据审批流程

```
┌─────────────────────┐
│   创建/编辑单据      │
└──────────┬──────────┘
           │
           ▼
┌─────────────────────────────┐
│  before_insert 钩子触发      │
│  attach_dynamic_workflow()  │
└──────────┬──────────────────┘
           │
           ├─ 检查是否启用工作流
           ├─ 获取审批矩阵
           └─ 初始化审批引擎
           │
           ▼
┌──────────────────────────────┐
│   显示审批按钮                │
│  (提交前需完成审批)           │
└──────────┬───────────────────┘
           │
           ▼
┌──────────────────────────────┐
│   用户点击 [审批] 按钮         │
│  (打开审批对话框)             │
└──────────┬───────────────────┘
           │
           ▼
┌──────────────────────────────┐
│  approve_document() API      │
│  (前端调用后端)              │
└──────────┬───────────────────┘
           │
           ├─ 验证用户权限
           ├─ 保存审批意见
           ├─ 创建 Approval Log
           └─ 检查是否所有步骤完成
           │
           ▼ (所有审批通过)
┌──────────────────────────────┐
│   execute_business_actions()  │
│   (执行业务动作)              │
└──────────┬───────────────────┘
           │
           ▼
┌──────────────────────────────┐
│   提交文档                    │
│   (标记为已提交)              │
└──────────────────────────────┘
```

### 权限委托流程

```
┌──────────────────────┐
│  创建委托记录         │
│ (delegator → delegatee)
└──────────┬───────────┘
           │
           ▼
┌──────────────────────────────┐
│  sync_delegations()          │
│  (每日自动检查)              │
└──────────┬───────────────────┘
           │
           ├─ 检查委托是否过期
           ├─ 过期委托改为 Expired
           └─ 活跃委托保持 Active
           │
           ▼
┌──────────────────────────────┐
│  get_delegatee()             │
│  (审批时调用)                │
└──────────┬───────────────────┘
           │
           ├─ 检查是否有活跃委托
           ├─ 有则改为被委托人审批
           └─ 无则由原审批人审批
           │
           ▼
┌──────────────────────────────┐
│  Approval Log 记录委托        │
│  (delegation_used 字段)      │
└──────────────────────────────┘
```

### 超时升级流程

```
┌────────────────────────────┐
│  check_and_escalate()      │
│  (每小时运行一次)          │
└──────────┬─────────────────┘
           │
           ▼
┌────────────────────────────────┐
│  查询所有待审批的记录           │
│  (Approval Log, status=Pending)│
└──────────┬─────────────────────┘
           │
           ▼
┌────────────────────────────────┐
│  检查是否超过超时时间           │
└──────────┬─────────────────────┘
           │
    ┌──────┴───────┐
    │              │
 未超时            已超时
    │              │
    │              ▼
    │     ┌─────────────────────┐
    │     │ 根据规则执行升级动作 │
    │     │ (Auto Approve/      │
    │     │  Reassign/Notify)   │
    │     └─────────────────────┘
    │              │
    │              ▼
    │     ┌──────────────────────┐
    │     │ 发送催办通知         │
    │     │ (邮件/微信/短信)     │
    │     └──────────────────────┘
    │              │
    └──────┬───────┘
           │
           ▼
    ┌──────────────────────┐
    │ 更新 Approval Log    │
    │ (记录升级操作)       │
    └──────────────────────┘
```

---

## 关键算法

### 1. 审批人计算算法

```python
def calculate_approvers(doctype, document, matrix):
    """
    根据矩阵规则计算审批人
    
    算法步骤：
    1. 遍历所有启用的矩阵规则
    2. 按优先级排序
    3. 对每个规则检查条件匹配
    4. 条件匹配则计算审批人
    5. 使用该规则的审批链
    """
    applicable_rules = []
    
    for rule in matrix.approval_rules:
        if check_conditions(rule, document):
            applicable_rules.append(rule)
    
    # 按优先级排序
    applicable_rules.sort(key=lambda r: r.priority)
    
    if applicable_rules:
        selected_rule = applicable_rules[0]
        
        # 如果指定了具体审批人
        if selected_rule.approver:
            return [selected_rule.approver]
        
        # 如果指定了审批角色
        if selected_rule.approver_role:
            users = get_users_by_role(selected_rule.approver_role)
            return users
    
    return []
```

### 2. 权限校验算法

```python
def can_approve(user, document, approval_step):
    """
    判断用户是否有权审批
    
    检查优先级：
    1. 是否为 System Manager
    2. 是否在委托名单中
    3. 是否在该步骤的审批人名单中
    4. 用户所属角色是否在审批角色中
    """
    # 检查1: System Manager 可以审批任何单据
    if has_role(user, "System Manager"):
        return True
    
    # 检查2: 是否有有效的委托
    delegation = get_active_delegation(user, document.doctype)
    if delegation:
        return True
    
    # 检查3: 是否在当前步骤的审批人中
    current_approvers = get_current_approvers(document, approval_step)
    if user in current_approvers:
        return True
    
    # 检查4: 用户角色是否在审批角色中
    approver_roles = get_current_approver_roles(document, approval_step)
    user_roles = get_user_roles(user)
    
    for role in user_roles:
        if role in approver_roles:
            return True
    
    return False
```

### 3. 流程分支算法 (并联/串联)

```python
def should_move_to_next_step(approval_log, approval_type):
    """
    判断是否应该进入下一个审批步骤
    
    串联 (Serial): 前一步完成后立即进入下一步
    并联 (Parallel): 所有并联步骤都完成后才进入下一步
    任意一人 (Any One): 任意一人审批通过即可进入下一步
    """
    current_step = approval_log.approval_step
    
    if approval_type == "Serial":
        # 串联：检查前一步是否已完成
        previous_logs = get_approval_logs(
            current_step - 1,
            approval_log.document_name
        )
        return all(log.status == "Approved" for log in previous_logs)
    
    elif approval_type == "Parallel":
        # 并联：检查同步骤的所有审批人是否都完成
        parallel_logs = get_approval_logs(
            current_step,
            approval_log.document_name
        )
        return all(log.status in ["Approved", "Rejected"] for log in parallel_logs)
    
    elif approval_type == "Any One":
        # 任意一人：检查是否有一个审批通过
        any_logs = get_approval_logs(
            current_step,
            approval_log.document_name
        )
        return any(log.status == "Approved" for log in any_logs)
```

---

## 扩展指南

### 添加新的文档类型支持

1. **修改 hooks.py**:
```python
doc_events = {
    "Your DocType": {
        "before_insert": "dynamic_workflow.api.document_integration.attach_dynamic_workflow",
        "before_submit": "dynamic_workflow.api.document_integration.validate_approval",
        "on_submit": "dynamic_workflow.api.document_integration.execute_business_actions",
    }
}
```

2. **创建工作流配置**:
在 UI 中创建 Dynamic Workflow Config 记录

### 添加新的通知渠道

1. **在 integrations/notification.py 中添加函数**:
```python
def send_custom_notification(recipient, message):
    # 自定义通知逻辑
    pass
```

2. **在 hooks.py 中注册**:
```python
notification_config = {
    "notification_methods": ["Email", "SMS", "WeChat", "Custom"]
}
```

### 自定义超时规则

在 timeout_escalation.py 中扩展 check_and_escalate() 函数

---

**文档最后更新**: 2026-07-26
