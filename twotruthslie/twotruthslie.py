import asyncio
import random

import discord
from discord import ui
from redbot.core import commands

JOIN_TIMEOUT = 60
VOTE_TIMEOUT = 30
MAX_EXTRA_INNINGS = 5


# ── Modal ─────────────────────────────────────────────────────────────────────

class StatementsModal(ui.Modal, title="Two Truths and a Lie"):
    truth1 = ui.TextInput(
        label="Truth #1",
        placeholder="A true statement about you...",
        max_length=200,
        style=discord.TextStyle.paragraph,
    )
    truth2 = ui.TextInput(
        label="Truth #2",
        placeholder="Another true statement about you...",
        max_length=200,
        style=discord.TextStyle.paragraph,
    )
    lie = ui.TextInput(
        label="The Lie",
        placeholder="The false statement (your lie)...",
        max_length=200,
        style=discord.TextStyle.paragraph,
    )

    def __init__(self, session: "TTLSession", player: discord.Member):
        super().__init__()
        self.session = session
        self.player = player

    async def on_submit(self, interaction: discord.Interaction):
        await self.session.on_statements_submitted(
            interaction,
            self.truth1.value,
            self.truth2.value,
            self.lie.value,
        )


# ── Views ─────────────────────────────────────────────────────────────────────

class EnterStatementsView(ui.View):
    def __init__(self, session: "TTLSession", current_player: discord.Member):
        super().__init__(timeout=120)
        self.session = session
        self.current_player = current_player
        self._used = False

    @ui.button(label="Enter My Statements", style=discord.ButtonStyle.primary, emoji="✏️")
    async def enter_btn(self, interaction: discord.Interaction, button: ui.Button):
        if interaction.user.id != self.current_player.id:
            await interaction.response.send_message(
                f"Only {self.current_player.display_name} can click this!", ephemeral=True
            )
            return
        if self._used:
            await interaction.response.send_message(
                "Statements already submitted!", ephemeral=True
            )
            return
        self._used = True
        modal = StatementsModal(self.session, self.current_player)
        await interaction.response.send_modal(modal)

    async def on_timeout(self):
        await self.session.skip_current_turn()


class VoteButton(ui.Button):
    def __init__(self, label: str, index: int, session: "TTLSession"):
        super().__init__(label=label, style=discord.ButtonStyle.secondary, row=0)
        self.vote_index = index
        self.session = session

    async def callback(self, interaction: discord.Interaction):
        await self.session.on_vote(interaction, self.vote_index)


class VoteView(ui.View):
    def __init__(self, session: "TTLSession"):
        super().__init__(timeout=VOTE_TIMEOUT)
        self.session = session
        for i in range(3):
            self.add_item(VoteButton(f"Statement {i + 1}", i, session))

    async def on_timeout(self):
        await self.session.finalize_vote()


class JoinView(ui.View):
    def __init__(self, session: "TTLSession"):
        super().__init__(timeout=JOIN_TIMEOUT)
        self.session = session

    @ui.button(label="Join Game", style=discord.ButtonStyle.success, emoji="✋")
    async def join_btn(self, interaction: discord.Interaction, button: ui.Button):
        await self.session.on_join(interaction)

    async def on_timeout(self):
        await self.session.on_join_timeout()


# ── Session ───────────────────────────────────────────────────────────────────

