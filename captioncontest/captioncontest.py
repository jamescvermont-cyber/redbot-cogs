import asyncio
import random
from urllib.parse import quote

import aiohttp
import discord
from redbot.core import commands
from redbot.core.bot import Red


# Appended to every scenario prompt to enforce the visual style
STYLE = (
    "New Yorker magazine cartoon, black and white ink line art, "
    "single panel, simple clean lines, crosshatching shading, "
    "white background, no text, no speech bubbles, no caption text, no words"
)

NUMBER_EMOJIS = ["1️⃣", "2️⃣", "3️⃣", "4️⃣", "5️⃣", "6️⃣", "7️⃣", "8️⃣", "9️⃣", "🔟"]
MAX_CAPTIONS = 10
MAX_CAPTION_LEN = 200

# ---------------------------------------------------------------------------
# Scenarios
# Each is (scene_description, type) where type is:
#   "speaker" — a character is clearly positioned to say something
#   "scene"   — the situation itself is the joke setup, caption goes below
# ---------------------------------------------------------------------------
SCENARIOS = [
    # ── Speaker scenarios ──────────────────────────────────────────────────
    ("a shark in a business suit presenting quarterly earnings charts to visibly terrified coworkers at a conference table", "speaker"),
    ("the Grim Reaper lying on a therapist's couch, the therapist nearby holding a clipboard and taking notes", "speaker"),
    ("a medieval knight furiously jabbing at a grocery store self-checkout machine while items pile up on the belt", "speaker"),
    ("two skeletons seated at a bar, one gesturing dramatically mid-explanation", "speaker"),
    ("a caveman delivering a TED talk to other seated cavemen in a cave, pointing at a crude stick figure drawing on the wall", "speaker"),
    ("God seated behind a complaints desk, an extremely long winding line of people stretching out through heaven's gate", "speaker"),
    ("a ghost nervously seated across from a hiring manager in a corporate job interview, interviewer looking skeptical", "speaker"),
    ("an elderly wizard jabbing his wand furiously at a broken laptop that refuses to work, useless sparks flying", "speaker"),
    ("an alien at a grocery store checkout with completely incomprehensible alien items on the conveyor belt, cashier bewildered", "speaker"),
    ("a robot and a human seated on opposite ends of a couch at couples therapy, therapist between them", "speaker"),
    ("a penguin in a tiny business suit pitching to three bored venture capitalists seated at a long table", "speaker"),
    ("a Viking warrior at a yoga class, deeply confused, attempting downward dog with terrible form", "speaker"),
    ("a pirate with an eyepatch at an eye doctor's office trying to read the letter chart, doctor looking puzzled", "speaker"),
    ("a full-size dinosaur standing at a tiny door labeled 'Evolution Department', clearly too large to enter", "speaker"),
    ("a mermaid at a DMV counter filling out paperwork, fin dangling awkwardly off the stool", "speaker"),
    ("a vampire staring at a blood bank ATM screen reading 'TRANSACTION DECLINED', fist raised", "speaker"),
    ("a bewildered time traveler in Victorian clothes arguing with a hotel receptionist holding the wrong century's ledger", "speaker"),
    ("an intense philosopher and a barista locked in a heated debate over a very simple coffee order", "speaker"),
    ("Santa Claus seated across from a very stern IRS auditor surrounded by enormous ledgers of gift deliveries", "speaker"),
    ("the devil at a desk reviewing a towering stack of employee satisfaction surveys with growing disappointment", "speaker"),
    ("an angel at an HR department filing a formal complaint, enormous stack of papers on the desk between them", "speaker"),
    ("Bigfoot at a passport control booth, officer squinting skeptically at the passport photo", "speaker"),
    ("a mummy tangled in its own unraveling bandages trying to fill out health insurance paperwork", "speaker"),
    ("a fortune teller at a career counseling session, crystal ball on the desk, career counselor taking notes", "speaker"),
    ("a large bear in a suit delivering annual performance reviews to a nervous smaller bear across a desk", "speaker"),
    ("a giant sea monster politely raising one enormous tentacle to be recognized in a small claims courtroom", "speaker"),
    ("a werewolf in a barber's chair, barber studying the result with profound uncertainty and a comb", "speaker"),
    ("a dog on a psychiatrist's couch earnestly explaining its complicated feelings about the mailman", "speaker"),
    ("a centaur visibly struggling to sit at a normal office desk and chair, coworkers pretending not to notice", "speaker"),
    ("a tiny devil on one person's shoulder arguing loudly with a tiny angel on the other shoulder, person between them looking completely exhausted", "speaker"),
    ("Frankenstein's monster on a first date at a fancy restaurant, date gripping menu nervously", "speaker"),
    ("a plague doctor at a modern hospital new employee orientation, clearly out of place among the others", "speaker"),
    ("a sphinx blocking a subway turnstile demanding a riddle from frustrated morning commuters behind her", "speaker"),
    ("two astronauts crammed in a very tiny elevator, one has brought an absurd amount of luggage", "speaker"),
    ("a talking parrot on a witness stand in court being cross-examined, one lawyer looking smug, the other horrified", "speaker"),
    ("a witch at a department of motor vehicles getting her broomstick registered, clerk filling out forms", "speaker"),
    ("two penguins at a couples counselor, one has brought a fish to the session as supporting evidence", "speaker"),
    ("a very small knight in full armor explaining something earnestly to a completely uninterested enormous bear", "speaker"),
    ("the sun and the moon in marriage counseling, earth sitting uncomfortably between them", "speaker"),
    ("a cat sitting across from a job interviewer, resume on the desk lists 'knocking things off shelves' under relevant experience", "speaker"),
    ("a life coach writing 'STEP 1: TRY' on a whiteboard to a single deeply unimpressed turtle seated in a folding chair", "speaker"),
    ("a dragon in a tiny office cubicle, fire suppression system going off above it, dragon looking guilty", "speaker"),
    # ── Scene scenarios ────────────────────────────────────────────────────
    ("a deserted island with two castaways on opposite sides: one side has a full mansion and swimming pool, the other a tiny stick hut, the mansion owner is crossing the beach holding a clipboard labeled 'HOA VIOLATION NOTICE'", "scene"),
    ("Noah's ark boarding two of every animal; at the gangplank a bouncer is checking a list while two confused humans argue they should qualify", "scene"),
    ("a small person trapped inside a snow globe, knocking on the glass while a gentle snowstorm swirls around them inside and bright sun shines in the normal world outside", "scene"),
    ("heaven's front gate with a large real-estate FOR SALE sign out front and a bright red SOLD sticker on it, smaller text reads 'sold as-is, no warranty'", "scene"),
    ("a dinosaur peering through a backyard telescope at a tiny incoming meteor, checking it off a to-do list on a clipboard", "scene"),
    ("a cheerful children's lemonade stand staffed entirely by wolves in business attire, one nervous human adult customer approaches with exact change", "scene"),
    ("two goldfish in a fishbowl, one fish has drawn elaborate multi-phase escape tunnel diagrams all over the glass in permanent marker", "scene"),
    ("a museum exhibit behind a velvet rope, placard reads 'Modern Man In Natural Habitat', displaying a man in a recliner holding a TV remote, surrounded by snacks", "scene"),
    ("a protest picket line outside the gates of heaven, signs read 'UNFAIR HOURS', 'CLOUDS NOT ERGONOMIC', 'HALO GIVES ME A HEADACHE'", "scene"),
    ("a vending machine in hell where every snack costs one dollar five cents; a demon holds only a dollar bill, staring at the machine", "scene"),
    ("a forked road in a dark forest; both paths have wooden signs pointing in opposite directions but both signs say 'REGRET'", "scene"),
    ("a corporate boardroom PowerPoint presentation on a large screen showing the Titanic hitting an iceberg, slide title reads 'Q3 RESULTS'", "scene"),
    ("two thunderclouds having a shouting argument, a lightning bolt crackling between them mid-debate, a smaller cloud off to the side rolling its eyes", "scene"),
    ("a fish looking up at a fisherman's lure dangling in the water, a second fish leaning over and whispering a warning", "scene"),
    ("raccoons in tiny tuxedos gathered formally around an overturned trash can set up as a fine dining table, complete with candelabra and cloth napkins", "scene"),
    ("a single ordinary door floating in the middle of empty outer space; an astronaut in a spacesuit approaches it, about to knock politely", "scene"),
    ("a framed obituary hung alone on a large bare wall, it reads in large elegant letters only: 'HE DID HIS BEST'", "scene"),
    ("a museum exhibit showing the classic evolution-of-man chart, but the final modern human at the end is hunched over a smartphone, with a small arrow curving back to the first hunched ape at the beginning", "scene"),
    ("a cemetery with identical neat gravestones in perfect rows; one headstone has a shiny gold 'PARTICIPATION AWARD' ribbon pinned to it", "scene"),
    ("a motivational poster on an office wall showing a man triumphantly falling off a cliff into fog; the caption area below the image is completely blank", "scene"),
    ("a waiting room in purgatory where everyone has clearly been sitting so long that they have started decorating, hanging pictures, and rearranging the furniture", "scene"),
    ("a very small embarrassed dragon standing under a prominent 'NO OPEN FLAMES' sign at the entrance to a public library", "scene"),
    ("a fully-stocked survival prepper's underground bunker that has been carefully set up for a dinner party; one confused normal dinner guest is descending the hatch ladder", "scene"),
    ("a man looking at his reflection in a bathroom mirror; the reflection is looking at its phone instead of looking back", "scene"),
    ("an 'EXIT' sign glowing above a door in a dark hallway; a smaller handwritten sign taped below it reads 'just kidding'", "scene"),
    ("a 'BEFORE and AFTER' advertisement poster; both panels are identical", "scene"),
    ("a doomsday clock on a wall showing one second to midnight, a sticky note on it reads 'REMINDER: change batteries'", "scene"),
    ("two mountains side by side; one has a dramatic flag planted on the summit, the other has a tiny 'CLOSED FOR MAINTENANCE' sign", "scene"),
]


