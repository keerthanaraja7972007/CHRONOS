import { Bell, BookOpen, ChevronLeft, ChevronRight, FileWarning, GitBranch, GitPullRequest, History, LayoutDashboard, Menu, Radio, Search, Settings, ShieldAlert, Sparkles, Workflow } from "lucide-react";
import { useState } from "react";
import { NavLink, Outlet } from "react-router-dom";
import { useUI } from "../context/ui-context";
import { cn } from "../lib/utils";

const links = [
  ["/dashboard", LayoutDashboard, "Dashboard"],
  ["/repositories", GitBranch, "Repositories"],
  ["/upload", GitPullRequest, "Pull Requests"],
  ["/live-analysis", Radio, "Live Analysis"],
  ["/risk-dashboard", ShieldAlert, "Risk Dashboard"],
  ["/pre-mortems", FileWarning, "Pre-Mortem Reports"],
  ["/counter-prs", Workflow, "Counter PRs"],
  ["/runbooks", BookOpen, "Runbooks"],
  ["/history", History, "History"],
  ["/settings", Settings, "Settings"],
] as const;

export function Layout() {
  const [collapsed, setCollapsed] = useState(false);
  const [mobile, setMobile] = useState(false);
  const { searchQuery, setSearchQuery } = useUI();

  return (
    <div className="min-h-screen bg-canvas">
      <aside className={cn("fixed inset-y-0 left-0 z-30 flex border-r bg-sidebar transition-all duration-200", collapsed ? "w-[76px]" : "w-64", mobile ? "translate-x-0" : "-translate-x-full", "lg:translate-x-0")}>
        <div className="flex w-full flex-col p-3">
          <div className="mb-7 flex h-10 items-center gap-3 px-2">
            <div className="grid size-8 place-items-center rounded-lg bg-primary text-white">
              <Sparkles size={16} />
            </div>
            {!collapsed && <span className="font-semibold tracking-[.16em] text-ink">CHRONOS</span>}
          </div>
          <nav className="flex-1 space-y-1">
            {links.map(([to, Icon, label]) => (
              <NavLink key={to} to={to} end={to === "/dashboard"} onClick={() => setMobile(false)} className="nav-link" title={collapsed ? label : undefined}>
                <Icon size={18} />
                {!collapsed && <span>{label}</span>}
              </NavLink>
            ))}
          </nav>
          <div className="border-t pt-3">
            <button onClick={() => setCollapsed(!collapsed)} className="nav-link hidden w-full lg:flex">
              {collapsed ? <ChevronRight size={18} /> : <><ChevronLeft size={18} /><span>Collapse</span></>}
            </button>
            <p className={cn("px-2 pt-4 text-xs leading-5 text-muted", collapsed && "hidden")}>Engineering foresight for reliable software.</p>
          </div>
        </div>
      </aside>

      {mobile && <button className="fixed inset-0 z-20 bg-slate-950/20 lg:hidden" aria-label="Close menu" onClick={() => setMobile(false)} />}

      <div className={cn("transition-[margin] duration-200", collapsed ? "lg:ml-[76px]" : "lg:ml-64")}>
        <header className="sticky top-0 z-10 flex h-16 items-center justify-between border-b bg-white/95 px-4 backdrop-blur md:px-8">
          <button className="rounded-lg p-2 text-muted hover:bg-slate-100 lg:hidden" onClick={() => setMobile(true)}>
            <Menu size={20} />
          </button>
          <label className="relative hidden w-full max-w-sm md:block">
            <Search className="absolute left-3 top-1/2 -translate-y-1/2 text-placeholder" size={17} />
            <input
              className="w-full rounded-lg border bg-slate-50 py-2 pl-10 pr-3 text-sm placeholder:text-placeholder"
              placeholder="Search repositories, pull requests…"
              value={searchQuery}
              onChange={(event) => setSearchQuery(event.target.value)}
            />
          </label>
          <div className="ml-auto flex items-center gap-3">
            <div className="hidden items-center gap-2 text-xs text-muted sm:flex">
              <span className="size-2 rounded-full bg-success" />
              GitHub operational
            </div>
            <button className="rounded-lg p-2 text-muted hover:bg-slate-100" aria-label="Notifications">
              <Bell size={19} />
            </button>
            <button className="flex items-center gap-2 rounded-lg p-1.5 text-sm hover:bg-slate-100" aria-label="Profile menu">
              <span className="grid size-7 place-items-center rounded-full bg-blue-100 text-xs font-semibold text-primary">AM</span>
              <span className="hidden font-medium sm:block">Alex Morgan</span>
            </button>
          </div>
        </header>
        <main className="p-5 md:p-8 lg:p-10">
          <Outlet />
        </main>
      </div>
    </div>
  );
}
