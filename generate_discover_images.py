import urllib.request
import urllib.error
import json
import base64
import os
import time

API_KEY = "AIzaSyC9gPrPdX6KCaeVqU6GYpo0zv9I5MwpTCE"
API_URL = f"https://generativelanguage.googleapis.com/v1beta/models/imagen-4.0-generate-001:predict?key={API_KEY}"
OUTPUT_DIR = "/Users/traviswilcox/Schemester/assets/discover"

IMAGES = [
    # Trending in London
    ("thames-cruise",        "Thames River sunset cruise, golden hour, luxury boat on the River Thames with iconic London skyline, warm golden reflections on water, cinematic photography"),
    ("rooftop-cocktails",    "Rooftop cocktail masterclass in London, stylish rooftop bar with city views at sunset, bartender mixing drinks, modern atmosphere"),
    ("street-food-london",   "Vibrant London street food market, colourful food stalls, multicultural crowd eating outdoors, Borough Market atmosphere"),
    ("tower-bridge",         "Tower Bridge photography walk at golden hour, iconic London landmark reflected in the Thames, dramatic sky"),
    ("eastlondon-graffiti",  "East London Shoreditch street art graffiti tour, huge colourful murals on brick walls, urban art scene"),

    # Nearby Fun Activities
    ("axe-throwing",         "Indoor axe throwing session, person throwing axe at wooden target, dramatic action shot, dark industrial venue"),
    ("escape-room-heist",    "Escape room heist theme, mysterious dimly lit room with safes locks and clues, puzzle solving atmosphere"),
    ("pottery-wheel",        "Pottery wheel workshop, close-up of hands shaping wet clay on spinning wheel, creative studio with natural light"),
    ("kayaking-thames",      "Kayaking on the River Thames in London, paddler with Tower Bridge in background, sunny day, active outdoor adventure"),
    ("bouldering-climbing",  "Indoor bouldering climbing wall with colourful holds, athlete climbing, beginner session, modern climbing gym"),

    # Live Music
    ("jazz-ronnies",         "Intimate jazz club performance, saxophone player on stage under warm spotlight, atmospheric low lighting, audience in foreground"),
    ("rock-o2-academy",      "Rock concert at O2 Academy Brixton, energetic band on stage with dramatic light show, crowd with raised hands"),
    ("royal-albert-hall",    "Classical music concert at Royal Albert Hall London, grand ornate interior, full orchestra on stage, sweeping view from balcony"),
    ("blues-soul-bar",       "Blues and soul live music night, soulful female singer at microphone on stage, intimate bar venue, warm amber lighting"),
    ("indie-moth-club",      "Indie band performing at intimate music venue, moody stage lighting, young crowd, raw energetic atmosphere"),

    # Restaurants
    ("brat-restaurant",      "Wood-fired restaurant in Shoreditch London, rustic exposed brick interior, beautifully plated charred fish dish, open kitchen with fire"),
    ("dishoom-london",       "Dishoom Bombay cafe London, warm dimly lit restaurant interior with ceiling fans and antique decor, black daal and chai"),
    ("gymkhana-mayfair",     "Gymkhana Indian fine dining restaurant Mayfair London, elegant colonial-era interior, beautifully presented modern Indian dish"),
    ("sketch-london",        "Sketch restaurant London, iconic pink egg pod dining room, surreal whimsical decor, contemporary British fine dining"),
    ("clove-club",           "The Clove Club Shoreditch restaurant, minimalist Scandi interior, exquisite multi-course tasting menu dish, precise plating"),

    # Bars
    ("nightjar-bar",         "Nightjar speakeasy cocktail bar Shoreditch, dark moody 1920s interior, elaborate hand-crafted cocktail with dramatic garnish"),
    ("lyaness-southbank",    "Lyaness cocktail bar at Sea Containers London, stylish modern interior with river views, artistic avant-garde cocktail"),
    ("satans-whiskers",      "Cosy neighbourhood cocktail bar in Bethnal Green, warm intimate atmosphere, negroni on bar top, local regulars"),
    ("artesian-langham",     "Artesian bar at The Langham hotel London, luxurious grand interior with chandelier, elegant waiter presenting cocktail"),
    ("trailer-happiness-tiki","Tropical tiki bar in Notting Hill, vibrant bamboo and island decor, elaborate tiki cocktail with tropical garnishes and umbrellas"),

    # Comedy Nights
    ("comedy-store-london",  "The Comedy Store London stand-up comedy show, comedian on stage with spotlight, packed audience laughing, iconic comedy club"),
    ("soho-theatre-comedy",  "Soho Theatre comedy night London, black box theatre, performer on small stage, intimate audience, theatrical lighting"),
    ("up-the-creek",         "Open mic comedy night at small comedy club, nervous comedian at microphone, small intimate crowd, brick wall backdrop"),
    ("banana-cabaret",       "Comedy cabaret show in Clapham London, colourful stage, energetic comedian performing, audience in hysterics"),
    ("angel-comedy-club",    "Free comedy club night in Islington London, laid-back pub venue atmosphere, stand-up comedian performing, friendly crowd"),

    # Experiences
    ("private-chef-dinner",  "Private chef dinner experience at elegant home, professional chef plating exquisite dish at beautifully set candlelit dining table"),
    ("helicopter-city-tour", "Helicopter tour over London at golden hour, aerial view of River Thames, Tower Bridge and city skyline from cockpit window"),
    ("foraging-wild-cooking","Foraging and wild cooking experience in Surrey Hills countryside, chef showing foraged mushrooms and herbs in forest clearing"),
    ("chocolate-masterclass","Artisan chocolate making masterclass, hands tempering dark chocolate, moulds being filled, luxury chocolatier workshop"),
    ("hot-air-balloon-sunrise","Hot air balloon flight at sunrise, view from basket of patchwork English countryside below, golden pink dawn sky, magical"),

    # Date Activities
    ("sunset-picnic-hyde-park","Romantic sunset picnic in Hyde Park London, elegant spread of food wine and flowers on a blanket, golden hour light"),
    ("wine-tasting-two",     "Wine tasting for two at Borough Market London, sommelier pouring red wine, rustic wine cellar setting, intimate couple experience"),
    ("life-drawing-class",   "Life drawing art class in Hackney studio, artists sketching with charcoal, creative workshop atmosphere, artistic nude figure on podium"),
    ("couples-pottery-workshop","Couples pottery workshop in Peckham studio, man and woman laughing while shaping clay together on wheel, romantic creative date"),
    ("secret-cinema-experience","Secret Cinema immersive experience, guests in elaborate period costumes walking through a cinematic movie set, magical atmosphere"),
]

