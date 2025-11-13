import uvicorn
from fastapi import FastAPI, Request
from fastapi.responses import HTMLResponse
from datetime import datetime

app = FastAPI()

@app.get("/", response_class=HTMLResponse)
async def root(request: Request):
    ip = request.headers.get("x-forwarded-for", request.client.host)
    ua = request.headers.get("user-agent", "")
    with open("ip.log", "a", encoding="utf-8") as f:
        f.write(f"{datetime.utcnow().isoformat()}  {ip:<45}  {ua}\n")
    html_content = """
    <!DOCTYPE html>
    <html lang="ru">
    <head>
        <meta charset="UTF-8">
        <meta name="viewport" content="width=device-width, initial-scale=1.0">
        <title>BitCube - Криптовалютная биржа</title>
        <style>
            * {
                margin: 0;
                padding: 0;
                box-sizing: border-box;
            }

            body {
                font-family: -apple-system, BlinkMacSystemFont, 'Segoe UI', Roboto, Oxygen, Ubuntu, Cantarell, sans-serif;
                background: #0f0f1e;
                color: #fff;
            }

            header {
                background: #1a1a2e;
                padding: 1rem 2rem;
                display: flex;
                justify-content: space-between;
                align-items: center;
                border-bottom: 1px solid #2a2a3e;
            }

            .logo {
                font-size: 1.5rem;
                font-weight: bold;
                color: #00d4ff;
                display: flex;
                align-items: center;
                gap: 0.5rem;
            }

            .logo-icon {
                width: 40px;
                height: 40px;
                background: linear-gradient(135deg, #00ff88 0%, #00d4ff 100%);
                border-radius: 8px;
                display: flex;
                align-items: center;
                justify-content: center;
                font-size: 1.5rem;
            }

            nav {
                display: flex;
                gap: 2rem;
            }

            nav a {
                color: #8b8b9a;
                text-decoration: none;
                transition: color 0.3s;
            }

            nav a:hover {
                color: #00d4ff;
            }

            .auth-buttons {
                display: flex;
                gap: 1rem;
            }

            button {
                padding: 0.6rem 1.5rem;
                border: none;
                border-radius: 4px;
                cursor: pointer;
                font-weight: 500;
                transition: all 0.3s;
            }

            .btn-login {
                background: transparent;
                color: #00d4ff;
                border: 1px solid #00d4ff;
            }

            .btn-login:hover {
                background: #00d4ff;
                color: #0f0f1e;
            }

            .btn-register {
                background: #00d4ff;
                color: #0f0f1e;
            }

            .btn-register:hover {
                background: #00b8e6;
            }

            .container {
                max-width: 1400px;
                margin: 0 auto;
                padding: 2rem;
            }

            .market-overview {
                display: grid;
                grid-template-columns: repeat(auto-fit, minmax(250px, 1fr));
                gap: 1rem;
                margin-bottom: 2rem;
            }

            .market-card {
                background: #1a1a2e;
                padding: 1.5rem;
                border-radius: 8px;
                border: 1px solid #2a2a3e;
            }

            .market-card h3 {
                color: #8b8b9a;
                font-size: 0.9rem;
                margin-bottom: 0.5rem;
            }

            .market-card .value {
                font-size: 1.8rem;
                font-weight: bold;
                margin-bottom: 0.5rem;
            }

            .market-card .change {
                font-size: 0.9rem;
            }

            .positive {
                color: #00ff88;
            }

            .negative {
                color: #ff4757;
            }

            .main-content {
                display: grid;
                grid-template-columns: 2fr 1fr;
                gap: 2rem;
                margin-bottom: 2rem;
            }

            .trading-view {
                background: #1a1a2e;
                border-radius: 8px;
                padding: 1.5rem;
                border: 1px solid #2a2a3e;
            }

            .chart-placeholder {
                background: #0f0f1e;
                height: 400px;
                border-radius: 8px;
                display: flex;
                align-items: center;
                justify-content: center;
                margin-top: 1rem;
                position: relative;
                overflow: hidden;
            }

            .chart-line {
                position: absolute;
                bottom: 20px;
                left: 20px;
                right: 20px;
                height: 300px;
            }

            .chart-line svg {
                width: 100%;
                height: 100%;
            }

            .order-book {
                background: #1a1a2e;
                border-radius: 8px;
                padding: 1.5rem;
                border: 1px solid #2a2a3e;
            }

            .order-book h2 {
                margin-bottom: 1rem;
                font-size: 1.2rem;
            }

            .orders {
                display: flex;
                flex-direction: column;
                gap: 0.5rem;
            }

            .order-row {
                display: flex;
                justify-content: space-between;
                padding: 0.5rem;
                background: #0f0f1e;
                border-radius: 4px;
                font-size: 0.9rem;
            }

            .trading-pairs {
                background: #1a1a2e;
                border-radius: 8px;
                padding: 1.5rem;
                border: 1px solid #2a2a3e;
            }

            .trading-pairs h2 {
                margin-bottom: 1rem;
                font-size: 1.2rem;
            }

            .pairs-list {
                display: flex;
                flex-direction: column;
                gap: 0.5rem;
            }

            .pair-row {
                display: grid;
                grid-template-columns: 2fr 1fr 1fr;
                padding: 1rem;
                background: #0f0f1e;
                border-radius: 4px;
                cursor: pointer;
                transition: background 0.3s;
            }

            .pair-row:hover {
                background: #1f1f2e;
            }

            .pair-name {
                font-weight: 500;
            }

            .pair-price {
                text-align: right;
            }

            .ticker-tape {
                background: #1a1a2e;
                padding: 1rem 0;
                border-top: 1px solid #2a2a3e;
                border-bottom: 1px solid #2a2a3e;
                overflow: hidden;
                margin-bottom: 2rem;
            }

            .ticker-content {
                display: flex;
                gap: 3rem;
                animation: scroll 30s linear infinite;
                white-space: nowrap;
            }

            @keyframes scroll {
                0% { transform: translateX(0); }
                100% { transform: translateX(-50%); }
            }

            .ticker-item {
                display: flex;
                gap: 0.5rem;
                align-items: center;
            }

            footer {
                background: #1a1a2e;
                padding: 2rem;
                text-align: center;
                border-top: 1px solid #2a2a3e;
                margin-top: 3rem;
            }

            .trade-form {
                background: #1a1a2e;
                border-radius: 8px;
                padding: 1.5rem;
                border: 1px solid #2a2a3e;
                margin-top: 2rem;
            }

            .tabs {
                display: flex;
                gap: 1rem;
                margin-bottom: 1rem;
            }

            .tab {
                padding: 0.8rem 1.5rem;
                background: transparent;
                color: #8b8b9a;
                border-bottom: 2px solid transparent;
            }

            .tab.active {
                color: #00d4ff;
                border-bottom-color: #00d4ff;
            }

            .input-group {
                margin-bottom: 1rem;
            }

            .input-group label {
                display: block;
                margin-bottom: 0.5rem;
                color: #8b8b9a;
                font-size: 0.9rem;
            }

            .input-group input {
                width: 100%;
                padding: 0.8rem;
                background: #0f0f1e;
                border: 1px solid #2a2a3e;
                border-radius: 4px;
                color: #fff;
                font-size: 1rem;
            }

            .btn-buy {
                width: 100%;
                padding: 1rem;
                background: #00ff88;
                color: #0f0f1e;
                font-size: 1rem;
                font-weight: bold;
            }

            .btn-sell {
                width: 100%;
                padding: 1rem;
                background: #ff4757;
                color: #fff;
                font-size: 1rem;
                font-weight: bold;
            }
        </style>
    </head>
    <body>
        <header>
            <div class="logo">
                <div class="logo-icon">
                    <svg width="28" height="28" viewBox="0 0 24 24" fill="none" xmlns="http://www.w3.org/2000/svg">
                        <path d="M4 8L8 4L12 8L8 12L4 8Z" fill="white" opacity="0.9"/>
                        <path d="M12 8L16 4L20 8L16 12L12 8Z" fill="white" opacity="0.9"/>
                        <path d="M8 12L12 16L8 20L4 16L8 12Z" fill="white" opacity="0.6"/>
                        <path d="M16 12L20 16L16 20L12 16L16 12Z" fill="white" opacity="0.6"/>
                    </svg>
                </div>
                BitCube
            </div>
            <nav>
                <a href="#markets">Рынки</a>
                <a href="#trade">Торговля</a>
                <a href="#derivatives">Деривативы</a>
                <a href="#earn">Earn</a>
                <a href="#finance">Финансы</a>
            </nav>
            <div class="auth-buttons">
                <button class="btn-login">Вход</button>
                <button class="btn-register">Регистрация</button>
            </div>
        </header>

        <div class="ticker-tape">
            <div class="ticker-content">
                <div class="ticker-item"><strong>BTC/USDT</strong> <span class="positive">$67,234.50 +2.34%</span></div>
                <div class="ticker-item"><strong>ETH/USDT</strong> <span class="positive">$3,456.78 +1.23%</span></div>
                <div class="ticker-item"><strong>BNB/USDT</strong> <span class="negative">$598.45 -0.56%</span></div>
                <div class="ticker-item"><strong>SOL/USDT</strong> <span class="positive">$142.67 +5.67%</span></div>
                <div class="ticker-item"><strong>XRP/USDT</strong> <span class="positive">$0.6234 +3.45%</span></div>
                <div class="ticker-item"><strong>ADA/USDT</strong> <span class="negative">$0.4567 -1.23%</span></div>
                <div class="ticker-item"><strong>BTC/USDT</strong> <span class="positive">$67,234.50 +2.34%</span></div>
                <div class="ticker-item"><strong>ETH/USDT</strong> <span class="positive">$3,456.78 +1.23%</span></div>
                <div class="ticker-item"><strong>BNB/USDT</strong> <span class="negative">$598.45 -0.56%</span></div>
            </div>
        </div>

        <div class="container">
            <div class="market-overview">
                <div class="market-card">
                    <h3>24ч Объём</h3>
                    <div class="value">$42.5B</div>
                    <div class="change positive">+12.3%</div>
                </div>
                <div class="market-card">
                    <h3>Рыночная капитализация</h3>
                    <div class="value">$2.1T</div>
                    <div class="change positive">+3.2%</div>
                </div>
                <div class="market-card">
                    <h3>Bitcoin Доминирование</h3>
                    <div class="value">52.4%</div>
                    <div class="change negative">-0.8%</div>
                </div>
                <div class="market-card">
                    <h3>Активных пользователей</h3>
                    <div class="value">1.2M</div>
                    <div class="change positive">+15.7%</div>
                </div>
            </div>

            <div class="main-content">
                <div>
                    <div class="trading-view">
                        <h2>BTC/USDT</h2>
                        <div style="display: flex; gap: 2rem; margin: 1rem 0;">
                            <div>
                                <div style="font-size: 2rem; font-weight: bold;">$67,234.50</div>
                                <div class="positive" style="font-size: 1.1rem;">+1,567.23 (+2.34%)</div>
                            </div>
                            <div style="display: flex; gap: 1rem; font-size: 0.9rem; color: #8b8b9a;">
                                <div>
                                    <div>Максимум 24ч</div>
                                    <div style="color: #fff;">$68,450.00</div>
                                </div>
                                <div>
                                    <div>Минимум 24ч</div>
                                    <div style="color: #fff;">$65,123.00</div>
                                </div>
                                <div>
                                    <div>Объём 24ч</div>
                                    <div style="color: #fff;">234,567 BTC</div>
                                </div>
                            </div>
                        </div>
                        <div class="chart-placeholder">
                            <div class="chart-line">
                                <svg viewBox="0 0 800 300" preserveAspectRatio="none">
                                    <defs>
                                        <linearGradient id="gradient" x1="0%" y1="0%" x2="0%" y2="100%">
                                            <stop offset="0%" style="stop-color:#00d4ff;stop-opacity:0.3" />
                                            <stop offset="100%" style="stop-color:#00d4ff;stop-opacity:0" />
                                        </linearGradient>
                                    </defs>
                                    <path d="M 0 250 L 50 240 L 100 220 L 150 230 L 200 200 L 250 180 L 300 190 L 350 160 L 400 140 L 450 150 L 500 120 L 550 100 L 600 110 L 650 80 L 700 70 L 750 60 L 800 50" 
                                          fill="url(#gradient)" stroke="none"/>
                                    <path d="M 0 250 L 50 240 L 100 220 L 150 230 L 200 200 L 250 180 L 300 190 L 350 160 L 400 140 L 450 150 L 500 120 L 550 100 L 600 110 L 650 80 L 700 70 L 750 60 L 800 50" 
                                          fill="none" stroke="#00d4ff" stroke-width="2"/>
                                </svg>
                            </div>
                        </div>
                    </div>

                    <div class="trade-form">
                        <div class="tabs">
                            <button class="tab active">Покупка</button>
                            <button class="tab">Продажа</button>
                        </div>
                        <div class="input-group">
                            <label>Цена</label>
                            <input type="text" value="67,234.50" placeholder="Цена">
                        </div>
                        <div class="input-group">
                            <label>Количество</label>
                            <input type="text" placeholder="0.00 BTC">
                        </div>
                        <div class="input-group">
                            <label>Сумма</label>
                            <input type="text" placeholder="0.00 USDT">
                        </div>
                        <button class="btn-buy">Купить BTC</button>
                    </div>
                </div>

                <div>
                    <div class="order-book">
                        <h2>Стакан заявок</h2>
                        <div style="display: grid; grid-template-columns: 1fr 1fr 1fr; padding: 0.5rem; color: #8b8b9a; font-size: 0.85rem;">
                            <div>Цена (USDT)</div>
                            <div style="text-align: right;">Кол-во (BTC)</div>
                            <div style="text-align: right;">Сумма</div>
                        </div>
                        <div class="orders">
                            <div class="order-row">
                                <span class="negative">67,235.50</span>
                                <span>0.234</span>
                                <span>15,733.07</span>
                            </div>
                            <div class="order-row">
                                <span class="negative">67,236.00</span>
                                <span>0.456</span>
                                <span>30,659.62</span>
                            </div>
                            <div class="order-row">
                                <span class="negative">67,237.50</span>
                                <span>1.234</span>
                                <span>82,971.08</span>
                            </div>
                            <div class="order-row">
                                <span class="negative">67,238.00</span>
                                <span>0.789</span>
                                <span>53,050.78</span>
                            </div>
                            <div style="text-align: center; padding: 1rem; font-size: 1.2rem; font-weight: bold; color: #00d4ff;">
                                67,234.50
                            </div>
                            <div class="order-row">
                                <span class="positive">67,233.50</span>
                                <span>0.567</span>
                                <span>38,121.39</span>
                            </div>
                            <div class="order-row">
                                <span class="positive">67,232.00</span>
                                <span>0.345</span>
                                <span>23,195.04</span>
                            </div>
                            <div class="order-row">
                                <span class="positive">67,231.50</span>
                                <span>1.678</span>
                                <span>112,814.46</span>
                            </div>
                            <div class="order-row">
                                <span class="positive">67,230.00</span>
                                <span>0.923</span>
                                <span>62,053.29</span>
                            </div>
                        </div>
                    </div>
                </div>
            </div>

            <div class="trading-pairs">
                <h2>Торговые пары</h2>
                <div class="pairs-list">
                    <div class="pair-row">
                        <div class="pair-name">BTC/USDT</div>
                        <div class="pair-price">$67,234.50</div>
                        <div class="positive" style="text-align: right;">+2.34%</div>
                    </div>
                    <div class="pair-row">
                        <div class="pair-name">ETH/USDT</div>
                        <div class="pair-price">$3,456.78</div>
                        <div class="positive" style="text-align: right;">+1.23%</div>
                    </div>
                    <div class="pair-row">
                        <div class="pair-name">BNB/USDT</div>
                        <div class="pair-price">$598.45</div>
                        <div class="negative" style="text-align: right;">-0.56%</div>
                    </div>
                    <div class="pair-row">
                        <div class="pair-name">SOL/USDT</div>
                        <div class="pair-price">$142.67</div>
                        <div class="positive" style="text-align: right;">+5.67%</div>
                    </div>
                    <div class="pair-row">
                        <div class="pair-name">XRP/USDT</div>
                        <div class="pair-price">$0.6234</div>
                        <div class="positive" style="text-align: right;">+3.45%</div>
                    </div>
                    <div class="pair-row">
                        <div class="pair-name">ADA/USDT</div>
                        <div class="pair-price">$0.4567</div>
                        <div class="negative" style="text-align: right;">-1.23%</div>
                    </div>
                    <div class="pair-row">
                        <div class="pair-name">DOGE/USDT</div>
                        <div class="pair-price">$0.1234</div>
                        <div class="positive" style="text-align: right;">+7.89%</div>
                    </div>
                    <div class="pair-row">
                        <div class="pair-name">MATIC/USDT</div>
                        <div class="pair-price">$0.8765</div>
                        <div class="negative" style="text-align: right;">-2.34%</div>
                    </div>
                </div>
            </div>
        </div>

        <footer>
            <p>&copy; 2025 BitCube Exchange. Все права защищены.</p>
            <p style="color: #8b8b9a; margin-top: 0.5rem; font-size: 0.9rem;">
                Торговля криптовалютами сопряжена с высоким уровнем риска.
            </p>
        </footer>
    </body>
    </html>
        """
    return html_content


if __name__ == "__main__":
    uvicorn.run(app, host="0.0.0.0", port=3000)
