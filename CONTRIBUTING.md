# 贡献指南

感谢您对 Dynamic Workflow 项目的关注和贡献！

## 行为准则

本项目采用《贡献者公约》，参与者应遵守以下准则：

- 尊重所有人
- 接受建设性批评
- 不使用骚扰性或侮辱性语言
- 尊重他人的观点和经验

## 如何贡献

### 报告 Bug

1. **搜索现有 Issue**
   - 访问 [Issues 页面](https://github.com/fwr567/dynamic_workflow/issues)
   - 检查是否已有类似报告

2. **创建新 Issue**
   - 点击 "New Issue"
   - 选择 "Bug Report" 模板
   - 填写以下信息：
     - **标题**: 简洁描述问题
     - **复现步骤**: 清楚地说明如何复现 bug
     - **预期行为**: 应该发生什么
     - **实际行为**: 实际发生什么
     - **截图**: 如果适用
     - **环境**: ERPNext 版本、浏览器版本等

### 建议功能

1. **使用 Discussions**
   - 访问 [Discussions 页面](https://github.com/fwr567/dynamic_workflow/discussions)
   - 新建讨论，分享您的想法

2. **或创建功能建议 Issue**
   - 选择 "Feature Request" 模板
   - 描述使用场景和预期结果
   - 解释为什么需要这个功能

### 提交代码

#### 前置准备

1. **Fork 仓库**
   ```bash
   # 在 GitHub 上点击 Fork 按钮
   ```

2. **克隆您的 Fork**
   ```bash
   git clone https://github.com/YOUR_USERNAME/dynamic_workflow.git
   cd dynamic_workflow
   ```

3. **添加上游远程**
   ```bash
   git remote add upstream https://github.com/fwr567/dynamic_workflow.git
   ```

#### 开发流程

1. **创建特性分支**
   ```bash
   # 从 develop 分支创建
   git checkout -b feature/your-feature-name
   
   # 分支命名规范:
   # feature/xxx - 新功能
   # bugfix/xxx - bug 修复
   # docs/xxx - 文档更新
   # refactor/xxx - 代码重构
   # test/xxx - 测试相关
   ```

2. **进行修改**
   - 遵循代码风格规范（见下文）
   - 编写或更新相关测试
   - 更新文档

3. **提交代码**
   ```bash
   # 查看修改
   git status
   
   # 添加修改
   git add .
   
   # 提交
   git commit -m "feat: 添加新的审批模式支持"
   
   # 提交消息规范见下文
   ```

4. **保持与上游同步**
   ```bash
   git fetch upstream
   git rebase upstream/develop
   ```

5. **推送到您的 Fork**
   ```bash
   git push origin feature/your-feature-name
   ```

6. **提交 Pull Request**
   - 访问 GitHub 上您的 Fork
   - 点击 "Compare & pull request"
   - 填写 PR 描述
   - 提交 PR

#### Pull Request 检查清单

- [ ] PR 标题清晰简洁
- [ ] 描述说明了修改的目的和背景
- [ ] 代码遵循项目风格规范
- [ ] 添加/更新了相关测试
- [ ] 更新了相关文档
- [ ] 没有新增 lint 错误
- [ ] 提交历史清晰（每个提交都有意义）
- [ ] 如果涉及 UI 变化，包含截图或演示

---

## 代码风格规范

### Python 代码

遵循 [PEP 8](https://www.python.org/dev/peps/pep-0008/) 规范。

```python
# ✅ 好的做法
def calculate_approval_amount(document, tax_amount=0):
    """计算需要审批的金额"""
    base_amount = document.total_amount
    return base_amount + tax_amount


class ApprovalEngine:
    """审批引擎核心类"""
    
    def __init__(self, doctype, docname):
        self.doctype = doctype
        self.docname = docname
    
    def get_current_approvers(self):
        """获取当前步骤的审批人"""
        pass

# ❌ 避免
def calc_amnt(doc, tax=0):
    base=doc.amt
    return base+tax

class ApprovalEng:
    def __init__(self, dt, dn):
        self.dt = dt
        self.dn = dn
```

### JavaScript 代码

遵循 [Airbnb JavaScript Style Guide](https://github.com/airbnb/javascript)。

```javascript
// ✅ 好的做法
frappe.ui.form.on("Purchase Order", {
  onload: function(frm) {
    // 初始化逻辑
  },
  
  before_submit: function(frm) {
    // 提交前检查
    if (!frm.doc.approval_status) {
      frappe.throw("需要完成审批");
    }
  }
});

// ❌ 避免
frappe.ui.form.on("PurchaseOrder",{onload:function(frm){//code}});
```

### 提交消息规范

遵循 [Conventional Commits](https://www.conventionalcommits.org/zh-hans/)。

格式：
```
<type>(<scope>): <subject>

<body>

<footer>
```

类型：
- `feat`: 新功能
- `fix`: bug 修复
- `docs`: 文档更新
- `style`: 代码风格修改（不影响功能）
- `refactor`: 代码重构
- `perf`: 性能优化
- `test`: 测试相关
- `chore`: 构建、依赖管理等

示例：
```
feat(approval): 添加加签功能

- 允许用户在审批过程中添加新的审批人
- 支持前加签和后加签两种模式
- 完整的加签历史记录

Closes #42
```

---

## 测试

### 运行测试

```bash
# 运行所有测试
bench run-tests --app dynamic_workflow

# 运行特定文件的测试
bench run-tests --app dynamic_workflow dynamic_workflow.tests.test_approval_engine

# 运行特定测试用例
bench run-tests --app dynamic_workflow dynamic_workflow.tests.test_approval_engine:TestApprovalEngine.test_calculate_approvers
```

### 编写测试

```python
# dynamic_workflow/tests/test_approval_engine.py

import frappe
from frappe.test_runner import make_test_records
from dynamic_workflow.dynamic_workflow.approval_engine import ApprovalEngine

class TestApprovalEngine(frappe.TestCase):
    def setUp(self):
        """测试前的准备"""
        self.purchase_order = frappe.new_doc("Purchase Order")
        self.purchase_order.supplier = "Test Supplier"
        self.purchase_order.total_amount = 50000
        self.purchase_order.insert()
    
    def test_calculate_approvers_amount_range(self):
        """测试金额范围的审批人计算"""
        engine = ApprovalEngine("Purchase Order", self.purchase_order.name)
        approvers = engine.get_current_approvers()
        
        # 50000 应该需要财务审批
        self.assertIn("finance_manager@company.com", approvers)
    
    def tearDown(self):
        """测试后的清理"""
        frappe.db.rollback()
```

---

## 文档

### 更新文档

1. 如果修改了功能，更新对应的文档文件
2. 如果添加了新 API，更新 `docs/api.md`
3. 如果改变了配置方式，更新 `docs/installation.md`
4. 更新 `CHANGELOG.md` 中的 "Unreleased" 部分

### 文档格式

- 使用 Markdown 格式
- 代码块包含语言标识（python、javascript 等）
- 包含实际示例和最佳实践
- 中英文混合时，英文和中文间保持空格

---

## 审查流程

1. **自动检查**
   - GitHub Actions 运行 lint 和测试
   - 所有检查必须通过

2. **代码审查**
   - 至少一名维护者审查代码
   - 可能需要修改
   - 通过审查后可以合并

3. **合并**
   - 维护者将 PR 合并到 develop 分支
   - 在下一个版本发布时合并到 main 分支

---

## 发布流程

1. 创建 Release PR
   - 更新版本号
   - 更新 CHANGELOG.md
   - 审查通过后合并

2. 创建 Release
   - GitHub 上创建新 Release
   - 标签格式：`v1.0.0`
   - 发布说明为 CHANGELOG 内容

3. 发布到应用市场
   - 在 Frappe 应用市场发布
   - 通知社区

---

## 获得帮助

- **文档**: 阅读 [docs/](../docs/) 目录
- **讨论**: 在 [Discussions](https://github.com/fwr567/dynamic_workflow/discussions) 提问
- **邮件**: 联系 fengweirui567@163.com

---

## 许可证

通过贡献代码，您同意将贡献遵循本项目的 AGPL-3.0 许可证。

---

感谢您的贡献！🎉
