// Decompile the entry point and its callees (depth 2).
// @category Fusion
import ghidra.app.script.GhidraScript;
import ghidra.app.decompiler.*;
import ghidra.program.model.address.AddressIterator;
import ghidra.program.model.listing.*;
import ghidra.program.model.symbol.*;
import ghidra.util.task.ConsoleTaskMonitor;
import java.io.*;
import java.util.*;

public class DumpEntryTree extends GhidraScript {
    private DecompInterface ifc;
    private ConsoleTaskMonitor mon;
    private PrintWriter out;
    private Set<Function> seen = new LinkedHashSet<Function>();

    private void dump(Function f, int depth) {
        if (f == null || depth < 0 || seen.contains(f)) return;
        seen.add(f);
        out.println("\n#### FUNCTION " + f.getName() + " @ " + f.getEntryPoint() + " depth=" + depth);
        DecompileResults res = ifc.decompileFunction(f, 60, mon);
        if (res != null && res.decompileCompleted()) {
            out.println(res.getDecompiledFunction().getC());
        } else {
            out.println("DECOMPILE FAILED");
        }
        if (depth == 0) return;
        for (Function callee : f.getCalledFunctions(mon)) {
            if (callee.isExternal()) continue;
            dump(callee, depth - 1);
        }
    }

    public void run() throws Exception {
        String outPath = System.getenv("DUMP_OUT");
        if (outPath == null) outPath = "entry.txt";
        out = new PrintWriter(new FileWriter(outPath));
        ifc = new DecompInterface();
        ifc.openProgram(currentProgram);
        mon = new ConsoleTaskMonitor();

        Function entry = getFunctionAt(currentProgram.getEntryPoint());
        if (entry == null) {
            java.util.Iterator<Function> fit =
                currentProgram.getFunctionManager().getFunctions(true).iterator();
            if (fit.hasNext()) entry = fit.next();
        }
        out.println("ENTRY " + (entry == null ? "null" : entry.getName() + " @ " + entry.getEntryPoint()));
        dump(entry, 2);

        // Also dump functions whose address appears in .init_array / constructors
        for (Function f : currentProgram.getFunctionManager().getFunctions(true)) {
            if (f.getName().contains("main") || f.getName().contains("Main")) {
                dump(f, 2);
            }
        }
        out.close();
        ifc.dispose();
        println("WROTE " + outPath + " functions=" + seen.size());
    }
}
