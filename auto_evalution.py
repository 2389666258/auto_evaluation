"""
 copyrigth: ICOVETOUS
 time: 2023-7-4 01:12
 version: 1.0.0
 language: python3.9
 system: windows10
 editor: PyCharm
 --- description ---
 此程序用于QLU教务系统(教学一体化服务平台)的自动评教
 --- warning ---
 1. 此程序需要安装 selenium 包
 2. 此程序需要安装 ddddocr 包 源至:(https://github.com/sml2h3/ddddocr)
"""

import random
from time import sleep

from selenium import webdriver  # 操作浏览器的工具
from selenium.webdriver.common.by import By

import ddddocr  # 识别验证码

''' QLU一号通系统(教学管理信息服务平台) '''
# 登录页
login_qlu_url = 'https://sso.qlu.edu.cn'
# 用户名(学号)
username_qlu = ''
# 密码
password_qlu = ''

''' QLU教务系统(教学一体化服务平台) '''
# 登录页
login_edu_url = 'http://jwxt-qlu-edu-cn.vpn.qlu.edu.cn:8118/Logon.do?method=logon'
# 用户名(学号)
username_edu = ''
# 密码
password_edu = ''

''' 评教目标页面 '''
# 评教目标页
evaluation_url = 'http://jwxt-qlu-edu-cn.vpn.qlu.edu.cn:8118/jsxsd/xspj/xspj_find.do?Ves632DSdyV=NEW_XSD_JXPJ'

''' 操作间隔 '''
interval = 0.3


