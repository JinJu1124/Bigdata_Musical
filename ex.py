from urllib.parse import urlparse, parse_qsl, urlencode, urlunparse


url = 'http://mticket.interpark.com/Goods/GoodsInfo/info?GoodsCode=18011275&app_tapbar_state=fix#GoodsTabArea'
parts = urlparse('http://mticket.interpark.com/Goods/GoodsInfo/info?GoodsCode=18011275&app_tapbar_state=fix#GoodsTabArea')

print(parts)
# # 요소 분리
# qs = dict(parse_qsl(parts.netloc))
# # parse_qsl의 결과를 dictionary로 캐스팅
# qs['netloc'] = ''
# # 수정 작업
# parts = parts._replace(query=urlencode(qs))
# # dictionary로 되어 있는 query string을 urlencode에 넘겨 문자열화하고 replace
# new_url = urlunparse(parts)
# # urlunparse해서 새로운 URL 얻어내기


# parts = parts._replace(netloc='mobileticket.interpark.com')

# new_url = urlunparse(parts)

# print(new_url)