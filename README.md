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
* Decide whether to keep a download archive (`downloaded.txt`) to skip already downloaded files.
* Optional: choose a rate limit and enable deduplication after downloads.

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

* Adjust the rate limit parameter to balance speed and server load.
* Disable the download archive if re-downloading content is acceptable.

## Updating

```batch
update_repo.bat
```

or

```bash
git pull
```
