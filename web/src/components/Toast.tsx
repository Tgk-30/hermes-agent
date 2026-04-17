import { useEffect, useState } from "react";
import { createPortal } from "react-dom";

export function Toast({ toast }: { toast: { message: string; type: "success" | "error" } | null }) {
  const [displayToast, setDisplayToast] = useState(toast);
  const [exiting, setExiting] = useState(false);

  useEffect(() => {
    if (toast) {
      const timer = window.setTimeout(() => {
        setDisplayToast(toast);
        setExiting(false);
      }, 0);
      return () => clearTimeout(timer);
    }

    if (!displayToast) return;

    const enterExit = window.setTimeout(() => setExiting(true), 0);
    const timer = window.setTimeout(() => {
      setDisplayToast(null);
      setExiting(false);
    }, 200);
    return () => {
      clearTimeout(enterExit);
      clearTimeout(timer);
    };
  }, [toast, displayToast]);

  const current = toast ?? displayToast;
  if (!current) return null;

  // Portal to document.body so the toast escapes any ancestor stacking context
  // (e.g. <main> has `relative z-2`, which would trap z-50 below the header's z-40).
  return createPortal(
    <div
      role="status"
      aria-live="polite"
      className={`fixed top-16 right-4 z-50 border px-4 py-2.5 font-courier text-xs tracking-wider uppercase backdrop-blur-sm ${
        current.type === "success"
          ? "bg-success/15 text-success border-success/30"
          : "bg-destructive/15 text-destructive border-destructive/30"
      }`}
      style={{
        animation: exiting ? "toast-out 200ms ease-in forwards" : "toast-in 200ms ease-out forwards",
      }}
    >
      {current.message}
    </div>,
    document.body,
  );
}
