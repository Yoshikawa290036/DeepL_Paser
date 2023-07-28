import requests
from bs4 import BeautifulSoup
from selenium import webdriver
from selenium.webdriver.chrome.options import Options
import time
import io
import sys
import urllib

KEY = "****"


sys.stdout = io.TextIOWrapper(sys.stdout.buffer, encoding='utf-8')


def get_page_source(URL):
    options = Options()
    options.add_argument('--disable-logging')
    options.add_argument('--log-level=3')
    options.add_experimental_option('excludeSwitches', ['enable-logging'])
    driver = webdriver.Chrome(options=options)
    driver.get(URL)
    time.sleep(6)
    return driver.page_source


def Transrate_URL(text: str):
    URL_baes = 'https://www.deepl.com/translator#en/ja/'
    ntext = urllib.parse.quote(text)
    ntext = ntext.replace("/", "%5C%2F")
    return URL_baes + ntext


def get_jp_TR(html):
    soup = BeautifulSoup(html, 'html.parser')
    # print(soup)
    textareas = soup.findAll("d-textarea")
    # print(textareas[1].text)
    return textareas[1].text
    #     # print(textarea.string)
    #     # print(type(textarea))
    #     print(textarea.get("_d-id"))
    #     # print(type(textarea.get("_d-id")))
    #     if textarea.get("_d-id") == "35":
    #         print(textarea)
    # print(a)


def fix_text(jp: str):
    with open("text/fix_list.txt", "r") as f:
        lines = f.readlines()
    # fixbef = []
    # fixaft = []
    fix_key = []
    cnt = 0
    jp = jp.replace(" ", "")
    jp = jp.replace("　", "")
    for i in range(len(lines)):
        lc = lines[i].strip().split(KEY)
        if not len(lc) == 2:
            continue
        # fixbef.append(lc[0])
        # fixaft.append(lc[1])
        fix_key.append([len(lc[0].strip()), lc[0].strip(), lc[1].strip()])
        cnt += 1
    fix_key.sort(reverse=True)
    # sorted(fix_key, reverse=True)
    # print(fix_key)
    for i in range(cnt):
        if "\\" == fix_key[i][2][0]:
            jp = jp.replace(fix_key[i][1], fix_key[i][2]+" ")
        elif "．" == fix_key[i][2][0]:
            jp = jp.replace(fix_key[i][1], fix_key[i][2]+"\n")
        else:
            jp = jp.replace(fix_key[i][1], fix_key[i][2])
    return jp


def read_inp():
    text_list = []
    text = ''
    with open("text/inp.txt", "r") as f:
        lines = f.readlines()
    for line in lines:
        if KEY in line:
            lc = line.strip().split(KEY)
            text += lc[0]
            text_list.append(text)
            text = ''
        else:
            text += line.strip() + ' '
    text_list.append(text)
    return text_list


if __name__ == '__main__':
    output = []
    txt_list = read_inp()
    for txt in txt_list:
        url = Transrate_URL(txt)
        html = get_page_source(url)
        tr_jp = get_jp_TR(html)
        new_jp = fix_text(tr_jp)
        output.append(new_jp + '\n')

    with open("text/out.txt", 'w') as f:
        f.writelines(output)

    for out in output:
        print()
        print(out.strip())
