// Run with: node --test tests/js/mathjax_config.test.mjs
import assert from "node:assert/strict";
import { readFileSync } from "node:fs";
import { test } from "node:test";
import vm from "node:vm";

const JS = new URL("../../src/wagtail_polymath/static/wagtail_polymath/js/", import.meta.url);
const read = (file) => readFileSync(new URL(file, JS), "utf8");

const USER_CONFIG = {
  loader: { paths: { fonts: "[mathjax]/fonts" } },
  options: { menuOptions: { settings: { speech: false, braille: false, assistiveMml: true } } },
};

function run(file, { config, window = {} } = {}) {
  const warnings = [];
  const dataset = config ? { polymathConfig: JSON.stringify(config) } : {};
  const sandbox = {
    window,
    document: { currentScript: { dataset }, getElementById: () => null },
    console: { warn: (msg) => warnings.push(msg), error() {} },
    setTimeout,
    clearTimeout,
  };
  vm.runInNewContext(read(file), sandbox);
  return { MathJax: sandbox.window.MathJax, warnings };
}

test("mathjax_init.js without config keeps polymath's defaults", () => {
  const { MathJax } = run("mathjax_init.js");
  assert.deepEqual(JSON.parse(JSON.stringify(MathJax)), { loader: { load: ["input/asciimath"] } });
});

test("mathjax_init.js deep-merges the config and keeps AsciiMath", () => {
  const { MathJax } = run("mathjax_init.js", { config: USER_CONFIG });
  assert.deepEqual([...MathJax.loader.load], ["input/asciimath"]);  // copy: the sandbox array is from another realm
  assert.equal(MathJax.loader.paths.fonts, "[mathjax]/fonts");
  assert.equal(MathJax.options.menuOptions.settings.assistiveMml, true);
});

test("the widget deep-merges the config and keeps its startup.ready hook", () => {
  const { MathJax } = run("wagtail_polymath-mathjax-widget.js", {
    config: { ...USER_CONFIG, startup: { ready: "not a function", typeset: false } },
  });
  assert.deepEqual([...MathJax.loader.load], ["input/asciimath"]);  // copy: the sandbox array is from another realm
  assert.equal(MathJax.loader.paths.fonts, "[mathjax]/fonts");
  assert.equal(MathJax.options.menuOptions.settings.speech, false);
  assert.equal(typeof MathJax.startup.ready, "function");
  assert.equal(MathJax.startup.typeset, false);
});

test("the widget warns if MathJax already loaded and config can't be applied", () => {
  const loaded = { version: "4.1.3", startup: { promise: Promise.resolve() } };
  const { MathJax, warnings } = run("wagtail_polymath-mathjax-widget.js", {
    config: USER_CONFIG,
    window: { MathJax: loaded },
  });
  assert.equal(MathJax, loaded);
  assert.equal(warnings.length, 1);
});
