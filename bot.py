
import discord
from discord.ext import commands, tasks
from discord import app_commands
from discord.ui import View, Button, Select
from discord import Interaction
from difflib import get_close_matches
import json, os, re, asyncio, time, random, logging, sys, uuid, csv, hashlib
from datetime import datetime, timedelta
from flask import Flask
from threading import Thread

app = Flask(__name__)

@app.route("/")
def home():
    return "✅ Bot is alive!"

def _run_flask():
    port = int(os.environ.get("PORT", 5000))
    app.run(host="0.0.0.0", port=port, debug=False)

def keep_alive():
    t = Thread(target=_run_flask, daemon=True)
    t.start()

# ---------- Logging setup ----------
logging.basicConfig(level=logging.INFO, format="%(asctime)s [%(levelname)s]: %(message)s")

# ---------- CONFIG (EDIT) ----------
TOKEN = os.getenv("DISCORD_TOKEN")
GUILD_ID = 1402882455056420895

COOLDOWN_FILE = "cooldowns.json"
INVITES_FILE = "invites.json"
ALLOWED_ROLE_IDS = [1402955662455214151]
ROLE_ID_TO_GIVE = 1402882455056420895
ALLOWED_EVERYONE_ROLE_IDS = [1402955662455214151]
BYPASS_ROLE_IDS = [1402955662455214151]

PUBLIC_LOG_CHANNEL_ID = 1402958307437838439
PRIVATE_LOG_CHANNEL_ID = 1402958275263205500
RECEIPT_CHANNEL_ID = PRIVATE_LOG_CHANNEL_ID

KEY_FILE = 'keys.json'
STOCK_FILE = 'stock.json'
BULK_FILE = 'bulkstock.json'

