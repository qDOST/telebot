import telebot
from telebot import types
import requests
import json

BOT_TOKEN = '6158297491:AAGGtl0Lj4_-RMiVqhaepmTo37wUnfW2QXw'
GEOAPIFY_API_KEY = '72e22419dc9a43eb9f8c883653450e11'

bot = telebot.TeleBot(BOT_TOKEN)

user_language = {}
user_addresses = {}
user_quantities = {}
user_cart = {}
selected_food = {}
user_keyboards = {}
prices = {
    "Лаваш1": 16000,
    "Лаваш2": 17000,
    # добавьте цены для других блюд здесь
}

def reverse_geocode(lat, lon):
    url = f'https://api.geoapify.com/v1/geocode/reverse?lat={lat}&lon={lon}&apiKey={GEOAPIFY_API_KEY}'
    response = requests.get(url)
    data = json.loads(response.text)
    if 'features' in data and len(data['features']) > 0:
        address = data['features'][0]['properties']['formatted']
        return address
    else:
        return None

def send_location_request(chat_id):
    language = user_language.get(chat_id, "ru") # Получение текущего языка пользователя
    if language == "ru":
        text = "Отправьте геолокацию или выберите адрес доставки:"
        location_button_text = "Отправить геолокацию"
        my_addresses_text = "Мои адреса"
        back_text = "Назад"
    else:
        text = "Жойлашувингизни юборинг ёки етказиб бериш манзилини танланг:"
        location_button_text = "Жойлашувни юбориш"
        my_addresses_text = "Менинг манзилларим"
        back_text = "Ортга"
    keyboard = types.ReplyKeyboardMarkup(resize_keyboard=True)
    location_button = types.KeyboardButton(text=location_button_text, request_location=True)
    keyboard.row(my_addresses_text, location_button)
    keyboard.row(back_text)
    bot.send_message(chat_id, text, reply_markup=keyboard)

@bot.message_handler(commands=['start', 'help'])
def send_welcome(message):
    chat_id = message.chat.id
    language = user_language.get(chat_id, "ru") # Получение текущего языка пользователя
    if language == "ru":
        text = "Выберите одно из следующих:"
        menu_text = "Меню"
        orders_text = "Мои заказы"
        feedback_text = "Оставить отзыв"
        settings_text = "Выбрать язык"
    else:
        text = "Қуйидагилардан бирини танланг:"
        menu_text = "Меню"
        orders_text = "Менинг буюртмаларим"
        feedback_text = "Фикр қолдириш"
        settings_text = "Tilni tanlang"
    keyboard = types.ReplyKeyboardMarkup(resize_keyboard=True)
    keyboard.row(menu_text, orders_text)
    keyboard.row(feedback_text, settings_text)
    bot.send_message(chat_id, text, reply_markup=keyboard)
    
@bot.message_handler(func=lambda message: message.text in ["Русский язык", "Рус тили"])
def handle_russian_language(message):
    user_language[message.chat.id] = "ru"
    bot.send_message(message.chat.id, "Язык изменен на русский")
    send_welcome(message)

@bot.message_handler(func=lambda message: message.text in ["Узбекский язык", "Ўзбек тили"])
def handle_uzbek_language(message):
    user_language[message.chat.id] = "uz"
    bot.send_message(message.chat.id, "Тил ўзбек тилига ўзгартирилди")
    send_welcome(message)
    

@bot.message_handler(func=lambda message: message.text in ["Выбрать язык", "Tilni tanlang"])
def handle_settings(message):
    chat_id = message.chat.id
    language = user_language.get(chat_id, "ru") # Получение текущего языка пользователя
    if language == "ru":
        text = "Выберите язык:"
        russian_text = "Русский язык"
        uzbek_text = "Узбекский язык"
        back_text = "Назад"
    else:
        text = "Тилни танланг:"
        russian_text = "Рус тили"
        uzbek_text = "Ўзбек тили"
        back_text = "Ортга"
    keyboard = types.ReplyKeyboardMarkup(resize_keyboard=True)
    keyboard.row(russian_text, uzbek_text)
    keyboard.row(back_text)
    bot.send_message(chat_id, text, reply_markup=keyboard)

