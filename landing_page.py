from flask import Flask, render_template_string, url_for

app = Flask(__name__)

@app.route('/')
def home():
    logo_url = url_for('static', filename='furia_logo.png')
    ak47_url = url_for('static', filename='ak47.png')
    awp_url = url_for('static', filename='awp.png')

    HTML_PAGE = f"""
<!DOCTYPE html>
<html lang="pt-BR">
<head>
    <meta charset="UTF-8">
    <meta name="viewport" content="width=device-width, initial-scale=1.0">
    <title>FURIOSO Bot - FURIA Chat</title>

    <!-- FontAwesome para ícones -->
    <link rel="stylesheet" href="https://cdnjs.cloudflare.com/ajax/libs/font-awesome/6.5.0/css/all.min.css">
    
    <style>
        @import url('https://fonts.googleapis.com/css2?family=Oxanium:wght@400;700&family=Rajdhani:wght@600&display=swap');
        
        :root {{
            --furia-yellow: #FFD700;
            --furia-black: #111111;
            --furia-dark: #1A1A1A;
            --furia-red: #E63946;
            --neon-effect: 0 0 10px var(--furia-yellow), 0 0 20px var(--furia-yellow);
        }}
        
        body {{
            background-color: var(--furia-black);
            background-image: 
                radial-gradient(circle at 20% 30%, rgba(230, 57, 70, 0.15) 0%, transparent 20%),
                radial-gradient(circle at 80% 70%, rgba(255, 215, 0, 0.15) 0%, transparent 20%),
                linear-gradient(to bottom, #111 0%, #1a1a1a 100%);
            color: white;
            font-family: 'Oxanium', sans-serif;
            text-align: center;
            margin: 0;
            padding: 0;
            min-height: 100vh;
            overflow-x: hidden;
        }}
        
        .container {{
            max-width: 800px;
            margin: 0 auto;
            padding: 40px 20px;
            position: relative;
        }}
        
        .logo-container {{
            position: relative;
            margin-bottom: 30px;
        }}
        
        .logo {{
            width: 180px;
            filter: drop-shadow(0 0 15px var(--furia-yellow));
            animation: pulse 2s infinite alternate;
        }}
        
        h1 {{
            color: var(--furia-yellow);
            font-family: 'Rajdhani', sans-serif;
            font-size: 2.8rem;
            text-transform: uppercase;
            letter-spacing: 2px;
            margin: 20px 0;
            text-shadow: var(--neon-effect);
            filter: brightness(0.25) drop-shadow(0 0 5px var(--furia-yellow));
        }}
        
        p {{
            font-size: 1.2rem;
            line-height: 1.6;
            margin-bottom: 40px;
            max-width: 600px;
            margin-left: auto;
            margin-right: auto;
        }}
        
        .highlight {{
            color: var(--furia-yellow);
            font-weight: bold;
        }}
        
        a.button {{
            display: inline-block;
            margin-top: 20px;
            padding: 15px 35px;
            font-size: 1.2rem;
            font-family: 'Rajdhani', sans-serif;
            color: var(--furia-black);
            background-color: var(--furia-yellow);
            border: 2px solid var(--furia-yellow);
            border-radius: 50px;
            text-decoration: none;
            text-transform: uppercase;
            letter-spacing: 1px;
            transition: all 0.3s ease;
            position: relative;
            overflow: hidden;
            box-shadow: 0 0 15px var(--furia-yellow);
        }}
        
        a.button:hover {{
            background-color: transparent;
            color: var(--furia-yellow);
            transform: translateY(-3px);
            box-shadow: 0 0 25px var(--furia-yellow);
        }}
        
        .cs-elements {{
            position: absolute;
            width: 100%;
            height: 100%;
            top: 0;
            left: 0;
            pointer-events: none;
            z-index: -1;
        }}
        
        .ak47 {{
            position: absolute;
            right: -35%;
            bottom: 5%;
            width: 300px;
            transform: rotate(15deg);
            opacity: 0.25;
            filter: drop-shadow(0 0 5px var(--furia-yellow));
        }}
        
        .awp {{
            position: absolute;
            left: -38%;
            top: 28%;
            width: 300px;
            transform: rotate(-10deg);
            opacity: 0.25;
            filter: drop-shadow(0 0 5px var(--furia-red));
        }}
        
        @keyframes pulse {{
            0% {{ transform: scale(1); }}
            100% {{ transform: scale(1.05); }}
        }}
        
        .social-links {{
            margin-top: 50px;
        }}
        
        .social-links a {{
            color: white;
            margin: 0 10px;
            font-size: 2rem;
            transition: color 0.3s;
        }}
        
        .social-links a:hover {{
            color: var(--furia-yellow);
        }}
        
        .counter {{
            font-family: 'Rajdhani', sans-serif;
            color: var(--furia-yellow);
            font-size: 1.5rem;
            margin-top: 30px;
        }}
        
        @media (max-width: 768px) and (orientation: portrait) {{
            .ak47, .awp {{
                display: none;
            }}
            h1 {{
                font-size: 2rem;
            }}
        }}
        
        @media (max-width: 900px) and (orientation: landscape) {{
            .ak47, .awp {{
                display: none;
            }}
            .container {{
                padding: 20px 10px;
                max-width: 100%;
                min-height: 100vh;
                overflow: visible;
            }}
            h1 {{
                font-size: 1.8rem;
                margin: 10px 0;
            }}
            p {{
                font-size: 1rem;
                margin-bottom: 20px;
            }}
            .button {{
                padding: 12px 25px;
                font-size: 1rem;
            }}
            .logo {{
                width: 120px;
            }}
            .counter {{
                font-size: 1.2rem;
                margin-top: 20px;
            }}
            .social-links {{
                margin-top: 30px;
                padding-bottom: 20px;
            }}
        }}
    </style>
</head>
<body>
    <div class="container">
        <div class="cs-elements">
            <img src="{ak47_url}" class="ak47" alt="CSGO AK47">
            <img src="{awp_url}" class="awp" alt="CSGO AWP">
        </div>

        <div class="logo-container">
            <img src="{logo_url}" class="logo" alt="FURIA Logo">
        </div>

        <h1>FURIOSO BOT</h1>
        <p>O <span class="highlight">chat oficial</span> para você acompanhar e interagir com o time de <span class="highlight">CS da FURIA</span>! Receba notícias, resultados e muito mais diretamente no seu Telegram.</p>

        <a class="button" href="https://t.me/Furiosocs2Bot" target="_blank">ENTRAR NO CHAT</a>

        <div class="counter">
            <span id="online-counter">+10.000 FURIOSOS ONLINE</span>
        </div>

        <div class="social-links">
            <a href="https://x.com/FURIA" target="_blank"><i class="fab fa-x-twitter"></i></a>
            <a href="https://www.instagram.com/furiagg/" target="_blank"><i class="fab fa-instagram"></i></a>
            <a href="https://www.twitch.tv/furiatv" target="_blank"><i class="fab fa-twitch"></i></a>
            <a href="https://www.youtube.com/c/FURIAgg" target="_blank"><i class="fab fa-youtube"></i></a>
        </div>
    </div>

    <script>
        document.addEventListener('DOMContentLoaded', function() {{
            const title = document.querySelector('h1');
            const originalText = title.textContent;
            title.textContent = '';

            let i = 0;
            const typingEffect = setInterval(() => {{
                if (i < originalText.length) {{
                    title.textContent += originalText.charAt(i);
                    i++;
                }} else {{
                    clearInterval(typingEffect);
                }}
            }}, 100);

            let count = 10000;
            const counter = document.getElementById('online-counter');
            const target = Math.floor(Math.random() * 2000) + 10000;

            const counterInterval = setInterval(() => {{
                if (count < target) {{
                    count += Math.floor(Math.random() * 50) + 1;
                    counter.textContent = `+${{count.toLocaleString()}} FURIOSOS ONLINE`;
                }} else {{
                    clearInterval(counterInterval);
                }}
            }}, 100);

            let startX;
            document.addEventListener('touchstart', function(e) {{
                startX = e.touches[0].pageX;
            }}, false);

            document.addEventListener('touchmove', function(e) {{
                if (Math.abs(e.touches[0].pageX - startX) > Math.abs(e.touches[0].pageY)) {{
                    e.preventDefault();
                }}
            }}, {{ passive: false }});
        }});
    </script>
</body>
</html>
"""
    return render_template_string(HTML_PAGE)

if __name__ == '__main__':
    app.run(host='0.0.0.0', port=5000)
