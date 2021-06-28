import requests
import re
import pypandoc

def defaultUrl(url):
    #获得当前页内容
    headers = {
#header头
}

    index = requests.get(url = url,headers = headers)
    index.encoding = 'utf-8'
    src = index.text
    src = re.sub(r'<header class=\"am-topbar am-g am-g-collapse\">([\s\S]*?)</header>','',src)
    #去除header
    #print(src)
    src = src.replace("src=\"/media/images/","src=\"https://src.sjtu.edu.cn/media/images/")
    #图片处理
    src = src.replace("href=\"","href=\"https://src.sjtu.edu.cn/profile/")
    src = src.replace("<a href=\"https://src.sjtu.edu.cn/profile//profile/此处写一下uid/\">硝基苯</a>","请勿外传")
    #作者处理
    return src

def getSrcList(src):
    #获得当前页的src列表
    #print(src)
    srcRe = re.compile(r'/post/.*?>')
    srcList = srcRe.findall(src)
    #print(srcList)

    ####开始数据清洗
    #print (srcTimeList)
    srcLinkList = []
    for i in srcList:
        i = [i[1:-3]]
        #print(i)
        srcLinkList = srcLinkList + i
    #print (srcLinkList)
    return srcLinkList
        
def getSrcPage(src):
    #获得漏洞总页数
    srcRe = re.compile(r'<a href=\"https://src.sjtu.edu.cn/profile/\?page=([0-9].*?)">[0-9].*?</a>')
    srcPage = srcRe.findall(src)
    srcPageNum = srcPage[-1]
    return srcPageNum

def getSrcReport(srcList):
    #获得漏洞报告
    rootUrl = "https://src.sjtu.edu.cn/"+srcList
    srcReport = defaultUrl(rootUrl)
    return srcReport
    #print(srcReport)


def getHeader(src):
    #给文件命名
    srcRe = re.compile(r'<h1 class="am-article-title">(.*?)</h1>')
    header = srcRe.findall(src)
    srcRe = re.compile(r'<td>([0-9].*?-.*?)</td>')
    time = srcRe.findall(src)
    name = str(time)+str(header)
    name = name.replace("['","")
    name = name.replace("']","")
    name = name.replace(":","-")
    name = name.replace(" ","-")
    print(name)
    return name
    

def htmlToWord(header):
    pypandoc.convert_file(header+".html", 'docx', outputfile=header+".docx")
    return true
    
  
if __name__=="__main__":
    url = "https://src.sjtu.edu.cn/profile/"
    src = defaultUrl(url)
    #访问首页，获得漏洞页数
    srcPageNum = getSrcPage(src)
    print ("总页数："+srcPageNum)
    
    #获得页数后进行遍历，得到每页的src列表
    for i in range(1,int(srcPageNum)+1):
        url = "https://src.sjtu.edu.cn/profile/post/?page={}".format(str(i))
        print("当前第{}页".format(i))
        src = defaultUrl(url)
        #print(src)
        srcList = getSrcList(src)
        #print(srcList)

        #读取漏洞报告
        for i in srcList:
            #print(i)
            srcReport = getSrcReport(i)
            #print(SrcReport)
            #给文件取名字
            header = getHeader(srcReport)

            #文件存储
            file = open(header+".html",'w',encoding='utf-8')
            file.write(srcReport)
            file.close()
            htmlToWord(header)
            
