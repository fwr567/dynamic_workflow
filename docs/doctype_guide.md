# Dynamic Workflow 核心文档类型说明

## 目录
1. [审批矩阵 (Approval Matrix)](#审批矩阵)
2. [审批矩阵规则 (Approval Matrix Rule)](#审批矩阵规则)
3. [工作流配置 (Dynamic Workflow Config)](#工作流配置)
4. [审批委托 (Approval Delegation)](#审批委托)
5. [审批日志 (Approval Log)](#审批日志)
6. [超时升级 (Workflow Timeout Escalation)](#超时升级)
7. [业务动作 (Business Action)](#业务动作)
8. [节点模板 (Dynamic Node Template)](#节点模板)

---

## 审批矩阵

### 功能描述
审批矩阵是整个工作流的核心配置，定义了不同文档类型在不同条件下的审批权限。

### 关键字段

| 字段名 | 类型 | 必填 | 说明 |
|-------|------|------|------|
| name | String | ✓ | 矩阵标识名称 (如: PO-01-10000) |
| doctype | Link | ✓ | 单据类型 (Material Request/Purchase Order/Sales Order 等) |
| description | Text |  | 矩阵描述 |
| enabled | Checkbox | ✓ | 是否启用此矩阵 |
| approval_rules | Table |  | 审批规则列表 (子表) |
| priority | Int |  | 优先级 (值越小越优先) |
| conditions | JSON |  | 复杂条件定义 (金额范围、部门等) |

### 审批规则子表 (approval_rules)

| 字段 | 类型 | 说明 |
|-----|------|------|
| seq | Int | 序号 |
| approver | Link | 审批人 (User) |
| approver_role | Link | 审批角色 (若指定角色则所有该角色用户都可审批) |
| approval_type | Select | 审批类型: Serial (串联) / Parallel (并联) |
| min_amount | Currency | 最小金额条件 |
| max_amount | Currency | 最大金额条件 |
| department | Link | 部门限制 |
| is_optional | Checkbox | 是否可选审批 |
| timeout_days | Int | 审批超时天数 |
| escalation_user | Link | 超时升级至用户 |

### 使用场景示例

**场景1：采购订单按金额分级审批**
```
矩阵: PO-Amount-Based
单据类型: Purchase Order

规则1 (0-5000):
  - 审批人: 部门主管
  - 审批类型: Serial
  
规则2 (5000-50000):
  - 审批人: 部门主管 → 采购经理
  - 审批类型: Serial
  
规则3 (50000+):
  - 审批人: 部门主管 → 采购经理 → 财务总监
  - 审批类型: Serial
```

---

## 审批矩阵规则

### 功能描述
Approval Matrix Rule 是审批矩阵下的具体规则项，支持更细粒度的条件控制。

### 关键字段

| 字段名 | 类型 | 必填 | 说明 |
|-------|------|------|------|
| approval_matrix | Link | ✓ | 所属矩阵 |
| step_number | Int | ✓ | 审批步骤序号 |
| condition_type | Select | ✓ | 条件类型: Amount/Department/Role/Custom |
| condition_value | Text |  | 条件值 (如: 10000 或 DEPT-001) |
| operator | Select |  | 操作符: = / > / < / >= / <= / in |
| approvers | Table |  | 审批人列表 |
| approval_mode | Select | ✓ | 审批模式: Any (任意一人)/All (全部) |
| is_active | Checkbox | ✓ | 规则是否有效 |
| created_date | Date |  | 创建日期 |
| valid_from | Date |  | 生效日期 |
| valid_to | Date |  | 失效日期 |

### 条件类型说明

- **Amount**: 按金额范围
- **Department**: 按部门
- **Role**: 按角色
- **Custom**: 自定义条件表达式
- **Combination**: 组合条件 (多个条件的 AND/OR 组合)

---

## 工作流配置

### 功能描述
Dynamic Workflow Config 用于配置具体单据类型是否启用工作流，以及工作流的基本参数。

### 关键字段

| 字段名 | 类型 | 必填 | 说明 |
|-------|------|------|------|
| doctype_name | Link | ✓ | 单据类型 |
| enabled | Checkbox | ✓ | 是否启用此单据的���作流 |
| approval_matrix | Link | ✓ | 使用的审批矩阵 |
| workflow_template | Link |  | 工作流模板 (可选) |
| require_approval | Checkbox | ✓ | 提交前是否必须审批 |
| allow_skip_approval | Checkbox |  | 是否允许跳过审批 |
| skip_approval_roles | Table |  | 允许跳过审批的角色列表 |
| auto_approve | Checkbox |  | 自动审批 (仅管理员) |
| enable_feedback | Checkbox | ✓ | 启用审批反馈 |
| enable_attachment | Checkbox | ✓ | 启用审批附件 |
| attachment_required | Checkbox |  | 审批附件是否必填 |
| enable_delegation | Checkbox | ✓ | 启用权限委托 |
| enable_rejection | Checkbox | ✓ | 启用回退功能 |
| enable_reassign | Checkbox | ✓ | 启用转办功能 |
| enable_add_approval | Checkbox | ✓ | 启用加签功能 |
| notify_method | Select | ✓ | 通知方式: Email/SMS/WeChat/All |
| timeout_action | Select |  | 超时动作: Escalate/Skip/Hold |
| created_on | DateTime |  | 创建时间 |
| modified_on | DateTime |  | 修改时间 |

### 跳过审批角色子表

| 字段 | 类型 | 说明 |
|-----|------|------|
| role | Link | 角色 (如 System Manager) |
| allow_comment | Checkbox | 是否需要添加备注 |

---

## 审批委托

### 功能描述
Approval Delegation 允许审批人将其权限临时委托给他人。

### 关键字段

| 字段名 | 类型 | 必填 | 说明 |
|-------|------|------|------|
| delegation_id | String | ✓ | 委托ID (自动生成) |
| delegator | Link | ✓ | 委托人 (原审批人) |
| delegatee | Link | ✓ | 被委托人 (代理人) |
| doctype | Link | ✓ | 限制单据类型 (可选) |
| from_date | Date | ✓ | 委托开始日期 |
| to_date | Date | ✓ | 委托结束日期 |
| status | Select | ✓ | 状态: Active/Expired/Revoked |
| reason | Text |  | 委托原因 |
| auto_revoke | Checkbox | ✓ | 到期自动撤销 |
| created_on | DateTime |  | 创建时间 |
| revoked_on | DateTime |  | 撤销时间 |
| revoked_by | Link |  | 撤销人 |

### 使用场景

```
场景：采购经理出差，委托权限给副经理
- 委托人: 张三 (采购经理)
- 被委托人: 李四 (副经理)
- 单据类型: Purchase Order
- 开始日期: 2026-08-01
- 结束日期: 2026-08-15
- 状态: Active
```

---

## 审批日志

### 功能描述
Approval Log 记录所有审批操作的详细历史，用于追踪和审计。

### 关键字段

| 字段名 | 类型 | 必填 | 说明 |
|-------|------|------|------|
| workflow_log_id | String | ✓ | 日志ID (自动生成) |
| document_type | Link | ✓ | 单据类型 |
| document_name | String | ✓ | 单据名称/编号 |
| document_link | Dynamic Link |  | 文档链接 |
| approval_step | Int | ✓ | 审批步骤 |
| approver | Link | ✓ | 审批人 |
| status | Select | ✓ | 审批状态: Pending/Approved/Rejected/Withdrawn |
| comments | Text |  | 审批意见 |
| action_time | DateTime | ✓ | 操作时间 |
| response_time | Int |  | 审批用时 (秒) |
| attachment | Attachment |  | 审批附件 |
| rejection_reason | Text |  | 回退原因 |
| reassigned_to | Link |  | 转办至 |
| delegation_used | Link |  | 使用的委托ID |
| ip_address | String |  | IP地址 |
| user_agent | String |  | User Agent |
| is_auto_approved | Checkbox |  | 是否自动审批 |
| approval_matrix_rule | Link |  | 使用的审批规则 |

### 关键视图

**待审核 (Pending)**
- 显示所有待处理的审批项

**已完成 (Completed)**
- 显示已处理的审批记录

**统计信息**
- 平均审批时间
- 拒绝率
- 按审批人统计

---

## 超时升级

### 功能描述
Workflow Timeout Escalation 定义当审批超时时的自动升级规则。

### 关键字段

| 字段名 | 类型 | 必填 | 说明 |
|-------|------|------|------|
| escalation_id | String | ✓ | 升级ID (自动生成) |
| document_type | Link | ✓ | 适用单据类型 |
| approval_step | Int | ✓ | 审批步骤号 |
| timeout_hours | Int | ✓ | 超时时间 (小时) |
| escalation_action | Select | ✓ | 升级动作: Auto Approve/Reassign/Notify/Hold |
| escalate_to_user | Link |  | 升级至用户 |
| escalate_to_role | Link |  | 升级至角色 |
| notify_approver | Checkbox | ✓ | 是否通知原审批人 |
| send_reminder | Checkbox | ✓ | 是否发送提醒 |
| reminder_count | Int |  | 最多发送提醒次数 |
| reminder_interval | Int |  | 提醒间隔 (小时) |
| enabled | Checkbox | ✓ | 是否启用此规则 |
| priority | Int |  | 优先级 |

### 升级动作说明

| 动作 | 说明 | 用途 |
|-----|------|------|
| Auto Approve | 自动通过审批 | 低风险单据的快速流转 |
| Reassign | 转移给其他审批人 | 原审批人无法及时处理 |
| Notify | 仅发送通知 | 提醒原审批人处理 |
| Hold | 暂停处理 | 等待手动干预 |

---

## 业务动作

### 功能描述
Business Action 定义审批完成后应执行的自动化业务操作。

### 关键字段

| 字段名 | 类型 | 必填 | 说明 |
|-------|------|------|------|
| action_id | String | ✓ | 动作ID (自动生成) |
| document_type | Link | ✓ | 应用单据类型 |
| trigger_status | Select | ✓ | ��发条件: All Approved/Any Rejected/On Step |
| approval_step | Int |  | 指定步骤 (当trigger_status为On Step时) |
| action_type | Select | ✓ | 动作类型: Update Field/Call API/Execute Script/Change Status |
| target_field | String |  | 目标字段名 |
| field_value | String |  | 新字段值 |
| api_endpoint | String |  | API端点 (HTTP方法) |
| api_payload | JSON |  | API请求体 |
| script_code | Code |  | 执行脚本 (Python) |
| new_status | Select |  | 新状态 (如提交、取消等) |
| enabled | Checkbox | ✓ | 是否启用 |
| order | Int | ✓ | 执行顺序 |
| error_handling | Select |  | 错误处理: Continue/Rollback/Alert |

### 使用场景示例

**场景1：审批通过后自动将采购订单改为已确认**
```
文档类型: Purchase Order
触发条件: All Approved (所有审批步骤都通过)
动作类型: Change Status
新状态: Submitted
```

**场景2：审批通过后自动创建收货单**
```
文档类型: Purchase Order
触发条件: All Approved
动作类型: Call API
API端点: POST /api/v2/purchase-receipt/create
API请求体: 
{
  "purchase_order": "{docname}",
  "auto_create": true
}
```

---

## 节点模板

### 功能描述
Dynamic Node Template 用于定义可重复使用的审批流程模板。

### 关键字段

| 字段名 | 类型 | 必填 | 说明 |
|-------|------|------|------|
| template_id | String | ✓ | 模板ID (自动生成) |
| template_name | String | ✓ | 模板名称 (如: 标准采购审批流) |
| description | Text |  | 模板描述 |
| node_type | Select | ✓ | 节点类型: Approval/Condition/Parallel/Serial |
| approval_steps | Table | ✓ | 审批步骤列表 (子表) |
| conditions | Table |  | 条件判断 (子表) |
| is_reusable | Checkbox | ✓ | 是否可重用 |
| version | Int |  | 版本号 |
| status | Select | ✓ | 状态: Draft/Active/Archived |
| created_by | Link | ✓ | 创建人 |
| created_on | DateTime | ✓ | 创建时间 |

### 审批步骤子表

| 字段 | 类型 | 说明 |
|-----|------|------|
| step_no | Int | 步骤号 |
| step_name | String | 步骤名称 |
| approvers | Table | 审批人员 |
| approval_type | Select | Serial/Parallel/Any One |
| timeout_days | Int | 超时天数 |
| on_reject_action | Select | 回退至/循环/停止 |

### 预定义模板库

```
1. 标准单据审批流
   - 部门主管 (Serial) → 部门经理 (Serial) → 财务 (Serial)

2. 金额分级审批
   - 金额 < 5000: 部门主管
   - 金额 5000-50000: 部门主管 → 部门经理
   - 金额 > 50000: 部门主管 → 部门经理 → 总经理

3. 并联审批
   - 部门审批 (Parallel) & 财务审批 (Parallel) & 法律审批 (Parallel)

4. 条件分支
   - IF 紧急 THEN 快速审批流
   - ELSE 标准审批流
```

---

## 最佳实践

### 1. 矩阵设计
- ✓ 按业务场景分类设计矩阵
- ✗ 不要在单个矩阵中设置过多规则
- ✓ 定期审查和优化审批流程

### 2. 权限委托
- ✓ 设置合理的委托期限
- ✓ 启用自动撤销防止权限泄露
- ✗ 避免过长期限的委托

### 3. 超时管理
- ✓ 根据单据类型设置不同超时
- ✓ 配置逐级升级规则
- ✓ 定期检查超时升级日志

### 4. 审计追踪
- ✓ 启用完整的审批日志记录
- ✓ 定期导出审批报表
- ✓ 保留IP和User Agent用于安全审计

---

**文档最后更新**: 2026-07-26
