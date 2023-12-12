


def sentence_chunker(text):
    sentences = []
    spans = []
    start = 0
    punctuations = [".", ".", "!", "؟"]
    found = [text.find(p) for p in punctuations]
    while max(found) > -1:
        end = min([idx for idx in found if idx > -1])
        sentences.append(text[start:end + 1])
        spans.append((start, end))
        start = end + 1
        found = [text[start:].find(p) for p in punctuations]
        print(sentences)
    sentences.append(text[start:len(text)])
    spans.append((start, len(text)))
    return {"sentences": sentences, "spans": spans}
    # pattern = re.compile(r"(?=("+'|'.join(punctuations)+r"))")
    # return [m.span() for m in re.finditer(pattern, text)]

# data = {}
# with open("../Data/cleaned_data.json") as f_in:
#     data = json.load(f_in)
# d= {'ورزش': '5233', 'سیاست': '1109', 'اجتماعی': '541', 'فرهنگ': '1774', 'بین الملل': '83', 'فناوری اطلاعات': '148', 'دانش': '359', 'اقتصاد': '202', 'وبلاگ': '229', 'استان\u200cها': '61'}
# print(sum(map(int, d.values())))
# stopwords_verb = re.compile(rf'(^|می\u200c|نمی\u200c|ب)({"|".join(stopwords_list())})(م|ی|یم|ید|ند|$)')
stopwords = re.compile(rf'(^|\s)({"|".join(stopwords_list())})(``)({"|".join(tagset)})')
puncts = re.compile(rf'(^|\s)({"|".join(punct_set)})(``)(PUNCT)')
# pos_regex = re.compile(rf'({"|".join(tagset)})')