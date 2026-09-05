from http.server import ThreadingHTTPServer, SimpleHTTPRequestHandler
from pathlib import Path
import json
import urllib.parse
import os

ROOT = Path(__file__).resolve().parent
CHAR_DIR = ROOT / "characters"
PORT = 8000


# =========================================================
# 全キャラクター共通の音声順
# =========================================================

SOUND_ORDER = [
    "title.ogg",

    "aisatsu.ogg",
    "jikoshokai.ogg",
    "home.ogg",

    "login1.ogg",
    "login2.ogg",
    "login3.ogg",
    "login4.ogg",
    "login5.ogg",
    "login6.ogg",
    "login7.ogg",
    "login8.ogg",
    "login9.ogg",
    "login10.ogg",
    "login 10.ogg",
    "login11.ogg",
    "login12.ogg",

    "loginbonus1.ogg",
    "loginbonus2.ogg",

    "aiduchi1.ogg",
    "aiduchi2.ogg",

    "yorokobi.ogg",
    "warai.ogg",
    "kangeki.ogg",
    "kansha.ogg",

    "odoroki.ogg",
    "ikari.ogg",
    "kanashii.ogg",
    "nayami.ogg",
    "makekomihagemashi.ogg",

    "deai.ogg",
    "wakare.ogg",
    "friendshinsei.ogg",
    "message.ogg",
    "presentbox1.ogg",
    "presentbox2.ogg",

    "hanyou1.ogg",
    "hanyou2.ogg",
    "hanyou3.ogg",
    "hanyou4.ogg",

    "damagesho.ogg",
    "damagechu.ogg",
    "damagedai.ogg",

    "taisenkaishi.ogg",
    "kaishi.ogg",
    "kaishiB.ogg",
    "chudanbattle.ogg",
    "chudanbattle.og",

    "gameshori.ogg",
    "gamehaiboku.ogg",

    "strigger.ogg",
    "kirifudadraw.ogg",

    "kimezerifu1.ogg",
    "kimezerifu2.ogg",
    "kimezerifu3.ogg",

    "kinou1.ogg",
    "kinou2.ogg",

    "judenchu.ogg",
    "shop1.ogg",
    "shop2.ogg",
    "shop3.ogg",

    "packopen1.ogg",
    "packopen2.ogg",
    "packopen3.ogg",
]


# =========================================================
# 音声の表示名
# =========================================================

SOUND_NAMES = {
    "aiduchi1.ogg": "相槌1",
    "aiduchi2.ogg": "相槌2",
    "aisatsu.ogg": "あいさつ",
    "aizu.ogg": "合図",

    "chudanbattle.og": "バトル中断",
    "chudanbattle.ogg": "バトル中断",

    "damagechu.ogg": "ダメージ中",
    "damagedai.ogg": "ダメージ大",
    "damagesho.ogg": "ダメージ小",

    "deai.ogg": "出会い",
    "friendshinsei.ogg": "フレンド申請",

    "gamehaiboku.ogg": "敗北",
    "gameshori.ogg": "勝利",

    "hanyou1.ogg": "汎用1",
    "hanyou2.ogg": "汎用2",
    "hanyou3.ogg": "汎用3",
    "hanyou4.ogg": "汎用4",

    "home.ogg": "ホーム",
    "ikari.ogg": "怒り",
    "jikoshokai.ogg": "自己紹介",
    "judenchu.ogg": "充電",

    "kanashii.ogg": "悲しみ",
    "kangeki.ogg": "感激",
    "kansha.ogg": "感謝",

    "kimezerifu1.ogg": "決めセリフ1",
    "kimezerifu2.ogg": "決めセリフ2",
    "kimezerifu3.ogg": "決めセリフ3",

    "kinou1.ogg": "特殊1",
    "kinou2.ogg": "特殊2",

    "kirifudadraw.ogg": "切り札",

    "kaishi.ogg": "開始",
    "kaishiB.ogg": "開始B",

    "login1.ogg": "ログイン1",
    "login2.ogg": "ログイン2",
    "login3.ogg": "ログイン3",
    "login4.ogg": "ログイン4",
    "login5.ogg": "ログイン5",
    "login6.ogg": "ログイン6",
    "login7.ogg": "ログイン7",
    "login8.ogg": "ログイン8",
    "login9.ogg": "ログイン9",
    "login10.ogg": "ログイン10",
    "login 10.ogg": "ログイン10",
    "login11.ogg": "ログイン11",
    "login12.ogg": "ログイン12",

    "loginbonus1.ogg": "ログインボーナス1",
    "loginbonus2.ogg": "ログインボーナス2",

    "message.ogg": "お知らせ",
    "odoroki.ogg": "驚き",

    "packopen1.ogg": "開封1",
    "packopen2.ogg": "開封2",
    "packopen3.ogg": "開封3",

    "makekomihagemashi.ogg": "励まし",
    "nayami.ogg": "悩み",

    "presentbox1.ogg": "プレゼント1",
    "presentbox2.ogg": "プレゼント2",

    "shop1.ogg": "ショップ1",
    "shop2.ogg": "ショップ2",
    "shop3.ogg": "ショップ3",

    "strigger.ogg": "シールドトリガー",
    "taisenkaishi.ogg": "対戦開始",

    "tutorial1.ogg": "ネガティブ",
    "tutorial2.ogg": "対戦開始2",

    "wakare.ogg": "別れ",
    "warai.ogg": "笑い",
    "yorokobi.ogg": "喜び",

    "title.ogg": "タイトル",
}