# class Concert:
class Connection:
    # 初始化加载
    def __init__(self):
        # 当前浏览器驱动对象
        self.driver = webdriver.Chrome()

    ''' 登录 QLU一号通系统(教学管理信息服务平台) '''
    def login_qlu(self):
        self.driver.get(login_qlu_url)
        print(' 开始登录 QLU一号通系统(教学管理信息服务平台)...')
        while True:
            try:
                # 输入账号
                xpath_u = '/html/body/app-root/app-right-root/rg-page-container/div/div[2]/div[2]/div[2]/div[' \
                          '2]/div/app-login-auth-panel/div/div[1]/app-login-normal/div/form/div[1]/nz-input-group/input'
                self.driver.find_element(By.XPATH, xpath_u).clear()
                self.driver.find_element(By.XPATH, xpath_u).send_keys(username_qlu)
                sleep(interval)

                # 输入密码
                xpath_p = '/html/body/app-root/app-right-root/rg-page-container/div/div[2]/div[2]/div[2]/div[' \
                          '2]/div/app-login-auth-panel/div/div[1]/app-login-normal/div/form/div[2]/nz-input-group/input'
                self.driver.find_element(By.XPATH, xpath_p).clear()
                self.driver.find_element(By.XPATH, xpath_p).send_keys(password_qlu)
                sleep(interval)

                # 点击登录
                xpath_b = '/html/body/app-root/app-right-root/rg-page-container/div/div[2]/div[2]/div[2]/div[' \
                          '2]/div/app-login-auth-panel/div/div[1]/app-login-normal/div/form/div[6]/div/button'
                self.driver.find_element(By.XPATH, xpath_b).click()
                sleep(interval)

                # 判断是否登录成功
                if 'login' not in self.driver.current_url:
                    print(' QLU一号通系统(教学管理信息服务平台) 登录成功！')
                    print("当前界面为:", self.driver.current_url)
                    break
                else:
                    print(' QLU一号通系统(教学管理信息服务平台) 登录失败，正在重试...')
                    sleep(interval * 3)

            except:
                print("当前界面为:", self.driver.current_url)
                sleep(interval * 3)
                continue

    ''' 登录 QLU教务系统(教学一体化服务平台) '''
    def login_edu(self):
        self.driver.get(login_edu_url)
        print(' 开始登录 QLU教务系统(教学一体化服务平台)...')
        while True:
            try:
                # 输入账号
                xpath_u = '/html/body/form/div/div/div[2]/div[1]/div[2]/table/tbody/tr[1]/td[2]/input[1]'
                self.driver.find_element(By.XPATH, xpath_u).clear()
                self.driver.find_element(By.XPATH, xpath_u).send_keys(username_edu)
                sleep(interval)

                # 输入密码
                xpath_p = '/html/body/form/div/div/div[2]/div[1]/div[2]/table/tbody/tr[2]/td[2]/input[1]'
                self.driver.find_element(By.XPATH, xpath_p).clear()
                self.driver.find_element(By.XPATH, xpath_p).send_keys(password_edu)
                sleep(interval)

                # 输入验证码
                xpath_i = '/html/body/form/div/div/div[2]/div[1]/div[2]/table/tbody/tr[3]/td[2]/img'
                xpath_c = '/html/body/form/div/div/div[2]/div[1]/div[2]/table/tbody/tr[3]/td[2]/input'
                self.ocr_captcha_img(xpath_i, xpath_c)
                sleep(interval)

                # 点击登录
                xpath_b = '/html/body/form/div/div/div[2]/div[1]/div[2]/table/tbody/tr[4]/td/input'
                self.driver.find_element(By.XPATH, xpath_b).click()
                sleep(interval)

                # 判断是否登录成功
                if 'logon' not in self.driver.current_url:
                    print(' QLU教务系统(教学一体化服务平台) 登录成功！')
                    print("当前界面为:", self.driver.current_url)
                    break
                else:
                    print(' QLU教务系统(教学一体化服务平台) 登录失败，正在重试...')
                    sleep(interval * 3)

            except:
                print("当前界面为:", self.driver.current_url)
                sleep(interval * 3)
                continue

    ''' 识别 QLU教务系统(教学一体化服务平台) 的验证码 并填入 '''
    def ocr_captcha_img(self, xpath_i, xpath_c):
        # 获取验证码图片
        img = self.driver.find_element(By.XPATH, xpath_i)

        # 保存图片到本地
        img.screenshot('captcha.png')

        # 识别验证码
        ocr = ddddocr.DdddOcr()
        with open('captcha.png', 'rb') as f:
            image = f.read()
        code = ocr.classification(image)
        print(' 验证码为:', code)

        # 填入验证码
        self.driver.find_element(By.XPATH, xpath_c).clear()
        self.driver.find_element(By.XPATH, xpath_c).send_keys(code)

    ''' 进入 评教课程分类 页面 '''
    def enter_evaluation_course_classification(self):
        self.driver.get(evaluation_url)
        print(' 进入 评教课程分类 页面...')
        # 索引
        index = 1
        while True:
            try:
                # 找到 tbody
                tbody = self.driver.find_element(By.XPATH, '/html/body/div[3]/div[2]/form/table/tbody')
                trs1 = tbody.find_elements(By.TAG_NAME, 'tr')
                # tr遍历
                for tr1 in trs1[index:]:
                    # td遍历
                    tds1 = tr1.find_elements(By.TAG_NAME, 'td')
                    for td1 in tds1:
                        # 点击 进入评价 按钮
                        if '进入评价' in td1.text:
                            td1.find_element(By.TAG_NAME, 'a').click()
                            index += 1
                            # 关掉alert
                            self.driver.switch_to.alert.accept()
                            # 进入 评教课程 页面
                            self.enter_evaluation_course()
                print(' 评教全部完成！')
                break
            except:
                print("当前界面为:", self.driver.current_url)
                sleep(interval * 3)
                continue

    ''' 进入 评教课程 页面 '''
    def enter_evaluation_course(self):
        print(' 进入 评教课程 页面...')
        while True:
            try:
                # 找到 tbody
                tbody = self.driver.find_element(By.XPATH, '/html/body/div[3]/form/table/tbody')
                trs = tbody.find_elements(By.TAG_NAME, 'tr')
                # tr遍历
                for tr in trs:
                    # td遍历
                    tds = tr.find_elements(By.TAG_NAME, 'td')
                    for td in tds:
                        # 点击 评价 按钮
                        if '评价' in td.text or '修改' in td.text:
                            td.find_element(By.TAG_NAME, 'a').click()
                            # 进入打开的评教新窗口
                            self.driver.switch_to.window(self.driver.window_handles[-1])
                            # 开始评教
                            self.evaluation()
                            break
                # 点击 提交 按钮
                try:
                    self.driver.find_element(By.XPATH, '/html/body/div[3]/div/input[1]').click()
                finally:
                    print(" 此 课程类 评教完成！")
                    sleep(interval)
                    # 返回 评教课程分类 页面
                    self.driver.get(evaluation_url)
                break

            except:
                print("当前界面为:", self.driver.current_url)
                sleep(interval * 3)
                continue

    ''' 开始评教 '''
    def evaluation(self):
        print(' 正在评教...')
        while True:
            try:
                # 找到 tbody
                tbody = self.driver.find_element(By.XPATH, '/html/body/div/form/table[1]/tbody')
                trs = tbody.find_elements(By.TAG_NAME, 'tr')
                # tr遍历
                for tr in trs:
                    # td遍历
                    tds = tr.find_elements(By.TAG_NAME, 'td')
                    for td in tds:
                        # 选择td中多选框的第一个选项
                        if 'radio' in td.get_attribute('innerHTML'):
                            # 选择input中的 随机 第1或3 项
                            random_num1 = random.choice([0, 2])
                            td.find_elements(By.TAG_NAME, 'input')[random_num1].click()
                            # 选择select中的 随机 第1-10 项
                            if random_num1 == 2:
                                random_num1 = 1
                            random_num2 = random.randint(1, 10)
                            td.find_elements(By.TAG_NAME, 'select')[random_num1].find_elements(By.TAG_NAME, 'option')[random_num2].click()
                            break
                # 点击 保存 按钮
                self.driver.find_element(By.XPATH, '/html/body/div/form/table[2]/tbody/tr/td/input[1]').click()
                # 关闭当前评教窗口
                self.driver.close()
                # 切换回评教课程页面
                self.driver.switch_to.window(self.driver.window_handles[-1])
                break
            except:
                print("当前界面为:", self.driver.current_url)
                sleep(interval)
                continue

    ''' 退出 '''
    def finish(self):
        self.driver.quit()


if __name__ == '__main__':
    print('--> 程序开始')

    con = Connection()
    try:
        # 登录 (两个)
        con.login_qlu()
        con.login_edu()
        # 进入评教页面
        con.enter_evaluation_course_classification()
    except Exception as e:
        print(e)
    finally:
        con.finish()

    print('程序结束 <--')

