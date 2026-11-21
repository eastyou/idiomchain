"""成语接龙：词库、接龙搜索与练习纸题目。"""

from __future__ import annotations

import random
import re
from dataclasses import dataclass
from typing import Dict, List, Optional, Sequence, Tuple

MAX_LENGTH = 8
MIN_LENGTH = 2
DEFAULT_LENGTH = 4

IDIOM_TEXT = """
一心一意|心思专一，没有杂念
意气风发|精神振奋，气概昂扬
发扬光大|使优良传统更加发展壮大
大公无私|一心为公，毫无私心
私心杂念|为个人打算的各种念头
念念不忘|牢记在心，时刻不忘
忘乎所以|因得意而忘记一切
以德报怨|用恩德回报怨恨
怨天尤人|遇到挫折只责怪别人
人山人海|形容聚集的人极多
海阔天空|形容广阔无边或说话漫无边际
空前绝后|以前没有，以后也不会有
后来居上|后起的超过先前的
上行下效|上面怎么做，下面就跟着学
天下太平|国家安定，没有战乱
平易近人|态度和蔼，容易接近
人定胜天|人的力量可以战胜自然
天马行空|比喻才思豪放，不受拘束
空谷足音|比喻难得的音信或言论
天人合一|人与自然相互统一的观念
一举成名|一次行动就出了名
名列前茅|名次排在前面
茅塞顿开|一下子想通了
开卷有益|读书总有好处
益寿延年|增加寿命
年富力强|年纪轻，精力旺盛
强词夺理|本来没理却硬要争辩
理直气壮|理由充分，说话有底气
壮志凌云|志向远大
云淡风轻|形容天气晴好或心境淡然
轻描淡写|说话写文章轻轻带过
风平浪静|没有风浪，比喻平静无事
静观其变|冷静地观察事情变化
变化无常|变化多端，没有规律
常来常往|经常来往
风和日丽|微风和暖，阳光明媚
风调雨顺|风雨适合农时
顺水推舟|顺着形势办事
舟车劳顿|旅途疲劳
水到渠成|条件成熟，事情自然成功
成千上万|形容数量极多
万无一失|绝对不会出差错
失之交臂|擦肩而过，错过机会
水落石出|真相完全显露
出人头地|超出一般人
地大物博|土地辽阔，物产丰富
博学多才|学问广博，才能多样
才高八斗|形容文才极高
斗志昂扬|斗争的意志高涨
扬眉吐气|摆脱压抑，心情舒畅
气壮山河|气概豪迈
河清海晏|天下太平
目不暇接|东西太多，看不过来
接二连三|一个接一个
三心二意|犹豫不决，不专心
意味深长|含蓄深刻，耐人寻味
长驱直入|迅速地向远方挺进
入木三分|形容见解或描写深刻
分秒必争|一分一秒也不放过
争分夺秒|抓紧时间
两全其美|做一件事顾全两方面
美不胜收|美好的东西太多，看不过来
学以致用|把学到的用到实际中
用兵如神|指挥作战极其灵活
神清气爽|形容头脑清醒，心情舒畅
温故知新|复习旧知识，得到新体会
新陈代谢|新事物取代旧事物
博古通今|通晓古今
今非昔比|现在不是过去能比的
比翼双飞|比喻夫妻恩爱，共同前进
飞黄腾达|比喻官职升得很快
达官贵人|地位高的人物
人杰地灵|杰出人物出生或到过的地方
灵机一动|突然想出办法
动人心弦|使人内心深受感动
弦外之音|言外之意
一举两得|做一件事得到两方面好处
得心应手|心手相应，运用自如
手忙脚乱|做事慌张，没有条理
乱七八糟|形容混乱不堪
一鸣惊人|平时不显眼，一下子做出惊人成绩
人云亦云|别人怎么说就跟着怎么说
云开见日|比喻黑暗过去，光明到来
日新月异|每天每月都有新变化
异想天开|想法离奇，不切实际
开门见山|说话写文章直截了当
山穷水尽|陷入绝境
尽善尽美|十分完美
美中不足|大体很好，还有缺陷
足智多谋|智谋很多，善于谋划
谋事在人|事情要靠人去谋划
人尽其才|每个人都能充分发挥才能
才华横溢|很有才华
一帆风顺|非常顺利
顺理成章|写文章或做事合乎条理
一见如故|初次见面就像老朋友
故步自封|安于现状，不求进步
一望无际|一眼看不到边
生龙活虎|形容活泼有力
虎头蛇尾|开始声势大，后来劲头小
花好月圆|比喻美好圆满
圆满成功|事情顺利完成
功成名就|功业建立了，名声也有了
就事论事|只就事情本身来讨论
事半功倍|用力小而收效大
倍道兼行|加快速度前进
行云流水|自然流畅，不受拘束
水天一色|水天相连，景色开阔
马到成功|很快就取得成功
大器晚成|大才需要长期磨练才能成就
成家立业|成了家，建立了事业
业精于勤|学业靠勤奋才能精深
勤能补拙|勤奋能弥补天资不足
大同小异|大体相同，略有差异
大显身手|充分展示本领
手到擒来|毫不费力就办成
来日方长|未来的日子还很长
长话短说|把长话简短地说
说一不二|说话算数，说到做到
二话不说|不说什么，立刻行动
说三道四|随意评论，乱加议论
四面楚歌|陷入孤立无援的境地
歌舞升平|太平盛世，一片欢庆
平步青云|一下子升到高位
云消雾散|事物消失干净
不耻下问|向学问不如自己的人请教
问心无愧|自问没有对不起人的地方
不约而同|没有约定而彼此一致
同心协力|齐心合力
力挽狂澜|尽力挽回险恶局势
不劳而获|自己不劳动却占有别人成果
不言而喻|不用说就能明白
不由自主|控制不住自己
由表及里|从表面到内部
里应外合|内外配合
合情合理|合乎情理
理所当然|按道理应当这样
百发百中|每次都能命中目标
中流砥柱|能起支柱作用的人或力量
百折不挠|意志坚强，不屈服
千方百计|想尽一切办法
计上心来|突然想出计策
来者不拒|对来的人或事一概不拒绝
千军万马|形容雄壮的队伍
万象更新|一切事物都变得焕然一新
自强不息|自己努力向上，永不停息
息息相关|关系非常密切
关怀备至|关心得十分周到
至理名言|最正确、最有价值的话
言而有信|说话算数，讲信用
信口开河|随口乱说
自由自在|不受拘束，安闲舒适
在所不辞|决不推辞
辞旧迎新|告别旧岁，迎接新年
自言自语|自己跟自己说话
语重心长|言辞诚恳，情意深长
长年累月|形容经历很多年月
月下老人|指媒人
耳聪目明|听觉视觉都灵敏
明察秋毫|目光敏锐，能看清细微之处
毫不犹豫|一点也不迟疑
目不斜视|眼睛不往旁边看
视死如归|把死看得像回家一样
归心似箭|想回家的心情十分急切
箭在弦上|形势所迫，不得不做
上下其手|暗中玩弄手法作弊
手足无措|慌慌张张，不知怎么办
高瞻远瞩|眼光远大
高枕无忧|安稳睡觉，不必担忧
忧国忧民|为国家人民而忧虑
心平气和|心情平静，态度温和
和蔼可亲|态度温和，容易接近
亲力亲为|事情亲自去做
为所欲为|想做什么就做什么
为人师表|在品德学问上作别人的榜样
表里如一|外表和内心一致
一往无前|不怕困难，奋勇前进
前程似锦|前途十分美好
锦上添花|在美好的基础上再添美好
花团锦簇|形容五彩缤纷，十分华丽
心花怒放|心情极其愉快
放虎归山|放走敌人，留下祸患
山明水秀|山水景色清秀
秀外慧中|外表秀美，内心聪慧
见多识广|见过的多，知道的广
广开言路|尽量给人们发表意见的机会
路不拾遗|社会风气良好
遗臭万年|坏名声永远流传
年深日久|时间很久
久别重逢|分别很久后再次相见
逢凶化吉|遇到凶险转化为吉祥
吉星高照|运气很好
照本宣科|照着本子念，缺乏创造
有条不紊|有条理，一点不乱
有备无患|事先有准备就不会有祸患
患得患失|对得失斤斤计较
失道寡助|违背道义的人得不到支持
助人为乐|把帮助别人当作快乐
乐不思蜀|快乐得不想回去
蜀犬吠日|少见多怪
日积月累|一天天积累
有目共睹|大家都看得见
睹物思人|看到东西就想起人
有机可乘|有空子可以利用
乘胜追击|趁着胜利继续追击
无中生有|凭空捏造
有口皆碑|人人称赞
无微不至|关怀照顾非常细致
无独有偶|虽然少见，却不止一个
名副其实|名声或名义与实际相符
实事求是|按照实际情况办事
是非曲直|事情的对错
直言不讳|直率地说出，没有顾忌
事与愿违|事情的发展跟愿望相反
违心之论|违背本心的话
论功行赏|按功劳大小给奖赏
赏心悦目|看到美好景物而心情舒畅
目瞪口呆|受惊而发愣的样子
呆若木鸡|因恐惧或惊讶而发愣
鸡犬不宁|被搅扰得不得安宁
宁死不屈|宁可死也不屈服
屈指可数|数量很少
数不胜数|数量极多，数不过来
数一数二|名列前茅
"""