# Hardcoded stock data
HARDCODED_STOCK = {
    "bedwars": {
        "vulcan rigged": "https://www.mediafire.com/file/edhlcubvlc5b7nx/Vulcan.blend/file",
        "pyro rigged": "https://www.mediafire.com/file/i0onkrsali1nozp/PYRO_RIGGED.blend/file",
        "kaida rigged": "https://www.mediafire.com/file/i0onkrsali1nozp/PYRO_RIGGED.blend/file",
        "nahla rigged": "https://www.mediafire.com/file/1f9mtsvxps2xm6l/Nahla_Kit.blend/file",
        "warden rigged": "https://www.mediafire.com/file/dk9jakibl682rib/Warden.blend/file",
        "davey rigged": "https://www.mediafire.com/file/mvt0yc8k9mroqvd/Davey.blend/file",
        "isabel rigged": "https://www.mediafire.com/file/yqp465svjjth158/isabel.blend/file",
        "adetunde rigged": "https://www.mediafire.com/file/qo2cgmtdy1c2fw7/adetunde_rigged.blend/file",
        "triton rigged": "https://www.mediafire.com/file/e27znw25csrw0lz/Triton.blend/file",
        "aery rigged": "https://www.mediafire.com/file/aherq6faml93t46/Aery.blend/file",
        "ares rigged": "https://www.mediafire.com/file/nqdlt7mwxyt2vbz/Ares.blend/file",
        "gingerbread rigged": "https://www.mediafire.com/file/p2046oigyralh39/GingerBread.blend/file",
        "deep void barbarian rigged": "https://www.mediafire.com/file/ufewvqejshtyqxj/deep_void_barb_rigged.blend/file",
        "krystal rigged": "https://www.mediafire.com/file/9e96eay3z2syd31/Krystal_Kit.blend/file",
        "milo rigged": "https://www.mediafire.com/file/guwz5tmvngirn09/Milo_Rigged_Kit.blend/file",
        "stella rigged": "https://www.mediafire.com/file/wo7i770hwmymwyz/rigged_stella.blend/file",
        "fortuna rigged": "https://www.mediafire.com/file/w2n3aq41hs1b550/Fortuna.blend/file",
        "builder rigged": "https://www.mediafire.com/file/7pu4enlpfoqqp8o/Builder.blend/file",
        "martin rigged": "https://www.mediafire.com/file/79kiurl1emo7tcs/Martin_Kit.blend/file",
        "metal detector rigged": "https://www.mediafire.com/file/03e7vybk12lp4ks/Metal_Kit.blend/file",
        "ragnar rigged": "https://www.mediafire.com/file/t2kimvd60sif2la/Ragnar.blend/file",
        "noelle rigged": "https://www.mediafire.com/file/6q5ozh0e2ed0k1f/noelle.blend/file",
        "yuzi rigged": "https://www.mediafire.com/file/2dtir2mrkedrxj8/Yuzi.blend/file",
        "barbarian rigged": "https://www.mediafire.com/file/g0ieay0eqlu4j1j/Barbarian.blend/file",
        "sigrid rigged": "https://www.mediafire.com/file/zgwpd1ks7jw2wnq/Sigrid_Rigged.blend/file",
        "silas rigged": "https://www.mediafire.com/file/osbfqkgvd2q8dbh/Silas_Rigged.blend/file",
        "lani rigged": "https://www.mediafire.com/file/9oc15z62ivux83r/Lani.blend/file",
        "agni rigged": "https://www.mediafire.com/file/9io4bshyk4uzhbg/Agni.blend/file",
        "cyber rigged": "https://www.mediafire.com/file/839zsvpehwc0pyz/Cyber_Rigged.blend/file",
        "miner rigged": "https://www.mediafire.com/file/hb7p1s7sbcsym4x/Miner.blend/file",
        "eldric rigged": "https://www.mediafire.com/file/pqbhf0x4dhrbqs1/Eldric_Eig.blend/file",
        "lucia rigged": "https://www.mediafire.com/file/n3j0d2vacfyt76c/Lucia.blend/file",
        "nazar rigged": "https://www.mediafire.com/file/rooy8iv9ke45p65/Nazar.blend/file",
        "styx rigged": "https://www.mediafire.com/file/58q52sh9oqmoxen/Styx_Rigged.blend/file",
        "terra rigged": "https://www.mediafire.com/file/uhe3mcnergrf5fk/Terra.blend/file",
        "uma rigged": "https://www.mediafire.com/file/mbhaa8bu3o4c3yq/Uma.blend/file",
        "sheila rigged": "https://www.mediafire.com/file/tkdhr5rlf5mluah/Sheila.blend/file",
        "kaliyah rigged": "https://www.mediafire.com/file/c6z5cdvlfg8pozt/Kaliyah.blend/file",
        "whim rigged": "https://www.mediafire.com/file/ec5liwegfksqhcy/whim.blend/file",
        "yamini rigged": "https://www.mediafire.com/file/afb547wxd2gmtci/Yamini_Kit.blend/file",
        "zephyr rigged": "https://www.mediafire.com/file/opz8tdvj9mzj5c6/Zephyr.blend/file",
        "zarrah rigged": "https://www.mediafire.com/file/db9d8f6wguqv6dl/Zarrah_rigged.blend/file",
        "blossom 5v5 map": "https://www.mediafire.com/file/txru6bil95jns4s/Blosssom_5v5_%25284%2529.zip/file",
        "krampus ember rigged": "https://www.mediafire.com/file/dkqpt2b58lb25oq/krampus_ember_rigged.blend/file",
        "christmas sprirt eldric rigged": "https://www.mediafire.com/file/eougdzl4cj3d1ov/christmas_spirit_eldric_rigged.blend/file",
        "elder tree rigged": "https://www.mediafire.com/file/o7egkv7qlfjqwhj/elder_rigged2.blend/file",
        "caitlyn rigged": "https://www.mediafire.com/file/j1bunp5egvzbm6w/Caitlyn_Rigged.blend/file",
        "emerald armour rigged": "https://www.mediafire.com/file/77ebopz0nky8j1c/emerald_armour_rigged1.blend/file",
        "watergun": "https://www.mediafire.com/file/6jtndo5pvsjidei/WATERGUN.zip/file",
        "voidaxe": "https://www.mediafire.com/file/axkpml0lq81srco/void_axe.zip/file",
        "telepearl": "https://www.mediafire.com/file/anmkmbp374kzget/Telepearl.zip/file",
        "summertime marina rigged": "https://www.mediafire.com/file/cxymocrjab0qbn7/Summertime_marina_rigged2_%25281%2529.blend/file",
        "tidal wren rigged": "https://www.mediafire.com/file/im3lp68vk4s8c8z/TIDAL_WREN_RIGGED1.blend/file",
        "armor trims rigged": "https://www.mediafire.com/file/9tvz3gs49cosff8/armor+trims+rigged.blend/file",
        "trixie rigged": "https://www.mediafire.com/file/dqo5ltahcqujniq/trixie2.blend/file"
    },
    "steal a brainrot": {
        "Graipuss Medussi": "https://www.mediafire.com/file/8yr569xt5x59c3y/Graipuss_Medussi.zip/file",
        "Los Tralaleritos": "https://www.mediafire.com/file/b2jgd03xh6acxj9/Los_Tralaleritos.zip/file",
        "Karkerkar Kurkur": "https://www.mediafire.com/file/2dbk8clidldf2xs/Karkerkar_Kurkur.zip/file",
        "Los Combinasionas": "https://www.mediafire.com/file/qviyu12m8ijriwm/Los_Combinasionas.zip/file",
        "Chicleteira Bicicleteira": "https://www.mediafire.com/file/jdgb08tzbiwrhey/Chicleteira_Bicicleteira.zip/file",
        "Dragon Cannelloni": "https://www.mediafire.com/file/9m7gzhugde9n1oc/Dragon_Cannelloni.zip/file",
        "La Grande Combinasion": "https://www.mediafire.com/file/41ojt6x5kbq54cg/La_Grande_Combinasion.zip/file",
        "Agarrini la Palini": "https://www.mediafire.com/file/oztk1djo0xw7dq7/Agarrini_la_Palini.zip/file",
        "Esok Sekolah": "https://www.mediafire.com/file/7kzvk2ucqakvsr5/Esok_Sekolah.zip/file",
        "La Vacca Saturno Saturnita": "https://www.mediafire.com/file/7pdndpw18j0eba5/La_Vacca_Saturno_Saturnita.zip/file",
        "Nuclearo Dinossauro": "https://www.mediafire.com/file/qdpi8snrfmbdeae/Nuclearo_Dinossauro.zip/file",
        "Las Vaquitas Saturnitas": "https://www.mediafire.com/file/d39imnawbf8lezg/Las_Vaquitas_Saturnitas.zip/file",
        "Pot Hotspot": "https://www.mediafire.com/file/b8r4vx4cmkapyx6/Pot_Hotspot.zip/file",
        "admin luckyblock": "https://www.mediafire.com/file/wa4xhlxgs6lhsom/admin_luckyblock.zip/file",
        "empty base": "https://www.mediafire.com/file/s3737zudcwiaxjt/empty_base.zip/file",
        "fuse machine": "https://www.mediafire.com/file/l9ubvvmf95xmxmi/fuse_machine.zip/file",
        "Job Job Job Sahur": "https://www.mediafire.com/file/ek3w6cndyl768wg/Job_Job_Job_Sahur.zip/file",
        "La Supreme Combinasion": "https://www.mediafire.com/file/1ieg5715usrnqum/La_Supreme_Combinasion.zip/file",
        "Las Tralaleritas": "https://www.mediafire.com/file/0hqdzsfglu6hi4s/Las_Tralaleritas.zip/file",
        "Los Crocodillitos": "https://www.mediafire.com/file/tnl1nf6w3vukw9q/Los_Crocodillitos.zip/file",
        "Los Matteos": "https://www.mediafire.com/file/xjgp1f16m4czvys/Los_Matteos.zip/file",
        "Los orcalitos": "https://www.mediafire.com/file/l8e9yaaxtao0n5x/Los_orcalitos.zip/file",
        "Los Spyderinis": "https://www.mediafire.com/file/kqmjucds7rc8d22/Los_Spyderinis.zip/file",
        "Los Tungtungtungcitos": "https://www.mediafire.com/file/qo5yx24kf7wi0oi/Los_Tungtungtungcitos.zip/file",
        "Nooo My Hotspot": "https://www.mediafire.com/file/2ssxlsoang8tdaa/Nooo_My_Hotspot.zip/file",
        "Raccooni Jandelini": "https://www.mediafire.com/file/dipnjy0o18coj7a/Raccooni_Jandelini.zip/file",
        "steal a brainrot map": "https://www.mediafire.com/file/0vd1aqks33vu5lq/steal_a_brainrot_map_obj.zip/file"
    },
    "grow a garden": {
        "grow a garden map": "https://www.mediafire.com/file/p2h464qg28vt3tx/Grow_a_garden_map.zip/file",
        "flower seed pack": "https://www.mediafire.com/file/8ahajydgj69uei1/Flower_Seed_Pack.zip/file",
        "gourmet seed pack": "https://www.mediafire.com/file/sr7ymew0ajs6h2t/Gourmet_Seed_Pack.zip/file",
        "night premium seed pack": "https://www.mediafire.com/file/5wdypqnkmyy2tpk/Night_Premium_Seed_Pack.zip/file",
        "night seed pack": "https://www.mediafire.com/file/xogbjlv8vki63i0/Night_Seed_Pack.zip/file",
        "normal seed pack": "https://www.mediafire.com/file/m0iw3f9icdv5lxn/Normal_Seed_Pack.zip/file",
        "rainbow exotic crafters seed pack": "https://www.mediafire.com/file/1h6sm27lcy9jhon/Rainbow_Exotic_Crafters_Seed_Pack.zip/file",
        "seed sack basic": "https://www.mediafire.com/file/nqhysnb0aqhgo9d/SeedSackBasic.zip/file",
        "seed sack premium": "https://www.mediafire.com/file/3pinq2uyut2rgx9/SeedSackPremium.zip/file",
        "summer seed pack": "https://www.mediafire.com/file/wfcawccsv4k9uvz/Summer_Seed_Pack.zip/file",
        "zen seed pack": "https://www.mediafire.com/file/iplyllzd4w6chtq/Zen_Seed_Pack.zip/file",
        "ancient seed pack": "https://www.mediafire.com/file/ydppssoahi7ypvv/Ancient_Seed_Pack.zip/file",
        "corrupted zen seed pack": "https://www.mediafire.com/file/khdnk7niysd1irk/Corrupted_Zen_Seed_Pack.zip/file",
        "exotic ancient seed pack": "https://www.mediafire.com/file/rlzumpjbatsn3r3/exotic_ancient_seed_pack.zip/file",
        "exotic crafters seed pack": "https://www.mediafire.com/file/35dwxnoq5l5i75p/exotic_crafters_seed_pack.zip/file",
        "exotic flower seed pack": "https://www.mediafire.com/file/m17qa460hdb6x1k/exotic_flower_seed_pack.zip/file",
        "exotic gourmet seed pack": "https://www.mediafire.com/file/i2mmg15puafrb1g/exotic_gourmet_seed_pack.zip/file",
        "exotic summer seed pack": "https://www.mediafire.com/file/ic9l6ihbvho6dzr/exotic_summer_seed_pack.zip/file",
        "exotic zen seed pack": "https://www.mediafire.com/file/nfiyt3esokgmj76/exotic_zen_seed_pack.zip/file",
        "culinarian chest": "https://www.mediafire.com/file/vx4u6tdicv57nvw/Culinarian_Chest.zip/file",
        "kitsune chest": "https://www.mediafire.com/file/vbfjbl02vjluhnw/Kitsune_Chest.zip/file",
        "exotic kitsune chest": "https://www.mediafire.com/file/0qqgr5l9ub74ufw/Exotic_Kitsune_Chest.zip/file",
        "exotic culinarian chest": "https://www.mediafire.com/file/inpfs6nucz9ykro/Exotic_Culinarian_Chest.zip/file"
    },
    "rivals": {
        "arena": "https://www.mediafire.com/file/8jo2jo6egsnjm5z/arena.zip/file",
        "battlegrounds": "https://www.mediafire.com/file/xhdbypn1q2b8hk6/battlegrounds.zip/file",
        "big arena": "https://www.mediafire.com/file/uqadj75gd7ddirr/big_arena.zip/file",
        "big crossroads": "https://www.mediafire.com/file/1hcnxgljb4n6lit/big_crossroads.zip/file",
        "big graveyard": "https://www.mediafire.com/file/ursrlu5m1p8kru8/big_graveyard.zip/file",
        "big onyx": "https://www.mediafire.com/file/mk1d0lg7iolnxmk/big_onyx.zip/file",
        "crossroads": "https://www.mediafire.com/file/cdfr2hi2hhjdkeg/Crossroads.zip/file",
        "docks": "https://www.mediafire.com/file/w1re6v2jfl6j305/docks.zip/file",
        "legacy backrooms": "https://www.mediafire.com/file/u682yn3sdv3jjo5/legacy_backrooms.zip/file",
        "legacy crossroads": "https://www.mediafire.com/file/fn2ksiqi4m33ub9/legacy_crossroads.zip/file",
        "legacy docks": "https://www.mediafire.com/file/qlqnz3q2iemm59g/legacy_docks.zip/file",
        "legacy onyx": "https://www.mediafire.com/file/mrmldppctetrstl/legacy_onyx.zip/file",
        "legacy splash": "https://www.mediafire.com/file/aawd723t5tm5zur/legacy_splash.zip/file",
        "playground": "https://www.mediafire.com/file/bwdglove6s0h2xw/playground.zip/file",
        "shooting range": "https://www.mediafire.com/file/w8qwgfnjez1efe4/shooting_range.zip/file",
        "station": "https://www.mediafire.com/file/lb312yw0ytgse36/station.zip/file",
        "rivals rig": "https://www.mediafire.com/file/1xt6y4w86igavw0/rivals_rig.zip/file",
        "festive skin case": "https://www.mediafire.com/file/t3qh8qinrwcelol/festive_skin_case.zip/file",
        "festive wrap box": "https://www.mediafire.com/file/6ngsxb6i658lis1/festive_wrap_box.zip/file",
        "finisher pack 1": "https://www.mediafire.com/file/t89keywo2urzu1i/finisher_pack_1.zip/file",
        "finisher pack 2": "https://www.mediafire.com/file/k4kgqbwtzogxs85/finisher_pack_2.zip/file",
        "jolly chest": "https://www.mediafire.com/file/roingno24qaeggg/jolly_chest.zip/file",
        "prime weapon crate": "https://www.mediafire.com/file/64d7ai179a9aufm/prime_weapon_crate.zip/file",
        "skin case 1": "https://www.mediafire.com/file/z0bb0xiceiqjfxj/skin_case_1.zip/file",
        "skincase 2": "https://www.mediafire.com/file/i0bhqysgkxodgzl/skin_case_2.zip/file",
        "skin case 3": "https://www.mediafire.com/file/hys1saz10yn4mt2/skin_case_3.zip/file",
        "spooky skin case": "https://www.mediafire.com/file/gl71nlevvih2pjh/spooky_skin_case.zip/file",
        "standard weapon crate": "https://www.mediafire.com/file/rxihikwsfs548qs/standard_weapon_crate.zip/file",
        "weapon crate": "https://www.mediafire.com/file/7ed26l6rqazesa0/weapon_crate.zip/file",
        "wrap box 1": "https://www.mediafire.com/file/flmaoxtjjd407ln/wrap_box_1.zip/file",
        "wrap box 2": "https://www.mediafire.com/file/q6dsijlzoxkujlq/wrap_box_2.zip/file",
        "wrap box 3": "https://www.mediafire.com/file/6kvoa5rs129u7lu/wrap_box_3.zip/file",
        "philhood charm": "https://www.mediafire.com/file/7m80lhk5z6ionfl/phillhood_charm.zip/file",
        "keynade": "https://www.mediafire.com/file/p5zqmz672glwd3b/keynade.zip/file",
        "chibi shotgun charm": "https://www.mediafire.com/file/q2iqx4kgoqnh19w/chibi_shotgun_charm.zip/file",
        "chibi assault rifle charm": "https://www.mediafire.com/file/hhp6fwa6m3kgusx/chibi_assault_rifle_charm.zip/file",
        "atroix charm": "https://www.mediafire.com/file/xl2bee7w0eb5qhu/atorix_charm.zip/file"
    },
    "plants vs brainrots": {
        "67": "https://www.mediafire.com/file/lvcvb9ioqrb228t/67.zip/file",
        "garama": "https://www.mediafire.com/file/dabcd03ov5yt7ol/garama.zip/file",
        "pot hotspot": "https://www.mediafire.com/file/yu5ehc0s1ulv7z5/POT_HOTSPOT.zip/file",
        "tralalero tralala": "https://www.mediafire.com/file/x1djqgajnsyxoxq/tralalero_tralala.zip/file",
        "map": "https://www.mediafire.com/file/3varqwrb9fwiqjp/plants_vs_brainrots_map.zip/file"
    }
}
REDEEMED_FILE = 'redeemed.json'
USAGE_FILE = 'usage.json'
ACTIVITY_FILE = 'activity.json'
COUPON_FILE = 'coupons.json'
RECEIPTS_FILE = 'receipts.json'
SAVED_FILE = 'saved_baskets.json'
UPTIME_FILE = 'bot_uptime.json'  # New file to track bot uptime

MODELS_PER_PAGE = 25
MAX_RIGS = 10

