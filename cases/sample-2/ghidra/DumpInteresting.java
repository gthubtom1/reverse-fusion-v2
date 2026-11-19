// Dump decompilation of functions that reference interesting strings.
// @category Fusion
import ghidra.app.script.GhidraScript;
import ghidra.app.decompiler.*;
import ghidra.program.model.listing.*;
import ghidra.program.model.symbol.Reference;
import ghidra.util.task.ConsoleTaskMonitor;
import java.io.*;
import java.util.*;

public class DumpInteresting extends GhidraScript {
    private static final String[] KEYS = {
        "password", "Password", "PASSWORD", "serial", "Serial", "key", "Key",
        "Enter", "enter", "Wrong", "wrong", "Correct", "correct", "invalid",
        "Invalid", "Usage", "usage", "flag", "FLAG", "Good", "good", "congrat",
        "keygen", "KeyGen", "license", "License"
    };

    public void run() throws Exception {
        String outPath = System.getenv("DUMP_OUT");
        if (outPath == null) outPath = "dump.txt";
        PrintWriter out = new PrintWriter(new FileWriter(outPath));

        DecompInterface ifc = new DecompInterface();
        ifc.openProgram(currentProgram);
        ConsoleTaskMonitor mon = new ConsoleTaskMonitor();

        Set<Function> targets = new LinkedHashSet<Function>();
        DataIterator it = currentProgram.getListing().getDefinedData(true);
        while (it.hasNext() && !mon.isCancelled()) {
            Data d = it.next();
            if (d == null) continue;
            String v;
            try { v = d.getValue() == null ? "" : d.getValue().toString(); }
            catch (Exception e) { continue; }
            if (v.length() < 3 || v.length() > 200) continue;
            boolean hit = false;
            for (String k : KEYS) if (v.contains(k)) { hit = true; break; }
            if (!hit) continue;
            Reference[] refs = getReferencesTo(d.getAddress());
            for (Reference r : refs) {
                Function f = getFunctionContaining(r.getFromAddress());
                if (f != null) targets.add(f);
            }
            out.println("STRING " + d.getAddress() + " : " + v.replace("\n", "\\n"));
        }

        out.println("\n==== FUNCTIONS: " + targets.size() + " ====");
        for (Function f : targets) {
            out.println("\n#### FUNCTION " + f.getName() + " @ " + f.getEntryPoint());
            DecompileResults res = ifc.decompileFunction(f, 60, mon);
            if (res != null && res.decompileCompleted()) {
                out.println(res.getDecompiledFunction().getC());
            } else {
                out.println("DECOMPILE FAILED: " + (res == null ? "null" : res.getErrorMessage()));
            }
        }
        out.close();
        ifc.dispose();
        println("WROTE " + outPath + " functions=" + targets.size());
    }
}
