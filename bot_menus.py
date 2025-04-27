from telegram import Update, InlineKeyboardButton, InlineKeyboardMarkup
from telegram.ext import (
    CommandHandler,
    CallbackQueryHandler,
    MessageHandler,
    filters,
    ContextTypes
)
from telegram.constants import ChatAction
from bot_scrapers import fetch_latest_news, fetch_team_data, fetch_last_matches, fetch_upcoming_tournaments
import random
import asyncio
from collections import deque
import logging

logger = logging.getLogger(__name__)

# ========== CONSTANTES ==========
SAUDACOES = [
    "🔥 Olá, FURIA-FÃ! Eu me chamo FURIOSO Bot!! Vamos acompanhar tudo sobre a FURIA CS juntos?",
    "⚡ E aí, fã da FURIA CS! Eu me chamo FURIOSO Bot!! Pronto para as melhores informações?",
    "👋 Fala player! Eu me chamo FURIOSO Bot!! Quer saber tudo sobre a FURIA CS?",
    "💛🖤 Bem-vindo ao universo FURIA CS! Eu me chamo FURIOSO Bot!! Vamos começar?"
]

RESPOSTAS_INVALIDAS = deque([
    "🤔 Eu sou um bot de menu, não entendo texto. Vamos usar os botões?",
    "😅 Melhor navegar pelos botões do menu, que tal?",
    "⚠️ Ops! Só consigo responder quando você usa os botões do menu",
    "🎮 Vamos jogar conforme as regras? Use os botões abaixo, por favor!",
    "🤖 Parece que você digitou algo... Eu funciono melhor com os botões!",
    "🎮 Ei, fera da FURIA! Vamos usar os botões do menu?",
    "🔍 Quase lá! Eu só entendo os botões do menu, vamos tentar?",
    "⚡ Vamos de botões? É mais rápido e fácil!",
    "😅 Sou um bot simples - botões sim, texto não!",
    "💡 Dica: use os botões abaixo para navegar facilmente!"
])

MENU_PRINCIPAL = """
    ⚡                 *MENU PRINCIPAL                ⚡\n\n
Aqui você encontra tudo sobre a FURIA CS!\n\n
Escolha uma opção abaixo para começar👇*
    """

# ========== ESTADO DO CHAT ==========
chat_states = {}

# ========== HANDLERS PRINCIPAIS ==========
async def start(update: Update, context: ContextTypes.DEFAULT_TYPE):
    chat_id = update.effective_chat.id
    
    await context.bot.send_chat_action(chat_id=chat_id, action=ChatAction.TYPING)
    await asyncio.sleep(0.5)
    
    saudacao = random.choice(SAUDACOES)
    await context.bot.send_message(chat_id=chat_id, text=saudacao)
    
    chat_states[chat_id] = {'welcome_sent': True}
    await mostrar_menu(update, context)

async def mostrar_menu(update: Update, context: ContextTypes.DEFAULT_TYPE):
    keyboard = [
        [InlineKeyboardButton("📱 Redes Sociais", callback_data='redes')],
        [InlineKeyboardButton("🛍️ Loja Oficial", callback_data='shop')],
        [InlineKeyboardButton("👥 Equipe Atual", callback_data='equipe')],
        [InlineKeyboardButton("📰 Principais Notícias", callback_data='noticias')],
        [InlineKeyboardButton("📊 Últimos Resultados", callback_data='resultados')],
        [InlineKeyboardButton("🏆 Próximos Campeonatos", callback_data='proximos')]
    ]
    
    reply_markup = InlineKeyboardMarkup(keyboard)
    
    await context.bot.send_message(
        chat_id=update.effective_chat.id,
        text=MENU_PRINCIPAL,
        reply_markup=reply_markup,
        parse_mode='Markdown'
    )

async def handle_invalid_input(update: Update, context: ContextTypes.DEFAULT_TYPE):
    chat_id = update.effective_chat.id
    
    if chat_id not in chat_states or not chat_states[chat_id].get('welcome_sent'):
        await start(update, context)
        return
    
    RESPOSTAS_INVALIDAS.rotate(-1)
    resposta = RESPOSTAS_INVALIDAS[0]
    
    await context.bot.send_message(chat_id=chat_id, text=resposta)
    await mostrar_menu(update, context)

