import asyncio
import pathlib
import random

import discord
from redbot.core import commands

# ── Dev mode — set DEV_MODE = False for production ───────────────────────────
DEV_MODE = False

if DEV_MODE:
    import subprocess as _sp, pathlib as _pl
    try:
        _sha = _sp.check_output(
            ["git", "-C", str(_pl.Path(__file__).parent), "rev-parse", "--short", "HEAD"],
            stderr=_sp.DEVNULL, text=True,
        ).strip()
    except Exception:
        _sha = "dev"
    DEV_LABEL = f"  [{_sha}]"
else:
    DEV_LABEL = ""
# ─────────────────────────────────────────────────────────────────────────────


# ── Fruit list (~120 fruits) ──────────────────────────────────────────────────

FRUITS = [
    # Apples
    "Apple", "Fuji Apple", "Honeycrisp Apple", "Granny Smith Apple",
    "Gala Apple", "Braeburn Apple", "Pink Lady Apple", "McIntosh Apple",
    # Pears
    "Pear", "Bartlett Pear", "Asian Pear", "Bosc Pear",
    # Citrus
    "Orange", "Blood Orange", "Clementine", "Tangerine", "Mandarin",
    "Grapefruit", "Pomelo", "Lemon", "Lime", "Meyer Lemon", "Kumquat",
    "Yuzu", "Bergamot", "Cara Cara Orange", "Satsuma", "Ugli Fruit",
    # Berries
    "Strawberry", "Raspberry", "Blueberry", "Blackberry", "Cranberry",
    "Gooseberry", "Boysenberry", "Elderberry", "Mulberry", "Huckleberry",
    "Lingonberry", "Cloudberry", "Acai",
    # Stone Fruits
    "Peach", "Nectarine", "Plum", "Cherry", "Apricot", "Damson Plum",
    # Tropical (common)
    "Banana", "Plantain", "Pineapple", "Mango", "Papaya", "Coconut",
    "Guava", "Passion Fruit", "Dragon Fruit", "Lychee", "Longan",
    "Rambutan", "Jackfruit", "Durian", "Mangosteen", "Starfruit",
    # Tropical (less common but recognizable)
    "Soursop", "Cherimoya", "Feijoa", "Tamarind", "Breadfruit",
    "Ackee", "Sapodilla", "Sugar Apple", "Mamey Sapote", "Jabuticaba",
    # Melons
    "Watermelon", "Cantaloupe", "Honeydew Melon", "Canary Melon",
    "Galia Melon", "Crenshaw Melon",
    # Grapes
    "Grape", "Concord Grape", "Moondrop Grape", "Cotton Candy Grape",
    "Muscat Grape",
    # Other common
    "Kiwi", "Golden Kiwi", "Fig", "Date", "Pomegranate", "Avocado",
    "Persimmon", "Quince", "Loquat", "Currant", "Olive", "Noni",
    "Finger Lime",
]

# ── Taste factoids ───────────────────────────────────────────────────────────

