#-*- coding:utf-8 -*-
#디스코드 봇
import discord
from discord.ext import commands
import asyncio,discord

#os, 토큰값
import os


#번역
from googletrans import Translator
#랜덤
import random
#웹 리퀘스트
import requests
#글자 제거
import re
#데이터베이스
import psycopg2

#bs4, html 예쁘게 보기
from bs4 import BeautifulSoup

#time.sleep(5)
import time

#json
import json

#인코딩할떄쓰는거
from urllib import parse



#google_translater 구글번역
translator = Translator(service_urls=[
    'translate.google.co.kr',
    'translate.google.com',
])
#@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@


"""

바꾼거

준식머니 일하기
준식머니 정보
준식머니 가입
준식머니 취업
준식머니 공부

준식외워 인풋 아웃풋 모두 중복시 안되게
준식외워 인풋에 따른 아웃풋 랜덤출력
준식아 대답을 키워드형식으로

준식영어 기능 추가

"""

#토큰
TOKEN = os.environ['token']
#데이타베이스 prostgsql
database_url = os.environ['DATABASE_URL']
#라이엇 api키
riot_api = os.environ['riot_api']
naver_id = os.environ['naver_id']
naver_pw = os.environ['naver_pw']

#@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@
#봇 접두사
bot = commands.Bot(command_prefix='준식')


#데이타베이스 연결



"""
할거



"""






#discord 함수
@bot.event
async def on_ready():
    HowPlay = discord.Game("준식아도와줘")
    await bot.change_presence(status=discord.Status.idle, activity=HowPlay)
    print('Ready!')


@bot.command(name="아도와줘")
async def help(ctx):
    embeds = discord.Embed(title="엄준식 명령어 리스트", description="엄준식이 이곳을 점령할테니 잘 새겨들어라, 괄호는 제거하고 입력하도록.", color=0x000000)
    embeds.add_field(name='준식아 (할말)', value= '준식이와 대화를 할 수 있다.\n\n', inline=False)
    embeds.add_field(name='준식외워 (이렇게하면) (이렇게반응)',value=' 왼쪽이 유저가 하는말, 오른쪽이 준식이가 받아치는거 우리 무뇌준식이에게 지능을 선물하자\n\n', inline=False)
    embeds.add_field(name='준식랜덤 (숫자) (숫자)',value=' 준식이가 숫자에서 숫자사이의 숫자 아무거나 하나 뽑아준다\n\n', inline=False)
    embeds.add_field(name='준식번역 (번역할 단어)', value='아무거나 한글로 번역해준다. 토익 100점인 준식이가 번역해준다\n\n', inline=False)
    embeds.add_field(name='준식백과 (궁금한거)', value='준식이가 네이땡형아한테 물어봐서 알려준다.')
    embeds.add_field(name='준식전적 (롤닉네임)', value='준식이가 라이엇 본사에 찾아가서 전적을 가져와준다. 그래서 꽤 오래걸린다. 약25초\n\n',inline=False)
    embeds.add_field(name='준식사전 (궁금한 단어)', value='46개국어를 하는 준식이가 두뇌사전으로 알려준다.\n\n',inline=False)
    embeds.add_field(name='준식스크램블 (5글자이하의 글자)', value='준식이가 해당 글자로 가능한 모든 경우의 수를 알려준다.\n\n',inline=False)
    embeds.add_field(name='준식섞어 (섞을 단어)', value='준식이가 단어를 막 섞어준다. 볶음장인 준식이')
    embeds.set_footer(text="ps.준식머니 도움말")
    await ctx.send(embed=embeds)

