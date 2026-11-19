// Decompile a function by address (DUMP_ADDR) plus its callees (DUMP_DEPTH, default 1).
// @category Fusion
import ghidra.app.script.GhidraScript;
import ghidra.app.decompiler.*;
import ghidra.program.model.address.Address;
import ghidra.program.model.listing.*;
import ghidra.util.task.ConsoleTaskMonitor;
import java.io.*;
import java.util.*;

public class DumpFunction extends GhidraScript {
    private DecompInterface ifc;
    private ConsoleTaskMonitor mon;
    private PrintWriter out;
    private Set<Function> seen = new LinkedHashSet<Function>();

    private void dump(Function f, int depth) {
        if (f == null || depth < 0 || seen.contains(f)) return;
        seen.add(f);
        out.println("\n#### FUNCTION " + f.getName() + " @ " + f.getEntryPoint());
        DecompileResults res = ifc.decompileFunction(f, 90, mon);
        if (res != null && res.decompileCompleted())
            out.println(res.getDecompiledFunction().getC());
        else
            out.println("DECOMPILE FAILED");
        if (depth > 0) {
            for (Function c : f.getCalledFunctions(mon)) {
                if (c.isExternal() || seen.contains(c)) continue;
                dump(c, depth - 1);
                if (seen.size() > 40) return;
            }
        }
    }

    public void run() throws Exception {
        String outPath = System.getenv("DUMP_OUT");
        if (outPath == null) outPath = "function.txt";
        String addrStr = System.getenv("DUMP_ADDR");
        int depth = Integer.parseInt(System.getenv().getOrDefault("DUMP_DEPTH", "1"));
        out = new PrintWriter(new FileWriter(outPath));
        ifc = new DecompInterface();
        ifc.openProgram(currentProgram);
        mon = new ConsoleTaskMonitor();

        Address addr = currentProgram.getAddressFactory()
            .getDefaultAddressSpace().getAddress(addrStr);
        Function f = getFunctionContaining(addr);
        out.println("TARGET " + addrStr + " -> " +
            (f == null ? "no function" : f.getName() + " @ " + f.getEntryPoint()));
        dump(f, depth);
        out.close();
        ifc.dispose();
        println("WROTE " + outPath + " functions=" + seen.size());
    }
}
