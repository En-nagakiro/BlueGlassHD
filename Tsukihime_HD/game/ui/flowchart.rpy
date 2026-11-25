## ==============================================================================
## ui/flowchart.rpy - 100% Truth-Verified Tsukihime 5-Route Flowchart & Jump
## Every label, branch_label, thumbnail, and preset state verified against 0.txt
## ==============================================================================

init -2 python:
    FLOWCHART_CATEGORIES = [
        ("all", "全部物语"),
        ("common", "序章与共通"),
        ("arc", "爱尔奎特线"),
        ("ciel", "希耶尔线"),
        ("akiha", "秋叶线"),
        ("hisui", "翡翠线"),
        ("kohaku", "琥珀线"),
        ("extra", "知得留与月蚀"),
    ]

    # Verified canonical nodes: branch_label is the exact `fXX` label for jump-and-continue!
    FLOWCHART_NODES = [
        # --- 序章与共通 (COMMON & PROLOGUE) ---
        {
            "id": "com_00", "cat": "common", "day": "序章 · 割草之夏",
            "title": "伤痕、直死与魔术之镜", "sub": "PROLOGUE · THE BLUE GLASSES",
            "seen_label": "s20", "branch_label": "f20", "mode": "continue",
            "thumb": "images/bg/cmo_01.webp", "cast": "远野志贵、苍崎青子",
            "desc": "八年前的事故后，少年看到了布满世界的黑线。在夏末的城郊草原上，红发魔术使苍崎青子赐予了封印魔眼的眼镜与活下去的约定。",
            "branch_info": "全作起点 · 之后进入第一日晨曦分歧（教室 / 中庭）。",
            "preset": {},
        },
        {
            "id": "com_01", "cat": "common", "day": "DAY 01 · 教室",
            "title": "翻转的日常与挚友有彦", "sub": "DAY 01 · CLASSROOM MORNING",
            "seen_label": "s21", "branch_label": "f21", "mode": "continue",
            "thumb": "images/bg/bg_06a.webp", "cast": "远野志贵、乾有彦",
            "desc": "清晨早早来到教室与死党乾有彦闲谈。寄宿在有间家八年的志贵，即将收到返回远野本家的通知。",
            "branch_info": "偏秋叶分支入口 · 午休可决定食堂或走廊行动。",
            "preset": {},
        },
        {
            "id": "com_02", "cat": "common", "day": "DAY 01 · 中庭",
            "title": "中庭邂逅 · 希耶尔学姐", "sub": "DAY 01 · COURTYARD ENCOUNTER",
            "seen_label": "s22", "branch_label": "f22", "mode": "continue",
            "thumb": "images/cg/cel_e01.webp", "cast": "远野志贵、希耶尔",
            "desc": "循着敲打声走进林荫道中庭，遇见正蹲在地上用铁锤修理花架的三年级学姐希耶尔。",
            "branch_info": "希耶尔好感关键起点 · 开启后续茶道室路线交集。",
            "preset": {},
        },
        {
            "id": "com_03", "cat": "common", "day": "DAY 01 · 归途",
            "title": "夕阳十字路与弓塚五月", "sub": "DAY 01 · SUNSET INTERSECTION",
            "seen_label": "s35", "branch_label": "f35", "mode": "continue",
            "thumb": "images/bg/bg_01b.webp", "cast": "远野志贵、弓塚五月",
            "desc": "放学走出校门，在斜阳笼罩的十字路口偶遇同班同学弓塚五月，开启前往远野宅邸的归途。",
            "branch_info": "提升五月伏笔（flg6）并衔接到远野本家正门。",
            "preset": {},
        },
        {
            "id": "com_04", "cat": "common", "day": "DAY 01 · 远野宅邸",
            "title": "坡道洋馆与阔别八年的重逢", "sub": "DAY 01 · TOHNO MANSION",
            "seen_label": "s41", "branch_label": "f41", "mode": "continue",
            "thumb": "images/bg/bg_32b.webp", "cast": "远野志贵、翡翠、琥珀、远野秋叶",
            "desc": "登上坡道来到宏伟森严的远野宅邸，重逢当家妹妹秋叶与双子侍女翡翠、琥珀。",
            "branch_info": "远野本家篇开端 · 晚饭后决定夜间行动与表里线分水岭。",
            "preset": {"flg6": 1},
        },
        {
            "id": "com_05", "cat": "common", "day": "DAY 01 · 深夜分水岭",
            "title": "表线与里线的命运十字路", "sub": "DAY 01 · NEAR / FAR SIDE GATE",
            "seen_label": "s46", "branch_label": "f46", "mode": "continue",
            "thumb": "images/bg/bg_40d.webp", "cast": "远野志贵",
            "desc": "宅邸的第一夜，窗外传来异样的犬吠与骚动。是否推门出去确认情形，将把命运彻底劈开为「表线」与「里线」。",
            "branch_info": "核心分水岭 ·【去看看情形】进表线（爱尔奎特/希耶尔），【老实睡觉】进里线（表线通关后开放）。",
            "preset": {"flg6": 1},
        },
        {
            "id": "com_06", "cat": "common", "day": "DAY 02 · 表线序幕",
            "title": "直死魔眼之梦与白昼冲动", "sub": "DAY 02 · EYES OF DEATH PERCEPTION",
            "seen_label": "s51", "branch_label": "f51", "mode": "continue",
            "thumb": "images/bg/bg_22b.webp", "cast": "远野志贵、爱尔奎特",
            "desc": "梦中回想起青子老师关于「线」的教诲。表线第二日的学园日常背后，决定命运的邂逅正悄然逼近。",
            "branch_info": "表线第二日入口 · 通往第五节课后的商业街十七分割。",
            "preset": {"ark_regard": 3, "flg6": 1},
        },
        {
            "id": "com_07", "cat": "common", "day": "DAY 02 · 十七分割",
            "title": "阳台的乌鸦与致命杀意", "sub": "DAY 02 · SEVENTEEN PIECES",
            "seen_label": "s65", "branch_label": "f65", "mode": "continue",
            "thumb": "images/cg/ark_e01.webp", "cast": "远野志贵、爱尔奎特",
            "desc": "第五节古文课的窗外落下一只乌鸦。早退步入商业街的志贵，在金发白衣少女擦肩的瞬间被不可遏制的杀意彻底吞噬。",
            "branch_info": "《月姬》表线最震撼的核心引爆点。",
            "preset": {"ark_regard": 3, "flg6": 1},
        },

        # --- 表线 · 爱尔奎特线 (ARCUEID ROUTE) ---
        {
            "id": "arc_01", "cat": "arc", "day": "DAY 03 · 爱尔奎特线",
            "title": "雨过天晴与不死的真祖", "sub": "DAY 03 · RESURRECTION",
            "seen_label": "s69", "branch_label": "f69", "mode": "continue",
            "thumb": "images/bg/bg_20a.webp", "cast": "远野志贵、爱尔奎特",
            "desc": "从血腥噩梦般的昏沉中醒来，雨已停歇。在通往街区的道路上，本已被十七分割的少女正含笑迎面走来。",
            "branch_info": "爱尔奎特线第三日主干 · 真祖问责与护卫同盟开端。",
            "preset": {"ark_regard": 4, "flg6": 1},
        },
        {
            "id": "arc_02", "cat": "arc", "day": "DAY 03 · 血之誓约",
            "title": "酒店护卫与尼禄的阴影", "sub": "DAY 03 · GUARDIAN PACT",
            "seen_label": "s81", "branch_label": "f81", "mode": "continue",
            "thumb": "images/bg/bg_19b.webp", "cast": "远野志贵、爱尔奎特",
            "desc": "既已许下约定便不能反悔。志贵守候在苍白沉睡的爱尔奎特身旁，而二十七祖尼禄·卡欧斯的黑兽已在夜幕中包围酒店。",
            "branch_info": "表线决战前夕 · 切勿在后续选择回家逃避。",
            "preset": {"ark_regard": 5, "flg6": 1},
        },
        {
            "id": "arc_03", "cat": "arc", "day": "DAY 03 · 死斗",
            "title": "贯彻信念 · 直面混沌之兽", "sub": "DAY 03 · AGAINST CHAOS",
            "seen_label": "s87", "branch_label": "f87", "mode": "continue",
            "thumb": "images/cg/nero_e04.webp", "cast": "远野志贵、爱尔奎特、尼禄·卡欧斯",
            "desc": "回想起老师的话语，志贵抛开迷惘决定留在爱尔奎特身边，向拥有六百六十六只魔兽的死徒尼禄·卡欧斯发起殊死反击。",
            "branch_info": "尼禄·卡欧斯决战核心段。",
            "preset": {"ark_regard": 6, "flg6": 1},
        },
        {
            "id": "arc_04", "cat": "arc", "day": "DAY 04 · 同行",
            "title": "无吸血鬼气息的公寓与重聚", "sub": "DAY 04 · THE WHITE ROOM",
            "seen_label": "s94", "branch_label": "f94", "mode": "continue",
            "thumb": "images/bg/bg_28b.webp", "cast": "远野志贵、爱尔奎特",
            "desc": "清晨在爱尔奎特的酒店房间醒来，两人开始正式联手追查潜伏在三咲町的「蛇」——转生无限者罗阿。",
            "branch_info": "第四日章节入口 · 决定进入爱尔奎特线还是希耶尔线的前置节点。",
            "preset": {"ark_regard": 7, "flg6": 1},
        },
        {
            "id": "arc_05", "cat": "arc", "day": "DAY 05 · 约会前奏",
            "title": "晨光苏醒与城中搜查", "sub": "DAY 05 · MORNING LIGHT",
            "seen_label": "s108", "branch_label": "f108", "mode": "continue",
            "thumb": "images/bg/bg_33d.webp", "cast": "远野志贵、爱尔奎特",
            "desc": "在远野家感受着清晨阳光醒来。围绕爱尔奎特的秘密与罗阿的线索逐渐明朗。",
            "branch_info": "爱尔奎特线第五日主干。",
            "preset": {"ark_regard": 8, "flg6": 1},
        },
        {
            "id": "arc_06", "cat": "arc", "day": "DAY 07 · 回忆之庭",
            "title": "旧日的游乐场与吸血冲动", "sub": "DAY 07 · FORGOTTEN GARDEN",
            "seen_label": "s143", "branch_label": "f143", "mode": "continue",
            "thumb": "images/bg/bg_47.webp", "cast": "远野志贵、爱尔奎特",
            "desc": "梦境掠过幼年宽广的宅邸与庭院。醒来后的第七日，爱尔奎特被压抑的吸血冲动与两人日益深厚的情愫正面碰撞。",
            "branch_info": "爱尔奎特线第七日核心篇章。",
            "preset": {"ark_regard": 10, "flg6": 1},
        },
        {
            "id": "arc_07", "cat": "arc", "day": "DAY 09 · 纯白之伤",
            "title": "鸟鸣清晨与宿命倒计时", "sub": "DAY 09 · EVE OF FATE",
            "seen_label": "s162", "branch_label": "f162", "mode": "continue",
            "thumb": "images/cg/ark_e04.webp", "cast": "远野志贵、爱尔奎特",
            "desc": "清风与鸟鸣穿过敞开的窗户。罗阿的真身与爱尔奎特隐瞒的真相即将揭晓。",
            "branch_info": "通向校舍决战与最终夜的关键分支。",
            "preset": {"ark_regard": 12, "flg6": 1},
        },
        {
            "id": "arc_08", "cat": "arc", "day": "DAY 11 · 最终夜",
            "title": "冲向宿敌 · 千年宿怨的终结", "sub": "DAY 11 · FINAL CONFRONTATION",
            "seen_label": "s194", "branch_label": "f194", "mode": "continue",
            "thumb": "images/bg/cmo_14.webp", "cast": "远野志贵、爱尔奎特、希耶尔、罗阿",
            "desc": "被翡翠唤醒后的最终之日。所有的因果与死线都汇聚于月夜校舍。",
            "branch_info": "爱尔奎特线最终高潮，直通结局分歧。",
            "preset": {"ark_regard": 14, "flg6": 1},
        },
        {
            "id": "arc_09", "cat": "arc", "day": "EPILOGUE · TRUE END",
            "title": "爱尔奎特 TRUE END · 月姬", "sub": "ARCUEID TRUE · MOON PRINCESS",
            "seen_label": "s52a", "branch_label": "f52", "mode": "continue",
            "thumb": "images/cg/ark_e10.webp", "cast": "远野志贵、爱尔奎特",
            "desc": "罗阿伏诛，深秋步入尾声。在燃烧般的黄昏教室里，少年静静履行承诺，仰望那轮永不褪色的苍蓝明月直到天明。",
            "branch_info": "爱尔奎特正史真结局（连播 s52 前奏 + s52a 终章 + ED 演职员表）。",
            "preset": {"ark_regard": 15},
        },
        {
            "id": "arc_10", "cat": "arc", "day": "EPILOGUE · GOOD END",
            "title": "爱尔奎特 GOOD END · 白昼之月", "sub": "ARCUEID GOOD · DAWN MOON",
            "seen_label": "s53a", "branch_label": "f53", "mode": "continue",
            "thumb": "images/cg/ark_e02.webp", "cast": "远野志贵、爱尔奎特",
            "desc": "无法忘记那个金发少女的约定。在澄澈无云的苍空下，跨越了永眠宿命的两人再度牵起双手，迈向未知的新天地。",
            "branch_info": "爱尔奎特二周目好结局（连播 s53 前奏 + s53a 终章 + ED）。",
            "preset": {"ark_regard": 15},
        },

        # --- 表线 · 希耶尔线 (CIEL ROUTE) ---
        {
            "id": "ciel_01", "cat": "ciel", "day": "DAY 05 · 希耶尔线",
            "title": "晨光分化 · 代行者的暗面", "sub": "DAY 05 · EXECUTOR OF THE CHURCH",
            "seen_label": "s200", "branch_label": "f200", "mode": "continue",
            "thumb": "images/cg/cel_e02a.webp", "cast": "远野志贵、希耶尔",
            "desc": "正式踏入希耶尔个人线。温和亲切的三年级学姐背后，埋藏着圣堂教会埋葬机关代行者的沉重身份。",
            "branch_info": "希耶尔线第五日正式入口（含 flgE 路线旗标）。",
            "preset": {"ciel_regard": 7, "flgE": 1, "flg6": 1},
        },
        {
            "id": "ciel_02", "cat": "ciel", "day": "DAY 07 · 灼热之雨",
            "title": "爱与罪责 · 学姐的告白", "sub": "DAY 07 · SCORCHING RAIN",
            "seen_label": "s260", "branch_label": "f260", "mode": "continue",
            "thumb": "images/cg/cel_e03a.webp", "cast": "远野志贵、希耶尔、爱尔奎特",
            "desc": "灼热的雨中梦境与纷乱的情感。希耶尔与爱尔奎特的对立逐渐浮出水面，志贵直面学姐深藏心底的罪业。",
            "branch_info": "希耶尔线第七日主线入口。",
            "preset": {"ciel_regard": 9, "flgE": 1, "flg6": 1},
        },
        {
            "id": "ciel_03", "cat": "ciel", "day": "DAY 09 · 阴暗八年",
            "title": "罗阿的残响与第七圣典", "sub": "DAY 09 · EIGHT YEARS IN SHADOW",
            "seen_label": "s273", "branch_label": "f273", "mode": "continue",
            "thumb": "images/cg/cel_e05a.webp", "cast": "远野志贵、希耶尔",
            "desc": "潜藏在黑暗角落八年的罗阿宿魂开始侵蚀志贵。希耶尔举起第七圣典，踏上赎罪与斩断轮回的战场。",
            "branch_info": "希耶尔线第九日高潮开篇。",
            "preset": {"ciel_regard": 11, "flgE": 1, "flg6": 1},
        },
        {
            "id": "ciel_04", "cat": "ciel", "day": "DAY 10 · 惊醒",
            "title": "被侵蚀的理智与最后的抉择", "sub": "DAY 10 · EROSION OF SANITY",
            "seen_label": "s284", "branch_label": "f284", "mode": "continue",
            "thumb": "images/cg/cel_e07a.webp", "cast": "远野志贵、希耶尔、爱尔奎特",
            "desc": "如弹簧人偶般从梦魇中惊醒，体内的罗阿人格日益狂暴。校园与夜街之上，三人的宿命走向终局对撞。",
            "branch_info": "希耶尔线第十日，直通最终日决战。",
            "preset": {"ciel_regard": 12, "flgE": 1, "flg6": 1},
        },
        {
            "id": "ciel_05", "cat": "ciel", "day": "DAY 12 · 黎明前夕",
            "title": "空荡的房间与最终审判", "sub": "DAY 12 · FINAL JUDGMENT",
            "seen_label": "s307", "branch_label": "f307", "mode": "continue",
            "thumb": "images/cg/cel_e08.webp", "cast": "远野志贵、希耶尔、爱尔奎特",
            "desc": "希耶尔不辞而别，房间骤然空荡。为了终结一切悲剧，志贵追向等待着最终审判的战地。",
            "branch_info": "希耶尔线最终日入口，根据好感与选择进入 TRUE / GOOD 双结局。",
            "preset": {"ciel_regard": 14, "flgE": 1, "flg6": 1},
        },
        {
            "id": "ciel_06", "cat": "ciel", "day": "EPILOGUE · TRUE END",
            "title": "希耶尔 TRUE END · 日光", "sub": "CIEL TRUE · SUNLIGHT",
            "seen_label": "s310", "branch_label": "f310", "mode": "continue",
            "thumb": "images/cg/cel_e09.webp", "cast": "远野志贵、希耶尔",
            "desc": "斩断诅咒与不死的轮回，不再被黑夜与罪恶束缚。沐浴在久违的温暖日光下，两人迎来了真正属于彼此的明天。",
            "branch_info": "希耶尔线真结局（含完整终章与 ED）。",
            "preset": {"ciel_regard": 15, "flgE": 1},
        },
        {
            "id": "ciel_07", "cat": "ciel", "day": "EPILOGUE · GOOD END",
            "title": "希耶尔 GOOD END · 白昼之梦", "sub": "CIEL GOOD · DAYDREAM",
            "seen_label": "s308", "branch_label": "f308", "mode": "continue",
            "thumb": "images/cg/cel_f02.webp", "cast": "远野志贵、希耶尔、爱尔奎特",
            "desc": "谁都不愿放手的奇迹结局。学姐与吸血姬围绕着志贵展开喧闹又温馨的奇妙日常，往复不止。",
            "branch_info": "希耶尔线经典后宫喜剧好结局（含完整终章与 ED）。",
            "preset": {"ciel_regard": 15, "flgE": 1},
        },

        # --- 里线 · 秋叶线 (AKIHA ROUTE) ---
        {
            "id": "aki_01", "cat": "akiha", "day": "DAY 01 · 里线入口",
            "title": "未曾踏出的夜晚 · 远野家深渊", "sub": "FAR SIDE · SLEEPLESS NIGHT",
            "seen_label": "s48", "branch_label": "f48", "mode": "continue",
            "thumb": "images/bg/bg_40d.webp", "cast": "远野志贵、远野秋叶",
            "desc": "选择留在床上无视窗外犬吠，没有遇见真祖的志贵，由此踏入远野宅邸尘封八年的禁忌与血脉暗面。",
            "branch_info": "秋叶向里线起始节点。",
            "preset": {"akiha_regard": 4, "flg6": 1},
        },
        {
            "id": "aki_02", "cat": "akiha", "day": "DAY 03 · 盛夏幻影",
            "title": "酷暑之夏与弓塚五月的异变", "sub": "DAY 03 · SUMMER MIRAGE",
            "seen_label": "s235", "branch_label": "f235", "mode": "continue",
            "thumb": "images/bg/cmo_19.webp", "cast": "远野志贵、远野秋叶、弓塚五月",
            "desc": "遥远酷暑的蝉鸣回忆掠过脑海。里线第三日，悄然蔓延的吸血怪异正步步逼近身边的同班少女弓塚五月。",
            "branch_info": "里线第三日主干 · 弓塚悲剧与宅邸谜团展开。",
            "preset": {"akiha_regard": 5, "flg6": 1},
        },
        {
            "id": "aki_03", "cat": "akiha", "day": "DAY 04 · 茜之兆",
            "title": "强光惊醒与秋叶的秘密", "sub": "DAY 04 · CRIMSON OMEN",
            "seen_label": "s305", "branch_label": "f305", "mode": "continue",
            "thumb": "images/cg/aki_e01.webp", "cast": "远野志贵、远野秋叶",
            "desc": "在强光下睁开双眼。作为远野家当代家主的妹妹秋叶，高傲冷静的外表之下隐藏着以红发为代价的血脉诅咒。",
            "branch_info": "秋叶线第四日关键篇章。",
            "preset": {"akiha_regard": 7, "flg6": 1},
        },
        {
            "id": "aki_04", "cat": "akiha", "day": "DAY 05 · 剧痛苏醒",
            "title": "远野血脉与反转冲动", "sub": "DAY 05 · BLOOD OF TOHNO",
            "seen_label": "s325", "branch_label": "f325", "mode": "continue",
            "thumb": "images/cg/aki_e03.webp", "cast": "远野志贵、远野秋叶",
            "desc": "伴随剧痛在清晨苏醒，志贵正式锁定秋叶个人线。兄妹之间跨越八年时光的羁绊与远野家狂血开始正面交锋。",
            "branch_info": "秋叶个人线正式分支起点（f325）。",
            "preset": {"akiha_regard": 9, "flgP": 1, "flg6": 1},
        },
        {
            "id": "aki_05", "cat": "akiha", "day": "DAY 08 · 红发掠夺",
            "title": "秋叶的真相与炽热一夜", "sub": "DAY 08 · VERMILION TRUTH",
            "seen_label": "s361", "branch_label": "f361", "mode": "continue",
            "thumb": "images/cg/aki_e09.webp", "cast": "远野志贵、远野秋叶",
            "desc": "淡薄晨光中醒来，历经贫血与动荡的志贵愈发靠近秋叶拼命隐瞒的「槛发」真相与生命共享的秘密。",
            "branch_info": "秋叶线第八日核心情感章。",
            "preset": {"akiha_regard": 11, "flgP": 1, "flg6": 1},
        },
        {
            "id": "aki_06", "cat": "akiha", "day": "DAY 10 · 庭院丝带",
            "title": "远野四季与八年前的哭泣", "sub": "DAY 10 · RIBBON IN THE GARDEN",
            "seen_label": "s365", "branch_label": "f365", "mode": "continue",
            "thumb": "images/bg/cmo_20.webp", "cast": "远野志贵、远野秋叶、远野四季",
            "desc": "无人的庭院里，幼年秋叶泣不成声地道歉。被替换的兄长身份、产土神之血与地下牢狱的真相彻底揭晓。",
            "branch_info": "秋叶线第十日真相揭露章。",
            "preset": {"akiha_regard": 12, "flgP": 1, "flg6": 1},
        },
        {
            "id": "aki_07", "cat": "akiha", "day": "DAY 12 · 最终夜",
            "title": "他人的梦与生死的抉择", "sub": "DAY 12 · SOMEONE ELSE'S DREAM",
            "seen_label": "s375", "branch_label": "f375", "mode": "continue",
            "thumb": "images/cg/aki_e07a.webp", "cast": "远野志贵、远野秋叶、远野四季",
            "desc": "在梦中窥见了属于远野四季的残酷往事。面临彻底红赤化的秋叶，志贵必须做出最惨烈也最温柔的抉择。",
            "branch_info": "秋叶线最终决战入口，通向 TRUE / GOOD 双结局。",
            "preset": {"akiha_regard": 14, "flgP": 1, "flg6": 1},
        },
        {
            "id": "aki_08", "cat": "akiha", "day": "EPILOGUE · TRUE END",
            "title": "秋叶 TRUE END · 苍之月", "sub": "AKIHA TRUE · BLUE MOON",
            "seen_label": "s385", "branch_label": "f385", "mode": "continue",
            "thumb": "images/cg/aki_f02.webp", "cast": "远野志贵、远野秋叶",
            "desc": "死亡绝非救赎。将一半生命归还给妹妹后，秋叶独自站在坡道洋馆前，坚信兄长终会归来，永远等待下去。",
            "branch_info": "秋叶线催泪真结局（含完整终章与 ED）。",
            "preset": {"akiha_regard": 15, "flgP": 1},
        },
        {
            "id": "aki_09", "cat": "akiha", "day": "EPILOGUE · NORMAL END",
            "title": "秋叶 NORMAL END · 四季之梦", "sub": "AKIHA NORMAL · DREAM OF SEASONS",
            "seen_label": "s384", "branch_label": "f384", "mode": "continue",
            "thumb": "images/cg/aki_e08.webp", "cast": "远野志贵、远野秋叶",
            "desc": "为了有一天当秋叶再度睁开双眼时，能够用一句稀松平常的「嗨」去迎接她，少年选择带着希望继续活下去。",
            "branch_info": "秋叶线普通结局（原版官方定名 Normal End，含完整终章、ED 与知得留授课）。",
            "preset": {"akiha_regard": 15, "flgP": 1},
        },

        # --- 里线 · 翡翠线 (HISUI ROUTE) ---
        {
            "id": "his_01", "cat": "hisui", "day": "DAY 04 · 翡翠线",
            "title": "金属门扉与沉寂的侍女", "sub": "DAY 04 · SILENT MAID",
            "seen_label": "s315", "branch_label": "f315", "mode": "continue",
            "thumb": "images/cg/his_e01.webp", "cast": "远野志贵、翡翠",
            "desc": "推开沉重的铁门回到宅邸。总是一丝不苟、沉默克制的专属侍女翡翠，眼神深处似乎始终藏着无法言说的秘密。",
            "branch_info": "翡翠线前期核心节点。",
            "preset": {"hisui_regard": 6, "flg6": 1},
        },
        {
            "id": "his_02", "cat": "hisui", "day": "DAY 05 · 欢迎酒宴",
            "title": "翡翠个人线 · 微醺之夜", "sub": "DAY 05 · MANSION BANQUET",
            "seen_label": "s323", "branch_label": "f323", "mode": "continue",
            "thumb": "images/cg/his_e02.webp", "cast": "远野志贵、翡翠、琥珀、远野秋叶",
            "desc": "客厅里的欢迎会演变成酒宴，不胜酒力的翡翠渐渐露出罕见的破绽。自此正式锁定翡翠个人线。",
            "branch_info": "翡翠个人线锁定节点（f323）。",
            "preset": {"hisui_regard": 8, "flg6": 1},
        },
        {
            "id": "his_03", "cat": "hisui", "day": "DAY 07 · 深陷梦魇",
            "title": "难以醒来的幽闭病房", "sub": "DAY 07 · TRAPPED IN NIGHTMARE",
            "seen_label": "s399", "branch_label": "f399", "mode": "continue",
            "thumb": "images/cg/his_e04.webp", "cast": "远野志贵、翡翠",
            "desc": "身体日益衰弱、被困于暗黑噩梦中的志贵，逐渐发觉宅邸内的异样与自身记忆深处致命的违和感。",
            "branch_info": "翡翠线中盘悬疑高潮（幽闭期开端）。",
            "preset": {"hisui_regard": 10, "flg6": 1},
        },
        {
            "id": "his_04", "cat": "hisui", "day": "DAY 08 · 暗流",
            "title": "餐后红茶与崩溃的前奏", "sub": "DAY 08 · AFTERNOON TEA",
            "seen_label": "s402", "branch_label": "f402", "mode": "continue",
            "thumb": "images/cg/his_e08.webp", "cast": "远野志贵、翡翠、琥珀、远野秋叶",
            "desc": "客厅中看似平静的红茶时光背后，精神与肉体同步走向失控。双子侍女长达八年的命运轮盘开始加速旋转。",
            "branch_info": "翡翠线最核心的长篇转折章（共逾千句完整剧情）。",
            "preset": {"hisui_regard": 11, "flg6": 1},
        },
        {
            "id": "his_05", "cat": "hisui", "day": "DAY 13 · 敲门声",
            "title": "终焉之门 · 真相大白", "sub": "DAY 13 · KNOCKING AT THE DOOR",
            "seen_label": "s408", "branch_label": "f408", "mode": "continue",
            "thumb": "images/cg/his_e06.webp", "cast": "远野志贵、翡翠、琥珀、远野四季",
            "desc": "咚、咚咚、咚。打破幽闭的敲门声响起，《月姬》全篇最具冲击力的双子互换真相与最终对决拉开帷幕。",
            "branch_info": "翡翠线最终章入口，直通 TRUE / GOOD 双结局。",
            "preset": {"hisui_regard": 14, "flg6": 1},
        },
        {
            "id": "his_06", "cat": "hisui", "day": "EPILOGUE · TRUE END",
            "title": "翡翠 TRUE END · 拂晓之梦", "sub": "HISUI TRUE · DREAM AT DAWN",
            "seen_label": "s412", "branch_label": "f412", "mode": "continue",
            "thumb": "images/cg/his_f03.webp", "cast": "远野志贵、翡翠、琥珀",
            "desc": "在所有谎言与复仇尘埃落定后，翡翠终于卸下八年的重担。这也是全作最深沉震撼、解开琥珀线前置锁的终局。",
            "branch_info": "翡翠线真结局（通关后永久解锁琥珀线入口！）。",
            "preset": {"hisui_regard": 15},
        },
        {
            "id": "his_07", "cat": "hisui", "day": "EPILOGUE · GOOD END",
            "title": "翡翠 GOOD END · 阳向之梦", "sub": "HISUI GOOD · SUNNY DREAM",
            "seen_label": "s413", "branch_label": "f413", "mode": "continue",
            "thumb": "images/cg/his_e09.webp", "cast": "远野志贵、翡翠、琥珀",
            "desc": "千钧一发之际呼喊出那个名字，挽回了无法替代的羁绊。紧握翡翠的双手，无悔地向着微光继续前行。",
            "branch_info": "翡翠线二周目好结局（含完整终章与 ED）。",
            "preset": {"hisui_regard": 15},
        },

        # --- 里线 · 琥珀线 (KOHAKU ROUTE) ---
        {
            "id": "koh_01", "cat": "kohaku", "day": "DAY 05 · 琥珀线入口",
            "title": "假面后的微笑 · 琥珀个人线", "sub": "DAY 05 · BEHIND THE SMILE",
            "seen_label": "s324", "branch_label": "f324", "mode": "continue",
            "thumb": "images/cg/koha_e01a.webp", "cast": "远野志贵、琥珀",
            "desc": "通关翡翠线后方可踏入的隐藏终线。总是带着灿烂笑容操持宅邸的琥珀，内里却藏着无人触及的空洞与创伤。",
            "branch_info": "琥珀线正式分岐起点（f324 → f416）。",
            "preset": {"kohaku_regard": 9, "flg6": 1},
        },
        {
            "id": "koh_02", "cat": "kohaku", "day": "DAY 05 · 异变初现",
            "title": "孤身惊醒与庭院丝带", "sub": "DAY 05 · AWAKENING ALONE",
            "seen_label": "s416", "branch_label": "f416", "mode": "continue",
            "thumb": "images/cg/koha_e03.webp", "cast": "远野志贵、琥珀",
            "desc": "背脊残留着被压迫般的剧痛独自醒来。在阳光洒落的日本庭院里，志贵一步步走近琥珀尘封的真实心声。",
            "branch_info": "琥珀线第五日核心篇章。",
            "preset": {"kohaku_regard": 10, "flg6": 1},
        },
        {
            "id": "koh_03", "cat": "kohaku", "day": "DAY 07 · 探寻真相",
            "title": "向琥珀询问 · 过去的钥匙", "sub": "DAY 07 · ASKING KOHAKU",
            "seen_label": "s417", "branch_label": "f417", "mode": "continue",
            "thumb": "images/cg/koha_e04.webp", "cast": "远野志贵、琥珀",
            "desc": "决定直接找琥珀问清宅邸隐藏的一切。微笑的人偶第一次露出了属于真正人类的颤抖与悲哀。",
            "branch_info": "琥珀线第七日主线。",
            "preset": {"kohaku_regard": 11, "flg6": 1},
        },
        {
            "id": "koh_04", "cat": "kohaku", "day": "DAY 09 · 心跳声",
            "title": "暴走逼近与最后的守护", "sub": "DAY 09 · POUNDING HEART",
            "seen_label": "s422", "branch_label": "f422", "mode": "continue",
            "thumb": "images/cg/koha_e06.webp", "cast": "远野志贵、琥珀、远野秋叶",
            "desc": "沉重的心跳声回荡耳际，失控的狂血与远野家的最终清算已迫在眉睫。",
            "branch_info": "琥珀线第九日高潮。",
            "preset": {"kohaku_regard": 13, "flg6": 1},
        },
        {
            "id": "koh_05", "cat": "kohaku", "day": "DAY 11 · 决意",
            "title": "为了守护她的笑容", "sub": "DAY 11 · FOR HER SMILE",
            "seen_label": "s425", "branch_label": "f425", "mode": "continue",
            "thumb": "images/cg/koha_e08.webp", "cast": "远野志贵、琥珀、远野秋叶",
            "desc": "哪怕身体已达极限，志贵仍下定决心直面红赤化的秋叶，替一直独自承受地狱的琥珀斩断过往枷锁。",
            "branch_info": "琥珀线最终战前夕（注意此处含致命选项分歧）。",
            "preset": {"kohaku_regard": 14, "flg6": 1},
        },
        {
            "id": "koh_06", "cat": "kohaku", "day": "EPILOGUE · TRUE END",
            "title": "琥珀 TRUE END · 阳向之梦", "sub": "KOHAKU TRUE · SUNNY GARDEN",
            "seen_label": "s429", "branch_label": "f429", "mode": "continue",
            "thumb": "images/cg/koha_f03.webp", "cast": "远野志贵、琥珀、翡翠、远野秋叶",
            "desc": "「欢迎回来。这次，就真的完成小时候的约定了。」全作五线最终的救赎，绽放在满园向阳花海之中。",
            "branch_info": "琥珀线唯一真结局（含完整终章与 ED）。",
            "preset": {"kohaku_regard": 15},
        },

        # --- 知得留课堂与尾声月蚀 (DOJOS & ECLIPSE) ---
        {
            "id": "ext_01", "cat": "extra", "day": "知得留课堂 · 第 1 讲",
            "title": "动物乐园与首次 Dead End", "sub": "CIEL-SENSEI LESSON 01",
            "seen_label": "s511", "branch_label": "s511", "mode": "scene",
            "thumb": "images/bg/bg_06a.webp", "cast": "知得留老师、爱尔奎特",
            "desc": "欢迎来到《教教我吧！知得留老师！》第一回，为早早踏入 Dead End 的远野君送上无情吐槽与通关指南。",
            "branch_info": "独立道场小剧场（观看完毕返回标题菜单）。",
            "preset": {},
        },
        {
            "id": "ext_02", "cat": "extra", "day": "知得留课堂 · 第 2~4 讲",
            "title": "心惊胆战动物乐园连载篇", "sub": "CIEL-SENSEI · ANIMAL PARADISE",
            "seen_label": "s512", "branch_label": "s512", "mode": "scene",
            "thumb": "images/bg/bg_06a.webp", "cast": "知得留老师、爱尔奎特",
            "desc": "关于野生动物学与如何在尼禄·卡欧斯的兽群中活下来的爆笑吐槽课程。",
            "branch_info": "独立道场小剧场。",
            "preset": {},
        },
        {
            "id": "ext_03", "cat": "extra", "day": "知得留课堂 · 代班特辑",
            "title": "咖喱面包翘班事件", "sub": "CIEL-SENSEI · CURRY BREAK",
            "seen_label": "s515", "branch_label": "s515", "mode": "scene",
            "thumb": "images/bg/bg_06a.webp", "cast": "翡翠、爱尔奎特、远野志贵",
            "desc": "知得留老师跑去吃咖喱面包玩忽职守，由侍女翡翠临时主持的珍稀代班剧场！",
            "branch_info": "独立道场小剧场。",
            "preset": {},
        },
        {
            "id": "ext_04", "cat": "extra", "day": "知得留课堂 · 找人指南",
            "title": "左右不分与寻人基本法", "sub": "CIEL-SENSEI · FINDING ARCUEID",
            "seen_label": "s517", "branch_label": "s517", "mode": "scene",
            "thumb": "images/bg/bg_06a.webp", "cast": "知得留老师、爱尔奎特",
            "desc": "第六课：一针见血剖析远野君为什么总是在找人环节走错路。",
            "branch_info": "独立道场小剧场。",
            "preset": {},
        },
        {
            "id": "ext_05", "cat": "extra", "day": "知得留课堂 · 特别嘉宾",
            "title": "罗亚博士的吸血鬼讲座", "sub": "CIEL-SENSEI · DR. ROA",
            "seen_label": "s537", "branch_label": "s537", "mode": "scene",
            "thumb": "images/bg/bg_06a.webp", "cast": "知得留老师、罗阿博士",
            "desc": "请来反派 Boss 罗阿博士亲自客串点评如何与吸血鬼战斗的名场面道场。",
            "branch_info": "独立道场小剧场。",
            "preset": {},
        },
        {
            "id": "ext_06", "cat": "extra", "day": "知得留课堂 · 补习篇",
            "title": "课后强化补习（之一）", "sub": "CIEL-SENSEI · EXTRA LESSON I",
            "seen_label": "s543", "branch_label": "s543", "mode": "scene",
            "thumb": "images/bg/bg_06b.webp", "cast": "知得留老师、爱尔奎特",
            "desc": "琥珀线中面对无敌模式秋叶冲动出手的课后特别吐槽补习。",
            "branch_info": "独立道场小剧场。",
            "preset": {},
        },
        {
            "id": "ext_07", "cat": "extra", "day": "尾声 · 月蝕",
            "title": "「月蝕」ECLIPSE · 苍之魔法使的告别", "sub": "EPILOGUE · ECLIPSE",
            "seen_label": "eclipse", "branch_label": "eclipse", "mode": "scene",
            "thumb": "images/cg/ao_01.webp", "cast": "远野志贵、苍崎青子",
            "desc": "五线九结局全破后解锁的隐藏终章。在漫无边际的月夜草原上，少年与红发魔法使再度重逢，为整个《月姬》物语画下永恒句点。",
            "branch_info": "全结局达成后于标题画面与物语图谱同步开放。",
            "preset": {},
        },
    ]

    def get_flowchart_node(nid):
        for n in FLOWCHART_NODES:
            if n["id"] == nid:
                return n
        return FLOWCHART_NODES[0]

    def is_fc_node_available(node):
        """Multi-edition guard: ensure target labels exist in the user's imported script."""
        return bool(renpy.has_label(node["branch_label"]) and renpy.has_label(node["seen_label"]))

    def is_fc_node_unlocked(node):
        if not is_fc_node_available(node):
            return False
        if persistent.unlock_all_routes:
            return True
        if node["id"] == "com_00":
            return True
        if node["id"] == "ext_07":
            return is_tsukishoku_unlocked()
        if renpy.seen_label(node["seen_label"]):
            return True
        if node["branch_label"] and renpy.seen_label(node["branch_label"]):
            return True
        return False

    def get_fc_category_nodes(cat_id):
        if cat_id == "all":
            return FLOWCHART_NODES
        return [n for n in FLOWCHART_NODES if n["cat"] == cat_id]

    def get_fc_stats(cat_id):
        cn = get_fc_category_nodes(cat_id)
        cu = sum(1 for n in cn if is_fc_node_unlocked(n))
        au = sum(1 for n in FLOWCHART_NODES if is_fc_node_unlocked(n))
        at = len(FLOWCHART_NODES)
        cp = int(round(cu * 100.0 / len(cn))) if cn else 0
        ap = int(round(au * 100.0 / at)) if at else 0
        return cu, len(cn), cp, au, at, ap


