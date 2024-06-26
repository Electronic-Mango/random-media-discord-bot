# Random media Discord bot

[![CodeQL](https://github.com/Electronic-Mango/random-media-discord-bot/actions/workflows/codeql-analysis.yml/badge.svg)](https://github.com/Electronic-Mango/random-media-discord-bot/actions/workflows/codeql-analysis.yml)
[![Black](https://github.com/Electronic-Mango/random-media-discord-bot/actions/workflows/black.yml/badge.svg)](https://github.com/Electronic-Mango/random-media-discord-bot/actions/workflows/black.yml)
[![Flake8](https://github.com/Electronic-Mango/random-media-discord-bot/actions/workflows/flake8.yml/badge.svg)](https://github.com/Electronic-Mango/random-media-discord-bot/actions/workflows/flake8.yml)

A simple Discord bot sending random images, GIFs, videos and texts via Discord, build with [`disnake`](https://github.com/DisnakeDev/disnake) and [`deep_translator`](https://github.com/nidhaloff/deep-translator).



## Table of contents

- [Why? What it's for?](#why-what-its-for)
- [Requirements](#requirements)
- [Configuration](#configuration)
  - [Overwriting default values](#overwriting-default-values)
  - [Docker configuration](#docker-configuration)
  - [Storing persistent channel data](#storing-persistent-channel-data)
- [Running the bot](#running-the-bot)
  - [From source](#from-source)
  - [Docker](#docker)
- [Commands](#commands)
  - [Periodic media](#periodic-media)
  - [Text message language](#text-message-language)
  - [Deep-fried text messages](#deep-fried-text-messages)
- [Data sources](#data-sources)
  - [`url`](#url)
  - [`keys`](#keys)
  - [`headers`](#headers)
  - [`language`](#language)
  - [More examples](#more-examples)
- [Media and text size limits](#media-and-text-size-limits)



## Why? What it's for?

Memes!
At least that's what I use this bot for.
You can supply media sources for some memes and text sources for copypastas from the internet and get yourself a nice memes Discord bot.

Or you can use it to send inspirational quotes and images if it suits you more.
Or cute pictures of cats.
Overall usage can be pretty generic.

You can check my other repository [Memes Discord bot Docker deployment](https://github.com/Electronic-Mango/memes-discord-bot-docker-deployment) for an example of how you can deploy this bot to send back memes via Docker Compose.
It also uses my [Reddit API API](https://github.com/Electronic-Mango/reddit-fastapi-api) to access Reddit posts.



## Requirements

This bot was built using `Python 3.10`.
Full list of requirements is in `requirements.txt` file.



## Configuration

Necessary bot parameters are stored in a YAML file called `settings.yml` in project root.
This file is initially filled with some sensible defaults, **except Discord bot token which needs to be filled in**.

You can check it out for description of each parameter.


### Overwriting default values

Instead of modifying `settings.yml` file directly, you can supply a second file and overwrite only specific parameters there.
If a necessary value isn't found in this custom file it will be taken from `settings.yml`.

Bot will load this custom file from path defined by `CUSTOM_SETTINGS_PATH` environment variable. It can also be defined in a `.env`.

If you would like to use all default values except Discord bot token you can supply custom file such as:

```yaml
bot:
  token: your-secret-bot-token
```

Keep in mind, that when overwriting list entries entire list will be replaced, they won't be merged.


### Docker configuration

There's a `Dockerfile` in the repo, which will build a Docker image for the bot using `python:3.10-alpine` as base.

You can also use `docker-compose.yml` to build and start the container via:
```bash
docker compose up -d --build
```

`Dockerfile` will copy all YAML files from the project root into the image.
Specifically it will copy all files with `.yml` extension.

`docker-compose.yml` defines `CUSTOM_SETTINGS_PATH` environment variable as `custom_settings.yml`, so you can create and fill `custom_settings.yml` with values overwriting ones from default `settings.yml` without modifying project files.

This will require rebuilding the image every time you make a change, even to the custom one.
To get around this, you can define a mounted volume in `docker-compose.yml` with your custom settings YAML and modify value of `CUSTOM_SETTINGS_PATH` accordingly.


### Storing persistent channel data

Bot stores two types of data in its SQLite database:

1. Languages for texts per channel via `/text language set` command
2. Intervals used for periodic media per channel via `/media periodic enable` command

Default languages are not stored.
Restoring language to default removes language data about current channel from the database.
Similarly stopping periodic media removes current channel interval data.

You can configure DB location and table name via settings YAML:

```yml
db:
  # Path to SQLite DB file storing configured text language per Discord channel.
  path: channel_data.db
  # Table name within SQLite DB used for storing languages.
  languages_table_name: language
  # Table name within SQLite DB used for storing periodic media data.
  periodic_table_name: periodic
```

In case of Docker deployment you might want to store DB file in a mounted volume, rather than in the container itself.
This way data won't be lost if you recreate the container.

The stored data is channel ID and selected language, or interval.
Language and intervals are stored in separate tables for easier access.
Full tables schema is as follows:

```sql
CREATE TABLE language (
        channel_id INTEGER NOT NULL, 
        language VARCHAR NOT NULL, 
        PRIMARY KEY (channel_id)
);

CREATE TABLE periodic (
        channel_id INTEGER NOT NULL, 
        interval INTEGER NOT NULL, 
        PRIMARY KEY (channel_id)
);
```

Names of both tables can be configured settings YAML.



## Running the bot

You can run the bot from source, or in a Docker container.


### From source

 1. Create a Discord bot.
 2. Install all packages from `requirements.txt`.
 3. Fill missing values in `settings.yml` (mainly Discord bot token), or supply custom `settings.yml` file with overwriting values.
 4. Execute `src/main.py` via Python.


### Docker

 1. Create a Discord bot.
 2. Create and fill `custom_settings.yml` file with overwriting values from `settings.yml`, mainly Discord bot token.
    You can also fill `settings.yml` directly.
    Or you can modify `docker-compose.yml` to load custom `settings.yml` from a mounted volume, rather than from a file in the docker image.
 3. Run `docker compose up -d --build` in terminal.

You can skip the `--build` flag if you didn't modify the source code (or `custom_settings.yml` file).

By default, all YAML files from the project root are added to the Docker image.
If you don't want to rebuild the image every time you modify `settings.yml` or `custom_settings.yml` you can load custom one from a mounted volume.
This will require modification to `docker-compose.yml`.



## Commands

All bot commands are slash-commands.
Start typing `/` and Discord will suggest them.

All command names and descriptions can be configured through `settings.yml`, or through a custom settings YAML.
There are default values in `settings.yml` which can be used as-is.

 * `/help` - prints a simple help message describing all commands
 * `/media get` - sends back a media item (image, GIF, video, etc)
 * `/media periodic enable <interval>` - send periodic media with a given interval
 * `/media periodic disable` - stop sending periodic media
 * `/text get` - sends back a text message
 * `/text deepfried` - sends back a "deep-fried" text message
 * `/text language set <language>` - sets language of text messages, `<language>` parameter is required but autocompletion for it is enabled
 * `/text language reset` - resets language of text messages to default

Sources for media and texts are in `sources.yml` file, or whichever file is configured in settings YAML.


### Periodic media

Media items can be sent back periodically via the appropriate command.
Specified interval applies only to a given channel and can be changed between channels.
Intervals for given channel are stored in SQLite DB, alongside output text language for `text` command.


### Text message language

Setting text messages language doesn't change a source, it just translates the text received from a source.
Translation is done through [`deep_translator`](https://github.com/nidhaloff/deep-translator) and Google Translate.


### Deep-fried text messages

What does it mean?
Before a text from a source is sent back, it's translated through multiple languages, then to either original language or target language configured via `/text language set` command.

Translating between multiple different languages causes texts to be weirdly distorted and strange, which is the point of this command.

Intermediate languages can be configured via settings YAML.
It can be however many languages as you'd like, just keep in mind, that each translation does take some time.



## Data sources

Both media and texts are retrieved from external services, like REST APIs.
URLs to those APIs are defined in a sources YAML file, by default `sources.yml`, or whichever file is pointed to in settings YAML.

Sources YAML can be modified as the bot is running.
New values will be used without having to restart the bot.
YAML file is loaded every time values from it should be accessed.

Sources YAML has two main sections - `media` containing sources for media and `text` containing sources with texts.

**Sources for media should respond with URL to the media, not the media itself.**
**Sources for texts should just respond with the text itself.**

Both those section contain lists with different source items.
When appropriate command is executed a random source is selected to get data from.

**Bot assumes that each source will respond with a JSON, or will respond with needed data directly.**

Source items for both sections are pretty much the same:
|Key name|Type|Value|Optional|Default|
|-|-|-|-|-|
|`url`|string|URL to get data from|no|—|
|`keys`|list|keys where relevant data is located in received JSON|yes|raw output from source will be used|
|`headers`|list|list of headers to add to request for this source|yes|no headers will be added to requests|
|`title_keys`|list|keys used to extract filename for transmitted files|yes|—|
|`language`|string|relevant only for text sources, contains language of texts from this source|yes|english|


### `url`

It's just a URL for the source, most likely some kind of API URL.

**`url` parameter is required for all sources.**


### `keys`

List of keys where actual media/text resource is located within the JSON response.
Keys are sorted from the least to most nested within the JSON.

For example, for this JSON response:

```json
{
    "ID": "123",
    "date": "2000-01-01",
    "source": {
        "source-id": 1,
        "author": "author",
        "value": {
            "some other field": "some other value",
            "data": "the actual value which should be extracted"
        }
    }
}
```

In order to get to `the actual value which should be extracted` value within the JSON response you should define following keys:

```yaml
keys:
  - source
  - value
  - data
```

If a source returns needed value directly, not through a JSON you can define an empty list for `keys`:

```yaml
keys: []
```

Or omit `keys` parameter entirely.


### `headers`

List of HTTP headers to attach to GET request for this source.

Each header list entry has to contain two fields:
 * `name` name of the header
 * `value` value for this header

For example, these `headers` in `sources.yml`:

```yaml
headers:
  - name: Authentication-Header
    value: secret-authentication-value
  - name: Authorization-Header
    value: secret-authorization-value
```

Will cause these headers to be attached to GET request:

```json
{
    "Auth-Header": "secret-auth-value",
    "Authorization-Header": "secret-authorization-value"
}
```

You can also omit this parameter if no headers are required.


### `title_keys`

List of keys used to extract value for transmitted media filename from the JSON response.
Keys are sorted from the least to most nested within the JSON.
Resulting filename doesn't need extension.
Extension is added based on extracted URL, taken from the very end of the URL.

This field is optional, without it filename is selected based on media URL.

For example, for this JSON response:

```json
{
    "ID": "123",
    "date": "2000-01-01",
    "source": {
        "source-id": 1,
        "some other field": "some other value",
        "URL": "https://some-kind.of/some-filename.jpg",
        "title": "some kind of title"
    }
}
```

If `keys` is provided such as:

```yaml
keys:
  - source
  - URL
```

And `title_keys` is provided such as:

```yaml
title_keys:
  - source
  - title
```

Then resulting filename will use `some kind of title.jpg` as filename.
Name itself is extracted based on `title_keys`, while extension is extracted based on `keys`.

If `title_keys` is omitted, then resulting filename will be `some-filename.jpg`.
Filename is extracted only based on `keys`.

In general specifying filenames for transmitted media can be omitted.
Media itself still will be transmitted without `title_keys`, just their filenames will be based only on their URL.


### `language`

Applicable only for text sources, defines language of texts from this source.
Is used when deep-frying texts as a target language, if no target language is configured.

For example, this will mark source as english:

```yaml
language: en
```

English is also used as default, if this parameter is missing.


### More examples

You can check example `sources.yml` file in the project root for more examples of source items.



## Media and text size limits

Discord limits how large files can be sent in a message.

Max file to send is defined in settings YAML under `max_filesize_bytes`, by default it's 8MB.
If file downloaded from a source is too large a new one is selected and downloaded, until one under 8MB is found.
Keep this in mind when selecting sources, since downloading large files can slow down the bot.

Max length of text message is defined in settings YAML under `max_text_message_length`, by default it's 2000 characters.
Longer messages will be split into multiple messages, each up to `max_text_message_length` characters long.
Bot doesn't try and do this in any smart way, it just splits after `max_text_message_length` characters, so words can be split in half.