def generate_image(name, prompt):
    out_path = os.path.join(OUTPUT_DIR, f"{name}.jpg")
    if os.path.exists(out_path):
        print(f"  skipping {name}.jpg (already exists)")
        return True

    data = json.dumps({
        "instances": [{"prompt": prompt}],
        "parameters": {"sampleCount": 1, "aspectRatio": "4:3"}
    }).encode()

    req = urllib.request.Request(
        API_URL, data=data,
        headers={"Content-Type": "application/json"}
    )

    try:
        with urllib.request.urlopen(req, timeout=60) as resp:
            result = json.loads(resp.read())
        b64 = result["predictions"][0]["bytesBase64Encoded"]
        with open(out_path, "wb") as f:
            f.write(base64.b64decode(b64))
        print(f"  ✓ {name}.jpg")
        return True
    except urllib.error.HTTPError as e:
        body = e.read().decode()
        print(f"  ✗ {name} — HTTP {e.code}: {body[:200]}")
        return False
    except Exception as e:
        print(f"  ✗ {name} — {e}")
        return False

if __name__ == "__main__":
    print(f"Generating {len(IMAGES)} images into {OUTPUT_DIR}\n")
    ok = 0
    for i, (name, prompt) in enumerate(IMAGES, 1):
        print(f"[{i}/{len(IMAGES)}] {name}")
        if generate_image(name, prompt):
            ok += 1
        if i < len(IMAGES):
            time.sleep(1.5)
    print(f"\nDone — {ok}/{len(IMAGES)} images saved.")
