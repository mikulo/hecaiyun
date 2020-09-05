import requests as req
import random,re
from flask import Flask,request,redirect
app = Flask(__name__)
@app.route('/', methods = ["GET"])
def outlink():
    try:
        mobilelist = []
        num = random.randint(0,len(mobilelist)-1)
        mobile = mobilelist[num]
        pwd = ""#填你的密码
        logindata = {'mobile':mobile,"pwd":pwd}
        headers = {'user-agent': r'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/83.0.4103.97 Safari/537.36'
        }
        linkid = request.args.get("id")
        passwd = request.args.get("passwd")
        if re.match(r'.{13}', linkid):
            pass
        elif linkid == "":
        	return "文件id为空!"
        	
        else:
            return "文件id格式错误!"
        if re.match(r'.{4}', passwd):
    	    pass
        elif passwd == "":
            return "文件提取码为空!"
        else:
            return "文件提取码错误!"
        url =r"https://qlink.mcloud.139.com/stapi/auth/login"
        login = req.post(url,headers=headers,data=logindata)
        dictid =eval(login.text)
        if dictid['code'] != 0:
            return "内置解析帐号"+str(num+1)+"登陆错误!"
        userid  = dictid["data"]["userid"]
        infodata={'linkId':linkid,'path':'root',"start":"1","end":"15","sortType":"0","sortDr":"1",r"pass":passwd}
        info = req.post('https://qlink.mcloud.139.com/stapi/outlink/info',data=infodata,headers=headers,cookies=login.cookies)
        infodict= eval(info.text)
        if infodict['code'] != 0:
            return "文件id或者提取码有误!"
        pcaid = infodict['data']['pCaID']
        coid = infodict['data']['coLst']['outLinkCoInfo']['coID']
        contentIds = pcaid+r"/"+coid

        downloaddata = {"linkId":linkid,"contentIds":contentIds,"catalogIds":""}
        download = req.post("https://qlink.mcloud.139.com/stapi/outlink/content/download",data=downloaddata,headers=headers,cookies=login.cookies)
        if eval(download.text)['code'] != 0:
            return "解析链接错误!"
        link = eval(download.text)["data"]["redrUrl"]
        
        return redirect(link)
    except:
        return '未知的错误!'
if __name__ == '__main__':
    app.run(host='0.0.0.0',
            debug=True)