@bot.command(name="전적")
async def lol_match(ctx,*,summoner_name):
    indexlen = 10
    kill = []
    death = []
    assists = []
    win = []
    multikill_name = [],[],['더블킬'],['트리플킬'],['쿼드라킬'],['펜타킬']
    multikill = []
    headers = {
        "Accept-Charset": "application / x-www-form-urlencoded; charset = UTF-8",
        "Origin": "https://developer.riotgames.com",
        "X-Riot-Token" : riot_api
    }
    
    params = {
        'api_key': riot_api
    }
    #username 으로  accountId얻기 
    summoner = requests.get(f"https://kr.api.riotgames.com/lol/summoner/v4/summoners/by-name/{summoner_name}",headers=headers,params = params)
    summoner_info = json.loads(summoner.text)
    summoner_accountId = summoner_info['accountId']
    
    #accountId 로 최근 match 리스트 얻기
    params = {
        'api_key': riot_api,
        'endIndex' : indexlen
    }
    summoner_match_list = requests.get(f"https://kr.api.riotgames.com/lol/match/v4/matchlists/by-account/{summoner_accountId}",headers=headers,params = params)
    summoner_match_list_json = json.loads(summoner_match_list.text)


    #match 리스트로 하나하나 matchDto 요청
    for match_list in summoner_match_list_json["matches"]:
        match_game_id = match_list["gameId"]
        time.sleep(1)
        match_game_info = requests.get(f"https://kr.api.riotgames.com/lol/match/v4/matches/{match_game_id}",headers=headers,params = params)
        match_game_info_json = json.loads(match_game_info.text)

        for match_info_player in match_game_info_json['participantIdentities']:
            if str(summoner_name) == str(match_info_player['player']['summonerName']):
                match_player_id = match_info_player['participantId']
                break



        for match_player_info in match_game_info_json['participants']:
            if match_player_id == match_player_info['participantId']:
                kill.append(match_player_info['stats']['kills'])
                death.append(match_player_info['stats']['deaths'])
                assists.append(match_player_info['stats']['assists'])
                multikill.append(match_player_info['stats']['largestMultiKill'])
                if True == match_player_info['stats']['win']:
                    win.append('승')     
                else:
                    win.append('패')
                break
            
    embed = discord.Embed(title="")
    embed.set_author(name=f"**{summoner_name}**의 전적")
    for i in range(indexlen):
        embed.add_field(name=f"{kill[i]}킬{death[i]}데스{assists[i]}어시스트",value=f"{win[i]}, {multikill_name[multikill[i]]}",inline=False)
    await ctx.send(embed= embed)
    

@bot.command(name="백과")
async def dictionary(ctx, *, word):
    headers = {"X-Naver-Client-Id" : naver_id,"X-Naver-Client-Secret" : naver_pw}
    params = {
        "query" : word, 
        'display' : '1'
        }
    parse.urlencode(params, encoding='UTF-8',doseq=True)
    word_json = requests.get("https://openapi.naver.com/v1/search/encyc.json",headers=headers,params=params)
    print(word_json.text)
    word_info = json.loads(word_json.text)
    for items in word_info['items']:
        title = items['title']
        description = items['description']
        link = items['link']
    title = title.replace('<b>','**')
    title = title.replace('</b>','**')
    description = description.replace('</b>','**')
    description = description.replace('<b>','**')
    embed = discord.Embed(title=f"{title}",description=f"{description}",url=f"{link}")
    await ctx.send(embed = embed)

@bot.command() 
async def cat(ctx):
    emoji = discord.utils.get(bot.emojis, name='11')
    #await message.channel.send(":regional_indicator_n::regional_indicator_o: :regional_indicator_m:  :regional_indicator_u: :regional_indicator_h: :regional_indicator_y: :regional_indicator_e: :regional_indicator_n: ")
    await ctx.send(str(emoji))

@bot.command(name="잊어")
async def talk_drop(ctx, text):
    conn = psycopg2.connect(database_url, sslmode='require')
    cur = conn.cursor()

    cur.execute(f"""
    DELETE FROM reaction
    WHERE user_text='{text}';
    """)
    conn.commit()
    cur.close()
    conn.close()
    
