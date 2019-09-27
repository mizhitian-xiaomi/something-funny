from PIL import Image
from io import BytesIO
import requests

# # 带参数的GET请求,timeout请求超时时间
# params = {'key1': 'python', 'key2': 'java'}
# r = requests.get(url='http://httpbin.org/get', params=params, timeout=3)
#
# # 注意观察url地址，它已经将参数拼接起来
# print('URL地址：', r.url)
# # 响应状态码，成功返回200，失败40x或50x
# print('请求状态码：', r.status_code)
# print('header信息:', r.headers)
# print('cookie信息：', r.cookies)
# print('响应的数据：', r.text)
# # 如响应是json数据 ，可以使用 r.json()自动转换为dict
# print('响应json数据', r.json())


# # 请求获取图片并保存
# r = requests.get('https://pic3.zhimg.com/247d9814fec770e2c85cc858525208b2_is.jpg')
# i = Image.open(BytesIO(r.content))
# # i.show()  # 查看图片
# # 将图片保存
# with open('img.jpg', 'wb') as fd:
#    for chunk in r.iter_content():
#        fd.write(chunk)



url = 'https://api.github.com/some/endpoint'
headers = {'user-agent': 'my-app/0.0.1'}
r = requests.get(url, headers=headers)
print(r.headers)  # 获取响应数据的header信息

with open('test.txt', 'w') as file:
    file.write('asdf')

with open('test.json', 'w') as file:
    date = json.loads(file)
