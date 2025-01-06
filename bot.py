from telethon import TelegramClient, events
import asyncio
import re

API_ID = '20873647'  # Замените на ваш API ID
API_HASH = 'e4ea9ff38bf42ef6c4f307a7cc28b898'  # Замените на ваш API Hash
BOT_USERNAME = 'kunacodebot'  # Telegram username бота

client = TelegramClient('kunacodebot_session', API_ID, API_HASH)

async def process_bids():
    """Основной цикл обработки заявок"""
    while True:
        # Отправляем сообщение "Хочу купити"
        await client.send_message(BOT_USERNAME, "Хочу купити")
        print("Сообщение 'Хочу купити' отправлено боту.")
        
        # Ждем 1 секунду перед получением ответа
        await asyncio.sleep(1)
        
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
                # Нажимаем команду сделки
                await client.send_message(BOT_USERNAME, deal_command)
                await asyncio.sleep(1)  # Ждем ответа бота
                
                # Ищем кнопку "Перейти до оплати"
                async for follow_up in client.iter_messages(BOT_USERNAME, limit=1):
                    if "Перейти до оплати" in follow_up.text or follow_up.buttons:
                        await follow_up.click(text="Перейти до оплати")
                        print("Кнопка 'Перейти до оплати' нажата. Процесс завершен.")
                        return
            else:
                print(f"Нужный процент не найден. Самый низкий процент: {percent_value}%.")
                await asyncio.sleep(5)  # Подождем перед повтором

async def main():
    """Главная функция программы"""
    await client.start()
    print("Телеграмм аккаунт подключен успешно.")
    await process_bids()

if __name__ == '__main__':
    with client:
        client.loop.run_until_complete(main())
