<div align="center">

# 🛰️ Airdrop Commander
## *Professional Multi-Server Dispatch Logic for Alpha Communities*

[![Version](https://img.shields.io/badge/version-1.2.0-blueviolet?style=for-the-badge)](https://github.com/HemachandRavulapalli/Discord-Airdrop-Bot)
[![Discord.py](https://img.shields.io/badge/Discord.py-2.6.4-blue?style=for-the-badge&logo=discord)](https://discordpy.readthedocs.io/)
[![FastAPI](https://img.shields.io/badge/FastAPI-0.128.0-green?style=for-the-badge&logo=fastapi)](https://fastapi.tiangolo.com/)

---

A high-performance Discord airdrop dispatch tool designed for alpha callers and community managers. Dispatch rich announcements, images, and forum threads across multiple servers simultaneously with real-time tracking.

[Explore Docs](#-getting-started) • [View Features](#-key-features) • [Report Bug](https://github.com/HemachandRavulapalli/Discord-Airdrop-Bot/issues)

</div>

---

## 📖 Table of Contents
- [✨ Key Features](#-key-features)
- [🛰️ Mission Control Explorer](#️-mission-control-explorer)
- [🛠️ Tech Stack](#️-tech-stack)
- [🚀 Getting Started](#-getting-started)
- [⚙️ Configuration](#️-configuration)
- [📁 Preset Management](#-preset-management)
- [📜 License](#-license)

---

## ✨ Key Features

#### 💎 Premium UI/UX
Sleek glassmorphism interface with live preview, progress tracking, and interactive mission logs.

#### 🛰️ Mission Control
Real-time logging and per-channel status updates during dispatch missions. Track your "Mission Accomplished" status live.

#### 🏷️ Visual Forum Tags
Scans Forum channels and lets you choose project tags (Announcement, Live, etc.) via clickable chips.

#### 🪄 Magic Sync
Automatically matches and selects tags across multiple servers based on their names. Pick one, sync them all.

#### 👤 Smart Role Memory
The bot **remembers** which ping role you use for each unique server and automatically reapplies it in future missions.

#### 🖼️ Rich Embeds
Full support for custom embed colors and drag-and-drop image attachments for maximum impact.

---

## 🛰️ Mission Control Explorer

The **Server Explorer** has been completely reinvented for speed:
- **🔍 Deep Search**: Filter through hundreds of servers and channels instantly.
- **✅ Multi-Select Checkboxes**: Manually pick your targets or Use "Select All Visible" for bulk operations.
- **📂 Thread Discovery**: Automatically finds active threads or creates new ones in Forum channels.

---

## 🛠️ Tech Stack

| Component | Technology | Use Case |
| :--- | :--- | :--- |
| **Backend** | Python / FastAPI | High-concurrency mission handling |
| **Discord** | Discord.py | Asynchronous gateway interactions |
| **Frontend** | Vanilla JS / CSS3 | Premium Glassmorphic Dashboard |
| **Logic** | Asynchronous Tasks | Background project dispatching |

---

## 🚀 Getting Started

### 1️⃣ Clone the Repository
```bash
git clone https://github.com/HemachandRavulapalli/Discord-Airdrop-Bot.git
cd Discord-Airdrop-Bot
```

### 2️⃣ Install Dependencies
```bash
pip install -U discord.py fastapi uvicorn pydantic
```

### 3️⃣ Launch the Commander
Run the PowerShell helper:
```bash
./run.ps1
```
*Or run directly:* `python bot_api.py`

---

## ⚙️ Configuration

Airdrop Commander uses a `.env` file for secure token management.
1. Create a `.env` file in the root.
2. Add your token: `DISCORD_BOT_TOKEN=your_token_here`

---

## 📁 Preset Management

Save complex mission configurations as **Presets**.
- **💾 Save**: Store channel sets, tags, and role configurations.
- **📂 Load**: Rapidly switch between different mission targets.
- **🗑️ Delete**: Clean up old configuration data from the server.

---

## 📜 License
This project is licensed under the MIT License - see the [LICENSE](LICENSE) file for details.

---

<div align="center">
Built with ❤️ for the Alpha Community. 🛰️🚀
</div>
