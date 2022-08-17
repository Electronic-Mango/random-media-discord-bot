"""
Command Cog sending back a help message.
"""

from disnake import CommandInteraction
from disnake.ext.commands import Cog, slash_command

from bot.command.media import HELP_MESSAGE as MEDIA_HELP_MESSAGE
from bot.command.text import HELP_MESSAGE as TEXT_HELP_MESSAGE

_FULL_HELP_MESSAGE = "\n".join([MEDIA_HELP_MESSAGE.strip(), TEXT_HELP_MESSAGE.strip()])


class HelpCog(Cog):
    @slash_command(name="help", description="Get help information for the bot")
    async def media(self, interaction: CommandInteraction) -> None:
        """Send back a 'help' message"""
        await interaction.send(_FULL_HELP_MESSAGE, ephemeral=True)
