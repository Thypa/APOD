import requests
import os

api_key = "9YcMRAW7oBmRAc0Di6dwgy5Ho4nrnyLanbtm5jg6"
APOD_URL = "https://api.nasa.gov/planetary/apod?api_key=" + api_key
EPIC_URL = "https://api.nasa.gov/EPIC/api/natural?api_key=" + api_key
apod_data = requests.get(APOD_URL).json()

# get url of APOD_image, if APOD is video then use EPIC picture.
# apod == 1: image is apod, apod == 0: image is epic

if apod_data["media_type"] == "image":
    if "hdurl" in str(apod_data):
        url = apod_data["hdurl"]
    else:
        url = apod_data["url"]
    imagename = url.split("/")[len(url.split("/"))-1] # image name from link
    apod = 1
else:
    epic_data = requests.get(EPIC_URL).json()
    imgnum = str(epic_data)[17:31]
    url = imagelink = "https://api.nasa.gov/EPIC/archive/natural/" + imgnum[:4] + "/" + imgnum[4:6] + "/" + imgnum[6:8] + "/png/epic_1b_" + imgnum + ".png?api_key=" + api_key
    imagename = "epic_1b_" + imgnum + ".png"
    apod = 0

# make path so we can download to it, only needed first time

os.system("mkdir c:\\Users\\" + os.getlogin() + "\\EPICimgs")

# download the file to imagename

os.system("powershell -c Invoke-WebRequest -Uri '" + url + "' -OutFile 'c:\\Users\\" + os.getlogin() + "\\EPICimgs\\" + imagename + "\'")

bmpname = imagename.replace("png", "bmp").replace("jpg", "bmp") # make name to save bmp to

# convert to bmp

os.system("powershell -c [Reflection.Assembly]::LoadWithPartialName(\\\"System.Windows.Forms\\\"); $convertfile = new-object System.Drawing.Bitmap(\\\"c:\\Users\\" + os.getlogin() + "\\EPICimgs\\" + imagename + "\\\"); $convertfile.Save(\\\"c:\\Users\\" + os.getlogin() + "\\EPICimgs\\" + bmpname + "\\\", \\\"bmp\\\")")


# if we want to set it as wallpaper, uncomment this:

os.system("reg add \"HKEY_CURRENT_USER\Control Panel\Desktop\" /v Wallpaper /t REG_SZ /d \"c:\\Users\\" + os.getlogin() + "\\EPICimgs\\" + bmpname + "\" /f | RUNDLL32.EXE user32.dll,UpdatePerUserSystemParameters")
