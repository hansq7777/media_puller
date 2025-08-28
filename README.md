# media_puller

Toolkit for pulling media from a user URL using [gallery-dl](https://github.com/mikf/gallery-dl).

## Installation

Use the provided batch script or run the command manually:

```batch
install_requirements.bat
```

or

```bash
pip install -r requirements.txt
```

## Configuration

* Export your browser cookies (Chrome compatible) and have the file ready.
* Choose a download directory if you enable the download archive; the file `downloaded.txt` will be saved alongside the media.
* Optional: specify a rate limit like `1M` or a sleep delay like `2` (seconds), and enable deduplication after downloads. When deduplication is on, duplicate files (determined by SHA256 hash) are removed automatically.

## Running

```batch
run_app.bat
```

or

```bash
python -m src.app
```

## Testing

```bash
pytest
```

## Troubleshooting

* Ensure `gallery-dl` is installed and available in your environment.
* When downloads fail, check the log output and your network connectivity.
* If cookies are required, confirm the file path is correct and not expired.

## Performance tuning

* Adjust the rate limit or sleep parameter to balance speed and server load.
* Disable the download archive if re-downloading content is acceptable.

## Updating

```batch
update_repo.bat
```

or

```bash
git pull
```
