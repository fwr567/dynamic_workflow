# Dynamic Workflow 快速参考

## 📚 文档导航

### 入门指南
- [安装指南](./docs/installation.md) - 详细的安装步骤和常见问题
- [快速开始](#快速开始) - 5分钟内快速部署

### 详细文档
- [文档类型说明](./docs/doctype_guide.md) - 核心数据模型详解
- [API 文档](./docs/api.md) - 完整的 API 参考
- [最佳实践](./docs/best_practices.md) - 设计原则和优化建议
- [架构设计](./docs/architecture.md) - 系统架构和扩展指南

### 社区
- [贡献指南](./CONTRIBUTING.md) - 如何参与项目
- [更新日志](./CHANGELOG.md) - 版本历史和改进记录

---

## 🚀 快速开始

### 1. 安装 (5分钟)

```bash
cd ~/frappe-bench
bench get-app https://github.com/fwr567/dynamic_workflow
bench install-app dynamic_workflow --site site.local
bench migrate --site site.local
bench restart
```

### 2. 创建第一个审批流 (10分钟)

```
1. 打开 ERPNext，搜索 "Dynamic Workflow"
2. 点击 "工作流配置"，新建配置
3. 选择单据类型：Purchase Order
4. 启用工作流：勾选 "启用"
5. 选择审批矩阵：PO-Standard-Matrix（如果存在）
6. 保存
```

### 3. 创建审批矩阵 (15分钟)

```
1. 进入 "审批矩阵"，新建
2. 设置基本信息：
   - 单据类型：Purchase Order
   - 描述：标准采购订单审批
   - 启用：勾选
3. 添加审批规则：
   - 序号 1：部门主管 (不需要金额限制)
   - 序号 2：采购经理 (最小5000元)
   - 序号 3：财务部 (最小50000元)
4. 提交
```

完成后，创建采购订单时会自动显示审批流程！

---

## 💡 常见场景

### 场景1：按金额分级审批

**需求**: 不同金额由不同级别审批

**配置**:
```json
{
  "矩阵": "按金额分级",
  "规则1": {
    "金额": "0-10000",
    "审批人": "部门主管"
  },
  "规则2": {
    "金额": "10000-100000", 
    "审批人": "部门主管 → 经理"
  },
  "规则3": {
    "金额": ">100000",
    "审批人": "部门主管 → 经理 → 总经理"
  }
}
```

### 场景2：多部门并联审批

**需求**: 多个部门同时审批（都同意才能通过）

**配置**:
```json
{
  "模板": "并联审批",
  "步骤1": {
    "审批人": ["采购部经理", "财务部经理", "法律部经理"],
    "模式": "并联",
    "条件": "所有人都同意才能通过"
  }
}
```

### 场景3：权限委托

**需求**: 出差时，权限临时委托给他人

**操作**:
1. 进入 "审批委托"
2. 新建委托
3. 填写：
   - 委托人：您的账户
   - 被委托人：代理人账户
   - 开始日期：出发日期
   - 结束日期：返回日期
4. 提交

期间您的所有审批权都由被委托人代理。

---

## 🔧 常见问题速查

### Q: 如何查看待审批单据？
**A**: 在主页顶部菜单中搜索 "待审批" 或访问 "Dynamic Workflow" 应用

### Q: 如何跳过某个审批步骤？
**A**: 在工作流配置中，将该步骤标记为 "可选"

### Q: 如何修改已提交的单据？
**A**: 单据通过所有审批后才能修改；如需修改未通过的单据，可回退到起始步骤

### Q: 超时了怎么办？
**A**: 系统会自动发送催办邮件；48小时未处理会自动升级

### Q: 如何导出审批报表？
**A**: 在 "审批日志" 列表中选择记录，点击 "导出" → "Excel"

### Q: 能否添加新的文档类型？
**A**: 可以，编辑 `hooks.py` 或联系管理员

---

## 📊 关键指标

| 指标 | 说明 |
|-----|------|
| 审批通过率 | 批准 / 提交总数 |
| 平均审批时间 | 从创建到通过的平均时间 |
| 超期比例 | 超过超时时间的审批占比 |
| 拒绝率 | 被拒绝的审批占比 |

**查看方式**: "Dynamic Workflow" → "审批统计"

---

## 🔐 权限管理

### 默认角色

| 角色 | 权限 |
|-----|------|
| System Manager | 管理所有工作流配置 |
| Workflow Manager | 配置审批矩阵和规则 |
| Document Approver | 审批和处理文档 |
| Department Head | 部门级审批权 |

### 如何给用户分配权限

1. 打开用户账户
2. 在 "角色" 标签中添加角色
3. 保存

---

## 🎓 学习资源

### 在线文档
- [安装指南](./docs/installation.md) - 详细的部署步骤
- [文档类型说明](./docs/doctype_guide.md) - 完整的字段说明
- [API 文档](./docs/api.md) - 所有 API 接口参考
- [最佳实践](./docs/best_practices.md) - 配置和优化建议

### 示例配置
- [标准制造企业审批流](https://github.com/fwr567/workflow-examples)
- [贸易公司采购流程](https://github.com/fwr567/workflow-examples)

---

## 🆘 获得帮助

### 寻求支持

1. **搜索文档** - 大多数问题都能在文档中找到答案
2. **查看 Issues** - 在 [GitHub Issues](https://github.com/fwr567/dynamic_workflow/issues) 中搜索
3. **提出问题** - 在 [Discussions](https://github.com/fwr567/dynamic_workflow/discussions) 中新建讨论
4. **邮件** - 联系 fengweirui567@163.com

### 报告 Bug

如果遇到问题：
1. 记录错误信息和操作步骤
2. 在 GitHub 上 [创建 Issue](https://github.com/fwr567/dynamic_workflow/issues/new)
3. 包含尽可能多的细节信息

---

## 📝 便捷命令

### Bench 命令

```bash
# 安装应用
bench get-app https://github.com/fwr567/dynamic_workflow
bench install-app dynamic_workflow

# 卸载应用
bench uninstall-app dynamic_workflow

# 更新应用
cd apps/dynamic_workflow && git pull && cd ../..
bench migrate

# 查看日志
bench --site site.local logs

# 进入数据库
bench --site site.local mysql-console
```

### 常用数据库查询

```sql
-- 查看待审批单据数
SELECT COUNT(*) FROM `tabApproval Log` WHERE status = 'Pending';

-- 查看平均审批时间
SELECT AVG(TIMESTAMPDIFF(HOUR, creation, modified)) 
FROM `tabApproval Log` 
WHERE status = 'Approved';

-- 按审批人统计
SELECT approver, COUNT(*) as count, 
  AVG(TIMESTAMPDIFF(HOUR, creation, modified)) as avg_hours
FROM `tabApproval Log`
WHERE status = 'Approved'
GROUP BY approver
ORDER BY count DESC;
```

---

## 🎉 做得好！

现在您已经掌握了 Dynamic Workflow 的基础知识。

**下一步**:
- 📖 阅读 [最佳实践](./docs/best_practices.md) 了解高级配置
- 🔌 探索 [API 功能](./docs/api.md) 进行系统集成
- 🤝 考虑 [贡献代码](./CONTRIBUTING.md) 参与项目

---

## 功能特性总结

✅ 灵活的审批矩阵配置  
✅ 支持多种审批模式 (串联、并联、任意一人)  
✅ 权限委托与转办  
✅ 自动超时升级  
✅ 业务动作自动化  
✅ 完整的审批追踪  
✅ 多渠道通知 (邮件、微信等)  
✅ RESTful API & WebHook  
✅ 详细的审计日志  
✅ 高性能和可扩展  

---

**更新时间**: 2026-07-26  
**版本**: 1.0.0  
**许可证**: AGPL-3.0