class CaptionContest(commands.Cog):
    """Caption Contest — a cartoon is generated and players compete for the best caption."""

    SUBMIT_SECONDS = 180  # 3 minutes to submit
    VOTE_SECONDS = 90     # 90 seconds to vote

    def __init__(self, bot: Red):
        self.bot = bot
        self._games: dict[int, dict] = {}  # guild_id -> game state

    def cog_unload(self):
        for game in self._games.values():
            for key in ("submit_task", "vote_task"):
                t = game.get(key)
                if t:
                    t.cancel()

    # ------------------------------------------------------------------
    # Image generation
    # ------------------------------------------------------------------

    async def _fetch_image(self, scenario: str) -> str | None:
        full_prompt = f"{scenario}, {STYLE}"
        seed = random.randint(1, 999999)
        url = (
            "https://image.pollinations.ai/prompt/"
            + quote(full_prompt)
            + f"?width=1024&height=768&nologo=true&model=flux&seed={seed}"
        )
        try:
            async with aiohttp.ClientSession() as session:
                async with session.get(url, timeout=aiohttp.ClientTimeout(total=60)) as resp:
                    if resp.status == 200:
                        return url
        except Exception:
            pass
        return None

    # ------------------------------------------------------------------
    # Game flow
    # ------------------------------------------------------------------

    async def _submit_timeout(self, guild_id: int):
        await asyncio.sleep(self.SUBMIT_SECONDS)
        game = self._games.get(guild_id)
        if not game or game["phase"] != "submitting":
            return
        ch = self.bot.get_channel(game["channel_id"])
        if ch:
            await ch.send("Time's up! Moving to voting...")
        await self._begin_voting(guild_id)

    async def _vote_timeout(self, guild_id: int):
        await asyncio.sleep(self.VOTE_SECONDS)
        await self._finish_game(guild_id)

    async def _begin_voting(self, guild_id: int):
        game = self._games.get(guild_id)
        if not game:
            return
        ch = self.bot.get_channel(game["channel_id"])
        if not ch:
            self._games.pop(guild_id, None)
            return

        captions = game["captions"]
        if len(captions) < 2:
            await ch.send("Not enough captions submitted (need at least 2). Game cancelled.")
            self._games.pop(guild_id, None)
            return

        game["phase"] = "voting"
        caption_list = list(captions.items())  # [(user_id, text), ...] — order is stable
        game["caption_list"] = caption_list

        embed = discord.Embed(
            title="Vote for the best caption!",
            description=(
                f"React with a number. You can't vote for your own.\n"
                f"Voting closes in **{self.VOTE_SECONDS} seconds**."
            ),
            color=discord.Color.gold(),
        )
        embed.set_image(url=game["image_url"])

        lines = [f"{NUMBER_EMOJIS[i]}  {text}" for i, (_, text) in enumerate(caption_list)]
        embed.add_field(name="The Captions", value="\n".join(lines), inline=False)

        vote_msg = await ch.send(embed=embed)
        game["vote_message_id"] = vote_msg.id

        for i in range(len(caption_list)):
            await vote_msg.add_reaction(NUMBER_EMOJIS[i])

        game["vote_task"] = asyncio.create_task(self._vote_timeout(guild_id))

    async def _finish_game(self, guild_id: int):
        game = self._games.pop(guild_id, None)
        if not game:
            return
        ch = self.bot.get_channel(game["channel_id"])
        if not ch:
            return

        caption_list = game.get("caption_list", [])
        if not caption_list:
            await ch.send("No captions were submitted. Game over.")
            return

        # Tally votes from reactions, excluding bot reactions and self-votes
        vote_counts = {uid: 0 for uid, _ in caption_list}
        vote_msg_id = game.get("vote_message_id")
        if vote_msg_id:
            try:
                vote_msg = await ch.fetch_message(vote_msg_id)
                for reaction in vote_msg.reactions:
                    emoji_str = str(reaction.emoji)
                    if emoji_str not in NUMBER_EMOJIS:
                        continue
                    idx = NUMBER_EMOJIS.index(emoji_str)
                    if idx >= len(caption_list):
                        continue
                    author_id = caption_list[idx][0]
                    async for user in reaction.users():
                        if user.bot:
                            continue
                        if user.id == author_id:
                            continue  # no self-votes
                        vote_counts[author_id] += 1
            except Exception:
                pass

        sorted_results = sorted(caption_list, key=lambda x: vote_counts[x[0]], reverse=True)
        winner_uid = sorted_results[0][0]
        winner_votes = vote_counts[winner_uid]

        embed = discord.Embed(title="Caption Contest — Results!", color=discord.Color.green())
        embed.set_image(url=game["image_url"])

        lines = []
        for uid, text in sorted_results:
            member = ch.guild.get_member(uid)
            name = member.display_name if member else f"User {uid}"
            votes = vote_counts[uid]
            trophy = "🏆 " if (uid == winner_uid and winner_votes > 0) else ""
            lines.append(f"{trophy}**{name}** — {text}  *({votes} vote{'s' if votes != 1 else ''})*")

        embed.add_field(name="Results", value="\n".join(lines), inline=False)

        if winner_votes == 0:
            embed.set_footer(text="No votes cast — everyone's a winner (or loser).")
        else:
            member = ch.guild.get_member(winner_uid)
            name = member.display_name if member else f"User {winner_uid}"
            embed.set_footer(text=f"🏆 Winner: {name}")

        await ch.send(embed=embed)

    # ------------------------------------------------------------------
    # Commands
    # ------------------------------------------------------------------

    @commands.group(name="captioncontest", aliases=["cc"], invoke_without_command=True)
    @commands.guild_only()
    async def captioncontest(self, ctx: commands.Context):
        """Start a Caption Contest. A cartoon is generated; players compete for the best caption."""
        await ctx.invoke(self.cc_start)

    @captioncontest.command(name="start")
    async def cc_start(self, ctx: commands.Context):
        """Start a caption contest."""
        gid = ctx.guild.id
        if gid in self._games:
            await ctx.send("A caption contest is already running!")
            return

        self._games[gid] = {
            "channel_id": ctx.channel.id,
            "host_id": ctx.author.id,
            "image_url": None,
            "phase": "submitting",
            "captions": {},       # user_id -> caption text
            "caption_list": None, # set during voting: [(uid, text), ...]
            "vote_message_id": None,
            "submit_task": None,
            "vote_task": None,
        }

        wait_msg = await ctx.send("Generating cartoon, please wait...")
        scenario, stype = random.choice(SCENARIOS)
        url = await self._fetch_image(scenario)

        if not url:
            self._games.pop(gid, None)
            await wait_msg.edit(content="Image generation failed. Try again in a moment.")
            return

        self._games[gid]["image_url"] = url

        if stype == "speaker":
            hint = "Someone in this scene has something to say — what is it?"
        else:
            hint = "What's the caption for this scene?"

        embed = discord.Embed(
            title="Caption Contest!",
            description=(
                f"{hint}\n\n"
                f"Submit your caption: `$caption <your caption>`\n"
                f"You have **{self.SUBMIT_SECONDS // 60} minutes**. Captions are anonymous until the reveal."
            ),
            color=discord.Color.blurple(),
        )
        embed.set_image(url=url)

        await wait_msg.delete()
        await ctx.send(embed=embed)

        self._games[gid]["submit_task"] = asyncio.create_task(
            self._submit_timeout(gid)
        )

    @captioncontest.command(name="end")
    async def cc_end(self, ctx: commands.Context):
        """Force end the current caption contest (host or admin only)."""
        gid = ctx.guild.id
        game = self._games.get(gid)
        if not game:
            await ctx.send("No caption contest is running.")
            return
        if ctx.author.id != game["host_id"] and not ctx.author.guild_permissions.manage_guild:
            await ctx.send("Only the host or a server admin can end the game early.")
            return

        for key in ("submit_task", "vote_task"):
            t = game.get(key)
            if t:
                t.cancel()

        if game["phase"] == "submitting":
            await ctx.send("Ending submissions early, moving to voting...")
            await self._begin_voting(gid)
        elif game["phase"] == "voting":
            await ctx.send("Ending voting early...")
            await self._finish_game(gid)

    @captioncontest.command(name="status")
    async def cc_status(self, ctx: commands.Context):
        """Check how many captions have been submitted."""
        gid = ctx.guild.id
        game = self._games.get(gid)
        if not game:
            await ctx.send("No caption contest is running.")
            return
        if game["phase"] == "submitting":
            n = len(game["captions"])
            await ctx.send(f"{n} caption{'s' if n != 1 else ''} submitted so far.")
        else:
            await ctx.send("Voting is in progress.")

    @commands.command(name="caption")
    @commands.guild_only()
    async def submit_caption(self, ctx: commands.Context, *, caption: str):
        """Submit your caption for the current contest."""
        gid = ctx.guild.id
        game = self._games.get(gid)

        # Ignore silently if no game or wrong channel
        if not game or game["channel_id"] != ctx.channel.id:
            return

        if game["phase"] != "submitting":
            await ctx.message.add_reaction("❌")
            return

        if len(caption) > MAX_CAPTION_LEN:
            await ctx.send(
                f"{ctx.author.mention} Caption too long (max {MAX_CAPTION_LEN} chars).",
                delete_after=8,
            )
            return

        uid = ctx.author.id
        captions = game["captions"]

        if uid not in captions and len(captions) >= MAX_CAPTIONS:
            await ctx.send(
                f"{ctx.author.mention} Maximum captions reached ({MAX_CAPTIONS}).",
                delete_after=8,
            )
            return

        updating = uid in captions
        captions[uid] = caption

        # Try to delete the submission message to keep captions secret
        try:
            await ctx.message.delete()
        except (discord.Forbidden, discord.NotFound):
            pass

        if updating:
            await ctx.send(
                f"{ctx.author.mention} updated their caption. ({len(captions)} total)",
                delete_after=8,
            )
        else:
            await ctx.send(
                f"{ctx.author.mention} submitted a caption! ({len(captions)} total)",
                delete_after=8,
            )
