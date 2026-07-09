# 变更记录

## 2026-07-09

- 重新生成《独立自主吃饭》前三页 v2 预览底图，修正餐桌道具和三分格餐盘连续性，并更新 `scripts/render_episode_002_preview_pages.py` 支持 `v2` 非覆盖输出。
- 按新的分镜连续性规则重写《独立自主吃饭》`storyboard.md`，统一餐厅空间、桌椅、桌垫、餐盘、碗杯、儿童勺和食物移动逻辑，避免前后画面穿帮。
- 更新绘本专用技能和项目总技能，新增“分镜连续性硬规则”：每页必须记录主要道具和环境连续性，后续画面继承仍在现场的关键物件，同时当前画面氛围仍服从当页分镜。
- 更新绘本文字规则，要求台词对白必须完整显示在对话气泡或文字容器里，不能截断、溢出、压边或被遮挡；文案过长时先拆句或改写。
- 生成《独立自主吃饭》前三页绘本预览图，保存有字版 `images/page_01.png` 至 `images/page_03.png`，并保留无字底图 `images/page_01_base.png` 至 `images/page_03_base.png`。
- 新增前三页预览叠字脚本 `scripts/render_episode_002_preview_pages.py`，用于把准确中文文案叠入 AI 生成图的预留文字区。
- 完成《独立自主吃饭》10 页绘本分镜确认稿 `picture_books/episode_002_du_li_zi_zhu_chi_fan/storyboard.md`，补充每页文字安全区、角色一致性提示词和风险点。
- 更新绘本专用技能和项目总技能，新增“文字入画硬规则”：每页旁白和对白必须清晰、友好、艺术化地融入画面，不能遮挡主体，也不能在页面底部留下大面积空白文字区。
- 完成《独立自主吃饭》10 页绘本剧本文案确认稿 `picture_books/episode_002_du_li_zi_zhu_chi_fan/script.md`，并将主线稿状态更新为已确认。
- 新增《独立自主吃饭》绘本主线确认稿 `picture_books/episode_002_du_li_zi_zhu_chi_fan/storyline.md`，本次仅进入主线确认阶段，未生成完整剧本、分镜、图片或 PDF。
- 更新绘本专用技能和项目总技能，将“三个主角必须使用已定稿角色形象”明确为硬规则，要求分镜图、绘本页图和画面提示词都保持角色一致性。
- 根据用户反馈，确认第一集绘本制作效果基本符合预期，后续优先沉淀绘本制作流程。
- 新增项目专用绘本技能 `codex/skills/picture_book_creation.md`，明确新主题绘本的确认式流程：主线确认、剧本确认、分镜确认、图片生成、PDF 交付。
- 更新 `codex/skills/kids_story.md`，将绘本专用技能纳入本项目通用创作入口。
- 更新 `codex/memory.md`，记录下次用户只给主题时默认先做绘本，并暂时忽略视频制作优化。

## 2026-07-08

