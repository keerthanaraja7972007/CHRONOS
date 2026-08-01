import { useMutation, useQuery } from "@tanstack/react-query";
import { motion } from "framer-motion";
import { Activity, ArrowRight, BookOpen, CheckCircle2, Download, Github, LoaderCircle, Play, ShieldAlert, Sparkles, Upload as UploadIcon } from "lucide-react";
import { useEffect, useMemo, useRef, useState } from "react";
import { Link, useNavigate, useParams, useSearchParams } from "react-router-dom";
import { MetricsOverview, RiskBar, RiskPie, RiskRadar, RiskTrend } from "../components/charts/engineering-charts";
import { RiskGauge } from "../components/charts/risk-gauge";
import { ErrorState } from "../components/common/error-state";
import { Loading } from "../components/common/loading";
import { AgentBubble } from "../components/debate/agent-bubble";
import { DiffViewer } from "../components/diff/diff-viewer";
import { MarkdownViewer } from "../components/markdown/markdown-viewer";
import { Button } from "../components/ui/button";
import { Card } from "../components/ui/card";
import { useUI } from "../context/ui-context";
import { exportArtifact } from "../lib/export";
import { demoDashboard, demoIncidents, demoPullRequests, demoRepository, resetDemo } from "../services/api";
import { useSwarm } from "../hooks/use-swarm";
import type { DashboardMetrics, DebateEntry, DemoPR, Incident, SwarmRun } from "../types/api";

const Header = ({ title, copy }: { title: string; copy: string }) => (
  <header className="mb-8">
    <h1 className="page-title">{title}</h1>
    <p className="mt-2 text-sm text-body">{copy}</p>
  </header>
);

const riskBadge = (risk: string) => ({
  low: "rounded-full bg-green-50 px-2.5 py-1 text-xs text-success",
  medium: "rounded-full bg-amber-50 px-2.5 py-1 text-xs text-warning",
  high: "rounded-full bg-orange-50 px-2.5 py-1 text-xs text-warning",
  critical: "rounded-full bg-red-50 px-2.5 py-1 text-xs text-critical",
}[risk] ?? "rounded-full bg-slate-100 px-2.5 py-1 text-xs text-muted");

const formatDate = (date: string) => new Date(date).toLocaleDateString(undefined, { month: "short", day: "numeric", year: "numeric" });

const sortByRisk = (items: DemoPR[]) => [...items].sort((a, b) => {
  const order = { critical: 4, high: 3, medium: 2, low: 1 };
  return order[b.risk]-order[a.risk];
});

const ANALYSIS_STAGES = [
  { label: "Initializing Repository", detail: "Loading repository topology and dependency baseline." },
  { label: "Parsing Pull Request", detail: "Tracing changed files and impacted modules." },
  { label: "Building Dependency Graph", detail: "Modeling service and file relationships." },
  { label: "Loading Historical Incidents", detail: "Retrieving prior outage patterns and signatures." },
  { label: "Searching Vector Database", detail: "Ranking semantically similar incident records." },
  { label: "Ranking Similar Incidents", detail: "Confidence scoring historical matches." },
  { label: "Building Analysis Context", detail: "Combining repo facts with diff evidence." },
  { label: "Starting Agent Swarm", detail: "Kicking off side-by-side specialist reasoning." },
  { label: "Running Agent Debate", detail: "Cross-validating security, reliability, and cost signals." },
  { label: "Computing Risk Score", detail: "Blending domain confidence into a composite score." },
  { label: "Simulating Future Incident", detail: "Projecting blast radius and user impact." },
  { label: "Generating Pre-Mortem Report", detail: "Writing the operational incident narrative." },
  { label: "Creating Counter PR", detail: "Drafting a safer alternative remediation." },
  { label: "Building Runbook", detail: "Preparing rollback and recovery steps." },
  { label: "Final Decision", detail: "Fusing all evidence into a merge recommendation." },
] as const;

const pickRun = (run: SwarmRun) => ({
  preMortem: String(run.results["Pre-Mortem"]?.data.markdown ?? ""),
  rollback: (run.results.Rollback?.data as { steps?: string[]; trigger_conditions?: string[]; validation_steps?: string[]; escalation?: string }) ?? {},
  counter: (run.results["Counter PR"]?.data as { alternative_diff?: string; risk_delta?: string; adoption_recommendation?: string; target_files?: string[] }) ?? {},
  risk: (run.results["Risk Prediction"]?.data as { composite_score?: number; domain_scores?: Record<string, number>; confidence_interval?: number[]; explanation?: string }) ?? {},
  finalDecision: run.verdict,
});

