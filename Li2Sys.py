#timeとthreading,asyncioは標準ライブラリ(のはず)
#discord AND (RPI.GPIO or GPIO)が拡張ライブラリ
import time
import asyncio
import discord
import threading
import RPi.GPIO as GPIO

#discord.pyのintents,client宣言
intents = discord.Intents.default()
intents.message_content = True
client = discord.Client(intents=intents)

#discord.pyのDiscordに表示されるステータス,鑑賞中にする為'watching'
state0 = discord.Activity(name='🟥🟥|施錠|🟥🟥', type=discord.ActivityType.watching)
state1 = discord.Activity(name='🟩🟩|開錠|🟩🟩', type=discord.ActivityType.watching)
state2 = discord.Activity(name='🛑🛑|メンテ中だお|🛑🛑', type=discord.ActivityType.watching)
#RPI.GPIOのGPIO宣言
#18,23は仮,用途に応じて変更
GPIO.setmode(GPIO.BCM)
GPIO.setup(18, GPIO.IN, pull_up_down=GPIO.PUD_UP)
GPIO.setup(23, GPIO.IN, pull_up_down=GPIO.PUD_UP)

#GPIOの入力をint(0~3)に変換してsetactiveを起動する関数GP
def gp():
    swAm=4
    print("testtesttest")
    while True:
        #スイッチ状態取得
        sw01 = GPIO.input(18)
        sw10 = GPIO.input(23)
        swA=sw10*2+sw01
        #swAmはミラー
        if swA!=swAm:
            if (swA == 0):
                swAm=swA
                print("d0")
            elif (swA == 1):
                swAm=swA
                print("d1")
            elif (swA == 2):
                swAm=swA
                print("d2")
            elif (swA == 3):
                swAm=swA
                print("d3")
            asyncio.run(setactive(swA))
            #要らないかも？
            time.sleep(0.25)

#async関数、swAを貰ってDiscordの状態のフラグに使用
async def setactive(ans):
    if ans==0:
        await client.change_presence(status=discord.Status.online, activity=state0)
    if ans==1:
        await client.change_presence(status=discord.Status.online, activity=state1)
    if ans==2:
        await client.change_presence(status=discord.Status.online, activity=state2)

#サブスレッドの構築、ターゲットはGP
thread1 = threading.Thread(target=gp)

#Discordのデコレータ関数,on_readyにサブスレッド起動の構築,改善必須
@client.event
async def on_ready():
    print(f'We have logged in as {client.user}')
    thread1.start()
@client.event
async def on_message(message):
    if message.author == client.user:
        return

#Discord.pyのrun,譲渡する際はTokenを'token'に変更
#('token')にトークンを''で入力
client.run('token')




