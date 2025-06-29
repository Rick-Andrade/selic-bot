

# 🤖 SelicBot — Intelligent Copom Minutes Analyzer

SelicBot is an automated agent powered by OpenAI that downloads and analyzes the most recent *Copom* minutes (Brazilian Central Bank interest rate decisions), summarizing trends and recommending investment strategies based on natural language insights.


---

## 📌 Features

- 🧠 **AI-powered analysis** using GPT-4 or GPT-3.5
- 📥 **Automatic download** of the latest *Copom* minutes from the Brazilian Central Bank
- 📄 **PDF parsing** with `pdfplumber`
- ⏰ **Scheduled execution** using `systemd` (runs daily at 9 AM)
- 📝 **State tracking** to avoid reprocessing previously analyzed reports
- 💡 **Customizable prompts** for investment suggestions
- ✅ **Easy to deploy** on a Raspberry Pi or any Linux machine

---

## 📂 Project Structure

## 🚀 Quick Start

### 1. Clone the repo

```bash
git clone https://github.com/your-username/selic-bot.git
cd selic-bot
```
### 2. Create and activate virtual environment
```bash
python -m venv venv
source venv/bin/activate   # On Windows: venv\Scripts\activate
```
### 3. Install dependencies
```bash
pip install -r requirements.txt
```
### 4. Set your OpenAI API Key
Create a .env file in the root directory:
```bash
OPEN_AI_KEY=your_openai_api_key_here
```

## 🕒 Running daily with systemd (Linux)
Create the following two files in /etc/systemd/system/:

✅ selicbot.service

```ini
[Unit]
Description=SelicBot - Daily checker for Copom minutes
After=network.target

[Service]
Type=oneshot
User=pi
WorkingDirectory=/home/pi/selicBot
ExecStart=/home/pi/selicBot/venv/bin/python /home/pi/selicBot/selic_bot_main.py
Environment=PYTHONUNBUFFERED=1
Restart=on-failure

[Install]
WantedBy=multi-user.target
```

⏰ selicbot.timer

```ini
[Unit]
Description=Run SelicBot daily at 09:00 AM

[Timer]
OnCalendar=*-*-* 09:00:00
Persistent=true

[Install]
WantedBy=timers.target
```

Then run:

```bash
sudo systemctl daemon-reload
sudo systemctl enable selicbot.timer
sudo systemctl start selicbot.timer
```

## 💬 Example Output

```txt
📎 Looking for the latest valid report based on a map of known dates...
🔗 Trying to download: https://www.bcb.gov.br/content/copom/atascopom/Copom271-not20250618271.pdf
📥 Success! Report 271 downloaded from: https://www.bcb.gov.br/content/copom/atascopom/Copom271-not20250618271.pdf

📊 AI-generated commentary on Selic trend:
Based on the most recent Copom minutes, the Central Bank indicates...
Suggested investment strategy: consider fixed-income securities such as...
```

## 🧠 Ideas for future development

- 📲 Integration with WhatsApp via Twilio or WPPConnect
- 🧾 Store analysis results in a database (e.g. SQLite or Firebase)
- 🌐 Frontend dashboard to visualize trends
- 📡 API for third-party integration

## 📘 License
MIT License — see LICENSE

## ✨ Author
Developed by Henrique Andrade — suggestions and contributions welcome!