@bot.message_handler(func=lambda message: message.text == "Меню", )
def handle_menu(message):
    send_location_request(message.chat.id)

@bot.message_handler(func=lambda message: message.text in ["Нет", "Йўқ"])
def handle_no(message):
    send_location_request(message.chat.id)

@bot.message_handler(func=lambda message: message.text in ["Назад", "Ортга"])
def handle_back(message):
    chat_id = message.chat.id
    if chat_id in user_keyboards and len(user_keyboards[chat_id]) > 0:
        # Извлечение предыдущей клавиатуры из истории клавиатур пользователя
        previous_keyboard = user_keyboards[chat_id].pop()
        bot.send_message(chat_id, "Выберите одно из следующих:", reply_markup=previous_keyboard)
    else:
        send_welcome(message) # если история клавиатур пуста, отправляем приветственное сообщение

@bot.message_handler(func=lambda message: message.text in ["Да", "Ҳа"])
def handle_yes(message):
    chat_id = message.chat.id
    language = user_language.get(chat_id, "ru") # Получение текущего языка пользователя
    if language == "ru":
        text = "Выберите категорию:"
        set_text = "Сет"
        lavash_text = "Лаваш"
        shawarma_text = "Шаурма"
        donar_text = "Донар"
        burger_text = "Бургер"
        hotdog_text = "Хот-Дог"
        desserts_text = "Десерты"
        drinks_text = "Напитки"
        garnish_text = "Гарнир"
        cart_text = "Корзина"
        back_text = "Назад"
    else:
        text = "Туркумни танланг:"
        set_text = "Сет"
        lavash_text = "Лаваш"
        shawarma_text = "Шаурма"
        donar_text = "Донар"
        burger_text = "Бургер"
        hotdog_text = "Хот-Дог"
        desserts_text = "Десертлар"
        drinks_text = "Ичимликлар"
        garnish_text = "Гарнирлар"
        cart_text = "Саватча"
        back_text = "Ортга"
    keyboard = types.ReplyKeyboardMarkup(resize_keyboard=True)
    keyboard.row(set_text, lavash_text)
    keyboard.row(shawarma_text, donar_text)
    keyboard.row(burger_text, hotdog_text)
    keyboard.row(desserts_text, drinks_text)
    keyboard.row(garnish_text, cart_text)
    keyboard.row(back_text)
    bot.send_message(chat_id, text, reply_markup=keyboard)


@bot.message_handler(func=lambda message: message.text in ["Мои адреса", "Менинг манзилларим"])
def handle_addresses(message):
    chat_id = message.chat.id
    language = user_language.get(chat_id, "ru") # Получение текущего языка пользователя
    if chat_id in user_addresses:
        address = user_addresses[chat_id]
        if language == "ru":
            text = f"Ваш адрес:"
            back_text = "Назад"
        else:
            text = f"Сизнинг манзилингиз:"
            back_text = "Ортга"
        keyboard = types.ReplyKeyboardMarkup(resize_keyboard=True)
        keyboard.row(address)
        keyboard.row(back_text)
        bot.send_message(chat_id, text, reply_markup=keyboard)
    else:
        if language == "ru":
            text = f"Извините, у нас нет информации об вашем адресе. Пожалуйста, отправьте свою геолокацию."
        else:
            text = f"Кечирасиз, бизда сизнинг манзилингиз ҳақида маълумот йўқ. Илтимос жойлашувингизни юборинг."
        bot.send_message(chat_id, text)
        
