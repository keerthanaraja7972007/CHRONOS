import { createContext, useContext, useState, type ReactNode } from "react";

type UIState = {
  selectedRepository: string | null;
  setSelectedRepository: (value: string | null) => void;
  searchQuery: string;
  setSearchQuery: (value: string) => void;
  toast: string | null;
  notify: (message: string) => void;
};

const Context = createContext<UIState | undefined>(undefined);

export function UIProvider({ children }: { children: ReactNode }) {
  const [selectedRepository, setSelectedRepository] = useState<string | null>(null);
  const [searchQuery, setSearchQuery] = useState("");
  const [toast, setToast] = useState<string | null>(null);

  const notify = (message: string) => {
    setToast(message);
    setTimeout(() => setToast(null), 3500);
  };

  return (
    <Context.Provider value={{ selectedRepository, setSelectedRepository, searchQuery, setSearchQuery, toast, notify }}>
      {children}
      {toast && (
        <div className="fixed bottom-5 right-5 z-50 rounded-xl bg-ink px-4 py-3 text-sm text-white shadow-xl">{toast}</div>
      )}
    </Context.Provider>
  );
}

export function useUI() {
  const value = useContext(Context);
  if (!value) {
    throw new Error("useUI must be used inside UIProvider");
  }
  return value;
}
