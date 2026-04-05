import io
import random

import discord
from PIL import Image, ImageDraw, ImageFont
from redbot.core import commands

from .words import WORDS

# ── Colour palette (Wordle dark theme) ───────────────────────────────────────
_BG     = (18,  18,  19)   # board / empty cell background
_BORDER = (58,  58,  60)   # empty cell border
_GREEN  = (83,  141, 78)   # correct letter, correct position
_YELLOW = (181, 159, 59)   # correct letter, wrong position
_GRAY   = (58,  58,  60)   # letter not in word
_WHITE  = (255, 255, 255)

_COLOR_MAP = {"green": _GREEN, "yellow": _YELLOW, "gray": _GRAY}

# ── Board geometry ────────────────────────────────────────────────────────────
_CELL = 62   # px per cell (square)
_GAP  = 6    # px gap between cells
_PAD  = 20   # px outer padding


# ── Helpers ───────────────────────────────────────────────────────────────────

def _load_font(size: int = 36) -> ImageFont.FreeTypeFont:
    candidates = [
        "arialbd.ttf",                                                    # Windows
        "arial.ttf",                                                      # Windows
        "/usr/share/fonts/truetype/dejavu/DejaVuSans-Bold.ttf",          # Debian/Ubuntu
        "/usr/share/fonts/truetype/liberation/LiberationSans-Bold.ttf",  # Fedora/RHEL
        "/usr/share/fonts/truetype/freefont/FreeSansBold.ttf",           # Alpine
        "/usr/share/fonts/truetype/noto/NotoSans-Bold.ttf",              # NotoSans
    ]
    for path in candidates:
        try:
            return ImageFont.truetype(path, size)
        except OSError:
            continue
    # PIL ≥ 10 supports a size kwarg on the built-in bitmap font
    try:
        return ImageFont.load_default(size=size)
    except TypeError:
        return ImageFont.load_default()


def _score_guess(guess: str, answer: str) -> list:
    """
    Return a list of 5 colour strings (green / yellow / gray) comparing
    *guess* against *answer*.  Handles duplicate letters correctly using
    a two-pass algorithm.
    """
    result    = ["gray"] * 5
    remaining = list(answer)   # letters still available for yellow matching

    # Pass 1 – mark greens and consume those letters
    for i in range(5):
        if guess[i] == answer[i]:
            result[i]    = "green"
            remaining[i] = ""

    # Pass 2 – mark yellows from what's left
    for i in range(5):
        if result[i] == "green":
            continue
        if guess[i] in remaining:
            result[i] = "yellow"
            remaining[remaining.index(guess[i])] = ""

    return result


def _draw_board(guesses: list, total_rows: int = 7) -> io.BytesIO:
    """Render the Wordle grid and return it as a PNG byte-stream."""
    cols = 5
    img_w = cols * _CELL + (cols - 1) * _GAP + 2 * _PAD
    img_h = total_rows * _CELL + (total_rows - 1) * _GAP + 2 * _PAD

    img  = Image.new("RGB", (img_w, img_h), _BG)
    draw = ImageDraw.Draw(img)
    font = _load_font(36)

    for row in range(total_rows):
        for col in range(cols):
            x = _PAD + col * (_CELL + _GAP)
            y = _PAD + row * (_CELL + _GAP)
            x2, y2 = x + _CELL - 1, y + _CELL - 1

            if row < len(guesses):
                word, colours = guesses[row]
                letter = word[col]
                fill   = _COLOR_MAP[colours[col]]
                draw.rectangle([x, y, x2, y2], fill=fill)
                # Centre the letter inside the cell
                bbox   = draw.textbbox((0, 0), letter, font=font)
                tw, th = bbox[2] - bbox[0], bbox[3] - bbox[1]
                draw.text(
                    (x + (_CELL - tw) // 2 - bbox[0],
                     y + (_CELL - th) // 2 - bbox[1]),
                    letter, fill=_WHITE, font=font,
                )
            else:
                draw.rectangle([x, y, x2, y2], fill=_BG, outline=_BORDER, width=2)

    buf = io.BytesIO()
    img.save(buf, format="PNG")
    buf.seek(0)
    return buf


# ── Game state ────────────────────────────────────────────────────────────────

class WordleGame:
    MAX_GUESSES = 7

    def __init__(self, word: str):
        self.word    = word.upper()
        self.guesses = []   # list of (WORD, [colour, …])
        self.won     = False

    def submit(self, guess: str) -> list:
        guess  = guess.upper()
        result = _score_guess(guess, self.word)
        self.guesses.append((guess, result))
        if guess == self.word:
            self.won = True
        return result

    @property
    def over(self) -> bool:
        return self.won or len(self.guesses) >= self.MAX_GUESSES

    @property
    def remaining(self) -> int:
        return self.MAX_GUESSES - len(self.guesses)


# ── Cog ───────────────────────────────────────────────────────────────────────

class Wordle(commands.Cog):
    """Multiplayer Wordle — anyone in chat can guess the 5-letter word."""

    def __init__(self, bot):
        self.bot   = bot
        self.games: dict = {}   # channel_id → WordleGame

    # ── Commands ──────────────────────────────────────────────────────────────

    @commands.group(invoke_without_command=True)
    async def wordle(self, ctx: commands.Context):
        """Start a multiplayer Wordle game in this channel."""
        if ctx.channel.id in self.games:
            await ctx.send(
                "A Wordle game is already running here. "
                "Type `wordle stop` to end it early."
            )
            return

        word = random.choice(WORDS).upper()
        self.games[ctx.channel.id] = WordleGame(word)
        await ctx.send(
            "**Wordle started!** Guess the 5-letter word.\n"
            f"You have **{WordleGame.MAX_GUESSES} guesses** — anyone can play!\n"
            "Just type any 5-letter word in chat."
        )

    @wordle.command(name="stop")
    async def wordle_stop(self, ctx: commands.Context):
        """Stop the current Wordle game and reveal the answer."""
        game = self.games.pop(ctx.channel.id, None)
        if game is None:
            await ctx.send("No Wordle game is running in this channel.")
            return
        await ctx.send(f"Game stopped. The word was **{game.word}**.")

    # ── Guess listener ────────────────────────────────────────────────────────

    @commands.Cog.listener()
    async def on_message(self, message: discord.Message):
        # Ignore bots and channels with no active game
        if message.author.bot:
            return
        if message.channel.id not in self.games:
            return

        word = message.content.strip()

        # Must be exactly 5 alphabetic characters
        if len(word) != 5 or not word.isalpha():
            return

        # Don't steal bot commands (e.g. `$wordle stop`)
        ctx = await self.bot.get_context(message)
        if ctx.valid:
            return

        game   = self.games[message.channel.id]
        result = game.submit(word)
        buf    = _draw_board(game.guesses, total_rows=WordleGame.MAX_GUESSES)
        file   = discord.File(buf, filename="wordle.png")

        if game.won:
            del self.games[message.channel.id]
            await message.channel.send(
                f"Congratulations {message.author.mention}! "
                f"The word was **{game.word}** — solved in "
                f"**{len(game.guesses)}** guess(es)!",
                file=file,
            )
        elif game.over:
            del self.games[message.channel.id]
            await message.channel.send(
                f"No more guesses! The word was **{game.word}**.",
                file=file,
            )
        else:
            await message.channel.send(
                f"**{game.remaining}** guess(es) remaining.",
                file=file,
            )