@bot.message_handler(content_types=['location'])
def handle_location(message):
    chat_id = message.chat.id
    language = user_language.get(chat_id, "ru") # Получение текущего языка пользователя
    latitude = message.location.latitude
    longitude = message.location.longitude
    address = reverse_geocode(latitude, longitude)
    if address:
        user_addresses[chat_id] = address
        if language == "ru":
            text = f"Вы находитесь по адресу: {address}. Это верно?"
            yes_text = "Да"
            no_text = "Нет"
            back_text = "Назад"
        else:
            text = f"Сизнинг манзилингиз: {address}. Тўғрими?"
            yes_text = "Ҳа"
            no_text = "Йўқ"
            back_text = "Ортга"
        keyboard = types.ReplyKeyboardMarkup(resize_keyboard=True)
        keyboard.row(yes_text, no_text)
        keyboard.row(back_text)
        bot.send_message(chat_id, text, reply_markup=keyboard)
    else:
        if language == "ru":
            text = "Извините, мы не смогли найти ваш адрес"
        else:
            text = "Кечирасиз, биз сизнинг манзилингизни тополмадик"
        bot.send_message(chat_id, text)

@bot.message_handler(func=lambda message: message.text in user_addresses.values())
def handle_selected_address(message):
    handle_yes(message) # вызов функции для отображения клавиатуры с выбором еды

@bot.message_handler(func=lambda message: message.text == "Лаваш")
def handle_lavash(message):
    chat_id = message.chat.id
    language = user_language.get(chat_id, "ru") # Получение текущего языка пользователя

    # Отправка фотографии блюда
    photo = open('lavash.jpg', 'rb')
    bot.send_photo(chat_id, photo)

    if language == "ru":
        text = "Выберите вид блюда:"
        lavash1_text = "Лаваш1"
        lavash2_text = "Лаваш2"
        lavash3_text = "Лаваш3"
        lavash4_text = "Лаваш4"
        cart_text = "Корзина"
        back_text = "Назад"
    else:
        text = "Тамак турини танланг:"
        lavash1_text = "Лаваш1"
        lavash2_text = "Лаваш2"
        lavash3_text = "Лаваш3"
        lavash4_text = "Лаваш4"
        cart_text = "Саватча"
        back_text = "Ортга"

    # Отображение клавиатуры с выбором разных видов блюда
    keyboard = types.ReplyKeyboardMarkup(resize_keyboard=True)
    keyboard.row(lavash1_text, lavash2_text)
    keyboard.row(lavash3_text, lavash4_text)
    keyboard.row(cart_text) # Добавление кнопки "Корзина"
    keyboard.row(back_text)

    # Сохранение текущей клавиатуры в истории клавиатур пользователя
    if chat_id not in user_keyboards:
        user_keyboards[chat_id] = []
    user_keyboards[chat_id].append(keyboard)

    bot.send_message(chat_id, text, reply_markup=keyboard)

@bot.message_handler(func=lambda message: message.text in ["Корзина", "Саватча"])
def handle_cart(message):
    handle_cart(message) # вызов функции для отображения содержимого корзины

@bot.message_handler(func=lambda message: message.text == "Шаурма")
def handle_shawarma(message):
    chat_id = message.chat.id
    language = user_language.get(chat_id, "ru") # Получение текущего языка пользователя

    # Отправка фотографии блюда
    photo = open('shawarma.jpg', 'rb')
    bot.send_photo(chat_id, photo)

    if language == "ru":
        text = "Выберите вид блюда:"
        shawarma1_text = "Шаурма1"
        shawarma2_text = "Шаурма2"
        shawarma3_text = "Шаурма3"
        shawarma4_text = "Шаурма4"
        cart_text = "Корзина"
        back_text = "Назад"
    else:
        text = "Тамак турини танланг:"
        shawarma1_text = "Шаурма1"
        shawarma2_text = "Шаурма2"
        shawarma3_text = "Шаурма3"
        shawarma4_text = "Шаурма4"
        cart_text = "Саватча"
        back_text = "Ортга"

    # Отображение клавиатуры с выбором разных видов блюда
    keyboard = types.ReplyKeyboardMarkup(resize_keyboard=True)
    keyboard.row(shawarma1_text, shawarma2_text)
    keyboard.row(shawarma3_text, shawarma4_text)
    keyboard.row(cart_text) # Добавление кнопки "Корзина"
    keyboard.row(back_text)

    # Сохранение текущей клавиатуры в истории клавиатур пользователя
    if chat_id not in user_keyboards:
        user_keyboards[chat_id] = []
    user_keyboards[chat_id].append(keyboard)

    bot.send_message(chat_id, text, reply_markup=keyboard)
    

		
