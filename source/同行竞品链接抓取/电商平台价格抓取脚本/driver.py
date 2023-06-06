import html

from selenium import webdriver
from selenium.webdriver.chrome.service import Service
from webdriver_manager.chrome import ChromeDriverManager
import random
import time
from loadUrl import LoadUrl


#初始化浏览器（一定要全局变量否则闪退）
options = webdriver.ChromeOptions()
options.add_argument("start-maximized")
options.add_experimental_option("excludeSwitches", ["enable-automation"])
options.add_experimental_option('useAutomationExtension', False)
driver = webdriver.Chrome(options=options, service=Service(ChromeDriverManager().install()))
driver.execute_script("Object.defineProperty(navigator, 'webdriver', "
                      "{get: () => undefined})")
driver.execute_cdp_cmd('Network.setUserAgentOverride',
                       {"userAgent": 'Mozilla/5.0 (Macintosh; Intel Mac OS X '
                                     '10_15_7) AppleWebKit/537.36 (KHTML, '
                                     'like Gecko) Chrome/106.0.0.0 '
                                     'Safari/537.36'})#置入自己浏览器的user-agent,模仿真人使用

#浏览器类，完成各大电商平台抓取价格任务
class MyDriver:

    #1.初始化，导入产品链接列表（从文件中提取后置入）
    def __init__(self):
        #登录开始网站和搜索需要网址
        self.loadUrl = LoadUrl()
        self.driver = driver
        #产品链接列表储存
        self.taobaoUrl = self.loadUrl.get_urlList_tb()
        self.ali1688Url = self.loadUrl.get_urlList_1688()
        self.alibabaUrl = self.loadUrl.get_urlList_alibaba()
    #配置浏览器切换页面功能
    def switchPage(self):
        handles = self.driver.window_handles
        for handle in handles:
            # print('handle:',handle)
            if handle != self.driver.current_window_handle:
                self.driver.close()
                self.driver.switch_to.window(handle)
                # print(driver.current_window_handle)
                break
    #退出浏览器
    def quit(self):
        self.driver.quit()

    #隐式等待
    def invi_wait(self):
        self.driver.implicitly_wait(10)

    #随机等待
    def wait(self,level):

        time.sleep(level)
        # else:
        #     time.sleep(random.randint(5,8))
    #淘宝登录
    def get_login_tb(self):
        #初始化浏览器并打开淘宝首页准备登录
        self.driver.get('https://www.taobao.com/')
        self.invi_wait()

        #登录（进入页面后扫码登录）

        self.driver.find_element('xpath','//a[@class="btn-login ml1 tb-bg weight"]').click()
        # <a href="//login.taobao.com/member/login.jhtml?f=top&amp;redirectURL=http%3A%2F%2Fwww.taobao.com%2F" class="btn-login ml1 tb-bg weight">登录</a>
        time.sleep(random.randint(1,3))
        self.switchPage()
        while True:
            print('waiting')
            time.sleep(3)
            # print(driver.current_url)
            if self.driver.current_url == 'https://www.taobao.com/':
                print('login success')
                # print(driver.execute_script("return navigator.userAgent;"))
                break

    #1688登录
    def get_login_1688(self):
        self.driver.get('https://login.taobao.com/?redirect_url=https%3A%2F%2Flogin.1688.com%2Fmember%2Fjump.htm%3Ftarget%3Dhttps%253A%252F%252Flogin.1688.com%252Fmember%252FmarketSigninJump.htm%253FDone%253Dhttps%25253A%25252F%25252Fwww.1688.com%25252F&style=tao_custom&from=1688web')
        self.invi_wait()
        #登录（进入页面后扫码登录）

        while True:
            print('waiting')
            time.sleep(3)
            print(self.driver.current_url)
            if self.driver.current_url == 'https://www.1688.com/':
                print('login success')
                print(self.driver.current_url)
                # print(driver.execute_script("return navigator.userAgent;"))
                break
        self.wait(1)


    #国际站登录
    def get_login_alibaba(self):
        self.wait(2)
        pass

    #淘宝价格抓取
    def get_product_tb(self):
        f = self.loadUrl.export_to_csv_tb()
        writer = self.loadUrl.writer(f)
        self.wait(2)
        for url in self.taobaoUrl:

            self.driver.get(url)#每次获得一个列表中的URL
            self.invi_wait()
            try:#个人店铺
                storeName = self.driver.find_element('xpath','//*[@id="J_ShopInfo"]/div[@class="tb-shop-info-wrap"]/div[@class="tb-shop-info-hd"]/div[@class="tb-shop-name"]/dl/dd/strong/a').text
            except:#公司店铺
                storeName = self.driver.find_element('xpath','//*[@id="header-content"]/div[2]/div[1]/div[1]/a').text
            print(storeName)
            productTitle = self.driver.find_element('xpath','//*[@id="J_Title"]/h3').text
            print(productTitle)
            #范围价格或者单一价格
            productPrice = self.driver.find_element('xpath','//*[@id="J_StrPrice"]/em[2]').text
            print('price',productPrice)

           #月销量
            monthSales = self.driver.find_element('xpath','//*[@id="J_SellCounter"]').text
            print('monthSale',monthSales)
            try:
                promoPrice = self.driver.find_element('xpath','//*[@id="J_PromoPriceNum"]').text
                print('promoPrice',promoPrice)
            except:
                promoPrice = ''
                print('没有优惠价格')

            writer.writerow([url,storeName,productTitle,productPrice,promoPrice,monthSales])
            time.sleep(8)
            #抓取SKU价格（SKU有多有少如何解决）
            #//*[@id="J_isku"]/div/dl[1]/dd/ul/li[1]/a
            try:
                skuList = self.driver.find_elements('xpath','//*[@id="J_isku"]/div/dl[1]/dd/ul/li/a')
                i = 1
                for sku in skuList:
                    # self.driver.execute_script("arguments[0].click();", sku)
                    sku.click()
                    time.sleep(1)
                    skuName = self.driver.find_element('xpath','//*[@id="J_isku"]/div/dl[1]/dd/ul/li[%d]/a/span' % (i,)).get_attribute('innerHTML')

                    # self.driver.save_screenshot(i,'.png')
                    i +=1
                    print('skuName ',skuName)
                    skuPrice = self.driver.find_element('xpath','//*[@id="J_StrPrice"]/em[2]').text
                    print('price',skuPrice)
                    try:
                        skuPromoPrice = self.driver.find_element('xpath','//*[@id="J_PromoPriceNum"]').text
                        print('skuPromoPrice',skuPromoPrice)
                    except:
                        skuPromoPrice = ''
                        print('没有优惠价格')
                    writer.writerow(['','','','','','',skuName,skuPrice,skuPromoPrice])
            except:
                print('无SKU')
            self.wait(1)
            print(driver.current_url)#TEMP:检测当前链接

        self.wait(2)
        f.close()

    #1688价格抓取
    def get_product_1688(self):
        f = self.loadUrl.export_to_csv_1688()
        writer = self.loadUrl.writer(f)

        for url in self.ali1688Url:
            # rows = []
            self.driver.get(url)
            self.invi_wait()
            storeName = self.driver.find_element('xpath','//*[@id="hd_0_container_0"]//span[@title]').get_attribute('innerHTML')

            # print(storeName)
            productTitle = self.driver.find_element('xpath','//*[@class="title-text"]').text
            # print(productTitle)

            #90天成交数
            qtrSales = self.driver.find_element('xpath','//*[@class="title-sale-column"]//span[@class="title-info-number"]').get_attribute('innerHTML')
            qtrSales = html.unescape(qtrSales)#>,<等符号Html转换成常见形式

            # print('qtrSale',qtrSales)

            #范围价格或者单一价格
            # price-wrapper 无区间价， step-price-wrapper 区间价格
            try:
                #无区间价
                productPriceList = self.driver.find_elements('xpath','//*[@class="price-wrapper"]//div[@class="price-box"]//span[@class="price-text"]')
                moq = self.driver.find_element('xpath','//span[@class="unit-text"]').text
                # print('moq',moq)
                #SKU阶梯名称
                self.wait(1)




                if productPriceList == []:#如果没有值代表是阶梯价格\

                    productPriceList = self.driver.find_elements('xpath','//*[@class="step-price-wrapper"]//div[@class="step-price-item"]')
                    #添加进rows中
                    # ([url, storeName, productTitle, qtrSales, '阶梯价格', 'SKU名称',''])
                    stepList = [url, storeName, productTitle, qtrSales]
                    for item in productPriceList:
                        # print(item.text)
                        stepPrice = item.text.splitlines()[1]
                        stepRange = item.text.splitlines()[2]
                        tempStr = stepRange + ': ' + stepPrice
                        # writer.writerow(['','','','',tempStr])#添加阶梯价格
                        stepList.append(tempStr)
                        # stepPriceList, stepRangeList = [],[]#储存区间价格和区间范围
                        # stepRangeList.append(stepRange)
                        # stepPriceList.append(stepPrice)
                        # print('stepRange', stepRange)
                        # print('stepPrice', stepPrice)
                    writer.writerow(stepList)


                else:
                # SKU价格抓取
                    tempList = []#如果有多个SKU且价格不一样，会显示一个范围价格所以用List储存

                    for productPrice in productPriceList:
                        # print('区间价',productPrice.get_attribute('innerHTML'))
                        tempList.append(productPrice.get_attribute('innerHTML'))
                    # print('区间price',tempList)
                    try:
                        temp = tempList[0]+'~'+tempList[1]
                    except:
                        temp = tempList[0]
                    writer.writerow([url, storeName, productTitle, qtrSales, temp])
                try:
                    self.driver.find_element('xpath','//*[@class="sku-wrapper-expend-button"]').click()
                except:
                    pass
                sku_item = self.driver.find_elements('xpath','//*[@class="sku-item-wrapper"]')
                for sku in sku_item:
                    try:
                        if self.driver.find_element('xpath','//*[@class="sku-item-name"]').text == '':
                            skuName = ''
                            skuPrice = sku.text.splitlines()[0]
                        else:

                            skuName = sku.text.splitlines()[0]

                            skuPrice = sku.text.splitlines()[1]
                    except:
                        print("error on sku_item")

                    # print('skuName',skuName)
                    # print('skuPrice',skuPrice)
                    writer.writerow(['','','','','',skuName,skuPrice])
            except:
                #有区间价
                print('错误，请重试')



        self.wait(2)


        f.close()

    #国际站价格抓取
    def get_product_alibaba(self):
        pass
