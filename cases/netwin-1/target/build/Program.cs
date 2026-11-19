using System;
namespace LicCheck.NetWin;
public static class Program {
    // license check: serial of 4 uppercase groups, XOR-sum must equal 0x2F
    public static bool ValidateSerial(string s) {
        if (string.IsNullOrEmpty(s) || s.Length != 12) return false;
        if (s[3] != '-' || s[7] != '-') return false;
        int sum = 0;
        for (int i = 0; i < s.Length; i++) {
            if (i == 3 || i == 7) continue;
            sum += s[i] ^ (i * 7);
        }
        return (sum % 256) == 0x2F;
    }
    public static int Main(string[] args) {
        var input = args.Length > 0 ? args[0] : "";
        Console.WriteLine(input.Length == 12 && ValidateSerial(input) ? "VALID" : "INVALID");
        return 0;
    }
}
