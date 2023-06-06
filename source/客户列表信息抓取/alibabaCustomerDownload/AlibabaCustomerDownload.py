import time
import json
import datetime
import pandas
from selenium import webdriver
from selenium.webdriver.chrome.service import Service
from webdriver_manager.chrome import ChromeDriverManager
from selenium.webdriver.common.action_chains import ActionChains

# 初始化浏览器（一定要全局变量否则闪退）
options = webdriver.ChromeOptions()
options.add_argument("start-maximized")
options.add_experimental_option("excludeSwitches", ["enable-automation"])
options.add_experimental_option('useAutomationExtension', False)
driver = webdriver.Chrome(options=options,
                          service=Service(ChromeDriverManager().install()))
driver.execute_script("Object.defineProperty(navigator, 'webdriver', "
                      "{get: () => undefined})")
driver.execute_cdp_cmd('Network.setUserAgentOverride',
                       {"userAgent": 'Mozilla/5.0 (Macintosh; Intel Mac OS X '
                                     '10_15_7) AppleWebKit/537.36 (KHTML, '
                                     'like Gecko) Chrome/106.0.0.0 '
                                     'Safari/537.36'})  # 置入自己浏览器的user-agent,模仿真人使用
# 将数据写入json文件子模块
def json_dumps(dict):
    json_obj = json.dumps(dict)
    filename = f'customer_export_{datetime.date.today().strftime("%m%d%Y")}'
    with open(f'{filename}.json', 'w') as file:
        file.write(json_obj)

# 将json文件转换成Excel
def json_to_excel():
    while True:
        try:
            filename = f'customer_export_{datetime.date.today().strftime("%m%d%Y")}'
            pandas.read_json(f'{filename}.json').to_excel(f'{filename}.xlsx')
            break
        except:
            print('请关闭打开的excel文件，10秒后自动再次尝试！')
            time.sleep(10)
            continue

# 获取客户列表信息模块
def getCustomerInfo():
    customer_dict = {}
    list_name = []
    list_email = []
    list_company = []
    list_country = []
    customer_list = driver.find_elements(
        'xpath',
        f'//*[@style="max-height: 10000px; position: relative;"]/table/tbody/tr')
    try:
        total_pages = int(driver.find_element(
            'xpath', '//*[@class="next-pagination-display"]'
        ).text.split('/')[-1])
    except:
        total_pages = len(driver.find_elements('xpath',
                                               '//*['
                                               '@class="next-pagination-list"]/button'))
    print(total_pages)
    for i in range(total_pages):
        print(f'This is {i+1}/{total_pages} page')
        for times in range(len(customer_list)):

            try:
                name = driver.find_element(
                    'xpath',
                    f'//*[@style="max-height: 10000px; position: '
                    f'relative;"]/table/tbody/tr[{times + 1}]//div[@class="name"]').text
            except:
                name = ''
            try:
                email = driver.find_element(
                    'xpath',
                    f'//*[@style="max-height: 10000px; position: '
                    f'relative;"]/table/tbody/tr[{times + 1}]//div['
                    f'@class="contact-methods"]').text
            except:
                email = ''
            try:
                company = driver.find_element(
                    'xpath',
                    f'//*[@style="max-height: 10000px; position: '
                    f'relative;"]/table/tbody/tr[{times + 1}]//div['
                    f'@class="column-component-company-name-companyName"]').text
            except:
                company = ''
            try:
                country = driver.find_element(
                    'xpath',
                    f'//*[@style="max-height: 10000px; position: '
                    f'relative;"]/table/tbody/tr[{times + 1}]//div['
                    f'@class="country-flag-container "]').text
            except:
                country = ''
            # print(f'name:{name}')
            # print(f'email:{email}')
            # print(f'company:{company}')
            # print(f'country:{country}')

            # times += 1

            list_name.append(name)
            list_email.append(email)
            list_company.append(company)
            list_country.append(country)

    # 翻页
        try:
            driver.find_element('xpath','//button[@class="next-btn next-medium '
                                        'next-btn-normal next-pagination-item '
                                        'next-next"]').click()
            # driver.implicitly_wait(1)
            time.sleep(3)
        except:
            print('this is the end of page')
            break



    customer_dict['客户名'] = list_name
    customer_dict['邮箱'] = list_email
    customer_dict['公司名'] = list_company
    customer_dict['国家'] = list_country

    json_dumps(customer_dict)
    json_to_excel()

def getSearchKeywords():
    keywords_list = []
    try:
        mouse_locations = driver.find_elements('xpath','//*['
                                                 '@class="search-keywords"]')
        for mouse in mouse_locations:

            ActionChains(driver).move_to_element(mouse).perform()

            search_keywords = driver.find_elements('xpath','//*['
                                                 '@id="J-search-keywords-copydiv-PageEffects"]/div')
            for keywords in search_keywords:
                keywords_list.append(keywords.text)
        print(keywords_list)
    except:
        print("search_keywords error")

#登录国际站账号模块
def login():
    driver.get(
        'https://alicrm.alibaba.com/?spm=a2756.trade-list-seller.0.0.27b076e94J9kpe#my-customer')
    while True:
        key_to_continue = input('press any key to continue')
        if key_to_continue:
            break

#关闭浏览器结束程序模块
def closeDriver():
    key_to_continue = input('End app? [Y/N]')
    if key_to_continue == 'Y' or key_to_continue == 'y':
        driver.quit()
        return True
    else:
        return False

#主程序模块
if __name__ == '__main__':
    login()  # 登录国际站账号
    while True:  #设置循环方便反复抓取不同条件筛选的客户列表
        # getCustomerInfo()  # 获取客户列表信息模块+写入json文件
        getSearchKeywords()
        if closeDriver():  # 结束程序关闭浏览器
            break
        while True:
            key_to_continue = input('press any key to continue')
            if key_to_continue:
              break