const analysisStoryByNumber = (pr?: DemoPR) => {
  const base = { riskScore: 18, recommendation: "Merge approved", narrative: "This change is documentation-only and should ship safely after a quick review.", timeline: ["Documentation context loaded", "No affected services detected", "No rollback risk expected"], blastRadius: "Limited to engineering docs", runbook: ["No action required", "Confirm docs are published in the release notes"], summary: "No measurable runtime surface area", counterDiff: "diff --git a/docs/architecture.md b/docs/architecture.md\n@@ -1 +1 @@\n-# Checkout architecture\n+# Checkout service architecture\n", domainScores: { Security: 14, Reliability: 16, Performance: 12, Cost: 10, Maintainability: 18 } };

  if (!pr) return base;
  if (pr.number === 102) {
    return {
      riskScore: 42,
      recommendation: "Merge with caution",
      narrative: "The reservation validation adds a new guardrail, but the change introduces edge-case behavior that needs targeted validation.",
      timeline: ["Validation logic introduces a new control path", "Quiet failure mode could mask invalid requests", "Configure a focused QA check before rollout"],
      blastRadius: "Checkout and inventory reservation path",
      runbook: ["Enable metric alerts on reservation rejections", "Verify a negative quantity path cannot reach downstream checkout"],
      summary: "Medium risk, limited blast radius, and a need for careful validation coverage",
      counterDiff: "diff --git a/services/inventory/src/reservation.py b/services/inventory/src/reservation.py\n@@ -1,2 +1,4 @@\n def reserve(sku, quantity): return True\n+def validate(quantity): return quantity > 0\n+if quantity <= 0: raise ValueError('invalid quantity')\n",
      domainScores: { Security: 38, Reliability: 44, Performance: 24, Cost: 18, Maintainability: 30 },
    };
  }
  if (pr.number === 103) {
    return {
      riskScore: 67,
      recommendation: "High risk recommendation",
      narrative: "The retry scheduling path can amplify downstream payment failures and increase queue pressure during recovery.",
      timeline: ["Retry path now loops through the payment queue", "Missed bounded timeout creates persistent retry amplification", "Cashier and payment resilience become the primary concern"],
      blastRadius: "Payments, orders, and customer checkout retries",
      runbook: ["Disable the retry scheduler", "Pause the queue publisher", "Drain the retry backlog and restore a bounded backoff policy"],
      summary: "High risk due to retry amplification and possibly unbounded execution",
      counterDiff: "diff --git a/services/payments/src/retry.py b/services/payments/src/retry.py\n@@ -1,3 +1,4 @@\n from shared.queue import publish\n def retry_payment(payment): publish('payments.retry', payment)\n+def schedule_retry(payment): return retry_payment(payment)\n+if payment.status == 'terminal': return None\n",
      domainScores: { Security: 52, Reliability: 74, Performance: 64, Cost: 57, Maintainability: 48 },
    };
  }
  return {
    riskScore: 91,
    recommendation: "Block merge",
    narrative: "The queue publish path and retry policy create a dangerous auth+payment blast radius that can reconnect failures across the platform.",
    timeline: ["Unsafe publish path is introduced", "Retry policy no longer bounds the loop", "Repeated downstream errors can cascade to every order and payment event"],
    blastRadius: "Authentication, payments, inventory, and checkout orchestration",
    runbook: ["Immediately disable the new queue path", "Disable the retry policy rollout", "Rollback to the last known safe payment queue configuration"],
    summary: "Critical risk with cross-service dependency amplification and a severe production incident profile",
    counterDiff: "diff --git a/shared/queue.py b/shared/queue.py\n@@ -1 +1,3 @@\n def publish(topic, payload): return None\n+def publish_safe(topic, payload): return publish(topic, payload)\n+if topic == 'payments.retry': raise RuntimeError('blocked')\n",
    domainScores: { Security: 87, Reliability: 92, Performance: 78, Cost: 66, Maintainability: 56 },
  };
};

function AnalysisPipeline({ activeStage, completed, timestamps }: { activeStage: number; completed: number; timestamps: Record<string, string> }) {
  return (
    <div className="space-y-3">
      {ANALYSIS_STAGES.map((stage, index) => {
        const isComplete = index < completed;
        const isActive = index === activeStage;
        return (
          <div key={stage.label} className="flex items-start gap-3 rounded-xl border bg-slate-50/80 p-3">
            <div className="mt-0.5 flex size-8 items-center justify-center rounded-full border bg-white">
              {isComplete ? <CheckCircle2 size={16} className="text-success" /> : isActive ? <LoaderCircle size={16} className="animate-spin text-primary" /> : <Sparkles size={16} className="text-muted" />}
            </div>
            <div className="min-w-0 flex-1">
              <div className="flex items-center justify-between gap-3">
                <p className="text-sm font-medium text-ink">{stage.label}</p>
                <span className="text-[11px] text-muted">{timestamps[stage.label] ?? (isComplete ? "complete" : isActive ? "running" : "queued")}</span>
              </div>
              <p className="mt-1 text-xs text-body">{stage.detail}</p>
            </div>
          </div>
        );
      })}
    </div>
  );
}

export function Landing() {
  const floatingPoints = [
    { left: "8%", top: "18%", size: 16, delay: 0 },
    { left: "20%", top: "72%", size: 10, delay: 0.4 },
    { left: "32%", top: "14%", size: 12, delay: 0.8 },
    { left: "54%", top: "25%", size: 18, delay: 0.2 },
    { left: "74%", top: "12%", size: 10, delay: 1.1 },
    { left: "82%", top: "64%", size: 14, delay: 0.7 },
    { left: "92%", top: "26%", size: 8, delay: 1.4 },
  ];

  return (
    <main className="landing-page relative min-h-screen overflow-hidden bg-canvas">
      <div className="pointer-events-none absolute inset-0 overflow-hidden" aria-hidden="true">
        <div className="absolute inset-0 bg-[radial-gradient(circle_at_top_left,_rgba(59,130,246,0.12),_transparent_35%),radial-gradient(circle_at_bottom_right,_rgba(14,165,233,0.12),_transparent_30%)]" />
        {floatingPoints.map((point, index) => (
          <motion.span
            key={`${point.left}-${point.top}`}
            className="absolute rounded-full border border-white/80 bg-white/90 shadow-[0_10px_35px_rgba(59,130,246,0.18)]"
            style={{ left: point.left, top: point.top, width: point.size, height: point.size }}
            animate={{ y: [0, -18, 0], opacity: [0.45, 0.95, 0.45] }}
            transition={{ duration: 5 + index, repeat: Infinity, ease: "easeInOut", delay: point.delay }}
          />
        ))}
      </div>

      <div className="relative z-10 mx-auto max-w-6xl">
        <nav className="flex items-center justify-between p-6">
          <b className="tracking-[.18em] text-primary">CHRONOS</b>
          <Link to="/dashboard"><Button variant="secondary">Open workspace</Button></Link>
        </nav>
        <section className="grid gap-12 px-6 py-10 md:grid-cols-[1.1fr_0.9fr] md:items-center md:py-20">
          <motion.div initial={{ opacity: 0, y: 16 }} animate={{ opacity: 1, y: 0 }}>
            <p className="eyebrow">AI-native engineering</p>
            <h1 className="mt-4 max-w-2xl text-5xl font-semibold tracking-tight text-ink md:text-6xl">We write tomorrow’s incident report today.</h1>
            <p className="mt-6 max-w-xl text-lg leading-8 text-body">CHRONOS transforms each pull request into grounded reliability intelligence with a calm, premium engineering workflow.</p>
            <div className="mt-8 flex flex-wrap gap-3">
              <Link to="/upload"><Button><Play size={16} className="mr-2" />Try demo mode</Button></Link>
              <Button variant="secondary" onClick={() => window.location.assign("/api/v1/auth/github")}><Github size={16} className="mr-2" />Connect GitHub</Button>
            </div>
            <div className="mt-8 flex flex-wrap gap-3 text-sm text-muted">
              <span className="rounded-full bg-white/80 px-3 py-1 shadow-sm">Live PR analysis</span>
              <span className="rounded-full bg-white/80 px-3 py-1 shadow-sm">Incident forecasting</span>
              <span className="rounded-full bg-white/80 px-3 py-1 shadow-sm">Rollback-ready runbooks</span>
            </div>
          </motion.div>

          <motion.div initial={{ opacity: 0, y: 20 }} animate={{ opacity: 1, y: 0 }} transition={{ delay: 0.1 }}>
            <Card className="border-white/70 bg-white/75 p-7 shadow-[0_35px_100px_-40px_rgba(37,99,235,0.45)] backdrop-blur-xl">
              <p className="font-medium text-primary">Offline engineering intelligence</p>
              <div className="mt-6 space-y-3">{["Repository context assembled", "Historical incidents retrieved", "Specialist agents debating", "Rollback plan prepared"].map((item, index) => <motion.p initial={{ opacity: 0, x: 8 }} animate={{ opacity: 1, x: 0 }} transition={{ delay: index * 0.12 }} key={item} className="rounded-xl bg-slate-50/90 p-3 text-sm text-body shadow-sm">● {item}</motion.p>)}</div>
            </Card>
          </motion.div>
        </section>
      </div>
    </main>
  );
}

