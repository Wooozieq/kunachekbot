from telethon import TelegramClient, events
from telethon.errors import FloodWaitError
import asyncio
import re
import time

API_ID = '26996220'  # Замените на ваш API ID
API_HASH = '8954457e71c11e4adb7aa891c03b9cc9'  # Замените на ваш API Hash
BOT_USERNAME = 'kunacodebot'  # Telegram username бота

client = TelegramClient('kunacodebot_session', API_ID, API_HASH)

async def process_bids():
    """Основной цикл обработки заявок"""
    attempt_count = 0  # Счетчик попыток отправки команды "Хочу купити"

    while True:
        try:
            start_time = time.time()  # Засекаем время перед отправкой сообщения
            
            # Отправляем сообщение "Хочу купити"
            await client.send_message(BOT_USERNAME, "Хочу купити")
            attempt_count += 1
            print(f"Попытка {attempt_count}: Сообщение 'Хочу купити' отправлено боту.")
            
            # Засекаем время после отправки
            elapsed_time = time.time() - start_time
            print(f"Время, затраченное на отправку: {elapsed_time:.2f} секунд")
            
            # Если прошло меньше 5 секунд, добавляем оставшееся время до 5 секунд
            if elapsed_time < 5:
                sleep_time = 5 - elapsed_time
                print(f"Ждем ещё {sleep_time:.2f} секунд перед следующей попыткой.")
                await asyncio.sleep(sleep_time)

            # Проверяем последние сообщения от бота
            async for message in client.iter_messages(BOT_USERNAME, limit=1):
                if not message.text:
                    continue

                print(f"Получено сообщение от бота: {message.text}")

                # Ищем заявки в сообщении с помощью регулярного выражения
                deal_pattern = r"(/deal\S+).*?(-?\d+\.\d+%)"
                deals = re.findall(deal_pattern, message.text)

                if not deals:
                    print("Не удалось найти сделки в сообщении.")
                    continue

                # Ищем минимальный процент
                best_deal = min(deals, key=lambda x: float(x[1].replace('%', '')))
                deal_command, percent = best_deal
                percent_value = float(percent.replace('%', ''))

                if percent_value < 0:
                    print(f"Нужный процент найден: {percent_value}%. Нажимаем на {deal_command}.")
                    # Немедленно нажимаем на команду сделки
                    await client.send_message(BOT_USERNAME, deal_command)
                    print(f"Команда {deal_command} отправлена.")

                    # Ждем ответа с кнопкой "Перейти до оплати"
                    async for follow_up in client.iter_messages(BOT_USERNAME, limit=1):
                        if "Перейти до оплати" in follow_up.text or follow_up.buttons:
                            print("Нажимаем на кнопку 'Перейти до оплати'.")
                            await follow_up.click(text="Перейти до оплати")
                            print("Кнопка 'Перейти до оплати' нажата. Процесс завершен.")
                            return
                else:
                    print(f"Нужный процент не найден. Самый низкий процент: {percent_value}%.")
            
            # Если достигнуто 25 попыток, делаем перерыв
            if attempt_count >= 25:
                print("Достигнуто 25 попыток. Ожидание 2 минуты перед повтором.")
                await asyncio.sleep(120)  # Перерыв на 2 минуты
                attempt_count = 0  # Сброс счетчика попыток

        except FloodWaitError as e:
            print(f"FloodWaitError: Необходимо подождать {e.seconds} секунд.")
            await asyncio.sleep(e.seconds)  # Ждем, пока Telegram разрешит отправку сообщений

async def main():
    """Главная функция программы"""
    await client.start()
    print("Телеграмм аккаунт подключен успешно.")
    await process_bids()

if __name__ == '__main__':
    with client:
        client.loop.run_until_complete(main())

if __name__ == '__main__':
    with client:
        client.loop.run_until_complete(main())
