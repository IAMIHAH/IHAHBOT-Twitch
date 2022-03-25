# dpy
import discord
from discord import player
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

# 캘린더 근데 버그
import time
import calendar

twclid = "Twitch Application ID"
twclsc = "Twitch Application Secret"
helix = twitch.Helix(twclid, twclsc)

token = "Your Token"
bot = commands.Bot(command_prefix=["이하야 ","ㅇ","d"])
slash = SlashCommand(bot, sync_commands=True)
owner_avator = "avatar"

@bot.event
async def on_ready():
	print("ready")

@bot.remove_command('help')

@slash.slash(name="help", description="도움말을 불러옵니다.")
@bot.command(aliases=["도와줘", "도움",">"])
async def help(ctx):
	embed = discord.Embed(color=0xffffff, title="이하봇 빗금 명령어 도움말")
	embed.add_field(name="/twitch [ID]", value="\'이하야 트위치 [ID]\' 또는 \'ㅇㅌ [ID]\' 또는 \'dx [ID]\'로도 가능\n[ID] = 트위치 유저 ID\n[ID]란에 작성한 유저에 대한 정보를 불러옵니다.", inline=False)
	embed.add_field(name="/invite", value="이하봇 초대 링크를 가져옵니다.", inline=False)
	await ctx.send(embed=embed)

@slash.slash(name="ping", description="이하봇 지연시간을 가져옵니다.")
@bot.command(aliases=["vld","v","ㅍ"])
async def ping(ctx):
	t1 = time.perf_counter()
	async with ctx.typing():
		t2 = time.perf_counter()
	msglatency = round((t2-t1)*1000)
	latancy = bot.latency
	embed = discord.Embed(color=0xabcdef, title=":ping_pong: 퐁!")
	embed.add_field(name = ':ping_pong: 기본 지연시간', value = f'{round(latancy*1000)}ms', inline=False)
	embed.add_field(name = ':trophy: 메시지 지연시간', value = f"{msglatency}ms", inline=False)
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
@bot.command(aliases=["ㅌ","트위치", "x", "t"])
async def twitch(ctx, id: str):
	user = helix.user(f'{id}')

	tid = user.id
	badge = ""
	streamerType = ""
	badgeInfo = ""
	button = manage_components.create_button(
		style=ButtonStyle.URL,
		label=" 트위치 채널 바로가기",
		url=f"https://www.twitch.tv/{id}"
	)

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
		badge = f"{badge}<:bot:883734868951961621> "
		badgeInfo = f"{badgeInfo}<:bot:883734868951961621> 봇"
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
		embed.add_field(name="현재 시청자 수", value=f"<:viewer:883687516979486761> {user.stream.viewer_count}", inline=False)
		embed.add_field(name="방송 제목", value=f"{user.stream.title}", inline=False)
	if user.description != "":
		embed.add_field(name="사용자 소개", value=f"{user.description}", inline=False)
	else:
		embed.add_field(name="사용자 소개", value=f"그들에 관해 아는 게 많지 않지만, {user.display_name}님이 대단하다는 건 확실해요.", inline=False)
	embed.add_field(name="보유한 뱃지", value=f"{badgeInfo}", inline=False)
	embed.set_footer(text="봇 개발자: 이하님#3559")
	embed.set_thumbnail(url=user.profile_image_url)
	action_row = manage_components.create_actionrow(button)
	if streamerType != "트수":
		await ctx.send(
			embed=embed,
			components=[action_row]
		)
	else:
		await ctx.send(embed=embed)

@bot.event
async def on_slash_command_error(ctx, ex):
	if f"{ex}" == "'NoneType' object has no attribute 'id'":
		embed = discord.Embed(color=0xff5555, title=f"오류!", description="존재하지 않는 ID예요.")
	elif "400 Client Error: Bad Request for url: https://api.twitch.tv/" in f"{ex}":
		embed = discord.Embed(color=0xff5555, title=f"오류!", description="ID가 아닌데요?")
	else:
		embed = discord.Embed(color=0xff5555, title=f"오류!", description="오류가 발생했어요.")
		embed.add_field(name="출력", value=f"{ex}", inline=False)
	embed.set_footer(text="봇 개발자: 이하님#3559")
	await ctx.send(embed=embed)

@bot.event
async def on_command_error(ctx, ex):
	if "'NoneType' object has no attribute 'id'" in f"{ex}":
		embed = discord.Embed(color=0xff5555, title=f"오류!", description="존재하지 않는 ID예요.")
	elif "400 Client Error: Bad Request for url: https://api.twitch.tv/" in f"{ex}":
		embed = discord.Embed(color=0xff5555, title=f"오류!", description="ID가 아닌데요?")
	else:
		embed = discord.Embed(color=0xff5555, title=f"오류!", description="오류가 발생했어요.")
		embed.add_field(name="출력", value=f"{ex}", inline=False)
	embed.set_footer(text="봇 개발자: 이하님#3559")
	await ctx.send(embed=embed)

bot.run(token)
