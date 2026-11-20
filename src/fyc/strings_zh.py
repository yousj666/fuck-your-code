"""fuck-your-code 的中文字符串表。

工具能用中文打印的每一句标签、检查名、判决、吐槽和正经
建议都收在这张表里，和英文版一一对应。把文案单独放进
数据模块，检查代码就不用把逻辑和文字搅在一起，翻译也
只需要盯着这一个文件看。
"""

STRINGS_ZH = {
    # 报告标签和表头
    "app_tagline": "fuck-your-code -- 来测测你的代码到底有多屎山",
    "report_title": "屎山代码检测报告",
    "overall_quality": "综合质量分",
    "shit_index": "屎气指数",
    "verdict": "判决",
    "files_analyzed": "已分析文件",
    "total_lines": "总行数",
    "check_breakdown": "分项体检（条越长越屎）",
    "worst_files": "耻辱榜 -- 最屎的文件",
    "top_issues": "重罪清单",
    "recommendations_title": "正经建议",
    "no_files": "没找到能分析的文件。你是不是指了个寂寞？",
    "col_file": "文件",
    "col_score": "屎气",
    "col_quality": "质量",
    "col_lines": "行数",
    "col_lang": "语言",
    "clean_bill": "居然没挑出什么毛病。干净得有点可疑。",
    "paste_label": "（粘贴的代码）",
    "stdin_hint": "正在从标准输入读代码……粘贴完按 Ctrl-D 结束（Windows 用 Ctrl-Z 回车）。",

    # 二十项检查的名字
    "checks": {
        "complexity": "复杂度",
        "nesting": "嵌套深度",
        "funclen": "函数长度",
        "size": "体量臃肿",
        "structure": "结构混乱",
        "duplication": "重复粘贴",
        "errors": "异常处理",
        "secrets": "硬编码秘密",
        "dangerous": "危险函数",
        "deadcode": "死代码",
        "globals": "全局状态",
        "params": "参数泛滥",
        "imports": "依赖导入",
        "docs": "注释文档",
        "commented": "注释掉的代码",
        "techdebt": "技术债标注",
        "naming": "命名品味",
        "magic": "魔法数字",
        "formatting": "格式卫生",
        "debug": "调试残留与占位",
    },

    # 五档判决：门槛、名号、判词
    "tiers": [
        (90, "干净得不像亲生的",
         "我喷子都举起来了，愣是没找到下嘴的地方。这代码干净得能当无菌车间参观。"),
        (75, "能见人，挺体面",
         "有点小瑕疵，但瑕不掩瑜，穿上外套就能出门见客户。"),
        (55, "半瓶水晃荡",
         "能跑是能跑，就是跑起来浑身叮当响。属于那种你不敢动、动了就响的代码。"),
        (35, "屎山景区开放了",
         "游客已经开始打卡了。山里有个函数，全靠意念和分号撑着没塌。"),
        (0, "建议直接火化",
         "这已经不是屎山了，这是屎界的珠穆朗玛。删了吧，就当无事发生，连夜买站票跑路。"),
    ],

    # 每项检查能查出的罪状文案
    "issue_complex_function": "函数 {name} 的圈复杂度约 {n}，一本选择结局的冒险小说",
    "issue_nesting": "嵌套挖到了 {n} 层深，进山请系安全绳、戴头灯、写遗书",
    "issue_deep_lines": "{pct}% 的行埋在四层以上的嵌套里",
    "issue_long_function": "函数 {name} 一口气写了 {n} 行不换气（第 {line} 行）",
    "issue_many_long_functions": "{n} 个函数超过五十行，一场马拉松聚会",
    "issue_god_file": "上帝文件：{n} 行一个人干完整个公司的活",
    "issue_big_file": "文件有 {n} 行，不违法，就是看着累",
    "issue_too_many_funcs": "一个文件塞了 {n} 个函数，这是人群，不是模块",
    "issue_bare_except": "光秃秃的裸 except，什么异常都往肚子里吞，第 {line} 行",
    "issue_except_pass": "except 后面直接 pass，错误进去了，寂静出来了，第 {line} 行",
    "issue_empty_catch": "空 catch 块：错误被看了一眼，然后被无视，第 {line} 行",
    "issue_no_comments": "基本零注释，未来的你翻到这里，会有很多问号",
    "issue_too_many_comments": "注释多到喧宾夺主（占全文件 {pct}%）",
    "issue_single_letter": "单字母变量满天飞（共 {n} 个），这是写代码，不是做代数题",
    "issue_meaningless": "tmp、data1 这类没灵魂的名字在干正经活（共 {n} 个）",
    "issue_mixed_case": "snake_case 和 camelCase 在同一个文件里打架（{a} 对 {b}）",
    "issue_dup_lines": "{pct}% 的行是复制粘贴的复读机",
    "issue_dup_blocks": "{n} 处重复的五行代码块，复制、粘贴、丢人",
    "issue_todo": "给后人埋了 {n} 颗债务标记地雷，谁踩谁知道",
    "issue_commented_code": "{n} 行代码停在注释里，不活不死，专职闹鬼",
    "issue_magic_numbers": "{n} 个魔法数字在逻辑里裸奔，连个名字都没有",
    "issue_secret_assignment": "长得像秘密的字面量直接写给了 {name}，第 {line} 行，秘密不该住在源码里",
    "issue_credential_url": "网址里直接嵌了账号密码，第 {line} 行",
    "issue_hardcoded_ip": "代码里硬编码了 IP 地址（共 {n} 处）",
    "issue_unused_imports": "{n} 个导入从没被用过：{names}",
    "issue_dead_functions": "{n} 个函数定义了却没人调用：{names}",
    "issue_unreachable": "{n} 条语句排在 return 或 raise 后面，永远执行不到",
    "issue_globals": "{n} 处模块级可变状态，谁都能改，谁都不敢信",
    "issue_global_keyword": "{n} 处 global 语句，隔空改状态，阴森得很",
    "issue_mutable_default": "函数 {name} 用了可变默认参数，它记得每一次调用",
    "issue_too_many_params": "函数 {name} 有 {n} 个参数，这是家庭聚会，不是函数",
    "issue_star_args": "{n} 个函数躲在可变参数大口袋后面",
    "issue_import_chaos": "文件头 {n} 个导入，依赖跳蚤市场开张了",
    "issue_star_import": "第 {line} 行有星号导入，现在谁也不知道这里住了哪些名字",
    "issue_midfile_imports": "{n} 个导入躲在文件中间",
    "issue_long_lines": "{n} 行超过长度上限，横向滚动不是功能，是惩罚",
    "issue_trailing_ws": "{n} 行尾巴上拖着空白",
    "issue_mixed_indent": "制表符和空格混着用，选一边站吧",
    "issue_dangerous_call": "危险调用：{kind}，第 {line} 行",
    "issue_debug_statements": "{n} 条调试打印或日志没撤干净，还留在现场",
    "issue_empty_function": "函数 {name} 是个空壳（第 {line} 行）",

    # 正经建议，每项检查一条，写给最差的那个文件
    "advice_complexity": (
        "{file}：把最复杂的函数拆成职责单一的小函数，嵌套分支改用提前返回。"
        "每个函数的圈复杂度尽量压到十以内。"),
    "advice_nesting": (
        "{file}：用守卫语句和提前返回把深嵌套拍平，内层代码块抽成有名字的"
        "函数。嵌套层数尽量不超过三到四层。"),
    "advice_funclen": (
        "{file}：把超过约五十行的函数拆成解析、校验、计算、渲染这样有名字"
        "的步骤。一个函数只做一件事。"),
    "advice_size": (
        "{file}：这个文件干的活太多了。把内聚的一组函数搬进以职责命名的"
        "新模块里，各管一摊。"),
    "advice_structure": (
        "{file}：一个文件里函数太多。按职责拆分模块，对外只留一小圈清晰的"
        "公开接口。"),
    "advice_duplication": (
        "{file}：把重复的代码块抽成一个共享函数，各处都去调它，这样同一份"
        "逻辑永远只需要改一个地方。"),
    "advice_errors": (
        "{file}：抓具体的异常类型，不要用裸捕获；记录带上下文的日志，绝不"
        "用空块把失败吞掉。"),
    "advice_docs": (
        "{file}：给模块补一句总览说明，给公开函数各补一行讲意图的文档，"
        "讲为什么，不讲怎么做的。"),
    "advice_naming": (
        "{file}：把单字母和占位用的变量名换成有意义的词，并在一个文件里"
        "固定用一种命名风格，不要混着来。"),
    "advice_techdebt": (
        "{file}：把每条债务标记转成有负责人的正式事项，然后删掉标记。"
        "陈年标记就是把已知问题养成事故的温床。"),
    "advice_commented": (
        "{file}：删掉注释掉的代码，版本控制本来就替你记着。真要留，就用"
        "文字说明理由，并给它一个过期日期。"),
    "advice_magic": (
        "{file}：给每个来历不明的数字起个名字，做成命名常量，这样数值既"
        "有了含义，也只有一个地方能改。"),
    "advice_secrets": (
        "{file}：把秘密挪出源码，放进环境变量或专门的密钥管理工具；已经"
        "提交过的凭据要立刻轮换。"),
    "advice_deadcode": (
        "{file}：删掉没人用的导入和没人调用的函数。死代码照样要被人读、"
        "被评审、被维护，让代码库说的每句话都是真心的。"),
    "advice_globals": (
        "{file}：用参数、返回值或一个显式的小状态对象替代模块级可变状态，"
        "并避开可变默认参数。"),
    "advice_params": (
        "{file}：参数太多的函数通常想要一个配置对象或数据类。把相关的参数"
        "收成一组，并给这组起个名字。"),
    "advice_imports": (
        "{file}：删掉星号导入，让所有导入都待在文件顶部，并清掉这个模块"
        "根本没用到的依赖。"),
    "advice_formatting": (
        "{file}：跑一遍格式化工具，把行长压到约定上限以内，清掉行尾空白，"
        "一个文件只用一种缩进风格。"),
    "advice_dangerous": (
        "{file}：用结构化接口替代动态求值和字符串拼命令，数据库查询一律"
        "参数化，绝不要反序列化不可信的数据。"),
    "advice_debug": (
        "{file}：清掉残留的调试输出和空壳占位函数。真值得留的信息，交给"
        "带级别的日志模块。"),
}
