import asyncio
import time
from datetime import datetime, timezone
from pathlib import Path
from typing import Optional

import aiosqlite
import discord
from discord.ui import Button, View
from redbot.core import commands
from redbot.core.data_manager import cog_data_path

from .items import ITEMS

# ── Constants ─────────────────────────────────────────────────────────────────

DEFAULT_COUNT = 20
RECENT_WINDOW = 86400  # 24 hours in seconds
# If total matched items across all categories exceeds this, dump as plain text
EMBED_LIST_THRESHOLD = 12

CHOICE_GROUPS = {
    "hate": "negative",
    "dont_like": "negative",
    "neutral": "neutral",
    "like": "positive",
    "love": "positive",
}

CHOICE_LABELS = {
    "hate": "Hate It",
    "dont_like": "Don't Like It",
    "neutral": "Neutral",
    "like": "Like It",
    "love": "Love It ❤️",
}

# Label shown in parentheses when both players chose the exact same option
EXACT_LABELS = {
    "hate": "hate",
    "dont_like": "dislike",
    "neutral": "neutral",
    "like": "like",
    "love": "love",
}


# ── Views ─────────────────────────────────────────────────────────────────────

class ItemView(View):
    """Five-button view shown for each question."""

    def __init__(self, cog: "InCommon", channel_id: int):
        super().__init__(timeout=300)
        self.cog = cog
        self.channel_id = channel_id

    async def handle_choice(self, interaction: discord.Interaction, choice: str):
        game = self.cog.active_games.get(self.channel_id)
        if not game:
            await interaction.response.send_message("No active game in this channel.", ephemeral=True)
            return

        player1: discord.Member = game["player1"]
        player2: discord.Member = game["player2"]

        if interaction.user.id not in (player1.id, player2.id):
            await interaction.response.send_message("You're not part of this game!", ephemeral=True)
            return

        responses = game["current_responses"]

        if interaction.user.id in responses:
            already = CHOICE_LABELS[responses[interaction.user.id]]
            await interaction.response.send_message(
                f"You already locked in **{already}** for this one!", ephemeral=True
            )
            return

        responses[interaction.user.id] = choice

        # Private confirmation
        await interaction.response.send_message(
            f"Locked in: **{CHOICE_LABELS[choice]}** ✓  *(only you can see this)*",
            ephemeral=True,
        )

        # Update shared embed to show who has responded (without revealing choice)
        index = game["current_index"]
        item = game["items"][index]
        total = len(game["items"])
        p1_status = "✅" if player1.id in responses else "⏳"
        p2_status = "✅" if player2.id in responses else "⏳"

        embed = discord.Embed(
            title=item["text"],
            description=(
                f"**Question {index + 1} of {total}**\n\n"
                f"{p1_status} {player1.display_name}\n"
                f"{p2_status} {player2.display_name}"
            ),
            color=discord.Color.og_blurple(),
        )
        embed.set_footer(text="Choices are private until the end.")

        try:
            await game["current_message"].edit(embed=embed)
        except Exception:
            pass

        if len(responses) == 2:
            await asyncio.sleep(0.4)
            await self.cog.advance_game(self.channel_id)

    @discord.ui.button(label="😡 Hate It", style=discord.ButtonStyle.danger, row=0)
    async def hate_it(self, interaction: discord.Interaction, button: Button):
        await self.handle_choice(interaction, "hate")

    @discord.ui.button(label="👎 Don't Like It", style=discord.ButtonStyle.secondary, row=0)
    async def dont_like_it(self, interaction: discord.Interaction, button: Button):
        await self.handle_choice(interaction, "dont_like")

    @discord.ui.button(label="😐 Neutral", style=discord.ButtonStyle.primary, row=0)
    async def neutral_btn(self, interaction: discord.Interaction, button: Button):
        await self.handle_choice(interaction, "neutral")

    @discord.ui.button(label="👍 Like It", style=discord.ButtonStyle.success, row=0)
    async def like_it(self, interaction: discord.Interaction, button: Button):
        await self.handle_choice(interaction, "like")

    @discord.ui.button(label="❤️ Love It", style=discord.ButtonStyle.success, row=0)
    async def love_it(self, interaction: discord.Interaction, button: Button):
        await self.handle_choice(interaction, "love")

    async def on_timeout(self):
        game = self.cog.active_games.pop(self.channel_id, None)
        if game:
            channel: discord.TextChannel = game["channel"]
            try:
                p1 = game["player1"]
                p2 = game["player2"]
                await channel.send(
                    f"⏰ Game timed out — {p1.mention} {p2.mention}\n"
                    f"*One of you went quiet. Start again with `$incommon`.*"
                )
            except Exception:
                pass


