import { motion } from "framer-motion";
import type { DebateEntry } from "../../types/api";

const colors: Record<string, string> = {
  Security: "border-red-400",
  Reliability: "border-green-500",
  Performance: "border-purple-500",
  "Cost Optimization": "border-orange-400",
  Maintainability: "border-yellow-500",
  "Risk Prediction": "border-cyan-500",
  "Incident Simulation": "border-emerald-500",
  "Pre-Mortem": "border-indigo-500",
  Rollback: "border-red-700",
  "Counter PR": "border-violet-500",
  "Final Decision": "border-slate-700",
  "PR Analysis": "border-blue-500",
};

const avatars: Record<string, string> = {
  Security: "🛡️",
  Reliability: "🧱",
  Performance: "⚡",
  "Cost Optimization": "💸",
  Maintainability: "🛠️",
  "Risk Prediction": "📈",
  "Incident Simulation": "🧪",
  "Pre-Mortem": "🧾",
  Rollback: "↩️",
  "Counter PR": "🔁",
  "Final Decision": "✅",
  "PR Analysis": "📦",
};

export function AgentBubble({ entry }: { entry: DebateEntry }) {
  return (
    <motion.article
      initial={{ opacity: 0, y: 8 }}
      animate={{ opacity: 1, y: 0 }}
      className={`card border-l-4 ${colors[entry.agent_name] ?? "border-primary"}`}
    >
      <div className="flex items-center justify-between gap-2">
        <div className="flex items-center gap-2">
          <span className="flex size-9 items-center justify-center rounded-full bg-slate-100 text-lg">{avatars[entry.agent_name] ?? "🤖"}</span>
          <b className="text-sm">{entry.agent_name}</b>
        </div>
        <span className="text-xs text-muted">{new Date(entry.timestamp).toLocaleTimeString()}</span>
      </div>
      <p className="mt-3 rounded-xl bg-slate-50 p-3 text-sm text-body">{entry.message}</p>
      <div className="mt-3 flex flex-wrap gap-2 text-xs">
        <span className="rounded bg-slate-100 px-2 py-1 capitalize">{entry.severity}</span>
        <span className="rounded bg-blue-50 px-2 py-1 text-primary">{Math.round(entry.confidence * 100)}% confidence</span>
      </div>
    </motion.article>
  );
}
