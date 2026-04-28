import { resolve } from 'path'
import { defineConfig, externalizeDepsPlugin } from 'electron-vite'
import react from '@vitejs/plugin-react'
import type { Plugin } from 'vite'
import { loadEnv } from 'vite'

const env = loadEnv('', process.cwd(), '')

/**
 * Vite injects `crossorigin` on bundled script/link tags. With `BrowserWindow.loadFile()`
 * (`file://`), that can prevent module scripts from running, leaving a blank window.
 * Strip it only for same-folder `./assets/*` references (not font preconnect hints).
 */
function stripCrossoriginOnLocalAssetTags(): Plugin {
  return {
    name: 'scriptora-strip-local-asset-crossorigin',
    apply: 'build',
    enforce: 'post',
    transformIndexHtml: {
      order: 'post',
      handler(html) {
        return html
          .replace(
            /<script([^>]*?)\s+crossorigin(?:=["'][^"']*["'])?(\s+src=["'])(\.\/assets\/[^"']+["'])([^>]*>)/gi,
            '<script$1$2$3$4'
          )
          .replace(
            /<link([^>]*?)\s+crossorigin(?:=["'][^"']*["'])?(\s+[^>]*?href=["'])(\.\/assets\/[^"']+["'])([^>]*>)/gi,
            '<link$1$2$3$4'
          )
      }
    }
  }
}

export default defineConfig({
  main: {
    plugins: [externalizeDepsPlugin()],
    define: {
      'process.env.SCRIPTORA_USER_DATA_ROOT': JSON.stringify(env['SCRIPTORA_USER_DATA_ROOT'] ?? '')
    }
  },
  preload: {
    plugins: [externalizeDepsPlugin()]
  },
  renderer: {
    /** Project-root `public/` (e.g. scripture-search-web.json) must ship beside index.html. */
    publicDir: resolve('public'),
    resolve: {
      alias: {
        '@renderer': resolve('src/renderer/src')
      }
    },
    plugins: [react(), stripCrossoriginOnLocalAssetTags()]
  }
})
