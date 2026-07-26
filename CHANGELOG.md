# Changelog

所有对 Dynamic Workflow 的重要改变都将在此文件中记录。

版本号遵循 [语义化版本](https://semver.org/lang/zh-CN/) 规范。

## [1.0.0] - 2026-07-26

### 新增
- ✨ 核心审批引擎
  - 灵活的审批矩阵配置
  - 支持串联、并联等多种审批模式
  - 动态审批人计算
  
- ✨ 审批权委托
  - 临时权限委托功能
  - 按日期范围的委托管理
  - 自动过期撤销
  
- ✨ 审批转办和加签
  - 支持单据在审批中的转办
  - 审批过程中的加签功能
  - 灵活的权限转移
  
- ✨ 超时升级管理
  - 可配置的超时时间
  - 多种升级动作 (自动通过/转移/通知)
  - 定期催办提醒
  
- ✨ 业务动作引擎
  - 审批完成后的自动化业务操作
  - 支持字段更新、API 调用、脚本执行等
  - 灵活的条件触发
  
- ✨ 审批追踪和审计
  - 完整的审批历史记录
  - 可视化审批流程时间线
  - 详细的操作日志
  
- ✨ 多渠道通知
  - 邮件通知
  - 企业微信集成 (可选)
  - 短信通知支持 (可选)
  
- ✨ API 接口
  - RESTful API 支持
  - WebHook 集成
  - 第三方系统对接

### 支持的文档类型
- Material Request (物料需求)
- Purchase Order (采购订单)
- Sales Order (销售订单)
- Expense Claim (费用申请) - 部分支持
- Leave Application (请假申请) - 部分支持

### 文档
- 📖 完整的安装部署指南
- 📖 核心文档类型说明
- 📖 最佳实践和故障排查
- 📖 详细的 API 文档
- 📖 项目架构和扩展指南

---

## [1.1.0] - 规划中

### 计划新增功能
- [ ] ERPNext v17 支持
- [ ] 移动端适配
- [ ] 批量审批功能
- [ ] 审批模板库
- [ ] 更多集成渠道 (钉钉、企业飞书等)
- [ ] 高级权限配置 (基于属性的访问控制)
- [ ] 审批数据分析和报表

---

## 版本说明

### 如何升级

```bash
cd ~/frappe-bench
cd apps/dynamic_workflow
git pull origin version-16
cd ~/frappe-bench
bench migrate --site site.local
bench build --site site.local
bench restart
```

### 向后兼容性

- v1.0.x 之间完全向后兼容
- v1.1.0 将支持 ERPNext v17，但保持 v16 兼容

### 支持周期

- v1.0.x: 长期支持 (LTS) - 至少 2 年
- v1.1.x: 标准支持 - 1 年

---

## 贡献

如果您发现 bug 或有功能建议，欢迎提交 Issue 或 Pull Request！

- [报告 Bug](https://github.com/fwr567/dynamic_workflow/issues)
- [功能建议](https://github.com/fwr567/dynamic_workflow/discussions)
- [贡献代码](./CONTRIBUTING.md)
