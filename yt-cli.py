import sys
import shutil
import subprocess

def get_stream_url(query):
    """Uses yt-dlp to extract direct playable stream URLs using client rotation without cookies."""
    if "youtube.com" in query or "youtu.be" in query:
        target = query
    else:
        target = f"ytsearch1:{query}"

    print(f"\033[38;5;39m[+] Resolving YouTube stream for: '{query}'...\033[0m")

    # We omit --cookies-from-browser completely to allow Android/iOS clients to return raw URLs
    cmd = [
        "yt-dlp",
        "--extractor-args", "youtube:player_client=ios,android,mweb",
        "-g",
        "-f", "bestvideo[height<=480]+bestaudio/best[height<=480]/best",
        target
    ]

    try:
        result = subprocess.run(cmd, capture_output=True, text=True, check=True)
        lines = result.stdout.strip().splitlines()
        if lines:
            # First line is video stream, second line (if present) is audio stream
            return lines
    except subprocess.CalledProcessError as e:
        print(f"[-] yt-dlp extraction failed: {e.stderr}")
        return None

def main():
    if len(sys.argv) > 1:
        query = " ".join(sys.argv[1:])
    else:
        query = input("Enter YouTube URL or Search term: ")

    if not query.strip():
        return

    stream_urls = get_stream_url(query)

    if not stream_urls:
        print("[-] Could not retrieve stream.")
        return

    print("\033[38;5;118m[+] Stream acquired! Launching ASCII Stream  (Press 'q' to quit)...\033[0m\n")

    # Prepare mpv command using raw stream links
    mpv_cmd = ["mpv", stream_urls[0], "--vo=tct", "--quiet"]
    
    # If video and audio streams are separated
    if len(stream_urls) > 1:
        mpv_cmd.append(f"--audio-file={stream_urls[1]}")

    if shutil.which("mpv"):
        subprocess.run(mpv_cmd)
    else:
        print("[-] mpv is required for terminal streaming.")

if __name__ == "__main__":
    main()