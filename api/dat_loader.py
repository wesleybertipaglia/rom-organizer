dat_files = {
    "Nintendo": {
        "NES - Nintendo Entertainment System": "./data/nintendo/nes.dat",
        "SNES - Super Nintendo Entertainment System": "./data/nintendo/snes.dat",
        "FDS - Famicom Disk System": "./data/nintendo/fds.dat",
        "GB - Game Boy": "./data/nintendo/gb.dat",
        "GBC - Game Boy Color": "./data/nintendo/gbc.dat",
        "GBA - Game Boy Advance": "./data/nintendo/gba.dat",
        "N64 - Nintendo 64": "./data/nintendo/n64.dat",
        "NDS - Nintendo DS": "./data/nintendo/nds.dat",
        "VB - Virtual Boy": "./data/nintendo/vb.dat"
    },
    "Sega": {
        "SG-1000": "./data/sega/sg1000.dat",
        "Master System": "./data/sega/master_system.dat",
        "Genesis / Mega Drive": "./data/sega/genesis.dat",
        "Game Gear": "./data/sega/game_gear.dat",
        "32X": "./data/sega/32x.dat",
        "Pico": "./data/sega/pico.dat"
    },
    "SNK": {
        "NGP - Neo Geo Pocket": "./data/snk/ngp.dat",
        "NGPC - Neo Geo Pocket Color": "./data/snk/ngpc.dat"
    },
    "Sony": {
        "PS1 - PlayStation 1": "./data/sony/ps1.dat",
        "PS2 - PlayStation 2": "./data/sony/ps2.dat",
        "PSP - PlayStation Portable": "./data/sony/psp.dat",
    },
    "Atari": {
        "2600": "./data/atari/2600.dat",
        "5200": "./data/atari/5200.dat",
        "7800": "./data/atari/7800.dat",
        "Atari 8-bit": "./data/atari/8bit.dat",
        "Atari ST": "./data/atari/st.dat",
        "Atari Lynx": "./data/atari/lynx.dat",
        "Atari Jaguar": "./data/atari/jaguar.dat"
    },
    "PC": {
        "Apple II": "./data/pc/apple2.dat"
    },
    "Others": {
        "Arduboy": "./data/others/arduboy.dat"
    }
}

def choose_dat_file():
    print("🎮 Choose a type:")
    brands = list(dat_files.keys())
    for idx, brand in enumerate(brands, start=1):
        print(f"{idx} - {brand}")

    try:
        brand_choice = int(input("🔢 Enter number: ").strip())
        brand_name = brands[brand_choice - 1]
    except (ValueError, IndexError):
        print("❌ Invalid brand choice.")
        return None

    systems = list(dat_files[brand_name].keys())
    print(f"\n📦 Choose a system from {brand_name}:")
    for idx, system in enumerate(systems, start=1):
        print(f"{idx} - {system}")

    try:
        system_choice = int(input("🔢 Enter number: ").strip())
        system_name = systems[system_choice - 1]
        return dat_files[brand_name][system_name]
    except (ValueError, IndexError):
        print("❌ Invalid system choice.")
        return None
