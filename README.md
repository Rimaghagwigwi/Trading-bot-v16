# RSI Backtest – From a Real Binance Trading Bot

⚠️ This repository contains **only the backtesting module** of a complete trading bot that runs live on Binance with real funds.

The full version includes:
- Live trading with Binance API (spot only)
- RSI-based strategy, and the possibility to easily add more conditions
- Configurable parameters (symbol, timeframe, RSI thresholds, etc.)
- Signal-only mode or full auto-execution

📄 More details and backtest results here:  
👉 [Notion page with screenshots & performance](https://regal-friday-0d4.notion.site/Rimagh-s-Trading-bot-246031a720ff80b2b35bd602251ed6cb)

🔗 The full version of the bot is available for purchase:  
👉 [Gumroad – RSI Bot for Binance](https://akamisuta.gumroad.com/)

This repo is meant for **educational and transparency purposes**, and as a technical preview of the complete product.

# 🚀 CRYPTO TRADING BOT - Complete Beginner's Guide

> **⚠️ IMPORTANT:** This bot uses real money! ALWAYS start in TEST mode before using real funds.

## 📋 Table of Contents
1. [What is this?](#what-is-this-)
2. [What do I need?](#what-do-i-need-)
3. [Step-by-step Installation](#step-by-step-installation)
4. [Binance Setup](#binance-setup)
5. [First Launch](#first-launch)
6. [How does it work?](#how-does-it-work-)
7. [Going Live (Real Trading)](#going-live-real-trading)
8. [Common Problems](#common-problems)

---

## What is this? 🤔

This trading bot automatically buys and sells cryptocurrencies using the RSI indicator:
- 📈 **RSI < 30** → Bot buys (potentially low price)
- 📉 **RSI > 70** → Bot sells (potentially high price)
- 🔄 It monitors the market 24/7 for you

**Supported Cryptos:** Bitcoin (BTC), Ethereum (ETH), Ripple (XRP), Dogecoin (DOGE), USDC, USDT

---

## What do I need? 📦

### 1. A computer with Internet
- Windows, Mac, or Linux
- Stable internet connection

### 2. A Binance account
- Create account at [binance.com](https://binance.com)
- Complete identity verification (required)
- Deposit some funds (start small!)

### 3. Python installed
- Download Python 3.10+ from [python.org](https://python.org)
- ✅ Check "Add to PATH" during installation

### 4. A text editor
- Notepad++ (Windows) or TextEdit (Mac) works fine
- Or VS Code for better experience

---

## Step-by-step Installation 🛠️

### Step 1: Download the bot
1. Download the ZIP file
2. Extract the file to your Desktop
3. You should have a `crypto_trading_bot` folder

### Step 2: Open Terminal/Command Prompt

**Windows:**
1. Press `Windows + R`
2. Type `cmd` and press Enter
3. Navigate to folder: `cd Desktop/crypto_trading_bot`

**Mac:**
1. Press `Cmd + Space`
2. Type `Terminal` and press Enter
3. Navigate to folder: `cd Desktop/crypto_trading_bot`

**Linux:**
1. Press `Ctrl + Alt + T`
2. Navigate to folder: `cd Desktop/crypto_trading_bot`

### Step 3: Install dependencies
In the terminal, type exactly:
```bash
pip install -r requirements.txt
```

⏱️ **Wait** for installation to complete (2-3 minutes)

---

## Binance Setup 🔑

### Step 1: Create API Keys

1. **Log in** to your Binance account
2. **Click** your profile (top right)
3. **Select** "API Management"
4. **Click** "Create API"
5. **Name** your API: "Trading Bot"
6. **Check** permissions:
   - ✅ Enable Reading
   - ✅ Enable Spot & Margin Trading
   - ❌ Leave everything else unchecked
7. **Write down** your API Key and Secret Key (keep them SECRET!)

### Step 2: Configure the .env file

1. **Open** the `.env` file with a text editor
2. **Replace** these lines:

```env
# BEFORE (example)
BINANCE_API_KEY=your_api_key_here
BINANCE_SECRET_KEY=your_secret_key_here

# AFTER (with your real keys)
BINANCE_API_KEY=AbCdEf123456789...
BINANCE_SECRET_KEY=XyZ987654321...
```

3. **Keep** `TESTNET=true` to start!
4. **Save** the file

> 🔒 **SECURITY:** NEVER share your API keys with anyone!

---

## First Launch 🚀

### Step 1: Start the bot

In the terminal, type:
```bash
python main.py
```

### Step 2: Interactive setup

The bot will ask you simple questions:

```
⚡️ CRYPTO TRADING BOT ⚡️
========================================
📈 Trading pair (ex: BTCUSDT): BTCUSDT
📊 RSI Overbought (default 70): 70
📊 RSI Oversold (default 30): 30
💰 Amount per trade in USDT (default 50): 25

🚀 Starting bot on BTCUSDT
📊 RSI: 30 / 70
💰 Amount: 25 USDT
Press Ctrl+C to stop
```

### Step 3: What you'll see

The bot will start and show messages like:
```
14:32:15 - INFO - 🚀 Bot started on BTCUSDT
14:32:45 - INFO - ⚪ BTCUSDT - No signal - RSI: 45.67 - Price: 67850.23
14:33:15 - INFO - ⚪ BTCUSDT - No signal - RSI: 44.12 - Price: 67920.45
14:33:45 - INFO - 🟢 BTCUSDT - BUY Signal - RSI: 28.43 - Price: 67650.12
14:33:46 - INFO - [SIMULATION] BUY 0.000369 BTCUSDT
14:33:46 - INFO - ✅ PURCHASE EXECUTED: 0.000369 BTCUSDT at 67650.12
```

---

## How does it work? 🧠

### The RSI Indicator
- **RSI** = Relative Strength Index (0-100 scale)
- **Below 30** = Asset might be "oversold" (good time to buy)
- **Above 70** = Asset might be "overbought" (good time to sell)

### Bot Logic
1. **Every 30 seconds**, the bot checks the RSI
2. **If RSI < 30** and no position → **BUY**
3. **If RSI > 70** and holding position → **SELL**
4. **Otherwise** → Wait and monitor

### Example Trading Cycle
```
Price: $67,000 | RSI: 75 → 🔴 SELL (if holding)
Price: $65,000 | RSI: 45 → ⚪ WAIT
Price: $63,000 | RSI: 25 → 🟢 BUY
Price: $68,000 | RSI: 72 → 🔴 SELL
```

---

## Going Live (Real Trading) ⚠️

### BEFORE going live:

1. **Test thoroughly** in simulation mode
2. **Start with small amounts** ($10-50)
3. **Understand the risks** - you can lose money!
4. **Monitor the bot** regularly

### To enable real trading:

1. **Open** the `.env` file
2. **Change** `TESTNET=true` to `TESTNET=false`
3. **Save** and restart the bot

```env
# Simulation mode
TESTNET=true

# Real trading mode
TESTNET=false
```

### 🚨 Risk Warning
- **Crypto is volatile** - prices can change rapidly
- **The bot can lose money** - no strategy is 100% profitable
- **Start small** - never risk more than you can afford to lose
- **Monitor regularly** - don't leave it unattended for days

---

## Common Problems 🔧

### Problem: "ModuleNotFoundError"
**Solution:** Install dependencies again
```bash
pip install -r requirements.txt
```

### Problem: "Invalid API Key"
**Solution:** 
1. Check your `.env` file has correct keys
2. Make sure API permissions are enabled in Binance
3. Wait 5 minutes after creating API keys

### Problem: "Insufficient Balance"
**Solution:**
1. Deposit funds to your Binance account
2. Reduce the trading amount
3. Check you're trading the right pair

### Problem: Bot stops suddenly
**Solution:**
1. Check your internet connection
2. Look at the error message in terminal
3. Restart the bot: `python main.py`

### Problem: "Permission denied" on files
**Solution:**
1. **Windows:** Right-click folder → Properties → Uncheck "Read-only"
2. **Mac/Linux:** Run `chmod 755 crypto_trading_bot`

### Problem: Python not found
**Solution:**
1. Reinstall Python from [python.org](https://python.org)
2. Make sure to check "Add to PATH"
3. Restart your computer
4. Try `python3 main.py` instead

---

## Understanding the Logs 📊

### Color Meanings:
- 🟢 **Green:** Good news (buy signals, successful trades)
- 🔴 **Red:** Action needed (sell signals, errors)
- ⚪ **White:** Information (monitoring, waiting)
- 🟡 **Yellow:** Warnings (low balance, issues)

### Example Log Breakdown:
```
14:32:15 - INFO - 🚀 Bot started on BTCUSDT
```
- `14:32:15` = Time
- `INFO` = Message type
- `🚀 Bot started on BTCUSDT` = What happened

---

## Customization Options ⚙️

### Change RSI Settings:
- **More sensitive:** RSI 20/80 (more trades, more risk)
- **Less sensitive:** RSI 25/75 (fewer trades, more selective)
- **Default:** RSI 30/70 (balanced)

### Change Trading Amount:
- **Conservative:** $10-25 per trade
- **Moderate:** $50-100 per trade
- **Aggressive:** $200+ per trade

### Change Trading Pairs:
Supported pairs:
- `BTCUSDT` (Bitcoin)
- `ETHUSDT` (Ethereum)
- `XRPUSDT` (Ripple)
- `DOGEUSDT` (Dogecoin)
- `USDCUSDT` (USD Coin)

---

## Getting Help 🆘

### Before asking for help:
1. ✅ Read this guide completely
2. ✅ Check the "Common Problems" section
3. ✅ Try restarting the bot
4. ✅ Make sure you're in TESTNET mode

### What to include when asking for help:
- Your operating system (Windows/Mac/Linux)
- The exact error message
- What you were trying to do
- Screenshots of the terminal

---

## Final Tips 💡

### ✅ DO:
- Start in simulation mode
- Use small amounts initially
- Monitor the bot regularly
- Keep your API keys secret
- Test with different RSI settings
- Read crypto market news

### ❌ DON'T:
- Risk money you can't afford to lose
- Leave the bot unattended for days
- Share your API keys
- Jump straight to large amounts
- Panic during market volatility
- Expect guaranteed profits

### 🎯 Success Tips:
1. **Paper trade first** - practice without real money
2. **Start small** - $10-25 trades to learn
3. **Be patient** - good trades take time
4. **Stay informed** - understand what you're trading
5. **Set limits** - decide max daily/weekly losses
6. **Keep learning** - crypto markets are always evolving

---

## 📞 Support

If you're still stuck after reading this guide:
Contact me at [MAIL ONLY AVAILABLE FOR PAID USERS]

**Remember:** Trading crypto carries risk. This bot is a tool, not a guarantee of profits. Always trade responsibly!

---

*Good luck with your crypto trading journey! 🚀*
