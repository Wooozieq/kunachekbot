from telethon import TelegramClient, events
import asyncio
import re

API_ID = '20873647'  # Замените на ваш API ID
API_HASH = 'e4ea9ff38bf42ef6c4f307a7cc28b898'  # Замените на ваш API Hash
BOT_USERNAME = 'kunacodebot'  # Telegram username бота

client = TelegramClient('kunacodebot_session', API_ID, API_HASH)

async def main():
    await client.start()
    me = await client.get_me()
    print(f"Телеграмм аккаунт подключен успешно: {me.username or me.first_name}")

    async def process_message(event):
        message = event.message.message
        if 'UAH' in message and '%' in message:
            print("Обрабатываем список заявок...")
            deal_pattern = r"(/deal\S+).*?(-?\d+\.\d+%)"
            deals = re.findall(deal_pattern, message)
            if not deals:
                print("Не удалось найти сделки в сообщении.")
                return

            # Найти самую низкую наценку
            best_deal = min(deals, key=lambda x: float(x[1].replace('%', '')))
            percent = float(best_deal[1].replace('%', ''))

            if percent < 0:
                print(f"Нужный процент найден: {percent}%. Нажимаем на {best_deal[0]}.")
                await client.send_message(BOT_USERNAME, best_deal[0])
                await asyncio.sleep(2)  # Подождем для получения ответа
                await client.send_message(BOT_USERNAME, 'Перейти до оплати')
                print("Нужный процент найден, заявка принята, ожидает оплату.")
                return
            else:
                print(f"Нужный процент не найден. Самый низкий процент: {percent}%")
                await asyncio.sleep(2)
                await client.send_message(BOT_USERNAME, "Хочу купити")

    @client.on(events.NewMessage(from_users=BOT_USERNAME))
    async def handler(event):
        await process_message(event)

    await client.send_message(BOT_USERNAME, "Хочу купити")
    print("Начинаем отслеживание бота...")
    await client.run_until_disconnected()

if __name__ == '__main__':
    with client:
        client.loop.run_until_complete(main())
