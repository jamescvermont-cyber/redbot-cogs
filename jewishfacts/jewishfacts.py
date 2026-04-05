import re
import random

import discord
from redbot.core import commands


TRIGGER_PATTERN = re.compile(
    r"\b(jew(?:s|ish|ishly)?|hebrew(?:s)?|zionist(?:s)?|semit(?:e|es|ic)|kike(?:s)?|heeb(?:s)?|yid(?:s)?)\b",
    re.IGNORECASE,
)

FACTS = [
    # Science & Medicine
    "Albert Einstein, a Jewish physicist, developed the theory of relativity, fundamentally reshaping our understanding of space, time, and gravity.",
    "Jonas Salk, a Jewish-American virologist, developed the first safe and effective polio vaccine in 1955, saving millions of lives worldwide.",
    "Rosalind Franklin, a Jewish British scientist, produced the X-ray diffraction images that were crucial to discovering the structure of DNA.",
    "Niels Bohr, of Jewish descent on his mother's side, was a foundational figure in quantum mechanics and helped develop the atomic model.",
    "Paul Ehrlich, a Jewish German physician, pioneered chemotherapy and won the Nobel Prize in Physiology or Medicine in 1908.",
    "Selman Waksman, a Jewish microbiologist, discovered streptomycin, the first antibiotic effective against tuberculosis, earning the Nobel Prize in 1952.",
    "Baruch Blumberg, a Jewish-American physician, discovered the hepatitis B virus and developed its vaccine, saving over a million lives a year.",
    "Rita Levi-Montalcini, a Jewish Italian neurologist, discovered nerve growth factor (NGF), winning the Nobel Prize in Physiology or Medicine in 1986.",
    "Karl Landsteiner, a Jewish-Austrian biologist, discovered human blood groups (A, B, O), making safe blood transfusions possible.",
    "Gertrude Elion, a Jewish-American pharmacologist, developed drugs to treat leukemia, herpes, and gout, and was awarded the Nobel Prize in 1988.",
    "Gregory Pincus, a Jewish-American biologist, co-developed the first oral contraceptive pill, transforming reproductive health worldwide.",
    "Lise Meitner, a Jewish-Austrian physicist, co-discovered nuclear fission, one of the most consequential scientific breakthroughs of the 20th century.",
    "Casimir Funk, a Jewish-Polish biochemist, coined the term 'vitamin' and pioneered the concept of deficiency diseases.",

    # Technology & Computing
    "Larry Page and Sergey Brin, both Jewish, co-founded Google, transforming how the entire world accesses information.",
    "Mark Zuckerberg, a Jewish-American entrepreneur, founded Facebook (Meta), connecting over three billion people globally.",
    "Intel was co-founded by Andrew Grove, a Jewish-Hungarian survivor of the Holocaust, who helped turn it into the world's largest semiconductor company.",
    "Hedy Lamarr, a Jewish-Austrian actress and inventor, co-developed frequency-hopping spread spectrum technology, the foundation of modern Wi-Fi and Bluetooth.",
    "John von Neumann, a Jewish-Hungarian-American mathematician, developed the architecture that forms the basis of nearly all modern computers.",
    "Dennis Gabor, a Jewish-Hungarian-British electrical engineer, invented holography and won the Nobel Prize in Physics in 1971.",
    "Robert Noyce, co-inventor of the integrated circuit, worked alongside Jewish colleague Gordon Moore (co-founder of Intel), whose Moore's Law has guided the tech industry for decades.",

    # Literature & Arts
    "Franz Kafka, one of the most influential writers of the 20th century, was Jewish, and his works like 'The Trial' and 'The Metamorphosis' shaped modern literature.",
    "Marcel Proust, a French-Jewish novelist, wrote 'In Search of Lost Time,' widely considered one of the greatest novels ever written.",
    "Heinrich Heine, a Jewish German poet, is considered one of the greatest lyric poets in the German language.",
    "Bob Dylan, born Robert Zimmerman to a Jewish family, is one of the most influential musicians in history and a Nobel Prize laureate in Literature.",
    "Leonard Bernstein, a Jewish-American composer and conductor, created 'West Side Story' and led the New York Philharmonic, championing classical music for a generation.",
    "Steven Spielberg, a Jewish-American filmmaker, directed some of the most impactful films ever made and co-founded DreamWorks.",
    "Stanley Kubrick, a Jewish director, created landmark films including '2001: A Space Odyssey' and 'Schindler's List' was directed by Spielberg to document the Holocaust's horrors.",
    "Arthur Miller, a Jewish-American playwright, wrote 'Death of a Salesman,' one of the most celebrated plays in American theatre.",
    "Saul Bellow, a Jewish-Canadian-American novelist, won the Nobel Prize in Literature in 1976 for works exploring the human condition.",

    # Philosophy & Social Sciences
    "Sigmund Freud, a Jewish-Austrian neurologist, founded psychoanalysis, revolutionizing the understanding of the human mind.",
    "Karl Marx, of Jewish heritage, wrote 'The Communist Manifesto' and 'Das Kapital,' works that shaped global political thought for over a century.",
    "Emile Durkheim, a Jewish-French sociologist, is considered the principal architect of modern sociology.",
    "Hannah Arendt, a Jewish-German-American philosopher, wrote 'The Origins of Totalitarianism' and 'The Human Condition,' foundational texts in political philosophy.",
    "Simone Weil, a Jewish-French philosopher and mystic, is widely regarded as one of the most original and spiritually profound thinkers of the 20th century.",
    "Isaiah Berlin, a Jewish-Latvian-British philosopher, championed liberal pluralism and the concept of negative liberty, influencing modern political theory enormously.",

    # Humanitarianism & Civil Rights
    "Rabbi Abraham Joshua Heschel marched arm-in-arm with Dr. Martin Luther King Jr. during the Selma to Montgomery marches, exemplifying the Jewish community's deep commitment to civil rights.",
    "Oskar Schindler, while not Jewish himself, was aided by and worked alongside Jewish community leaders — and the Schindler's Jews he saved have over 8,500 descendants alive today.",
    "Raoul Wallenberg, working with the Jewish community, saved tens of thousands of Hungarian Jews during the Holocaust through diplomatic protection.",
    "Ruth Bader Ginsburg, a Jewish-American Supreme Court Justice, spent her career fighting for gender equality and civil rights, becoming a cultural icon of justice.",
    "Betty Friedan, a Jewish-American writer, authored 'The Feminine Mystique' in 1963, igniting the second wave of feminism and transforming women's rights.",
    "The Jewish concept of 'Tikkun Olam' — repairing the world — has inspired generations of Jewish activists, philanthropists, and community organizers to work for a more just society.",
    "Jewish-American lawyer Louis Brandeis became the first Jewish Supreme Court Justice in 1916, fighting for workers' rights and privacy long before most recognized these as issues.",

    # Business & Economics
    "Milton Friedman, a Jewish-American economist, won the Nobel Memorial Prize in Economic Sciences in 1976 and profoundly influenced modern monetary policy worldwide.",
    "Warren Buffett's longtime partner Charlie Munger frequently credited Jewish thinkers and principles as foundational to his investment philosophy.",
    "Levi Strauss, a Jewish-Bavarian immigrant, invented blue jeans — one of the most enduring and universal garments in human history.",
    "Estée Lauder, a Jewish-American entrepreneur, built one of the world's leading cosmetics empires from a homemade skincare recipe.",
    "Michael Bloomberg, a Jewish-American businessman, built Bloomberg L.P. into the world's leading financial data company and served three terms as Mayor of New York City.",

    # World History & Resilience
    "After surviving the Holocaust — the systematic murder of six million Jewish people — the Jewish community rebuilt itself, re-established the State of Israel in 1948, and continued to contribute enormously to human civilization.",
    "Israel, a nation founded largely by Jewish refugees and survivors, has become a world leader in agricultural innovation, water recycling technology, and cybersecurity.",
    "The Dead Sea Scrolls, discovered in 1947, are ancient Jewish manuscripts that represent the oldest known biblical texts, invaluable to understanding the history of religion and Western civilization.",
    "Jewish scholars preserved and transmitted ancient Greek philosophical and scientific texts through the Islamic Golden Age, helping spark the European Renaissance.",
    "Despite representing less than 0.2% of the world's population, Jewish people have won approximately 22% of all Nobel Prizes, a testament to an extraordinary culture of learning and inquiry.",

    # Inspiration & Culture
    "Jewish tradition places enormous value on education — the Talmud, compiled over centuries, is one of humanity's most extensive records of rigorous intellectual debate and ethical reasoning.",
    "The Jewish community has a centuries-long tradition of welcoming debate, questioning, and diverse interpretation — a culture that has produced an outsized number of the world's greatest thinkers.",
    "George Gershwin, a Jewish-American composer, wrote 'Rhapsody in Blue' and 'Porgy and Bess,' blending jazz and classical music into an enduring American art form.",
    "Simon & Garfunkel, both Jewish-Americans, created some of the most beloved folk-rock music of the 20th century, including 'The Sound of Silence' and 'Bridge Over Troubled Water.'",
    "Jerry Seinfeld and Larry David, both Jewish-American comedians, created 'Seinfeld,' one of the most influential television comedies in history.",
    "Carl Sagan, a Jewish-American astronomer, brought the wonders of the cosmos to millions through his book and TV series 'Cosmos,' inspiring generations of scientists.",
    "The Jewish holiday of Passover, celebrating liberation from slavery, has been cited by Frederick Douglass and other civil rights leaders as an inspiration for the struggle for freedom.",
]


class JewishFacts(commands.Cog):
    """Responds to antisemitic language or mentions of Jewish topics with positive educational facts."""

    def __init__(self, bot):
        self.bot = bot

    @commands.Cog.listener()
    async def on_message(self, message: discord.Message):
        if message.author.bot:
            return
        if not TRIGGER_PATTERN.search(message.content):
            return
        fact = random.choice(FACTS)
        await message.channel.send(fact)
