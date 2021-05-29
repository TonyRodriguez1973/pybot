import discord
from discord.ext import commands, tasks
import random

bot = commands.Bot(command_prefix = "!", description = "Cacahuète Bot")

status = ["Gang",
		"A votre service",
		"L'eau mouille", 
		"Le feu brule", 
		"Lorsque vous volez, vous ne touchez pas le sol", 
		"Winter is coming", 
		"Mon créateur est Tony", 
		"Il n'est pas possible d'aller dans l'espace en restant sur terre", 
		"La terre est ronde",
		"La moitié de 2 est 1",
		"7 est un nombre heureux",
		"Les allemands viennent d'allemagne",
		"Le coronavirus est un virus se répandant en Europe, en avez vous entendu parler ?",
		"J'apparais 2 fois dans l'année, a la fin du matin et au début de la nuit, qui suis-je ?",
		"Le plus grand complot de l'humanité est",
		"Pourquoi lisez vous ca ?"]



@bot.event
async def on_ready():
	print("Ready !")
	changeStatus.start()


@bot.command()
async def say(ctx, *texte):
	await ctx.send(" ".join(texte))


@bot.command()
async def serverInfo(ctx):
	server = ctx.guild
	numberOfTextChannels = len(server.text_channels)
	numberOfVoiceChannels = len(server.voice_channels)
	serverDescription = server.description
	numberOfPerson = server.member_count
	serverName = server.name
	message = f"Le serveur *** {serverName} *** comptabilise \n{numberOfPerson} personnes. \n{numberOfTextChannels} salons écrit \n{numberOfVoiceChannels} salon vocaux."
	await ctx.send(message)
	print("répond a la commande !serverInfo")

def isOwner(ctx):
	return ctx.message.author.id == 416325533119283200 

@bot.command()
@commands.check(isOwner)
async def kick(ctx, user : discord.User, *reason):
	reason = " ".join(reason)
	await ctx.guild.kick(user, reason = reason)
	await ctx.send(f"{user} à été kick.")
	print(f"{user} à été kick pour la raison suivante: {reason}")



@bot.command()
@commands.check(isOwner)
async def private(ctx):
	await ctx.send("yes")
	print("tu es fort")


@bot.command()
@commands.check(isOwner)
async def ban(ctx, user : discord.User, *, reason = "aucune"):
	reason = " ".join(reason)
	#await ctx.guild.ban(user, reason = reason)
	embed = discord.Embed(title = "**Banissement**", description = "Un Staff a frappé !", url = "https://discord.com/assets/f7b3f6b926cb31a17d4928d076febab4.svg", color=0x20b2aa)
	embed.set_thumbnail(url = "https://discordemoji.com/assets/emoji/BanneHammer.png")
	embed.add_field(name = "Membre banni", value = user.name)
	embed.add_field(name = "Raison", value = reason)
	embed.add_field(name = "Staff", value = ctx.author.name)

	await ctx.send(embed = embed)

	#await ctx.send(f"{user} à été ban pour la raison suivante : {reason}.")
	print("Un staff a banni un membres")


@bot.command()
@commands.check(isOwner)
async def unban(ctx, user, reason):
	reason = " ".join(reason)
	userName, userId = user.split("#")
	bannedUsers = await ctx.guild.bans()
	for i in bannedUsers:
		if i.user.name == userName and i.user.discriminator == userId:
			await ctx.guild.unban(i.user, reason = reason)
			await ctx.send(f"{user} à été débanni.")
			print(f"L'utilisateur {user} à été débanni.")
			return
			#non trouvé
			await ctx.send(f"L'utilisateur {user} n'as pas était trouvé.")


@bot.command()
@commands.check(isOwner)
async def clear(ctx, nombre : int):
	messages = await ctx.channel.history(limit = nombre + 1).flatten()
	for message in messages:
		await message.delete()
		print(f"j'ai supprimer {nombre} messages.")


@bot.command()
async def start(ctx, secondes = 5):
	changeStatus.change_interval(seconds = secondes)


@tasks.loop(seconds = 5)
async def changeStatus():
	game = discord.Game(random.choice(status))
	await bot.change_presence(status = discord.Status.dnd, activity = game)

async def createMutedRole(ctx):
    mutedRole = await ctx.guild.create_role(name = "Muted",
                                            permissions = discord.Permissions(
                                                send_messages = False,
                                                speak = False),
                                            reason = "Creation du role Muted pour mute des gens.")
    for channel in ctx.guild.channels:
        await channel.set_permissions(mutedRole, send_messages = False, speak = False)
    return mutedRole

async def getMutedRole(ctx):
    roles = ctx.guild.roles
    for role in roles:
        if role.id == 848321726626005033:
            return role
    
    return await createMutedRole(ctx)

@bot.command()
async def mute(ctx, member : discord.Member, *, reason = "Aucune raison n'a été renseigné"):
    mutedRole = await getMutedRole(ctx)
    await member.add_roles(mutedRole, reason = reason)
    await ctx.send(f"{member.mention} a été mute !")
    print(f"{member} a été mute par <@{ctx.author.id}> pour {reason}")

@bot.command()
async def unmute(ctx, member : discord.Member, *, reason = "Aucune raison n'a été renseigné"):
    mutedRole = await getMutedRole(ctx)
    await member.remove_roles(mutedRole, reason = reason)
    await ctx.send(f"{member.mention} a été unmute !")
    print(f"{member} a été unmute par <@{ctx.author.id}>")

bot.run("ODQ3MjExNjM2MjA4OTU5NTcw.YK6xUg.xFKc-tnWNOZue0oFXZqkb8Kh6R8")