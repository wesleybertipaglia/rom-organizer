dat_files = {
    "Nintendo": {
        "NES - Nintendo Entertainment System": "./data/nintendo/nes.dat",
        "SNES - Super Nintendo Entertainment System": "./data/nintendo/snes.dat",
        "Famicom - Family Computer": "./data/nintendo/famicom.dat",
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
        "Genesis": "./data/sega/genesis.dat",
        "Mega Drive": "./data/sega/mega_drive.dat",
        "Game Gear": "./data/sega/game_gear.dat",
        "Sega CD": "./data/sega/sega_cd.dat",
        "32X": "./data/sega/32x.dat",
        "Saturn": "./data/sega/saturn.dat",
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
        "Atari Lynx": "./data/atari/lynx.dat",
        "Atari ST": "./data/atari/st.dat"
    },
    "NEC": {
        "PC Engine / TurboGrafx-16": "./data/nec/pc_engine.dat",
        "PC Engine CD / TurboGrafx-CD": "./data/nec/pc_engine_cd.dat",
        "SuperGrafx": "./data/nec/supergrafx.dat"
    },
    "Commodore": {
        "Commodore 64": "./data/commodore/c64.dat",
        "Commodore VIC-20": "./data/commodore/vic20.dat",
        "Commodore Amiga": "./data/commodore/amiga.dat"
    },
    "Amstrad": {
        "Amstrad CPC": "./data/amstrad/cpc.dat"
    },
    "Apple": {
        "Apple II": "./data/apple/apple2.dat"
    },
    "Arcade": {
        "MAME": "./data/arcade/mame.dat",
        "CPS1 - Capcom Play System 1": "./data/arcade/cps1.dat",
        "CPS2 - Capcom Play System 2": "./data/arcade/cps2.dat",
        "CPS3 - Capcom Play System 3": "./data/arcade/cps3.dat",
        "Neo Geo": "./data/arcade/neogeo.dat"
    },
    "Others": {
        "MSX": "./data/others/msx.dat",
        "MSX2": "./data/others/msx2.dat",
        "ZX Spectrum": "./data/others/zx_spectrum.dat",
        "WonderSwan": "./data/others/wonderswan.dat",
        "WonderSwan Color": "./data/others/wonderswan_color.dat",
        "3DO": "./data/others/3do.dat",
        "ColecoVision": "./data/others/colecovision.dat",
        "Intellivision": "./data/others/intellivision.dat"
    }
}

def choose_dat_file():
    print("🎮 Choose a brand:")
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
