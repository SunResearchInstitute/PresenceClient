using System.Runtime.InteropServices;
using System.Text;

namespace PresenceCommon.Types
{
    public class Title
    {
        public ulong Magic { get; }
        public ulong ProgramId { get; }
        public string Name { get; }

        [StructLayout(LayoutKind.Sequential, Size = 628)]
        private struct TitlePacket
        {
            [MarshalAs(UnmanagedType.U8)]
            public ulong magic;
            [MarshalAs(UnmanagedType.U8)]
            public ulong programId;
            [MarshalAs(UnmanagedType.ByValArray, SizeConst = 612)]
            public byte[] name;
        }

        public Title(byte[] bytes)
        {
            TitlePacket title = DataHandler.ByteArrayToStructure<TitlePacket>(bytes);
            Magic = title.magic;

            if (title.programId == 0)
            {
                ProgramId = 0x0100000000001000;
                Name = "Home Menu";
            }
            else
            {
                ProgramId = title.programId;
                Name = Encoding.UTF8.GetString(title.name, 0, title.name.Length).Split('\0')[0];
            }
            if (title.programId == 0xffaadd23)
            {
                if (Utils.QuestOverrides.ContainsKey(Name) && Utils.QuestOverrides[Name].CustomName != null)
                {
                    Name = Utils.QuestOverrides[Name].CustomName;
                }
            }
            else
            {
                if (Utils.SwitchOverrides.ContainsKey(Name) && Utils.SwitchOverrides[Name].CustomName != null)
                {
                    Name = Utils.SwitchOverrides[Name].CustomName;
                }
            }
        }
    }
}
