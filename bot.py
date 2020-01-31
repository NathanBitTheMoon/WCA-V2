token = ''

import discord
from discord.ext.commands import Bot
import wca, urllib
import datetime, time, json, announcement

client = Bot(command_prefix = '?')

announcement_client = announcement.Announcement(None)

def log_usage(command, arg):
    f = open('use.log', 'a')
    f.write("\n" + str(int(time.time())) + ":" + command + f"({arg})")
    f.close()

def log_action(action):
    f = open('use.log', 'a')
    f.write(";" + action)
    f.close()

@client.event
async def on_ready():
    print(f"{client.user.name} is now online")

    activity = discord.Game(name = "with squares. Type ?help, I'm back")
    await client.change_presence(status = discord.Status.online, activity = activity)

@client.command(name = "person", pass_context = True, help = "Get basic information about someone. Usage: ?person <name / WCA ID>")
async def person(ctx, *args):
    log_usage("person", ' '.join(args))
    query_string = ' '.join(args)

    embed_loading = discord.Embed(description = "Loading...")
    message = await ctx.channel.send(embed = embed_loading)

    user_data = None
    user_query_success = True

    if wca.Utils.is_wca_id(query_string):
        try:
            user_data = wca.User.from_page(f"https://www.worldcubeassociation.org/persons/{query_string.upper()}")
            log_action("wcaid-success")
        except IndexError:
            user_query_success = False
            log_action("wcaid-fail")
    
    if not wca.Utils.is_wca_id(query_string) or not user_query_success:
        try:
            search = wca.Search(query_string)
            user_data = wca.User.from_page(f"https://www.worldcubeassociation.org/persons/{search.user_result[0].wca_id}")
            user_query_success = True
            log_action("name-success")
        except:
            user_query_success = False
            log_action("name-fail")

    if user_query_success:
        embed_content = discord.Embed(title = f"WCA info for {user_data.name}")
        embed_content.set_thumbnail(url = user_data.avatar)

        embed_content.add_field(name = "Name", value = user_data.name)
        embed_content.add_field(name = "Country", value = f":flag_{user_data.country[0]}: {user_data.country[1]}")
        embed_content.add_field(name = "Gender", value = user_data.gender)
        embed_content.add_field(name = "WCA ID", value = user_data.wca_id)
        embed_content.add_field(name = "Completed Solves", value = user_data.completed_solves)
        embed_content.add_field(name = "Competitons Attended", value = user_data.comp_count)

        best_event = wca.User.best_event(user_data.personal_records, "wr_single")
        embed_content.add_field(name = "Best event (WR) single", value = best_event.event().name)

        best_event = wca.User.best_event(user_data.personal_records, "wr_average")
        embed_content.add_field(name = "Best event (WR) average", value = best_event.event().name)

        #best_event = wca.User.worst_event(user_data.personal_records, "wr_single")
        #embed_content.add_field(name = "Worst event (WR)", value = best_event.event().name)

        await message.edit(embed = embed_content)
        
        del embed_content

        #embed_content = discord.Embed(title = f"Medal and record collection")
        #embed_content.add_field(name = "Gold", value = user_data.medal_collection.gold)
        #embed_content.add_field(name = "Silver", value = user_data.medal_collection.silver)
        #embed_content.add_field(name = "Bronze", value = user_data.medal_collection.bronze)

        #if user_data.medal_collection.wr != 0:
        #   embed_content.add_field(name = "World records", value = user_data.medal_collection.wr)
        #embed_content.add_field(name = "Continental records", value = user_data.medal_collection.cr)
        #embed_content.add_field(name = "National records", value = user_data.medal_collection.nr)
            
        #if len(embed_content.fields) != 0:
        #    await ctx.channel.send(embed = embed_content)
    else:
        embed_content = discord.Embed(title = f"No results for \"{query_string}\"", description = ":warning: No results for your search. Check the spelling.")
        await message.edit(embed = embed_content)

@client.command(name = "ranking", pass_context = True, help = "Get a list of the top 5 people for an event. Usage: ?ranking country, event (country can be blank)")
async def ranking(ctx, *args):
    log_usage("ranking", ' '.join(args))
    query_string = ' '.join(args)

    embed_loading = discord.Embed(description = "Loading...")
    message = await ctx.channel.send(embed = embed_loading)

    countries = json.load(open('countries.json', 'r'))
    continents = json.load(open('continents.json', 'r'))
    country = "world"
    event = None
    found = ""

    # Get country
    for c in continents:
        if c['name'].lower() in query_string.lower():
            country = c['id']
            found = c['name']
            log_action("cid")
    for i in countries:
        if i['name'].lower() in query_string.lower() or query_string.lower() in i['name'].lower():
            country = i['id']
            found = i['name']
            log_action("name")
        elif i['id'].lower() in query_string.lower() or query_string.lower() in i['id'].lower():
            country = i['id']
            found = i['id']
            log_action("id")
    
    average = ['average', 'avg']
    single = ['single']
    ranking_type = "single"

    for i in average:
        if i in query_string:
            ranking_type = "average"
    
    for i in single:
        if i in query_string:
            ranking_type = "single"
    
    query_string = query_string.replace(found, "").strip()
    event = wca.Event.query_event(query_string)

    rankings = wca.Ranking(event, area = country, ranking_type = ranking_type)

    names = []
    wca_id = []
    value = []
    
    for i in rankings.results[:5]:
        names.append(i.name)
        wca_id.append(i.wca_id)
        value.append(i.result)
    
    embed_content = discord.Embed(title = f"{ranking_type[0].upper()}{ranking_type[1:]} {event().name} rankings for {country.replace('_', '')}")

    embed_content.add_field(name = "Name", value = '\n'.join(names))
    embed_content.add_field(name = "WCA ID", value = '\n'.join(wca_id))
    embed_content.add_field(name = "Result", value = '\n'. join(value))

    await message.edit(embed = embed_content)