FRUIT_TASTES = {
    # Apples
    "Apple":               "Sweet and slightly tart with a crisp, refreshing flavor — a mix of honey and mild citrus.",
    "Fuji Apple":          "Exceptionally sweet and juicy with a honeyed flavor and very low acidity.",
    "Honeycrisp Apple":    "A perfect balance of sweet and tart with notes of melon and honey.",
    "Granny Smith Apple":  "Very tart and acidic with a sharp, refreshing sourness that lingers.",
    "Gala Apple":          "Mild and sweet with a light floral aroma — like a softer, more delicate Fuji.",
    "Braeburn Apple":      "A balanced mix of sweet and tart with hints of spice and pear.",
    "Pink Lady Apple":     "Tangy-sweet with a fizzy, almost champagne-like effervescence.",
    "McIntosh Apple":      "Soft, mildly tart, and aromatic with a wine-like depth.",
    # Pears
    "Pear":                "Sweet and buttery with a mild floral flavor and subtle vanilla notes.",
    "Bartlett Pear":       "Very sweet and juicy with a classic pear flavor that's almost candy-like when ripe.",
    "Asian Pear":          "Crisp like an apple but lightly sweet and floral with a subtle honey undertone.",
    "Bosc Pear":           "Less sweet than most pears, with a spicy, earthy richness reminiscent of cinnamon.",
    # Citrus
    "Orange":              "Sweet and tangy with a bright, refreshing citrus flavor.",
    "Blood Orange":        "Like a regular orange but with added raspberry-like berry notes and deeper sweetness.",
    "Clementine":          "Very sweet and juicy with a mild, easy citrus flavor and almost no bitterness.",
    "Tangerine":           "Sweet and tangy like an orange but more intense and slightly more tart.",
    "Mandarin":            "Sweet, mild, and less acidic than oranges with a delicate floral note.",
    "Grapefruit":          "Bittersweet and tangy with a bold, slightly bitter citrus punch.",
    "Pomelo":              "Milder and less bitter than grapefruit with a sweet, floral citrus flavor.",
    "Lemon":               "Intensely sour and acidic with a bright, sharp citrus flavor.",
    "Lime":                "Sour and slightly more bitter than lemon with a distinctive tropical citrus edge.",
    "Meyer Lemon":         "Sweeter and less acidic than regular lemon — like a lemon-mandarin hybrid.",
    "Kumquat":             "The peel is sweet while the inside is tart and tangy — best eaten whole.",
    "Yuzu":                "Sour like a lemon but with a unique floral, almost mandarin-like complexity.",
    "Bergamot":            "Intensely fragrant with a bitter, floral citrus flavor — best known from Earl Grey tea.",
    "Cara Cara Orange":    "Sweeter than regular oranges with a hint of cherry or raspberry.",
    "Satsuma":             "Very sweet and easy to peel with almost no seeds and a mild, clean citrus flavor.",
    "Ugli Fruit":          "Sweet and mildly tangy like a cross between a grapefruit, orange, and tangerine.",
    # Berries
    "Strawberry":          "Sweet with a slight tartness and a rich, jammy red-berry flavor.",
    "Raspberry":           "Intensely tart and sweet with a bright, floral berry flavor.",
    "Blueberry":           "Mildly sweet and slightly tart with an earthy, floral undertone.",
    "Blackberry":          "Sweet and tart with a deep, jammy flavor and slight bitterness from the seeds.",
    "Cranberry":           "Extremely tart and astringent with very little natural sweetness.",
    "Gooseberry":          "Tart and tangy when unripe, turning sweet and muscat-like when fully ripe.",
    "Boysenberry":         "A deep, winey blend of blackberry, raspberry, and loganberry sweetness.",
    "Elderberry":          "Earthy and slightly tart with a floral, almost musky berry depth.",
    "Mulberry":            "Sweet and slightly tart with a complex flavor reminiscent of blackberry and raspberry.",
    "Huckleberry":         "Similar to blueberry but more intense, slightly tart, and earthier.",
    "Lingonberry":         "Very tart and slightly bitter — like cranberry but with a more floral taste.",
    "Cloudberry":          "Sweet and tart with a creamy flavor often compared to a mix of raspberry and apricot.",
    "Acai":                "Earthy and slightly bitter with a taste often described as a blend of wild berry and dark chocolate.",
    # Stone Fruits
    "Peach":               "Sweet, juicy, and fragrant with honey and vanilla undertones when ripe.",
    "Nectarine":           "Like a peach but with firmer flesh and a more intense, tangy sweetness.",
    "Plum":                "Sweet with a pleasant tartness and a rich, jammy depth of flavor.",
    "Cherry":              "Sweet and slightly tart with a deep, rich berry-like flavor.",
    "Apricot":             "Sweet and tangy with a distinctive floral note and a slight almond-like richness.",
    "Damson Plum":         "Very tart and astringent with an intensely rich, complex plum flavor.",
    # Tropical (common)
    "Banana":              "Sweet, creamy, and starchy with a mild tropical flavor that deepens as it ripens.",
    "Plantain":            "Starchier and less sweet than banana, with a savory edge when green and caramel sweetness when ripe.",
    "Pineapple":           "A bold mix of sweet and tart tropical flavor with bright, citrusy notes.",
    "Mango":               "Intensely sweet with a rich, tropical flavor often compared to a peachy-floral blend.",
    "Papaya":              "Mildly sweet with a musky, tropical flavor often described as a cross between peach and mango.",
    "Coconut":             "Rich, creamy, and mildly sweet with a distinctive nutty, tropical flavor.",
    "Guava":               "Sweet and slightly tart with a floral aroma — often described as a cross between pear and strawberry.",
    "Passion Fruit":       "Intensely tart and tropical with a sweet, floral, citrusy complexity.",
    "Dragon Fruit":        "Mild and slightly sweet with a subtle kiwi-like flavor and very little acidity.",
    "Lychee":              "Sweet and floral with a fragrant, rose-like aroma and a texture like a peeled grape.",
    "Longan":              "Similar to lychee but milder, with a subtly musky, honey-like sweetness.",
    "Rambutan":            "Very similar to lychee but slightly less floral and a bit creamier in texture.",
    "Jackfruit":           "Sweet and fruity with a flavor often compared to a mix of banana, mango, and pineapple.",
    "Durian":              "Rich, creamy, and sweet with a custard-almond complexity — famous for its powerful pungent odor.",
    "Mangosteen":          "Sweet and tangy with a delicate, floral flavor described as a mix of peach, strawberry, and citrus.",
    "Starfruit":           "Mildly sweet and slightly sour with a crisp, juicy flavor reminiscent of apple and grape.",
    # Tropical (less common)
    "Soursop":             "Sweet and tangy with a creamy texture and a flavor blending pineapple, strawberry, and coconut.",
    "Cherimoya":           "Incredibly sweet and creamy — often described as banana, pineapple, and vanilla custard combined.",
    "Feijoa":              "Sweet and tart with a unique flavor described as a cross between pineapple, guava, and strawberry.",
    "Tamarind":            "Intensely sour and tangy with a sweet, caramel-like depth.",
    "Breadfruit":          "Starchy and mild when unripe, turning sweet and banana-like when fully ripe.",
    "Ackee":               "Mild, buttery, and slightly nutty — its flavor is often compared to scrambled eggs.",
    "Sapodilla":           "Very sweet and grainy like a pear, with a rich flavor of brown sugar and vanilla.",
    "Sugar Apple":         "Intensely sweet and creamy with a custard-like texture and vanilla-coconut flavor.",
    "Mamey Sapote":        "Sweet and creamy with a complex flavor blending pumpkin, sweet potato, and almond.",
    "Jabuticaba":          "Sweet and grape-like with a jammy richness similar to muscadine grapes.",
    # Melons
    "Watermelon":          "Very sweet and refreshingly juicy with a light, watery sweetness.",
    "Cantaloupe":          "Sweet and musky with a rich, floral honey flavor.",
    "Honeydew Melon":      "Mildly sweet and very juicy with a light, floral taste and honey-like finish.",
    "Canary Melon":        "Sweet and mildly tangy with a slight pear-like flavor and crisp, pale flesh.",
    "Galia Melon":         "Sweet and aromatic, similar to cantaloupe but with a more tropical, slightly spicy edge.",
    "Crenshaw Melon":      "Very sweet and buttery with a spicy-sweet richness that's fuller than most melons.",
    # Grapes
    "Grape":               "Sweet and juicy with a bright, slightly tart flavor — varies widely by variety.",
    "Concord Grape":       "Bold, very sweet, and deeply grapey with the classic 'grape juice' flavor.",
    "Moondrop Grape":      "Crisp and very sweet with a subtle cherry-like taste.",
    "Cotton Candy Grape":  "Tastes remarkably like cotton candy — extremely sweet with almost no tartness.",
    "Muscat Grape":        "Very aromatic and sweet with a distinctive floral, almost rose-like flavor.",
    # Other common
    "Kiwi":                "Tart and sweet with a bright, tropical flavor combining hints of strawberry and banana.",
    "Golden Kiwi":         "Sweeter and less tart than green kiwi with a tropical, almost mango-like flavor.",
    "Fig":                 "Very sweet and honey-like with a jammy, earthy depth and a subtle nutty note.",
    "Date":                "Intensely sweet and caramel-like with hints of toffee and vanilla.",
    "Pomegranate":         "Sweet and tart with a bright, tangy berry-like flavor and a slight astringency.",
    "Avocado":             "Rich, creamy, and buttery with a mild, nutty flavor and almost no sweetness.",
    "Persimmon":           "Sweet and honey-like when ripe with silky, almost pudding-like texture and cinnamon-spice notes.",
    "Quince":              "Very astringent and tart when raw, but transforms into a sweet, rose-like flavor when cooked.",
    "Loquat":              "Sweet and mildly tangy with a flavor combining peach, citrus, and mild cherry.",
    "Currant":             "Very tart and sharp with a deep, earthy berry flavor.",
    "Olive":               "Bitter and tangy with a rich, savory, briny quality — quite unlike most fruits.",
    "Noni":                "Notoriously pungent and bitter with a strong, cheese-like flavor most people find unpleasant.",
    "Finger Lime":         "Bursts of intensely sour citrus juice similar to lime, with a unique effervescent, caviar-like texture.",
}