default flowchart_target_node_id = "com_00"
default current_fc_node_id = None

init -1 python:
    # Live label -> Flowchart node tracker (saved in save files & synced with rollback!)
    FC_LABEL_TO_NODE = {}
    for _n in FLOWCHART_NODES:
        if _n.get("branch_label"):
            FC_LABEL_TO_NODE[_n["branch_label"]] = _n["id"]
        if _n.get("seen_label"):
            FC_LABEL_TO_NODE[_n["seen_label"]] = _n["id"]

    # Map secondary epilogue & post-ending Ciel-sensei dojo labels back to their parent ending node
    FC_LABEL_TO_NODE.update({
        "f52a": "arc_09", "s52": "arc_09", "f520": "arc_09", "s520": "arc_09",
        "f53a": "arc_10", "s53": "arc_10", "f521": "arc_10", "s521": "arc_10",
        "f527": "ciel_06", "s527": "ciel_06",
        "f528": "ciel_07", "s528": "ciel_07",
        "f541": "aki_08",  "s541": "aki_08",
        "f542": "aki_09",  "s542": "aki_09",
        "f530": "his_06",  "s530": "his_06",
        "f531": "his_07",  "s531": "his_07",
        "f545": "koh_06",  "s545": "koh_06",
    })

    def tsuki_format_save_name(node):
        if not node:
            return ""
        if is_ui_en():
            return node.get("sub", "")
        return f"{node['day']} · {node['title']}"

    def _tsuki_track_flowchart_label(name, abnormal):
        nid = FC_LABEL_TO_NODE.get(name)
        if nid:
            store.current_fc_node_id = nid
            store.save_name = tsuki_format_save_name(FC_NODE_MAP.get(nid))

    if _tsuki_track_flowchart_label not in config.label_callbacks:
        config.label_callbacks.append(_tsuki_track_flowchart_label)

    def fc_scroll_to_node(view_id, nid):
        """Smoothly snap the Flowchart viewport vertically to center the target node."""
        nodes_out, _, _, _, canvas_h = get_fc_view_layout(view_id)
        vp = renpy.get_displayable("flowchart", "fc_vp")
        if vp is None:
            return
        max_scroll = max(0, canvas_h - 976)
        for _nid, _, _, ny, _, nh in nodes_out:
            if _nid == nid:
                target_px = max(0, min(max_scroll, int(ny + nh // 2 - 440)))
                vp.yadjustment.change(target_px)
                return

    def get_fc_initial_yfrac(view_id, nid):
        nodes_out, _, _, _, canvas_h = get_fc_view_layout(view_id)
        max_scroll = max(1, canvas_h - 976)
        for _nid, _, _, ny, _, nh in nodes_out:
            if _nid == nid:
                target_px = max(0, min(max_scroll, int(ny + nh // 2 - 440)))
                return float(target_px) / float(max_scroll)
        return 0.0

## ==============================================================================
## True Branch Continuation Dispatcher (Clears stale call stack + injects state!)
## ==============================================================================
label flowchart_jump_dispatcher:
    # CRITICAL: Wipe any stale in-game `call sXX` return frames so endings ALWAYS
    # return cleanly to Main Menu instead of popping back into an old Day 1 menu!
    $ renpy.set_return_stack([])
    $ renpy.block_rollback()
    $ quick_menu = True
    nvl clear
    stop music fadeout 1.0
    stop ambient fadeout 0.8
    stop sound
    $ tsuki_clear_stage()
    $ tsuki_reset_run_state()

    python:
        _fc_node = get_flowchart_node(flowchart_target_node_id)
        store.current_fc_node_id = _fc_node["id"]
        store.save_name = tsuki_format_save_name(_fc_node)
        for _vk, _vv in _fc_node.get("preset", {}).items():
            setattr(store, _vk, _vv)
        _fc_mode = _fc_node.get("mode", "continue")
        _fc_target = _fc_node["branch_label"]

    $ renpy.pause(0.35, hard=True)

    if _fc_mode == "continue":
        jump expression _fc_target
    else:
        call expression _fc_target
        nvl clear
        stop music fadeout 1.2
        $ current_fc_node_id = None
        $ tsuki_solid("#000000", "crossfade_mid")
        $ renpy.pause(0.4, hard=True)
        $ renpy.set_return_stack([])
        return


init -1 python:
    # ==========================================================================
    # Tsukihime R-Aligned Chronological Tree Topology (5 Routes + Eclipse + Dojos)
    # Every verified node placed on an orthogonal (col, row) timeline with ZERO crossings!
    # ==========================================================================
    FC_VIEW_TABS = [
        ("all",   "全五线总览", "All Routes"),
        ("near",  "表线 · 近月", "Near Side"),
        ("far",   "里线 · 远月", "Far Side"),
        ("extra", "月蝕与课堂",  "Eclipse & Dojos"),
    ]

    # Route lane visual metadata (Plan A soft Morandi-pastel palette!)
    FC_LANE_HEADERS = {
        "all": [
            (0, "爱尔奎特", "Arcueid", "#dec894"),
            (1, "希耶尔",   "Ciel",    "#98c2e2"),
            (2, "月蝕终章", "Eclipse", "#dec894"),
            (3, "远野秋叶", "Akiha",   "#d698a3"),
            (4, "翡翠",     "Hisui",   "#9ac9cf"),
            (5, "琥珀",     "Kohaku",  "#ddb692"),
        ],
        "near": [
            (0, "共通 · 爱尔奎特", "Common · Arcueid", "#dec894"),
            (1, "希耶尔线",       "Ciel Route",        "#98c2e2"),
        ],
        "far": [
            (0, "远野秋叶线", "Akiha Route",  "#d698a3"),
            (1, "翡翠线",     "Hisui Route",  "#9ac9cf"),
            (2, "琥珀线",     "Kohaku Route", "#ddb692"),
        ],
        "extra": [
            (0, "月蝕终章 · 知得留课堂", "Eclipse & Ciel-Sensei", "#dec894"),
        ],
    }

    # Master ALL-view (col, row) positions for all 54 verified nodes
    FC_MASTER_POS = {
        # Prologue & Day 1 Common
        "com_00": (0, 0),
        "com_01": (0, 1),  "com_02": (1, 1),
        "com_03": (0, 2),
        "com_04": (0, 3),
        "com_05": (0, 4),  "aki_01": (3, 4),
        # Day 2 Near Side
        "com_06": (0, 5),
        "com_07": (0, 6),
        # Day 3 Near & Far
        "arc_01": (0, 7),  "aki_02": (3, 7),
        "arc_02": (0, 8),
        "arc_03": (0, 9),
        # Day 4 Branch Prep
        "arc_04": (0, 10), "aki_03": (3, 10), "his_01": (4, 10),
        # Day 5 Five-Route Split
        "arc_05": (0, 11), "ciel_01": (1, 11), "aki_04": (3, 11), "his_02": (4, 11), "koh_01": (5, 11),
        "koh_02": (5, 12),
        # Day 7
        "arc_06": (0, 13), "ciel_02": (1, 13), "his_03": (4, 13), "koh_03": (5, 13),
        # Day 8
        "aki_05": (3, 14), "his_04": (4, 14),
        # Day 9
        "arc_07": (0, 15), "ciel_03": (1, 15), "koh_04": (5, 15),
        # Day 10
        "ciel_04": (1, 16), "aki_06": (3, 16),
        # Day 11-13 Climax
        "arc_08": (0, 17), "ciel_05": (1, 17), "aki_07": (3, 17), "his_05": (4, 17), "koh_05": (5, 17),
        # Epilogue: 5 TRUE ENDS
        "arc_09": (0, 18), "ciel_06": (1, 18), "aki_08": (3, 18), "his_06": (4, 18), "koh_06": (5, 18),
        # Epilogue: 4 GOOD ENDS
        "arc_10": (0, 19), "ciel_07": (1, 19), "aki_09": (3, 19), "his_07": (4, 19),
        # Grand Finale: 「月蝕」ECLIPSE (All 5 routes converge here!)
        "ext_07": (2, 20),
        # Bonus: Ciel-sensei Dojos
        "ext_01": (0, 21), "ext_02": (1, 21), "ext_03": (2, 21), "ext_04": (3, 21), "ext_05": (4, 21), "ext_06": (5, 21),
    }

    # Right-aligned Tsukihime R Day Divider Bands (row -> list of day titles shown on left)
    FC_MASTER_DAYS = {
        0:  ["0／割草之夏", "序章"],
        1:  ["1／翻转的日常", "远野宅邸"],
        5:  ["2／直死之眼", "十七分割"],
        7:  ["3／真祖与混沌", "盛夏幻影"],
        10: ["4／同行与茜兆"],
        11: ["5／五线分歧"],
        13: ["7／回忆与梦魇"],
        14: ["8／红发与暗流"],
        15: ["9／纯白之伤", "第七圣典"],
        16: ["10／庭院丝带"],
        17: ["11-13／最终夜"],
        18: ["终／五线结局"],
        20: ["月蝕／ECLIPSE"],
        21: ["番外／知得留"],
    }

    FC_MASTER_DAYS_EN = {
        0:  ["0 / Prologue", "Blue Glasses"],
        1:  ["1 / Tohno Mansion", "First Day"],
        5:  ["2 / Death Perception", "17 Pieces"],
        7:  ["3 / Chaos & Mirage", "Resurrection"],
        10: ["4 / White Room", "Crimson Omen"],
        11: ["5 / Five-Route Split"],
        13: ["7 / Forgotten Garden", "Nightmare"],
        14: ["8 / Vermilion Truth", "Afternoon Tea"],
        15: ["9 / Eve of Fate", "Seventh Scripture"],
        16: ["10 / Ribbon & Erosion"],
        17: ["11-13 / Final Night"],
        18: ["End / Five Routes"],
        20: ["ECLIPSE / Epilogue"],
        21: ["Extra / Ciel-Sensei"],
    }

    FC_CAST_EN = {
        "远野志贵": "Shiki Tohno",
        "苍崎青子": "Aoko Aozaki",
        "乾有彦": "Arihiko Inui",
        "希耶尔": "Ciel",
        "弓塚五月": "Satsuki Yumizuka",
        "翡翠": "Hisui",
        "琥珀": "Kohaku",
        "远野秋叶": "Akiha Tohno",
        "爱尔奎特": "Arcueid",
        "尼禄·卡欧斯": "Nrvnqsr Chaos",
        "罗阿": "Roa",
        "远野四季": "SHIKI Tohno",
        "知得留老师": "Ciel-Sensei",
        "罗阿博士": "Dr. Roa",
    }

    def fc_translate_cast(cast_zh):
        parts = [p.strip() for p in cast_zh.split("、") if p.strip()]
        return ", ".join(FC_CAST_EN.get(p, p) for p in parts)

    # Directed parent -> child edges (mode: "split" bends right after parent, "merge" bends right above child)
    FC_MASTER_EDGES = [
        ("com_00", "com_01", "split"),
        ("com_00", "com_02", "split"),
        ("com_01", "com_03", "merge"),
        ("com_02", "com_03", "merge"),
        ("com_03", "com_04", "split"),
        ("com_04", "com_05", "split"),
        # Day 1 Night Near / Far Split
        ("com_05", "com_06", "split"),
        ("com_05", "aki_01", "horiz"),
        # Near Side Spine
        ("com_06", "com_07", "split"),
        ("com_07", "arc_01", "split"),
        ("arc_01", "arc_02", "split"),
        ("arc_02", "arc_03", "split"),
        ("arc_03", "arc_04", "split"),
        # Arcueid & Ciel Route Split
        ("arc_04", "arc_05", "split"),
        ("arc_04", "ciel_01", "split"),
        ("arc_05", "arc_06", "split"),
        ("arc_06", "arc_07", "split"),
        ("arc_07", "arc_08", "split"),
        ("arc_08", "arc_09", "split"),
        ("arc_09", "arc_10", "split"),
        ("ciel_01", "ciel_02", "split"),
        ("ciel_02", "ciel_03", "split"),
        ("ciel_03", "ciel_04", "split"),
        ("ciel_04", "ciel_05", "split"),
        ("ciel_05", "ciel_06", "split"),
        ("ciel_06", "ciel_07", "split"),
        # Far Side Spine (Akiha / Hisui / Kohaku)
        ("aki_01", "aki_02", "split"),
        ("aki_02", "aki_03", "merge"),
        ("aki_02", "his_01", "merge"),
        ("aki_03", "aki_04", "split"),
        ("aki_04", "aki_05", "split"),
        ("aki_05", "aki_06", "split"),
        ("aki_06", "aki_07", "split"),
        ("aki_07", "aki_08", "split"),
        ("aki_08", "aki_09", "split"),
        ("his_01", "his_02", "split"),
        ("his_01", "koh_01", "split"),
        ("his_02", "his_03", "split"),
        ("his_03", "his_04", "split"),
        ("his_04", "his_05", "split"),
        ("his_05", "his_06", "split"),
        ("his_06", "his_07", "split"),
        ("koh_01", "koh_02", "split"),
        ("koh_02", "koh_03", "split"),
        ("koh_03", "koh_04", "split"),
        ("koh_04", "koh_05", "split"),
        ("koh_05", "koh_06", "split"),
        # All 5 Routes Converge into Grand Finale 「月蝕」ECLIPSE!
        ("arc_10", "ext_07", "eclipse"),
        ("ciel_07", "ext_07", "eclipse"),
        ("aki_09", "ext_07", "eclipse"),
        ("his_07", "ext_07", "eclipse"),
        ("koh_06", "ext_07", "eclipse"),
    ]

    FC_ENDING_BADGES = {
        "arc_09": "TRUE", "arc_10": "GOOD",
        "ciel_06": "TRUE", "ciel_07": "GOOD",
        "aki_08": "TRUE", "aki_09": "NORMAL",
        "his_06": "TRUE", "his_07": "GOOD",
        "koh_06": "TRUE",
        "ext_07": "ECLIPSE",
        "ext_01": "第1讲", "ext_02": "第2讲", "ext_03": "代班篇",
        "ext_04": "第6讲", "ext_05": "罗阿篇", "ext_06": "补习篇",
    }

    FC_ENDING_BADGES_EN = {
        "ext_01": "L-01", "ext_02": "L-02", "ext_03": "SUB",
        "ext_04": "L-06", "ext_05": "ROA", "ext_06": "EXTRA",
    }

    FC_NODE_MAP = {n["id"]: n for n in FLOWCHART_NODES}

    def get_fc_view_layout(view_id):
        """
        Compute exact pixel-perfect node coordinates, day bands & orthogonal connector
        segments for the selected flowchart view ('all', 'near', 'far', 'extra').
        """
        TREE_X0 = 286
        TREE_Y0 = 26
        COL_PITCH = 164
        ROW_PITCH = 108
        TILE_W = 132
        TILE_H = 74
        master_days = FC_MASTER_DAYS_EN if is_ui_en() else FC_MASTER_DAYS

        if view_id == "all":
            pos_map = dict(FC_MASTER_POS)
            days_map = dict(master_days)
        elif view_id == "near":
            keep = [nid for nid, n in FC_NODE_MAP.items() if n["cat"] in ("common", "arc", "ciel")]
            used_rows = sorted({FC_MASTER_POS[nid][1] for nid in keep})
            r_remap = {r: idx for idx, r in enumerate(used_rows)}
            pos_map = {nid: (FC_MASTER_POS[nid][0], r_remap[FC_MASTER_POS[nid][1]]) for nid in keep}
            days_map = {r_remap[r]: lbls for r, lbls in master_days.items() if r in r_remap}
        elif view_id == "far":
            keep = ["com_05"] + [nid for nid, n in FC_NODE_MAP.items() if n["cat"] in ("akiha", "hisui", "kohaku")]
            used_rows = sorted({FC_MASTER_POS[nid][1] for nid in keep})
            r_remap = {r: idx for idx, r in enumerate(used_rows)}
            pos_map = {}
            for nid in keep:
                mc, mr = FC_MASTER_POS[nid]
                nc = 0 if nid == "com_05" else max(0, mc - 3)
                pos_map[nid] = (nc, r_remap[mr])
            days_map = {r_remap[r]: lbls for r, lbls in master_days.items() if r in r_remap}
        else:  # "extra": Eclipse + 6 Dojos
            pos_map = {
                "ext_07": (0, 0),
                "ext_01": (0, 1), "ext_02": (1, 1), "ext_03": (2, 1),
                "ext_04": (0, 2), "ext_05": (1, 2), "ext_06": (2, 2),
            }
            if is_ui_en():
                days_map = {
                    0: ["ECLIPSE", "Grand Epilogue"],
                    1: ["Ciel-Sensei", "Lessons 1 - 3"],
                    2: ["Ciel-Sensei", "Specials & Extra"],
                }
            else:
                days_map = {
                    0: ["月蝕／ECLIPSE", "五线全通终章"],
                    1: ["番外／知得留", "第 1 ~ 3 讲"],
                    2: ["番外／知得留", "特别篇与补习"],
                }

        max_row = max((r for _, r in pos_map.values()), default=0)
        canvas_h = TREE_Y0 + (max_row + 1) * ROW_PITCH + 64
        canvas_w = 1320

        # Build node pixel rects
        nodes_out = []
        rect_map = {}
        for nid, (c, r) in pos_map.items():
            x = TREE_X0 + c * COL_PITCH
            y = TREE_Y0 + r * ROW_PITCH
            w = TILE_W
            h = TILE_H
            # Make 「月蝕」ECLIPSE subtly wider & centered on its column to emphasize the grand finale!
            if nid == "ext_07":
                w = 152
                h = 80
                x = TREE_X0 + c * COL_PITCH - 10
                y = TREE_Y0 + r * ROW_PITCH - 2
            rect_map[nid] = (x, y, w, h)
            nodes_out.append((nid, FC_NODE_MAP[nid], x, y, w, h))

        # Build orthogonal 2px connector segments (x, y, w, h, color)
        segs = []
        for u, v, mode in FC_MASTER_EDGES:
            if u not in rect_map or v not in rect_map:
                continue
            x1, y1, w1, h1 = rect_map[u]
            x2, y2, w2, h2 = rect_map[v]
            cx1, by1 = x1 + w1 // 2, y1 + h1
            cx2, ty2 = x2 + w2 // 2, y2

            u_ok = is_fc_node_unlocked(FC_NODE_MAP[u])
            v_ok = is_fc_node_unlocked(FC_NODE_MAP[v])
            if mode == "eclipse":
                col = "#dec894aa" if v_ok else "#5c534088"
            elif u_ok and v_ok:
                col = "#84a2be"
            else:
                col = "#3d4a5c"

            if mode == "horiz" and y1 == y2:
                lx = min(x1 + w1, x2 + w2)
                rx = max(x1, x2)
                if rx > lx:
                    segs.append((lx, y1 + h1 // 2, rx - lx, 2, col))
            elif cx1 == cx2:
                if ty2 > by1:
                    segs.append((cx1 - 1, by1, 2, ty2 - by1, col))
            else:
                if mode == "split":
                    mid_y = by1 + 16
                else:
                    mid_y = ty2 - 17
                if mid_y > by1:
                    segs.append((cx1 - 1, by1, 2, mid_y - by1, col))
                lx = min(cx1, cx2)
                rx = max(cx1, cx2)
                segs.append((lx - 1, mid_y, (rx - lx) + 2, 2, col))
                if ty2 > mid_y:
                    segs.append((cx2 - 1, mid_y, 2, ty2 - mid_y, col))

        # Build Day divider y-positions
        day_bands = []
        for r, lbls in sorted(days_map.items()):
            band_y = TREE_Y0 + r * ROW_PITCH
            day_bands.append((r, band_y, lbls))

        return nodes_out, segs, day_bands, canvas_w, canvas_h


init -1:
    transform fc_here_glow_pulse:
        alpha 0.82
        ease 1.1 alpha 1.0
        ease 1.1 alpha 0.82
        repeat

screen flowchart():
    tag menu

    $ active_here_id = current_fc_node_id if (not main_menu and current_fc_node_id) else None
    default current_view = "all"
    default selected_id = (current_fc_node_id if (not main_menu and current_fc_node_id) else "com_00")

    $ sel_node = get_flowchart_node(selected_id)
    $ sel_unlocked = is_fc_node_unlocked(sel_node)
    $ is_sel_here = bool(active_here_id and sel_node["id"] == active_here_id)
    $ is_sel_eclipse = (sel_node["id"] == "ext_07")
    $ is_sel_ending = (sel_node["id"] in ("arc_09", "arc_10", "ciel_06", "ciel_07", "aki_08", "aki_09", "his_06", "his_07", "koh_06"))
    $ _, _, _, au, at, ap = get_fc_stats("all")
    $ cleared_cnt = get_cleared_endings_count()
    $ tree_nodes, tree_segs, day_bands, canvas_w, canvas_h = get_fc_view_layout(current_view)
    $ lane_hdrs = FC_LANE_HEADERS.get(current_view, [])
    $ init_y_frac = get_fc_initial_yfrac(current_view, active_here_id) if active_here_id else 0.0

    # Softened Frosted-Mist Tsukihime-R Flowchart Backdrop
    add "gui/flowchart_bg.webp"

    # --------------------------------------------------------------------------
    # Soft Minimalist Capsule Header (Exact Plan A Frosted Mist!)
    # --------------------------------------------------------------------------
    fixed:
        xpos 0
        ypos 0
        xsize 1920
        ysize 70
        add Solid("#0d1119d8", xsize=1920, ysize=70)
        add Solid("#dce8f51c", xsize=1920, ysize=1) yalign 1.0

        hbox:
            xpos 36
            yalign 0.5
            xsize 1848

            hbox:
                spacing 24
                yalign 0.5
                hbox:
                    spacing 12
                    yalign 0.5
                    text ui_tr("物语图谱", "Flowchart") size 24 color "#eef4fa" font "fonts/lxgw_xihei_screen.ttf" yalign 0.5
                    if not is_ui_en():
                        text "FLOWCHART" size 12 color "#8fa5bc" font "fonts/lxgw_xihei.ttf" kerning 2 yalign 0.56

                frame:
                    background Frame("gui/mist/seg_track.png", 26, 22)
                    padding (5, 4)
                    hbox:
                        spacing 4
                        for vid, vlbl_zh, vlbl_en in FC_VIEW_TABS:
                            $ is_v = (current_view == vid)
                            button:
                                action SetScreenVariable("current_view", vid)
                                ysize 34
                                background (Frame("gui/mist/pill_active.png", 18, 14) if is_v else None)
                                hover_background (Frame("gui/mist/pill_active.png", 18, 14) if is_v else Frame("gui/mist/pill_hover.png", 18, 14))
                                padding (16, 0)
                                text ui_tr(vlbl_zh, vlbl_en) size 14 color ("#ffffff" if is_v else "#9eb0c4") font ("fonts/lxgw_xihei_screen.ttf" if is_v else "fonts/lxgw_xihei.ttf") yalign 0.5

            hbox:
                xalign 1.0
                yalign 0.5
                spacing 14

                if active_here_id:
                    button:
                        action [SetScreenVariable("current_view", "all"), SetScreenVariable("selected_id", active_here_id), Function(fc_scroll_to_node, "all", active_here_id)]
                        ysize 38
                        background Frame("gui/mist/pill_mint.png", 18, 14)
                        hover_background Frame("gui/mist/pill_hover.png", 18, 14)
                        padding (16, 0)
                        hbox:
                            yalign 0.5
                            spacing 7
                            add "gui/mist/dot_mint.png" yalign 0.5
                            text ui_tr("定位当前", "Locate") size 13 color "#d4f7ea" font "fonts/lxgw_xihei_screen.ttf" yalign 0.5

                button:
                    action [SetScreenVariable("current_view", "all"), SetScreenVariable("selected_id", "ext_07"), Function(fc_scroll_to_node, "all", "ext_07")]
                    ysize 38
                    background (Frame("gui/mist/pill_gold.png", 18, 14) if is_tsukishoku_unlocked() else Frame("gui/mist/pill_idle.png", 18, 14))
                    hover_background Frame("gui/mist/pill_hover.png", 18, 14)
                    padding (16, 0)
                    hbox:
                        yalign 0.5
                        spacing 7
                        add ("gui/mist/dot_gold.png" if is_tsukishoku_unlocked() else "gui/mist/dot_dim.png") yalign 0.5
                        text (ui_tr("月蝕 · 已解锁", "Eclipse · Open") if is_tsukishoku_unlocked() else ui_tr("月蝕 · 待解锁", "Eclipse · Locked")) size 13 color ("#f7e6b8" if is_tsukishoku_unlocked() else "#96a8bc") font "fonts/lxgw_xihei_screen.ttf" yalign 0.5

                text (f"Endings {cleared_cnt}/9 · Nodes {au}/{at}" if is_ui_en() else f"结局 {cleared_cnt}/9 · 节点 {au}/{at}") size 13 color "#95a8bd" font "fonts/lxgw_xihei.ttf" yalign 0.5

                button:
                    id "fc_return_btn"
                    action Return()
                    ysize 38
                    background Frame("gui/mist/pill_idle.png", 18, 14)
                    hover_background Frame("gui/mist/pill_hover.png", 18, 14)
                    padding (18, 0)
                    text ui_tr("返回", "Back") size 14 color "#d6e2ef" hover_color "#ffffff" font "fonts/lxgw_xihei.ttf" yalign 0.5

    # Sticky Route Lane Column Headers
    fixed:
        xpos 0
        ypos 70
        xsize 1360
        ysize 34
        add Solid("#0c1018c8", xsize=1360, ysize=34)
        add Solid("#dce8f514", xsize=1360, ysize=1) yalign 1.0

        text ui_tr("天数 / 章节", "Day / Chapter") xpos 256 xanchor 1.0 yalign 0.5 size 12 color "#75889e" font "fonts/lxgw_xihei.ttf"

        for lcol, llbl_zh, llbl_en, lcol_hex in lane_hdrs:
            $ lx = 286 + lcol * 164 + 66
            text ui_tr(llbl_zh, llbl_en) xpos lx xanchor 0.5 yalign 0.5 size 13 color lcol_hex font "fonts/lxgw_xihei_screen.ttf"

    # --------------------------------------------------------------------------
    # LEFT CANVAS: Tsukihime R Top-to-Bottom Chronological Tree (Softened!)
    # --------------------------------------------------------------------------
    viewport:
        id "fc_vp"
        xpos 0
        ypos 104
        xsize 1360
        ysize 976
        yinitial init_y_frac
        scrollbars "vertical"
        mousewheel True
        draggable True
        pagekeys True

        fixed:
            xsize canvas_w
            ysize canvas_h

            # Layer 1: Soft Mist-Blue Day Dividers & Right-Aligned Day Titles
            for r_idx, band_y, day_lbls in day_bands:
                if r_idx > 0:
                    add "gui/fc_day_line.png" xpos 12 ypos (band_y - 16)

                vbox:
                    xpos 256
                    xanchor 1.0
                    ypos (band_y + 4)
                    spacing 4
                    for dl_i, dl_txt in enumerate(day_lbls):
                        text dl_txt:
                            xalign 1.0
                            size (19 if dl_i == 0 else 14)
                            color ("#eef4fa" if dl_i == 0 else "#93a6bc")
                            font ("fonts/lxgw_xihei_screen.ttf" if dl_i == 0 else "fonts/lxgw_xihei.ttf")

            # Layer 2: Crisp Orthogonal Connector Lines
            for sx, sy, sw, sh, scol in tree_segs:
                add Solid(scol, xsize=sw, ysize=sh) xpos sx ypos sy

            # Layer 3: Compact Scene Thumbnail Nodes with Luminous Current-Node & Selection Glow!
            for nid, node, nx, ny, nw, nh in tree_nodes:
                $ nu = is_fc_node_unlocked(node)
                $ is_sel = (selected_id == nid)
                $ is_here = bool(active_here_id and nid == active_here_id)
                $ is_ecl = (nid == "ext_07")
                $ badge = (FC_ENDING_BADGES_EN.get(nid, FC_ENDING_BADGES.get(nid, "")) if is_ui_en() else FC_ENDING_BADGES.get(nid, ""))

                if is_here:
                    add Frame("gui/mist/fc_here_halo.png", 26, 26) at fc_here_glow_pulse xpos (nx - 14) ypos (ny - 14) xsize (nw + 28) ysize (nh + 28)
                elif is_sel:
                    add Frame("gui/mist/fc_sel_halo.png", 26, 26) xpos (nx - 14) ypos (ny - 14) xsize (nw + 28) ysize (nh + 28)

                button:
                    action SetScreenVariable("selected_id", nid)
                    xpos nx
                    ypos ny
                    xsize nw
                    ysize nh
                    background Solid("#0c1018")
                    hover_background Solid("#1c283a")
                    padding (0, 0)

                    fixed:
                        xfill True
                        yfill True

                        if nu:
                            $ _iw = nw - 4
                            $ _ih = nh - 4
                            $ _crop_h = min(1.0, (4.0 / 3.0) / (float(_iw) / float(_ih)))
                            add Transform(node["thumb"], crop=(0.0, 0.08, 1.0, _crop_h), crop_relative=True, xysize=(_iw, _ih)) xalign 0.5 yalign 0.5
                        else:
                            add Solid("#0f141e", xsize=(nw - 4), ysize=(nh - 4)) xalign 0.5 yalign 0.5
                            add Transform("gui/icons/lock.png", zoom=0.45) xalign 0.5 yalign 0.5

                        # High-Contrast Current Position Pill (readable even over bright sunset/snow!)
                        if is_here:
                            frame:
                                xpos 5
                                ypos 5
                                background Frame("gui/mist/pill_mint.png", 10, 8)
                                padding (8, 2)
                                hbox:
                                    spacing 5
                                    yalign 0.5
                                    add "gui/mist/dot_mint.png" yalign 0.5
                                    text ui_tr("当前", "Here") size 11 color "#f0fff9" font "fonts/lxgw_xihei_screen.ttf" yalign 0.5

                        if badge:
                            $ b_txt_col = "#f7e6b8" if is_ecl else ("#ebd49a" if badge == "TRUE" else ("#cbbcf0" if badge == "NORMAL" else "#a8cceb"))
                            frame:
                                xalign 0.96
                                yalign 0.94
                                background Frame("gui/mist/quick_pill.png", 10, 8)
                                padding (7, 2)
                                text badge size 10 color b_txt_col font "fonts/lxgw_xihei_screen.ttf"

                        # Crisp Luminous Foreground Rim drawn ON TOP of thumbnail!
                        $ b_col = "#96f5d6" if is_here else ("#a6d8ff" if is_sel else ("#dec894cc" if (is_ecl and nu) else ("#c4b082aa" if nu else "#3a4658")))
                        $ b_thk = 3 if (is_here or is_sel) else (2 if is_ecl else 1)
                        add Solid(b_col, xsize=nw, ysize=b_thk) yalign 0.0
                        add Solid(b_col, xsize=nw, ysize=b_thk) yalign 1.0
                        add Solid(b_col, xsize=b_thk, ysize=nh) xalign 0.0
                        add Solid(b_col, xsize=b_thk, ysize=nh) xalign 1.0

    # --------------------------------------------------------------------------
    # RIGHT FLOATING CARD: Softened Frosted-Mist Tsukihime-R "Note." Preview Card
    # --------------------------------------------------------------------------
    frame:
        xpos 1384
        ypos 136
        xsize 500
        ysize 764
        background Frame("gui/mist/modal.png", 28, 28)
        padding (14, 14)

        vbox:
            xsize 472
            spacing 0

            # 1. Scene Artwork Preview + Soft Angled Ribbon
            fixed:
                xsize 472
                ysize 296
                add Solid("#0c1018", xsize=472, ysize=296)

                if sel_unlocked:
                    add Transform(sel_node["thumb"], crop=(0.0, 0.05, 1.0, 0.8333), crop_relative=True, xysize=(472, 296)) xalign 0.5 yalign 0.5
                else:
                    vbox:
                        xalign 0.5
                        yalign 0.5
                        spacing 12
                        add Transform("gui/icons/lock.png", zoom=0.84) xalign 0.5
                        text ui_tr("命运之线尚未探明", "Locked Scenario Node") size 16 color "#7c90a6" font "fonts/lxgw_xihei.ttf" xalign 0.5

                add "gui/fc_ribbon.png" xpos 344 ypos 0
                $ ribbon_txt = ui_tr("当前进度", "Current") if is_sel_here else (ui_tr("月蝕终章", "Eclipse") if is_sel_eclipse else (ui_tr("结局节点", "Ending") if is_sel_ending else (ui_tr("本场景", "Scene") if sel_unlocked else ui_tr("未解锁", "Locked"))))
                text ribbon_txt xpos 416 xanchor 0.5 ypos 5 size 13 color ("#d8ffef" if is_sel_here else "#eef4fa") font "fonts/lxgw_xihei_screen.ttf"

            # 2. Soft Mist-Slate "Note." Divider Strip
            fixed:
                xsize 472
                ysize 30
                add Solid("#3d597d", xsize=472, ysize=30)
                text "Note." xpos 16 yalign 0.5 size 15 color "#ffffff" font "fonts/lora_reg.ttf"
                text (sel_node["sub"].split("·")[0].strip() if is_ui_en() else sel_node["day"]) xalign 0.96 yalign 0.5 size 12 color "#d8e6f5" font "fonts/lxgw_xihei.ttf"

            # 3. Clean Soft Pearl-White Paper Body
            fixed:
                xsize 472
                ysize 340
                add Solid("#f4f7fa", xsize=472, ysize=340)

                vbox:
                    xpos 24
                    ypos 20
                    xsize 424
                    spacing 13

                    vbox:
                        spacing 3
                        if sel_unlocked:
                            text (sel_node["sub"] if is_ui_en() else sel_node["title"]) size (19 if is_ui_en() else 22) color "#1a2433" font "fonts/lxgw_xihei_screen.ttf"
                            text (sel_node["title"] if is_ui_en() else sel_node["sub"]) size 12 color "#58708c" font "fonts/lxgw_xihei.ttf"
                        else:
                            text ui_tr("？？？ · 未探明章节", "??? · Locked Chapter") size 21 color "#5a697c" font "fonts/lxgw_xihei_screen.ttf"
                            text "LOCKED SCENARIO NODE" size 12 color "#8796a8" font "fonts/lxgw_xihei.ttf"

                    text ((f"Branch target: {sel_node['branch_label']}  ·  Reach this scene in-game or jump directly from this timeline node." if is_ui_en() else sel_node["desc"]) if sel_unlocked else ui_tr("此处深埋着尚未探明的因果脉络。在正篇中亲历对应分支后，即可驱散迷雾并随时从此跃迁。", "Reach this branch during normal gameplay to unlock direct timeline jumping.")):
                        size 16
                        color "#2a3748"
                        font "fonts/lxgw_xihei.ttf"
                        line_spacing 7

                    add Solid("#d6dfe9", xsize=424, ysize=1)

                    vbox:
                        spacing 6
                        hbox:
                            spacing 8
                            text ui_tr("出场", "Cast") size 13 color "#3d597d" font "fonts/lxgw_xihei_screen.ttf"
                            text ((fc_translate_cast(sel_node["cast"]) if is_ui_en() else sel_node["cast"]) if sel_unlocked else "—") size 13 color "#46586e" font "fonts/lxgw_xihei.ttf"

                        text ((f"Node ID: {sel_node['id']}  ·  Mode: {sel_node['mode']}" if is_ui_en() else sel_node["branch_info"]) if sel_unlocked else ui_tr("前置分支尚未触发。", "Prerequisite branch not yet reached.")) size 13 color "#5a6c82" font "fonts/lxgw_xihei.ttf" line_spacing 4

            null height 14

            # 4. Soft Rounded Capsule Jump Action Button
            if sel_unlocked:
                $ jump_lbl = ui_tr("开启「月蝕」隐藏终章", "Play ECLIPSE Epilogue") if is_sel_eclipse else (ui_tr("从此节点跃迁续玩", "Jump to This Branch") if sel_node["mode"] == "continue" else ui_tr("观看知得留课堂", "Watch Ciel-Sensei Lesson"))
                button:
                    id "fc_jump_btn"
                    action (
                        Confirm(ui_tr("确定要跃迁至该章节并重置当前未保存进度吗？", "Jump to this chapter?\nUnsaved progress will be lost."), [
                            SetVariable("flowchart_target_node_id", sel_node["id"]),
                            Start("flowchart_jump_dispatcher"),
                        ]) if not main_menu else [
                            SetVariable("flowchart_target_node_id", sel_node["id"]),
                            Start("flowchart_jump_dispatcher"),
                        ]
                    )
                    activate_sound "audio/ui_choice.wav"
                    xsize 472
                    ysize 50
                    background (Frame("gui/mist/pill_gold.png", 22, 18) if is_sel_eclipse else Frame("gui/mist/pill_active.png", 22, 18))
                    hover_background Frame("gui/mist/pill_hover.png", 22, 18)
                    text jump_lbl size 16 color ("#fff5d8" if is_sel_eclipse else "#ffffff") font "fonts/lxgw_xihei_screen.ttf" xalign 0.5 yalign 0.5
            else:
                frame:
                    xsize 472
                    ysize 50
                    background Frame("gui/mist/pill_idle.png", 22, 18)
                    text ui_tr("需在正篇中亲历此分支后方可跃迁", "Unlock in main story to jump here") size 14 color "#7e90a6" font "fonts/lxgw_xihei.ttf" xalign 0.5 yalign 0.5

    text ui_tr("滚轮或拖动浏览五线时间轴 · 点击缩略图查看「Note.」简报，全五线通关汇入「月蝕」", "Scroll or drag timeline · Click any unlocked node to inspect and jump"):
        xpos 1392
        ypos 916
        xsize 484
        size 12
        color "#778ba2"
        font "fonts/lxgw_xihei.ttf"
        line_spacing 5

    key "K_ESCAPE" action Return()
    key "game_menu" action Return()
