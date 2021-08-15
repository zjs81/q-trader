from agent.agent import Agent
from functions import *
import sys
best = {}
if len(sys.argv) != 4:
	print("Usage: python train.py [stock] [window] [episodes]")
	exit()

stock_name, window_size, episode_count = sys.argv[1], int(sys.argv[2]), int(sys.argv[3])

agent = Agent(window_size)
data = getStockDataVec(stock_name)
l = len(data) - 1
batch_size = 32
batch_size = 64
S_money = 100
#bought_price = 10
for e in range(episode_count + 1):
	
	print ("Episode " + str(e) + "/" + str(episode_count))
	state = getState(data, 0, window_size + 1)
	
	total_profit = 0
	agent.inventory = []
	b=0
	a=0
	S_money = 10000
	for t in range(l):
		
		action = agent.act(state)

		# sit
		next_state = getState(data, t + 1, window_size + 1)
		reward = 0
		a+=1

		if action == 1: # buy
			price = formatPrice(data[t])
			price = price.replace("$","")
			price = float(price)
			if(price <= S_money):
				S_money = S_money - price
				agent.inventory.append(data[t])
				print ("Buy: " + formatPrice(data[t]))
				b=b+1
				a=0
			else:
				print("Not enough money")
				

		elif action == 2 and len(agent.inventory) > 0: # sell
			bought_price = agent.inventory.pop(0)
			try:
				print(agent.inventory.pop(0))
			except:
				pass
			reward = max(data[t] - bought_price, 0)
			reward =(data[t] - bought_price)*100
			total_profit += data[t] - bought_price
			S_money = S_money + total_profit 
			total_profit - bought_price
			b=0
			a=0
			print ("Sell: " + formatPrice(data[t]) + " | Profit: " + formatPrice(data[t] - bought_price))
			print("Total Money is now " + str(S_money))
			
		if(b>10 or a>20):
			reward+=-200
		done = True if t == l - 1 else False

		agent.memory.append((state, action, reward, next_state, done))
		state = next_state
		
		#if e % 10 == 0:
		#	agent.model.save("models/model_ep" + str(e))
	print("Total Profit For Epoc is " + str(total_profit))
	S_money = 100
	best[e] = total_profit
	

  
Keymax = max(best, key=best.get)
Keymin = min(best, key=best.get)
print(Keymax)
print("The best ep was " + str(Keymax) + ":" + str(best[Keymax]))
print("The worst ep was " + str(Keymin) + ":" + str(best[Keymin]))
#print(best)
	