@bot.command(name="머니")
async def economy(ctx, *text):
    def find_user():
        cur.execute(f"""
        SELECT EXISTS (
            SELECT * FROM economy
            WHERE user_name = '{ctx.message.author}'
        );
        """)


    if (text[0] == "도움말"):
        embeds = discord.Embed(title="엄준식 머니 명령어 리스트", description="엄준식이 이곳의 경제를 점령할테니 잘 새겨들어라. 괄호는 제거하고 입력하도록.", color=0x000000)
        embeds.add_field(name='준식머니 가입', value= '너의 신상정보를 갈취해서 준식이가 금융계좌를 만들어준다. 그냥 해라.\n\n', inline=False)
        embeds.add_field(name='준식머니 정보',value='너에게 돈이 얼마나 있는지 준식이가 알려준다.\n\n', inline=False)
        embeds.add_field(name='준식머니 도박 (종류) (돈)',value='준식이와 돈을 걸고 도박을 한다. 준식이는 판돈이 작으면 안한다.\n\n', inline=False)
        embeds.add_field(name='도박 종류',value='"묵찌빠", "야바위", "전설의확률조작똥망도박", "무조건패도박" \n\n', inline=False)
        embeds.add_field(name='준식머니 일하기',value= '성실하게 일해서 돈벌어라. 할 수록 경험치가 쌓인다.')
        embeds.set_footer(text="ps.준식머니 도움말")
        await ctx.send(embed=embeds)
    
    if (text[0] == "가입"):
        #데이터베이스 접근
        conn = psycopg2.connect(database_url, sslmode='require')
        cur = conn.cursor()
        #이코노미 데이터 베이스에서 유저네임항목 일치 검색
        find_user()

        #만약 사용자가 리스트에 없는 사람일경우, 벤리스트가 아닌경우
        if (cur.fetchone()[0] == False):
            #사용자의 user_name, money INSERT
            
            cur.execute(f"""
            INSERT INTO economy VALUES('{ctx.message.author}', 0, 0, 0);
            """)
            await ctx.send(f"{ctx.message.author}, 가입되었다. 자본주의사회에 온 것을 환영한다.")
        else:
            await ctx.send("이미 가입된 것 같다.")

        conn.commit()
        cur.close()
        conn.close()

    if (text[0] == "정보"):
        conn = psycopg2.connect(database_url, sslmode='require')
        cur = conn.cursor()

        find_user()

        if (cur.fetchone()[0] == True):
            cur.execute(f"""
            SELECT * FROM economy
            WHERE user_name = '{ctx.message.author}';
            """)
            user_money = cur.fetchone()
            
            await ctx.send(f"소지 준식머니: {user_money[1]}$ ")# 0 : 이름, 1 : 돈, 2 : 돈받은시간
            
        else:
            await ctx.send("'준식머니 가입' 으로 가입해라.")

        conn.commit()
        cur.close()
        conn.close()
        
    if (text[0] == "도박"):
        #도박
        conn = psycopg2.connect(database_url, sslmode='require')
        cur = conn.cursor()

        find_user()

        #데이터 있나 확인
        if (cur.fetchone()[0] == True):#있으면
            print()


        conn.commit()
        cur.close()
        conn.close()
    
    if (text[0] == "일하기"):
        conn = psycopg2.connect(database_url, sslmode='require')
        cur = conn.cursor()

        rand_money = random.randrange(1000,5000)
        
        #이코노미 항목 존재여부
        find_user()
        

        if (cur.fetchone()[0] == True):
            cur.execute(f"""
            SELECT * FROM economy WHERE user_name = '{ctx.message.author}'
            """)
            float_num = cur.fetchone()[2]
            if (float_num + 60 < time.time()):
                cur.execute(f"""
                UPDATE economy 
                SET money = money + {rand_money}, time = {time.time()}
                WHERE user_name = '{ctx.message.author}';
                """)
                
                await ctx.send(f"{rand_money}$ 입금했다.")# 0 : 이름, 1 : 돈
            else:
                now_time = time.time() 
                delay_time = 60 - int(now_time - float_num)
                await ctx.send(f"{delay_time}초 쉬었다 일해라.")

        else:
            await ctx.send("'준식머니 가입' 으로 가입해라.")

        conn.commit()
        cur.close()
        conn.close()
               
@bot.command(name="아")
async def talk(ctx, *,chat):
    conn = psycopg2.connect(database_url, sslmode='require')
    cur = conn.cursor()

    cur.execute(f"""
    SELECT * FROM reaction;
    """)
    result = cur.fetchall()
    conn.commit()
    cur.close()
    conn.close()
    result_R = []
    for i in range(0 ,len(result)):
        if result[i][0] in chat:
            result_R.append(result[i])
    if result_R == []:    
        await ctx.send("뭐라고? 안들린다.")
    else:
        result_len = random.randrange(0, len(result_R))
        await ctx.send(f"{str(result_R[result_len][1])}```{result_R[result_len][2]}가 알려주었다.```")

