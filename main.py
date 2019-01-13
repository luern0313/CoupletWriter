import jieba, random, json

global infile, outfile, zishi, writemode
try:
    with open("zknow.txt", "r", encoding='utf-8') as zishi_file:
        zishi = json.loads(zishi_file.read())
except IOError:
    zishi = {}

def learns():
    global infile, outfile, zishi
    size = len(infile)
    for i in range(size):
        if i % 2000 == 0:
            print(" 学习进度：" + str(i) + "/" + str(size) + "，" + str(i / size * 100) + "%")
        cut = jieba.lcut(infile[i])
        for j in range(len(cut)):
            position = infile[i].find(cut[j])
            learn(cut[j], outfile[i][position: position + len(cut[j])])
        for j in range(len(infile[i])):
            learn(infile[i][j], outfile[i][j])


# 单个的词语学习
def learn(word, nword):
    global zishi
    zikey = zishi.keys()
    if word in zikey:
        zishikey = zishi[word].keys()
        if nword in zishikey:
            for j in zishikey:
                if j != '$':
                    if j != nword:
                        zishi[word][j] = zishi[word][j] / (1 + 1 / zishi[word]['$'])
            zishi[word][nword] = (zishi[word][nword] + 1 / zishi[word]['$']) / (1 + 1 / zishi[word]['$'])
            zishi[word]['$'] = zishi[word]['$'] + 1
        else:
            for j in zishikey:
                if j != '$':
                    zishi[word][j] = zishi[word][j] / (1 + 1 / zishi[word]['$'])
            zishi[word][nword] = (1 / zishi[word]['$']) / (1 + 1 / zishi[word]['$'])
            zishi[word]['$'] = zishi[word]['$'] + 1
    else:
        zishi[word] = {'$': 1, nword: 1}


def couplet(s):
    x = []
    for i in range(len(s)):
        x.append(ran(s[i], random.random()))
    return "".join(x)


def ran(w, r):
    global zishi, writemode
    zikey = zishi.keys()
    if w != '' and w in zikey:
        zishikey = zishi[w].keys()
        max = ["", 0.0]
        for i in zishikey:
            if i != '$':
                if writemode == 1:
                    if r < float(zishi[w][i]):
                        return i
                    else:
                        r = r - float(zishi[w][i])
                elif writemode == 2:
                    if float(zishi[w][i]) > max[1]:
                        max[0] = i
                        max[1] = float(zishi[w][i])
        return max[0]
    else:
        return "".join([ran(i, random.random()) for i in w])


while True:
    print("学习/对对联")
    choose = input()
    if choose == "学习":
        print(" 正在读取...")
        with open("couplet/train/in.txt", "rt", encoding='utf-8') as zishi_file:
            infile = zishi_file.read().split("\n")
        with open("couplet/train/out.txt", "rt", encoding='utf-8') as zishi_file:
            outfile = zishi_file.read().split("\n")
        print(" 读取完成，开始学习")
        learns()
        with open("zknow.txt", "wt", encoding='utf-8') as out_file:
            out_file.write(str(zishi))
        print("学习完成")
    elif choose == "对对联":
        writemode = int(input("输入生成对联模式，1为随机模式，2为固定模式"))
        while True:
            try:
                s = input("输入上联：")
                s = jieba.lcut(s)
                print("-----------------------------------")
                print("上联：" + "".join(s))
                print("下联：" + couplet(s))
                print("-----------------------------------")
                print("")
            except Exception:
                print("出错")
    elif choose == "调试":
        while True:
            print(jieba.lcut(input()))