/*
 * Copyright (C) 2026 Zhou Qiankang <wszqkzqk@qq.com>
 *
 * SPDX-License-Identifier: LGPL-3.0-or-later
 */

package io.github.wszqkzqk.pvzportable;

import android.app.Activity;
import android.content.Intent;
import android.os.Bundle;

import java.io.File;

/** Routes first-run users to resource import without starting the SDL runtime. */
public class LauncherActivity extends Activity {
    @Override
    protected void onCreate(Bundle savedInstanceState) {
        super.onCreate(savedInstanceState);

        File extDir = getExternalFilesDir(null);
        if (extDir != null && !extDir.exists()) extDir.mkdirs();

        Class<?> destination = hasGameResources(extDir)
            ? PvZPortableActivity.class
            : ResourceImportActivity.class;
        startActivity(new Intent(this, destination));
        finish();
    }

    private static boolean hasGameResources(File dir) {
        if (dir == null || !dir.isDirectory()) return false;
        File pak = new File(dir, "main.pak");
        File props = new File(dir, "properties");
        return pak.exists() && props.isDirectory();
    }
}