@bot.command(name="외워")
async def memory(ctx, user_text, *, bot_text):
    user_name = ctx.message.author
    conn = psycopg2.connect(database_url, sslmode='require')
    cur = conn.cursor()
    
    cur.execute(f"""
    SELECT EXISTS (
            SELECT * FROM reaction
            WHERE user_text = '{user_text}'
        );
    """)
    fst_if = cur.fetchone()[0]
    cur.execute(f"""
    SELECT EXISTS (
            SELECT * FROM reaction
            WHERE bot_text = '{bot_text}'
        );
    """)
    scd_if = cur.fetchone()[0]
    #중복확인
    
    if(fst_if == True and scd_if == True):
        await ctx.send("이것과 똑같은 것을 알고있다.") 
    else:
        cur.execute(f"""
        INSERT INTO reaction VALUES('{user_text}','{bot_text}','{user_name}'); 
        """)
        await ctx.send("음, 확실히 외웠다.")
    conn.commit()
    cur.close()
    conn.close()


@bot.command(name="서버정보")
async def info(ctx):
    await ctx.send(f'서버 이름:{ctx.message.guild.name}\n서버 인원:{ctx.message.guild.member_count}')

#번역
@bot.command(name="번역")
async def trans(ctx, *,text):
    headers = {"X-Naver-Client-Id" : naver_id,"X-Naver-Client-Secret" : naver_pw}
    #언어감지

    params = {
        'query' : text
    }
    word_dev = requests.post("https://openapi.naver.com/v1/papago/detectLangs",headers=headers,data=params)
    word_dev_json = json.loads(word_dev.text)

    params = {
        'text': text,
        'source': word_dev_json['langCode'],
        'target': 'ko'
    }
    result = requests.post("https://openapi.naver.com/v1/papago/n2mt",headers=headers, data=params)
    result_json = json.loads(result.text)
    about = result_json['message']['result']["translatedText"]
    """
    #google
    trans_text = translator.translate(text, dest='ko')


    result = trans_text[0].text
    """
    await ctx.send(f"{text}은(는) \n {about} \n 이다 인간.")
    

@bot.command(name="사전")
async def word_search(ctx, *,text):
    respon = requests.get(url="https://dic.daum.net/search.do?q="+ text)
    html = respon.text
    soup = BeautifulSoup(html, 'html.parser')
    hyper_link = soup.select(".txt_cleansch")[0]['href']
    print(hyper_link)

    respon = requests.get(url=f"https://dic.daum.net{hyper_link}")
    html = respon.text
    soup = BeautifulSoup(html, 'html.parser')
    word_name = soup.select(".txt_cleanword")[0].get_text()
    print(word_name)
    word_info = soup.select(".list_mean")[0].get_text()
    print(word_info)
    await ctx.send(f"{text}(은)는\n```{word_name}\n{word_info}```")

@bot.command(name="영어")
async def eng_word(ctx, ):
    en_file = open("discordBot\en_study.txt", 'rt',encoding='utf-8')
    lines = en_file.readlines()
    random_num = random.randrange(1, len(lines), 2)
    eng_word = [lines[random_num],lines[random_num-1]]
    random.shuffle(eng_word)
    en_file.close()
    await ctx.send(f"```{eng_word[1]}```\n||{eng_word[0]}||")

#스크램블 함수
@bot.command(name="스크램블")
async def scramble(ctx, *,text):
    r = len(text)
    if(r > 5):
        await ctx.send("너무 길다 5글자 이하로 해줘라")
    else:
        text = sorted(text)
        used = [0 for _ in range(r)]
        scramble_list = []

        def generate(chosen, used):
            if len(chosen) == r:
                scramble_list.append(''.join(chosen)) 
                return

            for i in range(r):
                if not used[i] and (i == 0 or text[i-1] != text[i] or used[i-1]):
                    chosen.append(text[i])
                    used[i] = 1
                    generate(chosen, used)
                    used[i] = 0
                    chosen.pop()

        generate([], used)
        await ctx.send(f"{', '.join(scramble_list)}##{len(scramble_list)}개")

@bot.command(name="섞어")
async def shuffle(ctx, *,text):
    text_list = []
    for i in text:
        text_list.append(i)
    random.shuffle(text_list)
    text_shuffle = ''.join(text_list)
    await ctx.send(text_shuffle)
    
#랜덤숫자출력
@bot.command(name="랜덤")
async def rand(ctx, *number):
    num1 = int(number[0])
    num2 = int(number[1])
    random_num = random.randrange(num1,num2,1)
    await ctx.send(f"{random_num}가 나왔다")
    

@bot.command()
async def foo(ctx, arg):
    await ctx.send(arg)

bot.run(TOKEN)