IMAGE_EXTS = {
    ".png",
    ".jpg",
    ".jpeg",
    ".webp",
    ".gif",
}

AUDIO_EXTS = {
    ".ogg",
    ".mp3",
    ".wav",
    ".m4a",
}


# =========================================================
# order.txtを読む
# =========================================================

def read_order(folder):

    order_file = folder / "order.txt"

    if not order_file.is_file():
        return []

    lines = order_file.read_text(
        encoding="utf-8-sig"
    ).splitlines()

    return [
        line.strip()
        for line in lines
        if line.strip()
        and not line.lstrip().startswith("#")
    ]


# =========================================================
# キャラクター・衣装の順番
# =========================================================

def ordered(items, order):

    items_dict = {
        item.name: item
        for item in items
    }

    result = []

    for name in order:

        if name in items_dict:
            result.append(items_dict.pop(name))

    result += sorted(
        items_dict.values(),
        key=lambda p: p.name.casefold()
    )

    return result


# =========================================================
# 音声を共通順に並べる
# =========================================================

def ordered_sounds(items):

    items_dict = {
        item.name: item
        for item in items
    }

    result = []

    # 共通順に並べる
    for name in SOUND_ORDER:

        if name in items_dict:

            result.append(
                items_dict.pop(name)
            )

    # 共通リストにない新しい音声は最後へ
    result += sorted(
        items_dict.values(),
        key=lambda p: p.name.casefold()
    )

    return result


def relative_path(path):

    return path.relative_to(ROOT).as_posix()


# =========================================================
# キャラクターデータ作成
# =========================================================

def make_data():

    CHAR_DIR.mkdir(exist_ok=True)

    characters = []

    character_dirs = [
        p
        for p in CHAR_DIR.iterdir()
        if p.is_dir()
    ]

    character_dirs = ordered(
        character_dirs,
        read_order(CHAR_DIR)
    )

    for character_dir in character_dirs:

        outfits = []

        outfit_dirs = [
            p
            for p in character_dir.iterdir()
            if p.is_dir()
        ]

        outfit_dirs = ordered(
            outfit_dirs,
            read_order(character_dir)
        )

        for outfit_dir in outfit_dirs:

            images = [
                p
                for p in outfit_dir.iterdir()
                if p.is_file()
                and p.suffix.lower() in IMAGE_EXTS
            ]

            audio_files = [
                p
                for p in outfit_dir.iterdir()
                if p.is_file()
                and p.suffix.lower() in AUDIO_EXTS
            ]

            # 全キャラクター共通の順番
            audio_files = ordered_sounds(
                audio_files
            )

            sounds = []

            for audio in audio_files:

                sounds.append({
                    "file": relative_path(audio),
                    "name": SOUND_NAMES.get(
                        audio.name,
                        audio.stem
                    )
                })

            outfits.append({
                "name": outfit_dir.name,

                "image":
                    relative_path(images[0])
                    if images
                    else None,

                "sounds": sounds
            })

        representative_image = next(
            (
                outfit["image"]
                for outfit in outfits
                if outfit["image"]
            ),
            None
        )

        characters.append({
            "name": character_dir.name,
            "image": representative_image,
            "outfits": outfits
        })

    return characters


# =========================================================
# WEBサーバー
# =========================================================

class Handler(SimpleHTTPRequestHandler):

    def do_GET(self):

        path = urllib.parse.urlparse(
            self.path
        ).path

        if path == "/api/data":

            data = make_data()

            body = json.dumps(
                data,
                ensure_ascii=False
            ).encode("utf-8")

            self.send_response(200)

            self.send_header(
                "Content-Type",
                "application/json; charset=utf-8"
            )

            self.send_header(
                "Content-Length",
                str(len(body))
            )

            self.end_headers()

            self.wfile.write(body)

            return

        if path == "/":

            file = ROOT / "index.html"

            body = file.read_bytes()

            self.send_response(200)

            self.send_header(
                "Content-Type",
                "text/html; charset=utf-8"
            )

            self.send_header(
                "Content-Length",
                str(len(body))
            )

            self.end_headers()

            self.wfile.write(body)

            return

        super().do_GET()


if __name__ == "__main__":

    os.chdir(ROOT)

    print("================================")
    print("Voice Soundboard")
    print("================================")
    print()
    print("サイトを起動しました")
    print()
    print("http://localhost:8000/")
    print()
    print("終了する場合は Ctrl + C")
    print()

    server = ThreadingHTTPServer(
        ("0.0.0.0", int(os.environ.get("PORT", PORT))),
        Handler
    )

    server.serve_forever()