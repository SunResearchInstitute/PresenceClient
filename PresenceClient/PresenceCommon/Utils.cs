using DiscordRPC;
using Newtonsoft.Json;
using PresenceCommon.Types;
using System.Collections.Generic;
using System.Net;
using System.Net.Sockets;

namespace PresenceCommon
{
    public static class Utils
    {
        private static readonly Dictionary<string, OverrideInfo> QuestOverrides;
        private static readonly Dictionary<string, OverrideInfo> SwitchOverrides;
        static Utils()
        {
            WebClient client = new WebClient();
            string json = client.DownloadString("https://raw.githubusercontent.com/Sun-Research-University/PresenceClient/master/Resource/QuestApplicationOverrides.json");
            QuestOverrides = JsonConvert.DeserializeObject<Dictionary<string, OverrideInfo>>(json);

            json = client.DownloadString("https://raw.githubusercontent.com/Sun-Research-University/PresenceClient/master/Resource/SwitchApplicationOverrides.json");
            SwitchOverrides = JsonConvert.DeserializeObject<Dictionary<string, OverrideInfo>>(json);

            client.Dispose();
        }

        public static RichPresence CreateDiscordPresence(Title title, Timestamps time, string largeImageKey = "", string largeImageText = "", string smallImageKey = "", string state = "")
        {
            RichPresence presence = new RichPresence()
            {
                State = state
            };

            Assets assets = new Assets
            {
                SmallImageKey = smallImageKey,
            };

            if (title.ProgramId != 0xffaadd23)
            {
                assets.SmallImageText = "SwitchPresence-Rewritten";
                if (!SwitchOverrides.ContainsKey(title.Name))
                {
                    if (title.Name == "SNULL")
                    {
                        assets.LargeImageText = !string.IsNullOrWhiteSpace(largeImageText) ? largeImageText : "Home Menu";
                        assets.LargeImageKey = !string.IsNullOrWhiteSpace(largeImageKey) ? largeImageKey : $"0{0x0100000000001000:x}";
                        presence.Details = "In the home menu";
                    }
                    else
                    {
                        assets.LargeImageText = !string.IsNullOrWhiteSpace(largeImageText) ? largeImageText : title.Name;
                        assets.LargeImageKey = !string.IsNullOrWhiteSpace(largeImageKey) ? largeImageKey : $"0{title.ProgramId:x}";
                        presence.Details = $"Playing {title.Name}";
                    }
                }
                else
                {
                    OverrideInfo pkgInfo = SwitchOverrides[title.Name];
                    assets.LargeImageKey = pkgInfo.CustomKey ?? (!string.IsNullOrWhiteSpace(largeImageKey) ? largeImageKey : $"0{title.ProgramId:x}");

                    presence.Details = pkgInfo.CustomPrefix ?? "Playing";

                    if (pkgInfo.CustomName != null)
                    {
                        presence.Details += $" {pkgInfo.CustomName}";
                        assets.LargeImageText = pkgInfo.CustomName;
                    }
                    else
                    {
                        presence.Details += $" {title.Name}";
                        assets.LargeImageText = title.Name;
                    }
                }
            }
            else
            {
                assets.SmallImageText = "QuestPresence";
                if (!QuestOverrides.ContainsKey(title.Name))
                {
                    assets.LargeImageText = !string.IsNullOrWhiteSpace(largeImageText) ? largeImageText : title.Name;
                    assets.LargeImageKey = !string.IsNullOrWhiteSpace(largeImageKey) ? largeImageKey : title.Name.ToLower().Replace(" ", "");
                    presence.Details = $"Playing {title.Name}";
                }
                else
                {
                    OverrideInfo pkgInfo = QuestOverrides[title.Name];
                    assets.LargeImageKey = pkgInfo.CustomKey ?? (!string.IsNullOrWhiteSpace(largeImageKey) ? largeImageKey : title.Name.ToLower().Replace(" ", ""));

                    presence.Details = pkgInfo.CustomPrefix ?? "Playing";

                    if (pkgInfo.CustomName != null)
                    {
                        presence.Details += $" {pkgInfo.CustomName}";
                        assets.LargeImageText = pkgInfo.CustomName;
                    }
                    else
                    {
                        presence.Details += $" {title.Name}";
                        assets.LargeImageText = title.Name;
                    }
                }
            }

            presence.Assets = assets;
            presence.Timestamps = time;

            return presence;
        }

        public static byte[] ReceiveExactly(Socket handler, int length = 628)
        {
            var buffer = new byte[length];
            var receivedLength = 0;
            while (receivedLength < length)
            {
                int nextLength = handler.Receive(buffer, receivedLength, length - receivedLength, SocketFlags.None);
                if (nextLength == 0)
                {
                    throw new SocketException();
                }
                receivedLength += nextLength;
            }
            return buffer;
        }

        private partial class OverrideInfo
        {
            public string CustomName { set; get; }
            public string CustomPrefix { set; get; }
            public string CustomKey { set; get; }
        }
    }
}
