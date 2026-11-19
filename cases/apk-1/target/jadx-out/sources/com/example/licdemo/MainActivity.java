package com.example.licdemo;

import android.app.Activity;
import android.os.Bundle;
import android.widget.Button;
import android.widget.EditText;
import android.widget.TextView;

/* JADX INFO: loaded from: MainActivity.class */
public class MainActivity extends Activity {
    private static final byte[] KEY = {70, 85, 83, 73, 79, 78};

    @Override // android.app.Activity
    protected void onCreate(Bundle bundle) {
        super.onCreate(bundle);
        setContentView(2130837504);
        ((Button) findViewById(2130771968)).setOnClickListener(new 1(this, (EditText) findViewById(2130771969), (TextView) findViewById(2130771970)));
    }

    public static boolean validate(String str) {
        if (str == null || str.length() < 4) {
            return false;
        }
        long jCharAt = 0;
        for (int i = 0; i < str.length(); i++) {
            jCharAt += (long) ((str.charAt(i) & 255) ^ KEY[i % KEY.length]);
        }
        return (jCharAt & 255) == 208 && str.startsWith("FUSION");
    }
}
