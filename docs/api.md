# Dynamic Workflow API 文档

## 目录
1. [基础 API](#基础-api)
2. [审批矩阵 API](#审批矩阵-api)
3. [审批操作 API](#审批操作-api)
4. [委托管理 API](#委托管理-api)
5. [工作流查询 API](#工作流查询-api)
6. [WebHook 集成](#webhook-集成)
7. [错误处理](#错误处理)

---

## 基础 API

### 1. 获取文档的审批状态

**端点**: `GET /api/resource/Approval%20Log`

**参数**:
```json
{
  "filters": {
    "document_type": "Purchase Order",
    "document_name": "PO-2026-00001",
    "status": "Pending"
  },
  "fields": ["name", "approver", "approval_step", "creation"],
  "limit_page_length": 100
}
```

**响应**:
```json
{
  "data": [
    {
      "name": "APL-001",
      "approver": "manager@company.com",
      "approval_step": 1,
      "creation": "2026-07-26 10:00:00"
    }
  ]
}
```

### 2. 获取用户待审批单据列表

**端点**: `GET /api/method/dynamic_workflow.api.approval.get_pending_approvals`

**参数**:
```json
{
  "user": "user@company.com",
  "limit": 20
}
```

**响应**:
```json
{
  "message": [
    {
      "doctype": "Purchase Order",
      "docname": "PO-2026-00001",
      "approval_step": 2,
      "approver_count": 3,
      "pending_count": 1,
      "owner": "applicant@company.com",
      "amount": 25000,
      "creation": "2026-07-25 14:30:00",
      "days_pending": 1
    }
  ]
}
```

---

## 审批矩阵 API

### 1. 获取适用的审批矩阵

**端点**: `GET /api/method/dynamic_workflow.api.approval_matrix.get_approval_matrix`

**参数**:
```json
{
  "doctype": "Purchase Order",
  "amount": 50000,
  "department": "采购部"
}
```

**响应**:
```json
{
  "message": {
    "matrix_id": "PO-Matrix-001",
    "rules": [
      {
        "step": 1,
        "approver": "dept_manager@company.com",
        "approver_role": "Department Manager",
        "approval_type": "Serial",
        "timeout_days": 1
      },
      {
        "step": 2,
        "approver": "finance_manager@company.com",
        "approver_role": "Finance Manager",
        "approval_type": "Serial",
        "timeout_days": 1
      }
    ]
  }
}
```

### 2. 创建审批矩阵

**端点**: `POST /api/resource/Approval%20Matrix`

**请求体**:
```json
{
  "doctype": "Approval Matrix",
  "doctype_name": "Purchase Order",
  "description": "标准采购订单审批流",
  "enabled": true,
  "priority": 1,
  "conditions": {
    "amount_range": [0, 100000],
    "department": "采购部"
  },
  "approval_rules": [
    {
      "seq": 1,
      "approver": "manager@company.com",
      "approver_role": "Department Head",
      "approval_type": "Serial",
      "timeout_days": 1
    }
  ]
}
```

**响应**:
```json
{
  "data": {
    "name": "PO-Matrix-001",
    "doctype": "Approval Matrix",
    "creation": "2026-07-26 10:30:00"
  }
}
```

### 3. 更新审批矩阵规则

**端点**: `PUT /api/resource/Approval%20Matrix%20Rule/{rule_id}`

**请求体**:
```json
{
  "approvers": [
    {"user": "new_approver@company.com"}
  ],
  "timeout_days": 2
}
```

---

## 审批操作 API

### 1. 提交审批（批准）

**端点**: `POST /api/method/dynamic_workflow.api.approval.approve_document`

**请求体**:
```json
{
  "doctype": "Purchase Order",
  "docname": "PO-2026-00001",
  "comments": "已审批通过",
  "approval_log_id": "APL-001"
}
```

**响应**:
```json
{
  "message": {
    "status": "success",
    "approval_id": "APL-001",
    "next_step": 2,
    "next_approver": "finance_manager@company.com"
  }
}
```

### 2. 拒绝审批（回退）

**端点**: `POST /api/method/dynamic_workflow.api.approval.reject_document`

**请求体**:
```json
{
  "doctype": "Purchase Order",
  "docname": "PO-2026-00001",
  "rejection_reason": "需要调整价格",
  "reject_to_step": 0,
  "approval_log_id": "APL-001"
}
```

**响应**:
```json
{
  "message": {
    "status": "success",
    "message": "审批已回退",
    "rejection_log_id": "APL-REJECT-001"
  }
}
```

### 3. 转办审批

**端点**: `POST /api/method/dynamic_workflow.api.approval.reassign_approval`

**请求体**:
```json
{
  "doctype": "Purchase Order",
  "docname": "PO-2026-00001",
  "current_approver": "manager@company.com",
  "new_approver": "deputy_manager@company.com",
  "reason": "原审批人出差，转办至副经理",
  "approval_log_id": "APL-001"
}
```

**响应**:
```json
{
  "message": {
    "status": "success",
    "reassigned_to": "deputy_manager@company.com",
    "reassign_log_id": "APL-REASSIGN-001"
  }
}
```

### 4. 加签审批

**端点**: `POST /api/method/dynamic_workflow.api.approval.add_approval_signer`

**请求体**:
```json
{
  "doctype": "Purchase Order",
  "docname": "PO-2026-00001",
  "new_approver": "director@company.com",
  "position": "before",
  "reason": "需要高层审核",
  "approval_log_id": "APL-001"
}
```

**参数说明**:
- `position`: "before" (前加签) 或 "after" (后加签)

**响应**:
```json
{
  "message": {
    "status": "success",
    "message": "已添加加签审批人",
    "new_approval_chain": [
      {"step": 1, "approver": "director@company.com"},
      {"step": 2, "approver": "manager@company.com"},
      {"step": 3, "approver": "finance_manager@company.com"}
    ]
  }
}
```

### 5. 催办审批

**端点**: `POST /api/method/dynamic_workflow.api.approval.send_approval_reminder`

**请求体**:
```json
{
  "doctype": "Purchase Order",
  "docname": "PO-2026-00001",
  "approval_log_id": "APL-001",
  "message": "请尽快处理此采购订单"
}
```

**响应**:
```json
{
  "message": {
    "status": "success",
    "reminded_user": "manager@company.com",
    "notification_method": "email"
  }
}
```

---

## 委托管理 API

### 1. 创建审批权委托

**端点**: `POST /api/resource/Approval%20Delegation`

**请求体**:
```json
{
  "doctype": "Approval Delegation",
  "delegator": "manager@company.com",
  "delegatee": "deputy_manager@company.com",
  "doctype_filter": "Purchase Order",
  "from_date": "2026-08-01",
  "to_date": "2026-08-15",
  "reason": "出差期间权限委托",
  "auto_revoke": true
}
```

**响应**:
```json
{
  "data": {
    "name": "APD-001",
    "delegation_id": "DEL-2026-00001",
    "status": "Active"
  }
}
```

### 2. 获取活跃委托

**端点**: `GET /api/method/dynamic_workflow.api.delegation.get_active_delegations`

**参数**:
```json
{
  "user": "manager@company.com"
}
```

**响应**:
```json
{
  "message": [
    {
      "delegation_id": "DEL-2026-00001",
      "delegatee": "deputy_manager@company.com",
      "doctype_filter": "Purchase Order",
      "from_date": "2026-08-01",
      "to_date": "2026-08-15",
      "days_remaining": 5,
      "status": "Active"
    }
  ]
}
```

### 3. 撤销委托

**端点**: `POST /api/method/dynamic_workflow.api.delegation.revoke_delegation`

**请求体**:
```json
{
  "delegation_id": "DEL-2026-00001"
}
```

**响应**:
```json
{
  "message": {
    "status": "success",
    "message": "委托已撤销"
  }
}
```

---

## 工作流查询 API

### 1. 获取审批历史

**端点**: `GET /api/method/dynamic_workflow.api.workflow.get_approval_history`

**参数**:
```json
{
  "doctype": "Purchase Order",
  "docname": "PO-2026-00001"
}
```

**响应**:
```json
{
  "message": {
    "document_name": "PO-2026-00001",
    "document_type": "Purchase Order",
    "status": "Approved",
    "timeline": [
      {
        "step": 1,
        "approver": "dept_manager@company.com",
        "status": "Approved",
        "comments": "已审核",
        "action_time": "2026-07-26 10:30:00",
        "response_time_hours": 2
      },
      {
        "step": 2,
        "approver": "finance_manager@company.com",
        "status": "Approved",
        "comments": "财务审批通过",
        "action_time": "2026-07-26 14:00:00",
        "response_time_hours": 3.5
      }
    ]
  }
}
```

### 2. 获取审批统计

**端点**: `GET /api/method/dynamic_workflow.api.workflow.get_approval_statistics`

**参数**:
```json
{
  "from_date": "2026-07-01",
  "to_date": "2026-07-31",
  "doctype": "Purchase Order"
}
```

**响应**:
```json
{
  "message": {
    "total_submitted": 150,
    "total_approved": 145,
    "total_rejected": 5,
    "approval_rate": "96.67%",
    "average_approval_time_hours": 24,
    "by_approver": {
      "manager@company.com": {
        "processed": 50,
        "approved": 48,
        "rejected": 2,
        "avg_time_hours": 20
      }
    }
  }
}
```

### 3. 获取超时审批列表

**端点**: `GET /api/method/dynamic_workflow.api.workflow.get_timeout_approvals`

**参数**:
```json
{
  "hours_overdue": 24
}
```

**响应**:
```json
{
  "message": [
    {
      "approval_id": "APL-001",
      "document_type": "Purchase Order",
      "document_name": "PO-2026-00001",
      "approver": "manager@company.com",
      "pending_since": "2026-07-24 10:00:00",
      "hours_overdue": 28,
      "escalation_status": "Pending",
      "amount": 50000
    }
  ]
}
```

### 4. 获取用户审批权限

**端点**: `GET /api/method/dynamic_workflow.api.workflow.get_user_approval_authority`

**参数**:
```json
{
  "user": "manager@company.com"
}
```

**响应**:
```json
{
  "message": {
    "user": "manager@company.com",
    "approval_authorities": [
      {
        "doctype": "Purchase Order",
        "matrices": ["PO-Matrix-001", "PO-Matrix-002"],
        "amount_authority": 100000,
        "roles": ["Department Manager", "Approver"]
      }
    ],
    "delegations": [
      {
        "from_user": "cfo@company.com",
        "valid_until": "2026-08-15"
      }
    ]
  }
}
```

---

## WebHook 集成

### 1. 审批事件 WebHook

当审批状态变化时，系统会发送 WebHook 通知。

**配置 WebHook URL**:
在工作流配置中设置 WebHook 端点

**事件类型**:

#### approval.submitted
```json
{
  "event": "approval.submitted",
  "timestamp": "2026-07-26T10:30:00Z",
  "data": {
    "doctype": "Purchase Order",
    "docname": "PO-2026-00001",
    "approver": "manager@company.com",
    "approval_step": 1,
    "status": "Approved",
    "comments": "已审批"
  }
}
```

#### approval.rejected
```json
{
  "event": "approval.rejected",
  "timestamp": "2026-07-26T11:00:00Z",
  "data": {
    "doctype": "Purchase Order",
    "docname": "PO-2026-00001",
    "approver": "manager@company.com",
    "approval_step": 1,
    "rejection_reason": "需要调整预算",
    "reject_to_step": 0
  }
}
```

#### approval.escalated
```json
{
  "event": "approval.escalated",
  "timestamp": "2026-07-26T12:00:00Z",
  "data": {
    "doctype": "Purchase Order",
    "docname": "PO-2026-00001",
    "original_approver": "manager@company.com",
    "escalated_to": "director@company.com",
    "reason": "Timeout"
  }
}
```

### 2. 设置 WebHook

**端点**: `POST /api/resource/Webhook`

**请求体**:
```json
{
  "doctype": "Webhook",
  "webhook_doctype": "Approval Log",
  "webhook_events": ["after_insert"],
  "webhook_url": "https://your-service.com/webhooks/approval",
  "webhook_document_events": [
    "approval.submitted",
    "approval.rejected"
  ]
}
```

---

## 错误处理

### 常见错误响应

#### 401 Unauthorized
```json
{
  "exc_type": "AuthenticationError",
  "message": "用户未授权"
}
```

#### 403 Forbidden
```json
{
  "exc_type": "PermissionError",
  "message": "没有权限执行此操作"
}
```

#### 404 Not Found
```json
{
  "exc_type": "DoesNotExistError",
  "message": "审批记录不存在"
}
```

#### 400 Bad Request
```json
{
  "exc_type": "ValidationError",
  "message": "必填字段缺失: comments"
}
```

#### 409 Conflict
```json
{
  "exc_type": "ConflictError",
  "message": "该单据已被其他人审批"
}
```

### 错误处理最佳实践

```python
try:
    response = requests.post(
        'http://localhost:8000/api/method/dynamic_workflow.api.approval.approve_document',
        json={
            "doctype": "Purchase Order",
            "docname": "PO-2026-00001",
            "comments": "Approved"
        },
        headers={'Authorization': 'Bearer token'}
    )
    
    if response.status_code == 200:
        result = response.json()
        print(result['message'])
    elif response.status_code == 403:
        print("权限不足，请检查用户角色")
    elif response.status_code == 404:
        print("审批记录不存在")
    else:
        print(f"错误: {response.text}")
        
except requests.exceptions.RequestException as e:
    print(f"请求失败: {str(e)}")
```

---

## 认证

所有 API 请求需要在请求头中包含认证信息：

**Token 认证**:
```
Authorization: Bearer your_token_here
```

**Cookie 认证**:
```
Cookie: sid=your_session_id
```

**获取 Token**:
```bash
curl -X POST http://localhost:8000/api/method/frappe.auth.get_logged_in_user \
  -d "usr=user@company.com&pwd=password"
```

---

## 速率限制

- 每分钟最多 60 个请求
- 每小时最多 3000 个请求

超限后返回 429 Too Many Requests

---

**API 文档版本**: 1.0.0  
**最后更新**: 2026-07-26
