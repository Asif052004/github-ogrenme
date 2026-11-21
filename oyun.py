"""oyun.py - github-ogrenme icin 10 levellik Git/GitHub oyunu.

Kullanim:
    python oyun.py            # durumu goster, tamamlananlari kontrol et
    python oyun.py harita     # sadece level haritasi
    python oyun.py ipucu      # bulundugun levelin ipucu
    python oyun.py durum      # XP ve rutbe
    python oyun.py sifirla    # ilerlemeyi sifirla (oyun-alani kalir)
    python oyun.py yardim     # komutlar

Oyun, oyun-alani/ icindeki gercek git deposunu inceler; gorevleri sen
yaparsin, dogrulamayi oyun yapar.
"""

from __future__ import annotations

import json
import os
import subprocess
import sys
from dataclasses import dataclass, field
from datetime import datetime
from pathlib import Path

KOK = Path(__file__).resolve().parent
ALAN = KOK / "oyun-alani"
DURUM_DOSYA = KOK / "oyun-durum.json"

if hasattr(sys.stdout, "reconfigure"):
    try:
        sys.stdout.reconfigure(encoding="utf-8", errors="replace")
    except Exception:  # pragma: no cover
        pass

if os.name == "nt":
    os.system("")  # Windows konsolunda ANSI renklerini ac


class R:
    SIFIR = "\033[0m"
    KALIN = "\033[1m"
    SOLUK = "\033[2m"
    YESIL = "\033[92m"
    SARI = "\033[93m"
    MAVI = "\033[94m"
    KIRMIZI = "\033[91m"
    MOR = "\033[95m"
    CYAN = "\033[96m"


RUTBELER = [
    (0, "Caylak", "sadece merak var"),
    (100, "Ogrenci", "temeller oturuyor"),
    (250, "Cirak", "artik dal acabiliyorsun"),
    (450, "Kalfa", "merge korkutmuyor"),
    (700, "Usta", "etiket ve surum senin isin"),
    (1000, "Efsane", "gecmisi geri sarabiliyorsun"),
    (1550, "Git Ustasi", "her sey tamam"),
]


# --------------------------------------------------------------------------
# git yardimcilari
# --------------------------------------------------------------------------
def git(*args: str) -> subprocess.CompletedProcess:
    return subprocess.run(
        ["git", *args],
        cwd=str(ALAN),
        capture_output=True,
        text=True,
        encoding="utf-8",
        errors="replace",
    )


def git_metin(*args: str) -> str:
    sonuc = git(*args)
    return sonuc.stdout.strip() if sonuc.returncode == 0 else ""


@dataclass
class Ortam:
    """Oyun alanindaki deponun anlik durumu."""

    var: bool = False
    commitler: list[tuple[str, list[str], str]] = field(default_factory=list)
    dosyalar: dict[str, list[tuple[str, str]]] = field(default_factory=dict)
    dallar: list[str] = field(default_factory=list)
    etiketler: list[str] = field(default_factory=list)
    anotasyonlu: list[str] = field(default_factory=list)
    merge_head: int = 0
    kirli: bool = False
    origin: bool = False
    uc_var: bool = False
    gonderilmemis: int = 0
    catisma: str = ""
    catisma_takip: bool = False
    surum: str = ""