# ========== HANDLERS DE CALLBACK ==========
async def button_handler(update: Update, context: ContextTypes.DEFAULT_TYPE):
    query = update.callback_query
    await query.answer()
    
    logger.info(f"Botão pressionado: {query.data}")
    
    try:
        await context.bot.send_chat_action(
            chat_id=query.message.chat_id,
            action=ChatAction.TYPING
        )
        await asyncio.sleep(0.3)

        handler = {
            'redes': show_redes_sociais,
            'shop': show_shop,
            'equipe': show_equipe_atual,
            'noticias': show_noticias,
            'resultados': show_ultimos_resultados,
            'proximos': show_proximos_campeonatos,
            'menu': mostrar_menu
        }.get(query.data)

        if handler:
            if handler == mostrar_menu:
                await handler(update, context)
            else:
                await handler(query, context)
        else:
            await context.bot.send_message(
                chat_id=query.message.chat_id,
                text="⚠️ Comando não reconhecido. Voltando ao menu..."
            )
            await mostrar_menu(update, context)

    except Exception as e:
        logger.error(f"Erro no button_handler: {str(e)}")
        await context.bot.send_message(
            chat_id=query.message.chat_id,
            text="⚠️ Ocorreu um erro ao processar sua requisição."
        )
        await mostrar_menu(update, context)

# ========== FUNÇÕES DE EXIBIÇÃO ==========
async def show_redes_sociais(query, context):
    texto = (
    "🔥 *SIGA A FURIA EM TODAS AS PLATAFORMAS!* 🔥\n\n"
    "Acompanhe os jogadores, veja conteúdos exclusivos e não perca nenhuma atualização da equipe mais vibrante do cenário de CS!\n\n"
    "💛 *Redes Sociais Oficiais* 🖤\n"
)
    redes = [
        ("𝕏 Twitter (X)", "https://x.com/FURIA"),
        ("📸 Instagram", "https://www.instagram.com/furiagg/"),
        ("📘 Facebook", "https://www.facebook.com/furiagg"),
        ("📺 YouTube", "https://www.youtube.com/c/FURIAgg"),
        ("🎵 TikTok", "https://www.tiktok.com/@furiagg")
    ]
    
    await context.bot.send_message(
        chat_id=query.message.chat_id,
        text=texto,
        parse_mode='Markdown',
        reply_markup=InlineKeyboardMarkup(
            [[InlineKeyboardButton(nome, url=url)] for nome, url in redes] +
            [[InlineKeyboardButton("🔙 Voltar ao Menu", callback_data='menu')]]
        )
    )

async def show_shop(query, context):
    try:
        texto = (
            "🛍️          *LOJA OFICIAL DA FURIA*         🛍️\n\n"
            "Confira nossos produtos exclusivos e mostre seu apoio à equipe!🔥\n\n"
            "*Algumas categorias disponíveis:*"
        )
        
        await context.bot.send_message(
            chat_id=query.message.chat_id,
            text=texto,
            parse_mode='Markdown',
            reply_markup=InlineKeyboardMarkup([
                # Botão principal
                [InlineKeyboardButton("🌐 Loja Completa", url='https://www.furia.gg/produtos')],
                
                # Primeira linha de vestuário
                [
                    InlineKeyboardButton("👕 Camisetas", url='https://www.furia.gg/produtos/vestuario/camisetas'),
                    InlineKeyboardButton("🧥 Jaquetas", url='https://www.furia.gg/produtos/vestuario/jaquetas')
                ],
                
                # Segunda linha de vestuário
                [
                    InlineKeyboardButton("👖 Calças", url='https://www.furia.gg/produtos/vestuario/calcas'),
                    InlineKeyboardButton("🩳 Shorts", url='https://www.furia.gg/produtos/vestuario/shorts')
                ],
                
                # Terceira linha de vestuário
                [
                    InlineKeyboardButton("👚 Croppeds", url='https://www.furia.gg/produtos/vestuario/croppeds'),
                    InlineKeyboardButton("🧣 Moletons", url='https://www.furia.gg/produtos/vestuario/moletons')
                ],
                
                # Primeira linha de acessórios
                [
                    InlineKeyboardButton("🧢 Bonés", url='https://www.furia.gg/produtos/acessorios/bones'),
                    InlineKeyboardButton("🧦 Meias", url='https://www.furia.gg/produtos/acessorios/meias')
                ],
                
                # Segunda linha de acessórios
                [
                    InlineKeyboardButton("🧢 Buckets", url='https://www.furia.gg/produtos/acessorios/buckets'),
                    InlineKeyboardButton("🎒 Mochilas", url='https://www.furia.gg/produtos/acessorios/mochilas')
                ],
                
                # Botão de voltar
                [InlineKeyboardButton("🔙 Voltar", callback_data='menu')]
            ])
        )
    except Exception as e:
        logger.error(f"Erro em show_shop: {str(e)}")
        await context.bot.send_message(
            chat_id=query.message.chat_id,
            text="⚠️ Ocorreu um erro ao acessar a loja. Tente novamente mais tarde.",
            reply_markup=InlineKeyboardMarkup([
                [InlineKeyboardButton("🔙 Voltar ao Menu", callback_data='menu')]
            ])
        )

