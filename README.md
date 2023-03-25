# jellyfin-exporter-py

A very simple exporter for jellyfin written in python

## Exposed metrics

Right now, it only exposes two metrics: server info and stream info. These metrics are called `jellyfin_stream_info` and `jellyfin_server_info`

The metrics are available on <IP>:9000

## Configuration

Configuration is done via environment variables.

* `JELLYFIN_URL`: URL of the jellyfin server. Defaults to `http://localhost:8096`
* `JELLYFIN_API_KEY`: Jellyfin API key