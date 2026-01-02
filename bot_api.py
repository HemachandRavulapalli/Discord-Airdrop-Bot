import os
import base64
import asyncio
import io
import json
import traceback
from pathlib import Path
import discord
from discord.ext import commands
from fastapi import FastAPI, HTTPException, BackgroundTasks
from fastapi.responses import FileResponse
from fastapi.staticfiles import StaticFiles
from pydantic import BaseModel
from typing import List, Optional
from contextlib import asynccontextmanager
import uvicorn
from fastapi.middleware.cors import CORSMiddleware

# --- Configuration ---
def load_env_file():
    env_path = Path(".env")
    if env_path.exists():
        with open(env_path, "r") as f:
            for line in f:
                if "=" in line and not line.startswith("#"):
                    key, value = line.strip().split("=", 1)
                    os.environ[key] = value.strip().strip('"').strip("'")

load_env_file()
TOKEN = os.getenv("DISCORD_BOT_TOKEN")

# --- Lifespan Setup ---
@asynccontextmanager
async def lifespan(app: FastAPI):
    # Startup: Start the bot in the background
    if TOKEN:
        # Define a task that won't crash the server if the bot fails
        async def run_bot():
            try:
                await bot.start(TOKEN)
            except Exception as e:
                print(f"[Bot Error] Could not start bot: {e}")
        
        asyncio.create_task(run_bot())
        print("Bot connection task initialized.")
    else:
        print("[!] CRITICAL: DISCORD_BOT_TOKEN is missing. Please check your .env file.")
    yield
    # Shutdown: Close the bot connection
    print("Shutting down bot...")
    await bot.close()

# --- FastAPI Setup ---
app = FastAPI(title="Airdrop Commander API", lifespan=lifespan)

# Enable CORS for the frontend
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# --- Discord Bot Setup ---
intents = discord.Intents.default()
intents.message_content = True
bot = commands.Bot(command_prefix="!", intents=intents)

# --- Data Models ---
class ChannelConfig(BaseModel):
    nickname: Optional[str] = None
    channelId: str
    tagIds: List[str] = []
    roleId: Optional[str] = None

class DispatchPayload(BaseModel):
    title: str
    content: str
    imageDataURI: Optional[str] = None
    channels: List[ChannelConfig]
    useEmbed: bool = False
    embedColor: str = "#5865f2"

class PresetPayload(BaseModel):
    name: str
    channels: List[ChannelConfig]

PRESETS_FILE = Path("presets.json")

def load_presets_from_file():
    if not PRESETS_FILE.exists():
        return {}
    with open(PRESETS_FILE, "r") as f:
        return json.load(f)

def save_presets_to_file(presets):
    with open(PRESETS_FILE, "w") as f:
        json.dump(presets, f, indent=4)

# --- Logging System ---
dispatch_logs = []

def add_log(status, message, channel_name="System", details=""):
    dispatch_logs.append({
        "time": discord.utils.utcnow().isoformat(),
        "status": status, # "success", "error", "processing"
        "message": message,
        "channel": channel_name,
        "details": details
    })
    if len(dispatch_logs) > 100:
        dispatch_logs.pop(0)