@bot.message_handler(func=lambda message: message.text == "Лаваш1")
def handle_lavash1(message):
    chat_id = message.chat.id
    language = user_language.get(chat_id, "ru") # Получение текущего языка пользователя

    selected_food[chat_id] = "Лаваш1"

    # Инициализация количества товаров для пользователя
    if chat_id not in user_quantities:
        user_quantities[chat_id] = 1

    # Отправка фотографии блюда
    photo = open('lavash1.jpg', 'rb')
    if language == "ru":
        caption = "Цена: 16 000 сум"
        text = "Выберите количество:"
        minus_text = "-"
        plus_text = "+"
        add_to_cart_text = "Добавить в корзину"
    else:
        caption = "Нархи: 16 000 сўм"
        text = "Микдорни танланг:"
        minus_text = "-"
        plus_text = "+"
        add_to_cart_text = "Саватга қўшиш"
    bot.send_photo(chat_id, photo, caption=caption)

    # Отображение встроенной клавиатуры для выбора количества и добавления в корзину
    keyboard = types.InlineKeyboardMarkup()
    keyboard.row(
        types.InlineKeyboardButton(minus_text, callback_data="-"),
        types.InlineKeyboardButton(str(user_quantities[chat_id]), callback_data="quantity"),
        types.InlineKeyboardButton(plus_text, callback_data="+")
    )
    keyboard.row(types.InlineKeyboardButton(add_to_cart_text, callback_data="add_to_cart"))
    bot.send_message(chat_id, text, reply_markup=keyboard)

@bot.message_handler(func=lambda message: message.text == "Лаваш1")
def handle_lavash1(message):
    chat_id = message.chat.id
    language = user_language.get(chat_id, "ru") # Получение текущего языка пользователя

    selected_food[chat_id] = "Лаваш1"

    # Инициализация количества товаров для пользователя
    if chat_id not in user_quantities:
        user_quantities[chat_id] = 1

    # Отправка фотографии блюда
    photo = open('lavash1.jpg', 'rb')
    if language == "ru":
        caption = "Цена: 16 000 сум"
        text = "Выберите количество:"
        minus_text = "-"
        plus_text = "+"
        add_to_cart_text = "Добавить в корзину"
    else:
        caption = "Нархи: 16 000 сўм"
        text = "Микдорни танланг:"
        minus_text = "-"
        plus_text = "+"
        add_to_cart_text = "Саватга қўшиш"
    bot.send_photo(chat_id, photo, caption=caption)

    # Отображение встроенной клавиатуры для выбора количества и добавления в корзину
    keyboard = types.InlineKeyboardMarkup()
    keyboard.row(
        types.InlineKeyboardButton(minus_text, callback_data="-"),
        types.InlineKeyboardButton(str(user_quantities[chat_id]), callback_data="quantity"),
        types.InlineKeyboardButton(plus_text, callback_data="+")
    )
    keyboard.row(types.InlineKeyboardButton(add_to_cart_text, callback_data="add_to_cart"))
    bot.send_message(chat_id, text, reply_markup=keyboard)

