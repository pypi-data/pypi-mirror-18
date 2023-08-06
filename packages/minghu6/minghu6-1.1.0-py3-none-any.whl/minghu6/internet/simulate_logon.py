# -*- coding:utf-8 -*-
#!/usr/bin/env python3

"""

"""
import requests
from bs4 import BeautifulSoup

from minghu6.graphic.captcha.url_captcha import CAPTCHA_ID

class KwargsError(BaseException):

    def __str__(self):
        return 'error args'


def pythonscraping__com_humans_only(session=None, **kwargs):

    if session == None:
        session = requests.session()

    try:
        captchaToken = kwargs['captcha_token']
        captchaSid = kwargs['captcha_sid']
        captchaResponse = kwargs[CAPTCHA_ID]
        formBuildId = kwargs['form_build_id']
    except KeyError:
        raise KwargsError


    params = {
        "captcha_token":captchaToken, "captcha_sid":captchaSid,
        "form_id":"comment_node_page_form", "form_build_id": formBuildId,
        "captcha_response":captchaResponse, "name":"一个模拟登陆的人",
        "subject": "到此一游",
        "comment_body[und][0][value]":
        "我不是个机器人"
    }

    r = session.post("http://www.pythonscraping.com/comment/reply/10",
                      data=params)
    responseObj = BeautifulSoup(r.text)
    if responseObj.find("div", {"class":"messages"}) is not None:
        print(responseObj.find("div", {"class":"messages"}).get_text())

    return r.text

url_logon_dict = {'http://www.pythonscraping.com/humans-only':pythonscraping__com_humans_only}

if __name__ == '__main__':
    raise KwargsError