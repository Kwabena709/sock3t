// electron.vite.config.ts
import { resolve } from "path";
import { defineConfig, externalizeDepsPlugin } from "electron-vite";
import react from "@vitejs/plugin-react";
import { loadEnv } from "vite";
var env = loadEnv("", process.cwd(), "");
function stripCrossoriginOnLocalAssetTags() {
  return {
    name: "scriptora-strip-local-asset-crossorigin",
    apply: "build",
    enforce: "post",
    transformIndexHtml: {
      order: "post",
      handler(html) {
        return html.replace(
          /<script([^>]*?)\s+crossorigin(?:=["'][^"']*["'])?(\s+src=["'])(\.\/assets\/[^"']+["'])([^>]*>)/gi,
          "<script$1$2$3$4"
        ).replace(
          /<link([^>]*?)\s+crossorigin(?:=["'][^"']*["'])?(\s+[^>]*?href=["'])(\.\/assets\/[^"']+["'])([^>]*>)/gi,
          "<link$1$2$3$4"
        );
      }
    }
  };
}
var electron_vite_config_default = defineConfig({
  main: {
    plugins: [externalizeDepsPlugin()],
    define: {
      "process.env.SCRIPTORA_USER_DATA_ROOT": JSON.stringify(env["SCRIPTORA_USER_DATA_ROOT"] ?? "")
    }
  },
  preload: {
    plugins: [externalizeDepsPlugin()]
  },
  renderer: {
    /** Project-root `public/` (e.g. scripture-search-web.json) must ship beside index.html. */
    publicDir: resolve("public"),
    resolve: {
      alias: {
        "@renderer": resolve("src/renderer/src")
      }
    },
    plugins: [react(), stripCrossoriginOnLocalAssetTags()]
  }
});
export {
  electron_vite_config_default as default
};
