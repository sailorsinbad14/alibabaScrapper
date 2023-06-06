from driver import MyDriver

def scrapTaobao():
    driver = MyDriver()
    driver.get_login_tb()
    driver.get_product_tb()
    driver.quit()

def scrap1688():
    driver = MyDriver()
    driver.get_login_1688()
    driver.get_product_1688()
    driver.quit()

scrapTaobao()
# scrap1688()
