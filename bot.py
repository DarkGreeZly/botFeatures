import asyncio

from aiogram import Bot, Dispatcher, executor, types
from aiogram.types import WebAppInfo
from aiogram.utils.callback_data import CallbackData

from botFeatures import languages

API_TOKEN = "1738735128:AAEzxX2htCTnnNYX92YRLtG43veio8qkeIA"

bot = Bot(API_TOKEN)
dp = Dispatcher(bot)
cb_inline = CallbackData("post", "action", "data")


@dp.message_handler(commands=["start"])
async def start(message: types.Message):
    ua = types.InlineKeyboardButton("Українська", callback_data="ua")
    eng = types.InlineKeyboardButton("Англійська", callback_data="eng")
    mar = types.InlineKeyboardMarkup().add(ua, eng)
    await bot.send_message(message.from_user.id, "Вітаємо вас у ботові, який представляє частину доступних функцій"
                           " телеграм. Оберіть мову:", reply_markup=mar)


@dp.callback_query_handler(text="ua")
async def change_ua(callback_query: types.CallbackQuery):
    menu = types.KeyboardButton(languages.ua['menu_button'])
    mar = types.ReplyKeyboardMarkup().add(menu)
    await bot.send_message(callback_query.from_user.id, languages.ua['menu'],
                           parse_mode=types.ParseMode.MARKDOWN, reply_markup=mar)
    await bot.delete_message(callback_query.from_user.id, callback_query.message.message_id)


@dp.callback_query_handler(text="eng")
async def change_eng(callback_query: types.CallbackQuery):
    menu = types.KeyboardButton(languages.eng['menu_button'])
    mar = types.ReplyKeyboardMarkup(resize_keyboard=True).add(menu)
    await bot.send_message(callback_query.from_user.id, languages.eng['menu'],
                           parse_mode=types.ParseMode.MARKDOWN, reply_markup=mar)
    await bot.delete_message(callback_query.from_user.id, callback_query.message.message_id)


@dp.message_handler(text=languages.ua['menu_button'])
@dp.message_handler(text=languages.eng['menu_button'])
async def main_menu(message: types.Message):
    if message.text == languages.ua['menu_button']:
        web_app = types.InlineKeyboardButton(languages.ua['web_app'], callback_data="web_app")
        newsletter = types.InlineKeyboardButton(languages.ua['newsletter'], callback_data="newsletter")
        user_info = types.InlineKeyboardButton(languages.ua['user_info'], callback_data="user_info")
        analysis = types.InlineKeyboardButton(languages.ua['analysis'], callback_data="analysis")
        special = types.InlineKeyboardButton(languages.ua['special'], callback_data="special")
    elif message.text == languages.eng['menu_button']:
        web_app = types.InlineKeyboardButton(languages.eng['web_app'], callback_data="web_app")
        newsletter = types.InlineKeyboardButton(languages.eng['newsletter'], callback_data="newsletter")
        user_info = types.InlineKeyboardButton(languages.eng['user_info'], callback_data="user_info")
        analysis = types.InlineKeyboardButton(languages.eng['analysis'], callback_data="analysis")
        special = types.InlineKeyboardButton(languages.eng['special'], callback_data="special")
    mar = types.InlineKeyboardMarkup(row_width=1).add(web_app, newsletter, user_info, analysis, special)
    await bot.send_message(message.from_user.id, message.text, reply_markup=mar)
    await bot.delete_message(message.from_user.id, message.message_id)


@dp.callback_query_handler(text="web_app")
async def web_app(callback_query: types.CallbackQuery):
    if callback_query.message.text == languages.ua['menu_button']:
        fill = types.InlineKeyboardButton(languages.ua['form_button'],
                                          web_app=WebAppInfo(url=f"https://darkgreezly.pythonanywhere.com"))
        message = languages.ua['form_text']
    elif callback_query.message.text == languages.eng['menu_button']:
        fill = types.InlineKeyboardButton(languages.ua['form_button'],
                                          web_app=WebAppInfo(url=f"https://darkgreezly.pythonanywhere.com"))
        message = languages.eng['form_text']
    mar = types.InlineKeyboardMarkup().add(fill)
    await bot.send_message(callback_query.from_user.id, message, reply_markup=mar)
    await bot.delete_message(callback_query.from_user.id, callback_query.message.message_id)


