# 📢 Telegram Integration with Tornado

This project allows you to run an **HTTP server with Tornado** that receives `POST` requests and automatically forwards them as messages to a **Telegram bot**.  

---

## 🚀 Prerequisites

- Python 3.10+  
- A **Telegram** account  
- A bot token generated via **BotFather**  
- `pip` to install dependencies  

---

## 📌 Step 1 – Create the Bot and Get the Token

1. In Telegram, open a chat with [**@BotFather**](https://t.me/BotFather).  
2. Send the command: `/newbot`
3. Choose a **name** and a **username** (must end with `bot`, e.g., `my_test_bot`).  
4. BotFather will reply with something like: Done! Use this token to access the HTTP API: 123456789:ABCdefGhIJKlmNoPQRstuVWXyz1234567890

👉 This value is your **`TELEGRAM_TOKEN`**.

---

## 📌 Step 2 – Find the Chat ID

The `chat_id` identifies where the messages will be sent (a user, group, or channel).

### 🔹 Case A – Sending to **yourself**

1. Open a chat with your bot (`t.me/your_bot_username`).  
2. Send any message (e.g., `hi`).  
3. Run in your terminal:
```bash
curl https://api.telegram.org/bot<TELEGRAM_TOKEN>/getUpdates
```
4. You’ll see something like: 
```json
"chat": {
  "id": 123456789,
  "first_name": "YourName",
  "type": "private"
}
```
👉 The value 123456789 is your TELEGRAM_CHAT_ID.

### 🔹 Case B – Sending to a group**

1. Add the bot to the group.
2. Send any message in the group.
3. Run again:
```bash
curl https://api.telegram.org/bot<TELEGRAM_TOKEN>/getUpdates
```
4. You’ll see something like:
```json
"chat": {
  "id": -1234567890,
  "title": "COPOM Report",
  "type": "group"
}
```
👉 The value -1234567890 is the TELEGRAM_CHAT_ID for the group.
(IDs for groups are negative, that’s expected.)

## 📌 Step 3 – Update the .env File

Update the file called .env in the project root:
```env
TELEGRAM_TOKEN=123456789:ABCdefGhIJKlmNoPQRstuVWXyz1234567890
TELEGRAM_CHAT_ID=-1234567890
```