async def show_equipe_atual(query, context):
    try:
        await context.bot.send_chat_action(
            chat_id=query.message.chat_id,
            action=ChatAction.TYPING
        )
        
        team_info = await fetch_team_data()
        
        if team_info:
            texto = "👥 *Equipe Atual da FURIA CS2* 👥\n\n" + "\n".join(team_info) + \
                   "\n🔗 [Veja mais no HLTV](https://www.hltv.org/team/8297/furia#tab-rosterBox)"
        else:
            texto = "⚠️ Não foi possível obter a equipe atual. Tente novamente mais tarde."
        
        await context.bot.send_message(
            chat_id=query.message.chat_id,
            text=texto,
            parse_mode='Markdown',
            reply_markup=InlineKeyboardMarkup([
                [InlineKeyboardButton("🔙 Voltar ao Menu", callback_data='menu')]
            ])
        )
    except Exception as e:
        logger.error(f"Erro em show_equipe_atual: {str(e)}")
        await context.bot.send_message(
            chat_id=query.message.chat_id,
            text="⚠️ Ocorreu um erro ao buscar os dados da equipe."
        )

async def show_noticias(query, context):
    chat_id = query.message.chat_id
    
    try:
        await context.bot.send_chat_action(chat_id=chat_id, action=ChatAction.TYPING)
        temp_msg = await context.bot.send_message(chat_id, "🔍 Buscando as últimas notícias! Um segundinho ae 😅...")
        
        news = await fetch_latest_news()
        
        await context.bot.delete_message(chat_id=chat_id, message_id=temp_msg.message_id)
        
        if not news:
            await context.bot.send_message(
                chat_id=chat_id,
                text="⚠️ Não foi possível carregar as notícias no momento",
                reply_markup=InlineKeyboardMarkup([
                    [InlineKeyboardButton("🌐 Acessar Site", url='https://themove.gg/esports/cs')],
                    [InlineKeyboardButton("🔙 Voltar ao Menu", callback_data='menu')]
                ])
            )
            return
        
        message = ["<b>📰 ÚLTIMAS NOTÍCIAS DA FURIA</b>\n"]
        for idx, item in enumerate(news, 1):
            date_str = f" ({item['date']})" if item['date'] else ""
            message.append(f"{idx}. <a href='{item['link']}'>{item['title']}</a>{date_str}\n")

        message.append("\n🔍 Mais notícias: <a href='https://themove.gg/esports/cs'>THE MOVE</a>")
        
        await context.bot.send_message(
            chat_id=chat_id,
            text="\n".join(message),
            parse_mode='HTML',
            disable_web_page_preview=False,
            reply_markup=InlineKeyboardMarkup([
                [InlineKeyboardButton("🔙 Voltar ao Menu", callback_data='menu')]
            ])
        )
    except Exception as e:
        logger.error(f"Erro em show_noticias: {str(e)}")
        await context.bot.send_message(
            chat_id=chat_id,
            text="⚠️ Ocorreu um erro inesperado."
        )

