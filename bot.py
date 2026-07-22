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
    ("gfx-b trimax", "please review"): 1529226642688577687,
}

GENERAL_ROUTES = {
    "gfx-a max level": 1529244047657533500,
    "socials max level": 1529243389923557396,
    "video trimax": 1529243080585248981,
    "gfx-b trimax": 1529244101055086632,
}

COMMENT_ROUTES = {
    "@faizanahmad116": 1529466762943271082,
    "@bishalhaldar": 1529466857449586770,
    "@pushpindersingh44": 1529467024281964674,
    "@yashtehlan": 1529467090329665576,
    "@ankit1005": 1529467211213705386,
    "@abhishekkharwar": 1529467141214961704,
    "@udbhavkatyal1": 1529467607139356743,
}

IGNORED_LISTS = {
    "done",
    "saved stuff",
    "ideas/trends",
    "awaiting inputs",
    "please review",
    "zappp",
    "⚡zappp",
    "changes",
    "priority list",
    "client review",
    "delivery",
}


def normalize_list_name(name):
    return name.lower().replace("⚡", "").strip()


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

    # Destination list (works for both moved and newly created cards)
    new_list = ""

    # Trello comment text
    comment_text = ""

    for embed in message.embeds:

        # Project name can appear in these places
        if embed.title:
            searchable += " " + embed.title.lower()

        if embed.description:
            desc = embed.description.lower()
            searchable += " " + desc
            comment_text += " " + desc

        if embed.author and embed.author.name:
            searchable += " " + embed.author.name.lower()

        if embed.footer and embed.footer.text:
            searchable += " " + embed.footer.text.lower()

        # Read only the destination list
        for field in embed.fields:

            field_name = field.name.strip().lower()

            # Card moved
            if field_name == "new list":
                new_list = normalize_list_name(field.value)

            # Card created
            elif field_name == "list" and not new_list:
                new_list = normalize_list_name(field.value)

    print("=" * 60)
    print("SEARCHABLE:", searchable)
    print("NEW LIST :", new_list)
    print("COMMENT  :", comment_text)
    print("=" * 60)

    # -----------------------------
    # COMMENT MENTIONS
    # -----------------------------
    if comment_text:

        sent_channels = set()

        for username, destination in COMMENT_ROUTES.items():

            if username.lower() in comment_text:

                if destination in sent_channels:
                    continue

                target = client.get_channel(destination)

                if target:
                    await target.send(
                        f"💬 You were mentioned in a Trello comment.\n\n"
                        f"{message.jump_url}"
                    )

                    sent_channels.add(destination)

    # -----------------------------
    # DELIVERY
    # -----------------------------
    if new_list == "delivery":

        delivery_channel = client.get_channel(DELIVERY_CHANNEL_ID)

        if delivery_channel:
            await delivery_channel.send(
                f"📦 **Delivery Ready**\n\n{message.jump_url}"
            )

    # -----------------------------
    # ROUTING
    # -----------------------------
    handled = False

    for (project, status), destination in ROUTES.items():

        if project in searchable and status == new_list:

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

            handled = True
            break

    # -----------------------------
    # GENERAL LIST ROUTING
    # -----------------------------
    if (
        not handled
        and new_list
        and new_list not in IGNORED_LISTS
    ):

        for project, destination in GENERAL_ROUTES.items():

            if project in searchable:

                target = client.get_channel(destination)

                if target:
                    await target.send(
                        f"🏷️ Task raised. Client/Project: {new_list.title()}\n\n"
                        f"{message.jump_url}"
                    )

                break


client.run(TOKEN)