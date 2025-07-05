# Video Uploader Agent

A command-line tool to automate video uploads to YouTube (or other platforms) using OAuth 2.0 credentials and the YouTube Data API.

![image](https://github.com/user-attachments/assets/d61a24f7-0b54-4c82-818b-fcdc2191a3a0)

## Features

* Authenticate with Google OAuth 2.0
* Upload videos with title, description, tags, and privacy settings
* Automatically create or add to playlists
* Retry on failures and log detailed upload progress
* Configurable via a JSON credentials file

## Prerequisites

* Python 3.8 or higher
* `pip` for installing dependencies

## Installation

1. **Clone the repository**

   ```bash
   git clone https://github.com/NaveenNMAK/VideoUploderAgent.git
   cd VideoUploderAgent
   ```

2. **Create a virtual environment (optional but recommended)**

   ```bash
   python3 -m venv venv
   source venv/bin/activate   # On Windows use `venv\Scripts\activate`
   ```

3. **Install dependencies**

   ```bash
   pip install -r requirements.txt
   ```

## Configuration

1. **Obtain OAuth 2.0 credentials**

   * Go to the [Google Cloud Console](https://console.cloud.google.com/) and create a new project (or select an existing one).
   * Enable the **YouTube Data API v3**.
   * Create OAuth 2.0 Client credentials for a **Desktop** application.
   * Download the JSON file and rename it to `credentials.json`.

2. **Place your credentials**

   Copy `credentials.json` into the project root directory.

3. **(Optional) Update settings**

   You can modify upload settings (e.g., default privacy, playlist ID) in `config.json`.

## Usage

Run the main script with the path to your video and metadata options:

```bash
python VideoUploaderAgent.py \
  --video "path/to/video.mp4" \
  --title "My Video Title" \
  --description "A detailed description of my video." \
  --tags "tag1,tag2,tag3" \
  --privacy public \
  --playlist "My Playlist Name"
```

### Command-line Arguments

| Argument        | Description                                        | Default    |
| --------------- | -------------------------------------------------- | ---------- |
| `--video`       | Path to the video file to upload (required)        |            |
| `--title`       | Video title                                        | `Untitled` |
| `--description` | Video description                                  | *(empty)*  |
| `--tags`        | Comma-separated list of tags                       | *(none)*   |
| `--privacy`     | Privacy status: `public`, `private`, or `unlisted` | `public`   |
| `--playlist`    | Playlist name to create/add the video to           | *(none)*   |

## Logging

Upload progress and errors are logged to `upload.log`. Review this file for troubleshooting.

## Examples

* **Basic upload**:

  ```bash
  python VideoUploaderAgent.py --video ./sample.mp4 --title "Test Upload"
  ```

* **Custom privacy and tags**:

  ```bash
  python VideoUploaderAgent.py --video ./promo.mov --title "Promo" --privacy unlisted --tags "promo,product"
  ```

## Contributing

Contributions are welcome! Please open an issue or submit a pull request.

1. Fork the repository
2. Create a feature branch (`git checkout -b feature/my-feature`)
3. Commit your changes (`git commit -m "Add my feature"`)
4. Push to branch (`git push origin feature/my-feature`)
5. Open a pull request

## License

This project is licensed under the MIT License. See [LICENSE](LICENSE) for details.

## Contact

For questions or feedback, reach out to **Naveen Nunna** at \[[nmaknaveen17@gmail.com](mailto:nmaknaveen17@gmail.com)].
