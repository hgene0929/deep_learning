from lib2to3.pgen2 import driver
from bs4 import BeautifulSoup
from selenium import webdriver
from time import sleep
import pandas
import requests
import os

# 전체 웹툰 페이지의 html 소스 가져오기
url_all = 'https://comic.naver.com/webtoon/weekday'
html_all = requests.get(url_all).text
soup_all = BeautifulSoup(html_all, 'html.parser')
title_all = soup_all.find_all('a', {'class' : 'title'})

num = 0

# webdriver을 이용하여 현재 크롬 페이지 창을 열어주기
driver = webdriver.Chrome('C:/chromedriver.exe')
driver.get(url_all)

for i in range(len(title_all)):
    sleep(0.5)
    page = driver.find_elements('title')
    page[i].click()
    sleep(0.5)

    # Webtoon URL 
    url = driver.current_url

    # 크롤링 우회
    headers = {'User-Agent':'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/105.0.0.0 Safari/537.36'}
    html = requests.get(url, headers = headers)
    result = BeautifulSoup(html.content, "html.parser")

    # webtoonName
    webtoonName = result.find("span", {"class", "title"}).parent.get_text().strip().split('\n')

    # 현재 디렉토리의 하위 폴더에 이미지를 저장할 폴더 생성
    cwd = os.getcwd()
    files = os.listdir(cwd)

    # 현재 디렉토리 위치
    print(cwd, end='\n\n')

    #크롤링한 이미지를 저장할 폴더를 만듦
    if os.path.isdir(os.path.join(cwd, webtoonName[0])) == False:
        os.mkdir(webtoonName[0])

    print(webtoonName[0] + " folder created successfully!")
    os.chdir(os.path.join(cwd, webtoonName[0]))

    # title 클래스의 td 태그를 찾은 후, 최근 10회차에 대한 웹툰 이미지를 크롤링한다.
    title = result.find_all("td", {"class", "title"})

    for t in title:
        # 회차별로 디렉토리를 만든 후 해당 디렉토리로 이동
        os.mkdir((t.text).strip().split(" :")[0])
        os.chdir(os.getcwd() + "\\" + (t.text).strip().split(" :")[0])

        # 각 회차별 html 소스 가져오기
        url2 = "https://comic.naver.com" + t.a['href']
        html2 = requests.get(url2, headers = headers)
        result2 = BeautifulSoup(html2.content, "html.parser")

        # webtoon image 가져오기
        webtoonImg = result2.find("div", {"class", "wt_viewer"}).find_all("img")
        num = 1 # image_name

        for i in webtoonImg:
            saveName = os.getcwd() + "\\" + str(num) + ".jpg"
            with open(saveName, "wb") as file:
                src = requests.get(i['src'], headers = headers)
                file.write(src.content)
            num += 1
        
        os.chdir("..")

        # 한 회차 이미지 저장 완료!
        print((t.text).strip() + "  saved completely!")
    
    driver.back()