def ortam_oku() -> Ortam:
    o = Ortam()
    if not (ALAN / ".git").exists():
        return o
    o.var = True

    for satir in git_metin("log", "--all", "--pretty=format:%H%x1f%P%x1f%s").splitlines():
        parcalar = satir.split("\x1f")
        if len(parcalar) < 3:
            continue
        h, ebeveyn, konu = parcalar[0], parcalar[1], parcalar[2]
        o.commitler.append((h, ebeveyn.split(), konu))

    mevcut: str | None = None
    cikti = git("log", "--all", "--name-status", "--pretty=format:@@%H")
    for satir in cikti.stdout.splitlines():
        if satir.startswith("@@"):
            mevcut = satir[2:].strip()
            o.dosyalar.setdefault(mevcut, [])
        elif satir.strip() and mevcut and "\t" in satir:
            durum, yol = satir.split("\t", 1)
            o.dosyalar[mevcut].append((durum.strip(), yol.strip()))

    o.dallar = [d for d in git_metin("branch", "--format=%(refname:short)").splitlines() if d]
    o.etiketler = [t for t in git_metin("tag", "--list").splitlines() if t]
    for satir in git_metin("for-each-ref", "refs/tags", "--format=%(objecttype) %(refname:short)").splitlines():
        tip, _, ad = satir.partition(" ")
        if tip.strip() == "tag" and ad.strip():
            o.anotasyonlu.append(ad.strip())

    o.merge_head = int(git_metin("rev-list", "--merges", "HEAD", "--count") or 0)
    # oyunun kendi dosyalari (oyun.cmd, .gitignore) temizlik kontrolunde sayilmaz
    yok_say = {"oyun.cmd", ".gitignore"}
    kirli_satirlar = [
        s
        for s in git_metin("status", "--porcelain").splitlines()
        if s[3:].strip().strip('"') not in yok_say
    ]
    o.kirli = bool(kirli_satirlar)
    o.origin = git("remote", "get-url", "origin").returncode == 0
    if git("rev-parse", "--abbrev-ref", "--symbolic-full-name", "@{u}").returncode == 0:
        takip = git_metin("rev-parse", "--abbrev-ref", "--symbolic-full-name", "@{u}")
        o.uc_var = bool(takip) and takip != "HEAD"
        if o.uc_var:
            o.gonderilmemis = int(git_metin("rev-list", "@{u}..HEAD", "--count") or 0)

    catisma_yolu = ALAN / "catisma.txt"
    if catisma_yolu.exists():
        o.catisma = catisma_yolu.read_text(encoding="utf-8", errors="replace")
    o.catisma_takip = git("ls-files", "--error-unmatch", "catisma.txt").returncode == 0
    surum_yolu = ALAN / "SURUM.txt"
    if surum_yolu.exists():
        o.surum = surum_yolu.read_text(encoding="utf-8", errors="replace")
    return o


# --------------------------------------------------------------------------
# level kurallari
# --------------------------------------------------------------------------
def k1(o: Ortam) -> bool:
    return o.var and len(o.commitler) >= 1


def k2(o: Ortam) -> bool:
    return len(o.commitler) >= 3


def k3(o: Ortam) -> bool:
    return any(
        len(dosyalar) == 1 and dosyalar[0][0].upper().startswith("A")
        for dosyalar in o.dosyalar.values()
    )


def k4(o: Ortam) -> bool:
    return len(o.dallar) >= 2


def k5(o: Ortam) -> bool:
    return o.merge_head >= 1


def k6(o: Ortam) -> bool:
    return (
        o.catisma_takip
        and "cozuldu" in o.catisma.lower()
        and "<<<<<<<" not in o.catisma
    )


def k7(o: Ortam) -> bool:
    return len(o.anotasyonlu) >= 1


def k8(o: Ortam) -> bool:
    return "v1.0.0" in o.etiketler and "1.0.0" in o.surum


def k9(o: Ortam) -> bool:
    return any(konu.startswith("Revert ") for _, _, konu in o.commitler)


def k10(o: Ortam) -> bool:
    return o.origin and o.uc_var and o.gonderilmemis == 0 and not o.kirli