# Global gamepass mapping for checkout links (price -> url)
GAMEPASSES = {
    49: "https://www.roblox.com/game-pass/1393138833/49",
    98: "https://www.roblox.com/game-pass/1371009477/98",
    132: "https://www.roblox.com/game-pass/1367604830/132",
    176: "https://www.roblox.com/game-pass/1332664325/176",
    220: "https://www.roblox.com/game-pass/1452698336/220",
    264: "https://www.roblox.com/game-pass/1452508323/264",
    308: "https://www.roblox.com/game-pass/1452918285/308",
    352: "https://www.roblox.com/game-pass/1452346140/352",
    396: "https://www.roblox.com/game-pass/1452796283/396",
    441: "https://www.roblox.com/game-pass/1452150156/441"
}

# ---------- Regex & Intents ----------
INVITE_REGEX = re.compile(r"(?:https?://)?(?:www\.)?(?:discord\.gg|discordapp\.com/invite|discord.com/invite)/\S+", re.IGNORECASE)

intents = discord.Intents.default()
intents.message_content = True
intents.members = True
intents.guilds = True
intents.messages = True
intents.reactions = True

bot = commands.Bot(command_prefix="?", intents=intents)
bot.remove_command("help")
tree = bot.tree

# ---------- Bot uptime tracking ----------
bot_start_time = None
total_uptime_seconds = 0

def load_uptime_data():
    """Load bot uptime data from file"""
    global total_uptime_seconds
    if os.path.exists(UPTIME_FILE):
        try:
            with open(UPTIME_FILE, "r") as f:
                data = json.load(f)
                total_uptime_seconds = data.get("total_uptime_seconds", 0)
        except:
            total_uptime_seconds = 0
    else:
        total_uptime_seconds = 0

def save_uptime_data():
    """Save bot uptime data to file"""
    global bot_start_time, total_uptime_seconds
    if bot_start_time:
        current_session_time = (datetime.utcnow() - bot_start_time).total_seconds()
        total_session_uptime = total_uptime_seconds + current_session_time
    else:
        total_session_uptime = total_uptime_seconds

    data = {
        "total_uptime_seconds": total_session_uptime,
        "last_shutdown": datetime.utcnow().isoformat()
    }
    with open(UPTIME_FILE, "w") as f:
        json.dump(data, f, indent=4)

def get_current_uptime_seconds():
    """Get total uptime including current session"""
    global bot_start_time, total_uptime_seconds
    if bot_start_time:
        current_session_time = (datetime.utcnow() - bot_start_time).total_seconds()
        return total_uptime_seconds + current_session_time
    return total_uptime_seconds

# ---------- JSON helpers ----------
def ensure_file(path, default=None):
    if not os.path.exists(path):
        with open(path, "w", encoding="utf-8") as f:
            json.dump(default if default is not None else {}, f, indent=4)

def load_json(path):
    ensure_file(path)
    with open(path, "r", encoding="utf-8") as f:
        try:
            return json.load(f)
        except json.JSONDecodeError:
            return {}

def save_json(path, data):
    with open(path, "w", encoding="utf-8") as f:
        json.dump(data, f, indent=4)

def load_redeemed():
    return load_json(REDEEMED_FILE)

def save_redeemed(data):
    save_json(REDEEMED_FILE, data)

def load_coupons():
    ensure_file(COUPON_FILE, {})
    data = load_json(COUPON_FILE)
    return data if isinstance(data, dict) else {}

def save_coupons(data):
    save_json(COUPON_FILE, data)

def load_receipts():
    ensure_file(RECEIPTS_FILE, [])
    data = load_json(RECEIPTS_FILE)
    return data if isinstance(data, list) else []

def save_receipts(data):
    save_json(RECEIPTS_FILE, data)

def load_saved_baskets():
    return load_json(SAVED_FILE)

def save_saved_baskets(data):
    save_json(SAVED_FILE, data)

def load_activity():
    return load_json(ACTIVITY_FILE)

def save_activity(data):
    save_json(ACTIVITY_FILE, data)

def load_usage():
    return load_json(USAGE_FILE)

def save_usage(data):
    save_json(USAGE_FILE, data)

def load_invites():
    return load_json(INVITES_FILE)

def save_invites(data):
    save_json(INVITES_FILE, data)

def load_keys():
    return load_json(KEY_FILE)

def save_keys(data):
    save_json(KEY_FILE, data)

def load_stock():
    # Return hardcoded stock instead of loading from file
    return HARDCODED_STOCK

def save_stock(data):
    save_json(STOCK_FILE, data)

def load_bulk():
    return load_json(BULK_FILE)

def load_cooldowns():
    return load_json(COOLDOWN_FILE)

def save_cooldowns(data):
    save_json(COOLDOWN_FILE, data)

# ---------- Bot Configuration ----------
ai_responses_enabled = False
logged_in_users = {}  # {user_id: username} - This is now unused as the account system is removed
muted_users = set()

