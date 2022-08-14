"""
Command Cog sending back a random media (image, GIFs, videos, etc.).
"""

from aiohttp import ClientSession
from logging import getLogger
from io import BytesIO
from sys import getsizeof

from discord import ApplicationContext, File, SlashCommandGroup

from resources import get_random_media_url
from settings import BOT_COMMANDS, BOT_MAX_FILESIZE_BYTES

_MEDIA_GROUP = BOT_COMMANDS["media_group"]
_MEDIA_GROUP_NAME = _MEDIA_GROUP["name"]
_MEDIA_GROUP_DESCRIPTION = _MEDIA_GROUP.get("description")
_GET = _MEDIA_GROUP["commands"]["get"]

_logger = getLogger(__name__)

media_command_group = SlashCommandGroup(_MEDIA_GROUP_NAME, _MEDIA_GROUP_DESCRIPTION)
_command = media_command_group.command


@_command(name=_GET.get("name"), description=_GET.get("description"))
async def get_media(context: ApplicationContext) -> None:
    """Get a random media"""
    await context.defer()
    media, url = await _get_media()
    while getsizeof(media) > BOT_MAX_FILESIZE_BYTES:
        _logger.info(f"[{url}] [{getsizeof(media)}] exceeds [{BOT_MAX_FILESIZE_BYTES}]")
        media, url = await _get_media()
    await context.respond(file=File(media, url.split("/")[-1]))


async def _get_media() -> tuple[bytes, str]:
    media_url = get_random_media_url()
    media_bytes = await _download_media(media_url)
    _logger.info(f"Trying to send [{media_url}] [{getsizeof(media_bytes)}] bytes")
    return media_bytes, media_url


async def _download_media(url: str) -> bytes:
    async with ClientSession() as session:
        async with session.get(url) as response:
            return BytesIO(await response.read())
