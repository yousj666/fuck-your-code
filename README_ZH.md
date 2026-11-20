# Fuck Your Code

骂的不是你，是你的代码。拿你自己的代码来测测，看它到底有多烂。

一个自带幽默感的命令行屎山代码检测工具。给它一个文件、一整个项目
文件夹，或者直接粘贴一段代码进来，它就能给这堆东西打分：每个文件
一个**屎气指数**（0–100，越高越屎），再汇总出一个**综合质量分**
（0–100，越高越好），最后附赠一句可以拿去代码评审会上念的判决。

玩笑归玩笑，底下是真测量：复杂度、嵌套深度、函数长度、体量、结构、
重复粘贴、异常处理、硬编码秘密、危险函数、死代码、全局状态、参数
泛滥、依赖导入、注释文档、注释掉的代码、技术债标注、命名品味、魔法
数字、格式卫生、调试残留，共二十项检查，支持 20 多种语言（Python、
JavaScript/TypeScript、Go、Java、C/C++、Rust、C#、PHP、Ruby、
Swift、Kotlin、Shell、Lua、Perl、Scala……）。

**全程离线。**不联网、不上传、无遥测——你的耻辱只留在你自己的机器上。
纯 Python 3 标准库，零第三方依赖。

## 安装

只需要 Python 3.8+，别的什么都不用装。

```bash
unzip fuck-your-code-zh.zip   # 或英文版 -en
cd fuck-your-code
./fuck-your-code --help       # Windows 用 fuck-your-code.bat
```

中文版默认输出中文，英文版（`fuck-your-code-en.zip`）默认输出英文；
运行时都可以用 `--lang en|zh` 切换。默认语言来自启动器旁边的
`edition.json`：`{"default_lang": "zh"}`。

## 用法

```bash
# 单个文件（把文件拖进终端也行）
./fuck-your-code analyze app.py
./fuck-your-code app.py

# 整个目录，或一次多个路径
./fuck-your-code analyze src/ legacy/ tools/

# 直接粘贴代码（Ctrl-D 结束；--ext 提示语言）
./fuck-your-code paste --ext js
cat snippet.py | ./fuck-your-code paste --ext py

# 或者把代码片段直接写在命令行里
./fuck-your-code --code "def f(x): return x+1" --ext py
```

## 参数

| 参数 | 说明 |
|---|---|
| `--lang en\|zh` | 报告语言（默认读 `edition.json`） |
| `--format console\|markdown\|json` | 输出格式 |
| `--output <file>` | 把报告写进文件，而不是打印到终端 |
| `--top <n>` | 耻辱榜列几个最屎的文件（默认 10） |
| `--exclude <glob>` | 额外排除规则（可重复写多次） |

默认排除：`.git`、`node_modules`、`__pycache__`、`dist`、`build`、
`vendor`、`*.min.js`，二进制文件永远跳过。

## 打分方式

每个文件先算二十项「屎度」子分（0–100），再按权重混合——复杂度 11%、
重复 9%、异常处理 7%、嵌套 6%、硬编码秘密 6%、危险函数 6%、函数长度
5%、命名 5%、魔法数字 5%、死代码 5%、体量 4%、结构 4%、文档 4%、全局
状态 4%、导入 4%、技术债 3%、注释掉的代码 3%、参数 3%、格式 3%、调试
残留 3%——得到该文件的屎气指数。项目质量分 = 100 − 按行数加权的屎气
指数，并对应五档判决，从「干净得不像亲生的」一路到「建议直接火化」。

骂完之后，每份报告最后还有一节**正经建议**：根据本次检测的真实结果
生成的专业整改意见——哪个维度扣分、在哪个文件、具体该怎么改。

顺带说一句，这工具给自己打分是 100.0。而且不是改分改出来的，是
照着它自己的意见一条一条改出来的，过程见 `SELF_FIX_LOG.md`。

拿自带示例试试：

```bash
./fuck-your-code analyze examples/good.py           # 干净的那个
./fuck-your-code analyze examples/shit_mountain.py  # 案发现场
./fuck-your-code analyze examples/ --lang en        # 换英文再看一遍
```

## 测试

```bash
python3 tests/run_tests.py
```

## 许可证

MIT，© Yousj。见 `LICENSE`。
