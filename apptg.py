import telegram
import appcontext


async def send_msg(ctx: appcontext.AppContext):
    msg = f"temp: {ctx.sht4x_ctx.msr.temp:.2f}, rh: {ctx.sht4x_ctx.msr.rh:.2f}"
    bot = telegram.Bot(ctx.tg_bot_cfg.token)
    async with bot:
        await bot.send_message(text=msg, chat_id=ctx.tg_bot_cfg.chat_id)
