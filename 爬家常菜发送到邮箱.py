import requests
from bs4 import BeautifulSoup
import smtplib
import schedule
import time
from email.mime.text import MIMEText
from email.header import Header

account = input('请输入你的邮箱：')
password = input('请输入你的密码：')
receiver = input('请输入收件人的邮箱：')

def food():
    res_foods = requests.get('http://www.xiachufang.com/explore/')
    bs_foods = BeautifulSoup(res_foods.text, 'html.parser')
    list_foods = bs_foods.find_all('div', class_='info pure-u')

    list_all = []

    for food in list_foods:
        tag_a = food.find('a')
        name = tag_a.text[17:-13]
        URL = 'http://www.xiachufang.com' + tag_a['href']
        tag_p = food.find('p', class_='ing ellipsis')
        ingredients = tag_p.text[1:-1]
        list_all.append([name, URL, ingredients])
    return list_all
print(food())


def send_email(list_all):

    smtp_server = 'smtp.qq.com'
    qqmail = smtplib.SMTP()
    qqmail.connect(smtp_server, 25)

    qqmail.login(account, password)

    text = str(list_all)
    msg = MIMEText(text, 'plain', 'utf-8')

    # 邮件头信息
    msg['From'] = Header(account)
    msg['To'] = Header(",".join(receiver))
    msg['Subject'] = Header('python test')


    try:
        qqmail.sendmail(account, receiver, msg.as_string())
        print ('邮件发送成功')
    except:
        print ('邮件发送失败')
    qqmail.quit()

def job():
    print('开始一次任务')
    list_all = food()
    send_email(list_all)
    print('任务完成')

schedule.every().monday.do(job)
while True:
    schedule.run_pending()
    time.sleep(1)