# Dynamic Workflow 安装和配置指南

## 目录
1. [系统要求](#系统要求)
2. [安装步骤](#安装步骤)
3. [初始配置](#初始配置)
4. [常见安装问题](#常见安装问题)
5. [升级指南](#升级指南)
6. [卸载步骤](#卸载步骤)

---

## 系统要求

### 硬件要求

| 组件 | 最低要求 | 推荐配置 |
|-----|---------|---------|
| CPU | 2 核 | 4 核+ |
| 内存 | 4GB | 8GB+ |
| 存储 | 10GB | 50GB+ |
| 网络 | 100Mbps | 1Gbps |

### 软件要求

- **ERPNext**: v16.0 或更高版本
- **Frappe**: v16.0 或更高版本
- **Python**: 3.10 或更高版本
- **MariaDB**: 10.3+ 或 **PostgreSQL**: 12+
- **Redis**: 4.0 或更高版本
- **Node.js**: 16+ (用于前端资源编译)

### 浏览器支持

- Chrome 90+
- Firefox 88+
- Safari 14+
- Edge 90+

---

## 安装步骤

### 步骤 1: 准备 Bench 环境

```bash
# 进入 Bench 目录
cd ~/frappe-bench

# 确保 Bench 已更新
bench update

# 创建新的站点（如果需要）
bench new-site site.local
```

### 步骤 2: 克隆应用

```bash
# 方式 1: 从 GitHub 克隆
git clone https://github.com/fwr567/dynamic_workflow apps/dynamic_workflow

# 方式 2: 从本地文件安装
# 将应用文件夹复制到 apps 目录
cp -r /path/to/dynamic_workflow ~/frappe-bench/apps/
```

### 步骤 3: 安装应用

```bash
# 获取应用
bench get-app dynamic_workflow

# 安装到当前站点
bench install-app dynamic_workflow --site site.local
```

### 步骤 4: 执行初始化

```bash
# 运行数据库迁移
bench migrate --site site.local

# 重新构建资源
bench build --site site.local

# 清除缓存
bench clear-cache --site site.local

# 重启 Bench
bench restart
```

### 步骤 5: 验证安装

```bash
# 检查应用是否安装成功
bench list-apps | grep dynamic_workflow

# 查看应用版本
bench version

# 测试访问
# 打开浏览器访问: http://localhost:8000
# 搜索 "Dynamic Workflow" 检查应用是否可用
```

---

## 初始配置

### 配置 1: 创建审批管理员角色

**步骤**:

1. 进入 ERPNext 系统
2. 搜索 "Role" → 新建角色
3. 角色名: `Dynamic Workflow Manager`
4. 权限配置:

```
DocType 权限:
- Approval Matrix: Create, Read, Write, Submit, Amend, Cancel
- Approval Matrix Rule: Create, Read, Write
- Dynamic Workflow Config: Create, Read, Write, Submit
- Approval Delegation: Create, Read, Write, Submit
- Approval Log: Read (查看所有)
- Workflow Timeout Escalation: Create, Read, Write

页面权限:
- Dynamic Workflow (Workspace): Read

自定义权限:
- 可访问所有相关报表
- 可执行超时升级操作
```

### 配置 2: 创建审批人角色

**步骤**:

1. 新建角色: `Document Approver`
2. 权限配置:

```
DocType 权限:
- Approval Log: Read (仅限自己的审批)
- Purchase Order: Read, Submit (受审批矩阵限制)
- Sales Order: Read, Submit (受审批矩阵限制)
- Material Request: Read, Submit (受审批矩阵限制)
```

### 配置 3: 设置用户权限

```bash
# 为用户分配角色
# 1. 进入 User 文档
# 2. 添加角色: Dynamic Workflow Manager 或 Document Approver
# 3. 保存
```

### 配置 4: 启用工作流

**第一次启用工作流流程**:

1. 进入 **Dynamic Workflow** 应用
2. 点击 **工作流配置** 卡片
3. 新建配置

```json
{
  "doctype_name": "Purchase Order",
  "enabled": true,
  "approval_matrix": "PO-Standard-Matrix",
  "require_approval": true,
  "allow_skip_approval": false,
  "enable_feedback": true,
  "enable_attachment": true,
  "enable_delegation": true,
  "enable_rejection": true,
  "enable_reassign": true,
  "enable_add_approval": true,
  "notify_method": "Email",
  "timeout_action": "Escalate"
}
```

4. 点击保存和提交

### 配置 5: 创建审批矩阵

**示例配置**:

1. 进入 **审批矩阵**
2. 新建矩阵

```json
{
  "doctype_name": "Purchase Order",
  "description": "标准采购订单审批矩阵",
  "enabled": true,
  "priority": 1,
  "approval_rules": [
    {
      "seq": 1,
      "approver_role": "Department Head",
      "approval_type": "Serial",
      "timeout_days": 1,
      "is_optional": false
    },
    {
      "seq": 2,
      "approver_role": "Purchase Manager",
      "approval_type": "Serial",
      "timeout_days": 1,
      "is_optional": false,
      "min_amount": 5000,
      "max_amount": 50000
    },
    {
      "seq": 3,
      "approver_role": "Finance Manager",
      "approval_type": "Serial",
      "timeout_days": 1,
      "is_optional": false,
      "min_amount": 50000
    }
  ]
}
```

### 配置 6: 配置通知

**邮件通知设置**:

1. 进入 **系统设置**
2. 搜索 "SMTP"
3. 配置邮件服务:

```
SMTP Server: smtp.gmail.com
SMTP Port: 587
Use TLS: 是
邮箱地址: your-email@company.com
邮箱密码: your-app-password
```

**WeChat 通知设置** (可选):

1. 进入 **Dynamic Workflow 设置**
2. 配置企业微信机器人:

```json
{
  "wechat_enabled": true,
  "wechat_webhook_url": "https://qyapi.weixin.qq.com/cgi-bin/webhook/send?key=YOUR_KEY",
  "wechat_mention_all": false
}
```

### 配置 7: 配置超时规则

```json
{
  "document_type": "Purchase Order",
  "approval_step": 1,
  "timeout_hours": 24,
  "escalation_action": "Notify",
  "notify_approver": true,
  "send_reminder": true,
  "reminder_interval": 4,
  "reminder_count": 3,
  "enabled": true
}
```

---

## 常见安装问题

### 问题 1: 应用无法安装 - "Missing dependency"

**症状**: 安装时出现缺少依赖错误

**解决方案**:

```bash
# 检查依赖
pip list | grep frappe

# 更新 pip
pip install --upgrade pip

# 安装缺少的依赖
pip install -r apps/dynamic_workflow/requirements.txt

# 重新安装应用
bench install-app dynamic_workflow
```

### 问题 2: 数据库迁移失败

**症状**: 执行 `bench migrate` 时出错

**解决方案**:

```bash
# 检查数据库连接
bench --site site.local mysql-console

# 查看迁移日志
bench migrate --site site.local --verbose

# 如果是表冲突，备份后删除冲突表
bench --site site.local mysql-console
mysql> DROP TABLE IF EXISTS `tabApproval Matrix`;

# 重新运行迁移
bench migrate --site site.local
```

### 问题 3: 前端资源加载失败

**症状**: 页面打开时样式错乱或 JS 不加载

**解决方案**:

```bash
# 清除前端缓存
bench clear-cache

# 重新构建前端资源
bench build

# 清除浏览器缓存
# 按 Ctrl+Shift+Delete (Chrome) 或 Cmd+Shift+Delete (Mac)

# 重启 Bench
bench restart
```

### 问题 4: 权限不足 - "User does not have permission"

**症状**: 用户无法访问工作流功能

**解决方案**:

```bash
# 为用户分配角色
bench console

from frappe.auth import _add_user_to_role
_add_user_to_role("user@company.com", "Dynamic Workflow Manager")

# 或在 UI 中手动添加
```

### 问题 5: ���时任务不执行

**症状**: 超时检查、委托同步等定时任务无法执行

**解决方案**:

```bash
# 检查 Bench 后台工作进程
ps aux | grep bench

# 启动后台工作进程（如果未运行）
bench worker

# 在另一个终端启动调度程序
bench schedule

# 查看任务日志
bench --site site.local logs -n 50
```

---

## 升级指南

### 升级前检查清单

- [ ] 备份数据库
- [ ] 备份上传的文件
- [ ] 记录当前版本号
- [ ] 创建测试站点进行测试
- [ ] 通知用户维护时间

### 升级步骤

```bash
# 1. 进入 Bench 目录
cd ~/frappe-bench

# 2. 拉取最新代码
cd apps/dynamic_workflow
git pull origin version-16

# 3. 返回 Bench 目录
cd ~/frappe-bench

# 4. 更新依赖
pip install -r apps/dynamic_workflow/requirements.txt

# 5. 执行数据库迁移
bench migrate --site site.local

# 6. 清除缓存
bench clear-cache --site site.local

# 7. 重新构建资源
bench build --site site.local

# 8. 重启 Bench
bench restart

# 9. 验证升级
# 进入应用检查版本号
```

### 版本兼容性

| Dynamic Workflow 版本 | ERPNext 版本 | Frappe 版本 | 状态 |
|----------------------|-------------|-----------|------|
| 1.0.x | v16 | v16 | ✅ 支持 |
| 1.1.x | v17 | v17 | 🔄 开发中 |

### 回滚方案

如果升级后出现问题：

```bash
# 1. 恢复上一个版本
cd ~/frappe-bench/apps/dynamic_workflow
git revert HEAD

# 2. 重新运行迁移（某些迁移可能不支持回滚）
bench migrate --site site.local

# 3. 清除缓存
bench clear-cache --site site.local

# 4. 重启
bench restart

# 5. 如果仍有问题，恢复数据库备份
```

---

## 卸载步骤

如果需要卸载应用：

```bash
# 1. 备份数据
bench backup --site site.local

# 2. 卸载应用
bench uninstall-app dynamic_workflow --site site.local

# 3. 删除应用文件夹
rm -rf ~/frappe-bench/apps/dynamic_workflow

# 4. 清除缓存
bench clear-cache --site site.local

# 5. 重启
bench restart
```

**注意**: 卸载应用后，审批相关的数据（如 Approval Log）仍会保留在数据库中，用于审计目的。

---

## 性能调优

### 1. 数据库优化

```sql
-- 创建关键字段索引
ALTER TABLE `tabApproval Log` ADD INDEX `idx_document` (`document_type`, `document_name`);
ALTER TABLE `tabApproval Log` ADD INDEX `idx_status` (`status`, `creation`);
ALTER TABLE `tabApproval Delegation` ADD INDEX `idx_delegator` (`delegator`, `status`);
```

### 2. 缓存配置

在 `site_config.json` 中添加：

```json
{
  "cache_ttl": 300,
  "enable_frequent_update_check": false,
  "background_workers": 2,
  "async_task_workers": 2
}
```

### 3. 日志优化

```python
# 在 hooks.py 中配置日志
logger_config = {
    "level": "WARNING",  # 生产环境使用 WARNING
    "retention": 7,  # 保留 7 天日志
}
```

---

## 支持与反馈

- **问题报告**: https://github.com/fwr567/dynamic_workflow/issues
- **讨论区**: https://github.com/fwr567/dynamic_workflow/discussions
- **邮件**: fengweirui567@163.com

---

**安装指南版本**: 1.0.0  
**最后更新**: 2026-07-26
