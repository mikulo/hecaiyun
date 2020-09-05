import requests as req
import random,re
from flask import Flask,request,redirect
app = Flask(__name__)
@app.route('/', methods = ["GET"])
def outlink():
    try:
        shareid = request.args.get("id")
        passwd = request.args.get("passwd")
        if re.match(r'.{12}', shareid):
            pass
        elif shareid == "":
        	return "文件id为空!"
        	
        else:
            return "文件id格式错误!"
        if re.match(r'.{4}', passwd):
    	    pass
        elif passwd == "":
            pass
        else:
            return "文件提取码错误!"        
        headers = {'user-agent': r'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/83.0.4103.97 Safari/537.36'}
        url = r'https://cloud.189.cn/t/'+shareid
        sharehtml = req.get(url,headers=headers)
        fileidlist = re.findall(r"shareId\" value=\"(.+?)\"/>",sharehtml.text)
        if len(fileidlist)==0:
            return '获取文件id失败!'
        else:    
            fileid = fileidlist[0]
        getlinkurl="https://cloud.189.cn/shareFileVerifyPass.action?fileVO.id="+fileid+"&accessCode="+passwd
        getlinkhtml=req.get(getlinkurl,headers=headers)
        linklist = re.findall(r"longDownloadUrl\":\"(.+?)\",\"mediaType",getlinkhtml.text)
        if len(linklist)==0:
            return '获取文件下载链接失败,请检查提取码是否正确!'
        else:    
            link = linklist[0].replace('\\', '')
        return redirect(link)
    except:
        return '未知的错误!'
if __name__ == '__main__':
    app.run(host='0.0.0.0',
            port=5001,
            debug=True)