export function Dashboard() {
  const prs = useQuery({ queryKey: ["demo-prs"], queryFn: demoPullRequests });
  const dash = useQuery({ queryKey: ["dashboard"], queryFn: demoDashboard });
  const { searchQuery } = useUI();

  const filteredPrs = useMemo(() => {
    const terms = searchQuery.trim().toLowerCase();
    if (!terms) {
      return sortByRisk(prs.data ?? []);
    }
    return sortByRisk((prs.data ?? []).filter((item) => `${item.number} ${item.title} ${item.author} ${item.risk}`.toLowerCase().includes(terms)));
  }, [prs.data, searchQuery]);

  if (prs.isLoading || dash.isLoading) {
    return <Loading />;
  }
  if (prs.isError || dash.isError) {
    return <ErrorState message={(prs.error ?? dash.error)?.message ?? "Unable to load dashboard"} />;
  }

  const dashboard = dash.data as DashboardMetrics;
  const stats = dashboard.statistics;
  const recent = dashboard.recent_analyses ?? [];
  const trend = dashboard.risk_trend ?? [];
  const radarData = [
    { subject: "Security", score: Math.max(60, stats.high_risk * 3), fullMark: 100 },
    { subject: "Reliability", score: 74, fullMark: 100 },
    { subject: "Performance", score: 42, fullMark: 100 },
    { subject: "Cost", score: 56, fullMark: 100 },
    { subject: "Maintainability", score: 64, fullMark: 100 },
  ];

  return (
    <>
      <Header title="Engineering foresight" copy="Offline repository intelligence and pre-merge risk analysis." />
      <MetricsOverview metrics={[
        { label: "Repositories", value: String(stats.repositories) },
        { label: "High-risk analyses", value: String(stats.high_risk), tone: "text-critical" },
        { label: "Indexed files", value: String(stats.indexed_files) },
        { label: "Historical incidents", value: String(stats.incidents) },
      ]} />

      <div className="mt-6 grid gap-6 xl:grid-cols-[1.3fr_1fr]">
        <Card>
          <div className="flex items-center justify-between">
            <div>
              <h2 className="font-semibold">Weekly risk trend</h2>
              <p className="mt-1 text-sm text-muted">Dynamic risk progression across recent analyses.</p>
            </div>
            <span className="rounded-full bg-blue-50 px-2.5 py-1 text-xs font-medium text-primary">Last 30 days</span>
          </div>
          <div className="mt-4 h-72"><RiskTrend data={trend} /></div>
        </Card>
        <Card>
          <h2 className="font-semibold">Quick actions</h2>
          <div className="mt-4 space-y-3">
            <Link to="/upload" className="block rounded-xl border p-3 text-sm hover:border-primary">Analyze the latest pull request</Link>
            <Link to="/risk-dashboard" className="block rounded-xl border p-3 text-sm hover:border-primary">Open engineering analytics</Link>
            <Link to="/history" className="block rounded-xl border p-3 text-sm hover:border-primary">Review historical outcomes</Link>
          </div>
        </Card>
      </div>

      <div className="mt-6 grid gap-6 xl:grid-cols-[1.15fr_1fr]">
        <Card>
          <h2 className="font-semibold">All pull requests</h2>
          <div className="mt-4 grid gap-3">
            {filteredPrs.map((pr) => (
              <Link className="flex items-center justify-between rounded-lg border p-4 hover:border-primary" to={`/analysis/${pr.number}`} key={pr.number}>
                <div>
                  <b>{pr.title}</b>
                  <div className="mt-1 flex flex-wrap items-center gap-2 text-xs text-muted">
                    <span>#{pr.number}</span><span>·</span><span>{pr.author}</span><span>·</span><span>{formatDate(pr.date)}</span>
                  </div>
                </div>
                <div className="flex items-center gap-2">
                  <span className={riskBadge(pr.risk)}>{pr.risk}</span>
                  <ArrowRight className="text-muted" size={15} />
                </div>
              </Link>
            ))}
          </div>
        </Card>
        <Card>
          <h2 className="font-semibold">Recent activity</h2>
          <div className="mt-4 space-y-4">{((recent.length ? recent : dashboard.high_risk_prs) as Array<any>).slice(0, 6).map((item, index) => <div className="flex gap-3" key={`${item.number ?? index}-${item.title ?? item.id ?? index}`}><span className="mt-1.5 size-2 rounded-full bg-primary" /><div><p className="text-sm font-medium">{item.title ?? `PR #${item.number}`}</p><p className="mt-0.5 text-xs text-muted">{item.author ?? "demo"} · {item.decision ?? item.risk ?? item.risk_score ?? "analysis"}</p></div></div>)}</div>
        </Card>
      </div>

      <div className="mt-6 grid gap-6 xl:grid-cols-2">
        <Card>
          <h2 className="font-semibold">Domain mix</h2>
          <div className="mt-4"><RiskRadar data={radarData} /></div>
        </Card>
        <Card>
          <h2 className="font-semibold">Risk distribution</h2>
          <div className="mt-4"><RiskPie data={[{ name: "High", value: stats.high_risk }, { name: "Medium", value: Math.max(1, stats.analyses - stats.high_risk) }, { name: "Low", value: Math.max(1, Math.floor(stats.indexed_files / 10)) }]} /></div>
        </Card>
      </div>
    </>
  );
}