# ---------- New key system with offline-aware time tracking ----------
def seconds_to_duration(seconds):
    """Convert seconds to human readable duration"""
    if seconds <= 0:
        return "Expired"

    days = int(seconds // 86400)
    hours = int((seconds % 86400) // 3600)
    minutes = int((seconds % 3600) // 60)

    parts = []
    if days > 0:
        parts.append(f"{days}d")
    if hours > 0:
        parts.append(f"{hours}h")
    if minutes > 0:
        parts.append(f"{minutes}m")

    return " ".join(parts) if parts else "Less than 1m"

def update_key_times():
    """Update all key times, only counting online time"""
    current_uptime = get_current_uptime_seconds()

    # Update redeemed keys
    redeemed = load_redeemed()
    updated = False

    for uid, data in list(redeemed.items()):
        if isinstance(data, dict) and "last_online_time" in data:
            # Calculate time that passed while online
            last_check = data.get("last_online_time", current_uptime)
            time_passed = current_uptime - last_check

            # Subtract online time from remaining time
            new_remaining = data["remaining_seconds"] - time_passed

            if new_remaining <= 0:
                del redeemed[uid]
                updated = True
                logging.info(f"Removed expired access for user {uid}")
            else:
                data["remaining_seconds"] = new_remaining
                data["last_online_time"] = current_uptime
                updated = True

    if updated:
        save_redeemed(redeemed)

    # Update unredeemed keys
    keys = load_keys()
    keys_updated = False

    for key_code, key_data in list(keys.items()):
        if isinstance(key_data, dict) and "remaining_seconds" in key_data:
            last_check = key_data.get("last_online_time", current_uptime)
            time_passed = current_uptime - last_check

            new_remaining = key_data["remaining_seconds"] - time_passed

            if new_remaining <= 0:
                del keys[key_code]
                keys_updated = True
                logging.info(f"Removed expired key {key_code}")
            else:
                key_data["remaining_seconds"] = new_remaining
                key_data["last_online_time"] = current_uptime
                keys_updated = True

    if keys_updated:
        save_keys(keys)

# ---------- quick helpers ----------
def has_permission(interaction: discord.Interaction):
    if not interaction.guild:
        return False
    member = interaction.guild.get_member(interaction.user.id)
    return member and any(role.id in ALLOWED_ROLE_IDS for role in member.roles)

def is_user_muted(user_id: int) -> bool:
    """Check if user is muted from using bot commands"""
    return user_id in muted_users

def member_has_bypass(member: discord.Member):
    return any(role.id in BYPASS_ROLE_IDS for role in member.roles)

def user_has_access(user_id: int):
    """Check if user has valid access, considering only online time"""
    redeemed = load_redeemed()
    uid = str(user_id)
    if uid not in redeemed:
        return False

    # New format: store remaining seconds instead of absolute time
    remaining_data = redeemed[uid]
    if isinstance(remaining_data, str):
        # Old format - convert to new format
        try:
            expiry = datetime.fromisoformat(remaining_data)
            if datetime.utcnow() >= expiry:
                del redeemed[uid]
                save_redeemed(redeemed)
                return False
            else:
                # Convert to new format: remaining seconds
                remaining_seconds = (expiry - datetime.utcnow()).total_seconds()
                redeemed[uid] = {
                    "remaining_seconds": max(0, remaining_seconds),
                    "last_online_time": get_current_uptime_seconds()
                }
                save_redeemed(redeemed)
                return remaining_seconds > 0
        except:
            del redeemed[uid]
            save_redeemed(redeemed)
            return False

    # New format - check remaining time
    if not isinstance(remaining_data, dict):
        del redeemed[uid]
        save_redeemed(redeemed)
        return False

    remaining_seconds = remaining_data.get("remaining_seconds", 0)
    if remaining_seconds <= 0:
        del redeemed[uid]
        save_redeemed(redeemed)
        return False

    return True

def get_access_remaining_time(user_id: int):
    """Get remaining access time in seconds"""
    redeemed = load_redeemed()
    uid = str(user_id)
    if uid not in redeemed:
        return 0

    remaining_data = redeemed[uid]
    if isinstance(remaining_data, str):
        # Old format - convert
        try:
            expiry = datetime.fromisoformat(remaining_data)
            remaining = (expiry - datetime.utcnow()).total_seconds()
            return max(0, remaining)
        except:
            return 0

    if isinstance(remaining_data, dict):
        return max(0, remaining_data.get("remaining_seconds", 0))

    return 0

# ---------- Pagination for Stock View ----------
class ModelPagesView(View):
    def __init__(self, category: str, models: list):
        super().__init__(timeout=None)
        self.category = category
        self.models = models
        self.total_pages = (len(self.models) + MODELS_PER_PAGE - 1) // MODELS_PER_PAGE
        self.current_page = 0
        self.update_buttons()

    def create_embed(self) -> discord.Embed:
        start_index = self.current_page * MODELS_PER_PAGE
        end_index = start_index + MODELS_PER_PAGE
        models_on_page = self.models[start_index:end_index]

        description = "\n".join(f"`{model_name}`" for model_name in models_on_page)

        embed = discord.Embed(
            title=f"{self.category} Models",
            description=description,
            color=discord.Color.blue()
        )
        embed.set_footer(text=f"Page {self.current_page + 1}/{self.total_pages}")
        return embed

    def update_buttons(self):
        self.children[0].disabled = self.current_page == 0
        self.children[1].disabled = self.current_page >= self.total_pages - 1

    @discord.ui.button(label="Previous", style=discord.ButtonStyle.secondary)
    async def previous_page(self, interaction: Interaction, button: Button):
        if self.current_page > 0:
            self.current_page -= 1
            self.update_buttons()
            await interaction.response.edit_message(embed=self.create_embed(), view=self)
        else:
            await interaction.response.defer()

    @discord.ui.button(label="Next", style=discord.ButtonStyle.secondary)
    async def next_page(self, interaction: Interaction, button: Button):
        if self.current_page < self.total_pages - 1:
            self.current_page += 1
            self.update_buttons()
            await interaction.response.edit_message(embed=self.create_embed(), view=self)
        else:
            await interaction.response.defer()

class CategorySelect(Select):
    def __init__(self, stock):
        options = [discord.SelectOption(label=c, description=f"{len(models)} models") for c, models in stock.items()]
        super().__init__(placeholder="Select a category...", options=options, min_values=1, max_values=1)
        self.stock = stock

    async def callback(self, interaction: Interaction):
        category = self.values[0]
        models = self.stock.get(category, {})
        if not models:
            return await interaction.response.send_message("No models in this category.", ephemeral=True)

        model_names = list(models.keys())
        paginated_view = ModelPagesView(category, model_names)

        await interaction.response.send_message(embed=paginated_view.create_embed(), view=paginated_view, ephemeral=True)

class CategorySelectView(View):
    def __init__(self, stock):
        super().__init__(timeout=None)
        self.add_item(CategorySelect(stock))

# ---------- NEW: BWS Kits Dropdown ----------
BWS_KITS = list(set([
    "Isabel", "None", "Ragnar", "Random", "Marcel", "Abaddon", "Adetunde", "Arachne", "Archer", "Axolotl Amy", "Baker", "Barbarian", "Builder", "Crypt", "Cyber", "Death Adder", "Eldertree", "Eldric", "Evelyn", "Farmer Cletus", "Freiya", "Grim Reaper", "Grove", "Hannah", "Infernal Shielder", "Kaida", "Lassy", "Lyla", "Marina", "Martin", "Melody", "Milo", "Miner", "Nahla", "Nazar", "Nox", "Davey", "Ramil", "Silas", "Skoll", "Tally", "Triton", "Trixie", "Uma", "Vanessa", "Void Knight", "Vulcan", "Wren", "Yuzu", "Zarah", "Zenith", "Zeno", "Whisper", "Taliyah", "Warrior", "Bounty Hunter", "Beekeeper Beatrix", "Jade", "Raven", "Spirit Catcher", "Pyro", "Trapper", "Gompy", "Fisherman", "Jack", "Ares", "Santa", "Gingerbread Man", "Smoke", "Yeti", "Frosty", "Aery", "Metal Detector", "Alchemist", "Sheep Herder", "CrocoWolf", "Conqueror", "Nyx", "Lucia", "Merchant Marco", "Dino Tamer Dom", "Cobalt", "Star Collector Stella", "Zephyr", "Lani", "Whim", "Xu'rot", "Warden", "Kaliyah", "Drill", "Flora", "Umbra", "Caitlyn", "Ignis", "Fortuna", "Elektra", "Umeko", "Yamini", "Cogsworth", "Noelle", "Terra", "Agni", "Styx", "Nyoka", "Bekzat", "Hephaestus", "Ember", "Lumen", "Void Regent", "Sheila", "Sigrid", "Krystal"
]))

BWS_RIGS_OPTIONS = [f"{kit} rigged" for kit in BWS_KITS]

class InitialBuyKitRigsView(View):
    def __init__(self):
        super().__init__(timeout=None)

    @discord.ui.button(label="Add Kit Rigs", style=discord.ButtonStyle.primary)
    async def add_kit_rigs_button(self, interaction: Interaction, button: Button):
        await interaction.response.edit_message(
            content="Choose a BWS rigged kit to add to your basket:",
            view=BWSRigsView()
        )

class CheckoutView(View):
    def __init__(self, user_id: int):
        super().__init__(timeout=None)
        self.user_id = user_id
        self.applied_coupon = {"code": None, "amount": 0}

    def get_basket_info(self) -> tuple[list, int, bool]:
        items = baskets.get(str(self.user_id), [])
        total_price, discount = calculate_total(items)
        return items, total_price, discount

    def create_basket_embed(self) -> discord.Embed:
        items, total_price, discount = self.get_basket_info()
        embed = discord.Embed(title="Your Basket", color=discord.Color.green())
        if items:
            embed.description = "\n".join(f"- {m}" for m in items)
            embed.add_field(name="Total", value=f"{total_price} Robux", inline=True)
            if discount:
                embed.add_field(name="Discount", value="10% OFF (3+ rigs)", inline=False)
        else:
            embed.description = "Your basket is empty."
        return embed

    @discord.ui.button(label="Checkout", style=discord.ButtonStyle.success)
    async def checkout_button(self, interaction: Interaction, button: Button):
        if interaction.user.id != self.user_id:
            return await interaction.response.send_message("Not your basket.", ephemeral=True)

        items, total_price, discount = self.get_basket_info()
        if not items:
            return await interaction.response.send_message("Your basket is empty.", ephemeral=True)

        confirm_embed = discord.Embed(title="Checkout", description="\n".join(f"- {m}" for m in items), color=discord.Color.blurple())
        confirm_embed.add_field(name="Total", value=f"{total_price} Robux", inline=True)
        if discount:
            confirm_embed.add_field(name="Discount", value="10% OFF (3+ rigs)", inline=False)
        confirm_embed.set_footer(text="Use Redeem Coupon before confirming.")

        await interaction.response.edit_message(embed=confirm_embed, view=self)

    @discord.ui.button(label="Clear Basket", style=discord.ButtonStyle.danger)
    async def clear_button(self, interaction: Interaction, button: Button):
        if interaction.user.id != self.user_id:
            return await interaction.response.send_message("Not your basket.", ephemeral=True)
        baskets[str(self.user_id)] = []
        await interaction.response.edit_message(embed=self.create_basket_embed(), view=self)

    @discord.ui.button(label="Redeem Coupon", style=discord.ButtonStyle.secondary)
    async def redeem_button(self, interaction: Interaction, button: Button):
        if interaction.user.id != self.user_id:
            return await interaction.response.send_message("Not your basket.", ephemeral=True)

        class CouponModal(discord.ui.Modal, title="Enter Coupon Code"):
            code = discord.ui.TextInput(label="Coupon Code", placeholder="Enter code")
            def __init__(self, checkout_view):
                super().__init__(timeout=300)
                self.view = checkout_view

            async def on_submit(self, modal_inter: Interaction):
                coupons = load_coupons()
                entered = str(self.code.value).strip().upper()
                if entered in coupons and not coupons[entered].get("used", False):
                    self.view.applied_coupon["code"] = entered
                    self.view.applied_coupon["amount"] = coupons[entered]["amount"]
                    coupons[entered]["used"] = True
                    save_coupons(coupons)
                    await modal_inter.response.send_message(f"Coupon `{entered}` applied (-{self.view.applied_coupon['amount']} Robux).", ephemeral=True)
                else:
                    await modal_inter.response.send_message("Invalid or used coupon.", ephemeral=True)

        await interaction.response.send_modal(CouponModal(self))

    @discord.ui.button(label="Confirm", style=discord.ButtonStyle.success)
    async def confirm_button(self, interaction: Interaction, button: Button):
        if interaction.user.id != self.user_id:
            return await interaction.response.send_message("Not your basket.", ephemeral=True)

        items, total_price, discount = self.get_basket_info()
        final_price = max(total_price - self.applied_coupon["amount"], 0)

        receipt_id = generate_receipt_id()
        receipt = discord.Embed(title="Purchase Receipt", color=discord.Color.green())
        receipt.add_field(name="Receipt ID", value=f"`{receipt_id}`", inline=False)
        receipt.add_field(name="User", value=f"{interaction.user.mention}", inline=False)
        receipt.add_field(name="Models", value="\n".join(f"- {m}" for m in items), inline=False)
        receipt.add_field(name="Total Paid", value=f"**{final_price} Robux**", inline=True)

        if self.applied_coupon["code"]:
            receipt.add_field(name="Coupon", value=f"{self.applied_coupon['code']} (-{self.applied_coupon['amount']} Robux)", inline=False)
        if discount:
            receipt.add_field(name="Discount", value="10% OFF (3+ rigs)", inline=False)

        receipt.set_footer(text=f"User ID: {self.user_id}")
        receipt.timestamp = datetime.utcnow()
        receipts = load_receipts()
        receipts.append({"id": receipt_id, "user": str(self.user_id), "items": items, "total": final_price, "time": datetime.utcnow().isoformat()})
        save_receipts(receipts)

        view3 = View()
        if final_price in GAMEPASSES:
            view3.add_item(Button(label="Buy Gamepass", style=discord.ButtonStyle.link, url=GAMEPASSES[final_price]))
        log_channel = bot.get_channel(RECEIPT_CHANNEL_ID)
        if log_channel:
            await log_channel.send(embed=receipt)

        await interaction.response.edit_message(embed=receipt, view=view3)
        baskets[str(self.user_id)] = []

class BWSRigsSelect(Select):
    def __init__(self, options_list, placeholder):
        options = [
            discord.SelectOption(label=name)
            for name in options_list
        ]
        super().__init__(placeholder=placeholder, options=options)

    async def callback(self, interaction: Interaction):
        model_name = self.values[0]
        uid = str(interaction.user.id)
        current = baskets.setdefault(uid, [])
        if count_rigs(current) >= MAX_RIGS:
            return await interaction.response.send_message(f"Max {MAX_RIGS} rigs allowed.", ephemeral=True)

        current.append(model_name)

        checkout_view = CheckoutView(interaction.user.id)
        embed = checkout_view.create_basket_embed()

        await interaction.response.edit_message(
            content=None,
            embed=embed,
            view=checkout_view
        )

class BWSRigsView(View):
    def __init__(self):
        super().__init__(timeout=None)
        chunk_size = 25
        chunks = [BWS_RIGS_OPTIONS[i:i + chunk_size] for i in range(0, len(BWS_RIGS_OPTIONS), chunk_size)]

        for i, chunk in enumerate(chunks):
            placeholder = f"Select Kit (Part {i+1})" if len(chunks) > 1 else "Select a BWS Kit..."
            self.add_item(BWSRigsSelect(chunk, placeholder))

@tree.command(name="buykitrigs", description="Buy a rigged BWS kit with Robux.", guild=discord.Object(id=GUILD_ID))
async def buykitrigs_slash(interaction: discord.Interaction):
    embed = discord.Embed(title="BWS Kit Rig Shop", description="Click the button below to start shopping for BWS kit rigs.", color=discord.Color.blue())
    await interaction.response.send_message(embed=embed, view=InitialBuyKitRigsView(), ephemeral=True)

# ---------- cleanup task ----------
@tasks.loop(seconds=30)  # More frequent updates for better accuracy
async def update_key_timers():
    """Update key timers every 30 seconds when bot is online"""
    try:
        update_key_times()
        save_uptime_data()  # Save uptime data regularly
    except Exception as e:
        logging.error(f"Error updating key timers: {e}")

@update_key_timers.before_loop
async def before_update():
    await bot.wait_until_ready()

# ---------- invite cache ----------
invite_cache = {}
# ---------- baskets ----------
baskets = {}  # user_id -> list of models

# ---------- AI Response Function ----------
async def get_ai_response(message_content: str) -> str:
    """Simple AI responses - can be expanded to use real AI APIs"""
    content_lower = message_content.lower()

    # Basic responses
    if any(word in content_lower for word in ['hello', 'hi', 'hey']):
        return "Hello. How can I assist you?"
    elif any(word in content_lower for word in ['help', 'support']):
        return "Use /panel to access bot features."
    elif any(word in content_lower for word in ['thanks', 'thank you']):
        return "You're welcome."
    elif any(word in content_lower for word in ['rigs', 'models']):
        return "Check out kit rigs with /buykitrigs. BWS models available."
    elif any(word in content_lower for word in ['price', 'cost', 'robux']):
        return "Kit rigs are 49 Robux each. 10% off when you buy 3 or more."
    else:
        return "Use /panel for bot features."

# ---------- helpers for shop ----------
def generate_receipt_id():
    return f"RCPT-{datetime.utcnow().strftime('%Y%m%d-%H%M')}-{uuid.uuid4().hex[:4].upper()}"

def calculate_price(model_name: str) -> int:
    return 49 if "rig" in model_name.lower() else 45

def calculate_total(items: list) -> tuple[int, bool]:
    base_total = sum(calculate_price(m) for m in items)
    rigs_count = sum(1 for m in items if "rig" in m.lower())
    discount_applied = rigs_count >= 3
    if discount_applied:
        return int(base_total * 0.9), True
    return base_total, False

def count_rigs(items: list) -> int:
    return sum(1 for m in items if "rig" in m.lower())

# ---------- Additional basket helpers ----------
def load_saved_baskets():
    return load_json(SAVED_FILE)

def save_saved_baskets(data):
    save_json(SAVED_FILE, data)

# ---------- PANEL: Redeem Modal + View ----------
class RedeemKeyModal(discord.ui.Modal, title="Redeem Key"):
    key_input = discord.ui.TextInput(label="Enter Key", placeholder="Paste your key here", required=True, max_length=128)

    async def on_submit(self, interaction: discord.Interaction):
        key = str(self.key_input.value).strip()
        keys = load_keys()
        uid = str(interaction.user.id)

        if key in keys:
            key_data = keys[key]

            # Check if key belongs to this user (if user_id is set)
            if "user_id" in key_data and key_data["user_id"] != uid:
                return await interaction.response.send_message("This key belongs to someone else.", ephemeral=True)

            # Check if key is still valid
            remaining_seconds = key_data.get("remaining_seconds", 0)
            if remaining_seconds <= 0:
                del keys[key]
                save_keys(keys)
                return await interaction.response.send_message("This key has expired.", ephemeral=True)

            # Redeem the key
            redeemed = load_redeemed()
            current_uptime = get_current_uptime_seconds()

            # If user already has access, add time to existing access
            if uid in redeemed and isinstance(redeemed[uid], dict):
                current_remaining = redeemed[uid].get("remaining_seconds", 0)
                new_total = current_remaining + remaining_seconds
            else:
                new_total = remaining_seconds

            redeemed[uid] = {
                "remaining_seconds": new_total,
                "last_online_time": current_uptime
            }
            save_redeemed(redeemed)

            # Remove the key
            del keys[key]
            save_keys(keys)

            # Send confirmation
            duration_str = seconds_to_duration(new_total)
            pub = bot.get_channel(PUBLIC_LOG_CHANNEL_ID)
            if pub:
                e = discord.Embed(title="Key Redeemed", color=discord.Color.green(), timestamp=datetime.utcnow())
                e.add_field(name="User", value=f"{interaction.user} ({interaction.user.id})", inline=False)
                e.add_field(name="Access Duration", value=duration_str, inline=False)
                await pub.send(embed=e)

            # Give role
            try:
                role = interaction.guild.get_role(ROLE_ID_TO_GIVE)
                if role and role not in interaction.user.roles:
                    await interaction.user.add_roles(role)
            except Exception as e:
                logging.error(f"Failed to give role: {e}")

            return await interaction.response.send_message(f"Key redeemed! You have access for {duration_str}.", ephemeral=True)

        return await interaction.response.send_message("Invalid key.", ephemeral=True)

class PanelView(discord.ui.View):
    def __init__(self):
        super().__init__(timeout=None)

    @discord.ui.button(label="Redeem Key", style=discord.ButtonStyle.green, custom_id="panel:redeem")
    async def redeem_key(self, interaction: discord.Interaction, button: discord.ui.Button):
        await interaction.response.send_modal(RedeemKeyModal())

    @discord.ui.button(label="Get Role", style=discord.ButtonStyle.blurple, custom_id="panel:getrole")
    async def get_role(self, interaction: discord.Interaction, button: discord.ui.Button):
        if not user_has_access(interaction.user.id):
            return await interaction.response.send_message("You must redeem a key first.", ephemeral=True)
        guild = interaction.guild
        if not guild:
            return await interaction.response.send_message("Command must be used in a server.", ephemeral=True)
        member = guild.get_member(interaction.user.id)
        if not member:
            return await interaction.response.send_message("Unable to find you on this server.", ephemeral=True)
        role = guild.get_role(ROLE_ID_TO_GIVE)
        if not role:
            return await interaction.response.send_message("Role not found on this server.", ephemeral=True)
        if role in member.roles:
            return await interaction.response.send_message("You already have this role.", ephemeral=True)
        try:
            await member.add_roles(role)
            await interaction.response.send_message(f"Successfully gave you the {role.name} role!", ephemeral=True)
        except Exception as e:
            await interaction.response.send_message("Failed to give role.", ephemeral=True)

    @discord.ui.button(label="Check Status", style=discord.ButtonStyle.secondary, custom_id="panel:status")
    async def check_status(self, interaction: discord.Interaction, button: discord.ui.Button):
        uid = str(interaction.user.id)
        activity = load_activity()
        user_activity = activity.get(uid, {"messages": 0, "reactions": 0})

        embed = discord.Embed(title="Your Status", color=discord.Color.blue())

        if user_has_access(interaction.user.id):
            remaining_time = get_access_remaining_time(interaction.user.id)
            duration_str = seconds_to_duration(remaining_time)
            embed.add_field(name="Access", value=f"{duration_str} remaining", inline=False)
        else:
            embed.add_field(name="Access", value="No valid access", inline=False)

        embed.add_field(name="Messages Sent", value=str(user_activity["messages"]), inline=True)
        embed.add_field(name="Reactions Added", value=str(user_activity["reactions"]), inline=True)
        embed.set_footer(text="Time only counts down when bot is online")
        embed.timestamp = datetime.utcnow()

        await interaction.response.send_message(embed=embed, ephemeral=True)

# ---------- More SLASH COMMANDS ----------
@tree.command(name="panel", description="Control panel", guild=discord.Object(id=GUILD_ID))
async def panel_slash(interaction: discord.Interaction):
    if not has_permission(interaction):
        return await interaction.response.send_message("Admin only.", ephemeral=True)

    embed = discord.Embed(title="Control Panel", description="Click buttons below.", color=discord.Color.blurple())
    await interaction.response.send_message(embed=embed, view=PanelView())

@tree.command(name="genkey", description="Make keys", guild=discord.Object(id=GUILD_ID))
@app_commands.describe(
    duration_days="Days",
    duration_hours="Extra hours", 
    user="For who (optional)",
    count="How many keys"
)
async def genkey_slash(interaction: discord.Interaction, duration_days: int = 1, duration_hours: int = 0, user: discord.Member = None, count: int = 1):
    if not has_permission(interaction):
        return await interaction.response.send_message("No perms.", ephemeral=True)

    if count < 1 or count > 50:
        return await interaction.response.send_message("1-50 keys only.", ephemeral=True)

    if duration_days < 0 or duration_hours < 0:
        return await interaction.response.send_message("Can't be negative.", ephemeral=True)

    total_seconds = (duration_days * 86400) + (duration_hours * 3600)
    if total_seconds <= 0:
        return await interaction.response.send_message("Need some duration.", ephemeral=True)

    await interaction.response.defer(ephemeral=True)

    keys = load_keys()
    generated_keys = []
    current_uptime = get_current_uptime_seconds()

    for _ in range(count):
        key_code = uuid.uuid4().hex[:16].upper()
        key_data = {
            "remaining_seconds": total_seconds,
            "last_online_time": current_uptime,
            "created": datetime.utcnow().isoformat(),
            "creator": str(interaction.user.id)
        }

        if user:
            key_data["user_id"] = str(user.id)

        keys[key_code] = key_data
        generated_keys.append(key_code)

    save_keys(keys)

    duration_str = seconds_to_duration(total_seconds)
    embed = discord.Embed(title="Keys Created", color=discord.Color.green())
    embed.add_field(name="Duration", value=duration_str, inline=True)
    embed.add_field(name="Count", value=str(count), inline=True)

    if user:
        embed.add_field(name="For", value=user.mention, inline=True)

    # Send keys in DM
    keys_text = "\n".join(f"`{key}`" for key in generated_keys)

    try:
        dm_embed = discord.Embed(title="Keys", description=keys_text, color=discord.Color.green())
        dm_embed.add_field(name="Duration", value=duration_str, inline=False)
        dm_embed.set_footer(text="Keep safe")
        await interaction.user.send(embed=dm_embed)
        embed.add_field(name="Sent", value="Check DMs", inline=False)
    except:
        embed.add_field(name="Warning", value="DMs closed", inline=False)

    # Log to private channel
    log_channel = bot.get_channel(PRIVATE_LOG_CHANNEL_ID)
    if log_channel:
        log_embed = discord.Embed(title="Keys Generated", color=discord.Color.blue())
        log_embed.add_field(name="Admin", value=f"{interaction.user.mention}", inline=True)
        log_embed.add_field(name="Count", value=str(count), inline=True)
        log_embed.add_field(name="Duration", value=duration_str, inline=True)
        if user:
            log_embed.add_field(name="Assigned to", value=user.mention, inline=True)
        log_embed.timestamp = datetime.utcnow()
        await log_channel.send(embed=log_embed)

    await interaction.followup.send(embed=embed, ephemeral=True)


@tree.command(name="checkpurchase", description="Check if a Roblox user owns a gamepass", guild=discord.Object(id=GUILD_ID))
@app_commands.describe(
    user_id="Roblox user ID",
    gamepass_id="Gamepass ID to check"
)
async def checkpurchase_slash(interaction: discord.Interaction, user_id: str, gamepass_id: str):
    await interaction.response.defer(ephemeral=True)

    try:
        import aiohttp
        async with aiohttp.ClientSession() as session:
            url = f"https://inventory.roblox.com/v1/users/{user_id}/items/GamePass/{gamepass_id}"
            async with session.get(url) as resp:
                if resp.status == 200:
                    data = await resp.json()
                    owns = data.get("data", [])

                    embed = discord.Embed(
                        title="Gamepass Ownership Check",
                        color=discord.Color.green() if owns else discord.Color.red()
                    )
                    embed.add_field(name="Roblox User ID", value=user_id, inline=True)
                    embed.add_field(name="Gamepass ID", value=gamepass_id, inline=True)
                    embed.add_field(
                        name="Owns Gamepass",
                        value="✅ Yes" if owns else "❌ No",
                        inline=False
                    )
                    embed.set_footer(text=f"Checked by {interaction.user}")
                    embed.timestamp = datetime.utcnow()

                    await interaction.followup.send(embed=embed, ephemeral=True)
                else:
                    await interaction.followup.send(
                        f"Failed to check gamepass. Status code: {resp.status}",
                        ephemeral=True
                    )
    except Exception as e:
        await interaction.followup.send(f"Error checking gamepass: {str(e)}", ephemeral=True)

# Removed genauth_slash command as it was related to the account system

# ---------- Admin Commands ----------
@tree.command(name="addstock", description="Add model", guild=discord.Object(id=GUILD_ID))
@app_commands.describe(category="Category", name="Model name", link="Download link")
async def addstock_slash(interaction: discord.Interaction, category: str, name: str, link: str):
    if not has_permission(interaction):
        return await interaction.response.send_message("No perms.", ephemeral=True)

    stock = load_stock()
    if category not in stock:
        stock[category] = {}

    stock[category][name] = link
    save_stock(stock)

    await interaction.response.send_message(f"Added {name} to {category}.", ephemeral=True)

@tree.command(name="removestock", description="Remove a model from stock", guild=discord.Object(id=GUILD_ID))
@app_commands.describe(category="Category name", name="Model name")
async def removestock_slash(interaction: discord.Interaction, category: str, name: str):
    if not has_permission(interaction):
        return await interaction.response.send_message("No permission.", ephemeral=True)

    stock = load_stock()
    if category in stock and name in stock[category]:
        del stock[category][name]
        if not stock[category]:  # Remove empty category
            del stock[category]
        save_stock(stock)
        await interaction.response.send_message(f"Removed **{name}** from **{category}**.", ephemeral=True)
    else:
        await interaction.response.send_message("Model not found.", ephemeral=True)

@tree.command(name="stats", description="View bot statistics", guild=discord.Object(id=GUILD_ID))
async def stats_slash(interaction: discord.Interaction):
    if not has_permission(interaction):
        return await interaction.response.send_message("No permission.", ephemeral=True)

    keys = load_keys()
    redeemed = load_redeemed()
    stock = load_stock()
    usage = load_usage()

    total_models = sum(len(models) for models in stock.values())
    total_categories = len(stock)
    active_keys = len(keys)
    active_users = len(redeemed)

    embed = discord.Embed(title="📊 Bot Statistics", color=discord.Color.blue())
    embed.add_field(name="Stock", value=f"{total_models} models\n{total_categories} categories", inline=True)
    embed.add_field(name="Keys", value=f"{active_keys} pending\n{active_users} redeemed", inline=True)
    embed.add_field(name="Usage", value=f"{len(usage)} users tracked", inline=True)
    embed.timestamp = datetime.utcnow()

    await interaction.response.send_message(embed=embed, ephemeral=True)

# ---------- NEW: /seekeys command ----------
@tree.command(name="seekeys", description="View all active keys and who redeemed them", guild=discord.Object(id=GUILD_ID))
async def seekeys_slash(interaction: discord.Interaction):
    if not has_permission(interaction):
        return await interaction.response.send_message("No permission.", ephemeral=True)

    await interaction.response.defer(ephemeral=True)

    redeemed = load_redeemed()
    keys = load_keys()

    embed = discord.Embed(title="Active Keys Overview", color=discord.Color.blue())

    # Show redeemed keys (active users)
    active_users = []
    for user_id, data in redeemed.items():
        try:
            remaining_time = get_access_remaining_time(int(user_id))
            if remaining_time > 0:
                user = bot.get_user(int(user_id))
                username = user.display_name if user else f"User {user_id}"
                time_str = seconds_to_duration(remaining_time)
                active_users.append(f"**{username}** - {time_str} left")
        except:
            continue

    if active_users:
        # Split into chunks if too many users
        if len(active_users) <= 10:
            embed.add_field(name="👥 Active Users", value="\n".join(active_users), inline=False)
        else:
            # Show first 10 and count
            embed.add_field(name="👥 Active Users (Showing first 10)", value="\n".join(active_users[:10]), inline=False)
            embed.add_field(name="📊 Total Active", value=f"{len(active_users)} users with access", inline=False)
    else:
        embed.add_field(name="👥 Active Users", value="No active users", inline=False)

    # Show unredeemed keys count
    unredeemed_count = 0
    for key_code, key_data in keys.items():
        if isinstance(key_data, dict):
            remaining = key_data.get("remaining_seconds", 0)
            if remaining > 0:
                unredeemed_count += 1

    embed.add_field(name="🗝️ Unredeemed Keys", value=f"{unredeemed_count} keys available", inline=True)
    embed.add_field(name="⏱️ Bot Uptime", value=f"{seconds_to_duration(get_current_uptime_seconds())}", inline=True)

    embed.set_footer(text="Keys only count down when bot is online")
    embed.timestamp = datetime.utcnow()

    await interaction.followup.send(embed=embed, ephemeral=True)

# ---------- Event Handlers ----------
# ---------- Model Commands ----------
@tree.command(name="stock", description="View all available models in stock", guild=discord.Object(id=GUILD_ID))
async def stock_slash(interaction: discord.Interaction):
    """Display all available models organized by category"""
    if not user_has_access(interaction.user.id):
        return await interaction.response.send_message("❌ You need to redeem a valid key first to view stock.", ephemeral=True)
    
    stock = load_stock()
    
    if not stock:
        return await interaction.response.send_message("No stock available.", ephemeral=True)
    
    # Create embed showing all categories and items
    embed = discord.Embed(
        title="📦 Available Stock",
        description="Here are all available models organized by category:",
        color=discord.Color.blue()
    )
    
    for category, models in stock.items():
        if isinstance(models, dict):
            # Get all model names (not links)
            model_names = [name for name in models.keys() if isinstance(models[name], str)]
            if model_names:
                # Limit display to avoid embed size limits
                if len(model_names) > 20:
                    display_names = model_names[:20]
                    models_text = "\n".join(f"• {name}" for name in display_names)
                    models_text += f"\n*...and {len(model_names) - 20} more*"
                else:
                    models_text = "\n".join(f"• {name}" for name in model_names)
                
                embed.add_field(
                    name=f"**{category.upper()}** ({len(model_names)} items)",
                    value=models_text,
                    inline=False
                )
    
    embed.set_footer(text="Use /getmodel <model_name> to download a specific model")
    await interaction.response.send_message(embed=embed, ephemeral=True)

@tree.command(name="getmodel", description="Get a model from stock", guild=discord.Object(id=GUILD_ID))
@app_commands.describe(model_name="The model you want to get")
async def getmodel_slash(interaction: discord.Interaction, model_name: str):
    # Check if user has valid access (redeemed key)
    if not user_has_access(interaction.user.id):
        return await interaction.response.send_message("❌ You need to redeem a valid key first to access models. Use `/panel` to redeem a key.", ephemeral=True)

    stock = load_stock()
    found_model = None
    found_category = None
    model_name_lower = model_name.lower()
    
    # Search for the model in all categories
    for category, models in stock.items():
        if isinstance(models, dict):
            for item_name, item_link in models.items():
                if isinstance(item_link, str):
                    if item_name.lower() == model_name_lower:
                        found_model = item_link
                        model_name = item_name
                        found_category = category
                        break
            if found_model:
                break
    
    # If exact match not found, try fuzzy matching
    if not found_model:
        for category, models in stock.items():
            if isinstance(models, dict):
                model_names = [name for name in models.keys() if isinstance(models[name], str)]
                matches = get_close_matches(model_name, model_names, n=1, cutoff=0.6)
                if matches:
                    matched_name = matches[0]
                    found_model = models[matched_name]
                    model_name = matched_name
                    found_category = category
                    break

    if not found_model:
        return await interaction.response.send_message(f"❌ Model `{model_name}` not found in stock. Use `/stock` to see all available models.", ephemeral=True)

    # Track usage
    uid = str(interaction.user.id)
    usage = load_usage()
    usage.setdefault(uid, {})
    usage[uid].setdefault("redeemed", 0)
    usage[uid]["redeemed"] += 1
    save_usage(usage)

    # Send MediaFire link to DMs
    try:
        embed = discord.Embed(
            title="✅ Model Download",
            description=f"**{model_name}**",
            color=discord.Color.green()
        )
        embed.add_field(name="Category", value=found_category, inline=True)
        embed.add_field(name="📥 Download Link", value=f"[Click Here to Download]({found_model})", inline=False)
        embed.set_footer(text=f"Requested by {interaction.user.display_name}")
        embed.timestamp = datetime.utcnow()
        
        await interaction.user.send(embed=embed)
        await interaction.response.send_message("✅ Download link sent to your DMs!", ephemeral=True)
    except discord.Forbidden:
        # If DMs are closed, send in channel as ephemeral
        embed = discord.Embed(
            title="✅ Model Download",
            description=f"**{model_name}**",
            color=discord.Color.green()
        )
        embed.add_field(name="Category", value=found_category, inline=True)
        embed.add_field(name="📥 Download Link", value=f"[Click Here to Download]({found_model})", inline=False)
        embed.set_footer(text="⚠️ Enable DMs for private downloads")
        embed.timestamp = datetime.utcnow()
        
        await interaction.response.send_message(embed=embed, ephemeral=True)

@bot.event
async def on_message(message):
    if message.author.bot:
        return

    # Track activity
    uid = str(message.author.id)
    activity = load_activity()
    if uid not in activity:
        activity[uid] = {"messages": 0, "reactions": 0}
    activity[uid]["messages"] += 1
    save_activity(activity)

    # Anti-invite for non-bypass users
    if message.guild and not member_has_bypass(message.author):
        if INVITE_REGEX.search(message.content):
            try:
                await message.delete()
                await message.channel.send(f"{message.author.mention}, invite links are not allowed!", delete_after=5)
            except Exception:
                pass

    await bot.process_commands(message)

@bot.event
async def on_raw_reaction_add(payload):
    if payload.user_id == bot.user.id:
        return

    # Track activity
    uid = str(payload.user_id)
    activity = load_activity()
    if uid not in activity:
        activity[uid] = {"messages": 0, "reactions": 0}
    activity[uid]["reactions"] += 1
    save_activity(activity)

@bot.event 
async def on_member_join(member):
    try:
        # Track invites (simplified)
        invites = load_invites()
        guild_id = str(member.guild.id)
        if guild_id not in invites:
            invites[guild_id] = {"total": 0}
        invites[guild_id]["total"] += 1
        save_invites(invites)

        # Log to public channel
        log_channel = bot.get_channel(PUBLIC_LOG_CHANNEL_ID)
        if log_channel:
            embed = discord.Embed(title="Member Joined", color=discord.Color.green())
            embed.add_field(name="User", value=f"{member} ({member.id})", inline=False)
            embed.add_field(name="Account Created", value=f"<t:{int(member.created_at.timestamp())}:R>", inline=True)
            embed.timestamp = datetime.utcnow()
            await log_channel.send(embed=embed)
    except Exception as e:
        logging.error(f"Error in on_member_join: {e}")

@bot.event
async def on_command_error(ctx, error):
    if isinstance(error, commands.CommandNotFound):
        return
    try:
        await ctx.send(f"An error occurred: {error}", delete_after=10)
    except Exception as e:
        logging.error("Failed to send error message: %s", e)

# ---------- Basket & Shop System ----------
MAX_RIGS = 10
baskets = {}  # {user_id: [model1, model2, ...]}

# ---------- Shop Commands ----------
@tree.command(name="savebasket", description="Save your current basket", guild=discord.Object(id=GUILD_ID))
async def savebasket(interaction: discord.Interaction):
    uid = str(interaction.user.id)
    items = baskets.get(uid, [])
    if not items:
        return await interaction.response.send_message("Your basket is empty, nothing to save.", ephemeral=True)
    data = load_saved_baskets()
    data[uid] = items
    save_saved_baskets(data)
    await interaction.response.send_message(f"💾 Basket saved with **{len(items)} items**.", ephemeral=True)

@tree.command(name="loadbasket", description="Load your saved basket", guild=discord.Object(id=GUILD_ID))
async def loadbasket(interaction: discord.Interaction):
    uid = str(interaction.user.id)
    data = load_saved_baskets()
    if uid not in data or not data[uid]:
        return await interaction.response.send_message("You don't have a saved basket.", ephemeral=True)
    saved_items = data[uid]
    current_items = baskets.get(uid, [])
    total_rigs = count_rigs(current_items) + count_rigs(saved_items)
    if total_rigs > MAX_RIGS:
        return await interaction.response.send_message(
            f"Cannot load saved basket. You would exceed the **{MAX_RIGS} rig limit**.",
            ephemeral=True
        )
    baskets[uid] = current_items + saved_items
    del data[uid]
    save_saved_baskets(data)
    await interaction.response.send_message(
        f"📂 Loaded **{len(saved_items)} items** into your basket. You now have **{len(baskets[uid])} items total**.",
        ephemeral=True
    )

@tree.command(name="buymodel", description="Add a model to your shopping basket", guild=discord.Object(id=GUILD_ID))
@app_commands.describe(model="The name of the model to add to your basket")
async def buymodel(interaction: discord.Interaction, model: str):
    if "rig" not in model.lower():
        return await interaction.response.send_message("You can only purchase **kit rigs** at this time.", ephemeral=True)

    uid = str(interaction.user.id)
    current = baskets.setdefault(uid, [])
    if count_rigs(current) >= MAX_RIGS:
        return await interaction.response.send_message(f"You can only buy up to **{MAX_RIGS}** kit rigs per checkout.", ephemeral=True)

    current.append(model)
    price = calculate_price(model)
    total_items = len(baskets[uid])
    total_price, discount = calculate_total(baskets[uid])

    embed = discord.Embed(
        title="Item Added",
        description=f"**{model}** added to basket.\nPrice: **{price} Robux**\nItems: **{total_items}**",
        color=discord.Color.green()
    )
    if discount:
        embed.add_field(name="Discount Active", value="10% OFF applied (3+ rigs)", inline=False)
    embed.set_footer(text=f"User ID: {interaction.user.id}")
    embed.timestamp = datetime.utcnow()

    view = discord.ui.View()

    # Checkout button
    checkout_button = discord.ui.Button(label="Checkout", style=discord.ButtonStyle.success)
    async def checkout_callback(checkout_interaction: discord.Interaction):
        if checkout_interaction.user.id != interaction.user.id:
            return await checkout_interaction.response.send_message("Not your basket.", ephemeral=True)
        items = baskets.get(uid, [])
        if not items:
            return await checkout_interaction.response.send_message("Your basket is empty.", ephemeral=True)
        if count_rigs(items) > MAX_RIGS:
            return await checkout_interaction.response.send_message(f"Basket exceeds limit of {MAX_RIGS} rigs.", ephemeral=True)

        total_price, discount = calculate_total(items)
        applied_coupon = {"code": None, "amount": 0}

        confirm_embed = discord.Embed(
            title="Checkout Confirmation",
            description="\n".join(f"- {m}" for m in items),
            color=discord.Color.blurple()
        )
        confirm_embed.add_field(name="Total", value=f"**{total_price} Robux**", inline=True)
        if discount:
            confirm_embed.add_field(name="Discount", value="10% OFF (3+ rigs)", inline=False)
        confirm_embed.set_footer(text="Use Redeem Coupon before confirming.")
        confirm_embed.timestamp = datetime.utcnow()

        view2 = discord.ui.View()

        # Redeem Coupon Button
        redeem_button = discord.ui.Button(label="Redeem Coupon", style=discord.ButtonStyle.secondary)
        async def redeem_callback(redeem_interaction: discord.Interaction):
            if redeem_interaction.user.id != checkout_interaction.user.id:
                return await redeem_interaction.response.send_message("Not your basket.", ephemeral=True)
            class CouponModal(discord.ui.Modal, title="Enter Coupon Code"):
                code = discord.ui.TextInput(label="Coupon Code", placeholder="Enter your code here")
                async def on_submit(self, modal_interaction: discord.Interaction):
                    coupons = load_coupons()
                    entered = str(self.code.value).strip().upper()
                    if entered in coupons and not coupons[entered]["used"]:
                        applied_coupon["code"] = entered
                        applied_coupon["amount"] = coupons[entered]["amount"]
                        coupons[entered]["used"] = True
                        save_coupons(coupons)
                        await modal_interaction.response.send_message(
                            f"Coupon `{entered}` applied! -{applied_coupon['amount']} Robux", ephemeral=True
                        )
                    else:
                        await modal_interaction.response.send_message("Invalid or already used coupon.", ephemeral=True)
            await redeem_interaction.response.send_modal(CouponModal())
        redeem_button.callback = redeem_callback
        view2.add_item(redeem_button)

        # Confirm Button
        confirm_button = discord.ui.Button(label="Confirm", style=discord.ButtonStyle.success)
        async def confirm_callback(confirm_interaction: discord.Interaction):
            if confirm_interaction.user.id != checkout_interaction.user.id:
                return await confirm_interaction.response.send_message("Not your basket.", ephemeral=True)
            final_price = max(total_price - applied_coupon["amount"], 0)
            receipt_id = generate_receipt_id()
            receipt = discord.Embed(title="Purchase Receipt", color=discord.Color.green())
            receipt.add_field(name="Receipt ID", value=f"`{receipt_id}`", inline=False)
            receipt.add_field(name="User", value=f"{confirm_interaction.user.mention}", inline=False)
            receipt.add_field(name="Models", value="\n".join(f"- {m}" for m in items), inline=False)
            receipt.add_field(name="Total Paid", value=f"**{final_price} Robux**", inline=True)
            if applied_coupon["code"]:
                receipt.add_field(name="Coupon", value=f"{applied_coupon['code']} (-{applied_coupon['amount']} Robux)", inline=False)
            if discount:
                receipt.add_field(name="Discount", value="10% OFF (3+ rigs)", inline=False)
            receipt.set_footer(text=f"User ID: {uid}")
            receipt.timestamp = datetime.utcnow()

            receipts = load_receipts()
            receipts.append({"id": receipt_id, "user": uid, "items": items, "total": final_price, "time": datetime.utcnow().isoformat()})
            save_receipts(receipts)

            view3 = discord.ui.View()
            if final_price in GAMEPASSES:
                buy_button = discord.ui.Button(label="Buy Gamepass", style=discord.ButtonStyle.link, url=GAMEPASSES[final_price])
                view3.add_item(buy_button)

            log_channel = bot.get_channel(RECEIPT_CHANNEL_ID)
            if log_channel:
                await log_channel.send(embed=receipt)

            await confirm_interaction.response.send_message(embed=receipt, view=view3, ephemeral=True)
            baskets[uid] = []
        confirm_button.callback = confirm_callback
        view2.add_item(confirm_button)

        # Cancel Button
        cancel_button = discord.ui.Button(label="Cancel", style=discord.ButtonStyle.danger)
        async def cancel_callback(cancel_interaction: discord.Interaction):
            baskets[uid] = []
            await cancel_interaction.response.send_message("Checkout cancelled. Basket cleared.", ephemeral=True)
        cancel_button.callback = cancel_callback
        view2.add_item(cancel_button)

        await checkout_interaction.response.send_message(embed=confirm_embed, view=view2, ephemeral=True)
    checkout_button.callback = checkout_callback
    view.add_item(checkout_button)

    await interaction.response.send_message(embed=embed, view=view, ephemeral=True)

# ---------- Admin Shop Commands ----------
@tree.command(name="giftbasket", description="Gift a basket to a user", guild=discord.Object(id=GUILD_ID))
@app_commands.describe(user="User to gift", models="Comma separated list of models")
async def giftbasket(interaction: discord.Interaction, user: discord.Member, models: str):
    if not interaction.user.guild_permissions.administrator:
        return await interaction.response.send_message("Only admins can gift baskets.", ephemeral=True)
    uid = str(user.id)
    model_list = [m.strip() for m in models.split(",") if m.strip()]
    baskets[uid] = baskets.get(uid, []) + model_list
    await interaction.response.send_message(f"🎁 Gifted {len(model_list)} models to {user.mention}.", ephemeral=True)

@tree.command(name="gen_coupon", description="Generate a one-time coupon", guild=discord.Object(id=GUILD_ID))
@app_commands.describe(amount="Discount amount in Robux")
async def gen_coupon(interaction: discord.Interaction, amount: int):
    if not interaction.user.guild_permissions.administrator:
        return await interaction.response.send_message("Only admins can generate coupons.", ephemeral=True)
    code = uuid.uuid4().hex[:8].upper()
    coupons = load_coupons()
    coupons[code] = {"amount": amount, "used": False}
    save_coupons(coupons)
    await interaction.response.send_message(f"Coupon generated: `{code}` (-{amount} Robux)", ephemeral=True)

@tree.command(name="sales", description="View total sales", guild=discord.Object(id=GUILD_ID))
async def sales(interaction: discord.Interaction):
    if not interaction.user.guild_permissions.administrator:
        return await interaction.response.send_message("Only admins can view sales.", ephemeral=True)
    receipts = load_receipts()
    total_sales = sum(r["total"] for r in receipts)
    await interaction.response.send_message(f"Total Sales: **{total_sales} Robux** from {len(receipts)} transactions.", ephemeral=True)

# ---------- Moderation Commands ----------
@tree.command(name="mute", description="Mute a user from using the bot", guild=discord.Object(id=GUILD_ID))
@app_commands.describe(user="User to mute", reason="Reason for muting")
async def mute_user(interaction: discord.Interaction, user: discord.Member, reason: str = "No reason provided"):
    if not interaction.user.guild_permissions.administrator:
        return await interaction.response.send_message("Only admins can mute users.", ephemeral=True)

    muted_users.add(user.id)
    embed = discord.Embed(
        title="User Muted",
        description=f"**User:** {user.mention}\n**Reason:** {reason}\n**Muted by:** {interaction.user.mention}",
        color=discord.Color.red()
    )
    embed.timestamp = datetime.utcnow()
    await interaction.response.send_message(embed=embed, ephemeral=True)

@tree.command(name="unmute", description="Unmute a user", guild=discord.Object(id=GUILD_ID))
@app_commands.describe(user="User to unmute")
async def unmute_user(interaction: discord.Interaction, user: discord.Member):
    if not interaction.user.guild_permissions.administrator:
        return await interaction.response.send_message("Only admins can unmute users.", ephemeral=True)

    if user.id in muted_users:
        muted_users.remove(user.id)
        embed = discord.Embed(
            title="User Unmuted",
            description=f"**User:** {user.mention}\n**Unmuted by:** {interaction.user.mention}",
            color=discord.Color.green()
        )
        embed.timestamp = datetime.utcnow()
        await interaction.response.send_message(embed=embed, ephemeral=True)
    else:
        await interaction.response.send_message("User is not muted.", ephemeral=True)

# ---------- AI Auto-Response System ----------
@tree.command(name="toggle_ai", description="Toggle AI auto-responses on/off", guild=discord.Object(id=GUILD_ID))
async def toggle_ai_responses(interaction: discord.Interaction):
    if not interaction.user.guild_permissions.administrator:
        return await interaction.response.send_message("Only admins can toggle AI responses.", ephemeral=True)

    global ai_responses_enabled
    ai_responses_enabled = not ai_responses_enabled
    status = "enabled" if ai_responses_enabled else "disabled"

    embed = discord.Embed(
        title="AI Auto-Responses",
        description=f"AI auto-responses are now **{status}**.",
        color=discord.Color.green() if ai_responses_enabled else discord.Color.red()
    )
    embed.set_footer(text=f"Changed by {interaction.user.display_name}")
    embed.timestamp = datetime.utcnow()

    await interaction.response.send_message(embed=embed, ephemeral=True)

# ---------- Expire Access Command ----------
@tree.command(name="expireaccess", description="Remove user access", guild=discord.Object(id=GUILD_ID))
@app_commands.describe(user="User to remove access from")
async def expireaccess_slash(interaction: discord.Interaction, user: discord.Member):
    if not has_permission(interaction):
        return await interaction.response.send_message("No perms.", ephemeral=True)

    uid = str(user.id)
    redeemed = load_redeemed()

    if uid not in redeemed:
        return await interaction.response.send_message(f"{user.mention} doesn't have any active access.", ephemeral=True)

    # Remove access
    del redeemed[uid]
    save_redeemed(redeemed)

    # Try to remove role
    try:
        role = interaction.guild.get_role(ROLE_ID_TO_GIVE)
        if role and role in user.roles:
            await user.remove_roles(role)
    except Exception as e:
        logging.error(f"Failed to remove role: {e}")

    # Send confirmation
    embed = discord.Embed(
        title="Access Expired",
        description=f"**User:** {user.mention}\n**Expired by:** {interaction.user.mention}",
        color=discord.Color.red()
    )
    embed.timestamp = datetime.utcnow()
    await interaction.response.send_message(embed=embed, ephemeral=True)

    # Log to private channel
    log_channel = bot.get_channel(PRIVATE_LOG_CHANNEL_ID)
    if log_channel:
        log_embed = discord.Embed(title="Access Manually Expired", color=discord.Color.red())
        log_embed.add_field(name="Admin", value=f"{interaction.user.mention}", inline=True)
        log_embed.add_field(name="User", value=f"{user.mention} ({user.id})", inline=True)
        log_embed.timestamp = datetime.utcnow()
        await log_channel.send(embed=log_embed)

    # Try to notify user
    try:
        dm_embed = discord.Embed(
            title="Access Expired",
            description="Your access has been manually expired by an administrator.",
            color=discord.Color.red()
        )
        dm_embed.timestamp = datetime.utcnow()
        await user.send(embed=dm_embed)
    except:
        # If can't DM, that's fine
        pass

# ---------- Global Command Check for Muted Users ----------
@bot.check
async def global_check(ctx):
    """Global check to prevent muted users from using commands"""
    if hasattr(ctx, 'interaction') and ctx.interaction:
        # For slash commands
        user_id = ctx.interaction.user.id
    else:
        # For text commands  
        user_id = ctx.author.id

    # Allow unmute command for admins even if they're muted
    if hasattr(ctx, 'interaction') and ctx.interaction:
        if ctx.interaction.data.get('name') == 'unmute':
            return True
    elif ctx.command and ctx.command.name == 'unmute':
        return True

    return not is_user_muted(user_id)

# ---------- Bot Setup ----------
@bot.event
async def on_ready():
    global bot_start_time
    bot_start_time = datetime.utcnow()

    print(f"Logged in as {bot.user} (ID: {bot.user.id})")
    print("------")

    # Load uptime data
    load_uptime_data()

    # Sync slash commands
    try:
        synced = await tree.sync(guild=discord.Object(id=GUILD_ID))
        print(f"Synced {len(synced)} command(s)")
    except Exception as e:
        print(f"Failed to sync commands: {e}")

    # Start background tasks
    if not update_key_timers.is_running():
        update_key_timers.start()

    print("Bot is ready and time tracking is active!")

# ---------- AI Auto-Response Message Handler ----------
@bot.event
async def on_message(message):
    # Don't respond to self or other bots
    if message.author == bot.user or message.author.bot:
        return

    # Don't respond to commands
    if message.content.startswith(('/', '?', '!')):
        return

    # Check if user is muted
    if message.author.id in muted_users:
        return

    # Only respond if AI is enabled and bot is mentioned or DM
    if ai_responses_enabled:
        if isinstance(message.channel, discord.DMChannel) or bot.user in message.mentions:
            try:
                response = await get_ai_response(message.content)
                await message.reply(response)
            except Exception as e:
                logging.error(f"Error in AI response: {e}")

    # Process commands
    await bot.process_commands(message)

# ---------- Extend Keys Command ----------
@tree.command(name="extendkey", description="Extend all valid keys as compensation for downtime", guild=discord.Object(id=GUILD_ID))
@app_commands.describe(hours="Hours to extend all valid keys")
async def extendkey_slash(interaction: discord.Interaction, hours: int):
    if not has_permission(interaction):
        return await interaction.response.send_message("No permission.", ephemeral=True)

    await interaction.response.defer(ephemeral=True)

    # Track users who get extensions
    extended_users = []
    extension_seconds = hours * 3600

    # Extend unredeemed keys (keys.json)
    keys = load_keys()
    keys_extended = 0
    for key_code, key_data in keys.items():
        if key_data.get("remaining_seconds", 0) > 0:
            keys[key_code]["remaining_seconds"] += extension_seconds
            keys_extended += 1

            user_id = key_data.get("user_id")
            if user_id and user_id not in [u["user_id"] for u in extended_users]:
                extended_users.append({
                    "user_id": user_id,
                    "type": "unredeemed_key"
                })

    save_keys(keys)

    # Extend redeemed access (redeemed.json) 
    redeemed = load_redeemed()
    redeemed_extended = 0
    for user_id, access_data in redeemed.items():
        if isinstance(access_data, dict) and access_data.get("remaining_seconds", 0) > 0:
            redeemed[user_id]["remaining_seconds"] += extension_seconds
            redeemed_extended += 1

            # Check if we already added this user from unredeemed keys
            existing_user = next((u for u in extended_users if u["user_id"] == user_id), None)
            if existing_user:
                existing_user["type"] = "both"
            else:
                extended_users.append({
                    "user_id": user_id, 
                    "type": "redeemed_access"
                })

    save_redeemed(redeemed)

    # DM all affected users
    success_count = 0
    for user_data in extended_users:
        try:
            user = bot.get_user(int(user_data["user_id"]))
            if user:
                embed = discord.Embed(title="Access Extended - Downtime Compensation", color=discord.Color.green())
                embed.add_field(name="Extension", value=f"**{hours} hours** added to your access", inline=False)
                embed.add_field(name="Reason", value="Compensation for recent bot downtime", inline=False)
                embed.set_footer(text="Thank you for your patience! Time only counts down when bot is online.")
                embed.timestamp = datetime.utcnow()

                await user.send(embed=embed)
                success_count += 1
        except Exception as e:
            logging.error(f"Failed to DM user {user_data['user_id']}: {e}")
            continue

    # Send confirmation to admin
    total_extensions = keys_extended + redeemed_extended
    await interaction.followup.send(
        f"Extended {keys_extended} unredeemed keys and {redeemed_extended} active accesses by {hours} hours.\n"
        f"Total affected: {total_extensions} keys/accesses\n"
        f"Successfully notified {success_count}/{len(extended_users)} users via DM.",
        ephemeral=True
    )

    # Log to private channel
    log_channel = bot.get_channel(PRIVATE_LOG_CHANNEL_ID)
    if log_channel:
        log_embed = discord.Embed(title="Mass Key Extension", color=discord.Color.blue())
        log_embed.add_field(name="Admin", value=f"{interaction.user.mention}", inline=True)
        log_embed.add_field(name="Extension", value=f"{hours} hours", inline=True)
        log_embed.add_field(name="Unredeemed Keys", value=str(keys_extended), inline=True)
        log_embed.add_field(name="Active Access", value=str(redeemed_extended), inline=True)
        log_embed.add_field(name="DMs Sent", value=f"{success_count}", inline=True)
        log_embed.timestamp = datetime.utcnow()
        await log_channel.send(embed=log_embed)

# ---------- Graceful Shutdown ----------
import signal

def handle_shutdown():
    """Handle graceful shutdown and save uptime data"""
    print("Bot shutting down... saving uptime data")
    save_uptime_data()
    print("Uptime data saved successfully")

def signal_handler(signum, frame):
    """Handle system shutdown signals"""
    handle_shutdown()
    exit(0)

# Register signal handlers for graceful shutdown
signal.signal(signal.SIGINT, signal_handler)
signal.signal(signal.SIGTERM, signal_handler)

# Add graceful shutdown for the bot
original_close = bot.close
async def graceful_close():
    handle_shutdown()
    await original_close()
bot.close = graceful_close

if __name__ == "__main__":
    keep_alive()
    token = os.getenv("DISCORD_TOKEN")
    if not token:
        raise ValueError("⚠️ No DISCORD_TOKEN found in environment variables.")
    bot.run(token)
