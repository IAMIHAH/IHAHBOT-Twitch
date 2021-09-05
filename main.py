# 뭐였더라
from zlib import decompress

# dpy
import discord
from discord.ext import commands
from discord.gateway import DiscordWebSocket

# 슬커 사용하기
from discord_slash import SlashCommand
from discord_slash.utils.manage_commands import create_option

# 디코 정보 가져오기
from discord.utils import get

# 트위치 정보 가져오기
import twitch
from twitch.helix.models import Stream

# 슬커에서 버튼사용하기
from discord_slash.utils import manage_components
from discord_slash.model import ButtonStyle

import time
import calendar

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

@slash.slash(name="help", description="도움말을 불러옵니다.")
async def help(ctx):
	embed = discord.Embed(color=0xffffff, title="이하봇 슬래시명령어 도움말")
	embed.add_field(name="/twitch [ID]", value="[ID] = 트위치 유저 ID\n[ID]란에 작성한 유저에 대한 정보를 불러옵니다.", inline=False)
	embed.add_field(name="/invite", value="이하봇 초대 링크를 가져옵니다.", inline=False)
	await ctx.send(embed=embed)

@slash.slash(name="invite", description="이하봇 초대 링크를 가져옵니다.")
async def invite(ctx):
	embed = discord.Embed(color=0xffffff, title=f"초대하기", description="[바로가기](https://discord.com/oauth2/authorize?client_id=769163955137675275&permissions=8&scope=bot%20applications.commands)")
	await ctx.send(embed=embed)

@slash.slash(name="twitch",
		description="트위치 유저 정보 확인하기",
		options=[
			create_option(
				name="id",
				description="트위치 유저의 ID를 입력해주세요.",
				option_type=3,
				required=True
			)
		]
	)
async def twitch(ctx, id: str):
	user = helix.user(f'{id}')

	tid = user.id
	badge = ""
	streamerType = ""
	badgeInfo = ""
	# 스트리머 등급에 따른 표시 변경 및 이모지
	if f"{user.type}" == "admin":
		streamerType = "트위치 어드민 <:admin:883691115398717450> / "
		badge = f"{badge}<:admin:883691115398717450> "
		badgeInfo = f"{badgeInfo}<:admin:883691115398717450> 트위치 어드민\n"
	elif f"{user.type}" == "staff":
		streamerType = "트위치 스태프 <:staff:883691115348381697> / "
		badge = f"{badge}<:staff:883691115348381697> "
		badgeInfo = f"{badgeInfo}<:staff:883691115348381697> 트위치 스태프\n"
	elif f"{user.type}" == "global_mod":
		streamerType = "글로벌 모더레이터 <:globalmod:883691115084124283> / "
		badge = f"{badge}<:globalmod:883691115084124283> "
		badgeInfo = f"{badgeInfo}<:globalmod:883691115084124283> 글로벌 모더레이터\n"
	if f"{user.broadcaster_type}" == "partner":
		streamerType = f"{streamerType}파트너 스트리머 <:twitchpartner:883651633039417375>"
		badge = f"{badge}:star: <:twitchpartner:883651633039417375> "
		badgeInfo = f"{badgeInfo}<:twitchpartner:883651633039417375> 파트너 스트리머\n:star: 제휴 스트리머\n"
	elif f"{user.broadcaster_type}" == "affiliate":
		streamerType = f"{streamerType}제휴 스트리머 :star:"
		badge = f"{badge}:star: "
		badgeInfo = f"{badgeInfo}:star: 제휴 스트리머\n"
	else:
		if user.view_count > 1:
			streamerType = f"{streamerType}일반 스트리머"
		else:
			streamerType = "트수"
	
	if badgeInfo == "":
		badgeInfo = "없음"

	twbots = ["bbangddeock", "ssakdook", "nightbot", "commanderroot"]
	if id.lower() in twbots:
		badge = f"{badge} <:bot:883734868951961621>"
		streamerType = f"{streamerType} / 봇 <:bot:883734868951961621>"
	
	# 라이브 여부에 따른 이모지 표시
	if user.is_live is True:
		gotoChannel = f"현재 방송을 진행중입니다. <:streaming:883649148677672970>"
	else:
		gotoChannel = f"현재 방송을 진행중이지 않습니다. <:offline:883649829589352478>"
	
	# 임베드
	embed = discord.Embed(color=0xfffff, title=f"{user.display_name} {badge}님의 정보", description=gotoChannel)
	embed.add_field(name="트위치 등급", value=f"{streamerType}", inline=False)
	if user.view_count > 1:
		embed.add_field(name="누적 시청 수(채널 조회수)", value=format(user.view_count, ","), inline=False)
	if user.is_live is True:
		embed.add_field(name="현재 시청자 수", value=f"<:viewer:883687516979486761> {user.stream.viewer_count}")
	if user.description != "":
		embed.add_field(name="사용자 소개", value=f"{user.description}", inline=False)
	else:
		embed.add_field(name="사용자 소개", value=f"그들에 관해 아는 게 많지 않지만, {user.display_name}님이 대단하다는 건 확실해요.", inline=False)
	embed.add_field(name="보유한 뱃지", value=f"{badgeInfo}", inline=False)
	embed.set_footer(text="봇 개발자: 이하님#9999", icon_url=owner_avator)
	embed.set_thumbnail(url=user.profile_image_url)
	button = manage_components.create_button(
		style=ButtonStyle.URL,
		label=" 트위치 채널 바로가기",
		#emoji="tv",
		url=f"https://www.twitch.tv/{id}"
	)
	action_row = manage_components.create_actionrow(button)
	if streamerType != "트수":
		await ctx.send(
			embed=embed,
			components=[action_row]
		)
	else:
		await ctx.send(embed=embed)

@slash.slash(name="calendar",
		description="달력 출력하기",
		options=[
			create_option(
				name="year",
				description="연도를 숫자 4자리로 입력해주세요. (ex: 2021)",
				option_type=3,
				required=False
			),
                        create_option(
				name="month",
				description="월을 숫자로 입력해주세요. (1~12)",
				option_type=3,
				required=False
			)
		]
	)
async def calendar(ctx, year: int = time.localtime(time.time()).tm_year, month: int = time.localtime(time.time()).tm_mon):
    embed = discord.Embed(color=0xfffff, title=f"{year}년 {month}월 달력", description=f"{calendar.prmonth(year, month)}```")
    embed.set_footer(text="봇 개발자: 이하님#9999", icon_url=owner_avator)
    await ctx.send(embed=embed)

@bot.event
async def on_slash_command_error(ctx, ex):
	if f"{ex}" == "'NoneType' object has no attribute 'id'":
		embed = discord.Embed(color=0xff5555, title=f"오류!", description="존재하지 않는 ID에요.")
	elif "400 Client Error: Bad Request for url: https://api.twitch.tv/" in f"{ex}":
		embed = discord.Embed(color=0xff5555, title=f"오류!", description="ID가 아닌데요?")
	else:
		embed = discord.Embed(color=0xff5555, title=f"오류!", description="오류가 발생했어요.")
		embed.add_field(name="출력", value=f"{ex}", inline=False)
	embed.set_footer(text="봇 개발자: 이하님#9999", icon_url=owner_avator)
	await ctx.send(embed=embed)

bot.run(token)
