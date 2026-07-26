# 📚 Dynamic Workflow 文档中心

欢迎来到 Dynamic Workflow 文档中心！这里汇集了所有帮助您快速上手、深入学习和问题解决的资源。

---

## 🎯 按用途分类

### 👶 我是新用户

**目标**: 快速了解项目并完成第一个审批流配置

**推荐路径**:
1. 📖 [README.md](../README.md) - 了解项目概况 (5分钟)
2. 📖 [QUICKSTART.md](../QUICKSTART.md) - 快速参考指南 (10分钟)
3. 📖 [安装指南](./installation.md) - 完成安装和初始配置 (30分钟)
4. 🎓 实际操作 - 创建第一个审批矩阵 (15分钟)

**时间投入**: ~1小时

---

### 💼 我需要配置特定场景

**目标**: 根据业务需求配置审批流

**推荐资源**:
- 📖 [最佳实践](./best_practices.md#常见业务场景) - 常见场景配置
- 📖 [文档类型说明](./doctype_guide.md) - 理解核心数据模型
- 📖 [快速参考](../QUICKSTART.md#💡-常见场景) - 常见场景速查

**按场景**:
- 📋 按金额分级审批 → [最佳实践 - 场景1](./best_practices.md#场景1电商平台订单审批)
- 📋 多部门并联审批 → [最佳实践 - 场景2](./best_practices.md#场景2多部门协同审批)
- 📋 权限委托 → [QUICKSTART - 场景3](../QUICKSTART.md#场景3权限委托)
- 📋 超时自动升级 → [安装指南 - 配置7](./installation.md#配置-7-配置超时规则)

---

### 🔧 我遇到了问题

**目标**: 快速找到解决方案

**推荐资源**:
1. 📖 [快速参考 - FAQ](../QUICKSTART.md#🔧-常见问题速查) - 常见问题列表
2. 📖 [最佳实践 - 故障排查](./best_practices.md#故障排查指南) - 常见错误和解决方案
3. 📖 [安装指南 - 常见问题](./installation.md#常见安装问题) - 安装相关问题

**如果以上无法解决**:
- 💬 [GitHub Discussions](https://github.com/fwr567/dynamic_workflow/discussions)
- 🐛 [GitHub Issues](https://github.com/fwr567/dynamic_workflow/issues)
- 📧 邮件: fengweirui567@163.com

---

### 🔌 我需要集成 API

**目标**: 通过 API 与其他系统集成

**推荐资源**:
1. 📖 [API 文档](./api.md) - 完整的 API 参考 (30分钟)
2. 📖 [架构设计 - API 模块](./architecture.md#1-api-模块-api) - 理解 API 结构
3. 📖 [最佳实践 - API 集成](./best_practices.md#api-集成最佳实践) - 集成建议

**常见 API**:
- 获取待审批单据 → [API 文档 - 基础 API](./api.md#1-获取文档的审批状态)
- 提交审批 → [API 文档 - 审批操作](./api.md#1-提交审批批准)
- WebHook 集成 → [API 文档 - WebHook](./api.md#1-审批事件-webhook)

---

### 🏗️ 我想要扩展功能

**目标**: 自定义或扩展系统功能

**推荐资源**:
1. 📖 [架构设计](./architecture.md) - 了解系统结构 (45分钟)
2. 📖 [最佳实践 - 扩展指南](./best_practices.md#扩展和定制) - 扩展建议
3. 📖 [贡献指南](../CONTRIBUTING.md) - 开发规范

**常见扩展**:
- 添加新文档类型 → [架构 - 扩展指南](./architecture.md#添加新的文档类型支持)
- 添加通知渠道 → [架构 - 扩展指南](./architecture.md#添加新的通知渠道)
- 自定义超时规则 → [架构 - 扩展指南](./architecture.md#自定义超时规则)

---

### 🤝 我想要参与项目

**目标**: 贡献代码或文档

**推荐资源**:
1. 📖 [贡献指南](../CONTRIBUTING.md) - 完整的贡献流程
2. 📖 [架构设计](./architecture.md) - 理解项目结构
3. 📖 [更新日志](../CHANGELOG.md) - 了解项目状态

**流程**:
1. Fork 仓库
2. 创建特性分支
3. 按照 [贡献指南](../CONTRIBUTING.md#代码风格规范) 编写代码
4. 提交 Pull Request

---

## 📖 完整文档列表

### 核心文档

| 文档 | 内容 | 适合人群 | 时间 |
|-----|------|--------|------|
| [README.md](../README.md) | 项目概况和功能介绍 | 所有人 | 5分钟 |
| [QUICKSTART.md](../QUICKSTART.md) | 快速参考和常见问题 | 新用户/快速查询 | 10分钟 |
| [CHANGELOG.md](../CHANGELOG.md) | 版本历史和功能改进 | 关注更新 | 5分钟 |

### 安装部署

| 文档 | 内容 | 适合人群 | 时间 |
|-----|------|--------|------|
| [安装指南](./installation.md) | 安装步骤、配置、问题排查 | 部署人员 | 1小时 |
| [最佳实践](./best_practices.md) | 配置原则、性能优化、故障排查 | 管理员 | 1小时 |

### 开发文档

| 文档 | 内容 | 适合人群 | 时间 |
|-----|------|--------|------|
| [文档类型说明](./doctype_guide.md) | 核心数据模型详解 | 开发者 | 1.5小时 |
| [API 文档](./api.md) | REST API 完整参考 | 集成开发 | 1小时 |
| [架构设计](./architecture.md) | 系统架构、数据流、扩展指南 | 架构师/高级开发 | 2小时 |
| [贡献指南](../CONTRIBUTING.md) | 开发规范、测试、提交流程 | 贡献者 | 30分钟 |

---

## 🔍 按主题查找

### 审批流程配置

- [快速参考 - 快速开始](../QUICKSTART.md#🚀-快速开始)
- [安装指南 - 初始配置](./installation.md#初始配置)
- [文档类型说明 - 审批矩阵](./doctype_guide.md#1-审批矩阵approval-matrix)
- [最佳实践 - 常见业务场景](./best_practices.md#常见业务场景)

### 权限和角色

- [安装指南 - 权限管理](./installation.md#初始配置)
- [快速参考 - 权限管理](../QUICKSTART.md#🔐-权限管理)
- [最佳实践 - 权限设计](./best_practices.md#权限设计建议)

### 通知和集成

- [安装指南 - 通知配置](./installation.md#配置-6-配置通知)
- [API 文档 - WebHook](./api.md#webhook-集成)
- [最佳实践 - API 集成](./best_practices.md#api-集成最佳实践)
- [架构 - 集成模块](./architecture.md#5-集成模块-integrations)

### 性能和优化

- [安装指南 - 性能调优](./installation.md#性能调优)
- [最佳实践 - 性能优化](./best_practices.md#性能优化建议)
- [架构 - 关键算法](./architecture.md#关键算法)

### 故障和调试

- [快速参考 - FAQ](../QUICKSTART.md#🔧-常见问题速查)
- [安装指南 - 常见问题](./installation.md#常见安装问题)
- [最佳实践 - 故障排查](./best_practices.md#故障排查指南)

### 扩展和定制

- [架构 - 扩展指南](./architecture.md#扩���指南)
- [最佳实践 - 扩展定制](./best_practices.md#扩展和定制)
- [贡献指南 - 提交代码](../CONTRIBUTING.md#提交代码)

---

## 💡 热门问题快速导航

### Q: 如何安装 Dynamic Workflow？
→ [安装指南](./installation.md#安装步骤)

### Q: 如何创建审批流程？
→ [快速开始](../QUICKSTART.md#🚀-快速开始)

### Q: 如何配置不同的审批规则？
→ [最佳实践 - 常见场景](./best_practices.md#常见业务场景)

### Q: 如何与第三方系统集成？
→ [API 文档](./api.md)

### Q: 遇到了错误怎么办？
→ [故障排查](./best_practices.md#故障排查指南)

### Q: 如何贡献代码？
→ [贡献指南](../CONTRIBUTING.md)

### Q: 如何扩展功能？
→ [架构 - 扩展指南](./architecture.md#扩展指南)

---

## 📊 文档导图

```
START
  ↓
是否已安装？
  ├─ 否 → 安装指南 → 初始配置
  └─ 是 ↓
      需要快速了解？
      ├─ 是 → QUICKSTART → 快速参考
      └─ 否 ↓
          需要配置审批流？
          ├─ 是 → 最佳实践 → 常见场景
          └─ 否 ↓
              需要集成 API？
              ├─ 是 → API 文档 → 具体接口
              └─ 否 ↓
                  遇到问题？
                  ├─ 是 → 故障排查 → 解决方案
                  └─ 否 ↓
                      想要扩展？
                      ├─ 是 → 架构设计 → 扩展指南
                      └─ 否 → 贡献指南 → 参与项目
```

---

## 🎓 学习路径建议

### 初级用户 (1-2天)
1. README 概览 (5分钟)
2. QUICKSTART 快速参考 (10分钟)
3. 安装指南 (30分钟)
4. 实际操作：创建第一个审批流 (30分钟)

**总计**: ~1.5小时

### 中级用户 (1周)
1. 完成初级路径
2. 文档类型说明 (1小时)
3. 最佳实践 (1小时)
4. 实际操作：配置复杂审批流程
5. API 文档入门 (30分钟)

**总计**: ~4小时

### 高级用户 (2-4周)
1. 完成中级路径
2. 架构设计深入学习 (2小时)
3. API 文档详细研究 (1小时)
4. 实际操作：开发自定义扩展
5. 贡献指南 (30分钟)

**总计**: ~10小时

---

## 🔗 外部资源

### 相关文档
- [ERPNext 官方文档](https://docs.erpnext.com)
- [Frappe 框架文档](https://frappeframework.com)

### 社区
- [GitHub Issues](https://github.com/fwr567/dynamic_workflow/issues)
- [GitHub Discussions](https://github.com/fwr567/dynamic_workflow/discussions)
- [ERPNext Community](https://discuss.erpnext.com)

### 工具
- [GitHub 仓库](https://github.com/fwr567/dynamic_workflow)
- [发行版本](https://github.com/fwr567/dynamic_workflow/releases)

---

## 📝 文档维护

- **最后更新**: 2026-07-26
- **文档版本**: 1.0.0
- **维护者**: fwr567

### 如何反馈文档问题

如果您发现文档有误或不清楚：
1. [创建 Issue](https://github.com/fwr567/dynamic_workflow/issues)
2. 在 Discussions 中提问
3. 发送邮件至 fengweirui567@163.com

---

## 🎯 下一步行动

- ✅ 已安装？ → 查看 [QUICKSTART](../QUICKSTART.md)
- ✅ 想要学习？ → 按照 [学习路径](#🎓-学习路径建议) 学习
- ✅ 遇到问题？ → 查看 [FAQ](../QUICKSTART.md#🔧-常见问题速查)
- ✅ 想要参与？ → 阅读 [贡献指南](../CONTRIBUTING.md)

---

**祝您使用愉快！** 🎉
