# <div style="display: flex; align-items: center; justify-content: space-between">spotify-playlist-cloner [<img src="Spotify_Logo_RGB_Green.png" style="max-height: 100px; min-width: 70px">](Spotify_Logo_RGB_Green.png)</div>

---

## Features

- **clone / fork any Spotify playlist**
- **automatically update your cloned / forked playlists**
- **add one playlist to another**

---

## Getting Started

**Step 1**  
Clone the repo using `git clone https://github.com/smiley3307/spotify-playlist-cloner.git`

**Step 2**  
Create a new App in your [Spotify Developer Dashboard][1] and\
register `http://localhost:8888/callback` as `redirect_uri`

**Step 3**  
Create the file `config.py` in the `src` folder and add your `client_id` and `client_secret` so it looks like this

```python
client_id = "znapp8alfhn25h5tnzb7e0ax6j1axrqf"
client_secret = "1za02ax1juv6woqn33ybgn4yxf3demt5"
```

**the values used are not real values, they are for demonstration purposes only*

**Step 5**  
Enjoy!

---

## Bundle it [ with pyinstaller ]

**Step 0**  
You need to have `pyinstaller` installed for this to work  
Check if you have done everything from the [Getting Started](#Getting-Started) Section

**Step 1**  
run `pyinstaller -F src/SpotifyPlaylistCloner.py` from your project directory  
it will create the executable file in `./dist`

**Step 2**  
Now you can share your bundled file with your friends, but you might have to add their Spotify Accounts in
your [Developer Dashboard][1], so they can authorize with your `client_id`

---
&copy; 2022 smiley3307

[1]: https://developer.spotify.com/dashboard/applications
