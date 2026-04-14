# ── Food metadata: country of origin + key ingredients ───────────────────────
# origin: main country/region; parenthetical notes added where the dish is
#         eaten widely elsewhere or where origin is disputed.
# ingredients: up to 7 most distinctive ingredients.

FOOD_DATA = {
    # ── Tier 1: Universal icons ──────────────────────────────────────────────
    "Pizza": {
        "origin": "Italy (now enjoyed worldwide)",
        "ingredients": ["flour", "tomato sauce", "mozzarella", "olive oil", "yeast", "basil", "salt"],
    },
    "Hamburger": {
        "origin": "USA (now enjoyed worldwide)",
        "ingredients": ["beef patty", "bun", "lettuce", "tomato", "onion", "condiments", "cheese"],
    },
    "Sushi": {
        "origin": "Japan (now enjoyed worldwide)",
        "ingredients": ["sushi rice", "nori", "fresh fish", "rice vinegar", "wasabi", "soy sauce", "pickled ginger"],
    },
    "Tacos": {
        "origin": "Mexico (now enjoyed worldwide)",
        "ingredients": ["corn tortilla", "meat", "onion", "cilantro", "salsa", "lime", "cheese"],
    },
    "Pasta": {
        "origin": "Italy (now enjoyed worldwide)",
        "ingredients": ["flour", "eggs", "water", "tomato sauce", "olive oil", "garlic", "Parmesan"],
    },

    # ── Tier 2: Very widely known ────────────────────────────────────────────
    "Fried Chicken": {
        "origin": "USA — Southern (now enjoyed worldwide)",
        "ingredients": ["chicken", "flour", "buttermilk", "salt", "pepper", "oil", "spices"],
    },
    "Hot Dog": {
        "origin": "Germany/USA (now enjoyed worldwide)",
        "ingredients": ["sausage", "bun", "mustard", "ketchup", "onion", "relish"],
    },
    "French Fries": {
        "origin": "Belgium (origin disputed with France; eaten worldwide)",
        "ingredients": ["potatoes", "oil", "salt"],
    },
    "Burrito": {
        "origin": "Mexico/USA — Tex-Mex (now enjoyed worldwide)",
        "ingredients": ["flour tortilla", "rice", "beans", "meat", "cheese", "sour cream", "salsa"],
    },
    "Sandwich": {
        "origin": "England (now enjoyed worldwide)",
        "ingredients": ["bread", "meat or cheese", "lettuce", "tomato", "condiments"],
    },
    "Cheeseburger": {
        "origin": "USA (now enjoyed worldwide)",
        "ingredients": ["beef patty", "bun", "cheese", "lettuce", "tomato", "onion", "condiments"],
    },
    "Lasagna": {
        "origin": "Italy (now enjoyed worldwide)",
        "ingredients": ["lasagna sheets", "meat sauce", "béchamel", "mozzarella", "Parmesan", "tomatoes", "herbs"],
    },
    "Ramen": {
        "origin": "Japan (noodle roots in China; now enjoyed worldwide)",
        "ingredients": ["wheat noodles", "pork broth", "chashu pork", "soft-boiled egg", "nori", "bamboo shoots", "green onion"],
    },
    "Dumplings": {
        "origin": "China (many regional variants eaten worldwide)",
        "ingredients": ["dough", "pork or vegetable filling", "garlic", "ginger", "soy sauce", "sesame oil"],
    },
    "Mac and Cheese": {
        "origin": "USA (now enjoyed worldwide)",
        "ingredients": ["macaroni", "cheddar cheese", "butter", "milk", "flour", "salt", "breadcrumbs"],
    },
    "Pancakes": {
        "origin": "USA (similar flat cakes eaten worldwide)",
        "ingredients": ["flour", "eggs", "milk", "butter", "baking powder", "sugar", "salt"],
    },
    "Waffles": {
        "origin": "Belgium (now enjoyed worldwide)",
        "ingredients": ["flour", "eggs", "butter", "milk", "baking powder", "sugar", "vanilla"],
    },
    "Croissant": {
        "origin": "France (inspired by Austrian kipferl; now enjoyed worldwide)",
        "ingredients": ["flour", "butter", "yeast", "milk", "sugar", "salt", "eggs"],
    },
    "Cheesecake": {
        "origin": "USA (ancient Greek origins; now enjoyed worldwide)",
        "ingredients": ["cream cheese", "sugar", "eggs", "graham cracker crust", "butter", "vanilla", "sour cream"],
    },
    "Donut": {
        "origin": "USA (Dutch-inspired; now enjoyed worldwide)",
        "ingredients": ["flour", "sugar", "yeast", "eggs", "butter", "milk", "oil"],
    },
    "Grilled Cheese Sandwich": {
        "origin": "USA (now enjoyed worldwide)",
        "ingredients": ["bread", "cheese", "butter"],
    },
    "Caesar Salad": {
        "origin": "Mexico (invented by an Italian chef in Tijuana; popular worldwide)",
        "ingredients": ["romaine lettuce", "croutons", "Parmesan", "Caesar dressing", "lemon", "Worcestershire", "anchovy"],
    },
    "Scrambled Eggs": {
        "origin": "Global (no single country of origin)",
        "ingredients": ["eggs", "butter", "salt", "pepper", "milk or cream"],
    },
    "Pad Thai": {
        "origin": "Thailand (now enjoyed worldwide)",
        "ingredients": ["rice noodles", "shrimp or tofu", "eggs", "bean sprouts", "peanuts", "tamarind", "fish sauce"],
    },
    "Apple Pie": {
        "origin": "USA (pastry tradition from England; now enjoyed worldwide)",
        "ingredients": ["apples", "pie crust", "sugar", "cinnamon", "butter", "lemon juice", "flour"],
    },
    "Steak": {
        "origin": "Global (especially associated with Argentina and the USA)",
        "ingredients": ["beef", "salt", "pepper", "butter", "garlic", "herbs", "oil"],
    },
    "Fish and Chips": {
        "origin": "England (now enjoyed worldwide, especially in the Commonwealth)",
        "ingredients": ["white fish", "potatoes", "flour", "beer batter", "oil", "salt", "malt vinegar"],
    },
    "Chicken Curry": {
        "origin": "India (now enjoyed worldwide, especially in the UK)",
        "ingredients": ["chicken", "curry spices", "tomatoes", "onion", "garlic", "ginger", "cream"],
    },
    "Crepes": {
        "origin": "France (now enjoyed worldwide)",
        "ingredients": ["flour", "eggs", "milk", "butter", "sugar", "vanilla", "salt"],
    },
    "Omelette": {
        "origin": "France (eaten worldwide)",
        "ingredients": ["eggs", "butter", "salt", "cheese", "herbs", "pepper"],
    },

    # ── American ─────────────────────────────────────────────────────────────
    "BBQ Ribs": {
        "origin": "USA — Southern",
        "ingredients": ["pork ribs", "BBQ sauce", "brown sugar", "garlic", "paprika", "cayenne", "vinegar"],
    },
    "Buffalo Wings": {
        "origin": "USA (Buffalo, NY; now enjoyed worldwide)",
        "ingredients": ["chicken wings", "hot sauce", "butter", "garlic powder", "vinegar", "celery", "blue cheese"],
    },
    "Philly Cheesesteak": {
        "origin": "USA (Philadelphia, PA)",
        "ingredients": ["beef", "hoagie roll", "Cheez Whiz or provolone", "onion", "green pepper"],
    },
    "Clam Chowder": {
        "origin": "USA (New England)",
        "ingredients": ["clams", "potatoes", "cream", "onion", "bacon", "celery", "flour"],
    },
    "Corn Dog": {
        "origin": "USA",
        "ingredients": ["hot dog", "cornmeal batter", "flour", "eggs", "milk", "oil", "sugar"],
    },
    "Bacon and Eggs": {
        "origin": "USA/UK (eaten worldwide)",
        "ingredients": ["bacon", "eggs", "butter", "salt", "pepper"],
    },
    "Eggs Benedict": {
        "origin": "USA (New York City)",
        "ingredients": ["English muffin", "Canadian bacon", "poached eggs", "hollandaise sauce", "butter", "lemon"],
    },
    "BLT Sandwich": {
        "origin": "USA (now enjoyed worldwide)",
        "ingredients": ["bacon", "lettuce", "tomato", "bread", "mayonnaise"],
    },
    "Club Sandwich": {
        "origin": "USA (now enjoyed worldwide)",
        "ingredients": ["toast", "turkey or chicken", "bacon", "lettuce", "tomato", "mayonnaise"],
    },
    "Lobster Roll": {
        "origin": "USA (New England)",
        "ingredients": ["lobster", "mayonnaise or butter", "celery", "lemon", "hot dog bun", "chives"],
    },
    "Pulled Pork Sandwich": {
        "origin": "USA — Southern BBQ",
        "ingredients": ["pork shoulder", "BBQ sauce", "coleslaw", "bun", "vinegar", "spices"],
    },
    "Biscuits and Gravy": {
        "origin": "USA — Southern",
        "ingredients": ["biscuits", "pork sausage", "flour", "butter", "milk", "pepper"],
    },
    "Meatloaf": {
        "origin": "USA (similar dishes also in Germany and Scandinavia)",
        "ingredients": ["ground beef", "breadcrumbs", "eggs", "onion", "ketchup", "Worcestershire sauce", "milk"],
    },
    "Pot Roast": {
        "origin": "USA",
        "ingredients": ["beef chuck", "potatoes", "carrots", "onion", "beef broth", "garlic", "herbs"],
    },
    "Turkey and Stuffing": {
        "origin": "USA (Thanksgiving tradition)",
        "ingredients": ["turkey", "bread stuffing", "celery", "onion", "herbs", "butter", "broth"],
    },
    "Reuben Sandwich": {
        "origin": "USA (New York or Nebraska, origin debated)",
        "ingredients": ["rye bread", "corned beef", "Swiss cheese", "sauerkraut", "Russian dressing"],
    },
    "Cobb Salad": {
        "origin": "USA (Hollywood, CA)",
        "ingredients": ["romaine lettuce", "bacon", "chicken", "hard-boiled eggs", "avocado", "blue cheese", "tomato"],
    },
    "Chicken and Waffles": {
        "origin": "USA (Southern/Harlem soul food)",
        "ingredients": ["fried chicken", "waffles", "maple syrup", "butter", "hot sauce"],
    },
    "French Toast": {
        "origin": "USA/France (versions eaten worldwide)",
        "ingredients": ["bread", "eggs", "milk", "butter", "cinnamon", "sugar", "vanilla"],
    },
    "Cinnamon Roll": {
        "origin": "Sweden (hugely popular in the USA; now enjoyed worldwide)",
        "ingredients": ["flour", "cinnamon", "butter", "sugar", "yeast", "cream cheese frosting", "milk"],
    },
    "Banana Split": {
        "origin": "USA (Latrobe, PA)",
        "ingredients": ["banana", "vanilla ice cream", "chocolate ice cream", "strawberry ice cream", "hot fudge", "whipped cream", "maraschino cherry"],
    },
    "Brownie": {
        "origin": "USA (now enjoyed worldwide)",
        "ingredients": ["chocolate", "butter", "sugar", "eggs", "flour", "vanilla", "salt"],
    },
    "Pecan Pie": {
        "origin": "USA — Southern",
        "ingredients": ["pecans", "corn syrup", "eggs", "butter", "sugar", "vanilla", "pie crust"],
    },
    "Corn Bread": {
        "origin": "USA (Native American and Southern tradition)",
        "ingredients": ["cornmeal", "flour", "eggs", "butter", "milk", "sugar", "baking powder"],
    },
    "Potato Skins": {
        "origin": "USA",
        "ingredients": ["potatoes", "bacon", "cheddar cheese", "sour cream", "chives", "butter"],
    },
    "Deviled Eggs": {
        "origin": "USA (similar versions eaten across Europe)",
        "ingredients": ["eggs", "mayonnaise", "mustard", "vinegar", "paprika", "salt", "pepper"],
    },
    "Sloppy Joe": {
        "origin": "USA",
        "ingredients": ["ground beef", "tomato sauce", "onion", "green pepper", "bun", "brown sugar", "Worcestershire"],
    },
    "Funnel Cake": {
        "origin": "USA (Pennsylvania Dutch, inspired by German Strauben)",
        "ingredients": ["flour", "eggs", "milk", "sugar", "baking powder", "powdered sugar", "oil"],
    },
    "Lobster Bisque": {
        "origin": "France (classic French cuisine; popular in the USA)",
        "ingredients": ["lobster", "cream", "butter", "onion", "carrot", "cognac", "tomato paste"],
    },
    "Jalapeño Poppers": {
        "origin": "USA — Tex-Mex",
        "ingredients": ["jalapeños", "cream cheese", "cheddar", "bacon", "breadcrumbs", "egg", "oil"],
    },

    # ── Italian ──────────────────────────────────────────────────────────────
    "Margherita Pizza": {
        "origin": "Italy (Naples)",
        "ingredients": ["pizza dough", "tomato sauce", "mozzarella", "basil", "olive oil", "salt"],
    },
    "Pepperoni Pizza": {
        "origin": "USA (Italian-American invention; popular worldwide)",
        "ingredients": ["pizza dough", "tomato sauce", "mozzarella", "pepperoni", "olive oil"],
    },
    "Mushroom Pizza": {
        "origin": "Italy/USA (eaten worldwide)",
        "ingredients": ["pizza dough", "tomato sauce", "mozzarella", "mushrooms", "olive oil", "garlic"],
    },
    "Carbonara": {
        "origin": "Italy (Rome)",
        "ingredients": ["spaghetti", "guanciale", "eggs", "Pecorino Romano", "Parmesan", "black pepper"],
    },
    "Spaghetti Bolognese": {
        "origin": "Italy (Bologna; now enjoyed worldwide)",
        "ingredients": ["spaghetti", "ground beef", "tomatoes", "onion", "carrot", "celery", "wine"],
    },
    "Risotto": {
        "origin": "Italy (Northern Italy)",
        "ingredients": ["Arborio rice", "white wine", "Parmesan", "butter", "onion", "broth", "olive oil"],
    },
    "Tiramisu": {
        "origin": "Italy (Veneto; now enjoyed worldwide)",
        "ingredients": ["ladyfingers", "espresso", "mascarpone", "eggs", "sugar", "cocoa powder", "marsala"],
    },
    "Chicken Parmigiana": {
        "origin": "Italy/USA (popularized as Italian-American; now enjoyed worldwide)",
        "ingredients": ["chicken breast", "tomato sauce", "mozzarella", "Parmesan", "breadcrumbs", "eggs"],
    },
    "Gnocchi": {
        "origin": "Italy (now enjoyed worldwide)",
        "ingredients": ["potatoes", "flour", "eggs", "salt", "Parmesan", "butter", "sage"],
    },
    "Cannoli": {
        "origin": "Italy (Sicily)",
        "ingredients": ["pastry shells", "ricotta", "sugar", "chocolate chips", "pistachios", "orange zest", "vanilla"],
    },
    "Fettuccine Alfredo": {
        "origin": "Italy (Rome; hugely popular in the USA)",
        "ingredients": ["fettuccine", "Parmesan", "butter", "pasta water", "salt", "black pepper"],
    },
    "Focaccia": {
        "origin": "Italy (Liguria; now enjoyed worldwide)",
        "ingredients": ["flour", "olive oil", "yeast", "salt", "rosemary", "water"],
    },
    "Minestrone": {
        "origin": "Italy (now enjoyed worldwide)",
        "ingredients": ["mixed vegetables", "beans", "pasta or rice", "tomatoes", "onion", "garlic", "broth"],
    },
    "Ravioli": {
        "origin": "Italy (now enjoyed worldwide)",
        "ingredients": ["pasta dough", "ricotta or meat filling", "Parmesan", "eggs", "butter", "sage", "flour"],
    },
    "Osso Buco": {
        "origin": "Italy (Milan)",
        "ingredients": ["veal shanks", "white wine", "tomatoes", "onion", "carrots", "celery", "gremolata"],
    },
    "Bruschetta": {
        "origin": "Italy (now enjoyed worldwide)",
        "ingredients": ["crusty bread", "tomatoes", "garlic", "olive oil", "basil", "salt", "pepper"],
    },
    "Calzone": {
        "origin": "Italy (Naples)",
        "ingredients": ["pizza dough", "ricotta", "mozzarella", "ham or salami", "tomato sauce", "olive oil", "egg"],
    },
    "Panna Cotta": {
        "origin": "Italy (Piedmont; now enjoyed worldwide)",
        "ingredients": ["cream", "sugar", "gelatin", "vanilla", "milk", "fruit coulis"],
    },
    "Arancini": {
        "origin": "Italy (Sicily)",
        "ingredients": ["risotto rice", "breadcrumbs", "mozzarella", "tomato sauce", "eggs", "Parmesan", "oil"],
    },
    "Polenta": {
        "origin": "Italy (Northern Italy; also widely eaten in Eastern Europe and South America)",
        "ingredients": ["cornmeal", "water or broth", "butter", "Parmesan", "salt", "cream"],
    },

    # ── French ───────────────────────────────────────────────────────────────
    "French Onion Soup": {
        "origin": "France (now enjoyed worldwide)",
        "ingredients": ["onions", "beef broth", "butter", "white wine", "baguette", "Gruyère", "thyme"],
    },
    "Coq au Vin": {
        "origin": "France",
        "ingredients": ["chicken", "red wine", "bacon", "mushrooms", "onion", "garlic", "thyme"],
    },
    "Crème Brûlée": {
        "origin": "France (now enjoyed worldwide)",
        "ingredients": ["cream", "egg yolks", "sugar", "vanilla", "sugar (for caramelizing)"],
    },
    "Ratatouille": {
        "origin": "France (Provence)",
        "ingredients": ["zucchini", "eggplant", "tomatoes", "bell peppers", "onion", "garlic", "olive oil"],
    },
    "Bouillabaisse": {
        "origin": "France (Marseille)",
        "ingredients": ["mixed fish and seafood", "tomatoes", "onion", "garlic", "saffron", "fennel", "olive oil"],
    },
    "Beef Bourguignon": {
        "origin": "France (Burgundy; now enjoyed worldwide)",
        "ingredients": ["beef", "red wine", "bacon", "mushrooms", "pearl onions", "garlic", "thyme"],
    },
    "Éclair": {
        "origin": "France (now enjoyed worldwide)",
        "ingredients": ["choux pastry", "pastry cream", "chocolate glaze", "eggs", "butter", "flour", "milk"],
    },
    "Macarons": {
        "origin": "France (Paris; now enjoyed worldwide)",
        "ingredients": ["almond flour", "egg whites", "powdered sugar", "buttercream filling", "food coloring"],
    },
    "Soufflé": {
        "origin": "France",
        "ingredients": ["eggs", "butter", "flour", "milk", "Gruyère (savory) or chocolate (sweet)", "sugar"],
    },
    "Quiche": {
        "origin": "France (now enjoyed worldwide)",
        "ingredients": ["pie crust", "eggs", "cream", "Gruyère", "bacon or ham", "salt", "pepper"],
    },
    "Croque Monsieur": {
        "origin": "France",
        "ingredients": ["bread", "ham", "Gruyère", "béchamel sauce", "butter", "Dijon mustard"],
    },

    # ── Japanese ─────────────────────────────────────────────────────────────
    "Sashimi": {
        "origin": "Japan",
        "ingredients": ["fresh fish or seafood", "soy sauce", "wasabi", "pickled ginger"],
    },
    "Tempura": {
        "origin": "Japan (technique introduced by Portuguese missionaries)",
        "ingredients": ["shrimp or vegetables", "tempura batter", "flour", "ice water", "eggs", "dipping sauce"],
    },
    "Udon": {
        "origin": "Japan (now enjoyed worldwide)",
        "ingredients": ["thick wheat noodles", "dashi broth", "soy sauce", "mirin", "green onion", "fish cake"],
    },
    "Miso Soup": {
        "origin": "Japan (now enjoyed worldwide)",
        "ingredients": ["miso paste", "dashi", "tofu", "wakame seaweed", "green onion", "water"],
    },
    "Teriyaki Chicken": {
        "origin": "Japan (now enjoyed worldwide)",
        "ingredients": ["chicken", "soy sauce", "mirin", "sake", "sugar", "ginger", "garlic"],
    },
    "Yakitori": {
        "origin": "Japan",
        "ingredients": ["chicken skewers", "soy sauce", "mirin", "sake", "sugar", "green onion"],
    },
    "Tonkatsu": {
        "origin": "Japan",
        "ingredients": ["pork cutlet", "panko breadcrumbs", "eggs", "flour", "oil", "tonkatsu sauce", "cabbage"],
    },
    "Okonomiyaki": {
        "origin": "Japan",
        "ingredients": ["flour", "cabbage", "eggs", "dashi", "pork or shrimp", "mayonnaise", "okonomiyaki sauce"],
    },
    "Takoyaki": {
        "origin": "Japan (Osaka)",
        "ingredients": ["flour batter", "dashi", "eggs", "octopus", "green onion", "pickled ginger", "bonito flakes"],
    },
    "Onigiri": {
        "origin": "Japan",
        "ingredients": ["short-grain rice", "nori", "salt", "salmon or tuna or umeboshi filling"],
    },
    "Soba": {
        "origin": "Japan",
        "ingredients": ["buckwheat noodles", "dashi broth", "soy sauce", "mirin", "green onion", "wasabi"],
    },
    "Gyoza": {
        "origin": "Japan (adapted from Chinese jiaozi)",
        "ingredients": ["ground pork", "cabbage", "garlic", "ginger", "soy sauce", "sesame oil", "dumpling wrappers"],
    },
    "Yakisoba": {
        "origin": "Japan",
        "ingredients": ["egg noodles", "pork or chicken", "cabbage", "soy sauce", "oyster sauce", "Worcestershire", "bonito flakes"],
    },
    "Katsu Curry": {
        "origin": "Japan (now enjoyed worldwide)",
        "ingredients": ["pork or chicken cutlet", "curry sauce", "onion", "carrot", "potato", "rice", "breadcrumbs"],
    },
    "Mochi": {
        "origin": "Japan (also eaten widely across East and Southeast Asia)",
        "ingredients": ["glutinous rice flour", "sugar", "water", "red bean paste or ice cream filling"],
    },
    "Karaage": {
        "origin": "Japan (now enjoyed worldwide)",
        "ingredients": ["chicken", "soy sauce", "sake", "ginger", "garlic", "potato starch", "oil"],
    },
    "Sukiyaki": {
        "origin": "Japan",
        "ingredients": ["thinly sliced beef", "tofu", "glass noodles", "vegetables", "soy sauce", "sake", "mirin"],
    },

    # ── Chinese ──────────────────────────────────────────────────────────────
    "Peking Duck": {
        "origin": "China (Beijing)",
        "ingredients": ["whole duck", "hoisin sauce", "pancakes", "green onion", "cucumber", "plum sauce", "maltose"],
    },
    "Dim Sum": {
        "origin": "China (Cantonese; served worldwide in Chinese restaurants)",
        "ingredients": ["various dumplings and buns", "shrimp or pork filling", "soy sauce", "hoisin", "sesame oil", "ginger"],
    },
    "Kung Pao Chicken": {
        "origin": "China (Sichuan; now enjoyed worldwide)",
        "ingredients": ["chicken", "peanuts", "dried chilies", "soy sauce", "Sichuan pepper", "garlic", "ginger"],
    },
    "Sweet and Sour Pork": {
        "origin": "China (Cantonese; now enjoyed worldwide)",
        "ingredients": ["pork", "vinegar", "sugar", "ketchup", "pineapple", "bell peppers", "onion"],
    },
    "Hot Pot": {
        "origin": "China (widely eaten across East Asia, especially in winter)",
        "ingredients": ["spiced broth", "thinly sliced meat", "vegetables", "tofu", "noodles", "dipping sauces"],
    },
    "Mapo Tofu": {
        "origin": "China (Sichuan)",
        "ingredients": ["tofu", "ground pork", "doubanjiang", "soy sauce", "Sichuan peppercorns", "garlic", "ginger"],
    },
    "Char Siu": {
        "origin": "China (Cantonese)",
        "ingredients": ["pork", "hoisin sauce", "soy sauce", "honey", "five-spice powder", "garlic", "red food coloring"],
    },
    "General Tso's Chicken": {
        "origin": "USA (Chinese-American; inspired by Hunan cuisine; popular worldwide)",
        "ingredients": ["chicken", "soy sauce", "rice vinegar", "sugar", "garlic", "ginger", "dried chilies"],
    },
    "Wonton Soup": {
        "origin": "China (Cantonese; now enjoyed worldwide)",
        "ingredients": ["wonton wrappers", "pork and shrimp filling", "broth", "soy sauce", "ginger", "green onion", "sesame oil"],
    },
    "Spring Rolls": {
        "origin": "China (also eaten throughout Southeast and East Asia)",
        "ingredients": ["pastry wrapper", "cabbage", "carrots", "bean sprouts", "mushrooms", "pork or shrimp", "oil"],
    },
    "Egg Fried Rice": {
        "origin": "China (now enjoyed worldwide)",
        "ingredients": ["cooked rice", "eggs", "soy sauce", "green onion", "oil", "garlic", "mixed vegetables"],
    },
    "Sesame Chicken": {
        "origin": "USA (Chinese-American; popular worldwide)",
        "ingredients": ["chicken", "sesame seeds", "soy sauce", "honey", "rice vinegar", "garlic", "ginger"],
    },
    "Chow Mein": {
        "origin": "China (popularized in the USA as Chinese-American)",
        "ingredients": ["egg noodles", "vegetables", "soy sauce", "oyster sauce", "sesame oil", "garlic", "chicken or beef"],
    },
    "Pork Bao": {
        "origin": "China (eaten throughout Asia)",
        "ingredients": ["flour", "pork filling", "yeast", "sugar", "soy sauce", "hoisin", "sesame oil"],
    },
    "Xiaolongbao": {
        "origin": "China (Shanghai)",
        "ingredients": ["thin dough wrappers", "pork filling", "pork gelatin broth", "ginger", "soy sauce", "vinegar", "sesame oil"],
    },
    "Dan Dan Noodles": {
        "origin": "China (Sichuan)",
        "ingredients": ["noodles", "ground pork", "chili oil", "sesame paste", "Sichuan pepper", "soy sauce", "green onion"],
    },
    "Congee": {
        "origin": "China (also eaten throughout East and Southeast Asia)",
        "ingredients": ["rice", "water or broth", "ginger", "soy sauce", "green onion", "sesame oil", "toppings"],
    },

    # ── Mexican ──────────────────────────────────────────────────────────────
    "Enchiladas": {
        "origin": "Mexico (also popular throughout the USA)",
        "ingredients": ["corn tortillas", "meat or cheese", "enchilada sauce", "cheese", "sour cream", "onion", "cilantro"],
    },
    "Tamales": {
        "origin": "Mexico (also eaten throughout Latin America)",
        "ingredients": ["masa dough", "pork or chicken filling", "dried corn husks", "chili sauce", "lard"],
    },
    "Quesadilla": {
        "origin": "Mexico (now enjoyed worldwide)",
        "ingredients": ["flour or corn tortilla", "cheese", "meat or vegetables", "salsa", "sour cream", "jalapeño"],
    },
    "Guacamole": {
        "origin": "Mexico (now enjoyed worldwide)",
        "ingredients": ["avocados", "lime", "cilantro", "onion", "jalapeño", "tomato", "salt"],
    },
    "Pozole": {
        "origin": "Mexico",
        "ingredients": ["hominy", "pork", "dried chilies", "garlic", "onion", "oregano", "lime"],
    },
    "Chiles Rellenos": {
        "origin": "Mexico",
        "ingredients": ["poblano peppers", "cheese or meat filling", "eggs", "flour", "tomato sauce", "oil"],
    },
    "Carnitas": {
        "origin": "Mexico (Michoacán)",
        "ingredients": ["pork shoulder", "lard", "orange juice", "garlic", "cumin", "bay leaves", "salt"],
    },
    "Chilaquiles": {
        "origin": "Mexico",
        "ingredients": ["tortilla chips", "salsa verde or roja", "eggs", "sour cream", "cheese", "onion", "cilantro"],
    },
    "Mole Chicken": {
        "origin": "Mexico (Oaxaca and Puebla)",
        "ingredients": ["chicken", "dried chilies", "chocolate", "tomatoes", "onion", "garlic", "sesame seeds"],
    },
    "Huevos Rancheros": {
        "origin": "Mexico (also popular throughout the USA)",
        "ingredients": ["eggs", "corn tortillas", "tomato salsa", "black beans", "cheese", "jalapeño", "cilantro"],
    },
    "Elote": {
        "origin": "Mexico (also eaten throughout Latin America)",
        "ingredients": ["corn on the cob", "mayonnaise", "chili powder", "lime", "cotija cheese", "butter"],
    },

    # ── Indian ───────────────────────────────────────────────────────────────
    "Butter Chicken": {
        "origin": "India (Delhi; now enjoyed worldwide)",
        "ingredients": ["chicken", "butter", "tomato sauce", "cream", "onion", "garlic", "ginger"],
    },
    "Chicken Tikka Masala": {
        "origin": "UK/India (origin debated; hugely popular in the UK and worldwide)",
        "ingredients": ["chicken", "tomato sauce", "cream", "onion", "garlic", "ginger", "tikka masala spices"],
    },
    "Biryani": {
        "origin": "India (also eaten throughout Pakistan and the Middle East)",
        "ingredients": ["basmati rice", "meat", "saffron", "onion", "yogurt", "whole spices", "ghee"],
    },
    "Samosa": {
        "origin": "India (also eaten throughout South Asia and the Middle East)",
        "ingredients": ["pastry dough", "potatoes", "peas", "cumin", "cilantro", "onion", "oil"],
    },
    "Dal": {
        "origin": "India (staple throughout South Asia)",
        "ingredients": ["lentils", "onion", "tomatoes", "garlic", "ginger", "cumin", "turmeric"],
    },
    "Tandoori Chicken": {
        "origin": "India/Pakistan (now enjoyed worldwide)",
        "ingredients": ["chicken", "yogurt", "tandoori spices", "lemon", "ginger", "garlic", "oil"],
    },
    "Palak Paneer": {
        "origin": "India",
        "ingredients": ["spinach", "paneer", "cream", "onion", "garlic", "ginger", "spices"],
    },
    "Chana Masala": {
        "origin": "India (popular throughout South Asia)",
        "ingredients": ["chickpeas", "tomatoes", "onion", "garlic", "ginger", "cumin", "cilantro"],
    },
    "Aloo Gobi": {
        "origin": "India (popular throughout South Asia)",
        "ingredients": ["potatoes", "cauliflower", "onion", "tomatoes", "turmeric", "cumin", "garam masala"],
    },
    "Korma": {
        "origin": "India/Pakistan (Mughal cuisine; now enjoyed worldwide)",
        "ingredients": ["chicken or lamb", "yogurt", "cream", "onion", "cashews", "coconut", "spices"],
    },
    "Dosa": {
        "origin": "India (South India)",
        "ingredients": ["fermented rice batter", "urad dal", "fenugreek", "oil", "potato filling", "sambar", "coconut chutney"],
    },
    "Lamb Rogan Josh": {
        "origin": "India (Kashmir)",
        "ingredients": ["lamb", "tomatoes", "onion", "yogurt", "Kashmiri chilies", "garlic", "ginger"],
    },
    "Gulab Jamun": {
        "origin": "India (also enjoyed throughout South Asia and the Middle East)",
        "ingredients": ["milk solids or khoya", "flour", "ghee", "sugar syrup", "rose water", "cardamom"],
    },

    # ── Greek / Mediterranean ────────────────────────────────────────────────
    "Moussaka": {
        "origin": "Greece (also popular in the Middle East and Balkans)",
        "ingredients": ["eggplant", "ground lamb", "tomatoes", "béchamel", "onion", "cinnamon", "Parmesan"],
    },
    "Spanakopita": {
        "origin": "Greece",
        "ingredients": ["phyllo pastry", "spinach", "feta", "eggs", "onion", "olive oil", "dill"],
    },
    "Gyros": {
        "origin": "Greece (now enjoyed worldwide)",
        "ingredients": ["pork or chicken", "pita bread", "tzatziki", "tomato", "onion", "paprika"],
    },
    "Souvlaki": {
        "origin": "Greece",
        "ingredients": ["pork or chicken skewers", "olive oil", "lemon", "garlic", "oregano", "pita"],
    },
    "Baklava": {
        "origin": "Turkey/Greece/Levant (origin disputed; enjoyed throughout the Mediterranean and Middle East)",
        "ingredients": ["phyllo pastry", "walnuts or pistachios", "honey", "butter", "cinnamon", "sugar syrup"],
    },
    "Falafel": {
        "origin": "Middle East — Egypt/Israel/Lebanon (now enjoyed worldwide)",
        "ingredients": ["chickpeas or fava beans", "herbs", "garlic", "onion", "cumin", "oil", "parsley"],
    },
    "Hummus": {
        "origin": "Middle East — Lebanon/Israel/Palestine (now enjoyed worldwide)",
        "ingredients": ["chickpeas", "tahini", "lemon", "garlic", "olive oil", "salt", "cumin"],
    },
    "Shawarma": {
        "origin": "Middle East — Syria/Lebanon (now enjoyed worldwide)",
        "ingredients": ["marinated meat", "flatbread", "garlic sauce", "tahini", "pickled vegetables", "tomato", "spices"],
    },
    "Kebab": {
        "origin": "Middle East/Turkey (eaten worldwide)",
        "ingredients": ["meat", "onion", "bell pepper", "olive oil", "spices", "lemon", "yogurt"],
    },
    "Dolmas": {
        "origin": "Greece/Turkey/Middle East",
        "ingredients": ["grape leaves", "rice", "ground meat", "olive oil", "lemon", "herbs", "pine nuts"],
    },
    "Greek Salad": {
        "origin": "Greece (now enjoyed worldwide)",
        "ingredients": ["tomatoes", "cucumber", "Kalamata olives", "feta", "onion", "olive oil", "oregano"],
    },

    # ── Spanish ──────────────────────────────────────────────────────────────
    "Paella": {
        "origin": "Spain (Valencia; now enjoyed worldwide)",
        "ingredients": ["Bomba rice", "saffron", "chicken or seafood", "tomatoes", "onion", "olive oil", "paprika"],
    },
    "Gazpacho": {
        "origin": "Spain (Andalusia; now enjoyed worldwide)",
        "ingredients": ["tomatoes", "cucumber", "bell pepper", "garlic", "olive oil", "sherry vinegar", "bread"],
    },
    "Tortilla Española": {
        "origin": "Spain (also popular in Latin America)",
        "ingredients": ["eggs", "potatoes", "onion", "olive oil", "salt"],
    },
    "Churros": {
        "origin": "Spain (also hugely popular in Mexico and Latin America; now enjoyed worldwide)",
        "ingredients": ["flour", "water", "oil", "sugar", "cinnamon", "chocolate dipping sauce"],
    },
    "Patatas Bravas": {
        "origin": "Spain",
        "ingredients": ["potatoes", "spicy tomato sauce or aioli", "olive oil", "paprika", "garlic"],
    },

    # ── Thai ─────────────────────────────────────────────────────────────────
    "Green Curry": {
        "origin": "Thailand (now enjoyed worldwide)",
        "ingredients": ["green curry paste", "coconut milk", "chicken or tofu", "Thai basil", "fish sauce", "eggplant", "lime"],
    },
    "Tom Yum Soup": {
        "origin": "Thailand (now enjoyed worldwide)",
        "ingredients": ["shrimp or chicken", "lemongrass", "kaffir lime leaves", "galangal", "mushrooms", "fish sauce", "chili"],
    },
    "Som Tam": {
        "origin": "Thailand (also eaten throughout Southeast Asia)",
        "ingredients": ["green papaya", "tomatoes", "green beans", "peanuts", "fish sauce", "lime", "chili"],
    },
    "Massaman Curry": {
        "origin": "Thailand (influenced by Persian/Muslim traders)",
        "ingredients": ["beef or chicken", "coconut milk", "potatoes", "peanuts", "Massaman paste", "fish sauce", "palm sugar"],
    },
    "Tom Kha Gai": {
        "origin": "Thailand",
        "ingredients": ["chicken", "coconut milk", "galangal", "lemongrass", "kaffir lime leaves", "mushrooms", "fish sauce"],
    },
    "Mango Sticky Rice": {
        "origin": "Thailand (also eaten throughout Southeast Asia)",
        "ingredients": ["glutinous rice", "coconut milk", "mango", "sugar", "salt", "sesame seeds"],
    },

    # ── Vietnamese ───────────────────────────────────────────────────────────
    "Pho": {
        "origin": "Vietnam (now enjoyed worldwide)",
        "ingredients": ["rice noodles", "beef or chicken broth", "sliced beef or chicken", "star anise", "cinnamon", "ginger", "Thai basil"],
    },
    "Banh Mi": {
        "origin": "Vietnam (French colonial influence; now enjoyed worldwide)",
        "ingredients": ["baguette", "meat or pâté", "pickled daikon and carrot", "cilantro", "jalapeño", "mayonnaise"],
    },
    "Bun Bo Hue": {
        "origin": "Vietnam (Hue, Central Vietnam)",
        "ingredients": ["rice vermicelli", "beef and pork", "lemongrass broth", "shrimp paste", "chili", "herbs"],
    },
    "Vietnamese Spring Rolls": {
        "origin": "Vietnam (now enjoyed worldwide)",
        "ingredients": ["rice paper", "shrimp or pork", "vermicelli noodles", "lettuce", "fresh herbs", "hoisin or peanut sauce"],
    },

    # ── Korean ───────────────────────────────────────────────────────────────
    "Bibimbap": {
        "origin": "Korea (now enjoyed worldwide)",
        "ingredients": ["rice", "mixed vegetables", "gochujang", "fried or raw egg", "beef", "sesame oil"],
    },
    "Bulgogi": {
        "origin": "Korea (now enjoyed worldwide)",
        "ingredients": ["beef", "soy sauce", "sesame oil", "garlic", "ginger", "sugar", "green onion"],
    },
    "Tteokbokki": {
        "origin": "Korea",
        "ingredients": ["rice cakes", "gochujang", "fish cakes", "green onion", "sugar", "broth"],
    },
    "Korean Fried Chicken": {
        "origin": "Korea (now enjoyed worldwide)",
        "ingredients": ["chicken", "soy sauce", "garlic", "ginger", "gochujang", "honey", "potato starch"],
    },
    "Japchae": {
        "origin": "Korea (now enjoyed worldwide)",
        "ingredients": ["glass noodles", "beef", "mixed vegetables", "soy sauce", "sesame oil", "sugar", "garlic"],
    },
    "Korean BBQ": {
        "origin": "Korea (now enjoyed worldwide)",
        "ingredients": ["beef short ribs or pork belly", "soy sauce", "garlic", "sesame oil", "gochujang", "lettuce wraps"],
    },

    # ── German / Central European ────────────────────────────────────────────
    "Bratwurst": {
        "origin": "Germany (also popular throughout Central Europe)",
        "ingredients": ["pork or veal", "spices", "natural casing", "salt", "beer (for serving)", "mustard"],
    },
    "Schnitzel": {
        "origin": "Austria (now enjoyed worldwide, especially in Germany and Central Europe)",
        "ingredients": ["veal or pork", "breadcrumbs", "eggs", "flour", "oil", "lemon", "butter"],
    },
    "Pretzel": {
        "origin": "Germany/Austria (now enjoyed worldwide)",
        "ingredients": ["flour", "water", "yeast", "baking soda", "butter", "salt"],
    },
    "Goulash": {
        "origin": "Hungary (also popular throughout Central Europe)",
        "ingredients": ["beef", "onion", "paprika", "tomatoes", "carrots", "potatoes", "sour cream"],
    },
    "Black Forest Cake": {
        "origin": "Germany (now enjoyed worldwide)",
        "ingredients": ["chocolate sponge", "whipped cream", "cherries", "kirsch", "sugar", "chocolate shavings"],
    },
    "Apple Strudel": {
        "origin": "Austria (also popular throughout Central and Eastern Europe)",
        "ingredients": ["strudel pastry", "apples", "sugar", "cinnamon", "raisins", "breadcrumbs", "butter"],
    },
    "Paprikash": {
        "origin": "Hungary",
        "ingredients": ["chicken", "onion", "paprika", "sour cream", "tomatoes", "pepper", "flour"],
    },

    # ── Eastern European ─────────────────────────────────────────────────────
    "Borscht": {
        "origin": "Ukraine (also popular throughout Eastern Europe and Russia)",
        "ingredients": ["beets", "cabbage", "potatoes", "carrots", "onion", "beef broth", "sour cream"],
    },
    "Beef Stroganoff": {
        "origin": "Russia (now enjoyed worldwide)",
        "ingredients": ["beef strips", "mushrooms", "sour cream", "onion", "butter", "beef broth", "mustard"],
    },
    "Pierogies": {
        "origin": "Poland (also popular throughout Eastern Europe)",
        "ingredients": ["dough", "potato and cheese filling", "onion", "butter", "sour cream"],
    },
    "Blini": {
        "origin": "Russia (also eaten throughout Eastern Europe)",
        "ingredients": ["buckwheat or wheat flour", "eggs", "milk", "butter", "yeast", "sour cream", "caviar or smoked salmon"],
    },
    "Pelmeni": {
        "origin": "Russia",
        "ingredients": ["dough", "pork and beef filling", "onion", "garlic", "black pepper", "butter", "sour cream"],
    },

    # ── Turkish ──────────────────────────────────────────────────────────────
    "Doner Kebab": {
        "origin": "Turkey (now enjoyed worldwide)",
        "ingredients": ["lamb or beef or chicken", "flatbread or pita", "tomato", "onion", "garlic yogurt sauce", "spices"],
    },
    "Lahmacun": {
        "origin": "Turkey/Armenia (also popular in the Levant and Middle East)",
        "ingredients": ["flatbread", "minced lamb", "tomatoes", "onion", "parsley", "spices", "lemon"],
    },
    "Börek": {
        "origin": "Turkey (also popular throughout the Balkans and Middle East)",
        "ingredients": ["phyllo pastry", "feta or meat or spinach filling", "eggs", "butter", "olive oil"],
    },

    # ── Middle Eastern ───────────────────────────────────────────────────────
    "Shakshuka": {
        "origin": "North Africa/Israel (origin disputed; popular throughout the Middle East and worldwide)",
        "ingredients": ["eggs", "tomatoes", "onion", "garlic", "cumin", "paprika", "olive oil"],
    },
    "Mansaf": {
        "origin": "Jordan (national dish)",
        "ingredients": ["lamb", "jameed (dried fermented yogurt)", "rice", "flatbread", "pine nuts", "parsley"],
    },
    "Kabsa": {
        "origin": "Saudi Arabia (popular throughout the Arabian Peninsula)",
        "ingredients": ["rice", "chicken or lamb", "tomatoes", "onion", "dried lime", "baharat spices", "nuts"],
    },
    "Knafeh": {
        "origin": "Palestine/Levant (enjoyed throughout the Middle East)",
        "ingredients": ["shredded wheat or semolina", "white Arabic cheese", "sugar syrup", "rose water", "pistachios"],
    },

    # ── Brazilian ────────────────────────────────────────────────────────────
    "Feijoada": {
        "origin": "Brazil (national dish)",
        "ingredients": ["black beans", "pork or beef cuts", "onion", "garlic", "bay leaves", "orange", "rice"],
    },
    "Churrasco": {
        "origin": "Brazil/Argentina (popular throughout Latin America)",
        "ingredients": ["beef or various meats", "rock salt", "chimichurri sauce"],
    },
    "Coxinha": {
        "origin": "Brazil",
        "ingredients": ["chicken filling", "potato and flour dough", "cream cheese", "onion", "seasoning", "breadcrumbs", "oil"],
    },
    "Brigadeiro": {
        "origin": "Brazil (now enjoyed worldwide)",
        "ingredients": ["sweetened condensed milk", "cocoa powder", "butter", "chocolate sprinkles"],
    },

    # ── African ──────────────────────────────────────────────────────────────
    "Jollof Rice": {
        "origin": "West Africa — Nigeria/Ghana/Senegal (popular throughout West Africa)",
        "ingredients": ["rice", "tomatoes", "tomato paste", "onion", "bell pepper", "chicken broth", "spices"],
    },
    "Suya": {
        "origin": "Nigeria (popular throughout West Africa)",
        "ingredients": ["beef", "yaji spice mix", "peanuts", "ginger", "garlic", "oil", "onion"],
    },
    "Tagine": {
        "origin": "Morocco (also popular throughout North Africa)",
        "ingredients": ["lamb or chicken", "vegetables", "dried fruits", "onion", "garlic", "ras el hanout", "olive oil"],
    },
    "Doro Wat": {
        "origin": "Ethiopia (national dish)",
        "ingredients": ["chicken", "berbere spice blend", "onion", "niter kibbeh (spiced butter)", "hard-boiled eggs", "garlic", "ginger"],
    },
    "Bobotie": {
        "origin": "South Africa (national dish; Dutch and Malay influences)",
        "ingredients": ["ground beef", "curry spices", "onion", "milk", "eggs", "dried fruit", "bay leaves"],
    },
    "Peri Peri Chicken": {
        "origin": "Portugal/Mozambique (popularized by Nando's worldwide)",
        "ingredients": ["chicken", "peri peri chili", "lemon", "garlic", "olive oil", "herbs", "vinegar"],
    },
    "Couscous": {
        "origin": "Morocco/North Africa (also eaten throughout the Middle East and Mediterranean)",
        "ingredients": ["semolina couscous", "vegetables", "meat", "broth", "olive oil", "ras el hanout", "herbs"],
    },

    # ── Southeast Asian ──────────────────────────────────────────────────────
    "Nasi Goreng": {
        "origin": "Indonesia (also popular throughout Southeast Asia)",
        "ingredients": ["cooked rice", "eggs", "kecap manis (sweet soy)", "shrimp paste", "chili", "garlic", "shallots"],
    },
    "Satay": {
        "origin": "Indonesia/Malaysia (popular throughout Southeast Asia and worldwide)",
        "ingredients": ["meat skewers", "peanut sauce", "lemongrass", "turmeric", "galangal", "coconut milk"],
    },
    "Adobo": {
        "origin": "Philippines (national dish)",
        "ingredients": ["pork or chicken", "vinegar", "soy sauce", "garlic", "bay leaves", "black pepper", "sugar"],
    },
    "Sinigang": {
        "origin": "Philippines",
        "ingredients": ["pork or shrimp or fish", "tamarind broth", "vegetables", "tomatoes", "onion", "fish sauce"],
    },
    "Laksa": {
        "origin": "Singapore/Malaysia",
        "ingredients": ["rice noodles", "coconut milk broth", "shrimp or chicken", "tofu puffs", "bean sprouts", "sambal", "laksa paste"],
    },
    "Rendang": {
        "origin": "Indonesia/Malaysia (Minangkabau origin; popular throughout Southeast Asia)",
        "ingredients": ["beef", "coconut milk", "lemongrass", "galangal", "turmeric", "chilies", "kaffir lime leaves"],
    },
    "Hainanese Chicken Rice": {
        "origin": "Singapore/Malaysia (originally from Hainan, China; national dish of Singapore)",
        "ingredients": ["poached chicken", "rice cooked in chicken broth", "chicken fat", "ginger sauce", "chili sauce", "soy sauce"],
    },

    # ── British / Irish ──────────────────────────────────────────────────────
    "Shepherd's Pie": {
        "origin": "UK/Ireland (also popular in Australia and New Zealand)",
        "ingredients": ["lamb or beef", "mashed potatoes", "onion", "carrots", "peas", "beef broth", "Worcestershire"],
    },
    "Bangers and Mash": {
        "origin": "UK",
        "ingredients": ["pork sausages", "mashed potatoes", "onion gravy", "butter", "milk", "mustard"],
    },
    "Full English Breakfast": {
        "origin": "UK (also popular in Ireland and throughout the Commonwealth)",
        "ingredients": ["bacon", "eggs", "sausages", "baked beans", "tomatoes", "mushrooms", "toast"],
    },
    "Scones": {
        "origin": "UK/Ireland (popular throughout the Commonwealth)",
        "ingredients": ["flour", "butter", "sugar", "baking powder", "milk", "clotted cream", "jam"],
    },
    "Sticky Toffee Pudding": {
        "origin": "UK",
        "ingredients": ["dates", "butter", "brown sugar", "eggs", "flour", "toffee sauce", "cream"],
    },
    "Yorkshire Pudding": {
        "origin": "UK (England)",
        "ingredients": ["flour", "eggs", "milk", "beef drippings or oil", "salt"],
    },
    "Beef Wellington": {
        "origin": "UK (now enjoyed worldwide)",
        "ingredients": ["beef tenderloin", "pâté", "mushroom duxelles", "puff pastry", "Dijon mustard", "egg wash"],
    },
    "Scotch Eggs": {
        "origin": "UK",
        "ingredients": ["hard-boiled eggs", "sausage meat", "breadcrumbs", "flour", "oil", "mustard"],
    },

    # ── Caribbean / Latin American ───────────────────────────────────────────
    "Jerk Chicken": {
        "origin": "Jamaica (now enjoyed worldwide)",
        "ingredients": ["chicken", "jerk seasoning", "scotch bonnet peppers", "thyme", "allspice", "garlic", "soy sauce"],
    },
    "Ropa Vieja": {
        "origin": "Cuba (also popular throughout the Caribbean)",
        "ingredients": ["shredded beef", "tomatoes", "bell peppers", "onion", "garlic", "olive oil", "spices"],
    },
    "Mofongo": {
        "origin": "Puerto Rico",
        "ingredients": ["fried plantains", "garlic", "pork cracklings", "olive oil", "broth", "salt"],
    },
    "Ackee and Saltfish": {
        "origin": "Jamaica (national dish)",
        "ingredients": ["ackee fruit", "salt cod", "onion", "tomatoes", "thyme", "scotch bonnet pepper", "bell peppers"],
    },
    "Empanadas": {
        "origin": "Argentina/Colombia/Chile/Spain (eaten throughout Latin America and Spain)",
        "ingredients": ["pastry dough", "beef or chicken or cheese filling", "onion", "egg wash", "spices"],
    },
    "Ceviche": {
        "origin": "Peru (also popular throughout Latin America)",
        "ingredients": ["raw fish", "lime juice", "onion", "cilantro", "aji amarillo or chili", "salt", "sweet potato"],
    },
    "Arepa": {
        "origin": "Colombia/Venezuela (eaten throughout Latin America)",
        "ingredients": ["ground cornmeal", "water", "salt", "cheese or meat filling", "butter or oil"],
    },
    "Lomo Saltado": {
        "origin": "Peru (Chinese-Peruvian fusion)",
        "ingredients": ["beef strips", "soy sauce", "tomatoes", "onion", "aji amarillo", "French fries", "rice"],
    },

    # ── Caucasus / Georgian ──────────────────────────────────────────────────
    "Khachapuri": {
        "origin": "Georgia (national dish)",
        "ingredients": ["bread dough", "sulguni or Georgian cheese", "eggs", "butter"],
    },
    "Khinkali": {
        "origin": "Georgia",
        "ingredients": ["dough", "spiced meat filling", "onion", "garlic", "coriander", "chili", "broth (inside)"],
    },

    # ── Rounding out to 250 ──────────────────────────────────────────────────
    "Chocolate Chip Cookies": {
        "origin": "USA (Toll House, MA; now enjoyed worldwide)",
        "ingredients": ["flour", "butter", "sugar", "brown sugar", "eggs", "chocolate chips", "vanilla"],
    },
    "Pigs in a Blanket": {
        "origin": "USA/UK (now enjoyed worldwide)",
        "ingredients": ["mini hot dogs or sausages", "crescent roll dough", "mustard", "cheese"],
    },
    "Saltimbocca": {
        "origin": "Italy (Rome)",
        "ingredients": ["veal", "prosciutto", "sage", "white wine", "butter", "olive oil", "salt"],
    },
    "Penne Arrabbiata": {
        "origin": "Italy (Rome)",
        "ingredients": ["penne pasta", "tomatoes", "garlic", "red chili flakes", "olive oil", "parsley", "salt"],
    },
    "Unagi Don": {
        "origin": "Japan",
        "ingredients": ["grilled eel", "steamed rice", "unagi sauce (tare)", "mirin", "sake", "soy sauce", "sugar"],
    },
    "Braised Pork Belly": {
        "origin": "China (also popular throughout East Asia)",
        "ingredients": ["pork belly", "soy sauce", "Shaoxing rice wine", "sugar", "garlic", "ginger", "star anise"],
    },
    "Chole Bhature": {
        "origin": "India (North India, especially Punjab and Delhi)",
        "ingredients": ["chickpeas", "fried leavened bread (bhatura)", "flour", "yogurt", "oil", "onion and tomato gravy", "spices"],
    },
    "Steak Tartare": {
        "origin": "France (Belgium also claims origin; popular in European fine dining)",
        "ingredients": ["raw beef", "capers", "onion", "egg yolk", "Dijon mustard", "Worcestershire sauce", "Tabasco"],
    },
    "Eggs Florentine": {
        "origin": "France/USA (variant of Eggs Benedict with Florentine influence)",
        "ingredients": ["English muffin", "spinach", "poached eggs", "hollandaise sauce", "butter", "lemon"],
    },
    "Croque Madame": {
        "origin": "France",
        "ingredients": ["bread", "ham", "Gruyère", "béchamel sauce", "fried egg", "butter"],
    },
    "Harissa Chicken": {
        "origin": "North Africa — Tunisia/Morocco (also popular throughout the Middle East)",
        "ingredients": ["chicken", "harissa paste", "garlic", "lemon", "olive oil", "cumin", "yogurt"],
    },
    "Bigos": {
        "origin": "Poland (national dish; also eaten in Lithuania and Belarus)",
        "ingredients": ["sauerkraut", "fresh cabbage", "various meats", "onion", "mushrooms", "bay leaves", "allspice"],
    },
    "Jamaican Patty": {
        "origin": "Jamaica (popular throughout the Caribbean and Jamaican diaspora worldwide)",
        "ingredients": ["pastry dough", "ground beef", "scotch bonnet pepper", "onion", "thyme", "turmeric", "breadcrumbs"],
    },
    "Chili Con Carne": {
        "origin": "USA — Tex-Mex (now enjoyed worldwide)",
        "ingredients": ["beef", "kidney beans", "tomatoes", "chili powder", "onion", "garlic", "cumin"],
    },
}

assert len(FOOD_DATA) == 250, f"Expected 250 entries, got {len(FOOD_DATA)}"
