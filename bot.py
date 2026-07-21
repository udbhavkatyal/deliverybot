import os
import discord
from keep_alive import keep_alive

# Start web server (for Render Web Service / health check)
keep_alive()

TOKEN = os.environ["TOKEN"]

# Delivery notification channel
DELIVERY_CHANNEL_ID = 1529112525998784584

# Only monitor these channels
MONITORED_CHANNELS = {
    1528616846872547348,
    1528618690365620226,
    1528068088317350059,
    1528613251557097512,
}

# (Project, Status) -> Destination Channel
ROUTES = {
    ("gfx-a max level", "changes"): 1529209875505348628,
    ("gfx-a max level", "zappp"): 1529209943767646208,

    ("socials max level", "changes"): 1529211127890837554,
    ("socials max level", "zappp"): 1529210990909194280,

    ("video trimax", "changes"): 1529212411238944888,
    ("video trimax", "zappp"): 1529212366208634940,

    ("gfx-b trimax", "changes"): 1529212768287199252,
    ("gfx-b trimax", "zappp"): 1529212728693100726,
}

intents = discord.Intents.default()
intents.message_content = True

client = discord.Client(intents=intents)


@client.event
async def on_ready():
    print(f"Logged in as {client.user}")


@client.event
async def on_message(message):

    # Ignore this bot's own messages
    if message.author.id == client.user.id:
        return

    # Only monitor selected channels
    if message.channel.id not in MONITORED_CHANNELS:
        return

    searchable = message.content or ""

    # Include all embed text
    for embed in message.embeds:

        if embed.title:
            searchable += " " + embed.title

        if embed.description:
            searchable += " " + embed.description

        if embed.author and embed.author.name:
            searchable += " " + embed.author.name

        if embed.footer and embed.footer.text:
            searchable += " " + embed.footer.text

        for field in embed.fields:
            searchable += f" {field.name} {field.value}"

    searchable = searchable.lower()

    print("=" * 60)
    print(searchable)
    print("=" * 60)

    # -----------------------------
    # DELIVERY
    # -----------------------------
    if "delivery" in searchable:

        delivery_channel = client.get_channel(DELIVERY_CHANNEL_ID)

        if delivery_channel:
            await delivery_channel.send(
                f"📦 **Delivery Ready**\n\n{message.jump_url}"
            )

    # -----------------------------
    # ROUTING
    # -----------------------------
    for (project, status), destination in ROUTES.items():

        if project in searchable and status in searchable:

            target = client.get_channel(destination)

            if target:

                if status == "zappp":
                    await target.send(
                        f"Need your attention please, ⚡ **ZAP Request**\n\n{message.jump_url}"
                    )

                else:  # Changes
                    await target.send(
                        f"📨 Changes aya hai\n\n{message.jump_url}"
                    )

            break


client.run(TOKEN)