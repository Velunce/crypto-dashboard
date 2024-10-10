import logging
import os
from telegram import Update, InlineKeyboardButton, InlineKeyboardMarkup
from telegram.ext import Application, CommandHandler, CallbackQueryHandler, MessageHandler, filters, ContextTypes
from ahr999_calculator import get_ahr999_message
from dotenv import load_dotenv

# 加载环境变量
load_dotenv()

# 启用日志
logging.basicConfig(
    format='%(asctime)s - %(name)s - %(levelname)s - %(message)s',
    level=logging.INFO
)

logger = logging.getLogger(__name__)

# 设置你的bot token
TOKEN = os.getenv('TELEGRAM_BOT_TOKEN')
logger.info(f"Token: {TOKEN}")

# 定义欢迎消息处理函数
async def start(update: Update, context: ContextTypes.DEFAULT_TYPE) -> None:
    """发送欢迎消息和计算按钮"""
    logger.info("Start command received")
    keyboard = [
        [InlineKeyboardButton("计算 AHR999 指数", callback_data='calculate_ahr999')]
    ]
    reply_markup = InlineKeyboardMarkup(keyboard)
    await update.message.reply_text('欢迎使用 AHR999 指数计算器! 点击下方按钮计算:', reply_markup=reply_markup)

# 定义按钮回调的处理函数
async def button_callback(update: Update, context: ContextTypes.DEFAULT_TYPE) -> None:
    """处理按钮点击事件"""
    logger.info("Button callback received")
    query = update.callback_query
    await query.answer()
    ahr999_message = get_ahr999_message()
    keyboard = [
        [InlineKeyboardButton("再次计算", callback_data='calculate_ahr999')]
    ]
    reply_markup = InlineKeyboardMarkup(keyboard)
    await query.message.reply_text(text=ahr999_message, reply_markup=reply_markup)

# 错误处理函数
async def error_handler(update: object, context: ContextTypes.DEFAULT_TYPE) -> None:
    logger.error(f"更新 {update} 导致错误 {context.error}")

# 主函数
def main() -> None:
    """启动机器人"""
    logger.info("Starting bot")
    application = Application.builder().token(TOKEN).build()

    # 处理 /start 命令
    application.add_handler(CommandHandler("start", start))
    
    # 处理按钮回调
    application.add_handler(CallbackQueryHandler(button_callback))

    # 处理其他所有消息
    application.add_handler(MessageHandler(filters.TEXT & ~filters.COMMAND, start))

    application.add_error_handler(error_handler)

    logger.info("开始轮询")
    application.run_polling()

if __name__ == '__main__':
    main()
