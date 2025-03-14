import os
import sys
import string

sys.path.insert(0, os.path.abspath("deps"))
import vdf


def main():
    home = os.getenv("HOME")
    steam_icon_base_url = (
        "https://cdn.cloudflare.steamstatic.com/steamcommunity/public/images/apps/"
    )
    libraryfolders = str(home) + "/.local/share/Steam/steamapps/libraryfolders.vdf"
    icons_path = str(home) + "/.local/share/icons/hicolor/"

    all_game_id_list = []

    vdf_info_dict = vdf.load(open(libraryfolders))
    for lib_id in vdf_info_dict["libraryfolders"].keys():
        current_lib_id_list = list(
            vdf_info_dict["libraryfolders"][lib_id]["apps"].keys()
        )
        all_game_id_list.extend(current_lib_id_list)

    all_game_id_list = list(set(all_game_id_list))
    all_game_id_list = [int(gid) for gid in all_game_id_list]

    for app_id in all_game_id_list:
        print(app_id)
        clientico_id = ""  # from steamdb
        game_icon_url = (
            steam_icon_base_url + str(app_id) + "/" + str(clientico_id) + ".ico"
        )

        # Get ICO ID from steamdb
        # Get ICO from steam client
        # Convert ICO to png in 16, 24, 32, 48, 64, 96, 128, 192, 256
        # Put converted icon in right folder [steam_icon_{app_id}.png]


if __name__ == "__main__":
    main()
