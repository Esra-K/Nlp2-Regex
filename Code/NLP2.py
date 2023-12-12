import json
import re
from hazm import sent_tokenize, POSTagger, Normalizer
from collections import defaultdict


posTagger = POSTagger(model='../Data/pos_tagger.model', universal_tag=True)
normalizer = Normalizer()

all_text = {}
id_counter = 0
categories = defaultdict(list)
for file_postfix in ["train", "dev", "test"]:
    text_arr = []
    with open('../Data/perkey_data/data.' + file_postfix) as f:
        text_arr = json.load(f)
    print(len(text_arr))
    for i in range(len(text_arr)):
        text_arr[i]["body"] = normalizer.normalize(text_arr[i]["title"] + ". " + text_arr[i]["body"])
        if i % 10000 == 0:
            print(i)
    text_arr = [text for text in text_arr if len(sent_tokenize(text["body"])) > 20
                                            and "category" in text.keys()
                                            and not text["category"] is None]
    print(len(text_arr))
    main_categories = {"فرهنگ": "فرهنگ|رسانه|سینما|طنز|کتاب", "سیاست": "سیاست|سیاسی|مقاومت",
                       "ورزش": "ورزش|کشتی|فوتبال", "اقتصاد": "اقتصاد",
                       "بین الملل": "بین الملل|جهان", "اجتماعی": "جامعه|اجتماع", "استان‌ها": "استان‌ها",
                       "فناوری اطلاعات": "فناوری اطلاعات", "دانش": "دانش|سلامت|فناوری^(?!اطلاعات).*",
                       "صفحه نخست": "صفحه اصلی", "وبلاگ": "وبلاگ"}
    for category in main_categories.keys():
        main_categories[category] = re.compile(f'({main_categories[category]})')
    for i in range(len(text_arr)):
        # text_arr[i]["identity"] = file_postfix + str(i)

        print(i)
        print(text_arr[i]["keyphrases"])
        print(text_arr[i]["body"])
        for category in main_categories.keys():
            if re.search(main_categories[category], text_arr[i]["category"]):
                text_arr[i]["category"] = category
                all_text[id_counter] = {k: text_arr[i][k] for k in ["body", "keyphrases", "category"]}
                categories[text_arr[i]["category"]].append(id_counter)
                id_counter += 1
                break

with open('../Data/cleaned_data.json', 'w') as fp:
    json.dump(all_text, fp, sort_keys=True, indent=2, ensure_ascii=False)
print({k:str(len(v)) for k, v in categories.items()})
