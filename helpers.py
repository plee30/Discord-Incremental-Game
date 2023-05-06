import discord

def fail_embed_creator(ctx, title: str, description: str):
    embed = discord.Embed(
        title = title,
        description= description,
        color=discord.Color.red()
    )
    embed.set_author(
        name=ctx.author.display_name,
        icon_url=ctx.author.display_avatar.url
    )
    return embed

def success_embed_creator(ctx, title: str, description: str):
    embed = discord.Embed(
        title = title,
        description= description,
        color=discord.Color.green()
    )
    embed.set_author(
        name=ctx.author.display_name,
        icon_url=ctx.author.display_avatar.url
    )
    return embed