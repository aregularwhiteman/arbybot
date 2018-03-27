from bittrex import *
from lefunctions import *
from apis import *
import threading
import os
import time
from time import sleep
import csv

balance={}
balance['USDT']=100
coin='ETC'

operation = Bittrex(opkey,opsec)	

def caller(cmarket):
		time1=time.clock()
		global api
		

		while True:
			try:
				apim=random.choice(api)
				apic,secret=apim[0],apim[1]
				apiv=Bittrex(apic,secret)
				data = apiv.get_orderbook(cmarket,BOTH_ORDERBOOK,depth=1)
				market={}
				market['pair']=cmarket
				market['buyQuantity']=data['result']['buy'][0]['Quantity']
				market['buyRate']=data['result']['buy'][0]['Rate']
				market['sellQuantity']=data['result']['sell'][0]['Quantity']
				market['sellRate']=data['result']['sell'][0]['Rate']
				break
			except:
				sleep(1)

		return market

def writetofile(data):
	
	while True:	
		try:
			dataset='arbyprofit.csv'
			file=open(dataset,'a')	
			writer=csv.writer(file)
			writer.writerow([data],)
			file.close()
			break

		except PermissionError:
			print('PermissionError')
			sleep(3)

def bgetbalances():
	res=operation.get_balances()
	print(res)
	result=res['result']
	balances=[]
	print()
	
	for x in range(len(result)):
		Currency=result[x]['Currency']
		Available=result[x]['Available']
		if Available>0:
			print(Currency,Available)
			balances.append([Currency,Available])
	print()
	sleep(2)


def main(coin):
	
	USDTBTC=caller('USDT-BTC')
	BTCNEO=caller('BTC-'+coin)
	USDTNEO=caller('USDT-'+coin)

	info='buy btc, buy '+coin+' for btc, sell '+coin+' for usd'
	boughtbitcoins=balance['USDT']/USDTBTC['sellRate']
	boughtneo=boughtbitcoins/BTCNEO['sellRate']
	returnedusd=boughtneo*USDTNEO['buyRate']
	print(returnedusd)

	if returnedusd>102:
		print(info)
		pack=[info,boughtbitcoins,boughtneo,returnedusd]
		writetofile(pack)

	info='buy '+coin+', sell '+coin+' for btc, sell btc fo usd'
	boughtneo=balance['USDT']/USDTNEO['sellRate']
	gotbtc=boughtneo*BTCNEO['buyRate']
	returnedusd=gotbtc*USDTBTC['buyRate']
	print(returnedusd)

	if returnedusd>102:
		print(info)
		pack=[info,boughtneo,gotbtc,returnedusd]
		writetofile(pack)

			
	global it
	it=it+1	
	print(it)

bgetbalances()

it=0

while True:
	

	main(coin)
	sleep(0.2)



