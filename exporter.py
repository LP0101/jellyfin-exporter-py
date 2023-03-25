import time
import os
from prometheus_client.core import GaugeMetricFamily, REGISTRY
from prometheus_client import start_http_server
import requests

jellyfin_url = os.getenv("JELLYFIN_URL", "http://localhost:8096")
jellyfin_api_key = os.getenv("JELLYFIN_API_KEY")

def get_streams():
    try:
        sessions = requests.get(f"{jellyfin_url}/Sessions?api_key={jellyfin_api_key}").json()
        streams = [item for item in sessions if item.get("NowPlayingItem") is not None]
    except Exception as e:
        print("Failed to get sessions")
        print(e)
        streams = []
    return streams

class JellyfinTotalStreams(object):
    def __init__(self):
        pass
    def collect(self):
        jellyfin_streams = GaugeMetricFamily("jellyfin_total_streams", "Total number of active streams", labels=["state"])
        streams = get_streams()
        streams_playing = len([item for item in streams if not item["PlayState"]["IsPaused"]])
        streams_paused = len([item for item in streams if item["PlayState"]["IsPaused"]])
        jellyfin_streams.add_metric(["playing"], streams_playing)
        jellyfin_streams.add_metric(["paused"], streams_paused)
        yield jellyfin_streams

class JellyfinTotalTranscodedStreams(object):
    def __init__(self):
        pass
    def collect(self):
        jellyfin_streams = GaugeMetricFamily("jellyfin_total_transcoded_streams", "Total number of active transcoded streams", labels=["state"])
        streams = get_streams()
        streams_playing = len([item for item in streams if not item["PlayState"]["IsPaused"] and item["PlayState"]["PlayMethod"] == "Transcode"])
        streams_paused = len([item for item in streams if item["PlayState"]["IsPaused"] and item["PlayState"]["PlayMethod"] == "Transcode"])
        jellyfin_streams.add_metric(["playing"], streams_playing)
        jellyfin_streams.add_metric(["paused"], streams_paused)
        yield jellyfin_streams

class JellyfinServerInfo(object):
    def __init__(self):
        pass
    def get_server_info(self):
        try:
            return requests.get(f"{jellyfin_url}/System/Info?api_key={jellyfin_api_key}").json()
        except Exception as e:
            print("Failed to get server info")
            print(e)
            return {}
    def collect(self):
        jellyfin_server= GaugeMetricFamily("jellyfin_server_info", "Info about the Jellyfin server", labels=["version", "os", "hostname"])
        server_info = self.get_server_info()
        jellyfin_server.add_metric([server_info.get("Version"), server_info.get("OperatingSystem"), os.uname()[1]], 1)
        yield jellyfin_server

if __name__ == "__main__":
    start_http_server(9000)
    REGISTRY.register(JellyfinTotalStreams())
    REGISTRY.register(JellyfinTotalTranscodedStreams())
    REGISTRY.register(JellyfinServerInfo())
    while True: 
        time.sleep(1)