@client.command(name = "pr", pass_context = True, help = "Get the personal records for a given person. Usage: ?pr <name / WCA ID>")
async def pr(ctx, *args):
    log_usage("pr", ' '.join(args))
    query_string = ' '.join(args)

    embed_loading = discord.Embed(description = "Loading...")
    message = await ctx.channel.send(embed = embed_loading)

    user_data = None
    user_query_success = True

    if wca.Utils.is_wca_id(query_string):
        try:
            user_data = wca.User.from_page(f"https://www.worldcubeassociation.org/persons/{query_string.upper()}")
            log_action("wcaid-success")
        except IndexError:
            user_query_success = False
            log_action("wcaid-fail")
    
    if not wca.Utils.is_wca_id(query_string) or not user_query_success:
        try:
            search = wca.Search(query_string)
            user_data = wca.User.from_page(f"https://www.worldcubeassociation.org/persons/{search.user_result[0].wca_id}")
            user_query_success = True
            log_action("name-success")
        except:
            user_query_success = False
            log_action("name-fail")
    
    if user_query_success:
        embed_content = discord.Embed(title = f"Personal records for {user_data.name}")
        event = []
        single = []
        average = []

        for i in user_data.personal_records:
            event.append(i.event().name)
            single.append(i.single)
            average.append(i.average)
        
        embed_content.add_field(name = "Event", value = '\n'.join(event))
        embed_content.add_field(name = "Single", value = '\n'.join(single))
        embed_content.add_field(name = "Average", value = '\n'.join(average))
    
        await message.edit(embed = embed_content)

@client.command(name = 'info', pass_context = True)
async def info(ctx):
    embed_content = discord.Embed(title = "About this bot", description = "This bot was devoleped by AutoPlay5. The code for the API and Discord bot is open source and free for anyone to use and audit. The bot only gathers usage information such as a list of server name or the use of a particular command. This data is completly anonymous. It was written in Python 3.7.")
    embed_content.add_field(name = "GitHub (Source Code)", value = "https://github.com/NathanBitTheMoon/WCA-V2")
    embed_content.add_field(name = "Latency", value = str(round(client.latency * 1000, 0)) + "ms")
    embed_content.add_field(name = "ISO 3166 credits", value = "https://github.com/lukes/ISO-3166-Countries-with-Regional-Codes/blob/master/all/all.json")

    await ctx.channel.send(embed = embed_content)

@client.command(name = "subscribe", pass_context = True, help = "Subscribes a channel to record announcements about a particular event in a particular area. This action must be performed by an admin. If the event or country is two words or longer, it must be surrounded by double quotes. Usage: ?subscribe <channel> <event> <area> <single/average>\nEG. ?subscribe #wca-notify \"3x3 Multi Blind\" world single")
async def subscribe(ctx, channel : discord.TextChannel, event, area, s_a):
    # Check if author is admin or owner
    if ctx.author.id == ctx.guild.owner.id or ctx.author.top_role.permissions.administrator:
        # User is authorised
        event = wca.Event.query_event(event)

        countries = json.load(open('countries.json', 'r'))
        continents = json.load(open('continents.json', 'r'))
        country = "world"

        # Get country
        for c in continents: # Duplicate code!!! Clean later
            if c['name'].lower() in area.lower():
                country = c['id']
                log_action("cid")
        for i in countries:
            if i['name'].lower() in area.lower() or area.lower() in i['name'].lower():
                country = i['id']
                log_action("name")
            elif i['id'].lower() in area.lower() or area.lower() in i['id'].lower():
                country = i['id']
                log_action("id")
        
        ranking = wca.Ranking(event, area = country, ranking_type = s_a)
        hook = wca.RankingHook(ranking, None)
        announcement_client.add_hook(channel, hook)

        embed_content = discord.Embed(title = "Success", description = f":white_check_mark: <#{str(channel.id)}> has been subscribed to changes is {event().name} {area} {s_a} changes.")
        await ctx.channel.send(embed = embed_content)

    else:
        # Show error
        embed_error = discord.Embed(title = "Error", description = ":warning: You do not have permission to perform this action. This action must be performed by an admin or the owner of the server.")
        await ctx.channel.send(embed = embed_error)

client.run(open('.env', 'r').read())