# UFO News Feed

This repository is part of a locally hosted [n8n](https://n8n.io) automation project. It provides a Python utility that collects and trims YouTube transcripts so they can be consumed by downstream workflow nodes.

## Features

- Extracts a video ID from a full YouTube URL or a raw ID.
- Downloads the transcript using `youtube-transcript-api`.
- Cleans up timing markers and bracketed notes.
- Trims the text to 17,000 characters to stay within n8n payload limits.
- Outputs JSON for easy parsing in n8n.
- Includes a standalone interactive script that saves transcripts as PDFs.

## Requirements

- Python 3.8+
- `youtube-transcript-api` package (`pip install youtube-transcript-api`)

## Usage

```bash
python YT_transcripts.py <video_url_or_id1> [<video_url_or_id2> ...]
```

The script prints a JSON array describing each transcript. In a self-hosted n8n instance, an **Execute Command** node can run this script and pass its JSON output to later nodes for analysis or storage.

### Interactive PDF script

For a quick one-off transcript in PDF format, run:

```bash
python interactive_transcript_to_pdf.py
```

The script will prompt for a YouTube URL or video ID and create a `{video_id}_transcript.pdf` file in the current directory.

## Local n8n Integration

1. Place this repository on the same machine or volume as your n8n installation.
2. Within an n8n workflow, add an **Execute Command** node that runs the command shown above.
3. Use the resulting JSON to power additional workflow logic, such as summarization or posting to other services.

## License

This project is released under the MIT License.