export function Repository() {
  const repo = useQuery({ queryKey: ["repository"], queryFn: demoRepository });
  const incidents = useQuery({ queryKey: ["demo-incidents"], queryFn: demoIncidents });

  if (repo.isLoading || incidents.isLoading) {
    return <Loading />;
  }
  if (repo.isError || incidents.isError) {
    return <ErrorState message={(repo.error ?? incidents.error)?.message ?? "Repository intelligence unavailable"} />;
  }

  const repositoryData = repo.data as { name: string; files: string[]; file_count: number };
  const incidentRows = (incidents.data as Incident[]) ?? [];
  const topFiles = repositoryData.files.slice(0, 12);
  const riskMap = incidentRows.map((item) => ({ name: item.affected_files[0] ?? item.title, value: item.severity === "critical" ? 95 : item.severity === "high" ? 82 : 60 }));

  return (
    <>
      <Header title={repositoryData.name} copy="Engineering intelligence dashboard for the monitored repository." />
      <div className="grid gap-4 md:grid-cols-4">
        <Card><b className="text-3xl">{repositoryData.file_count}</b><p className="text-sm text-muted">Files</p></Card>
        <Card><b className="text-3xl">{incidentRows.length}</b><p className="text-sm text-muted">Incident locations</p></Card>
        <Card><b className="text-3xl">7</b><p className="text-sm text-muted">Services</p></Card>
        <Card><b className="text-3xl">94%</b><p className="text-sm text-muted">Readiness score</p></Card>
      </div>
      <div className="mt-6 grid gap-6 xl:grid-cols-2">
        <Card>
          <h2 className="font-semibold">Repository service graph</h2>
          <div className="mt-4 grid gap-2">{["auth → payments", "payments → checkout", "orders → inventory", "notifications → shipping"].map((edge) => <div key={edge} className="rounded-lg bg-slate-50 px-3 py-2 text-sm text-body">{edge}</div>)}</div>
        </Card>
        <Card>
          <h2 className="font-semibold">Risky files</h2>
          <div className="mt-4 grid gap-2">{riskMap.slice(0, 6).map((item) => <div key={item.name} className="flex items-center justify-between rounded-lg border px-3 py-2 text-sm"><span>{item.name}</span><span className="text-primary">{item.value}%</span></div>)}</div>
        </Card>
      </div>
      <div className="mt-6 grid gap-6 xl:grid-cols-[1.15fr_1fr]">
        <Card>
          <h2 className="font-semibold">Directory structure</h2>
          <div className="mt-4 max-h-[420px] overflow-auto rounded-xl bg-slate-950 p-4 font-mono text-xs text-slate-100">{topFiles.map((file) => <div key={file}>{file}</div>)}</div>
        </Card>
        <Card>
          <h2 className="font-semibold">Incident heatmap</h2>
          <div className="mt-4"><RiskBar data={riskMap.slice(0, 6).map((item) => ({ name: item.name.split("/").at(-1) ?? item.name, score: item.value }))} /></div>
        </Card>
      </div>
    </>
  );
}

export function Upload() {
  const prs = useQuery({ queryKey: ["demo-prs"], queryFn: demoPullRequests });
  const navigate = useNavigate();
  const { searchQuery } = useUI();

  const filtered = useMemo(() => {
    const terms = searchQuery.trim().toLowerCase();
    if (!terms) {
      return sortByRisk(prs.data ?? []);
    }
    return sortByRisk((prs.data ?? []).filter((pr) => `${pr.number} ${pr.title} ${pr.author} ${pr.risk}`.toLowerCase().includes(terms)));
  }, [prs.data, searchQuery]);

  if (prs.isLoading) {
    return <Loading />;
  }
  if (prs.isError) {
    return <ErrorState message={prs.error.message} />;
  }

  return (
    <>
      <Header title="Analyze a pull request" copy="Choose a seeded pull request to run the complete offline pipeline." />
      <Card>
        <div className="grid gap-3 md:grid-cols-2 lg:grid-cols-3">
          {(filtered ?? []).map((pr) => (
            <button key={pr.number} onClick={() => navigate(`/analysis/${pr.number}`)} className="rounded-xl border p-4 text-left hover:border-primary">
              <div className="flex items-start justify-between gap-3">
                <div>
                  <b>{pr.title}</b>
                  <p className="mt-1 text-sm text-muted">#{pr.number} · {pr.author}</p>
                </div>
                <span className={riskBadge(pr.risk)}>{pr.risk}</span>
              </div>
              <p className="mt-2 text-xs text-body">{pr.short_description}</p>
            </button>
          ))}
        </div>
        <label className="mt-6 block rounded-xl border-2 border-dashed p-8 text-center text-sm text-muted">
          <UploadIcon className="mx-auto mb-2" />
          Demo Mode ships with all seeded PRs and a full offline analysis pipeline.
        </label>
      </Card>
    </>
  );
}