class IdiomError(ValueError):
    """成语接龙相关的输入错误。"""


def _load_idioms(text: str) -> Dict[str, str]:
    table: Dict[str, str] = {}
    for line in text.strip().splitlines():
        line = line.strip()
        if not line:
            continue
        word, _, meaning = line.partition("|")
        word = word.strip()
        meaning = meaning.strip()
        if not word or not meaning:
            raise IdiomError("词库格式错误：%s" % line)
        if word in table:
            raise IdiomError("词库存在重复成语：%s" % word)
        table[word] = meaning
    return table


IDIOMS: Dict[str, str] = _load_idioms(IDIOM_TEXT)

FIRST_INDEX: Dict[str, List[str]] = {}
LAST_INDEX: Dict[str, List[str]] = {}
for _word in sorted(IDIOMS):
    FIRST_INDEX.setdefault(_word[0], []).append(_word)
    LAST_INDEX.setdefault(_word[-1], []).append(_word)
del _word

_IDIOM_RE = re.compile(r"^[\u4e00-\u9fff]{4}$")


def is_idiom(word: str) -> bool:
    """判断是否为词库中收录的四字成语。"""
    return isinstance(word, str) and word in IDIOMS


def is_idiom_word(word: str) -> bool:
    """判断是否为四个汉字的词语（不要求收录在词库中）。"""
    return isinstance(word, str) and bool(_IDIOM_RE.match(word))


