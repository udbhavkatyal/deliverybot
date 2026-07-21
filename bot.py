import os
import discord
from keep_alive import keep_alive

# Start web server (for Render)
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

# (Project, New List) -> Destination Channel
ROUTES = {
    ("gfx-a max level", "changes"): 1529209875505348628,
    ("gfx-a max level", "zappp"): 1529209943767646208,
    ("gfx-a max level", "please review"): 1529226562958786731,

    ("socials max level", "changes"): 1529211127890837554,
    ("socials max level", "zappp"): 1529210990909194280,
    ("socials max level", "please review"): 1529226439851905054,

    ("video trimax", "changes"): 1529212411238944888,
    ("video trimax", "zappp"): 1529212366208634940,
    ("video trimax", "please review"): 1529225648952840262,

    ("gfx-b trimax", "changes"): 1529212768287199252,
    ("gfx-b trimax", "zappp"): 1529212728693100726,
    ("gfx-b trimax", "zappp"): 1529226642688577687
}

intents = discord.Intents.default()
intents.message_content = True

client = discord.Client(intents=intents)


@client.event
async def on_ready():
    print(f"Logged in as {client.user}")


@client.event
async def on_message(message):

    # Ignore only this bot's own messages
    if message.author.id == client.user.id:
        return

    # Only monitor selected channels
    if message.channel.id not in MONITORED_CHANNELS:
        return

    # Used for finding the project name
    searchable = (message.content or "").lower()

    # We'll ONLY use this for Delivery / Changes / ZAPPP
    new_list = ""

    for embed in message.embeds:

        # Project name can appear in these places
        if embed.title:
            searchable += " " + embed.title.lower()

        if embed.description:
            searchable += " " + embed.description.lower()

        if embed.author and embed.author.name:
            searchable += " " + embed.author.name.lower()

        if embed.footer and embed.footer.text:
            searchable += " " + embed.footer.text.lower()

        # Read only the New List field
        for field in embed.fields:

            if field.name.strip().lower() == "new list":
                new_list = field.value.strip().lower()

    print("=" * 60)
    print("SEARCHABLE:", searchable)
    print("NEW LIST :", new_list)
    print("=" * 60)

    # -----------------------------
    # DELIVERY
    # -----------------------------
    if "delivery" in new_list:

        delivery_channel = client.get_channel(DELIVERY_CHANNEL_ID)

        if delivery_channel:
            await delivery_channel.send(
                f"📦 **Delivery Ready**\n\n{message.jump_url}"
            )

    # -----------------------------
    # ROUTING
    # -----------------------------
    for (project, status), destination in ROUTES.items():

        if project in searchable and status in new_list:

            target = client.get_channel(destination)

            if target:

                if status == "zappp":

                    await target.send(
                        f"Need your attention please, ⚡ **ZAP Request**\n\n"
                        f"{message.jump_url}"
                    )

                elif status == "changes":

                    await target.send(
                        f"📨 Changes aya hai\n\n"
                        f"{message.jump_url}"
                    )

                elif status == "please review":

                    await target.send(
                        f"🚔 Review and quality check required!\n\n"
                        f"{message.jump_url}"
                    )

            break


client.run(TOKEN)