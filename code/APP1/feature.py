from 特征提取 import utils
# 去除列表中重复元素，同时保持相对顺序不变
def remove_duplicate_elements(l):
    new_list = []
    for i in l:
        if i not in new_list:
            new_list.append(i)
    return new_list


# 将属于同一事件要素的词语合并

def func(file_name):
    words = []  # 保存所有属于事件要素的单词
    element_types = []  # 保存上述单词对应的事件要素类型

    with open(file_name, "r", encoding='utf-8') as f1:
        rows = []
        # 将文本转换成list，方便后续处理
        for line in f1.readlines():
            rows.append(line.strip("\n").split("\t"))

        for index, row in enumerate(rows):
            if "S" in row[-1]:
                # S出现在最后一个位置，说明这是一个单独的事件要素，将其加入words列表
                words.append(row[0])
                element_types.append(row[-1][-1])

            elif "B" in row[-1]:
                # 处理由多个单词组成的事件要素
                words.append(row[0])
                element_types.append(row[-1][-1])
                j = index + 1
                while "I" in rows[j][-1] or "E" in rows[j][-1]:
                    words[-1] += rows[j][0]
                    j += 1
                    if j == len(rows):
                        break

        # 将事件要素进行分类（将words列表中的元素按照类别分成6类）
        T = []  # 事故类型
        K = []  # 罪名
        D = []  # 主次责任
        P = []  # 积极因素（减刑因素）
        N = []  # 消极因素（加刑因素）
        R = []  # 判决结果

        for i in range(len(element_types)):
            if element_types[i] == "T":
                T.append(words[i])
            elif element_types[i] == "K":
                K.append(words[i])
            elif element_types[i] == "D":
                D.append(words[i])
            elif element_types[i] == "P":
                P.append(words[i])
            elif element_types[i] == "N":
                N.append(words[i])
            elif element_types[i] == "R":
                R.append(words[i])

        # 为了防止CRF未能抽取出全部的事件要素，因此使用规则化的方法，从原始文本中直接提取出部分事件要素，作为补充
        case = ""  # case是完整的案件内容
        for idx in range(len(rows)):
            case += rows[idx][0]

        if "无证" in case or "驾驶资格" in case:
            N.append("无证驾驶")
        if "无号牌" in case or "牌照" in case or "无牌" in case:
            N.append("无牌驾驶")
        if "酒" in case:
            N.append("酒后驾驶")
        if "吸毒" in case or "毒品" in case or "毒驾" in case:
            N.append("吸毒后驾驶")
        if "超载" in case:
            N.append("超载")
        if "逃逸" in case or "逃离" in case:
            N.append("逃逸")
        if ("有前科" in case or "有犯罪前科" in case) and (
                "无前科" not in case and "无犯罪前科" not in case):
            N.append("有犯罪前科")

        # 整理抽取结果
        event_elements = dict()  # 用字典存储各类事件要素
        event_elements["事故类型"] = remove_duplicate_elements(T)
        event_elements["罪名"] = remove_duplicate_elements(K)
        event_elements["主次责任"] = remove_duplicate_elements(D)
        event_elements["减刑因素"] = remove_duplicate_elements(P)
        event_elements["加刑因素"] = remove_duplicate_elements(N)
        event_elements["判决结果"] = remove_duplicate_elements(R)

        # 打印出完整的事件要素
        # for key, value in event_elements.items():
        #     print(key, value)

        return event_elements

def get_patterns_from_dict(event_elements):
    """
    将提取出的事件要素转换成特征
    :param event_elements: 字典形式的事件要素
    :return patterns: 字典形式的特征
    """
    patterns = dict()

    # 从事件要素中的"加刑因素"提取出三个特征：01死亡人数、02重伤人数、03轻伤人数
    patterns["01死亡人数"], patterns["02重伤人数"], patterns["03轻伤人数"] = utils.extract_seg(
        "".join(event_elements["加刑因素"]))

    # 从事件要素中的"主次责任"提取出特征：04责任认定
    patterns["04责任认定"] = utils.find_element(event_elements["主次责任"], "全部责任")

    # 从事件要素中的"加刑因素"提取出8个特征
    patterns["05是否酒后驾驶"] = utils.find_element(event_elements["加刑因素"], "酒")
    patterns["06是否吸毒后驾驶"] = utils.find_element(event_elements["加刑因素"], "毒")
    patterns["07是否无证驾驶"] = utils.find_element(event_elements["加刑因素"], "驾驶证", "证")
    patterns["08是否无牌驾驶"] = utils.find_element(event_elements["加刑因素"], "牌照", "牌")
    patterns["09是否不安全驾驶"] = utils.find_element(event_elements["加刑因素"], "安全")
    patterns["10是否超载"] = utils.find_element(event_elements["加刑因素"], "超载")
    patterns["11是否逃逸"] = utils.find_element(event_elements["加刑因素"], "逃逸", "逃离")
    patterns["是否初犯偶犯"] = 1 - int(utils.find_element(event_elements["加刑因素"], "前科"))

    # 从事件要素中的"减刑因素"提取出7个特征
    patterns["12是否抢救伤者"] = utils.find_element(event_elements["减刑因素"], "抢救", "施救")
    patterns["13是否报警"] = utils.find_element(event_elements["减刑因素"], "报警", "自首", "投案")
    patterns["14是否现场等待"] = utils.find_element(event_elements["减刑因素"], "现场", "等候")
    patterns["15是否赔偿"] = utils.find_element(event_elements["减刑因素"], "赔偿")
    patterns["16是否认罪"] = utils.find_element(event_elements["减刑因素"], "认罪")
    patterns["17是否如实供述"] = utils.find_element(event_elements["减刑因素"], "如实")
    if patterns["是否初犯偶犯"] == 0:
        patterns["18是否初犯偶犯"] = "0"
    else:
        patterns["18是否初犯偶犯"] = "1"
    return patterns


def feature(filename):
    dict=func(filename)
    pattern=get_patterns_from_dict(dict)
    return dict,pattern
