from urllib.request import urlopen
from bs4 import BeautifulSoup
import os

import telegram


# 텍스트 파일 만들기
os.rename('titleNew.txt', 'titleOld.txt')
f = open('msgNew.txt', 'w') # 메세지 본문 파일
t = open('titleNew.txt', 'w') # 비교를 위한 제목 파일

# 이전 기사 제목 파일의 첫번째 줄 찾아오기
t_old = open('titleOld.txt', 'r') # 비교를 위한 제목 파일
first_line = t_old.readline()

# 여러 웹페이지를 다 긁어서 기사 제목이나 내용 파싱
pgNum = range(1, 5)

escapeNum = 1

for i in pgNum:

    if escapeNum == 0:
        break

    # 중앙일보 인사 기사 페이지 열기
    html = urlopen("https://news.joins.com/people/personnel/list/"+str(i))

    # beautifulSoup으로 html 내용을 파싱하기
    bsObject = BeautifulSoup(html, "html.parser")

    # 웹페이지 소스코드를 보니, 인사 기사의 기본 클래스는 h2로 되어 있고, a 태그로 처리되고 있어, 이 부분을 가져오도록 함
    my_titles = bsObject.select('h2 > a')

    # 각 페이지마다 있는 "피플" 이름 지우기
    for link in my_titles:
        tMsg1 = link.text+'\n' # 기사 제목 만들기
        
        if escapeNum == 0:
            break

        # 어제 인사 기록의 첫번째 제목과 같지 않을 경우에만 돌아가도록
        if tMsg1 != first_line:
            if tMsg1 != "피플\n":
                f.write(tMsg1)
                t.write(tMsg1)

                tMsg2 = 'https://news.joins.com'+link.get('href')+'\n' # 기사 링크 만들기
                f.write(tMsg2)
        else:
            escapeNum = 0
        
f.close() # 파일 닫기
t.close()

# 만들어둔 텍스트 파일 불러서 텔레그램으로 보낼 msg 본문 만들기
f2 = open('msgNew.txt','r')
msg = f2.read()

# 텔레그램으로 메시지 보내기
bot = telegram.Bot(token='981208625:AAHHX0gjl8k1PjgFaq8CPZJBh2M80hNiLBI')
# bot.sendMessage(chat_id = '@HR_alert', text = 'test입니다') @HR_alert은 공개채널
bot.sendMessage(chat_id = '@HR_alert', text = msg)

# 해야 할일 
# 1) 지금은 첫 페이지만 가져오는데, 여러 페이지, 적어도 3페이지는 확인해서 가져오도록 변경 - done
# 2) 가져온 제목을 기존의 기사 제목과 비교해서 새로운 내용만 메세지 본문으로 만들기 - done
# 3) 고객사 리스트를 업로드 해, 거기에 있는 내용과 비교해서 고객사 리스트에 있는 기업의 인사만 추려내기