@bot.callback_query_handler(func=lambda call: call.data == "-")
def handle_minus(call):
    chat_id = call.message.chat.id
    language = user_language.get(chat_id, "ru") # Получение текущего языка пользователя

    # Уменьшение количества товаров для пользователя
    if chat_id in user_quantities and user_quantities[chat_id] > 1:
        user_quantities[chat_id] -= 1

    if language == "ru":
        text = "Выберите количество:"
        minus_text = "-"
        plus_text = "+"
        add_to_cart_text = "Добавить в корзину"
    else:
        text = "Микдорни танланг:"
        minus_text = "-"
        plus_text = "+"
        add_to_cart_text = "Саватга қўшиш"

    # Отображение обновленной встроенной клавиатуры для выбора количества и добавления в корзину
    keyboard = types.InlineKeyboardMarkup()
    keyboard.row(
        types.InlineKeyboardButton(minus_text, callback_data="-"),
        types.InlineKeyboardButton(str(user_quantities[chat_id]), callback_data="quantity"),
        types.InlineKeyboardButton(plus_text, callback_data="+")
    )
    keyboard.row(types.InlineKeyboardButton(add_to_cart_text, callback_data="add_to_cart"))

    # Проверка, изменился ли текст или клавиатура сообщения
    if call.message.text != text or call.message.reply_markup.to_dict() != keyboard.to_dict():
        bot.edit_message_text(text, chat_id, call.message.message_id, reply_markup=keyboard)

@bot.callback_query_handler(func=lambda call: call.data == "+")
def handle_plus(call):
    chat_id = call.message.chat.id
    language = user_language.get(chat_id, "ru") # Получение текущего языка пользователя

    # Увеличение количества товаров для пользователя
    if chat_id in user_quantities:
        user_quantities[chat_id] += 1

    if language == "ru":
        text = "Выберите количество:"
        minus_text = "-"
        plus_text = "+"
        add_to_cart_text = "Добавить в корзину"
    else:
        text = "Микдорни танланг:"
        minus_text = "-"
        plus_text = "+"
        add_to_cart_text = "Саватга қўшиш"

    # Отображение обновленной встроенной клавиатуры для выбора количества и добавления в корзину
    keyboard = types.InlineKeyboardMarkup()
    keyboard.row(
        types.InlineKeyboardButton(minus_text, callback_data="-"),
        types.InlineKeyboardButton(str(user_quantities[chat_id]), callback_data="quantity"),
        types.InlineKeyboardButton(plus_text, callback_data="+")
    )
    keyboard.row(types.InlineKeyboardButton(add_to_cart_text, callback_data="add_to_cart"))
    bot.edit_message_text(text, chat_id, call.message.message_id, reply_markup=keyboard)

@bot.callback_query_handler(func=lambda call: call.data == "add_to_cart")
def handle_add_to_cart(call):
    chat_id = call.message.chat.id
    language = user_language.get(chat_id, "ru") # Получение текущего языка пользователя

    # Получение информации о выбранном блюде и его количестве
    food = selected_food[chat_id]
    quantity = user_quantities[chat_id]

    # Сохранение информации в корзине пользователя
    if chat_id not in user_cart:
        user_cart[chat_id] = []
    user_cart[chat_id].append((food, quantity))

    if language == "ru":
        text = "Блюдо добавлено в корзину"
    else:
        text = "Таом саватга қўшилди"

    bot.answer_callback_query(call.id, text)
    
