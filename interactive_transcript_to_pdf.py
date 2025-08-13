from youtube_transcript_api import YouTubeTranscriptApi
from fpdf import FPDF
import re
from typing import Optional


def extract_video_id(url_or_id: str) -> Optional[str]:
    """Extract the 11-character video ID from a URL or return the ID if provided."""
    match = re.search(r"(?:v=|\/)([0-9A-Za-z_-]{11})", url_or_id)
    if match:
        return match.group(1)
    if re.match(r"^[0-9A-Za-z_-]{11}$", url_or_id):
        return url_or_id
    return None


def fetch_transcript(video_id: str) -> str:
    """Fetch and clean the transcript text for the given video ID."""
    entries = YouTubeTranscriptApi().fetch(video_id)
    text = " ".join(getattr(entry, "text", str(entry)) for entry in entries)
    text = re.sub(r"\[.*?\]", "", text)
    text = re.sub(r"\s+", " ", text).strip()
    return text


def save_pdf(text: str, filename: str) -> None:
    """Save the provided text into a simple PDF file."""
    pdf = FPDF()
    pdf.add_page()
    pdf.set_auto_page_break(auto=True, margin=15)
    pdf.set_font("Arial", size=12)
    pdf.multi_cell(0, 10, text)
    pdf.output(filename)


def main() -> None:
    url = input("Enter a YouTube video URL or ID: ").strip()
    video_id = extract_video_id(url)
    if not video_id:
        print("Invalid YouTube URL or ID.")
        return
    try:
        transcript = fetch_transcript(video_id)
    except Exception as exc:  # noqa: BLE001
        print(f"Error fetching transcript: {exc}")
        return
    filename = f"{video_id}_transcript.pdf"
    save_pdf(transcript, filename)
    print(f"Transcript saved to {filename}")


if __name__ == "__main__":
    main()
