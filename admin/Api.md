# 本项目微信API说明
# API格式

## Core
1、获取access_token(单独)
https请求方式: GET
https://api.weixin.qq.com/cgi-bin/token?grant_type=client_credential&appid=APPID&secret=APPSECRET
参数	是否必须	说明
grant_type	是	获取access_token填写client_credential
appid	是	第三方用户唯一凭证
secret	是	第三方用户唯一凭证密钥，即appsecret

返回
{"access_token":"ACCESS_TOKEN","expires_in":7200}
参数	说明
access_token	获取到的凭证
expires_in	凭证有效时间，单位：秒

错误返回
{"errcode":40013,"errmsg":"invalid appid"}
返回码	说明
-1	系统繁忙，此时请开发者稍候再试
0	请求成功
40001	AppSecret错误或者AppSecret不属于这个公众号，请开发者确认AppSecret的正确性
40002	请确保grant_type字段值为client_credential
40164	调用接口的IP地址不在白名单中，请在接口IP白名单中进行设置

## 微信API类
### 微信网页授权
全部页面加上是否微信内置浏览器判定
(1)是->(2)，否->(3)
(2)微信内置浏览器打开，判定是否关注公众号
a.重定向微信授权页(判断页)
https://open.weixin.qq.com/connect/oauth2/authorize?appid=wx12711df8339c07f9&redirect_uri=(需要用urlencode处理的跳转页)&response_type=code&scope=snsapi_userinfo&state=(随便填)#wechat_redirect
未关注公众号会提示，如果关注公众号则返回scope对应数据
snsapi_userinfo
前端(微信)发起请求，后端监听跳转页获取code

b.获取code和state
http://fsyjq.roswellcsy.com/index.html?code=021VU2w62BmI5K0B7Dw62788w62VU2wm&state=123
c.通过code获取access_token同时返回openid
d.遍历后台openid清单，判断是否存在该openid
e.存在openid，拉取用户基本信息，不存在openid，跳(4)
d.查看subscribe标志，如果是0，跳(4)，如果是1，跳(6)
(4)一个提示关注公众号页面
(6)回调
05060401

1900

1760

5479.93



1 第一步：用户同意授权，获取code
https://open.weixin.qq.com/connect/oauth2/authorize?appid=APPID&redirect_uri=REDIRECT_URI&response_type=code&scope=SCOPE&state=STATE#wechat_redirect


参数	是否必须	说明
appid	是	公众号的唯一标识
redirect_uri	是	授权后重定向的回调链接地址， 请使用 urlEncode 对链接进行处理
response_type	是	返回类型，请填写code
scope	是	应用授权作用域，snsapi_base （不弹出授权页面，直接跳转，只能获取用户openid），snsapi_userinfo （弹出授权页面，可通过openid拿到昵称、性别、所在地。并且， 即使在未关注的情况下，只要用户授权，也能获取其信息 ）
state	否	重定向后会带上state参数，开发者可以填写a-zA-Z0-9的参数值，最多128字节
#wechat_redirect	是	无论直接打开还是做页面302重定向时候，必须带此参数

用户同意授权后

如果用户同意授权，页面将跳转至 redirect_uri/?code=CODE&state=STATE。

code说明 ： code作为换取access_token的票据，每次用户授权带上的code将不一样，code只能使用一次，5分钟未被使用自动过期。

2 第二步：通过code换取网页授权access_token

获取code后，请求以下链接获取access_token：  https://api.weixin.qq.com/sns/oauth2/access_token?appid=APPID&secret=SECRET&code=CODE&grant_type=authorization_code

参数	是否必须	说明
appid	是	公众号的唯一标识
secret	是	公众号的appsecret
code	是	填写第一步获取的code参数
grant_type	是	填写为authorization_code

正确时返回JSON
{ "access_token":"ACCESS_TOKEN",
"expires_in":7200,
"refresh_token":"REFRESH_TOKEN",
"openid":"OPENID",
"scope":"SCOPE" }

参数	描述
access_token	网页授权接口调用凭证,注意：此access_token与基础支持的access_token不同
expires_in	access_token接口调用凭证超时时间，单位（秒）
refresh_token	用户刷新access_token
openid	用户唯一标识，请注意，在未关注公众号时，用户访问公众号的网页，也会产生一个用户和公众号唯一的OpenID
scope	用户授权的作用域，使用逗号（,）分隔

错误时返回JSON(其他API错误返回应该也一样格式)
{"errcode":40029,"errmsg":"invalid code"}

3 第三步：刷新access_token（如果需要）

refresh_token有效期为30天

获取第二步的refresh_token后，请求以下链接获取access_token：
https://api.weixin.qq.com/sns/oauth2/refresh_token?appid=APPID&grant_type=refresh_token&refresh_token=REFRESH_TOKEN


参数	是否必须	说明
appid	是	公众号的唯一标识
grant_type	是	填写为refresh_token
refresh_token	是	填写通过access_token获取到的refresh_token参数

正确时返回
{ "access_token":"ACCESS_TOKEN",
"expires_in":7200,
"refresh_token":"REFRESH_TOKEN",
"openid":"OPENID",
"scope":"SCOPE" }

4 第四步：拉取用户信息(需scope为 snsapi_userinfo)
http：GET（请使用https协议） https://api.weixin.qq.com/sns/userinfo?access_token=ACCESS_TOKEN&openid=OPENID&lang=zh_CN

参数	描述
access_token	网页授权接口调用凭证,注意：此access_token与基础支持的access_token不同
openid	用户的唯一标识
lang	返回国家地区语言版本，zh_CN 简体，zh_TW 繁体，en 英语
正确时返回

{    "openid":" OPENID",
" nickname": NICKNAME,
"sex":"1",
"province":"PROVINCE"
"city":"CITY",
"country":"COUNTRY",
"headimgurl":    "http://wx.qlogo.cn/mmopen/g3MonUZtNHkdmzicIlibx6iaFqAc56vxLSUfpb6n5WKSYVY0ChQKkiaJSgQ1dZuTOgvLLrhJbERQQ4eMsv84eavHiaiceqxibJxCfHe/46",
"privilege":[ "PRIVILEGE1" "PRIVILEGE2"     ],
"unionid": "o6_bmasdasdsad6_2sgVt7hMZOPfL"
}
参数	描述
openid	用户的唯一标识
nickname	用户昵称
sex	用户的性别，值为1时是男性，值为2时是女性，值为0时是未知
province	用户个人资料填写的省份
city	普通用户个人资料填写的城市
country	国家，如中国为CN
headimgurl	用户头像，最后一个数值代表正方形头像大小（有0、46、64、96、132数值可选，0代表640*640正方形头像），用户没有头像时该项为空。若用户更换头像，原有头像URL将失效。
privilege	用户特权信息，json 数组，如微信沃卡用户为（chinaunicom）
unionid	只有在用户将公众号绑定到微信开放平台帐号后，才会出现该字段。

5 附：检验授权凭证（access_token）是否有效
http：GET（请使用https协议） https://api.weixin.qq.com/sns/auth?access_token=ACCESS_TOKEN&openid=OPENID


参数	描述
access_token	网页授权接口调用凭证,注意：此access_token与基础支持的access_token不同
openid	用户的唯一标识

正确返回
{ "errcode":0,"errmsg":"ok"}
### 其他
1、自定义菜单
2、消息管理
3、微信网页开发
4、用户管理