def idioms_starting(char: str) -> List[str]:
    """返回以指定汉字开头的成语，按字典序排列。"""
    if not isinstance(char, str) or len(char) != 1:
        raise IdiomError("请提供单个汉字")
    return list(FIRST_INDEX.get(char, ()))


def idioms_ending(char: str) -> List[str]:
    """返回以指定汉字结尾的成语，按字典序排列。"""
    if not isinstance(char, str) or len(char) != 1:
        raise IdiomError("请提供单个汉字")
    return list(LAST_INDEX.get(char, ()))


def next_idioms(idiom: str) -> List[str]:
    """返回可以接在指定成语之后的成语。"""
    check_idiom(idiom)
    return idioms_starting(idiom[-1])


def previous_idioms(idiom: str) -> List[str]:
    """返回可以接在指定成语之前的成语。"""
    check_idiom(idiom)
    return idioms_ending(idiom[0])


def check_idiom(idiom: str) -> None:
    if not isinstance(idiom, str) or not idiom:
        raise IdiomError("成语不能为空")
    if not is_idiom_word(idiom):
        raise IdiomError("请输入四字成语：%s" % idiom)
    if idiom not in IDIOMS:
        raise IdiomError("词库中没有成语：%s" % idiom)


def is_chain(chain: Sequence[str], require_known: bool = False) -> bool:
    """判断是否为合法接龙：首尾相接、四字成语、不重复。"""
    if isinstance(chain, (str, bytes)) or not isinstance(chain, (list, tuple)):
        return False
    if not chain:
        return False
    seen = set()
    previous: Optional[str] = None
    for word in chain:
        if not is_idiom_word(word):
            return False
        if require_known and word not in IDIOMS:
            return False
        if word in seen:
            return False
        if previous is not None and word[0] != previous[-1]:
            return False
        seen.add(word)
        previous = word
    return True


def _random_chain(start: str, length: int, rng: random.Random) -> Optional[List[str]]:
    chain = [start]
    used = {start}

    def walk() -> bool:
        if len(chain) == length:
            return True
        candidates = [word for word in FIRST_INDEX.get(chain[-1][-1], ()) if word not in used]
        rng.shuffle(candidates)
        for word in candidates:
            chain.append(word)
            used.add(word)
            if walk():
                return True
            chain.pop()
            used.discard(word)
        return False

    return chain if walk() else None


