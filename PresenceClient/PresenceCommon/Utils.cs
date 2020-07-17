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
        private static Dictionary<string, PackageInfo> info;
        static Utils()
        {
            WebClient client = new WebClient();
            string json = client.DownloadString("https://raw.githubusercontent.com/Sun-Research-University/QuestPresence/master/Resource/Applications.json");
            info = JsonConvert.DeserializeObject<Dictionary<string, PackageInfo>>(json);
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

            if (title.ProgramId == 0xffaadd23)
            {
                assets.LargeImageText = !string.IsNullOrWhiteSpace(largeImageText) ? largeImageText : title.Name;
                assets.LargeImageKey = !string.IsNullOrWhiteSpace(largeImageKey) ? largeImageKey : title.Name.ToLower().Replace(" ", "");
                assets.SmallImageText = "QuestPresence";
                presence.Details = $"{title.Name}";
            }
            else
            {
                assets.SmallImageText = "SwitchPresence-Rewritten";
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


            presence.Assets = assets;
            presence.Timestamps = time;

            return presence;
        }

        public static byte[] ReceiveExactly(Socket handler, int length = 628)
        {
            var buffer = new byte[length];
            var receivedLength = 0;
            int cnt = 0;
            while (receivedLength < length)
            {
                int nextLength = handler.Receive(buffer, receivedLength, length - receivedLength, SocketFlags.None);
                if (nextLength == 0)
                {
                    if (cnt == 3)
                        throw new SocketException();
                    else
                    {
                        cnt += 1;
                        continue;
                    }
                }
                cnt = 0;
                receivedLength += nextLength;
            }
            return buffer;
        }

        private partial class PackageInfo
        {
            public string CustomName { set; get; }
            public string Prefixure { set; get; }
        }
    }
}
