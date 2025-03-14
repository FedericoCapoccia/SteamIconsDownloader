import os
import sys
import string
from urllib.request import urlretrieve
import subprocess

sys.path.insert(0, os.path.abspath("deps"))
import vdf
from steam.client import SteamClient

HOME = os.getenv("HOME")
TMP = "/tmp/"

max_retry = 5
steam_icons_url = (
    "https://cdn.cloudflare.steamstatic.com/steamcommunity/public/images/apps/"
)
libinfo_dir = str(HOME) + "/.local/share/Steam/steamapps/libraryfolders.vdf"
icons_path = str(HOME) + "/.local/share/icons/hicolor/"

resolutions = [
    "16x16",
    "24x24",
    "32x32",
    "48x48",
    "64x64",
    "96x96",
    "128x128",
    "192x192",
    "256x256",
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

            for res in resolutions:
                subprocess.run(
                    [
                        "magick",
                        os.path.join(TMP, icon_filename),
                        "-thumbnail",
                        res,
                        "-alpha",
                        "on",
                        "-background",
                        "none",
                        "-flatten",
                        os.path.join(TMP, png_filename),
                    ],
                    check=True,
                )

                subprocess.run(
                    [
                        "mv",
                        "-f",
                        os.path.join(TMP, png_filename),
                        icons_path + str(res) + "/apps/" + png_filename,
                    ],
                    check=True,
                )

            os.remove(os.path.join(TMP, icon_filename))


if __name__ == "__main__":
    list_games()
    main()