# ── Image library ─────────────────────────────────────────────────────────────

IMAGES_DIR = pathlib.Path(__file__).parent / "images"
_IMAGE_EXTS = {".jpg", ".jpeg", ".png", ".gif", ".webp"}

# ── Helpers ───────────────────────────────────────────────────────────────────

_WORD_COUNT_NAMES = {2: "Two", 3: "Three", 4: "Four", 5: "Five"}


def _scramble(name: str) -> str:
    """Scramble each word in the fruit name independently."""
    words = name.split()
    scrambled = []
    for word in words:
        letters = list(word)
        random.shuffle(letters)
        scrambled.append("".join(letters))
    return " ".join(scrambled)


def _build_first_hint(fruit: str) -> str:
    """Return the first hint string: first letter, letter count, word count."""
    words = fruit.split()
    first_letter = fruit[0].upper()
    letter_count = sum(len(w) for w in words)
    line = f"Starts with letter **{first_letter}** and is **{letter_count}** letters long"
    if len(words) > 1:
        word_label = _WORD_COUNT_NAMES.get(len(words), str(len(words)))
        line += f"\n{word_label} words"
    return line


# ── Game state ────────────────────────────────────────────────────────────────

class FruitGame:
    MAX_HINTS = 3

    def __init__(self, fruit: str, images: list, task: asyncio.Task):
        self.fruit = fruit
        self.images = images          # list[pathlib.Path]
        self.used: set = set()        # indices already shown this round
        self.hints_used = 0
        self.task = task
        self.participants: set = set()

    def pop_image(self) -> "pathlib.Path | None":
        if not self.images:
            return None
        unused = [i for i in range(len(self.images)) if i not in self.used]
        if not unused:                # exhausted all images — reset pool
            self.used.clear()
            unused = list(range(len(self.images)))
        idx = random.choice(unused)
        self.used.add(idx)
        return self.images[idx]


