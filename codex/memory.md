# Codex 项目记忆

## 项目定位

本项目是面向 3-6 岁孩子与家长的亲子搞笑卡通短片资料库，主打 9:16 竖屏短视频。内容围绕日常亲子小冲突展开，先好笑，再自然落到温情，不做说教。

## 当前业务进展

- 已建立完整项目结构：`docs/`、`templates/`、`episodes/`、`production/`、`assets/`。
- 已完成系列圣经、选题库、发布策略、制作流程、质量检查清单、单集模板和复盘模板。
- 已完成 4 个试播集策划稿：
  - `episodes/001_chi_fan_da_zuo_zhan.md`：吃饭大作战。
  - `episodes/002_shui_jue_xiao_tan_pan.md`：睡觉小谈判。
  - `episodes/003_wei_shen_me_lian_huan_pao.md`：为什么连环炮。
  - `episodes/001_bao_bao_chu_ru_you_er_yuan.md`：宝宝初入幼儿园。
- 已生成并保存 3 位主角的转面设定图，后续画面生成必须优先参考 `assets/characters/`。
- 婷婷妈妈形象已经统一为白 T 牛仔裤版，不再使用旧版冬装、裙装、围裙或靴子造型。
- 第一集《宝宝初入幼儿园》的绘本制作效果基本符合用户预期，后续优先沉淀并复用绘本流程。
- 已新增绘本专用技能 `codex/skills/picture_book_creation.md`：用户下次只给主题时，先做主线确认，再做剧本确认，再做分镜确认，最后生成图片、绘本文件夹和 PDF。
- 当前视频效果暂不作为标准流程，后续用户另行调整；新主题默认先忽略视频制作。
- 《独立自主吃饭》外部生图试验已终止并移除：不再使用、不再保留 coincoin.ai 和火山 Ark 作为候选方案；后续绘本页图统一使用 Codex 默认生图能力，并通过角色参考图、连续性提示词和人工复查保障一致性。

## 角色记忆

### 小北斗

- 4 岁半，中国男孩，圆脸、大眼睛，活泼、嘴甜、歪理多。
- 常用口头禅：“我有一个好办法！”、“再等一下下。”、“可是为什么呀？”
- 后续生成应参考 `assets/characters/xiao_bei_dou_turnaround.png`。

### 婷婷妈妈

- 年轻、有活力、有气质，细心、效率高，容易被小北斗的逻辑绕晕。
- 固定造型：长浅棕色自然卷发、白色短袖 T 恤、中蓝色修身牛仔裤、白色休闲鞋。
- 禁止恢复毛线帽、红色冬装、厚毛衣、裙装、围裙、靴子、破洞牛仔裤、低腰裤、露脐装或显老妇女感造型。
- 后续生成应参考 `assets/characters/ting_ting_ma_ma_turnaround.png` 和 `assets/characters/ting_ting_ma_ma_summer_turnaround.png`。

### 北斗爸爸

- 幽默、爱配合孩子演戏，有时帮倒忙。
- 形象为温和圆脸、短黑发、眼镜，服装以白色 T 恤、深蓝休闲裤、白色运动鞋为准。
- 后续生成应参考 `assets/characters/bei_dou_ba_ba_turnaround.png`。

## 内容边界

- 不出现危险模仿动作。
- 不出现打骂、羞辱、恐吓式教育。
- 不提供医疗、药品或疾病判断建议。
- 不展示儿童隐私或不适合儿童观看的内容。
- 不把撒谎、破坏规则、浪费食物包装成胜利。

## 下次继续时优先事项

1. 如用户给新绘本主题，先读取 `codex/skills/picture_book_creation.md`，按“主线确认 → 剧本确认 → 分镜确认 → 图片生成 → PDF 交付”推进。
2. 如继续第一集《宝宝初入幼儿园》，先检查 `episodes/001_bao_bao_chu_ru_you_er_yuan.md` 和角色图一致性。
3. 如新增剧集，从 `docs/topic_bank.md` 选择选题，并复制 `templates/episode_template.md`。
4. 如进入制作阶段，按 `production/workflow.md` 七阶段推进。
5. 如准备发布，按 `production/quality_checklist.md` 完成安全、视觉、声音和平台检查。
6. 每次协作结束前更新 `CHANGELOG.md`，记录日期、修改内容和素材状态。
7. 生图方案不得再回退到 coincoin.ai 或火山 Ark；如需评估其他外部方案，必须先单独确认，并不得复用已移除的两条路径。
