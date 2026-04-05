# create-friend

把一个现实里的朋友蒸馏成可复用的 AI Skill。

它适合把聊天记录、截图、笔记、社交媒体内容、共同经历和你的主观印象，整理成一个**有边界、尽量基于证据、不乱编记忆**的朋友画像。

生成结果不是单一 prompt，而是一整套可持续更新的朋友档案：

- `persona.md`：性格、语气、习惯、偏好、边界
- `memory.md`：共享记忆、关键事实、时间线、未知项
- `relationship.md`：你和 TA 的互动方式、支持风格、冲突方式、梗和默契
- `SKILL.md`：最终可调用的朋友 skill

---

## 适合什么场景

当你想让 Codex：

- 帮你蒸馏一个朋友
- 基于聊天记录还原一个朋友的说话方式
- 做一个“像这个朋友一样回复”的角色 skill
- 长期维护一个朋友 persona，并持续追加修正
- 让 AI 在安慰、闲聊、回忆共同经历时更像某个具体的人

---

## 目录结构

```text
create-friend/
├── SKILL.md
├── README.md
├── agents/
│   └── openai.yaml
├── prompts/
│   ├── intake.md
│   ├── persona_builder.md
│   ├── memory_builder.md
│   ├── relationship_builder.md
│   └── correction_handler.md
├── references/
│   └── evidence_model.md
└── scripts/
    ├── friend_writer.py
    └── version_manager.py
```

生成出来的朋友档案默认放在：

```text
./friends/{slug}/
```

例如：

```text
./friends/azhe/
├── meta.json
├── persona.md
├── memory.md
├── relationship.md
└── SKILL.md
```

---

## 两种使用方式

## 方式一：本地直接参考使用（最简单）

如果你只是想在当前项目里把它当模板/工作流来用，不一定要先安装到全局技能目录。

你可以直接让 Codex 参考这个 skill 路径，例如：

```text
用 /home/li/codex/FriendDistill/create-friend 这个 skill，帮我蒸馏一个朋友
```

或者：

```text
参考 create-friend 这个 skill，基于我接下来给你的聊天记录生成朋友档案
```

这种方式适合：
- 先试用
- 一次性生成
- 边调边改 skill

---

## 方式二：安装到 `~/.codex/skills`（推荐）

如果你希望以后在任何项目里都能直接调用，建议安装到 Codex 的技能目录。

### 安装命令

```bash
mkdir -p ~/.codex/skills
cp -R /home/li/codex/FriendDistill/create-friend ~/.codex/skills/create-friend
```

安装后，你就可以在之后的会话里直接提到：

```text
帮我用 create-friend 蒸馏一个朋友
```

或者更明确一点：

```text
Use $create-friend to distill my friend from chat logs and notes.
```

> 如果当前会话已经启动，安装后有时需要新开一个会话，Codex 才会重新发现新 skill。

---

## 怎么实际使用

## 第 1 步：准备材料

你可以提供任意组合：

- 聊天记录导出
- 截图
- 语音转文字
- 日记 / 笔记
- 社交媒体发言
- 你对 TA 的一句话描述
- 你们之间的共同回忆

建议优先级：

1. **真实聊天记录**
2. **TA 主动写的长文本 / 动态 / 笔记**
3. **你补充的主观印象**

---

## 第 2 步：先让 skill 建档

这个仓库自带一个脚本，用来初始化朋友档案目录。

### 示例

```bash
cd /home/li/codex/FriendDistill/create-friend
python3 scripts/friend_writer.py init --base-dir ./friends --name "阿哲"
```

执行后会生成：

```text
./friends/阿哲/
├── meta.json
├── persona.md
├── memory.md
├── relationship.md
└── SKILL.md
```

如果你想查看当前已经建过哪些朋友档案：

```bash
python3 scripts/friend_writer.py list --base-dir ./friends
```

---

## 第 3 步：把材料交给 Codex 进行蒸馏

你可以直接这样说：

```text
请参考 /home/li/codex/FriendDistill/create-friend 这个 skill。
我会给你一个朋友的聊天记录和一些描述，请帮我生成：
1. persona.md
2. memory.md
3. relationship.md
4. 最终可调用的 SKILL.md
```

也可以更口语一点：