class ChallengeView(View):
    """Accept / Decline view sent to the challenged player."""

    def __init__(
        self,
        cog: "InCommon",
        challenger: discord.Member,
        challenged: discord.Member,
        count: int,
    ):
        super().__init__(timeout=120)
        self.cog = cog
        self.challenger = challenger
        self.challenged = challenged
        self.count = count

    @discord.ui.button(label="✅ Accept", style=discord.ButtonStyle.success)
    async def accept(self, interaction: discord.Interaction, button: Button):
        if interaction.user.id != self.challenged.id:
            await interaction.response.send_message(
                "This challenge isn't for you!", ephemeral=True
            )
            return

        if interaction.channel.id in self.cog.active_games:
            await interaction.response.send_message(
                "A game just started in this channel — try again after it finishes.",
                ephemeral=True,
            )
            self.stop()
            return

        self.stop()
        await interaction.response.edit_message(
            content=(
                f"✅ **{self.challenged.display_name}** accepted!\n"
                f"Starting **{self.count}-question** In Common game…"
            ),
            embed=None,
            view=None,
        )
        await self.cog.start_game(
            interaction.channel, self.challenger, self.challenged, self.count
        )

    @discord.ui.button(label="❌ Decline", style=discord.ButtonStyle.danger)
    async def decline(self, interaction: discord.Interaction, button: Button):
        if interaction.user.id not in (self.challenged.id, self.challenger.id):
            await interaction.response.send_message(
                "Not your challenge to decline!", ephemeral=True
            )
            return
        self.stop()
        await interaction.response.edit_message(
            content=f"❌ Challenge declined.",
            embed=None,
            view=None,
        )

    async def on_timeout(self):
        pass  # message just stays, buttons become unclickable


# ── Cog ───────────────────────────────────────────────────────────────────────