# ── Hint button ───────────────────────────────────────────────────────────────

class FruitHintView(discord.ui.View):
    """Single-use green Hint button. Disables itself when clicked, then sends
    the next hint as a followup (with a fresh button if hints remain)."""

    def __init__(self, cog: "FruitGuesser", channel_id: int):
        super().__init__(timeout=70)
        self.cog = cog
        self.channel_id = channel_id
        self._used = False

    @discord.ui.button(label="Hint", style=discord.ButtonStyle.success)
    async def hint_button(self, interaction: discord.Interaction, button: discord.ui.Button):
        if self._used:
            await interaction.response.send_message(
                "Use the most recent Hint button!", ephemeral=True
            )
            return

        game = self.cog.games.get(self.channel_id)
        if not game:
            await interaction.response.send_message(
                "This game has already ended.", ephemeral=True
            )
            return
        if game.hints_used >= FruitGame.MAX_HINTS:
            await interaction.response.send_message(
                f"All **{FruitGame.MAX_HINTS}** hints have been used — keep guessing!",
                ephemeral=True,
            )
            return

        self._used = True
        button.disabled = True
        game.hints_used += 1
        remaining = FruitGame.MAX_HINTS - game.hints_used
        footer = f"{remaining} hint(s) remaining." if remaining else "No more hints after this!"
        is_final = game.hints_used == FruitGame.MAX_HINTS

        await interaction.response.edit_message(view=self)

        if game.hints_used == 1:
            # First hint: letter / word count info
            embed = discord.Embed(
                title=f"Hint {game.hints_used}/{FruitGame.MAX_HINTS}",
                description=_build_first_hint(game.fruit),
                color=discord.Color.gold(),
            )
            embed.set_footer(text=footer)
            await interaction.followup.send(
                embed=embed,
                view=FruitHintView(self.cog, self.channel_id),
            )
        elif is_final:
            # Last hint: scrambled name
            embed = discord.Embed(
                title=f"Hint {game.hints_used}/{FruitGame.MAX_HINTS} — Final Hint!",
                description=f"The fruit name scrambled: **{_scramble(game.fruit)}**",
                color=discord.Color.red(),
            )
            embed.set_footer(text=footer)
            await interaction.followup.send(embed=embed)
        else:
            # Middle hints: another image
            path = game.pop_image()
            embed = discord.Embed(
                title=f"Hint {game.hints_used}/{FruitGame.MAX_HINTS}",
                description="Here's another look!",
                color=discord.Color.gold(),
            )
            embed.set_footer(text=footer)
            embed.set_image(url="attachment://hint.jpg")
            await interaction.followup.send(
                embed=embed,
                file=discord.File(path, filename="hint.jpg"),
                view=FruitHintView(self.cog, self.channel_id),
            )