@dp.callback_query_handler(text="newsletter")
async def newsletter(callback_query: types.CallbackQuery):
    global recieved_message, newsletter_message
    recieved_message = False
    newsletter_message = ""
    if callback_query.message.text == languages.ua['menu_button']:
        message_text = languages.ua['letter_text']
    elif callback_query.message.text == languages.eng['menu_button']:
        message_text = languages.eng['letter_text']

    await bot.send_message(callback_query.from_user.id, message_text)

    @dp.message_handler(content_types=types.ContentType.ANY)
    async def message_for_newsletter(message: types.Message):
        global recieved_message, newsletter_message
        if message_text == languages.ua['letter_text']:
            seconds = languages.ua['seconds_text']
            time_left = languages.ua['time_left']
        elif message_text == languages.eng['letter_text']:
            seconds = languages.eng['seconds_text']
            time_left = languages.eng['time_left']

        if recieved_message is True and message.text.isdigit():
            recieved_message = False
            await asyncio.sleep(int(message.text))
            await bot.send_message(message.from_user.id, time_left.format(message.text), parse_mode=types.ParseMode.MARKDOWN)
            await bot.copy_message(message.from_user.id, message.chat.id, newsletter_message.message_id)
        elif recieved_message is False:
            recieved_message = True
            newsletter_message = message
            await bot.send_message(message.from_user.id, seconds)
    await bot.delete_message(callback_query.from_user.id, callback_query.message.message_id)


@dp.callback_query_handler(text="user_info")
async def user_info(callback_query: types.CallbackQuery):
    if callback_query.message.text == languages.ua['menu_button']:
        info_text = languages.ua['info_text']
    elif callback_query.message.text == languages.eng['menu_button']:
        info_text = languages.eng['info_text']
    await bot.send_message(callback_query.from_user.id, info_text)
    await bot.send_message(callback_query.from_user.id, f"id: {types.User.id}\n"
                                                            f"is_bot: {types.User.is_bot}\n"
                                                            f"first_name: {types.User.first_name}\n"
                                                            f"last_name: {types.User.last_name}\n"
                                                            f"username: {types.User.username}\n"
                                                            f"language_code: {types.User.language_code}\n"
                                                            f"is_premium: {types.User.is_premium}\n"
                                                            f"added_to_attachment_menu: {types.User.added_to_attachment_menu}\n"
                                                            f"can_join_groups: {types.User.can_join_groups}\n"
                                                            f"can_read_all_group_messages: {types.User.can_read_all_group_messages}\n"
                                                            f"supports_inline_queries: {types.User.supports_inline_queries}\n")
    await bot.delete_message(callback_query.from_user.id, callback_query.message.message_id)


@dp.callback_query_handler(text="analysis")
async def analysis(callback_query: types.CallbackQuery):
    if callback_query.message.text == languages.ua['menu_button']:
        analysis_text = languages.ua['analysis_text']
        recieved_analysis = languages.ua['recieved_analysis']
    elif callback_query.message.text == languages.eng['menu_button']:
        analysis_text = languages.eng['analysis_text']
        recieved_analysis = languages.eng['recieved_analysis']
    await bot.send_message(callback_query.from_user.id, analysis_text)

    @dp.message_handler(content_types=types.ContentType.ANY)
    async def analysis_message(message: types.Message):
        await bot.send_message(message.from_user.id, recieved_analysis.format(message.content_type),
                               parse_mode = types.ParseMode.MARKDOWN)
    await bot.delete_message(callback_query.from_user.id, callback_query.message.message_id)


@dp.callback_query_handler(text="special")
async def special(callback_query: types.CallbackQuery):
    await bot.delete_message(callback_query.from_user.id, callback_query.message.message_id)
    if callback_query.message.text == languages.ua['menu_button']:
        feature1 = languages.ua['feature1']
        feature2 = languages.ua['feature2']
        feature3 = languages.ua['feature3']
    elif callback_query.message.text == languages.eng['menu_button']:
        feature1 = languages.eng['feature1']
        feature2 = languages.eng['feature2']
        feature3 = languages.eng['feature3']
    main_message = await bot.send_message(callback_query.from_user.id, feature1, parse_mode = types.ParseMode.MARKDOWN)
    await asyncio.sleep(3)
    await bot.edit_message_text(chat_id=callback_query.from_user.id, message_id=main_message.message_id, text=feature2, parse_mode = types.ParseMode.MARKDOWN)
    await asyncio.sleep(3)
    await bot.edit_message_text(chat_id=callback_query.from_user.id, message_id=main_message.message_id, text=feature3, parse_mode = types.ParseMode.MARKDOWN_V2)
    await asyncio.sleep(3)
    await bot.delete_message(callback_query.from_user.id, main_message.message_id)


if __name__ == "__main__":
    executor.start_polling(dp, skip_updates=True)
