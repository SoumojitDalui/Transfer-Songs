import ytmusicapi
from ytmusicapi import YTMusic

ytmusicapi.setup_oauth('yt_oauth.json', open_browser=True)

ytmusic = YTMusic("oauth.json")
# playlistId = ytmusic.create_playlist("test", "test description")
# search_results = ytmusic.search("Oasis Wonderwall")
# ytmusic.add_playlist_items(playlistId, [search_results[0]['videoId']])