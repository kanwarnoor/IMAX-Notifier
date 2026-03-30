# IMAX Notifier for District.in

Monitors movie ticket availability (IMAX showtimes) on District.in and sends a Discord notification when found.

## Setup

1. Install dependencies:

```bash
pip install -r requirements.txt
```

2. Make sure you have [Chrome](https://www.google.com/chrome/) installed (required for Selenium ChromeDriver).

3. Create a `.env` file in the project root with the following variables:

```env
DISCORD_WEBHOOK=https://discord.com/api/webhooks/your-webhook-url
SCRAPE_URL=https://www.district.in/movies/your-movie-url?frmtid=etarl9n_zj&fromdate=2026-04-01
LATITUDE=28.5355
LONGITUDE=77.3910
DELAY=60
NOTIFICATION=Your notification message <@discord_user_id>
```

## Usage

```bash
python index.py
```

The script polls the given URL at the specified delay interval, selects the correct date, and checks if IMAX showtimes are available. Once found, it sends a Discord webhook notification and exits.
