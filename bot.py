import discord

TOKEN = "MTUyOTExMDkwMDcxNDUwNDE5Mw.GlXQtp.4insnm4j9VldBvN7d2rNJCX8uEegY5wI-uLELw"

TARGET_CHANNEL_ID = 1529112525998784584

KEYWORDS = [
    "delivery"
]

intents = discord.Intents.default()
intents.message_content = True

client = discord.Client(intents=intents)


@client.event
async def on_ready():
    print(f"Logged in as {client.user}")


@client.event
async def on_message(message):

    # Ignore only THIS bot's own messages
    if message.author.id == client.user.id:
        return

    searchable = message.content or ""

    # Include all embed text
    for embed in message.embeds:

        if embed.title:
            searchable += " " + embed.title

        if embed.description:
            searchable += " " + embed.description

        for field in embed.fields:
            searchable += f" {field.name} {field.value}"

        if embed.footer and embed.footer.text:
            searchable += " " + embed.footer.text

        if embed.author and embed.author.name:
            searchable += " " + embed.author.name

    searchable = searchable.lower()

    print("SEARCHABLE:")
    print(searchable)
    print("-" * 50)

    if any(word in searchable for word in KEYWORDS):

        target = client.get_channel(TARGET_CHANNEL_ID)

        if target:

            await target.send(
                f"📦 **Delivery Ready**\n\n"
                f"{message.jump_url}"
            )


client.run(TOKEN)