@bot.message_handler(func=lambda message: message.text == "Корзина")
def handle_cart(message):
    chat_id = message.chat.id
    language = user_language.get(chat_id, "ru") # Получение текущего языка пользователя
    if language == "ru":
        empty_text = "Корзина пуста"
    else:
        empty_text = "Саватча бўш"
    chat_id = message.chat.id
    language = user_language.get(chat_id, "ru") # Получение текущего языка пользователя

    if chat_id in user_cart:
        cart = user_cart[chat_id]
        if language == "ru":
            text = "Ваша корзина:\n"
            delivery_text = "Доставка:"
            total_text = "Итого:"
            empty_text = "Корзина пуста"
            checkout_text = "Оформить заказ"
            clear_cart_text = "Очистить корзину"
            delivery_time_text = "Время доставки"
            remove_text = "Удалить"
        else:
            text = "Сизнинг саватингиз:\n"
            delivery_text = "Этказиб бериш:"
            total_text = "Жами:"
            empty_text = "Сават бўш"
            checkout_text = "Буюртмани расмийлаштириш"
            clear_cart_text = "Саватни тозалаш"
            delivery_time_text = "Этказиб бериш вақти"
            remove_text = "Ўчириш"

        total = 0
        for food, quantity in cart:
            price = prices[food]
            text += f"{food} x {quantity} = {quantity * price} сум\n"
            total += quantity * price
        if len(cart) > 0: # Проверка наличия блюд в корзине
            delivery_fee = 10000
            total += delivery_fee
            text += f"\n{delivery_text} {delivery_fee} сум\n{total_text} {total} сум"
        else:
            text += f"\n{empty_text}"
        bot.send_message(chat_id, text)

        # Отображение встроенной клавиатуры с кнопками для оформления заказа и очистки корзины
        keyboard = types.InlineKeyboardMarkup()
        keyboard.row(types.InlineKeyboardButton(checkout_text, callback_data="checkout"))
        keyboard.row(types.InlineKeyboardButton(clear_cart_text, callback_data="clear_cart"))
        keyboard.row(types.InlineKeyboardButton(delivery_time_text, callback_data="delivery_time"))

        # Добавление кнопок для удаления каждого блюда из корзины
        for food, quantity in cart:
            keyboard.row(types.InlineKeyboardButton(f"{remove_text} {food}", callback_data=f"remove_{food}"))

        bot.send_message(chat_id, "Выберите действие:", reply_markup=keyboard)
    else:
        bot.send_message(chat_id, empty_text)
        
        
@bot.callback_query_handler(func=lambda call: call.data == "checkout")
def handle_checkout(call):
    chat_id = call.message.chat.id
    language = user_language.get(chat_id, "ru") # Получение текущего языка пользователя

    if language == "ru":
        text = "Выберите способ оплаты:"
        cash_text = "Наличными"
        click_text = "Click"
        payme_text = "Payme"
    else:
        text = "Тўлов усулини танланг:"
        cash_text = "Нақд пул"
        click_text = "Click"
        payme_text = "Payme"

    # Отображение клавиатуры с выбором способа оплаты
    keyboard = types.InlineKeyboardMarkup()
    keyboard.add(types.InlineKeyboardButton(cash_text, callback_data="cash"))
    keyboard.add(types.InlineKeyboardButton(click_text, callback_data="click"))
    keyboard.add(types.InlineKeyboardButton(payme_text, callback_data="payme"))
    bot.send_message(chat_id, text, reply_markup=keyboard)

@bot.callback_query_handler(func=lambda call: call.data == "cash")
def handle_cash(call):
    chat_id = call.message.chat.id
    language = user_language.get(chat_id, "ru") # Получение текущего языка пользователя

    # Получение информации о заказе
    address = user_addresses[chat_id]
    cart = user_cart[chat_id]
    if language == "ru":
        text = f"Адрес: {address}\nЗаказ:\n"
        delivery_text = "Доставка:"
        total_text = "Итого:"
        payment_type_text = "Тип оплаты:"
        cash_text = "Наличными"
        confirm_text = "Подтвердить"
        cancel_text = "Отменить"
    else:
        text = f"Манзил: {address}\nБуюртма:\n"
        delivery_text = "Этказиб бериш:"
        total_text = "Жами:"
        payment_type_text = "Тўлов тури:"
        cash_text = "Нақд пул"
        confirm_text = "Тасдиқлаш"
        cancel_text = "Бекор қилиш"

    total = 0
    for food, quantity in cart:
        price = prices[food]
        text += f"{food} x {quantity} = {quantity * price} сум\n"
        total += quantity * price
    delivery_fee = 10000
    total += delivery_fee
    text += f"\n{delivery_text} {delivery_fee} сум\n{total_text} {total} сум"
    text += f"\n{payment_type_text} {cash_text}"

    # Отображение встроенной клавиатуры с кнопками для подтверждения или отмены заказа
    keyboard = types.InlineKeyboardMarkup()
    keyboard.add(types.InlineKeyboardButton(confirm_text, callback_data="confirm"))
    keyboard.add(types.InlineKeyboardButton(cancel_text, callback_data="cancel"))

    bot.send_message(chat_id, text, reply_markup=keyboard)