- 为第一集《宝宝初入幼儿园》新增 HyperFrames 视频工程目录，准备按绘本关键帧制作 9:16 短视频。
- 新增视频视觉规范 `videos/episode_001_bao_bao_chu_ru_you_er_yuan/DESIGN.md`，明确使用定稿角色和暖色儿童绘本风格。
- 新增分句配音与音效生成脚本 `scripts/generate_episode_001_audio.py`，用于逐句对齐对白时间轴。
- 生成第一集视频配音、音效和背景音乐，保存到 `videos/episode_001_bao_bao_chu_ru_you_er_yuan/assets/audio/`。
- 新增第一集 HyperFrames 主合成文件 `videos/episode_001_bao_bao_chu_ru_you_er_yuan/index.html`，完成 10 个镜头、17 条字幕、音频与转场的时间线编排。
- 为视频工程安装本地静态 `ffmpeg-static` 和 `ffprobe-static` 依赖，用于 HyperFrames 导出 MP4。
- 完成第一集视频渲染，输出 `output/video/bao_bao_chu_ru_you_er_yuan.mp4`。
- 新增视频验收预览图 `output/video/bao_bao_chu_ru_you_er_yuan_scene_check.jpg` 和 `output/video/bao_bao_chu_ru_you_er_yuan_contact_sheet.jpg`。
- 完成 HyperFrames 验收：`lint` 0 错误，`validate` 通过，`inspect --samples 18` 0 布局问题，`ffprobe` 确认视频 93 秒且包含音轨。
- 修正第一集目标时长为 93 秒，与现有对白时间轴 `00:00-01:33` 保持一致。
- 生成第一集绘本最终版 PDF：`output/pdf/bao_bao_chu_ru_you_er_yuan_picture_book.pdf`，包含封面、10 页绘本正文和完整对白台词附录。
- 新增 `scripts/generate_picture_book_pdf.py`，用于从绘本页面数据和图片自动生成 PDF。
- 新增第一集《宝宝初入幼儿园》独立绘本目录 `picture_books/episode_001_bao_bao_chu_ru_you_er_yuan/`。
- 将 10 张分镜图复制为绘本页图 `page_01.png` 至 `page_10.png`，并新增 `storybook.md`、`pages.json` 和图片匹配检查记录。
- 重生成第 5 页“勇气贴纸”画面，使婷婷妈妈和北斗爸爸身上的贴纸都清晰可见，并同步替换绘本页图和原分镜图。
- 新增 `AGENTS.md`，记录 Codex 中国开发者默认规则、协作要求和项目启动顺序。
- 新增 `codex/memory.md`，沉淀项目定位、业务进展、角色记忆、内容边界和下次继续事项。
- 新增 `codex/skills/kids_story.md`，记录本项目短片策划、创作、分镜、审核和交付技能流程。
- 新增 `.gitignore`，排除系统文件、本地配置、环境变量、依赖缓存、日志和临时导出文件。
- 更新 README，加入 Codex 迁移说明，确保其他电脑 clone 后能直接继续协作。
- 更新角色提示词记录，移除本机绝对参考照片路径，改为以入库角色设定图作为可迁移参考。
- 为第一集《宝宝初入幼儿园》新增开场镜头：小北斗开心奔向幼儿园，婷婷妈妈和北斗爸爸跟在后面送他。
- 将开场歌唱段改写为原创入园小歌，并同步更新对白、分镜、字幕和音效点。
- 生成并整理第一集 10 张竖屏分镜关键帧，保存到 `assets/scenes/episode_001_bao_bao_chu_ru_you_er_yuan/`。
- 新增第一集分镜图片清单 `storyboard_assets.md`，用于后续剪辑和视频生成。
- 重新生成婷婷妈妈白 T 牛仔裤版角色图，并覆盖 `ting_ting_ma_ma_turnaround.png` 和 `ting_ting_ma_ma_summer_turnaround.png`。
- 更新角色提示词、系列圣经和已有剧集画面提示词，使婷婷妈妈统一呈现气质、干练、活泼、热情的新版造型。
- 新增第一集《宝宝初入幼儿园》剧情策划稿，包含对白、分镜、画面提示词、配音文本、字幕文本和发布信息。
- 更新选题库和 README，将《宝宝初入幼儿园》纳入当前试播集。
- 重新生成婷婷妈妈年轻夏装裙子版角色图，并覆盖 `ting_ting_ma_ma_turnaround.png` 和 `ting_ting_ma_ma_summer_turnaround.png` 两个旧妈妈角色图。
- 增加角色一致性要求，后续剧情分镜统一采用 `assets/characters/` 中的转面设定图。
- 生成过婷婷妈妈夏装裙子版转面设定图，后续已被年轻夏装新版覆盖。
- 更新系列圣经和角色提示词记录，使婷婷妈妈服装与小北斗、北斗爸爸的夏装保持一致。
- 根据三张参考照片生成三位主角的卡通转面设定图，并保存到 `assets/characters/`。
- 新增角色形象生成提示词记录，便于后续重生成和统一风格。
- 更新三位主角名称：小北斗、婷婷妈妈、北斗爸爸。
- 初始化儿童亲子搞笑卡通短片项目资料。
- 新增系列圣经，明确角色设定、视觉风格、声音风格和内容边界。
- 新增选题库，包含 3 集试播选题和 20 集后续主题。
- 新增制作流程、质量检查清单、单集模板和复盘模板。
- 完成 3 集试播策划稿：《吃饭大作战》《睡觉小谈判》《为什么连环炮》。
