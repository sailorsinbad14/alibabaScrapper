import csv

class LoadUrl:

    def __init__(self):
        pass

    def get_urlList_tb(self):
        urlList = []
        f = open(r'./urlBook/urlListTaobao.txt', mode='r')
        urls = f.readlines()
        for url in urls:
            urlList.append(url.strip())
        f.close()#关闭文件读取
        return urlList

    def get_urlList_1688(self):
        urlList = []
        f = open(r'./urlBook/urlList1688.txt', mode='r')
        urls = f.readlines()
        for url in urls:
            urlList.append(url.strip())
        f.close()#关闭文件读取
        return urlList

    def get_urlList_alibaba(self):
        urlList = []
        f = open(r'./urlBook/urlList1688.txt', mode='r')
        urls = f.readlines()
        for url in urls:
            urlList.append(url.strip())
        f.close()#关闭文件读取
        return urlList

    def writer(self,f):
        writer = csv.writer(f)
        return writer


    def export_to_csv_tb(self):
        f = open('./Report/productPriceTaobao.csv', mode='w', encoding='UTF-8')
        csvwriter = csv.writer(f)
        csvwriter.writerow(['商品链接', '店铺名称', '产品标题', '产品价格', '产品活动价','月销量', 'SKU名称','SKU价格','SKU活动价'])
        return f

    def export_to_csv_1688(self):
        f = open('./Report/productPrice1688.csv', mode='w', encoding='utf-8-sig')
        csvwriter = csv.writer(f)
        csvwriter.writerow(['商品链接', '店铺名称', '产品标题','90天销量', '产品价格', 'SKU名称','SKU价格'])
        return f
    def export_to_csv_alibaba(self):
        f = open('./Report/productPriceAlibaba.csv', mode='w', encoding='UTF-8')
        csvwriter = csv.writer(f)
        csvwriter.writerow(['商品链接', '店铺名称', '产品标题', '产品价格', '产品活动价','月销量', 'SKU名称','SKU价格','SKU活动价'])
        return f

