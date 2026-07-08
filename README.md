# 儿童亲子搞笑卡通短片项目

本项目用于策划、制作和复盘一系列面向 3-6 岁孩子与家长的竖屏亲子搞笑卡通短片。

## 项目定位

- 目标观众：3-6 岁孩子及其家长
- 内容方向：孩子和家长日常相处中的有趣、搞笑、容易共鸣的小故事
- 视频形态：9:16 竖屏短视频
- 单集时长：45-90 秒
- 制作方式：混合制作，人工统一角色和关键质量，AI 辅助分镜、背景、配音和轻动画
- 发布平台：抖音、视频号、小红书等竖屏内容平台

## 目录说明

```text
docs/                  系列设定、制作规范、选题库和复盘方法
templates/             单集策划、分镜和复盘模板
episodes/              已策划的试播集内容
production/            制作流程、检查清单和交付规范
assets/                角色、场景、声音、成片等素材目录
AGENTS.md              Codex 协作规则和启动顺序
codex/                 可迁移的项目记忆和本地技能说明
CHANGELOG.md           每次协作的变更记录
```

## 推荐工作流

1. 阅读 `AGENTS.md`，确认 Codex 协作规则和启动顺序。
2. 阅读 `codex/memory.md`，继承当前业务进展、角色记忆和后续重点。
3. 阅读 `docs/series_bible.md`，确认角色、风格和内容边界。
4. 从 `docs/topic_bank.md` 选择一个选题。
5. 复制 `templates/episode_template.md` 到 `episodes/` 下创建新单集。
6. 按 `production/workflow.md` 完成剧本、分镜、画面、配音、剪辑和审核。
7. 发布后使用 `templates/review_template.md` 做数据复盘。

## Codex 迁移说明

在其他电脑上 clone 本仓库后，先让 Codex 阅读 `AGENTS.md`、`codex/memory.md` 和 `codex/skills/kids_story.md`。这三个文件保存了协作规则、业务进展和项目专用工作流，可直接继续创作、制作和复盘。

## 当前试播集

- `episodes/001_bao_bao_chu_ru_you_er_yuan.md`：宝宝初入幼儿园
- `episodes/001_chi_fan_da_zuo_zhan.md`：吃饭大作战
- `episodes/002_shui_jue_xiao_tan_pan.md`：睡觉小谈判
- `episodes/003_wei_shen_me_lian_huan_pao.md`：为什么连环炮