export function Analysis() {
  const { number } = useParams();
  const [searchParams] = useSearchParams();
  const numberValue = Number(number ?? searchParams.get("pr") ?? 104);
  const prsQuery = useQuery({ queryKey: ["demo-prs"], queryFn: demoPullRequests });
  const swarm = useSwarm();
  const [pipelineIndex, setPipelineIndex] = useState(0);
  const [pipelineRunning, setPipelineRunning] = useState(false);
  const [stageTimestamps, setStageTimestamps] = useState<Record<string, string>>({});
  const timerRef = useRef<number | undefined>(undefined);
  const selectedPR = (prsQuery.data ?? []).find((pr) => pr.number === numberValue);

  useEffect(() => {
    if (!pipelineRunning) {
      if (timerRef.current) {
        window.clearInterval(timerRef.current);
      }
      return;
    }

    const activeStage = ANALYSIS_STAGES[pipelineIndex] ?? ANALYSIS_STAGES[0];
    setStageTimestamps((current) => ({ ...current, [activeStage.label]: new Date().toLocaleTimeString() }));

    timerRef.current = window.setInterval(() => {
      setPipelineIndex((current) => Math.min(current + 1, ANALYSIS_STAGES.length - 1));
    }, 650);

    return () => {
      if (timerRef.current) {
        window.clearInterval(timerRef.current);
      }
    };
  }, [pipelineRunning, pipelineIndex]);

  const startSwarm = async () => {
    setStageTimestamps({});
    setPipelineIndex(0);
    setPipelineRunning(true);
    try {
      await swarm.mutateAsync(numberValue);
    } finally {
      setPipelineRunning(false);
    }
  };

  if (prsQuery.isLoading) {
    return <Loading />;
  }
  if (prsQuery.isError) {
    return <ErrorState message={prsQuery.error.message} />;
  }

  return (
    <>
      <Header title="Live analysis" copy="Execute the offline agent swarm with repository and incident context." />
      {selectedPR && <Card className="mb-6"><div className="flex flex-wrap items-center justify-between gap-3"><div><p className="text-sm font-semibold">Selected PR #{selectedPR.number}</p><p className="text-sm text-muted">{selectedPR.title}</p></div><span className={riskBadge(selectedPR.risk)}>{selectedPR.risk}</span></div></Card>}
      {!swarm.data && !swarm.isPending && !pipelineRunning && <Card className="grid gap-4 lg:grid-cols-[1fr_auto] lg:items-start"><div><p className="eyebrow">AI reasoning pipeline</p><p className="mt-2 text-sm text-body">The workflow stages every step in sequence to feel like multiple senior engineers are reasoning through the change.</p><div className="mt-4"><AnalysisPipeline activeStage={pipelineIndex} completed={Math.min(pipelineIndex, ANALYSIS_STAGES.length - 1)} timestamps={stageTimestamps} /></div></div><div className="flex items-start"><Button onClick={startSwarm}><Activity size={16} className="mr-2" />Start agent swarm</Button></div></Card>}
      {(swarm.isPending || pipelineRunning) && <Card className="grid gap-6 lg:grid-cols-[1fr_1fr]"><div><p className="eyebrow">Streaming workflow</p><div className="mt-3 rounded-xl border bg-slate-50 p-4"><div className="flex items-center gap-2 text-sm text-primary"><LoaderCircle size={14} className="animate-spin" /> <span>{ANALYSIS_STAGES[pipelineIndex]?.label}</span></div><p className="mt-2 text-sm text-body">{ANALYSIS_STAGES[pipelineIndex]?.detail}</p><div className="mt-3 flex gap-1"><span className="h-2 w-2 animate-pulse rounded-full bg-primary" /><span className="h-2 w-2 animate-pulse rounded-full bg-primary/70" /><span className="h-2 w-2 animate-pulse rounded-full bg-primary/40" /></div></div></div><div><AnalysisPipeline activeStage={pipelineIndex} completed={pipelineIndex} timestamps={stageTimestamps} /></div></Card>}
      {swarm.isError && <ErrorState message={swarm.error.message} />}
      {swarm.data && <AnalysisResult run={swarm.data} pr={selectedPR} />}
    </>
  );
}

function DebateStream({ entries }: { entries: DebateEntry[] }) {
  const [visibleEntries, setVisibleEntries] = useState<DebateEntry[]>([]);
  const [typingIndex, setTypingIndex] = useState(0);
  const [typingText, setTypingText] = useState("");
  const scrollRef = useRef<HTMLDivElement | null>(null);

  useEffect(() => {
    setVisibleEntries([]);
    setTypingIndex(0);
    setTypingText("");
  }, [entries.length, entries[0]?.sequence]);

  useEffect(() => {
    if (typingIndex >= entries.length) {
      return;
    }

    const entry = entries[typingIndex];
    let current = 0;
    const timer = window.setInterval(() => {
      current += 1;
      setTypingText(entry.message.slice(0, current));
      if (current >= entry.message.length) {
        window.clearInterval(timer);
        setVisibleEntries((previous) => [...previous, entry]);
        setTypingIndex((previous) => previous + 1);
      }
    }, 16);

    return () => window.clearInterval(timer);
  }, [typingIndex, entries]);

  useEffect(() => {
    if (scrollRef.current) {
      scrollRef.current.scrollTop = scrollRef.current.scrollHeight;
    }
  }, [visibleEntries.length, typingText]);

  const activeEntry = entries[typingIndex];

  return (
    <div ref={scrollRef} className="mt-4 max-h-[420px] space-y-3 overflow-auto pr-1">
      {visibleEntries.map((entry) => <AgentBubble key={`${entry.sequence}-${entry.agent_name}`} entry={entry} />)}
      {activeEntry && (
        <motion.article initial={{ opacity: 0, y: 8 }} animate={{ opacity: 1, y: 0 }} className="card border-l-4 border-primary">
          <div className="flex items-center justify-between gap-2">
            <div className="flex items-center gap-2">
              <span className="flex size-9 items-center justify-center rounded-full bg-slate-100 text-lg">🤖</span>
              <b className="text-sm">{activeEntry.agent_name}</b>
            </div>
            <span className="text-xs text-muted">typing…</span>
          </div>
          <p className="mt-3 rounded-xl bg-slate-50 p-3 text-sm text-body">{typingText || "…"}</p>
        </motion.article>
      )}
    </div>
  );
}

function AnalysisResult({ run, pr }: { run: SwarmRun; pr?: DemoPR }) {
  const details = pickRun(run);
  const story = analysisStoryByNumber(pr);
  const metrics = details.risk?.domain_scores ?? story.domainScores;
  const confidence = details.risk?.confidence_interval ?? [72, 94];
  const exportBody = `${pr?.title ?? "analysis"}\n\n${details.preMortem}`;
  const originalRisk = Math.max(18, Math.min(91, run.verdict.final_risk_score + 12));
  const counterRisk = Math.max(8, originalRisk - Math.round((originalRisk * 0.72)));
  const improvement = Math.round(((originalRisk - counterRisk) / originalRisk) * 100);

  return (
    <div className="grid gap-6">
      <div className="grid gap-4 lg:grid-cols-[0.9fr_1.1fr]">
        <Card className="flex justify-center"><RiskGauge value={run.verdict.final_risk_score} /></Card>
        <Card>
          <p className="eyebrow">Final decision</p>
          <motion.h2 initial={{ opacity: 0, y: 8 }} animate={{ opacity: 1, y: 0 }} className="mt-2 text-2xl font-semibold">{run.verdict.verdict}</motion.h2>
          <p className="mt-2 text-sm text-body">{run.verdict.executive_summary}</p>
          <div className="mt-4 rounded-xl bg-slate-50 p-4 text-sm text-body">
            <p className="font-medium text-ink">Narrative outcome</p>
            <p className="mt-2">{story.narrative}</p>
          </div>
          <div className="mt-4 flex flex-wrap gap-2">
            <button className="rounded-lg bg-slate-100 px-3 py-2 text-xs" onClick={() => exportArtifact(pr?.title ?? "analysis", exportBody, "markdown")}>Export markdown</button>
            <button className="rounded-lg bg-slate-100 px-3 py-2 text-xs" onClick={() => exportArtifact(pr?.title ?? "analysis", exportBody, "pdf")}>Export PDF</button>
            <button className="rounded-lg bg-slate-100 px-3 py-2 text-xs" onClick={() => exportArtifact(pr?.title ?? "analysis", JSON.stringify(run, null, 2), "json")}>Export JSON</button>
          </div>
        </Card>
      </div>

      <motion.div initial={{ opacity: 0, y: 10 }} animate={{ opacity: 1, y: 0 }} className="grid gap-4 lg:grid-cols-[1fr_1.1fr]">
        <Card>
          <p className="eyebrow">Result screen</p>
          <div className="mt-4 space-y-3 text-sm">
            <div className="rounded-xl bg-slate-50 p-3"><span className="text-muted">Original Risk Score</span><div className="mt-1 text-2xl font-semibold text-ink">{originalRisk}</div></div>
            <div className="rounded-xl bg-slate-50 p-3"><span className="text-muted">Counter PR Applied</span><div className="mt-1 text-lg font-semibold text-primary">{story.recommendation}</div></div>
            <div className="rounded-xl bg-slate-50 p-3"><span className="text-muted">Updated Risk Score</span><div className="mt-1 text-2xl font-semibold text-success">{counterRisk}</div></div>
            <div className="rounded-xl bg-slate-50 p-3"><span className="text-muted">Percentage Improvement</span><div className="mt-1 text-2xl font-semibold text-warning">{improvement}%</div></div>
          </div>
        </Card>
        <Card>
          <p className="eyebrow">What changed?</p>
          <div className="mt-4 space-y-3">
            {story.timeline.map((point) => (
              <div key={point} className="flex items-start gap-3 rounded-xl border p-3">
                <span className="mt-1 h-2.5 w-2.5 rounded-full bg-primary" />
                <p className="text-sm text-body">{point}</p>
              </div>
            ))}
          </div>
        </Card>
      </motion.div>

      <div className="grid gap-6 xl:grid-cols-2">
        <Card>
          <h2 className="font-semibold">Live debate</h2>
          <DebateStream entries={run.debate_log} />
        </Card>
        <Card>
          <h2 className="font-semibold">Pre-mortem report</h2>
          <div className="mt-4"><MarkdownViewer value={details.preMortem || `# Pre-mortem\n\n${story.summary}`} /></div>
        </Card>
      </div>
      <div className="grid gap-6 xl:grid-cols-2">
        <Card>
          <h2 className="font-semibold">Risk breakdown</h2>
          <div className="mt-4"><RiskRadar data={Object.entries(metrics).map(([key, value]) => ({ subject: key, score: value, fullMark: 100 }))} /></div>
          <div className="mt-3 text-sm text-body"><b>Confidence interval:</b> {confidence[0]}% - {confidence[1]}%</div>
        </Card>
        <Card>
          <h2 className="font-semibold">Operational runbook</h2>
          <div className="mt-3 grid gap-4 md:grid-cols-2">
            <ul className="list-inside list-disc text-sm text-body">{((details.rollback.trigger_conditions ?? story.runbook).slice(0, 3)).map((item) => <li key={item}>{item}</li>)}</ul>
            <ol className="list-inside list-decimal text-sm text-body">{((details.rollback.steps ?? story.runbook).slice(0, 3)).map((item) => <li key={item}>{item}</li>)}</ol>
          </div>
        </Card>
      </div>
    </div>
  );
}

export function RiskDashboard() {
  const [searchParams] = useSearchParams();
  const number = Number(searchParams.get("pr") ?? 104);
  const prsQuery = useQuery({ queryKey: ["demo-prs"], queryFn: demoPullRequests });
  const selectedPR = (prsQuery.data ?? []).find((pr) => pr.number === number);

  if (prsQuery.isLoading) {
    return <Loading />;
  }
  if (prsQuery.isError) {
    return <ErrorState message={prsQuery.error.message} />;
  }

  const story = analysisStoryByNumber(selectedPR);
  const basis = Math.max(16, story.riskScore);
  const confidence = selectedPR?.risk === "critical" ? 93 : selectedPR?.risk === "high" ? 82 : selectedPR?.risk === "medium" ? 74 : 68;
  const radarData = Object.entries(story.domainScores).map(([subject, score]) => ({ subject, score, fullMark: 100 }));
  const pieData = [
    { name: "Security", value: Math.round(story.domainScores.Security * 0.85) },
    { name: "Reliability", value: Math.round(story.domainScores.Reliability * 0.78) },
    { name: "Performance", value: Math.round(story.domainScores.Performance * 0.72) },
    { name: "Cost", value: Math.round(story.domainScores.Cost * 0.68) },
    { name: "Maintainability", value: Math.round(story.domainScores.Maintainability * 0.7) },
  ];
  const trendData = [
    { week: "W1", score: Math.max(10, basis - 10) },
    { week: "W2", score: Math.max(18, basis - 6) },
    { week: "W3", score: Math.max(20, basis + 4) },
    { week: "W4", score: Math.max(22, basis + 8) },
    { week: "W5", score: Math.max(24, basis + 3) },
    { week: "W6", score: basis },
  ];

  return (
    <>
      <Header title="Risk dashboard" copy="Engineering analytics, domain breakdown, and operational insight for the selected PR." />
      <MetricsOverview metrics={[{ label: "Overall risk", value: String(basis) }, { label: "Confidence score", value: `${confidence}%` }, { label: "Incident probability", value: `${Math.max(34, basis - 6)}%` }, { label: "Estimated blast radius", value: story.blastRadius }]} />
      <div className="mt-6 grid gap-6 xl:grid-cols-2">
        <Card>
          <h2 className="font-semibold">Domain breakdown</h2>
          <div className="mt-4 h-72"><RiskRadar data={radarData} /></div>
        </Card>
        <Card>
          <h2 className="font-semibold">Risk distribution</h2>
          <div className="mt-4 h-72"><RiskPie data={pieData} /></div>
        </Card>
      </div>
      <div className="mt-6 grid gap-6 xl:grid-cols-[1.15fr_1fr]">
        <Card>
          <h2 className="font-semibold">Historical trend</h2>
          <div className="mt-4 h-72"><RiskTrend data={trendData} /></div>
        </Card>
        <Card>
          <h2 className="font-semibold">Recommendation</h2>
          <p className="mt-4 text-sm text-body">{story.narrative}</p>
          <div className="mt-4"><Link to={`/analysis/${number}`}><Button><Activity size={16} className="mr-2" />Run new analysis</Button></Link></div>
        </Card>
      </div>
    </>
  );
}

export function PreMortems() {
  const [searchParams] = useSearchParams();
  const number = Number(searchParams.get("pr") ?? 104);
  const prsQuery = useQuery({ queryKey: ["demo-prs"], queryFn: demoPullRequests });
  const swarm = useSwarm();

  if (prsQuery.isLoading) {
    return <Loading />;
  }
  if (prsQuery.isError) {
    return <ErrorState message={prsQuery.error.message} />;
  }

  const selectedPR = (prsQuery.data ?? []).find((pr) => pr.number === number);
  if (!swarm.data) {
    return <><Header title="Pre-mortem report" copy="Generate a production-ready incident report for the selected PR." /><Card><Button onClick={() => swarm.mutate(number)}><ShieldAlert size={16} className="mr-2" />Generate report</Button></Card></>;
  }

  const details = pickRun(swarm.data);
  const markdown = details.preMortem;

  return (
    <>
      <Header title="Pre-mortem report" copy="Executive-ready incident analysis for the selected pull request." />
      <Card>
        <div className="flex flex-wrap gap-3">
          <button className="rounded-lg bg-slate-100 px-3 py-2 text-xs" onClick={() => exportArtifact(`pre-mortem-${number}`, markdown, "markdown")}>Export markdown</button>
          <button className="rounded-lg bg-slate-100 px-3 py-2 text-xs" onClick={() => exportArtifact(`pre-mortem-${number}`, markdown, "pdf")}>Export PDF</button>
          <button className="rounded-lg bg-slate-100 px-3 py-2 text-xs" onClick={() => exportArtifact(`pre-mortem-${number}`, markdown, "text")}>Export text</button>
        </div>
        <div className="mt-4 rounded-xl bg-slate-50 p-4"><MarkdownViewer value={markdown} /></div>
        <p className="mt-4 text-sm text-muted">Selected PR: #{selectedPR?.number} · {selectedPR?.title}</p>
      </Card>
    </>
  );
}

export function CounterPRs() {
  const [searchParams] = useSearchParams();
  const number = Number(searchParams.get("pr") ?? 104);
  const prsQuery = useQuery({ queryKey: ["demo-prs"], queryFn: demoPullRequests });
  const swarm = useSwarm();

  if (prsQuery.isLoading) {
    return <Loading />;
  }
  if (prsQuery.isError) {
    return <ErrorState message={prsQuery.error.message} />;
  }

  const selectedPR = (prsQuery.data ?? []).find((pr) => pr.number === number);
  if (!swarm.data) {
    return <><Header title="Counter PR" copy="Compare the original diff against a safer proposed remediation." /><Card><Button onClick={() => swarm.mutate(number)}><BookOpen size={16} className="mr-2" />Generate comparison</Button></Card></>;
  }

  const details = pickRun(swarm.data);
  const suggested = details.counter?.alternative_diff ?? "";

  return (
    <>
      <Header title="Counter PR" copy="Original code versus a safer alternative with risk-reducing recommendations." />
      <div className="grid gap-6 xl:grid-cols-2">
        <Card>
          <h2 className="font-semibold">Original pull request</h2>
          <div className="mt-4"><DiffViewer diff={selectedPR?.diff ?? ""} /></div>
        </Card>
        <Card>
          <h2 className="font-semibold">Counter pull request</h2>
          <div className="mt-4"><DiffViewer diff={suggested} /></div>
        </Card>
      </div>
      <Card className="mt-6">
        <div className="grid gap-3 md:grid-cols-4">
          <div><p className="text-xs text-muted">Original risk</p><b className="text-2xl">{selectedPR?.risk === "critical" ? 89 : 62}</b></div>
          <div><p className="text-xs text-muted">New risk</p><b className="text-2xl">21</b></div>
          <div><p className="text-xs text-muted">Risk reduction</p><b className="text-2xl">68%</b></div>
          <div><p className="text-xs text-muted">Adoption</p><b className="text-sm">{details.counter?.adoption_recommendation}</b></div>
        </div>
        <div className="mt-4 flex flex-wrap gap-3">
          <Button>Adopt Counter PR</Button>
          <button className="rounded-lg bg-slate-100 px-3 py-2 text-xs" onClick={() => exportArtifact(`counter-pr-${number}`, suggested, "markdown")}>Export diff</button>
          <button className="rounded-lg bg-slate-100 px-3 py-2 text-xs" onClick={() => exportArtifact(`counter-pr-${number}`, suggested, "text")}>Copy diff</button>
        </div>
      </Card>
    </>
  );
}

export function Runbooks() {
  const [searchParams] = useSearchParams();
  const number = Number(searchParams.get("pr") ?? 104);
  const prsQuery = useQuery({ queryKey: ["demo-prs"], queryFn: demoPullRequests });
  const swarm = useSwarm();

  if (prsQuery.isLoading) {
    return <Loading />;
  }
  if (prsQuery.isError) {
    return <ErrorState message={prsQuery.error.message} />;
  }

  if (!swarm.data) {
    return <><Header title="Operational runbook" copy="Response guidance for the selected PR incident scenario." /><Card><Button onClick={() => swarm.mutate(number)}><Download size={16} className="mr-2" />Generate runbook</Button></Card></>;
  }

  const details = pickRun(swarm.data);
  const runbook = [`Incident Trigger: ${details.rollback.trigger_conditions?.join(", ") ?? "Unknown"}`, `Detection Rules: Monitor alerting thresholds and checkout smoke test.`, `Rollback Commands: ${details.rollback.steps?.join(" | ") ?? "N/A"}`, `Escalation: ${details.rollback.escalation ?? "Page the owning team"}`].join("\n");

  return (
    <>
      <Header title="Operational runbook" copy="Complete response guide for an engineering incident or rollback event." />
      <Card>
        <div className="flex flex-wrap gap-3">
          <button className="rounded-lg bg-slate-100 px-3 py-2 text-xs" onClick={() => exportArtifact(`runbook-${number}`, runbook, "markdown")}>Export markdown</button>
          <button className="rounded-lg bg-slate-100 px-3 py-2 text-xs" onClick={() => exportArtifact(`runbook-${number}`, runbook, "pdf")}>Export PDF</button>
        </div>
        <div className="mt-4 space-y-3 text-sm text-body">{(details.rollback.trigger_conditions ?? []).map((item) => <div key={item}>{item}</div>)}{(details.rollback.steps ?? []).map((item) => <div key={item}>{item}</div>)}{(details.rollback.validation_steps ?? []).map((item) => <div key={item}>{item}</div>)}</div>
      </Card>
    </>
  );
}

export function History() {
  const dashboardQuery = useQuery({ queryKey: ["dashboard"], queryFn: demoDashboard });
  const [filters, setFilters] = useState({ risk: "all", developer: "all", search: "" });
  const { searchQuery } = useUI();

  if (dashboardQuery.isLoading) {
    return <Loading />;
  }
  if (dashboardQuery.isError) {
    return <ErrorState message={dashboardQuery.error.message} />;
  }

  const data = (dashboardQuery.data as DashboardMetrics).recent_analyses ?? [];
  const filtered = data.filter((entry) => {
    const query = (filters.search || searchQuery).trim().toLowerCase();
    const matchesSearch = !query || [entry.title, entry.author, entry.decision, String(entry.number)].join(" ").toLowerCase().includes(query);
    const matchesRisk = filters.risk === "all" || entry.decision.toLowerCase().includes(filters.risk.toLowerCase()) || (filters.risk === "critical" && entry.risk_score >= 80);
    const matchesDeveloper = filters.developer === "all" || entry.author === filters.developer;
    return matchesSearch && matchesRisk && matchesDeveloper;
  });

  return (
    <>
      <Header title="Analysis history" copy="Every prior analysis, risk verdict, and report artifact in one place." />
      <Card>
        <div className="grid gap-3 md:grid-cols-4">
          <select className="rounded-lg border p-2" value={filters.risk} onChange={(event) => setFilters((current) => ({ ...current, risk: event.target.value }))}><option value="all">Risk: all</option><option value="critical">Critical</option><option value="high">High</option><option value="medium">Medium</option><option value="low">Low</option></select>
          <select className="rounded-lg border p-2" value={filters.developer} onChange={(event) => setFilters((current) => ({ ...current, developer: event.target.value }))}><option value="all">Developer: all</option><option value="alex">alex</option><option value="maya">maya</option><option value="noah">noah</option></select>
          <input className="rounded-lg border p-2" placeholder="Search history" value={filters.search} onChange={(event) => setFilters((current) => ({ ...current, search: event.target.value }))} />
        </div>
        <div className="mt-4 space-y-3">{filtered.map((item) => <div key={item.id} className="flex flex-wrap items-center justify-between gap-3 rounded-xl border p-4"><div><p className="font-semibold">#{item.number} · {item.title}</p><p className="mt-1 text-xs text-muted">{item.author} · {formatDate(item.created_at)} · {item.decision}</p></div><div className="flex items-center gap-2"><span className="rounded-full bg-slate-100 px-2.5 py-1 text-xs">{item.risk_score}</span><span className={riskBadge(item.decision.toLowerCase().includes("block") ? "critical" : "medium")}>{item.decision}</span></div></div>)}</div>
      </Card>
    </>
  );
}

export function Settings() {
  const reset = useMutation({ mutationFn: resetDemo });
  return (
    <>
      <Header title="Settings" copy="Offline demo controls and workspace preferences." />
      <Card>
        <h2 className="font-semibold">Reset demo state</h2>
        <p className="mt-2 text-sm text-muted">Restore the repository, incident corpus, and analysis history.</p>
        <Button variant="danger" className="mt-4" disabled={reset.isPending} onClick={() => reset.mutate()}>{reset.isPending ? "Resetting…" : "Reset demo"}</Button>
      </Card>
    </>
  );
}
