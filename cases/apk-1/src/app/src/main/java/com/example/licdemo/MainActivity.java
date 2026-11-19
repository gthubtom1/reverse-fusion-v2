package com.example.licdemo;

import android.app.Activity;
import android.os.Bundle;
import android.widget.EditText;
import android.widget.Button;
import android.widget.TextView;

public class MainActivity extends Activity {
    // license serial validation (demo for Stage 6 learning target)
    // expected serial: "FUSION-2026-OK"
    private static final byte[] KEY = {0x46, 0x55, 0x53, 0x49, 0x4f, 0x4e};

    @Override
    protected void onCreate(Bundle b) {
        super.onCreate(b);
        setContentView(R.layout.activity_main);
        EditText inp = findViewById(R.id.inp);
        Button go = findViewById(R.id.go);
        TextView out = findViewById(R.id.out);
        go.setOnClickListener(new android.view.View.OnClickListener() {
            @Override public void onClick(android.view.View v) {
                String serial = inp.getText().toString().trim();
                out.setText(serial.isEmpty() ? "empty" : (validate(serial) ? "valid license" : "invalid license"));
            }
        });
    }

    // validate: xor each char with rotating KEY, fold sum -> must equal 0xD0
    public static boolean validate(String serial) {
        if (serial == null || serial.length() < 4) return false;
        long sum = 0;
        for (int i = 0; i < serial.length(); i++) {
            int c = serial.charAt(i) & 0xFF;
            int k = KEY[i % KEY.length];
            sum += (c ^ k);
        }
        return (sum & 0xFF) == 0xD0 && serial.startsWith("FUSION");
    }
}