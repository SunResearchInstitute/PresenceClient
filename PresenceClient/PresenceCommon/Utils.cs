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
        public static readonly Dictionary<string, OverrideInfo> QuestOverrides;
        public static readonly Dictionary<string, OverrideInfo> SwitchOverrides;
        static Utils()
        {
            WebClient client = new WebClient();
            string json = client.DownloadString("https://raw.githubusercontent.com/Sun-Research-University/PresenceClient/master/Resource/QuestApplicationOverrides.json");
            QuestOverrides = JsonConvert.DeserializeObject<Dictionary<string, OverrideInfo>>(json);

            json = client.DownloadString("https://raw.githubusercontent.com/Sun-Research-University/PresenceClient/master/Resource/SwitchApplicationOverrides.json");
            SwitchOverrides = JsonConvert.DeserializeObject<Dictionary<string, OverrideInfo>>(json);

            client.Dispose();
        }

        public static RichPresence CreateDiscordPresence(Title title, Timestamps time, string largeImageKey = "", string largeImageText = "", string smallImageKey = "", string state = "", bool useProvidedTime = true)
        {
            RichPresence presence = new RichPresence()
            {
                State = state
            }; 

            Assets assets = new Assets
            {
                SmallImageKey = smallImageKey
            };

            assets.LargeImageText = title.Name;
            if (title.ProgramId != 0xffaadd23)
            {
                assets.SmallImageText = "SwitchPresence-Rewritten";

                if (!SwitchOverrides.ContainsKey(title.Name))
                {
                    assets.LargeImageKey = $"0{title.ProgramId:x}";
                    presence.Details = $"Playing {title.Name}";
                }
                else
                {
                    OverrideInfo pkgInfo = SwitchOverrides[title.Name];
                    assets.LargeImageKey = pkgInfo.CustomKey ?? $"0{title.ProgramId:x}";

                    presence.Details = pkgInfo.CustomPrefix ?? "Playing";
                    presence.Details += $" {title.Name}";
                }
            }
            else
            {
                assets.SmallImageText = "QuestPresence";

                if (!QuestOverrides.ContainsKey(title.Name))
                {
                    assets.LargeImageKey = title.Name.ToLower().Replace(" ", "");
                    presence.Details = $"Playing {title.Name}";
                }
                else
                {
                    OverrideInfo pkgInfo = QuestOverrides[title.Name];

                    assets.LargeImageKey = pkgInfo.CustomKey ?? title.Name.ToLower().Replace(" ", "");

                    presence.Details = pkgInfo.CustomPrefix ?? "Playing";
                    presence.Details += $" {title.Name}";
                }
            }
            if (!string.IsNullOrEmpty(largeImageKey))
                assets.LargeImageKey = largeImageKey;

            if (!string.IsNullOrEmpty(largeImageText))
                assets.LargeImageText = largeImageText;

            presence.Assets = assets;
            if (useProvidedTime)
                presence.Timestamps = time;

            return presence;
        }

        public static byte[] ReceiveExactly(Socket handler, int length = 628)
        {
            byte[] buffer = new byte[length];
            int receivedLength = 0;
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

        public partial class OverrideInfo
        {
            public string CustomName { set; get; }
            public string CustomPrefix { set; get; }
            public string CustomKey { set; get; }
        }
    }
}
