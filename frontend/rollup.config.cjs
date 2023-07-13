const { spawn } = require('child_process')
const svelte = require('rollup-plugin-svelte')
const commonjs = require('@rollup/plugin-commonjs')
const terser = require('@rollup/plugin-terser')
const resolve = require('@rollup/plugin-node-resolve')
const livereload = require('rollup-plugin-livereload')
const css = require('rollup-plugin-css-only')
const autoPreprocess = require('svelte-preprocess')
const typescript = require('@rollup/plugin-typescript')
const alias = require("@rollup/plugin-alias")
const path = require('path');
const { fileURLToPath } = require("url")
const { dirname } = require("path")


const production = !process.env.ROLLUP_WATCH;

function serve() {
	let server;

	function toExit() {
		if (server) server.kill(0);
	}

	return {
		writeBundle() {
			if (server) return;
			server = spawn('npm', ['run', 'start', '--', '--dev'], {
				stdio: ['ignore', 'inherit', 'inherit'],
				shell: true
			});

			process.on('SIGTERM', toExit);
			process.on('exit', toExit);
		}
	};
}

module.exports = {
	input: "src/main.ts",
	output: {
		sourcemap: true,
		format: "iife",
		name: "app",
		file: "public/build/bundle.js",
	},

	plugins: [
		alias({
			entries: {
				"@smui": path.resolve(__dirname, "node_modules/svelte-material-ui/dist"),
			},
		}),
		typescript({ sourceMap: !production }),
		svelte({
			preprocess: autoPreprocess(),
			compilerOptions: {
				// enable run-time checks when not in production
				dev: !production,
			},
		}),
		// we'll extract any component CSS out into
		// a separate file - better for performance
		css({ output: "bundle.css" }),

		// If you have external dependencies installed from
		// npm, you'll most likely need these plugins. In
		// some cases you'll need additional configuration -
		// consult the documentation for details:
		// https://github.com/rollup/plugins/tree/master/packages/commonjs
		resolve({
			browser: true,
			dedupe: ["svelte"],
			preferBuiltins: true,
			exportConditions: ["svelte"],
		}),
		commonjs(),

		// In dev mode, call `npm run start` once
		// the bundle has been generated
		!production && serve(),

		// Watch the `public` directory and refresh the
		// browser on changes when not in production
		!production && livereload("public"),

		// If we're building for production (npm run build
		// instead of npm run dev), minify
		production && terser(),
	],
	watch: {
		clearScreen: false,
	},
};
