# PresenceClient
Set your Discord rich presence using [SwitchPresence-Rewritten](https://github.com/Sun-Research-University/SwitchPresence-Rewritten) or [QuestPresence](https://github.com/Sun-Research-University/QuestPresence) running this app on your PC.

# Setup
Simply Create an application at the [Discord Developer Portal](https://discordapp.com/developers/applications/) call your application `Nintendo Switch`, `Oculus Quest` or whatever you would like and then enter your client ID and Device's IP into PresenceClient!<br>

If you're using QuestPresence, your icon name will be the application name in all lower capitalization with no spaces with the exception of some applications you can take a look [here](https://github.com/Sun-Research-University/PresenceClient/blob/master/Resource/QuestApplicationOverrides.json) for those exceptions, you will want to take of a note of the `CustomName` field and format using the above instructions for your icon name. Sometimes an app can have a `CustomKey` field that is filled out, you will want to use this instead of the formatted `CustomName`.

If you're using SwitchPresence, your icon name will the application title ID, these icons can be dumped from the manager app included in the SwitchPresence release, the dumped icons will be formatted for you to upload directly to your discord developer application.

Finally to connect you will need your device's IP for QuestPresence this will be on main application page and for SwitchPresence you will have to find it in the connection settings of the switch.

# Support
If you still need further asstiance you can find us on [Discord](https://link.headpat.services/discord)!