SEVIYELER = [
    {
        "no": 1,
        "ad": "Ilk Kan",
        "xp": 50,
        "amac": "Git deposunu kur ve ilk commit'ini at.",
        "olcut": "oyun-alani icinde en az 1 commit",
        "gorev": [
            "cd oyun-alani",
            "git init -b main",
            "echo ilk satir> gunluk.txt",
            "git add gunluk.txt",
            'git commit -m "feat: gunluk basladi"',
            "oyun",
        ],
        "ipucu": "oyun-alani ve icindeki oyun.cmd kisayolu ilk calistirmada otomatik olusur. "
        "PowerShell kullaniyorsan: Set-Content gunluk.txt 'ilk satir'",
        "kontrol": k1,
    },
    {
        "no": 2,
        "ad": "Uc Adim",
        "xp": 80,
        "amac": "Gecmise iki commit daha ekle, toplam en az 3 olsun.",
        "olcut": "en az 3 commit (tum dallar dahil)",
        "gorev": [
            "echo ikinci satir>> gunluk.txt",
            "git add gunluk.txt",
            'git commit -m "docs: ikinci satir"',
            "echo ucuncu satir>> gunluk.txt",
            "git add gunluk.txt",
            'git commit -m "docs: ucuncu satir"',
            "oyun",
        ],
        "ipucu": "Her commit tek bir anlama sahip olsun: 'docs: ...' gibi bir onek kullan.",
        "kontrol": k2,
    },
    {
        "no": 3,
        "ad": "Sahne Ustasi",
        "xp": 100,
        "amac": "Tek dosyalik, temiz bir commit at (sahneye sadece bir yeni dosya).",
        "olcut": "tek dosya ekleyen bir commit (baska degisiklik yok)",
        "gorev": [
            "echo fikirler> fikirler.txt",
            "git add fikirler.txt",
            'git commit -m "docs: fikir listesi"',
            "oyun",
        ],
        "ipucu": "git add -A yerine dosya adini ver: git add fikirler.txt. "
        "git status ile sahnede baska sey olmadigini kontrol et.",
        "kontrol": k3,
    },
    {
        "no": 4,
        "ad": "Dal Ac",
        "xp": 120,
        "amac": "Yeni bir dal ac, orada commit at, main'e don.",
        "olcut": "en az 2 yerel dal",
        "gorev": [
            "git switch -c deneme",
            "echo dal icin satir>> gunluk.txt",
            "git add gunluk.txt",
            'git commit -m "feat: deneme dalinda satir"',
            "git switch main",
            "oyun",
        ],
        "ipucu": "git branch ile dallari listele. Dali simdilik silme, sonraki levelda ise yarayacak.",
        "kontrol": k4,
    },
    {
        "no": 5,
        "ad": "Kopru",
        "xp": 150,
        "amac": "deneme dalini main'e merge commit'i olusturarak birlestir.",
        "olcut": "HEAD gecmisinde en az 1 merge commit",
        "gorev": [
            "git merge --no-ff deneme -m \"merge: deneme dali\"",
            "git log --graph --oneline --all",
            "oyun",
        ],
        "ipucu": "--no-ff, fast-forward olsa bile merge commit'i zorlar; boylece dal bilgisi gecmiste kalir.",
        "kontrol": k5,
    },
    {
        "no": 6,
        "ad": "Catisma Ustasi",
        "xp": 200,
        "amac": "Iki dalda ayni dosyayi degistir, cakismayi elle coz.",
        "olcut": "catisma.txt commit'lenmis ve icinde 'cozuldu' yaziyor",
        "gorev": [
            "echo catisma-hazir> catisma.txt",
            "git add catisma.txt",
            'git commit -m "chore: catisma hazirligi"',
            "git switch -c dal/catisma",
            "echo dal-tarafi> catisma.txt",
            "git add catisma.txt",
            'git commit -m "feat: dal tarafi"',
            "git switch main",
            "echo main-tarafi> catisma.txt",
            "git add catisma.txt",
            'git commit -m "feat: main tarafi"',
            "git merge dal/catisma      (cakisma cikacak)",
            "echo cozuldu> catisma.txt",
            "git add catisma.txt",
            "git commit --no-edit",
            "oyun",
        ],
        "ipucu": "<<<<<<< ======= >>>>>>> isaretlerini sil, dosyada 'cozuldu' kelimesi kalsin. "
        "Vazgecmek istersen: git merge --abort",
        "kontrol": k6,
    },
    {
        "no": 7,
        "ad": "Muhur",
        "xp": 120,
        "amac": "Anlamli bir tag (surum muhru) bas.",
        "olcut": "en az 1 anotasyonlu tag",
        "gorev": [
            'git tag -a v0.1.0 -m "ilk deneme surumu"',
            "git tag --list",
            "oyun",
        ],
        "ipucu": "-a olmadan tag 'hafif' olur; -a ile mesaj yazinca anotasyonlu (muhurlu) tag olur.",
        "kontrol": k7,
    },
    {
        "no": 8,
        "ad": "Surum Kapisi",
        "xp": 150,
        "amac": "Surum dosyasi olustur ve v1.0.0 tag'i ile isaretle.",
        "olcut": "SURUM.txt icinde 1.0.0 ve v1.0.0 tag'i",
        "gorev": [
            "echo 1.0.0> SURUM.txt",
            "git add SURUM.txt",
            'git commit -m "chore: surum dosyasi"',
            'git tag -a v1.0.0 -m "surum 1.0.0"',
            "oyun",
        ],
        "ipucu": "Gercek projelerde tag ile surum dosyasi ayni commit'te olur; okuyan kisi hangi kodun 1.0.0 oldugunu bilir.",
        "kontrol": k8,
    },
    {
        "no": 9,
        "ad": "Zamani Geri Sar",
        "xp": 180,
        "amac": "Bir commit'i revert ile guvenli sekilde geri al.",
        "olcut": "'Revert ...' ile baslayan bir commit",
        "gorev": [
            "echo gecici>> gunluk.txt",
            "git add gunluk.txt",
            'git commit -m "chore: gecici satir"',
            "git revert HEAD --no-edit",
            "git log --oneline -3",
            "oyun",
        ],
        "ipucu": "revert gecmisi silmez, tersini yapan yeni bir commit ekler. Ortak gecmiste guvenli yol budur.",
        "kontrol": k9,
    },
    {
        "no": 10,
        "ad": "Uzak Diyar (BOSS)",
        "xp": 400,
        "amac": "Depoyu GitHub'a tasi: remote ekle, push et, temiz calis.",
        "olcut": "origin var, upstream kurulu, gonderilmemis commit yok, calisma agaci temiz",
        "gorev": [
            "# github.com'da bos bir repo ac (README/gitignore EKLEMEDEN)",
            "git remote add origin https://github.com/KULLANICI/REPO.git",
            "git push -u origin main",
            "git status          (working tree clean olmali)",
            "oyun",
        ],
        "ipucu": "Repo'yu web'de acarken hicbir dosya ekleme; yoksa iki farkli gecmis cikar. "
        "Sonra git remote -v ile baglantiyi dogrula.",
        "kontrol": k10,
    },
]


