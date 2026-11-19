// Decompile the program entry point and list its callees (no recursion).
// @category Fusion
import ghidra.app.script.GhidraScript;
import ghidra.app.decompiler.*;
import ghidra.program.model.listing.*;
import ghidra.util.task.ConsoleTaskMonitor;
import java.io.*;

public class DumpEntryOnly extends GhidraScript {
    public void run() throws Exception {
        String outPath = System.getenv("DUMP_OUT");
        if (outPath == null) outPath = "entry-only.txt";
        PrintWriter out = new PrintWriter(new FileWriter(outPath));
        DecompInterface ifc = new DecompInterface();
        ifc.openProgram(currentProgram);
        ConsoleTaskMonitor mon = new ConsoleTaskMonitor();

        Function entry = getFunctionAt(currentProgram.getEntryPoint());
        out.println("ENTRY " + (entry == null ? "null" :
            entry.getName() + " @ " + entry.getEntryPoint()));
        if (entry != null) {
            DecompileResults res = ifc.decompileFunction(entry, 60, mon);
            if (res != null && res.decompileCompleted())
                out.println(res.getDecompiledFunction().getC());
            out.println("\nCALLEES:");
            for (Function c : entry.getCalledFunctions(mon)) {
                out.println(c.getName() + " @ " + c.getEntryPoint() +
                            (c.isExternal() ? " [external]" : ""));
            }
        }
        out.close();
        ifc.dispose();
        println("WROTE " + outPath);
    }
}