class TTLSession:
    def __init__(
        self,
        channel: discord.TextChannel,
        host: discord.Member,
        cog: "TwoTruthsLie",
    ):
        self.channel = channel
        self.host = host
        self.cog = cog
        self.players: list[discord.Member] = [host]
        self.scores: dict[int, int] = {host.id: 0}
        self.phase = "joining"
        self.turn_order: list[discord.Member] = []
        self.turn_index = 0
        self.extra_innings = 0
        # Per-turn state
        self.current_player: discord.Member | None = None
        self.shuffled_statements: list[str] = []
        self.lie_index: int = -1
        self.votes: dict[int, int] = {}
        self.eligible_voters: set[int] = set()
        self.vote_view: VoteView | None = None
        self.vote_message: discord.Message | None = None

    # ── Helpers ────────────────────────────────────────────────────────────────

    def _scores_str(self) -> str:
        parts = sorted(
            [(p, self.scores.get(p.id, 0)) for p in self.players],
            key=lambda x: x[1],
            reverse=True,
        )
        return "  |  ".join(f"{p.display_name}: {s}" for p, s in parts)

    def _scoreboard(self) -> str:
        medals = ["🥇", "🥈", "🥉"]
        sorted_players = sorted(
            [(p, self.scores.get(p.id, 0)) for p in self.players],
            key=lambda x: x[1],
            reverse=True,
        )
        return "\n".join(
            f"{medals[i] if i < 3 else f'{i+1}.'} **{p.display_name}** — "
            f"{s} pt{'s' if s != 1 else ''}"
            for i, (p, s) in enumerate(sorted_players)
        )

    # ── Join phase ─────────────────────────────────────────────────────────────

    async def on_join(self, interaction: discord.Interaction):
        member = interaction.user
        if self.phase != "joining":
            await interaction.response.send_message("Game has already started!", ephemeral=True)
            return
        if member.id in self.scores:
            await interaction.response.send_message("You're already in the game!", ephemeral=True)
            return
        self.players.append(member)
        self.scores[member.id] = 0
        names = ", ".join(p.display_name for p in self.players)
        await interaction.response.send_message(
            f"**{member.display_name}** joined! Players ({len(self.players)}): {names}"
        )

    async def on_join_timeout(self):
        if self.phase != "joining":
            return
        if len(self.players) < 2:
            await self.channel.send(
                "Not enough players joined (need at least 2). Game cancelled."
            )
            self.cog.sessions.pop(self.channel.id, None)
            self.phase = "done"
            return
        await self._begin_game()

    async def start_early(self):
        if self.phase != "joining":
            return
        if len(self.players) < 2:
            await self.channel.send("Need at least 2 players to start!")
            return
        await self._begin_game()

    async def _begin_game(self):
        self.phase = "playing"
        random.shuffle(self.players)
        self.turn_order = self.players * 2
        self.turn_index = 0

        names = " → ".join(p.display_name for p in self.players)
        embed = discord.Embed(
            title="Two Truths and a Lie — Starting!",
            description=(
                f"**Players ({len(self.players)}):** {names}\n"
                f"Each player takes **2 turns** total.\n\n"
                "Enter 2 true statements and 1 lie. "
                "Everyone else votes on which is the lie — correct guessers earn a point!"
            ),
            color=discord.Color.blurple(),
        )
        await self.channel.send(embed=embed)
        await self._next_turn()

    # ── Turn management ────────────────────────────────────────────────────────

    async def _next_turn(self):
        if self.phase == "done":
            return
        if self.turn_index >= len(self.turn_order):
            await self._check_end_of_game()
            return

        self.current_player = self.turn_order[self.turn_index]
        self.phase = "waiting_for_statements"
        self.shuffled_statements = []
        self.lie_index = -1
        self.votes = {}

        view = EnterStatementsView(self, self.current_player)

        if self.extra_innings > 0:
            title = "Extra Innings — Your Turn!"
            footer = f"Extra Inning {self.extra_innings}/{MAX_EXTRA_INNINGS}"
        else:
            round_num = (self.turn_index // len(self.players)) + 1
            turn_in_round = (self.turn_index % len(self.players)) + 1
            title = "Your Turn!"
            footer = f"Round {round_num}/2 — Player {turn_in_round}/{len(self.players)}"

        embed = discord.Embed(
            title=title,
            description=(
                f"**{self.current_player.mention}**, click the button below "
                "to enter your 2 truths and 1 lie.\n\n"
                f"*({footer})*"
            ),
            color=discord.Color.blurple(),
        )
        await self.channel.send(embed=embed, view=view)

    async def on_statements_submitted(
        self,
        interaction: discord.Interaction,
        truth1: str,
        truth2: str,
        lie: str,
    ):
        if self.phase != "waiting_for_statements":
            await interaction.response.send_message("Too late!", ephemeral=True)
            return

        # Shuffle the three statements, tracking where the lie lands
        stmts = [truth1, truth2, lie]
        indices = [0, 1, 2]
        random.shuffle(indices)
        self.shuffled_statements = [stmts[i] for i in indices]
        self.lie_index = indices.index(2)  # position of lie (original index 2) after shuffle

        self.phase = "voting"
        self.eligible_voters = {p.id for p in self.players if p.id != self.current_player.id}
        self.votes = {}

        await interaction.response.send_message(
            "Your statements have been submitted! Voting begins now.", ephemeral=True
        )

        lines = [f"**{i+1}.** {stmt}" for i, stmt in enumerate(self.shuffled_statements)]
        embed = discord.Embed(
            title=f"Which is the lie? — {self.current_player.display_name}",
            description="\n\n".join(lines),
            color=discord.Color.blurple(),
        )
        embed.set_footer(text=f"Vote below! {VOTE_TIMEOUT} seconds remaining.")

        self.vote_view = VoteView(self)
        self.vote_message = await self.channel.send(embed=embed, view=self.vote_view)

    async def skip_current_turn(self):
        if self.phase != "waiting_for_statements":
            return
        await self.channel.send(
            f"⏰ {self.current_player.display_name} took too long — skipping their turn."
        )
        self.turn_index += 1
        await self._next_turn()

    # ── Voting ─────────────────────────────────────────────────────────────────

    async def on_vote(self, interaction: discord.Interaction, vote_index: int):
        if self.phase != "voting":
            await interaction.response.send_message("Voting is already over!", ephemeral=True)
            return
        voter = interaction.user
        if voter.id == self.current_player.id:
            await interaction.response.send_message(
                "You can't vote on your own statements!", ephemeral=True
            )
            return
        if voter.id not in self.eligible_voters:
            await interaction.response.send_message(
                "You're not in this game!", ephemeral=True
            )
            return
        if voter.id in self.votes:
            await interaction.response.send_message(
                "You've already voted!", ephemeral=True
            )
            return

        self.votes[voter.id] = vote_index
        preview = self.shuffled_statements[vote_index][:60]
        await interaction.response.send_message(
            f"You voted for Statement {vote_index + 1}: *\"{preview}\"*", ephemeral=True
        )

        if len(self.votes) >= len(self.eligible_voters):
            if self.vote_view:
                self.vote_view.stop()
            await self.finalize_vote()

    async def finalize_vote(self):
        if self.phase != "voting":
            return
        self.phase = "revealing"

        if self.vote_view and self.vote_message:
            for item in self.vote_view.children:
                item.disabled = True
            try:
                await self.vote_message.edit(view=self.vote_view)
            except discord.HTTPException:
                pass

        # Award points to correct voters
        correct_voters = [
            p for p in self.players
            if p.id != self.current_player.id
            and self.votes.get(p.id) == self.lie_index
        ]
        for p in correct_voters:
            self.scores[p.id] = self.scores.get(p.id, 0) + 1

        lie_text = self.shuffled_statements[self.lie_index]
        result_lines = []
        for p in self.players:
            if p.id == self.current_player.id:
                continue
            voted = self.votes.get(p.id)
            if voted is None:
                result = "*(didn't vote)*"
            elif voted == self.lie_index:
                result = f"✅ Statement {voted + 1} — **correct!** (+1 pt)"
            else:
                result = f"❌ Statement {voted + 1} — wrong"
            result_lines.append(f"**{p.display_name}:** {result}")

        embed = discord.Embed(
            title=f"The lie was Statement {self.lie_index + 1}!",
            description=(
                f"**\"{lie_text}\"** was the lie!\n\n"
                + "\n".join(result_lines)
            ),
            color=discord.Color.blurple(),
        )
        embed.add_field(name="Scores", value=self._scores_str(), inline=False)
        await self.channel.send(embed=embed)

        self.turn_index += 1
        await asyncio.sleep(3)
        await self._next_turn()

    # ── End of game ────────────────────────────────────────────────────────────

    async def _check_end_of_game(self):
        max_score = max(self.scores.values(), default=0)
        leaders = [p for p in self.players if self.scores.get(p.id, 0) == max_score]

        if len(leaders) == 1:
            self.phase = "done"
            self.cog.sessions.pop(self.channel.id, None)
            await self._announce_winner(leaders[0])
            return

        if self.extra_innings >= MAX_EXTRA_INNINGS:
            self.phase = "done"
            self.cog.sessions.pop(self.channel.id, None)
            await self._announce_tie(leaders)
            return

        self.extra_innings += 1
        names = ", ".join(p.display_name for p in leaders)
        embed = discord.Embed(
            title=f"Extra Innings #{self.extra_innings}!",
            description=(
                f"**Tied at {max_score} pt{'s' if max_score != 1 else ''}:** {names}\n"
                f"Each tied player gets one more round! "
                f"*(Extra inning {self.extra_innings}/{MAX_EXTRA_INNINGS})*"
            ),
            color=discord.Color.blurple(),
        )
        await self.channel.send(embed=embed)

        random.shuffle(leaders)
        self.turn_order = leaders[:]
        self.turn_index = 0
        self.phase = "playing"
        await self._next_turn()

    async def _announce_winner(self, winner: discord.Member):
        embed = discord.Embed(
            title="We have a winner!",
            description=f"**{winner.display_name}** wins Two Truths and a Lie!",
            color=discord.Color.gold(),
        )
        embed.add_field(name="Final Scores", value=self._scoreboard(), inline=False)
        await self.channel.send(embed=embed)

    async def _announce_tie(self, tied_players: list[discord.Member]):
        max_score = self.scores.get(tied_players[0].id, 0)
        names = " and ".join(p.display_name for p in tied_players)
        embed = discord.Embed(
            title="It's a tie!",
            description=(
                f"After {MAX_EXTRA_INNINGS} extra innings, **{names}** are still tied "
                f"at **{max_score} pt{'s' if max_score != 1 else ''}**!\n"
                "It's a draw — well played everyone!"
            ),
            color=discord.Color.gold(),
        )
        embed.add_field(name="Final Scores", value=self._scoreboard(), inline=False)
        await self.channel.send(embed=embed)


# ── Cog ───────────────────────────────────────────────────────────────────────

class TwoTruthsLie(commands.Cog):
    """Two Truths and a Lie — submit 2 truths and 1 lie, everyone else votes!"""

    def __init__(self, bot):
        self.bot = bot
        self.sessions: dict[int, TTLSession] = {}

    def cog_unload(self):
        self.sessions.clear()

    @commands.group(name="ttl", invoke_without_command=True, aliases=["twotruthslie"])
    async def ttl(self, ctx: commands.Context):
        """Start a Two Truths and a Lie game!"""
        if ctx.channel.id in self.sessions:
            await ctx.send("A game is already running in this channel!")
            return

        session = TTLSession(ctx.channel, ctx.author, self)
        self.sessions[ctx.channel.id] = session

        embed = discord.Embed(
            title="Two Truths and a Lie",
            description=(
                f"**{ctx.author.display_name}** started a game!\n\n"
                "Click **Join Game** to participate. You need at least **2 players**.\n"
                f"Game starts automatically in **{JOIN_TIMEOUT} seconds**, "
                "or use `$ttl start` to begin early."
            ),
            color=discord.Color.blurple(),
        )
        await ctx.send(embed=embed, view=JoinView(session))

    @ttl.command(name="start")
    async def ttl_start(self, ctx: commands.Context):
        """Start the game early (during join phase)."""
        session = self.sessions.get(ctx.channel.id)
        if session is None:
            await ctx.send("No game is waiting to start in this channel.")
            return
        if session.phase != "joining":
            await ctx.send("The game has already started!")
            return
        await session.start_early()

    @ttl.command(name="end")
    async def ttl_end(self, ctx: commands.Context):
        """End the current game."""
        session = self.sessions.pop(ctx.channel.id, None)
        if session is None:
            await ctx.send("No game is running in this channel.")
            return
        session.phase = "done"
        await ctx.send("Game ended.")