# --- Bot Logic ---
async def process_dispatch(payload: DispatchPayload):
    if not bot.is_ready():
        add_log("error", "Bot not ready", "System", "Discord bot is not yet connected.")
        return

    add_log("processing", f"Starting dispatch for: {payload.title}", "System")

    # Decode image if present
    file = None
    if payload.imageDataURI and "," in payload.imageDataURI:
        try:
            header, encoded = payload.imageDataURI.split(",", 1)
            image_data = base64.b64decode(encoded)
            file = discord.File(io.BytesIO(image_data), filename="airdrop.png")
        except Exception as e:
            print(f"[Error] Failed to decode image: {e}")

    for config in payload.channels:
        try:
            if not config.channelId or not config.channelId.strip():
                continue
                
            channel = bot.get_channel(int(config.channelId))
            if not channel:
                channel = await bot.fetch_channel(int(config.channelId))
            
            if not channel:
                add_log("error", "Channel not found", config.nickname or str(config.channelId))
                continue

            # Prepare message content
            role_mention = ""
            if config.roleId:
                role_mention = f"<@&{config.roleId}>"

            # Put mention at the end as requested
            msg_content = payload.content
            if role_mention:
                msg_content = f"{payload.content}\n\n{role_mention}"
            
            # Reset variables for each channel
            current_file = None
            embed = None

            if payload.imageDataURI and "," in payload.imageDataURI:
                try:
                    header, encoded = payload.imageDataURI.split(",", 1)
                    image_data = base64.b64decode(encoded)
                    current_file = discord.File(io.BytesIO(image_data), filename="airdrop.png")
                except: pass
            
            if payload.useEmbed:
                embed = discord.Embed(
                    title=payload.title,
                    description=payload.content,
                    color=int(payload.embedColor.lstrip('#'), 16)
                )
                if current_file:
                    embed.set_image(url="attachment://airdrop.png")
                # When using embed, msg_content is just the footer mention
                msg_content = role_mention
            else:
                # Forum thread name handles title; Text channel header handled below
                pass

            # For text channels, if not using embed, add the title as bold header
            text_msg_content = msg_content
            if not payload.useEmbed and payload.title:
                text_msg_content = f"**{payload.title}**\n{msg_content}"

            # Prepare message parameters for text channels
            send_kwargs = {"content": text_msg_content}
            if embed:
                send_kwargs["embed"] = embed
            if current_file:
                send_kwargs["file"] = current_file

            if isinstance(channel, discord.ForumChannel):
                applied_tags = []
                if config.tagIds:
                    existing_tags = {str(t.id): t for t in channel.available_tags}
                    applied_tags = [existing_tags[tid] for tid in config.tagIds if tid in existing_tags]
                
                # Forum thread creation
                thread_kwargs = {
                    "name": payload.title or "Airdrop Update",
                    "content": msg_content
                }
                if embed: thread_kwargs["embed"] = embed
                if current_file: thread_kwargs["file"] = current_file
                if applied_tags: thread_kwargs["applied_tags"] = applied_tags

                await channel.create_thread(**thread_kwargs)
                add_log("success", f"Created NEW thread", channel.name)
            
            elif isinstance(channel, (discord.Thread, discord.TextChannel)):
                await channel.send(**send_kwargs)
                add_log("success", f"Sent message", channel.name)
            
            else:
                add_log("error", "Unsupported channel", str(config.channelId))

        except discord.Forbidden:
            add_log("error", "Forbidden (Missing Perms)", config.nickname or config.channelId)
        except Exception as e:
            error_details = traceback.format_exc()
            add_log("error", str(e), config.nickname or config.channelId, error_details)
            print(f"[Error] Dispatch failed for {config.channelId}: {error_details}")

        await asyncio.sleep(0.3)
    
    add_log("success", "MISSION_ACCOMPLISHED", "System")

@app.post("/dispatch")
async def dispatch(payload: DispatchPayload, background_tasks: BackgroundTasks):
    if not TOKEN:
        raise HTTPException(status_code=500, detail="Discord Bot Token is not set. Please add DISCORD_BOT_TOKEN to your .env file.")
    
    # We run the dispatch in the background to respond to the UI immediately
    background_tasks.add_task(process_dispatch, payload)
    return {"status": "dispatched", "message": f"Processing dispatch to {len(payload.channels)} channels"}

@app.get("/threads/{channel_id}")
async def get_channel_threads(channel_id: int):
    if not bot.is_ready():
        raise HTTPException(status_code=503, detail="Bot not ready")
    
    try:
        channel = bot.get_channel(channel_id)
        if not channel:
            channel = await bot.fetch_channel(channel_id)
            
        if not isinstance(channel, (discord.ForumChannel, discord.TextChannel)):
            return []
            
        threads = []
        # Active threads
        for t in channel.threads:
            threads.append({"name": t.name, "id": str(t.id)})
            
        # Archived threads (Forums only)
        if isinstance(channel, discord.ForumChannel):
            async for t in channel.archived_threads(limit=50):
                if not any(x["id"] == str(t.id) for x in threads):
                    threads.append({"name": t.name, "id": str(t.id)})
                    
        return threads
    except Exception as e:
        raise HTTPException(status_code=404, detail=str(e))

