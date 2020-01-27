token = ''

import discord
from discord.ext.commands import Bot
import wca, urllib

client = Bot(command_prefix = '?')

@client.event
async def on_ready():
    print(f"{client.user.name} is now online")


@client.command(name = "person", pass_context = True, help = "Get basic information about someone. Usage: ?person <name/wca ID>")
async def person(ctx, *args):
    query_string = ' '.join(args)

    embed_loading = discord.Embed(description = "Loading...")
    message = await ctx.channel.send(embed = embed_loading)

    user_data = None
    user_query_success = True

    if wca.Utils.is_wca_id(query_string):
        try:
            user_data = wca.User.from_page(f"https://www.worldcubeassociation.org/persons/{query_string.upper()}")
        except IndexError:
            user_query_success = False
    
    if not wca.Utils.is_wca_id(query_string) or not user_query_success:
        try:
            search = wca.Search(query_string)
            user_data = wca.User.from_page(f"https://www.worldcubeassociation.org/persons/{search.user_result[0].wca_id}")
            user_query_success = True
        except:
            user_query_success = False

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

client.run(open('.env', 'r').read())