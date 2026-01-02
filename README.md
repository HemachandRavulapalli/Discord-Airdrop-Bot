# 🛰️ Airdrop Commander - Junior Kai

![Version](https://img.shields.io/badge/version-1.2.0-blueviolet)
![Discord.py](https://img.shields.io/badge/Discord.py-2.6.4-blue)
![FastAPI](https://img.shields.io/badge/FastAPI-0.128.0-green)
![License](https://img.shields.io/badge/license-MIT-success)

**Airdrop Commander** (codenamed *Junior Kai*) is a high-performance Discord dispatch tool built for alpha callers, community managers, and project leads. It allows for seamless, instantaneous message distribution across multiple servers, channels, and forum threads with a premium glassmorphic interface.

---

## � Visual Excellence
*   **💎 Glassmorphism Dashboard**: A stunning, modern UI that feels premium and responsive.
*   **👁️ Live Discord Preview**: See exactly how your message will look on Discord (including embeds and images) before you hit dispatch.
*   **� Mission Control**: Real-time progress bars and logs tracking every successful delivery.

## 🚀 Core Features
- **🛰️ Server Explorer Deep-Scan**: Browse all your servers, text channels, and forum threads directly from the dashboard.
- **✅ Multi-Selection**: Pick specific target channels using checkboxes or use the "Select All Visible" master toggle.
- **🏷️ Smart Forum Tagging**: Automatically detects forum project tags and allows you to sync them by name across different servers.
- **� Role Memory**: Remembers the specific ping role for every unique server, automating your workflow over time.
- **📁 Advanced Presets**: Save complex multi-server configurations to the server and load or delete them with a single click.
- **�️ Rich Embed Support**: Customize embed colors and drag-and-drop images for high-impact announcements.

---

## �️ Installation & Setup

### 1. Prerequisites
- Python 3.11+
- Discord Bot Token (with Message Content Intent enabled)

### 2. Clone & Install
```bash
git clone https://github.com/yourusername/Airdrop-Commander.git
cd Airdrop-Commander
pip install discord.py fastapi uvicorn pydantic
```

### 3. Environment Configuration
Create a `.env` file in the root directory:
```env
DISCORD_BOT_TOKEN=your_token_here
```

### 4. Launch
```bash
python bot_api.py
```
Then navigate to `http://localhost:8000` in your browser.

---

## 📡 Tech Stack
- **Backend**: Python 3.11 with `FastAPI` & `Uvicorn`
- **Discord Integration**: `Discord.py` (Asynchronous Gateway)
- **Frontend**: Vanilla JavaScript (ES6+), HTML5, CSS3
- **Design System**: Glassmorphism with Antigravity animations
- **Persistence**: Local JSON storage for presets and memory

---

## 🤝 Contributing
Contributions are welcome! Please open an issue or submit a pull request for any features or bug fixes.

## 📜 License
This project is licensed under the MIT License - see the LICENSE file for details.

---
*Built for the next generation of Web3 community management.* 🛰️🚀