@app.get("/tags/{channel_id}")
async def get_channel_tags(channel_id: int):
    if not bot.is_ready():
        raise HTTPException(status_code=503, detail="Bot not ready")
    
    try:
        channel = bot.get_channel(channel_id)
        if not channel:
            channel = await bot.fetch_channel(channel_id)
            
        if not isinstance(channel, discord.ForumChannel):
            return []
            
        return [
            {"name": tag.name, "id": str(tag.id)} 
            for tag in channel.available_tags
        ]
    except Exception as e:
        raise HTTPException(status_code=404, detail=str(e))

@app.get("/roles/{channel_id}")
async def get_channel_roles(channel_id: int):
    if not bot.is_ready():
        raise HTTPException(status_code=503, detail="Bot not ready")
    
    try:
        channel = bot.get_channel(channel_id)
        if not channel:
            channel = await bot.fetch_channel(channel_id)
            
        guild = channel.guild
        return [
            {"name": role.name, "id": str(role.id), "guild_id": str(guild.id)} 
            for role in guild.roles if not role.is_default()
        ]
    except Exception as e:
        raise HTTPException(status_code=404, detail=str(e))

@app.get("/health")
async def health():
    return {"status": "ok", "bot_ready": bot.is_ready()}

@app.get("/")
async def get_dashboard():
    return FileResponse("index.html")

# --- Preset Endpoints ---
@app.get("/presets")
async def list_presets():
    return list(load_presets_from_file().keys())

@app.get("/presets/{name}")
async def get_preset(name: str):
    presets = load_presets_from_file()
    if name not in presets:
        raise HTTPException(status_code=404, detail="Preset not found")
    return presets[name]

@app.post("/presets")
async def save_preset(preset: PresetPayload):
    presets = load_presets_from_file()
    presets[preset.name] = preset.model_dump()
    save_presets_to_file(presets)
    return {"status": "saved"}

@app.delete("/presets/{name}")
async def delete_preset(name: str):
    presets = load_presets_from_file()
    if name in presets:
        del presets[name]
        save_presets_to_file(presets)
        return {"status": "deleted"}
    raise HTTPException(status_code=404, detail="Preset not found")

@app.get("/logs")
async def get_logs():
    return dispatch_logs

@app.get("/explore")
async def explore_servers():
    if not bot.is_ready():
        raise HTTPException(status_code=503, detail="Bot not ready")
    
    explorer_data = []
    for guild in bot.guilds:
        guild_info = {
            "name": guild.name,
            "id": str(guild.id),
            "channels": [],
            "roles": [{"name": r.name, "id": str(r.id)} for r in guild.roles if not r.is_default()]
        }
        
        # Get Forums and Text Channels
        for channel in guild.channels:
            if isinstance(channel, (discord.TextChannel, discord.ForumChannel)):
                chan_data = {
                    "name": channel.name,
                    "id": str(channel.id),
                    "guild_id": str(guild.id),
                    "type": "forum" if isinstance(channel, discord.ForumChannel) else "text",
                    "threads": [],
                    "available_tags": []
                }
                
                # Fetch tags for forum channels
                if isinstance(channel, discord.ForumChannel):
                    chan_data["available_tags"] = [
                        {"name": tag.name, "id": str(tag.id)} 
                        for tag in channel.available_tags
                    ]

                # Fetch active threads
                if hasattr(channel, 'threads'):
                    for thread in channel.threads:
                        chan_data["threads"].append({
                            "name": thread.name,
                            "id": str(thread.id)
                        })
                
                guild_info["channels"].append(chan_data)
        
        explorer_data.append(guild_info)
    
    return explorer_data

# (on_event startup moved to lifespan)

if __name__ == "__main__":
    uvicorn.run(app, host="0.0.0.0", port=8000)