class InCommon(commands.Cog):
    """OKCupid-style compatibility game. Find out what you have In Common!"""

    def __init__(self, bot):
        self.bot = bot
        self.active_games: dict = {}
        # guild_id -> {item_text: timestamp}  (24-hour dedup)
        self.recent_items: dict = {}
        self._db_ready = False
        bot.loop.create_task(self._init_db())

    @property
    def db_path(self) -> Path:
        p = cog_data_path(self) / "incommon.db"
        return p

    # ── DB setup ──────────────────────────────────────────────────────────────

    async def _init_db(self):
        await self.bot.wait_until_ready()
        self.db_path.parent.mkdir(parents=True, exist_ok=True)

        async with aiosqlite.connect(self.db_path) as db:
            await db.executescript("""
                CREATE TABLE IF NOT EXISTS items (
                    id       INTEGER PRIMARY KEY AUTOINCREMENT,
                    text     TEXT    NOT NULL UNIQUE,
                    category TEXT    NOT NULL
                );
                CREATE TABLE IF NOT EXISTS games (
                    id             INTEGER PRIMARY KEY AUTOINCREMENT,
                    guild_id       INTEGER NOT NULL,
                    player1_id     INTEGER NOT NULL,
                    player2_id     INTEGER NOT NULL,
                    played_at      TEXT    NOT NULL,
                    question_count INTEGER NOT NULL,
                    match_count    INTEGER NOT NULL
                );
                CREATE TABLE IF NOT EXISTS answers (
                    id             INTEGER PRIMARY KEY AUTOINCREMENT,
                    game_id        INTEGER NOT NULL,
                    item_text      TEXT    NOT NULL,
                    player1_choice TEXT    NOT NULL,
                    player2_choice TEXT    NOT NULL,
                    is_match       INTEGER NOT NULL,
                    FOREIGN KEY (game_id) REFERENCES games(id)
                );
            """)
            await db.commit()

            # Seed items if table is empty
            cur = await db.execute("SELECT COUNT(*) FROM items")
            count = (await cur.fetchone())[0]
            if count == 0:
                await db.executemany(
                    "INSERT OR IGNORE INTO items (text, category) VALUES (?, ?)",
                    [(it["text"], it["category"]) for it in ITEMS],
                )
                await db.commit()

        self._db_ready = True

    # ── gamestop integration ──────────────────────────────────────────────────

    async def force_stop_game(self, channel_id: int) -> Optional[str]:
        """Called by $end. Silently ends any active game. Returns cog name or None."""
        game = self.active_games.pop(channel_id, None)
        if not game:
            return None
        # Disable buttons on the current question message
        if game.get("current_message"):
            try:
                await game["current_message"].edit(view=None)
            except Exception:
                pass
        return "In Common"

    async def clear_recent_memory(self, guild: discord.Guild) -> Optional[str]:
        """Called by $clearmemory. Clears the 24-hour item dedup cache."""
        if guild.id in self.recent_items:
            self.recent_items[guild.id] = {}
            return "In Common"
        return None

    # ── Commands ──────────────────────────────────────────────────────────────

    @commands.command()
    @commands.guild_only()
    async def incommon(self, ctx, member: discord.Member, count: int = DEFAULT_COUNT):
        """Find out what you have In Common with someone!

        Usage: $incommon @someone [questions]
        Default 20 questions, max 100.
        """
        if not self._db_ready:
            await ctx.send("Still warming up — try again in a moment!")
            return
        if member.id == ctx.author.id:
            await ctx.send("You can't challenge yourself!")
            return
        if member.bot:
            await ctx.send("Bots don't have feelings. Challenge a human.")
            return
        if ctx.channel.id in self.active_games:
            await ctx.send("There's already a game running here. Wait for it to finish.")
            return

        count = max(5, min(count, 100))

        embed = discord.Embed(
            title="💕 In Common Challenge",
            description=(
                f"{ctx.author.mention} wants to see what they have **In Common** "
                f"with {member.mention}!\n\n"
                f"**{count} questions** — how compatible are you?\n\n"
                f"{member.mention}, do you accept?"
            ),
            color=discord.Color.blurple(),
        )
        view = ChallengeView(self, ctx.author, member, count)
        await ctx.send(f"{member.mention}", embed=embed, view=view)

    @commands.command()
    @commands.guild_only()
    async def incommonstats(self, ctx, member: discord.Member):
        """Check your all-time In Common history with someone."""
        if not self._db_ready:
            await ctx.send("Still warming up!")
            return

        p1_id = min(ctx.author.id, member.id)
        p2_id = max(ctx.author.id, member.id)

        async with aiosqlite.connect(self.db_path) as db:
            cur = await db.execute(
                "SELECT question_count, match_count, played_at FROM games "
                "WHERE player1_id = ? AND player2_id = ? ORDER BY played_at DESC",
                (p1_id, p2_id),
            )
            rows = await cur.fetchall()

        if not rows:
            await ctx.send(
                f"No games on record between {ctx.author.mention} and {member.mention}."
            )
            return

        all_q = sum(r[0] for r in rows)
        all_m = sum(r[1] for r in rows)
        all_pct = round((all_m / all_q) * 100) if all_q else 0

        embed = discord.Embed(
            title=f"{all_pct}% In Common — All Time",
            description=f"**{ctx.author.display_name}** & **{member.display_name}**",
            color=discord.Color.blurple(),
        )
        embed.add_field(name="Games Played", value=str(len(rows)), inline=True)
        embed.add_field(name="Total Questions", value=str(all_q), inline=True)
        embed.add_field(name="Total Matches", value=str(all_m), inline=True)

        recent = []
        for q, m, ts in rows[:5]:
            pct = round((m / q) * 100) if q else 0
            date = ts[:10]
            recent.append(f"{date}: **{pct}%** ({m}/{q})")
        embed.add_field(name="Recent Games", value="\n".join(recent), inline=False)

        await ctx.send(embed=embed)

    # ── Game logic ────────────────────────────────────────────────────────────

    async def start_game(
        self,
        channel: discord.TextChannel,
        player1: discord.Member,
        player2: discord.Member,
        count: int,
    ):
        guild_id = channel.guild.id
        now = time.time()

        # Prune expired entries from recent cache
        guild_recent = self.recent_items.get(guild_id, {})
        guild_recent = {
            text: ts for text, ts in guild_recent.items() if now - ts < RECENT_WINDOW
        }
        self.recent_items[guild_id] = guild_recent
        exclude = list(guild_recent.keys())

        async with aiosqlite.connect(self.db_path) as db:
            if exclude:
                placeholders = ",".join("?" * len(exclude))
                cur = await db.execute(
                    f"SELECT text, category FROM items "
                    f"WHERE text NOT IN ({placeholders}) ORDER BY RANDOM() LIMIT ?",
                    (*exclude, count),
                )
            else:
                cur = await db.execute(
                    "SELECT text, category FROM items ORDER BY RANDOM() LIMIT ?",
                    (count,),
                )
            rows = await cur.fetchall()

        # If we couldn't get enough fresh items, top up with anything
        if len(rows) < count:
            async with aiosqlite.connect(self.db_path) as db:
                got = {r[0] for r in rows}
                need = count - len(rows)
                extras_exclude = list(got)
                if extras_exclude:
                    ph = ",".join("?" * len(extras_exclude))
                    cur = await db.execute(
                        f"SELECT text, category FROM items "
                        f"WHERE text NOT IN ({ph}) ORDER BY RANDOM() LIMIT ?",
                        (*extras_exclude, need),
                    )
                else:
                    cur = await db.execute(
                        "SELECT text, category FROM items ORDER BY RANDOM() LIMIT ?",
                        (need,),
                    )
                extra_rows = await cur.fetchall()
            rows = list(rows) + list(extra_rows)

        items = [{"text": r[0], "category": r[1]} for r in rows]

        # Mark all as recently shown
        for item in items:
            self.recent_items[guild_id][item["text"]] = now

        self.active_games[channel.id] = {
            "player1": player1,
            "player2": player2,
            "items": items,
            "current_index": 0,
            "current_responses": {},
            "results": [],
            "channel": channel,
            "current_message": None,
        }

        await self.show_item(channel.id)

    async def show_item(self, channel_id: int):
        game = self.active_games.get(channel_id)
        if not game:
            return

        channel = game["channel"]
        index = game["current_index"]
        item = game["items"][index]
        total = len(game["items"])
        p1: discord.Member = game["player1"]
        p2: discord.Member = game["player2"]

        embed = discord.Embed(
            title=item["text"],
            description=(
                f"**Question {index + 1} of {total}**\n\n"
                f"⏳ {p1.display_name}\n"
                f"⏳ {p2.display_name}"
            ),
            color=discord.Color.og_blurple(),
        )
        embed.set_footer(text="Choices are private until the end.")

        view = ItemView(self, channel_id)
        msg = await channel.send(embed=embed, view=view)
        game["current_message"] = msg

    async def advance_game(self, channel_id: int):
        game = self.active_games.get(channel_id)
        if not game:
            return

        index = game["current_index"]
        item = game["items"][index]
        responses = game["current_responses"]
        p1: discord.Member = game["player1"]
        p2: discord.Member = game["player2"]

        p1_choice = responses[p1.id]
        p2_choice = responses[p2.id]
        is_match = CHOICE_GROUPS[p1_choice] == CHOICE_GROUPS[p2_choice]

        game["results"].append({
            "item": item["text"],
            "category": item["category"],
            "p1_choice": p1_choice,
            "p2_choice": p2_choice,
            "is_match": is_match,
        })

        # Disable buttons on finished question
        if game["current_message"]:
            try:
                await game["current_message"].edit(view=None)
            except Exception:
                pass

        game["current_index"] += 1
        game["current_responses"] = {}

        if game["current_index"] >= len(game["items"]):
            await self.finish_game(channel_id)
        else:
            await self.show_item(channel_id)

    async def finish_game(self, channel_id: int):
        game = self.active_games.pop(channel_id, None)
        if not game:
            return

        p1: discord.Member = game["player1"]
        p2: discord.Member = game["player2"]
        results = game["results"]
        channel: discord.TextChannel = game["channel"]

        total = len(results)
        matches = sum(1 for r in results if r["is_match"])
        pct = round((matches / total) * 100) if total else 0

        # Normalize IDs for consistent DB storage (smaller ID = player1 in DB)
        if p1.id < p2.id:
            p1_id, p2_id = p1.id, p2.id
            p1_key, p2_key = "p1_choice", "p2_choice"
        else:
            p1_id, p2_id = p2.id, p1.id
            p1_key, p2_key = "p2_choice", "p1_choice"

        async with aiosqlite.connect(self.db_path) as db:
            cur = await db.execute(
                "INSERT INTO games "
                "(guild_id, player1_id, player2_id, played_at, question_count, match_count) "
                "VALUES (?, ?, ?, ?, ?, ?)",
                (
                    channel.guild.id,
                    p1_id,
                    p2_id,
                    datetime.now(timezone.utc).isoformat(),
                    total,
                    matches,
                ),
            )
            game_id = cur.lastrowid

            for r in results:
                await db.execute(
                    "INSERT INTO answers "
                    "(game_id, item_text, player1_choice, player2_choice, is_match) "
                    "VALUES (?, ?, ?, ?, ?)",
                    (
                        game_id,
                        r["item"],
                        r[p1_key],
                        r[p2_key],
                        1 if r["is_match"] else 0,
                    ),
                )
            await db.commit()

            # All-time totals
            cur = await db.execute(
                "SELECT SUM(question_count), SUM(match_count), COUNT(*) FROM games "
                "WHERE player1_id = ? AND player2_id = ?",
                (p1_id, p2_id),
            )
            row = await cur.fetchone()

        at_total = row[0] or 0
        at_matches = row[1] or 0
        games_played = row[2] or 0
        at_pct = round((at_matches / at_total) * 100) if at_total else 0

        # Separate matched results by group
        # Note: for matched items, both players are in the same group, so p1_choice group == p2_choice group
        negatives = [r for r in results if r["is_match"] and CHOICE_GROUPS[r["p1_choice"]] == "negative"]
        neutrals  = [r for r in results if r["is_match"] and CHOICE_GROUPS[r["p1_choice"]] == "neutral"]
        positives = [r for r in results if r["is_match"] and CHOICE_GROUPS[r["p1_choice"]] == "positive"]

        total_matched_items = len(negatives) + len(neutrals) + len(positives)
        use_plain_text = total_matched_items > EMBED_LIST_THRESHOLD

        # Score color
        if pct >= 70:
            color = discord.Color.green()
        elif pct >= 40:
            color = discord.Color.gold()
        else:
            color = discord.Color.red()

        # ── Main results embed ────────────────────────────────────────────────
        embed = discord.Embed(
            title=f"{pct}% In Common",
            color=color,
        )
        embed.description = (
            f"**{p1.display_name}** & **{p2.display_name}** "
            f"matched on **{matches}/{total}** things this round."
        )
        embed.add_field(
            name="📊 All Time",
            value=(
                f"**{at_pct}%** across {games_played} game{'s' if games_played != 1 else ''}\n"
                f"{at_matches}/{at_total} matched overall"
            ),
            inline=False,
        )

        if not use_plain_text:
            # Fit everything inside the embed
            if negatives:
                embed.add_field(
                    name="👎 Both negative about",
                    value=self._format_match_list(negatives),
                    inline=False,
                )
            if neutrals:
                embed.add_field(
                    name="😐 Both neutral about",
                    value="\n".join(r["item"] for r in neutrals),
                    inline=False,
                )
            if positives:
                embed.add_field(
                    name="💚 Both positive about",
                    value=self._format_match_list(positives),
                    inline=False,
                )
            if not negatives and not neutrals and not positives:
                embed.add_field(
                    name="No matches this round",
                    value="You two couldn't agree on a single thing. Iconic.",
                    inline=False,
                )

        await channel.send(f"{p1.mention} {p2.mention}", embed=embed)

        # ── Plain-text overflow ───────────────────────────────────────────────
        if use_plain_text:
            if negatives:
                await channel.send(
                    f"**👎 Things you're both negative about:**\n"
                    + self._format_plain_list(negatives)
                )
            if neutrals:
                await channel.send(
                    f"**😐 Things you're both neutral about:**\n"
                    + "\n".join(f"• {r['item']}" for r in neutrals)
                )
            if positives:
                await channel.send(
                    f"**💚 Things you're both positive about:**\n"
                    + self._format_plain_list(positives)
                )
            if not negatives and not neutrals and not positives:
                await channel.send("No matches this round — you two couldn't agree on a single thing. Iconic.")

    # ── Helpers ───────────────────────────────────────────────────────────────

    def _format_match_list(self, items: list) -> str:
        """Format a list of matched results for an embed field (max ~950 chars)."""
        lines = []
        for r in items:
            if r["p1_choice"] == r["p2_choice"]:
                label = EXACT_LABELS[r["p1_choice"]]
                lines.append(f"**{r['item']}** *({label})*")
            else:
                lines.append(r["item"])

        result = "\n".join(lines)
        if len(result) > 950:
            truncated = []
            length = 0
            for i, line in enumerate(lines):
                if length + len(line) + 1 > 920:
                    truncated.append(f"*…and {len(lines) - i} more*")
                    break
                truncated.append(line)
                length += len(line) + 1
            result = "\n".join(truncated)
        return result or "none"

    def _format_plain_list(self, items: list) -> str:
        """Format a matched list as plain text (no length limit)."""
        lines = []
        for r in items:
            if r["p1_choice"] == r["p2_choice"]:
                label = EXACT_LABELS[r["p1_choice"]]
                lines.append(f"• **{r['item']}** ({label})")
            else:
                lines.append(f"• {r['item']}")
        return "\n".join(lines)