```text
帮我蒸馏一个朋友。
她是我大学同学，平时嘴挺毒但其实很照顾人。
我接下来会给你聊天记录和截图。
```

skill 的典型 intake 是这 3 个问题：

1. 朋友的昵称 / 代号
2. 你和 TA 的关系（一句话）
3. 你的第一印象（一句话）

例如：

```text
昵称：阿哲
关系：大学室友，现在偶尔一起打游戏
第一印象：嘴硬心软，深夜话很多，白天像失踪
```

---

## 第 4 步：持续更新

当你后面又拿到了新材料，可以继续追加，而不是推倒重来。

例如你可以说：

```text
我有这个朋友的新聊天记录，帮我增量更新之前的档案
```

或者：

```text
这段写得不像他，他不会这么说。请按我下面的修正更新 persona 和 relationship
```

在更新前，建议先做版本备份：

```bash
python3 scripts/version_manager.py backup --profile-dir ./friends/阿哲
```

查看历史版本：

```bash
python3 scripts/version_manager.py list --profile-dir ./friends/阿哲
```

恢复某个版本：

```bash
python3 scripts/version_manager.py restore --profile-dir ./friends/阿哲 --version 20260405T063658Z
```

---

## 推荐的提问方式

为了让结果更像真人，建议你在请求里明确目标。

### 1. 只想建档

```text
帮我把这个朋友蒸馏成一个长期可维护的 friend skill。
重点保留她的语气、习惯、我们之间的互动方式，以及她不喜欢什么。
不要胡编她没说过的经历。
```

### 2. 想让 AI 像 TA 一样陪你聊天

```text
帮我生成一个朋友 skill，重点是闲聊风格、安慰人的方式、吐槽风格和共同记忆。
```

### 3. 想做“高拟真但不乱编”

```text
请严格区分：
- 明确事实
- 高概率推断
- 低置信度推断
- 不知道的部分
不知道就明确说不知道。
```

### 4. 想修正 drift

```text
这部分太油腻了，不像她。
她其实更冷一点，嘴更损，但不会真的伤人。
请据此修正 persona 和 relationship。
```

---

## 输出质量怎么判断

一个好的朋友 skill，应该满足：

- **不像通用 AI 助手**，而像一个具体的人
- **能复现说话方式**，但不过度 caricature
- **知道哪些东西不知道**，不会乱编回忆
- **对你们的关系有感知**，不是单纯的人物设定
- **可以增量迭代**，不会每次更新都漂移

建议至少做 3 轮测试：

1. **闲聊测试**：让 TA 回一句日常话题
2. **安慰测试**：让 TA 回一句你情绪低落时的话
3. **回忆测试**：问一个你们共同经历的问题

如果结果太 generic，就应该回去补：
- 原始聊天风格
- 更具体的 shared memories
- 你们之间的互动模式

---

## 注意事项

- 这个 skill 的目标是“蒸馏”，不是“虚构角色创作”
- 如果材料不足，应该保守，不应该硬补设定
- 对已故、失联、前任、敏感关系，建议使用更温和的表达，并明确哪些内容只是近似还原
- 不建议无授权蒸馏特别私密的隐私内容

---

## 一套最小可运行示例

### 1）初始化

```bash
cd /home/li/codex/FriendDistill/create-friend
python3 scripts/friend_writer.py init --base-dir ./friends --name "阿哲"
```

### 2）在 Codex 里说

```text
请参考 /home/li/codex/FriendDistill/create-friend 这个 skill。
帮我蒸馏一个朋友，名字叫阿哲。
我和他是大学室友，现在偶尔一起打游戏。
我的第一印象是：嘴硬心软，深夜话很多，白天像失踪。
接下来我会继续给你聊天记录和共同经历。
请最后输出 persona.md、memory.md、relationship.md 和可调用的 SKILL.md。
```

### 3）后续修正

```text
这段不像他，他不会这么温柔。
他其实更像是会先损你两句，再认真给建议。
请更新 relationship 和 persona。
```

---

## 当前仓库路径

当前版本位于：

```text
/home/li/codex/FriendDistill/create-friend
```

如果你愿意，我下一步还可以继续帮你：

1. 直接拿一个朋友案例，帮你现场生成第一版档案
2. 再补一个中文示例目录 `friends/example_朋友名/`
3. 把这个 skill 再改成更像 `同事.skill` 的“命令式交互版”