def build_chain(
    start: str,
    length: int = DEFAULT_LENGTH,
    seed: Optional[int] = None,
    attempts: int = 60,
) -> List[str]:
    """从指定成语开始，随机构造一条指定长度的接龙。"""
    check_idiom(start)
    check_length(length)
    rng = random.Random(seed)
    for _ in range(attempts):
        found = _random_chain(start, length, rng)
        if found is not None:
            return found
    raise IdiomError("无法从「%s」接出 %d 个成语" % (start, length))


def check_length(length: int) -> None:
    if isinstance(length, bool) or not isinstance(length, int):
        raise IdiomError("接龙长度必须是整数")
    if length < MIN_LENGTH or length > MAX_LENGTH:
        raise IdiomError("接龙长度需在 %d 到 %d 之间" % (MIN_LENGTH, MAX_LENGTH))


def find_chains(start: str, length: int = DEFAULT_LENGTH, limit: int = 20) -> List[List[str]]:
    """按字典序搜索从指定成语出发的全部接龙，最多返回 limit 条。"""
    check_idiom(start)
    check_length(length)
    if isinstance(limit, bool) or not isinstance(limit, int) or limit < 1:
        raise IdiomError("返回数量必须是正整数")
    results: List[List[str]] = []
    chain = [start]
    used = {start}

    def walk() -> None:
        if len(results) >= limit:
            return
        if len(chain) == length:
            results.append(list(chain))
            return
        for word in FIRST_INDEX.get(chain[-1][-1], ()):
            if word in used:
                continue
            chain.append(word)
            used.add(word)
            walk()
            chain.pop()
            used.discard(word)
            if len(results) >= limit:
                return

    walk()
    return results


def normalize_chain(text: str) -> List[str]:
    """把用箭头、空格或标点分隔的答案拆成成语列表。"""
    if not isinstance(text, str):
        return []
    parts = re.split(r"[\s,，、;；\-—>→|/]+", text.strip())
    return [part for part in parts if part]


def _reaches(start: str, length: int) -> bool:
    chain = [start]
    used = {start}

    def walk() -> bool:
        if len(chain) == length:
            return True
        for word in FIRST_INDEX.get(chain[-1][-1], ()):
            if word in used:
                continue
            chain.append(word)
            used.add(word)
            if walk():
                return True
            chain.pop()
            used.discard(word)
        return False

    return walk()


_SOLVABLE: Dict[int, List[str]] = {}


def solvable_starts(length: int = DEFAULT_LENGTH) -> List[str]:
    """返回能够接出指定长度的成语列表，按字典序排列。"""
    check_length(length)
    if length not in _SOLVABLE:
        _SOLVABLE[length] = [word for word in sorted(IDIOMS) if _reaches(word, length)]
    return list(_SOLVABLE[length])


@dataclass(frozen=True)
class WorksheetItem:
    """一道接龙题：给出起始成语，要求接出指定数量。"""

    start: str
    length: int = DEFAULT_LENGTH

    @property
    def meaning(self) -> str:
        return IDIOMS[self.start]

    @property
    def answer(self) -> List[str]:
        return build_chain(self.start, self.length, seed=0)

    @property
    def answer_text(self) -> str:
        return " → ".join(self.answer)


def check_answer(item: WorksheetItem, text: str) -> bool:
    """校验学生的接龙答案：起点、长度与首尾相接均正确。"""
    if not isinstance(item, WorksheetItem):
        return False
    words = normalize_chain(text)
    if len(words) != item.length:
        return False
    if not words or words[0] != item.start:
        return False
    return is_chain(words)


def build_worksheet(
    count: int = 12,
    length: int = DEFAULT_LENGTH,
    seed: Optional[int] = None,
) -> List[WorksheetItem]:
    """随机抽取若干道接龙题，保证每题都有解。"""
    if isinstance(count, bool) or not isinstance(count, int) or count < 1:
        raise IdiomError("题目数量必须是正整数")
    check_length(length)
    pool = solvable_starts(length)
    if count > len(pool):
        raise IdiomError("可用题目不足 %d 道" % count)
    rng = random.Random(seed)
    chosen = rng.sample(pool, count)
    return [WorksheetItem(start=word, length=length) for word in chosen]


def chain_stats(length: int = DEFAULT_LENGTH) -> Tuple[int, int]:
    """返回（可出题数量，词库总数）。"""
    return len(solvable_starts(length)), len(IDIOMS)
