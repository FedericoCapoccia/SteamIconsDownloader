import os
import sys
from urllib.request import urlretrieve
import subprocess

sys.path.insert(0, os.path.abspath("deps"))
import vdf
from steam.client import SteamClient
from PIL import Image

HOME = os.getenv("HOME")
TMP = "/tmp/"

max_retry = 5
steam_icons_url = (
    "https://cdn.cloudflare.steamstatic.com/steamcommunity/public/images/apps/"
)
libinfo_dir = str(HOME) + "/.local/share/Steam/steamapps/libraryfolders.vdf"
icons_path = str(HOME) + "/.local/share/icons/hicolor/"

resolutions = [
    256,
    192,
    128,
    96,
    64,
    48,
    32,
    24,
    16,
]

id_list = []


## Retrieves all installed game's id
def list_games():
    global id_list

    vdf_info_dict = vdf.load(open(libinfo_dir))
    for lib_id in vdf_info_dict["libraryfolders"].keys():
        current_lib_id_list = list(
            vdf_info_dict["libraryfolders"][lib_id]["apps"].keys()
        )
        id_list.extend(current_lib_id_list)

    id_list = list(set(id_list))
    id_list = [int(gid) for gid in id_list]


def main():
    client = SteamClient()
    client.anonymous_login()
    assert client.logged_on

    for app_id in id_list:
        game = (
            client.get_product_info(
                apps=[
                    app_id,
                ]
            )
        )["apps"][
            app_id
        ]["common"]

        if game["name"] == "Steamworks Common Redistributables":
            continue

        if "clienticon" in list(game.keys()):
            print("Working on:", game["name"], "(", app_id, ")")
            icon_url = steam_icons_url + str(app_id) + "/" + game["clienticon"] + ".ico"
            icon_filename = "steam_icon_" + str(app_id) + ".ico"
            png_filename = "steam_icon_" + str(app_id) + ".png"

            trials = 0
            while trials < max_retry:
                try:
                    urlretrieve(icon_url, os.path.join(TMP, icon_filename))
                    break
                except:
                    trials += 1
                    print("Failed to retrieve icon, retrying...")

            img = Image.open(os.path.join(TMP, icon_filename))
            print("Icon size: ", img.size)

            max_size = img.width
            # 0 for 256x256, 1 for 192x192 etc...
            start_res_idx = resolutions.index(max_size)

            for idx in range(start_res_idx, len(resolutions)):
                size = resolutions[idx]
                resized_img = img.resize((size, size), Image.Resampling.LANCZOS)

                output_dir = icons_path + str(size) + "x" + str(size) + "/apps"
                os.makedirs(output_dir, exist_ok=True)
                output_path = os.path.join(output_dir, png_filename)
                resized_img.save(output_path, format="PNG")

            img.close()
            os.remove(os.path.join(TMP, icon_filename))


if __name__ == "__main__":
    list_games()
    main()
