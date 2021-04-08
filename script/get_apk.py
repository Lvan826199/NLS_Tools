# # str = "/product/priv-app/Settings/Settings.apk"
# # print(str.split("/")[-1])
#
# lang = {'ar': 'ar', 'bg': 'bg', 'cs': 'cs', 'da': 'da', 'de': 'de', 'el': 'el', 'en': 'en', 'es-rUS': 'es',
#                      'et': 'et', 'fi': 'fi', 'fr': 'fr', 'hi': 'hi', 'hr': 'hr', 'hu': 'hu', 'in': 'id', 'it': 'it',
#                      'iw': 'he',
#                      'ja': 'ja', 'ko': 'ko', 'lt': 'lt', 'lv': 'lv', 'ms': 'ms', 'nb': 'nb', 'nl': 'nl', 'pl': 'pl',
#                      'pt-rBR': 'pt', 'pt-rPT': 'pt', 'ro': 'ro', 'ru': 'ru', 'sk': 'sk', 'sl': 'sl', 'sr': 'sr',
#                      'sv': 'sv',
#                      'th': 'th', 'tl': 'tl', 'tr': 'tr', 'uk': 'uk', 'ur': 'ur', 'vi': 'vi', 'zh-rCN': 'zh',
#                      'zh-rTW': 'zh',
#                      'zh-rHK': 'zh'}
# # a = lang["zh-rCN"]
# # print(a)
#
#
# print("------------------------------")
#
# for i,j in lang.items():
#     print(f"key：{i}，value：{j}")
import langid
xml_string = "يتعذَّر الوصول إلى السجلّ الكامل"
print(langid.classify(xml_string))
print("------------------")
match_rate = str('%.2f' % (float(langid.classify(xml_string)[1]) * 100)) + '%'
print(match_rate)