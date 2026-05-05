import os
from flask import Flask, request
from telegram import InlineKeyboardButton, InlineKeyboardMarkup, Update
from telegram.ext import (
    Application,
    CommandHandler,
    CallbackQueryHandler,
    ContextTypes,
)

# ======================
# CONFIGURAÇÕES
# ======================

TOKEN = os.getenv("TOKEN")  # Defina no Render como variável de ambiente

LINK_SEMANAL = "https://mpago.la/1LEY4CP"
LINK_MENSAL = "https://mpago.la/2oL26cr"

# ======================
# FLASK APP
# ======================

app = Flask(__name__)
application = Application.builder().token(TOKEN).build()

@app.route("/")
def home():
    return "🤖 Bot está rodando no Render!"

@app.route(f"/{TOKEN}", methods=["POST"])
def webhook():
    update = Update.de_json(request.get_json(force=True), application.bot)
    application.update_queue.put(update)
    return "ok"

# ======================
# HANDLERS TELEGRAM
# ======================

async def start(update: Update, context: ContextTypes.DEFAULT_TYPE):
    text = (
        "🔞 *ENTRE PARA O GRUPO VIP* 🔞\n\n"
        "🔥 *O QUE VOCÊ VAI RECEBER* 🔥\n"
        "✅ Acesso imediato ao grupo fechado\n"
        "✅ Conteúdos exclusivos\n"
        "✅ Material que não fica público\n"
        "✅ Comunidade restrita\n\n"
        "⚡ A liberação ocorre automaticamente após a confirmação do pagamento.\n\n"
        "🔒 Pagamento 100% seguro via Mercado Pago\n\n"
        "👇 Escolha uma opção abaixo"
    )

    keyboard = [
        [InlineKeyboardButton("👀 Ver Prévias", callback_data="previas")],
        [InlineKeyboardButton("Plano Semanal – R$19", url=LINK_SEMANAL)],
        [InlineKeyboardButton("Plano Mensal – R$39 🔥", url=LINK_MENSAL)],
        [InlineKeyboardButton("✅ Já paguei", callback_data="ja_paguei")],
    ]

    reply_markup = InlineKeyboardMarkup(keyboard)

    await update.message.reply_text(
        text=text,
        reply_markup=reply_markup,
        parse_mode="MarkdownV2"
    )

async def previas(update: Update, context: ContextTypes.DEFAULT_TYPE):
    query = update.callback_query
    await query.answer()

    text = (
        "🚫 *Este conteúdo não pode ser exibido fora do ambiente VIP.*\n\n"
        "⚠️ *Prévia bloqueada por conter material sensível.*\n\n"
        "O conteúdo completo:\n"
