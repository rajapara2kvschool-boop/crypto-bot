import ccxt import pandas as pd import asyncio from telegram import Bot

૧. તમારી સાચી વિગતો
TOKEN = "8965507131:AAFO1bhoQZn0PU3kpsav5Mv_eunXKfDn8tM" CHAT_ID = "698366476"

bot = Bot(token=TOKEN)

async def send_alert(message): try: await bot.send_message(chat_id=CHAT_ID, text=message, parse_mode='Markdown') except Exception as e: print(f"Telegram મોકલવામાં એરર: {e}")

RSI (14) ગણવાની સચોટ રીત
def calculate_rsi(df, window=14): delta = df['close'].diff() gain = (delta.where(delta > 0, 0)).rolling(window=window).mean() loss = (-delta.where(delta < 0, 0)).rolling(window=window).mean() rs = gain / loss return 100 - (100 / (1 + rs))

Bollinger Bands (20, 2) ગણવાની સચોટ રીત
def calculate_bollinger_bands(df, window=20, std_dev=2): sma = df['close'].rolling(window=window).mean() std = df['close'].rolling(window=window).std() lower_band = sma - (std * std_dev) upper_band = sma + (std * std_dev) return lower_band, upper_band

ડેટા ફેચ કરવાનું ફંક્શન
def get_data(exchange, symbol, timeframe, limit=50): ohlcv = exchange.fetch_ohlcv(symbol, timeframe=timeframe, limit=limit) df = pd.DataFrame(ohlcv, columns=['timestamp', 'open', 'high', 'low', 'close', 'volume']) df['rsi'] = calculate_rsi(df) df['lower_band'], df['upper_band'] = calculate_bollinger_bands(df) return df

async def scan_market(): exchange = ccxt.binance() print("🚀 Exact Match Custom Crypto Scanner ચાલુ થઈ ગયું છે...") await send_alert("🚀 Strict Custom Crypto Scanner Active!\nબધી જ શરતો 100% પૂરી થશે ત્યારે જ એલર્ટ મળશે.")

while True:
    try:
        print("\n🔍 Binance માર્કેટ ચકાસી રહ્યા છીએ...")
        markets = exchange.load_markets()
        symbols = [symbol for symbol in markets if symbol.endswith('/USDT')]

        for symbol in symbols[:60]:  # Top 60 Coins
            try:
                # =============================================================
                # 🔴 શરત ૧: 30 મિનિટ (30m BB + RSI Reversal)
                # =============================================================
                df_30m = get_data(exchange, symbol, '30m')
                curr_30m = df_30m.iloc[-1]
                prev_30m = df_30m.iloc[-2]

                # 4 કડક શરતો:
                rsi_cross_25_30m = (prev_30m['rsi'] <= 25) and (curr_30m['rsi'] > 25)  # RSI crossed above 25
                green_candle_30m = curr_30m['close'] > curr_30m['open']               # Close > Open
                high_below_bb_30m = curr_30m['high'] < curr_30m['lower_band']         # High < Lower BB
                close_below_bb_30m = curr_30m['close'] < curr_30m['lower_band']       # Close < Lower BB

                # આ ચારેય સાચી પડે તો જ એલર્ટ આપશે
                if rsi_cross_25_30m and green_candle_30m and high_below_bb_30m and close_below_bb_30m:
                    msg = (
                        f"🟢 *[30 મિનિટ એલર્ટ: BB + RSI REVERSAL]*\n\n"
                        f"📌 *Coin:* `{symbol}`\n"
                        f"💰 *Price:* ${curr_30m['close']}\n"
                        f"📊 *30m RSI:* {round(curr_30m['rsi'], 2)}\n"
                        f"📉 *Lower BB:* {round(curr_30m['lower_band'], 4)}\n"
                        f"⏱️ *Timeframe:* 30 Minutes"
                    )
                    await send_alert(msg)

                # =============================================================
                # 🔵 શરત ૨: 5 મિનિટ (5m BB + RSI Reversal)
                # =============================================================
                df_5m = get_data(exchange, symbol, '5m')
                curr_5m = df_5m.iloc[-1]
                prev_5m = df_5m.iloc[-2]

                # 4 કડક શરતો:
                rsi_cross_25_5m = (prev_5m['rsi'] <= 25) and (curr_5m['rsi'] > 25)     # RSI crossed above 25
                green_candle_5m = curr_5m['close'] > curr_5m['open']                  # Close > Open
                high_below_bb_5m = curr_5m['high'] < curr_5m['lower_band']            # High < Lower BB
                close_below_bb_5m = curr_5m['close'] < curr_5m['lower_band']          # Close < Lower BB

                # આ ચારેય સાચી પડે તો જ એલર્ટ આપશે
                if rsi_cross_25_5m and green_candle_5m and high_below_bb_5m and close_below_bb_5m:
                    msg = (
                        f"🔵 *[5 મિનિટ એલર્ટ: BB + RSI REVERSAL]*\n\n"
                        f"📌 *Coin:* `{symbol}`\n"
                        f"💰 *Price:* ${curr_5m['close']}\n"
                        f"📊 *5m RSI:* {round(curr_5m['rsi'], 2)}\n"
                        f"📉 *Lower BB:* {round(curr_5m['lower_band'], 4)}\n"
                        f"⏱️ *Timeframe:* 5 Minutes"
                    )
                    await send_alert(msg)

                # =============================================================
                # 🟡 શરત ૩: 10 મિનિટ (Multi-Timeframe 2h & 10m RSI)
                # =============================================================
                df_2h = get_data(exchange, symbol, '2h')
                df_10m = get_data(exchange, symbol, '10m') # 10 મિનિટ સેટ કરેલ છે

                curr_2h = df_2h.iloc[-1]
                prev_2h = df_2h.iloc[-2]
                curr_10m = df_10m.iloc[-1]
                prev_10m = df_10m.iloc[-2]

                # 2 કડક શરતો:
                rsi_cross_60_2h = (prev_2h['rsi'] <= 60) and (curr_2h['rsi'] > 60)   # 2h RSI crossed above 60
                rsi_cross_40_10m = (prev_10m['rsi'] <= 40) and (curr_10m['rsi'] > 40) # 10m RSI crossed above 40

                # આ બંને સાચી પડે તો જ એલર્ટ આપશે
                if rsi_cross_60_2h and rsi_cross_40_10m:
                    msg = (
                        f"🟡 *[10 મિનિટ એલર્ટ: MULTI-TIMEFRAME RSI]*\n\n"
                        f"📌 *Coin:* `{symbol}`\n"
                        f"💰 *Price:* ${curr_10m['close']}\n"
                        f"📈 *2 Hours RSI:* {round(curr_2h['rsi'], 2)} (Crossed 60)\n"
                        f"📈 *10 Min RSI:* {round(curr_10m['rsi'], 2)} (Crossed 40)"
                    )
                    await send_alert(msg)

            except Exception as e:
                continue

        print("રાઉન્ડ પૂરો થયો. ૨ મિનિટ પછી ફરી ઓટો-સ્કેન થશે...")
        await asyncio.sleep(120)

    except Exception as e:
        print(f"એરર: {e}")
        await asyncio.sleep(60)
if name == 'main': asyncio.run(scan_market())