# --------------------------------------------------------------------------
# durum dosyasi
# --------------------------------------------------------------------------
def durum_oku() -> dict:
    varsayilan = {"xp": 0, "tamamlanan": [], "baslangic": datetime.now().isoformat(timespec="seconds")}
    if DURUM_DOSYA.exists():
        try:
            veri = json.loads(DURUM_DOSYA.read_text(encoding="utf-8"))
            if isinstance(veri, dict):
                varsayilan.update(veri)
        except (json.JSONDecodeError, OSError):
            pass
    varsayilan["tamamlanan"] = [int(n) for n in varsayilan.get("tamamlanan", [])]
    return varsayilan


def durum_yaz(durum: dict) -> None:
    durum["xp"] = sum(s["xp"] for s in SEVIYELER if s["no"] in durum["tamamlanan"])
    DURUM_DOSYA.write_text(json.dumps(durum, ensure_ascii=False, indent=2), encoding="utf-8")


def toplam_xp() -> int:
    return sum(s["xp"] for s in SEVIYELER)


def rutbe(xp: int) -> tuple[str, str]:
    ad, motto = RUTBELER[0][1], RUTBELER[0][2]
    for esik, isim, soz in RUTBELER:
        if xp >= esik:
            ad, motto = isim, soz
    return ad, motto


# --------------------------------------------------------------------------
# ekran
# --------------------------------------------------------------------------
def alan_hazirla() -> None:
    if ALAN.exists():
        return
    ALAN.mkdir(parents=True)
    (ALAN / "oyun.cmd").write_text(
        '@echo off\r\npython "%~dp0..\\oyun.py" %*\r\n', encoding="utf-8"
    )
    (ALAN / ".gitignore").write_text("oyun.cmd\n", encoding="utf-8")


def baslik() -> None:
    print()
    print(f" {R.MOR}{R.KALIN}  GIT MACERASI{R.SIFIR} {R.SOLUK}· 10 level · oyun-alani icinde gercek git{R.SIFIR}")
    print()


def xp_cubugu(xp: int) -> str:
    toplam = toplam_xp()
    oran = xp / toplam if toplam else 0
    dolu = int(round(oran * 24))
    renk = R.YESIL if oran >= 0.999 else R.CYAN
    return f"{renk}{'█' * dolu}{R.SOLUK}{'░' * (24 - dolu)}{R.SIFIR}"


def durum_satiri(durum: dict) -> None:
    xp = sum(s["xp"] for s in SEVIYELER if s["no"] in durum["tamamlanan"])
    ad, motto = rutbe(xp)
    print(f" XP {xp_cubugu(xp)} {xp}/{toplam_xp()}   {R.KALIN}Rutbe:{R.SIFIR} {ad} {R.SOLUK}({motto}){R.SIFIR}")
    print(f" Tamamlanan: {R.KALIN}{len(durum['tamamlanan'])}/10{R.SIFIR}")
    print()