# ── Play Again button ─────────────────────────────────────────────────────────

class FruitPlayAgainView(discord.ui.View):
    def __init__(self, cog: "FruitGuesser", channel_id: int):
        super().__init__(timeout=300)
        self.cog = cog
        self.channel_id = channel_id

    @discord.ui.button(label="Play Again", style=discord.ButtonStyle.green, emoji="🎮")
    async def play_again(self, interaction: discord.Interaction, button: discord.ui.Button):
        if self.channel_id in self.cog.games:
            await interaction.response.send_message(
                "A game is already running here!", ephemeral=True
            )
            return
        button.disabled = True
        await interaction.response.edit_message(view=self)
        await self.cog._start_game(interaction.channel)

    async def on_timeout(self):
        for item in self.children:
            item.disabled = True


# ── Cog ───────────────────────────────────────────────────────────────────────

class FruitGuesser(commands.Cog):
    """Fruit guessing game — who can identify the mystery fruit from a photo?"""

    _IS_IMAGE_GUESSER = True   # marker used by _rival_game_running
    _DISPLAY_NAME = "Fruit Guesser"

    def __init__(self, bot):
        self.bot = bot
        self.games: dict[int, FruitGame] = {}   # channel_id → FruitGame

    def _rival_game_running(self, channel_id: int) -> "str | None":
        """Return display name of another image-guesser running in this channel, or None."""
        for cog in self.bot.cogs.values():
            if cog is self:
                continue
            if getattr(cog, "_IS_IMAGE_GUESSER", False) and channel_id in getattr(cog, "games", {}):
                return getattr(cog, "_DISPLAY_NAME", type(cog).__name__)
        return None

    # ── Image loading ─────────────────────────────────────────────────────────

    def _load_images(self, fruit: str) -> list:
        """Return a shuffled list of image Paths from the fruit's folder."""
        folder = IMAGES_DIR / fruit
        if not folder.is_dir():
            return []
        paths = [p for p in folder.iterdir() if p.suffix.lower() in _IMAGE_EXTS and p.is_file()]
        random.shuffle(paths)
        return paths

    # ── Timer ─────────────────────────────────────────────────────────────────

    async def _game_timer(self, channel: discord.TextChannel, fruit: str):
        """Background task that ends the round after 60 seconds."""
        try:
            await asyncio.sleep(60)
        except asyncio.CancelledError:
            return  # game was won; task cancelled by on_message handler

        game = self.games.pop(channel.id, None)
        if game is None:
            return

        tp = self.bot.get_cog("TrackPoints")
        if tp:
            await tp.record_game_result(None, game.participants)
        embed = discord.Embed(
            title="Time's up!",
            description=f"Nobody guessed it. The fruit was **{fruit}**.",
            color=discord.Color(0x99aab5),
        )
        taste = FRUIT_TASTES.get(fruit)
        if taste:
            embed.add_field(name="Taste", value=taste, inline=False)
        await channel.send(embed=embed, view=FruitPlayAgainView(self, channel.id))

    # ── Start game ────────────────────────────────────────────────────────────

    async def _start_game(self, channel: discord.TextChannel):
        rival = self._rival_game_running(channel.id)
        if rival:
            await channel.send(f"**{rival}** is already running here! Finish that game first.")
            return
        fruit, images = None, []
        for candidate in random.sample(FRUITS, len(FRUITS)):
            imgs = self._load_images(candidate)
            if imgs:
                fruit, images = candidate, imgs
                break

        if fruit is None:
            await channel.send(
                "No fruit images found on disk. "
                "Run `python fruitguesser/download_images.py` to download the image library first."
            )
            return

        task = asyncio.create_task(self._game_timer(channel, fruit))
        game = FruitGame(fruit, images, task)
        self.games[channel.id] = game

        embed = discord.Embed(
            title=f"What fruit is this??{DEV_LABEL}",
            description=(
                "Type your guess in chat — anyone can answer!\n"
                "You have **60 seconds**. Use the **Hint** button below *(3 max)*."
            ),
            color=discord.Color.green(),
        )
        embed.set_footer(text="Hint 1: letter/length info  |  Hint 2: another image  |  Hint 3: scrambled name")
        embed.set_image(url="attachment://fruit.jpg")

        first_image = game.pop_image()
        await channel.send(
            embed=embed,
            file=discord.File(first_image, filename="fruit.jpg"),
            view=FruitHintView(self, channel.id),
        )

    # ── Commands ──────────────────────────────────────────────────────────────

    @commands.command()
    async def fruitguesser(self, ctx: commands.Context):
        """Start a fruit guessing game. 60 seconds — can you name it?"""
        if ctx.channel.id in self.games:
            await ctx.send(
                "A game is already running here! "
                "Type your guess or use the Hint button for another image."
            )
            return
        await self._start_game(ctx.channel)

    # ── Guess listener ────────────────────────────────────────────────────────

    @commands.Cog.listener()
    async def on_message(self, message: discord.Message):
        if message.author.bot:
            return
        game = self.games.get(message.channel.id)
        if not game:
            return

        # Ignore valid bot commands (e.g. $fruitguesser)
        ctx = await self.bot.get_context(message)
        if ctx.valid:
            return

        game.participants.add(message.author)

        if message.content.strip().lower() != game.fruit.lower():
            return

        # ── Correct guess ──────────────────────────────────────────────────
        game.task.cancel()
        del self.games[message.channel.id]

        tp = self.bot.get_cog("TrackPoints")
        total_pts = None
        if tp:
            await tp.record_game_result(message.author, game.participants)
            total_pts = await tp.get_points(message.author)
        pts_line = f"\nYou now have **{total_pts:,}** total points!" if total_pts is not None else ""
        embed = discord.Embed(
            title="Correct!",
            description=(
                f"**{message.author.display_name}** got it!{pts_line}\n\n"
                f"The fruit was **{game.fruit}**! Congratulations!"
            ),
            color=discord.Color.green(),
        )
        embed.set_footer(text="Start a new game any time with $fruitguesser!")
        await message.channel.send(embed=embed, view=FruitPlayAgainView(self, message.channel.id))

    # ── Cleanup on unload ─────────────────────────────────────────────────────

    async def force_stop_game(self, channel_id: int):
        """Stop any active game in channel_id. Returns game name if stopped, else None."""
        game = self.games.pop(channel_id, None)
        if game is None:
            return None
        game.task.cancel()
        return "Fruit Guesser"

    def cog_unload(self):
        for game in self.games.values():
            game.task.cancel()
        self.games.clear()
