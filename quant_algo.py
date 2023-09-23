import os
import alpaca_trade_api as tradeapi
from alpaca_trade_api.rest import TimeFrame
import pandas as pd
import smtplib
from email.mime.multipart import MIMEMultipart
from email.mime.text import MIMEText

def pairs_trading_algo(self):

  #specify paper trading environment
  os.environ["APCA_API_BASE_URL"] = "https://paper-api.alpaca.markets"

  #insert API credentials
  api = tradeapi.REST('API Key, 'secret key',api_version='v2')
  account = api.get_account()

  #the mail addresses and password
  sender_address = 'mail_id' #fill the newly created id and password
  sender_pass = 'password'
  receiver_address = 'maid_id'

  #setup the MIME
  message = MIMEMultipart()
  message['From'] = "Trading Bot"
  message['To'] = receiver_address
  message['Subject'] = 'Pairs Trading Algo'

  #selection of stocks
  days = 1000
  stock1 = 'ADBE'
  stock2 = 'AAPL'

  #put the historical data into variables
  stock1_barset = api.get_bars(stock1, TimeFrame.Day, limit=days)
  stock2_barset = api.get_bars(stock2, TimeFrame.Day, limit=days)
  stock1_bars = stock1_barset[stock1]
  stock2_bars = stock2_barset[stock2]
  print(stock2_bars)

  #grab stock1 data and put in to an array

  data_1 = []
  times_1 = []

  for i in range(days):
    stock1_close = stock1_bars[i].c
    stock1_time = stock1_bars[i].t
    data_1.append(stock1_close)
    times_1.append(stock1_time)

  #grab stock2 data and put in to an array

  data_2 = []
  times_2 = []

  for i in range(days):
    stock2_close = stock2_bars[i].c
    stock2_time = stock2_bars[i].t
    data_2.append(stock2_close)
    times_2.append(stock2_time)


  #putting them together

  hist_close = pd.DataFrame(data_1, columns=[stock1])
  hist_close[stock2] = data_2

  #current spread between the two stocks
  stock1_curr = data_1[days-1]
  stock2_curr = data_2[days-2]

  spread_curr = (stock1_curr-stock2_curr)

  #moving average of the two stocks
  mov_avg_days = 5

  #moving average for stock1
  stock1_last = []

  for i in range(mov_avg_days):
    stock1_last.append(data_1[(days-1)-i])

  stock1_hist = pd.DataFrame(stock1_last)

  stock1_mavg = stock1_hist.mean()

  #moving average for stock2
  stock2_last = []

  for i in range(mov_avg_days):
    stock2_last.append(data_2[(days-1)-i])

  stock2_hist = pd.DataFrame(stock2_last)

  stock2_mavg = stock2_hist.mean()

  #spread average
  spread_avg = min(stock1_mavg - stock2_mavg)
  #spread factor
  spreadFactor = .01

  wideSpread = spread_avg*(1+spreadFactor)
  thinSpread = spread_avg*(1-spreadFactor)

  #calc of shares to trade

  cash = float(account.buying_power)
  limit_stock1 = cash//stock1_curr
  limit_stock2 = cash//stock2_curr

  number_of_shares = int(min(limit_stock1,limit_stock2)/2)

  #trading algo

  portfolio = api.list_positions()
  clock = api.get_clock()

  if clock.is_open == True:
    if bool(portfolio) == False:
      #detect a widespread
      if spread_curr > wideSpread:
        #short top stock
        api.submit_order(symbol = stock1, qty = number_of_shares, side = 'sell', type = 'market', time_in_force = 'day')
        #long bottom stock
        api.submit_order(symbol = stock2, qty = number_of_shares, side = 'buy', type = 'market', time_in_force = 'day')
        mail_content = "Trades have been made, short top stock and long bottom stock"

      #detect a tight spread
      elif spread_curr < thinSpread:
        #long top stock
        api.submit_order(symbol = stock1, qty = number_of_shares, side = 'buy', type = 'market', time_in_force = 'day')
        #short bottom stock
        api.submit_order(symbol = stock2, qty = number_of_shares, side = 'sell', type = 'market', time_in_force = 'day')
        mail_content = "Trades have been made, long top stock and short bottom stock"
    else:
      wideTradeSpread = spread_avg*(1+spreadFactor + .03)
      thinTradeSpread = spread_avg*(1+spreadFactor - .03)

      if spread_curr <= wideTradeSpread and spread_curr >= thinTradeSpread:
        api.close_position(stock1)
        api.close_position(stock2)
        mail_content = "Position has been closed"
      else:
        mail_content = "No trades were made, position remains open"
        pass
  else:
    mail_content = "The Market is closed"

  #the body and the attachment for the mail
  message.attach(MIMEText(mail_content, 'plain'))
  #create SMTP session for sending the mail
  session = smtplib.SMTP('smtp.gmail.com', 587)
  #enable security
  session.starttls()
  #login with mail_id and password
  session.login(sender_address,sender_pass)
  text = message.as_string()
  session.sendmail(sender_address,receiver_address, text)
  session.quit()

  done = 'Mail Sent'

  return done
