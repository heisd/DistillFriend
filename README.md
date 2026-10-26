# DistillFriend · 人物档案与朋友风格整理

将聊天材料、共同经历和人工修正整理成可以持续维护的朋友档案。核心资源位于 [create-friend/](./create-friend)，包含工作流程、提示词、证据结构与本地管理脚本。

本项目生成的不是单一句子提示，而是将人物风格、共享记忆和关系模式分开保存，便于逐步补充与修正。初始化脚本只创建文件骨架，实际内容仍需要结合材料整理。

## 适合的使用方式

- 将零散聊天记录整理为表达习惯、偏好与事实。
- 为写作或模拟回复准备人物风格参考。
- 区分直接证据、人工印象、推断与未知内容。
- 在新材料出现后增量更新，并保留可恢复的历史版本。

档案是对已有材料的整理与近似表达，不等于本人，也不能据此保证某个人未来会如何回应。

## 项目结构

```text
create-friend/
├── README.md                   # 原始完整使用教程
├── SKILL.md                    # 工作流程定义
├── agents/openai.yaml          # Agent 元数据
├── prompts/
│   ├── intake.md
│   ├── persona_builder.md
│   ├── memory_builder.md
│   ├── relationship_builder.md
│   └── correction_handler.md
├── references/evidence_model.md
└── scripts/
    ├── friend_writer.py
    └── version_manager.py
```

| 输出文件 | 内容 |
| --- | --- |
| `meta.json` | 名称、slug、时间与来源摘要等元数据 |
| `persona.md` | 表达风格、性格、偏好与边界 |
| `memory.md` | 事实、共同经历、时间线与未知项 |
| `relationship.md` | 双方关系、互动模式、支持方式与共同梗 |
| `SKILL.md` | 读取上述资料并遵循边界的调用规则 |

## 获取与初始化

脚本使用 Python 标准库，源码使用了较新的 Python 类型标注；建议使用 Python 3.9 或以上。无需先配置模型 API，就可以运行档案初始化和版本管理。

```bash
git clone --branch lqy https://github.com/heisd/DistillFriend.git
cd DistillFriend/create-friend
python3 scripts/friend_writer.py init --base-dir ./friends --name "阿哲" --slug azhe
python3 scripts/friend_writer.py list --base-dir ./friends
```

Windows 可将 `python3` 替换为本机的 `python`。显式设置 `--slug azhe` 后，生成目录为 `friends/azhe/`，后续命令也使用该路径。

初始化采用“缺失时才写入”的逻辑，不会自动覆盖已有档案内容；重复运行初始化不能代替内容更新。

## 一次完整的整理流程

1. 准备昵称、关系、一句话印象，以及允许使用的聊天或经历材料。
2. 使用脚本创建档案骨架。
3. 参考 [create-friend/SKILL.md](./create-friend/SKILL.md) 与相应提示词整理内容。
4. 将有证据的事实与推断分开；不知道的部分保留未知。
5. 分别检查闲聊、安慰与记忆引用，定位偏差来自哪个文件。
6. 备份后修正，并记录改动原因。

可使用下面的请求作为起点：

```text
参考 create-friend 的流程，整理 friends/azhe 中的档案。
昵称：阿哲
关系：大学室友
材料：我接下来提供的聊天与共同经历。
请区分事实、主观印象和推断，不补写材料中没有的经历。
输出 persona.md、memory.md、relationship.md，并检查调用规则是否一致。
```

提示中的路径是从项目中选择的相对位置，实际使用时应让工具访问克隆后的真实目录。

## 备份、查询与恢复

在修改档案前创建快照：

```bash
python3 scripts/version_manager.py backup --profile-dir ./friends/azhe
python3 scripts/version_manager.py list --profile-dir ./friends/azhe
```

版本保存在档案目录下的 `.versions/`，目录名采用 UTC 时间标签。恢复时把下面的占位值替换成 list 返回的实际版本：

```bash
python3 scripts/version_manager.py restore --profile-dir ./friends/azhe --version VERSION_FROM_LIST
```

版本脚本跟踪上述五个文件。它不是整个目录的完整备份系统；恢复会复制快照中存在的文件，不自动管理所有额外材料，也不删除后续创建的其他文件。

## 如何避免档案越改越偏

| 问题 | 优先修改位置 |
| --- | --- |
| 语气过于热情或不像本人 | persona.md |
| 编造或混淆共同经历 | memory.md 与证据说明 |
| 安慰、冲突或玩笑方式不对 | relationship.md |
| 回复忽略边界或不读取材料 | SKILL.md |
| 新信息与旧信息矛盾 | 先核对来源，再记录修正原因 |

与其一次生成大量细节，更适合用小批材料反复核对。原始资料、人物推断和最终表达应保持可追溯。

## 常见问题

- **初始化后只有“待补充”**：脚本负责骨架生成，不会自动调用模型分析材料。
- **找不到原教程中的绝对路径**：那些路径来自原开发环境；从本机克隆目录进入 `create-friend/` 即可。
- **恢复不包含某些附件**：版本管理只复制固定的档案文件，附件需自行保存。
- **不知道人物某项信息**：在档案中明确未知，避免用常见人物设定补齐。
- **希望分享生成结果**：先核对原始材料的使用范围，移除不需要传播的个人信息。

更完整的原始示例见 [子目录教程](./create-friend/README.md)。
