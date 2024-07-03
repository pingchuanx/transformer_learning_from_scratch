sentences = [
    "我",
    "喜欢",
    "吃",
    "苹果",
    "他",
    "不",
    "喜欢",
    "吃",
    "苹果派",
    "I like to eat apples",
    "She has a cute cat",
    "you are very cute",
    "give you a hug",
]


# 统计每个词出现的频率并初始化初始词表：
from collections import defaultdict
# 构建频率统计
def build_stats(sentences):
    stats = defaultdict(int)
    for sentence in sentences:
        symbols = sentence.split()
        for symbol in symbols:
            stats[symbol] += 1
    return stats

stats = build_stats(sentences)
print("stats:", stats)

alphabet = []
for word in stats.keys():
    if word[0] not in alphabet:
        alphabet.append(word[0])
    for letter in word[1:]:
        if f"##{letter}" not in alphabet:
            alphabet.append(f"##{letter}")

alphabet.sort()
# 初始词表
vocab = alphabet.copy()
print("alphabet:", alphabet)

# 结果
# stats: defaultdict(<class 'int'>, {'我': 1, '喜欢': 2, '吃': 2, '苹果': 1, 
# 			'他': 1, '不': 1, '苹果派': 1, 'I': 1, 'like': 1, 'to': 1, 
# 			'eat': 1, 'apples': 1, 'She': 1, 'has': 1, 'a': 2, 'cute': 2, 
# 			'cat': 1, 'you': 2, 'are': 1, 'very': 1, 'give': 1, 'hug': 1})
# 初始词表
# alphabet: ['##a', '##e', '##g', '##h', '##i', '##k', '##l', '##o', '##p', 
# 			'##r', '##s', '##t', '##u', '##v', '##y', '##果', '##欢', '##派', 
#			'I', 'S', 'a', 'c', 'e', 'g', 'h', 'l', 't', 'v', 'y', '不', 
#			'他', '吃', '喜', '我', '苹']




# 根据初始词表拆分每个词：
splits = {
    word: [c if i == 0 else f"##{c}" for i, c in enumerate(word)]
    for word in stats.keys()
}
print("splits:", splits)

# 结果
# splits: {'我': ['我'], '喜欢': ['喜', '##欢'], '吃': ['吃'], 
# 			'苹果': ['苹', '##果'], '他': ['他'], '不': ['不'], 
#			'苹果派': ['苹', '##果', '##派'], 'I': ['I'], 
#			'like': ['l', '##i', '##k', '##e'], 'to': ['t', '##o'], 
#			'eat': ['e', '##a', '##t'], 'apples': ['a', '##p', '##p', '##l', '##e', '##s'], 
#			'She': ['S', '##h', '##e'], 'has': ['h', '##a', '##s'], 
#			'a': ['a'], 'cute': ['c', '##u', '##t', '##e'], 
#			'cat': ['c', '##a', '##t'], 'you': ['y', '##o', '##u'], 
#			'are': ['a', '##r', '##e'], 'very': ['v', '##e', '##r', '##y'], 
#			'give': ['g', '##i', '##v', '##e'], 'hug': ['h', '##u', '##g']}



# 根据上述提到的计算互信息的分数公式进行计算：
def compute_pair_scores(splits):
    letter_freqs = defaultdict(int)
    pair_freqs = defaultdict(int)
    for word, freq in stats.items():
        split = splits[word]
        if len(split) == 1:
            letter_freqs[split[0]] += freq
            continue
        for i in range(len(split) - 1):
            pair = (split[i], split[i + 1])
            letter_freqs[split[i]] += freq
            pair_freqs[pair] += freq
        letter_freqs[split[-1]] += freq

    scores = {
        pair: freq / (letter_freqs[pair[0]] * letter_freqs[pair[1]])
        for pair, freq in pair_freqs.items()
    }
    return scores

pair_scores = compute_pair_scores(splits)
for i, key in enumerate(pair_scores.keys()):
    print(f"{key}: {pair_scores[key]}")
    if i >= 5:
        break


# 一些结果：
# ('喜', '##欢'): 0.5
# ('苹', '##果'): 0.5
# ('##果', '##派'): 0.5
# ('l', '##i'): 0.5
# ('##i', '##k'): 0.5
# ('##k', '##e'): 0.125
# 我们需要的是将分数最高的进行合并然后开始循环迭代，看一看分数最高的pair（子词对）：
best_pair = ""
max_score = None
for pair, score in pair_scores.items():
    if max_score is None or max_score < score:
        best_pair = pair
        max_score = score

print(best_pair, max_score)

# 结果
# ('S', '##h') 1.0


# 结果为('S', '##h') 1.0，所以最先合成的就是('S', '##h')→'##Sh'，合并的函数如下：
def merge_pair(a, b, splits):
    for word in stats:
        split = splits[word]
        if len(split) == 1:
            continue
        i = 0
        while i < len(split) - 1:
            if split[i] == a and split[i + 1] == b:
                merge = a + b[2:] if b.startswith("##") else a + b
                split = split[:i] + [merge] + split[i + 2 :]
            else:
                i += 1
        splits[word] = split
    return splits


    
# 最后就是一直进行循环迭代，直到vocab达到了我们想要的数量
vocab_size = 50
while len(vocab) < vocab_size:
    scores = compute_pair_scores(splits)
    best_pair, max_score = "", None
    for pair, score in scores.items():
        if max_score is None or max_score < score:
            best_pair = pair
            max_score = score
    splits = merge_pair(*best_pair, splits)
    new_token = (
        best_pair[0] + best_pair[1][2:]
        if best_pair[1].startswith("##")
        else best_pair[0] + best_pair[1]
    )
    vocab.append(new_token)

print("vocab:", vocab)

# 结果
# vocab: ['##a', '##e', '##g', '##h', '##i', '##k', '##l', '##o', '##p', 
#			'##r', '##s', '##t', '##u', '##v', '##y', '##果', '##欢', '##派',
#			'I', 'S', 'a', 'c', 'e', 'g', 'h', 'l', 't', 'v', 'y', '不', 
#			'他', '吃', '喜', '我', '苹', 'Sh', '喜欢', '苹果', '苹果派', 
#			'li', 'lik', 'gi', 'giv', '##pl', '##ppl', '##ry', 'to', 'yo', 
#			'ea', 'eat']