def harita(durum: dict) -> None:
    simdiki = next((s for s in SEVIYELER if s["no"] not in durum["tamamlanan"]), None)
    print(f" {R.SOLUK}LEVEL HARITASI{R.SIFIR}")
    for s in SEVIYELER:
        tamam = s["no"] in durum["tamamlanan"]
        if tamam:
            imlec, renk, isaret = "[x]", R.YESIL, "✓"
        elif simdiki and s["no"] == simdiki["no"]:
            imlec, renk, isaret = "[>]", R.SARI, "▶"
        else:
            imlec, renk, isaret = "[ ]", R.SOLUK, " "
        ad = s["ad"]
        nokta = "." * max(3, 26 - len(ad))
        print(f"  {renk}{isaret} {s['no']:02d} {ad} {nokta} {s['xp']:>3} XP{R.SIFIR}")
    print()


def level_detay(s: dict, basarili: bool | None = None) -> None:
    cizgi = "─" * 60
    print(f" {R.MOR}┌{cizgi}{R.SIFIR}")
    print(f" {R.MOR}│{R.SIFIR} {R.KALIN}LEVEL {s['no']} · {s['ad']}{R.SIFIR}  {R.SOLUK}({s['xp']} XP){R.SIFIR}")
    print(f" {R.MOR}│{R.SIFIR}")
    print(f" {R.MOR}│{R.SIFIR} {R.KALIN}Amac:{R.SIFIR} {s['amac']}")
    print(f" {R.MOR}│{R.SIFIR}")
    print(f" {R.MOR}│{R.SIFIR} {R.KALIN}Gorev{R.SIFIR} {R.SOLUK}(oyun-alani icinde){R.SIFIR}:")
    for komut in s["gorev"]:
        if komut.strip().startswith("#"):
            print(f" {R.MOR}│{R.SIFIR}   {R.SOLUK}{komut}{R.SIFIR}")
        else:
            print(f" {R.MOR}│{R.SIFIR}   {R.CYAN}{komut}{R.SIFIR}")
    print(f" {R.MOR}│{R.SIFIR}")
    if basarili is None:
        print(f" {R.MOR}│{R.SIFIR} {R.SOLUK}Durum kontrol edilmedi. 'python oyun.py kontrol'{R.SIFIR}")
    elif basarili:
        print(f" {R.MOR}│{R.SIFIR} {R.YESIL}Durum: ✓ tamam{R.SIFIR}")
    else:
        print(f" {R.MOR}│{R.SIFIR} {R.SARI}Durum: ✗ henuz olmadi{R.SIFIR} {R.SOLUK}(olcut: {s['olcut']}){R.SIFIR}")
        print(f" {R.MOR}│{R.SIFIR} {R.SOLUK}Takildiysan: python oyun.py ipucu{R.SIFIR}")
    print(f" {R.MOR}└{cizgi}{R.SIFIR}")
    print()


def level_up(s: dict, yeni_rutbe: str | None) -> None:
    print()
    print(f" {R.YESIL}{R.KALIN}  ╔══════════════════════════════════════════╗{R.SIFIR}")
    print(f" {R.YESIL}{R.KALIN}  ║  LEVEL {s['no']} TAMAMLANDI · +{s['xp']} XP{' ' * 12}║{R.SIFIR}")
    print(f" {R.YESIL}{R.KALIN}  ║  {s['ad']:<40}║{R.SIFIR}")
    print(f" {R.YESIL}{R.KALIN}  ╚══════════════════════════════════════════╝{R.SIFIR}")
    if yeni_rutbe:
        print(f" {R.SARI}{R.KALIN}  Yeni rutbe: {yeni_rutbe}{R.SIFIR}")
    print()


def kontrol_et(durum: dict, o: Ortam) -> None:
    onceki_rutbe, _ = rutbe(sum(s["xp"] for s in SEVIYELER if s["no"] in durum["tamamlanan"]))
    while True:
        kalan = [s for s in SEVIYELER if s["no"] not in durum["tamamlanan"]]
        if not kalan:
            break
        s = kalan[0]
        try:
            basarili = s["kontrol"](o)
        except Exception:
            basarili = False
        if not basarili:
            break
        durum["tamamlanan"].append(s["no"])
        durum_yaz(durum)
        yeni, _ = rutbe(sum(x["xp"] for x in SEVIYELER if x["no"] in durum["tamamlanan"]))
        level_up(s, yeni if yeni != onceki_rutbe else None)
        onceki_rutbe = yeni


