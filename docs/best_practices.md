# Dynamic Workflow 最佳实践指南

## 目录
1. [审批流程设计原则](#审批流程设计原则)
2. [性能优化建议](#性能优化建议)
3. [安全与合规](#安全与合规)
4. [常见场景配置](#常见场景配置)
5. [故障排查](#故障排查)
6. [常见错误](#常见错误)

---

## 审批流程设计原则

### 1. 审批层级设计

#### ✅ 建议做法

**原则**：层级不超过5层，平均审批时间控制在2-3天内

```
采购流程示例：
第1层：申请部门主管 (1天内)
  └─ 第2层：采购部经理 (1天内)
    └─ 第3层：财务部审核 (1天内)
      └─ 第4层：总经理签字 (审批金额>100万)
```

#### ❌ 避免做法

```
过长的审批链（超过7层）
└─ 容易导致流程卡顿
└─ 审批人职责不清
└─ 成本和风险不匹配
```

### 2. 条件设置

#### 金额分级

```
金额范围设计遵循 2-3-5 法则：

| 金额 | 审批人 | 快速审批(可跳过) | 备注 |
|-----|--------|-----------------|------|
| < 5K | 部门主管 | 是 | 常规单据 |
| 5K-50K | 部门主管 + 采购经理 | 否 | 需谨慎 |
| 50K-500K | 部门主管 + 采购经理 + 财务 | 否 | 重点关注 |
| > 500K | 上述 + 总经理 | 否 | 最高层级 |
```

#### 部门限制

```python
# 使用条件表达式处理部门特定流程
conditions = {
    "department": "采购部",
    "amount": (5000, 50000),
    "doctype": "Purchase Order"
}
# 该条件下的审批人：采购经理 + 财务总监
```

### 3. 审批人选择

#### 推荐

- 使用**角色**而非个人用户
  ```
  优势：
  - 人员变动时无需修改配置
  - 自动适应组织结构变化
  - 支持多人共同审批
  ```

#### 示例

```
审批角色配置：
- Approval Manager (审批管理员)
- Finance Head (财务主管)
- Purchase Manager (采购经理)
- Department Head (部门主管)
```

---

## 性能优化建议

### 1. 索引优化

在 `hooks.py` 中已配置的关键索引：

```python
db_indexes = [
    ("dynamic_workflow_config", ["doctype", "enabled"]),
    ("approval_log", ["document_type", "document_name", "status"]),
    ("approval_delegation", ["delegator", "delegatee", "status"]),
]
```

### 2. 查询优化

#### 避免 N+1 问题

```python
# ❌ 不好的做法
approvals = frappe.get_list("Approval Log", filters={"status": "Pending"})
for approval in approvals:
    user = frappe.get_doc("User", approval.approver)  # N+1 查询
    # ...

# ✅ 好的做法
approvals = frappe.get_list(
    "Approval Log",
    filters={"status": "Pending"},
    fields=["*", "approver"]  # 关联查询
)
```

### 3. 缓存策略

```python
# 缓存审批矩阵规则 (30分钟)
@frappe.whitelist()
def get_approval_matrix(doctype, amount, department):
    cache_key = f"approval_matrix:{doctype}:{department}"
    cached = frappe.cache.get(cache_key)
    
    if cached:
        return cached
    
    result = calculate_approval_matrix(doctype, amount, department)
    frappe.cache.setex(cache_key, 30*60, result)
    return result
```

### 4. 批处理优化

```python
# 每小时运行一次的超时检查 - 使用批处理
def check_and_escalate():
    """每小时检查一次超时审批"""
    # 使用 limit 避免一次性加载大量数据
    pending_logs = frappe.get_list(
        "Approval Log",
        filters=[
            ["status", "=", "Pending"],
            ["creation", "<", get_datetime() - timedelta(hours=24)]
        ],
        limit=100  # 分批处理
    )
    
    for log in pending_logs:
        escalate_approval(log)
```

---

## 安全与合规

### 1. 权限控制

#### 文档级权限

```python
# 只有审批人可以看到待审批单据
from frappe.permissions import add_permission_rule

add_permission_rule(
    "Approval Log",
    {
        "read": ["approver"],
        "write": ["approver"],
        "submit": ["approver"]
    }
)
```

#### 角色权限

```
Dynamic Workflow Manager (工作流管理员)
- 可配置审批矩阵
- 可查看所有审批日志
- 可手动操作审批流程

Approval Administrator (审批管理员)
- 可进行超时升级操作
- 可撤销/重新启动审批
- 可生成审批报表

Document Approver (文档审批人)
- 只能看到自己需要审批的单据
- 只能审批授权范围内的单据
```

### 2. 审计追踪

#### 完整日志记录

```python
# 所有审批操作都应记录
def log_approval_action(
    doctype, 
    docname, 
    action, 
    approver, 
    timestamp, 
    ip_address,
    user_agent
):
    """记录每一项审批操作"""
    frappe.db.insert({
        "doctype": "Approval Audit Log",
        "document_type": doctype,
        "document_name": docname,
        "action": action,  # Approved/Rejected/Delegated/Reassigned
        "approver": approver,
        "action_timestamp": timestamp,
        "ip_address": ip_address,
        "user_agent": user_agent
    })
```

#### 审计报表

```
定期导出以下报表进行合规审查：
1. 按审批人统计 - 发现审批瓶颈
2. 按金额统计 - 验证财务控制
3. 超期审批统计 - 改进流程
4. 审批拒绝统计 - 发现问题模式
```

### 3. 数据保护

```python
# 敏感信息脱敏
def mask_sensitive_fields(approval_log):
    """对敏感字段进行脱敏"""
    sensitive_fields = ["comments", "amount"]
    
    for field in sensitive_fields:
        if not has_permission(field):
            approval_log[field] = "***MASKED***"
    
    return approval_log
```

---

## 常见场景配置

### 场景1：电商平台订单审批

**需求**：不同金额的订单需要不同审批

```
配置步骤：

1. 创建审批矩阵：E-Commerce Order Matrix
   
2. 设置规则：
   规则1 (0-1000): 自动通过
   规则2 (1000-10000): 运营经理审批
   规则3 (10000-100000): 运营经理 + 财务审批
   规则4 (>100000): 运营经理 + 财务 + 总经理
   
3. 配置超时：
   - 普通订单: 24小时
   - 大额订单: 4小时 (高优先级)
   
4. 业务动作：
   - 所有审批通过后，自动转为已发货状态
```

### 场景2：多部门协同审批

**需求**：需要多个部门同时审批，而非顺序

```
配置：
1. 创建 Dynamic Node Template: 并联审批模板
   
2. 设置步骤：
   - 并联步骤1: 采购部审批
   - 并联步骤2: 财务部审批  
   - 并联步骤3: 法律部审批
   
   三个部门需同时审批，任意一个拒绝则整体拒绝
   
3. 超时规则：
   - 任意部门超过48小时未审批，自动升级至部门主管
   
4. 通知：
   - 创建时: 通知所有审批人
   - 24小时后: 催办
   - 48小时后: 升级通知
```

### 场景3：按用户权限级别的动态审批

**需求**：相同金额可能有不同审批人，取决于申请人权限

```python
# 在 Approval Matrix Rule 中使用自定义条件
custom_condition = """
IF applicant_permission_level == 'Senior':
    amount_threshold = 100000  # 高级员工可以直接提高限额
ELSE IF applicant_permission_level == 'Junior':
    amount_threshold = 5000    # 初级员工限额较低
ELSE:
    amount_threshold = 10000   # 中级员工
"""

# 根据计算的 threshold 选择审批人
```

### 场景4：紧急审批快速通道

**需求**：紧急单据需要快速审批

```
配置：
1. 在工作流配置中添加 "is_urgent" 标志
   
2. 紧急单据规则：
   - 跳过某些审批步骤（仅限紧急）
   - 使用快速审批流模板
   - 超时时间: 4小时（而非24小时）
   - 超时后自动升级至最高管理者
   
3. 权限限制：
   - 只有特定角色可标记紧急
   - 紧急标记需要备注说明
```

---

## 故障排查

### 问题1：审批卡在某个步骤

#### 排查步骤

```python
# 1. 检查该步骤是否有活跃的委托
delegations = frappe.get_list(
    "Approval Delegation",
    filters={
        "delegator": "approver_user",
        "status": "Active"
    }
)

# 2. 检查审批人是否禁用或离职
approver = frappe.get_doc("User", "approver_user")
if approver.disabled or not approver.roles:
    print("审批人已禁用或无角色")

# 3. 检查权限是否正确
permissions = frappe.get_roles("approver_user")
required_role = "Approval Manager"
if required_role not in permissions:
    print(f"缺少角色: {required_role}")

# 4. 查看最近的审批日志
logs = frappe.get_list(
    "Approval Log",
    filters={
        "document_name": "PO-001",
        "approver": "approver_user"
    },
    order_by="creation desc",
    limit=1
)
print(logs[0])
```

### 问题2：审批权限配置不生效

#### 排查步骤

```python
# 1. 验证矩阵是否启用
matrix = frappe.get_doc("Approval Matrix", "PO-Matrix")
if not matrix.enabled:
    print("矩阵未启用")

# 2. 验证工作流配置
config = frappe.db.get_value(
    "Dynamic Workflow Config",
    {"doctype_name": "Purchase Order"},
    "enabled"
)
if not config:
    print("工作流未启用")

# 3. 检查条件是否匹配
rule = frappe.get_doc("Approval Matrix Rule", "rule_id")
if check_conditions(rule, document):
    print("条件已匹配")
else:
    print("条件未匹配")

# 4. 强制刷新缓存
frappe.cache.clear()
```

### 问题3：通知未发送

#### 排查步骤

```python
# 1. 检查通知配置
config = frappe.get_doc("Dynamic Workflow Config", "PO-Config")
print(f"通知方式: {config.notify_method}")

# 2. 检查用户邮箱是否配置
user = frappe.get_doc("User", "approver_user")
if not user.email:
    print("用户邮箱未配置")

# 3. 检查邮件队列
from frappe.tasks import send_mails
send_mails()  # 手动发送待发邮件

# 4. 查看邮件日志
email_logs = frappe.get_list(
    "Email Queue",
    filters={"status": "Error"},
    limit=10
)
for log in email_logs:
    print(f"错误: {log.error}")
```

---

## 常见错误

### 错误1：循环审批

**现象**：审批人A回退给B，B又审批给A

**解决方案**：
```python
# 在回退时检查是否形成循环
def check_rejection_loop(current_user, target_user, approval_log):
    """检查是否会形成循环"""
    # 查看历史，确保没有之前的相同流向
    recent_logs = frappe.get_list(
        "Approval Log",
        filters={
            "document_name": approval_log.document_name,
            "approver": target_user,
            "creation": [">", get_datetime() - timedelta(days=1)]
        }
    )
    
    if recent_logs:
        frappe.throw("不能回退给最近刚审批过的人员")
```

### 错误2：权限覆盖冲突

**现象**：多个矩阵规则应用到同一单据，产生矛盾

**解决方案**：
```python
# 使用优先级机制
def get_applicable_rules(document):
    """获取所有适用规则并按优先级排序"""
    rules = frappe.get_list(
        "Approval Matrix Rule",
        filters={"is_active": 1},
        order_by="priority asc"  # 优先级低的先应用
    )
    
    applicable = [r for r in rules if check_conditions(r, document)]
    
    if applicable:
        return applicable[0]  # 返回最高优先级的规则
    
    return None
```

### 错误3：超时规则冲突

**现象**：超时升级和委托同时生效，产生冲突

**解决方案**：
```python
# 在超时升级时检查是否存在活跃委托
def escalate_with_delegation_check(approval_log):
    """执行升级前检查委托状态"""
    # 检查是否有有效的委托
    delegation = frappe.db.get_value(
        "Approval Delegation",
        {
            "delegator": approval_log.approver,
            "to_date": [">=", get_datetime()],
            "status": "Active"
        }
    )
    
    if delegation:
        # 如果有委托，转移给被委托人而非升级
        approval_log.approver = delegation.delegatee
        return
    
    # 否则执行正常升级
    escalate_approval(approval_log)
```

### 错误4：重复审批

**现象**：同一个单据被某个审批人审批多次

**解决方案**：
```python
def validate_no_duplicate_approval(approval_log):
    """防止重复审批"""
    existing = frappe.db.count(
        "Approval Log",
        filters={
            "document_name": approval_log.document_name,
            "approver": approval_log.approver,
            "approval_step": approval_log.approval_step,
            "status": ["!=", "Withdrawn"]
        }
    )
    
    if existing > 0:
        frappe.throw(f"该审批人已在此步骤进行过审批")
```

---

## 性能基准

### 系统容量

| 指标 | 标准值 | 备注 |
|-----|-------|------|
| 日审批单据数 | 1000+ | 正常系统容量 |
| 审批日志查询 | <500ms | 使用索引优化 |
| 矩阵规则计算 | <200ms | 启用缓存 |
| 并发审批用户 | 100+ | 取决于硬件 |
| 历史数据保留 | 2年 | 定期归档 |

### 优化检查清单

- [ ] 已配置数据库索引
- [ ] 已启用缓存策略
- [ ] 已设置查询限制
- [ ] 已优化定时任务
- [ ] 已启用异步处理
- [ ] 已配置日志旋转
- [ ] 已设置历史数据归档

---

**文档最后更新**: 2026-07-26