async def show_ultimos_resultados(query, context):
    try:
        await context.bot.send_chat_action(
            chat_id=query.message.chat_id,
            action=ChatAction.TYPING
        )
        
        matches = await fetch_last_matches()
        
        if matches:
            texto = "⚡ *ÚLTIMOS JOGOS DA FURIA CS* ⚡\n\n"
            for match in matches:
                texto += (
                    f"📅 *Data*: {match['Data']}\n"
                    f"🏆 *Torneio*: {match['Torneio']} ({match['Tier']})\n"
                    f"🆚 *Adversário*: {match['Adversário']}\n"
                    f"🏁 *Placar*: {match['Placar']}\n"
                    f"────────────────────\n"
                )
            
            texto += "\n🔍 Mais detalhes: [DRAFT5](https://draft5.gg/equipe/330-FURIA/resultados)"
        else:
            texto = "⚠️ Não foi possível obter os últimos jogos."
        
        await context.bot.send_message(
            chat_id=query.message.chat_id,
            text=texto,
            parse_mode='Markdown',
            reply_markup=InlineKeyboardMarkup([
                [InlineKeyboardButton("🔙 Voltar ao Menu", callback_data='menu')]
            ])
        )
    except Exception as e:
        logger.error(f"Erro em show_ultimos_resultados: {str(e)}")
        await context.bot.send_message(
            chat_id=query.message.chat_id,
            text="⚠️ Ocorreu um erro ao buscar os jogos."
        )

async def show_proximos_campeonatos(query, context):
    chat_id = query.message.chat_id
    
    try:
        loading_msg = await context.bot.send_message(
            chat_id=chat_id,
            text="⏳ Um segundinho... tô fazendo uma busca pra você! 😊"
        )
        
        tournaments = await fetch_upcoming_tournaments()
        
        await context.bot.delete_message(chat_id=chat_id, message_id=loading_msg.message_id)
        
        if not tournaments:
            await context.bot.send_message(
                chat_id=chat_id,
                text="😕 Nenhum torneio encontrado no momento",
                reply_markup=InlineKeyboardMarkup([
                    [InlineKeyboardButton("🔙 Voltar ao Menu", callback_data='menu')]
                ])
            )
            return
            
        response = ["🏆         *Próximos Campeonatos*         🏆\n"]
        for t in tournaments:
            response.append(
                f"\n🎮 *{t['name']}*\n"
                f"📅 {t['date']}\n"
                f"⏳ {t['status']}\n"
                f"🔗 [Detalhes]({t['link']})\n"
                f"――――――――――"
            )
            
        response.append("\n🔍 [Ver todos os campeonatos AQUI!](https://draft5.gg/equipe/330-FURIA/campeonatos)")
        
        await context.bot.send_message(
            chat_id=chat_id,
            text="\n".join(response),
            parse_mode='Markdown',
            reply_markup=InlineKeyboardMarkup([
                [InlineKeyboardButton("🔙 Voltar ao Menu", callback_data='menu')]
            ])
        )
    except Exception as e:
        logger.error(f"Erro em show_proximos_campeonatos: {str(e)}")
        await context.bot.send_message(
            chat_id=chat_id,
            text="⚠️ Ocorreu um erro na busca."
        )

# ========== CONFIGURAÇÃO DOS HANDLERS ==========
def setup_handlers(app):
    app.add_handler(CommandHandler("start", start))
    app.add_handler(CallbackQueryHandler(button_handler))
    app.add_handler(MessageHandler(filters.TEXT & ~filters.COMMAND, handle_invalid_input))
    app.add_handler(MessageHandler(
        filters.AUDIO | filters.VOICE | filters.Document.ALL,
        handle_invalid_input
    ))
    app.add_handler(MessageHandler(
        filters.ATTACHMENT | filters.PHOTO | filters.VIDEO,
        handle_invalid_input
    ))