# --------------------------------------------------------------------------
# komutlar
# --------------------------------------------------------------------------
def cmd_kontrol(o: Ortam, durum: dict, ilk_calisma: bool = False) -> None:
    baslik()
    once = len(durum["tamamlanan"])
    kontrol_et(durum, o)
    sonra = len(durum["tamamlanan"])
    durum_satiri(durum)
    harita(durum)
    kalan = [s for s in SEVIYELER if s["no"] not in durum["tamamlanan"]]
    if not kalan:
        print(f" {R.YESIL}{R.KALIN}  Tum leveller tamam. Sen artik bir Git Ustasisin.{R.SIFIR}")
        print(
            f" {R.SOLUK}  Sirada ne var? GitHub'da issue ac, PR incele, baska bir repoya katki ver.{R.SIFIR}\n"
        )
        return
    if sonra == once:
        if ilk_calisma:
            print(f" {R.MOR}  Hos geldin.{R.SIFIR} {R.SOLUK}oyun-alani hazir; asagidaki komutlarla basla.{R.SIFIR}\n")
            level_detay(kalan[0])
        else:
            print(f" {R.SARI}  Yeni level yok.{R.SIFIR} {R.SOLUK}Siradaki gorev:{R.SIFIR}\n")
            level_detay(kalan[0], basarili=False)
    else:
        print(f" {R.SOLUK}  Siradaki gorev:{R.SIFIR}\n")
        level_detay(kalan[0])


def cmd_ipucu(durum: dict) -> None:
    kalan = [s for s in SEVIYELER if s["no"] not in durum["tamamlanan"]]
    if not kalan:
        print(f" {R.YESIL}Ipucuna ihtiyacin yok, hepsi bitti.{R.SIFIR}")
        return
    s = kalan[0]
    print(f"\n {R.KALIN}Level {s['no']} · {s['ad']}{R.SIFIR}")
    print(f" {R.CYAN}{s['ipucu']}{R.SIFIR}")
    print(f" {R.SOLUK}Olcut: {s['olcut']}{R.SIFIR}\n")


def cmd_durum(durum: dict) -> None:
    baslik()
    durum_satiri(durum)
    print(f" {R.SOLUK}Oyun alani: {ALAN}{R.SIFIR}")
    print(f" {R.SOLUK}Durum dosyasi: {DURUM_DOSYA.name}{R.SIFIR}\n")


def cmd_sifirla() -> None:
    if DURUM_DOSYA.exists():
        DURUM_DOSYA.unlink()
    print(f" {R.SARI}Ilerleme sifirlandi.{R.SIFIR} {R.SOLUK}oyun-alani/ ve icindeki depo duruyor.{R.SIFIR}\n")


def cmd_yardim() -> None:
    baslik()
    print("  python oyun.py            durumu goster + ilerlemeyi kontrol et")
    print("  python oyun.py kontrol    gorevleri dogrula, XP ver")
    print("  python oyun.py harita     level haritasi")
    print("  python oyun.py ipucu      bulundugun levelin ipucu")
    print("  python oyun.py durum      XP, rutbe, yollar")
    print("  python oyun.py sifirla    ilerlemeyi sifirla")
    print("  python oyun.py yardim     bu ekran")
    print()
    print(f"  {R.SOLUK}Oyun 'oyun-alani' icindeki gercek git deposunu okur; komutlari sen yazarsin.{R.SIFIR}")
    print(f"  {R.SOLUK}Alişkanlik: oyun-alani icindeyken sadece 'oyun' yaz (oyun.cmd).{R.SIFIR}\n")


def main(argv: list[str] | None = None) -> int:
    komutlar = {"kontrol", "harita", "ipucu", "durum", "sifirla", "yardim"}
    argv = list(sys.argv[1:] if argv is None else argv)
    komut = argv[0] if argv else ""
    if komut and komut not in komutlar:
        print(f" {R.KIRMIZI}Bilinmeyen komut: {komut}{R.SIFIR}  {R.SOLUK}(yardim icin: python oyun.py yardim){R.SIFIR}")
        return 2

    alan_hazirla()
    ilk_calisma = not DURUM_DOSYA.exists()
    durum = durum_oku()

    if komut == "yardim":
        cmd_yardim()
        return 0
    if komut == "sifirla":
        cmd_sifirla()
        return 0

    o = ortam_oku()
    if komut == "durum":
        cmd_durum(durum)
    elif komut == "harita":
        baslik()
        durum_satiri(durum)
        harita(durum)
    elif komut == "ipucu":
        cmd_ipucu(durum)
    else:
        cmd_kontrol(o, durum, ilk_calisma)
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
