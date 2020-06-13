#coding=utf-8
from selenium import webdriver
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.support.wait import WebDriverWait
from selenium.webdriver.common.by import By
from ShowapiRequest import ShowapiRequest
from PIL import Image
import random
import time
driver=webdriver.Chrome()
driver.get('http://www.5itest.cn/register')
time.sleep(5)
#title_contains判断页面是否正常显示
print(EC.title_contains('注册'))

#打开页面时，邮箱地址是否存在，存在在操作，不用担心元素不存在而导致程序报错

#element=driver.find_elements_by_class_name('controls')

locator=(By.ID,'register_email')

#在某个时间范围内找元素，找到显示，未找到报错
WebDriverWait(driver,1).until(EC.visibility_of_element_located(locator))

#用随机数生成用户名和邮箱,random.sample('1234567890abcdef',5)改方法生成出来的是list类型，需转化成字符串类型

for i in range(5):
    user_name=''.join(random.sample('1234567890abcdef',5))   #生成5个随机用户名
    print(user_name)

for i in range(5):
    email=''.join(random.sample('1234567890abcdef',5)) +'@163.com'  #生成5个随机邮箱
    print(email)


#获取验证码图片 
#1.保存整个页面图片
driver.save_screenshot('F:/selenium/images/full.png')
#获取验证码页面坐标
code_element=driver.find_element_by_id('getcode_num')
#获取验证码图片左上角的坐标，（x,y）
print(code_element.location)
left=code_element.location['x']
top=code_element.location['y']
#获取右下角坐标
right=left+code_element.size['width']
bottom=top+code_element.size['height']

#打开整张图片
img=Image.open('F:/selenium/images/full.png')
#在整张图片上裁剪验证码图片
image=img.crop((left,top,right,bottom))
image.save('F:/selenium/images/code.png')

#用第三方接口解析验证码图片
r = ShowapiRequest("http://route.showapi.com/184-4","my_appId","my_appSecret" )
r.addBodyPara("img_base64", "")
r.addBodyPara("typeId", "35")
r.addBodyPara("convert_to_jpg", "0")
r.addBodyPara("needMorePrecise", "0")
r.addFilePara("image",r"F:/selenium/images/code.png")
res = r.post()
text=res.json()['showapi_res_body']['Result']
print(text) # 返回信息

code=driver.find_element_by_id('captcha_code')
code.send_keys(text)


#定位元素 
email=driver.find_element_by_id('register_email')
print(email.get_attribute('placeholder'))
email.send_keys('test@163.com')
#获取输入的用户信息和设想的用户信息是否一致
print(email.get_attribute('value'))



element=driver.find_elements_by_class_name('controls')[1]

#user_element=element.find_elements_by_class_name('form-control')

#print(len(user_element))

#class_name为form-control的元素有好几个用find_elements_by_class_name定位，默认定位的是第一个元素，所以会在邮箱中输入值
user_element=element.find_element_by_class_name('form-control')

user_element.send_keys('wuotng')
 
driver.find_element_by_name('password').send_keys('111111')

driver.find_element_by_xpath('//*[@id="captcha_code"]').send_keys('2222')

time.sleep(3)

#driver.close()





