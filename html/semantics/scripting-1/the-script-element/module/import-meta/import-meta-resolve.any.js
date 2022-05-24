// META: global=dedicatedworker-module,sharedworker-module,serviceworker-module

import { importMetaOnRootModule, importMetaOnDependentModule }
  from "./import-meta-root.js";

test(() => {
  assert_equals(typeof import.meta.resolve, "function");
  assert_equals(import.meta.resolve.name, "resolve");
  assert_equals(import.meta.resolve.length, 1);
  assert_equals(Object.getPrototypeOf(import.meta.resolve), Function.prototype);
}, "import.meta.resolve is a function with the right properties");

test(() => {
  assert_false(isConstructor(import.meta.resolve));

  assert_throws_js(TypeError, () => new import.meta.resolve("./x"));
}, "import.meta.resolve is not a constructor");

test(() => {
  // Simpler cases like 1, undefined, null will fail because they don't start
  // with ./ or look like absolute URLs.
  // TODO(domenic): test those with an import map, including the no-arg case.
  const testCases = new Map([
    [{ toString() { return "./x"; } }, "./x"],
    [{ valueOf() { return "./x"; } }, "./x"],
    [{ toString() { return "./x"; }, valueOf() { return "./y" } }, "./x"]
  ]);

  for (const [input, relativeURL] of testCases) {
    const expected = (new URL(relativeURL, import.meta.url)).href;
    assert_equals(import.meta.resolve(input), expected, input);
  }

  assert_throws_js(TypeError, () => import.meta.resolve(Symbol("./x")), "symbol");

  assert_throws_js(TypeError, () => import.meta.resolve(), "no argument (which is treated like \"undefined\")");
}, "import.meta.resolve ToString()s its argument");

test(() => {

  assert_equals(import.meta.resolve("./x"), resolveURL(import.meta, "x"), "current module import.meta");
  assert_equals(importMetaOnRootModule.resolve("./x"), resolveURL(importMetaOnRootModule, "x"), "sibling module import.meta");
  assert_equals(importMetaOnDependentModule.resolve("./x"), resolveURL(importMetaOnDependentModule, "x"), "dependency module import.meta");
}, "Relative URL-like specifier resolution");

test(() => {
  assert_equals(import.meta.resolve("https://example.com/"), "https://example.com/", "current module import.meta");
  assert_equals(importMetaOnRootModule.resolve("https://example.com/"), "https://example.com/", "sibling module import.meta");
  assert_equals(importMetaOnDependentModule.resolve("https://example.com/"), "https://example.com/", "dependency module import.meta");
}, "Absolute URL-like specifier resolution");

test(() => {
  const { resolve } = import.meta;
  assert_equals(resolve("https://example.com/"), "https://example.com/", "current module import.meta");
}, "Works fine with no this value");

function resolveURL(importMeta, relativeURL) {
  return (new URL(relativeURL, importMeta.url)).href;
}

function isConstructor(o) {
  try {
    new (new Proxy(o, { construct: () => ({}) }));
    return true;
  } catch {
    return false;
  }
}
