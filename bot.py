import os
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

# Debug: confirm what value TOKEN holds at startup
print(f"[DEBUG] TOKEN value: {'SET (length=' + str(len(TOKEN)) + ')' if TOKEN else 'NOT SET / EMPTY'}")

if not TOKEN:
    raise RuntimeError(
        "TOKEN environment variable is not set or is empty. "
        "Please configure the TOKEN variable in your Railway service settings."
    )

LINK_SEMANAL = "https://mpago.la/1LEY4CP"
LINK_MENSAL = "https://mpago.la/2oL26cr"

# ======================
# APPLICATION
# ======================

application = Application.builder().token(TOKEN).build()

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
        "⚡ A liberação ocorre automaticamente após a confirmação do pagamento\\.\n\n"
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
        "🚫 *Este conteúdo não pode ser exibido fora do ambiente VIP\\.*\n\n"
        "⚠️ *Prévia bloqueada por conter material sensível\\.*\n\n"
        "O conteúdo completo está disponível apenas para membros VIP\\.\n\n"
        "👇 Escolha um plano abaixo para ter acesso imediato:"
    )

    keyboard = [
        [InlineKeyboardButton("Plano Semanal – R$19", url=LINK_SEMANAL)],
        [InlineKeyboardButton("Plano Mensal – R$39 🔥", url=LINK_MENSAL)],
        [InlineKeyboardButton("✅ Já paguei", callback_data="ja_paguei")],
    ]

    reply_markup = InlineKeyboardMarkup(keyboard)

    await query.edit_message_text(
        text=text,
        reply_markup=reply_markup,
        parse_mode="MarkdownV2"
    )

async def ja_paguei(update: Update, context: ContextTypes.DEFAULT_TYPE):
    query = update.callback_query
    await query.answer()

    text = (
        "✅ *Pagamento recebido\\!*\n\n"
        "Aguarde a confirmação e você será adicionado ao grupo VIP em breve\\.\n\n"
        "Se ainda não foi adicionado, entre em contato com o suporte\\."
    )

    await query.edit_message_text(
        text=text,
        parse_mode="MarkdownV2"
    )

# ======================
# REGISTRO DE HANDLERS
# ======================

application.add_handler(CommandHandler("start", start))
application.add_handler(CallbackQueryHandler(previas, pattern="^previas$"))
application.add_handler(CallbackQueryHandler(ja_paguei, pattern="^ja_paguei$"))

# ======================
# INICIALIZAÇÃO
# ======================

if __name__ == "__main__":
    application.run_polling()
