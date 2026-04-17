import assert from "node:assert/strict";
import test from "node:test";
import { sanitizeMarkdownUrl } from "../src/lib/markdownUrl.js";

test("allows safe http and https links", () => {
  assert.equal(sanitizeMarkdownUrl("https://example.com/docs"), "https://example.com/docs");
  assert.equal(sanitizeMarkdownUrl("http://example.com/docs"), "http://example.com/docs");
});

test("allows relative markdown links", () => {
  assert.equal(sanitizeMarkdownUrl("/sessions"), "/sessions");
  assert.equal(sanitizeMarkdownUrl("../logs"), "../logs");
  assert.equal(sanitizeMarkdownUrl("#status"), "#status");
});

test("blocks unsafe schemes", () => {
  assert.equal(sanitizeMarkdownUrl("javascript:alert(1)"), null);
  assert.equal(sanitizeMarkdownUrl("data:text/html;base64,PHNjcmlwdD4="), null);
  assert.equal(sanitizeMarkdownUrl("  \u0000javascript:alert(1)"), null);
});

test("blocks protocol-relative links", () => {
  assert.equal(sanitizeMarkdownUrl("//example.com/path"), null);
});
