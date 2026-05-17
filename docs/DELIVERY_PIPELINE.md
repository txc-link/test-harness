# 交付流水线

## 本地流水线

```text
bootstrap -> 校验 Harness 产物 -> lint -> 测试 -> 包检查
```

界面类需求在进入本地流水线前，还必须完成：

```text
Figma 原型 -> 人工确认 -> 需求回写 -> 排期开发 -> 浏览器验证
```

命令：

```powershell
.\scripts\check.ps1
```

## Pull Request 流水线

```text
schema 和产物校验
  -> 必要时校验 prototype review 证据
  -> lint
  -> 单元测试
  -> 必要时运行集成测试
  -> 必要时运行评估 smoke test
  -> 代码评审
```

## 发布流水线

```text
release branch
  -> 冻结范围
  -> 运行完整验证
  -> 生成发布说明
  -> 评审回滚计划
  -> 打 tag
  -> 发布文档和产物
  -> 监控
```

## 环境策略

| 环境 | 用途 | 允许行为 |
| --- | --- | --- |
| local | 本地开发 | 不允许实盘交易 |
| test | CI 验证 | 只允许合成 fixture |
| staging | 集成和 dry run | 只允许模拟交易 |
| shadow_live | 真实市场数据但不执行交易 | 只允许 shadow portfolio |
| production | 用户可见运行环境 | 交易必须经过人工门禁 |
