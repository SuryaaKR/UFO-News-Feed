from youtube_transcript_api import YouTubeTranscriptApi
import sys
import re
import json

ytt_api = YouTubeTranscriptApi()

def extract_video_id(url_or_id):
    # Try to extract video ID from URL, else return as is
    match = re.search(r"(?:v=|\/)([0-9A-Za-z_-]{11})", url_or_id)
    if match:
        return match.group(1)
    # If input is already a video ID
    if re.match(r"^[0-9A-Za-z_-]{11}$", url_or_id):
        return url_or_id
    return None

def fetch_and_trim(video_id, max_chars=17000):
    try:
        transcript_entries = ytt_api.fetch(video_id)
        # Join all transcript text into one string
        full_text = " ".join(getattr(entry, 'text', str(entry)) for entry in transcript_entries)
        # Clean: remove [Music], [Applause], etc.
        full_text = re.sub(r"\[.*?\]", "", full_text)
        full_text = re.sub(r"\s+", " ", full_text).strip()
        # Trim to max_chars
        trimmed_text = full_text[:max_chars]
        return {
            "video_id": video_id,
            "transcript": trimmed_text,
            "transcript_len": len(full_text),
            "trimmed_len": len(trimmed_text),
            "was_trimmed": len(full_text) > len(trimmed_text)
        }
    except Exception as e:
        return {"video_id": video_id, "error": str(e)}

if __name__ == "__main__":
    if len(sys.argv) < 2:
        print(json.dumps({"error": "Usage: python YT_transcripts.py <video_id_or_url1> [<video_id_or_url2> ...]"}))
        sys.exit(1)

    inputs = sys.argv[1:]
    results = []

    for inp in inputs:
        video_id = extract_video_id(inp)
        if video_id:
            results.append(fetch_and_trim(video_id))
        else:
            results.append({"input": inp, "error": "invalid_video_id"})

    # Output as JSON so n8n can parse it
    print(json.dumps(results))
