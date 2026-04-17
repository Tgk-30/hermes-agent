import { useContext } from "react";
import { I18nContext } from "./contextValue";

export function useI18n() {
  return useContext(I18nContext);
}