@bot.callback_query_handler(func=lambda call: call.data.startswith("remove_"))
def handle_remove_food(call):
    chat_id = call.message.chat.id
    language = user_language.get(chat_id, "ru") # Получение текущего языка пользователя

    # Получение информации о выбранном блюде для удаления из корзины
    food_to_remove = call.data.split("_")[1]

    # Удаление блюда из корзины пользователя
    if chat_id in user_cart:
        cart = user_cart[chat_id]
        for i in range(len(cart)):
            food, quantity = cart[i]
            if food == food_to_remove:
                del cart[i]
                break

    if language == "ru":
        text = f"{food_to_remove} удалено из корзины"
        delivery_text = "Доставка:"
        total_text = "Итого:"
        empty_text = "Корзина пуста"
        checkout_text = "Оформить заказ"
        clear_cart_text = "Очистить корзину"
        delivery_time_text = "Время доставки"
        remove_text = "Удалить"
    else:
        text = f"{food_to_remove} саватдан ўчирилди"
        delivery_text = "Этказиб бериш:"
        total_text = "Жами:"
        empty_text = "Сават бўш"
        checkout_text = "Буюртмани расмийлаштириш"
        clear_cart_text = "Саватни тозалаш"
        delivery_time_text = "Этказиб бериш вақти"
        remove_text = "Ўчириш"

    bot.answer_callback_query(call.id, text)

    # Обновление содержимого корзины
    if chat_id in user_cart:
        cart = user_cart[chat_id]
        text = f"{empty_text}\n" if len(cart) == 0 else ""
        total = 0
        for food, quantity in cart:
            price = prices[food]
            text += f"{food} x {quantity} = {quantity * price} сум\n"
            total += quantity * price
        if len(cart) > 0: # Проверка наличия блюд в корзине
            delivery_fee = 10000
            total += delivery_fee
            text += f"\n{delivery_text} {delivery_fee} сум\n{total_text} {total} сум"

        # Обновление текста сообщения с содержимым корзины
        message_id = call.message.message_id - 1 # Получение идентификатора сообщения с содержимым корзины
        bot.edit_message_text(text, chat_id, message_id)

        # Обновление встроенной клавиатуры с кнопками для оформления заказа и очистки корзины
        keyboard = types.InlineKeyboardMarkup()
        keyboard.row(types.InlineKeyboardButton(checkout_text, callback_data="checkout"))
        keyboard.row(types.InlineKeyboardButton(clear_cart_text, callback_data="clear_cart"))
        keyboard.row(types.InlineKeyboardButton(delivery_time_text, callback_data="delivery_time"))

        # Добавление кнопок для удаления каждого блюда из корзины
        for food, quantity in cart:
            keyboard.row(types.InlineKeyboardButton(f"{remove_text} {food}", callback_data=f"remove_{food}"))

        bot.edit_message_reply_markup(chat_id, message_id + 1, reply_markup=keyboard)

@bot.callback_query_handler(func=lambda call: call.data == "clear_cart")
def handle_clear_cart(call):
    chat_id = call.message.chat.id
    language = user_language.get(chat_id, "ru") # Получение текущего языка пользователя

    # Очистка корзины пользователя
    if chat_id in user_cart:
        del user_cart[chat_id]

    if language == "ru":
        text = "Корзина очищена"
    else:
        text = "Сават тозаланди"

    bot.answer_callback_query(call.id, text)

bot.polling()
