Taste Test Project

This project uses three different scripts running at the same time to swap AVAX to USDC on a sell order and swap USDC to AVAX on a buy order.  The buy trigger is when the 10 minute SMA becomes greater than the 20 minute SMA and the sell trigger is likewise when the 10 minute SMA is less than the 20 minute SMA.  I used the Alpaca free websocket to stream the AVAX price, calculate the SMAs, and when a trade event occurs it triggers the `selenium_trader.py` to make the swap!

To run this project you will need to:
1. Install the requirements
2. Download the mobile app apk
3. Write your own script to approve the transactions automatically using detox or appium
4. Create a api_config.py file to store your Alpaca keys/secrets
5. Put a breakpoint right before the WalletConnect step
6. Run the selenium script in the python debugger and connect the mobile app manually at the break point
7. Resume the selenium script
8. Run the approval script for the mobile app.  I have a script running in a `while true` loop that looks for the approval button and taps it when it appears on screen.  I have not included this script due to copyright issues but it should be simple enough if you want to try and get the project to run.
9. Run the trade_signal.py script 
