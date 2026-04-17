const RELATIVE_URL_PREFIX = /^(?:#|\/(?!\/)|\.{1,2}\/)/;

/**
 * Return a safe href for markdown links or null when the URL should not be rendered as a link.
 * The helper allows http/https URLs plus relative anchors and paths.
 *
 * @param {string} rawUrl
 * @returns {string | null}
 */
export function sanitizeMarkdownUrl(rawUrl) {
  const value = rawUrl.trim().replace(/[\u0000-\u001f\u007f-\u009f]/g, "");
  if (!value) return null;

  if (RELATIVE_URL_PREFIX.test(value)) {
    return value;
  }

  try {
    const url = new URL(value);
    return url.protocol === "http:" || url.protocol === "https:" ? url.href : null;
  } catch {
    return null;
  }
}
