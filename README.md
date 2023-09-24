# algorithmic-trading-bot

This is a algorithmic trading bot that utilizes pairs trade strategy to trade. It automates the trading by taking API key and secret key of your Alpaca trading platform. 

Libraries and technologies used:
1. Alpaca-trade-api
2. Google Cloud Functions
3. Google Colab
4. Python
5. Google Cloud Scheduler

The workflow of the entire project is following:
1. Install the dependencies like Pandas, Numpy, Alpaca Trade API
2. Create an account on Alpaca to get the API key and Secret. (This is the platform where bot will do the paper trading)
3. Create a GCP accoutn and go to the cloud functions
4. Once the Python function is ready.
5. Fill the code in the Cloud functions and test it.
6. Now, once your code is deployed, go to the Cloud Scheduler.
7. In the cloud scheduler, fill in the URL of the function and name of the function along with the details like when to trigger this function i.e, your bot
8. It will trigger the bot at the specified time.
9. Whenever the bot will take any action, it will send the an email to the mentioned email Id in the function.

   
