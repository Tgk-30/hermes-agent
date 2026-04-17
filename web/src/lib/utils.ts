import { type ClassValue, clsx } from "clsx";
import { twMerge } from "tailwind-merge";

export function cn(...inputs: ClassValue[]) {
  return twMerge(clsx(inputs));
}

function formatRelativeDelta(delta: number): string {
  if (Number.isNaN(delta)) return "unknown";

  const future = delta < 0;
  const seconds = Math.abs(delta);

  if (seconds < 60) return future ? "soon" : "just now";
  if (seconds < 3600) {
    const minutes = Math.floor(seconds / 60);
    return future ? `in ${minutes}m` : `${minutes}m ago`;
  }
  if (seconds < 86400) {
    const hours = Math.floor(seconds / 3600);
    return future ? `in ${hours}h` : `${hours}h ago`;
  }
  if (seconds < 172800) return future ? "tomorrow" : "yesterday";

  const days = Math.floor(seconds / 86400);
  return future ? `in ${days}d` : `${days}d ago`;
}

/** Relative time from a Unix epoch timestamp (seconds). */
export function timeAgo(ts: number): string {
  return formatRelativeDelta(Date.now() / 1000 - ts);
}

/** Relative time from an ISO-8601 timestamp string. */
export function isoTimeAgo(iso: string): string {
  return formatRelativeDelta((Date.now() - new Date(iso).getTime()) / 1000);
}
