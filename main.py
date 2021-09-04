import discord
from discord.ext import commands
from discord.gateway import DiscordWebSocket
from discord_slash import SlashCommand
from discord_slash.utils.manage_commands import create_option
from discord.utils import get
import twitch
from twitch.helix.models import stream

twclid = "0lfpvagxu5lpn2mscy5qf8mh05p9jp"
twclsc = "8s3ztphf7fqeinwdsj6o1vlkh5gzle"
helix = twitch.Helix(twclid, twclsc)

token = "NzY5MTYzOTU1MTM3Njc1Mjc1.X5LBwQ.7KX_iIByxfwdFcyLH7_u_ptbpII"
bot = commands.Bot(command_prefix="이하야 ")
slash = SlashCommand(bot, sync_commands=True)
owner_avator = "https://cdn.discordapp.com/avatars/741973166364164099/e2194f9f6d88a00123005bcfe4110acd.png"

@bot.event
async def on_ready():
	print("ready")

@slash.slash(name="twitch",
		description="트위치 스트리머 정보 확인하기",
		options=[
			create_option(
				name="id",
				description="스트리머의 ID를 입력해주세요.",
				option_type=3,
				required=True
			)
		]
	)
async def twitch(ctx, id: str):
	user = helix.user(f'{id}')
	tid = user.id
	if f"{user.broadcaster_type}" == "partner":
		streamerType = "파트너 스트리머"
	elif f"{user.broadcaster_type}" == "affiliate":
		streamerType = "제휴 스트리머"
	else:
		streamerType = "일반 스트리머"
	#라이브 여부 : user.is_live
	embed = discord.Embed(color=0xfffff, title=f"{user.display_name}님의 정보", description=f"[채널 바로가기](https://www.twitch.tv/{id})")
	embed.add_field(name="스트리머 등급", value=f"{streamerType}", inline=False)
	embed.add_field(name="시청 수", value=f"{user.view_count}", inline=False)
	embed.add_field(name="소개", value=f"{user.description}", inline=False)
	embed.set_footer(text="봇 개발자: 이하님#9999", icon_url=owner_avator)
	embed.set_thumbnail(url=user.profile_image_url)
	await ctx.send(embed=embed)

bot.run(token)
