import { motion } from "framer-motion";
import {
  Area,
  AreaChart,
  Bar,
  BarChart,
  CartesianGrid,
  Cell,
  Pie,
  PieChart,
  PolarAngleAxis,
  PolarGrid,
  PolarRadiusAxis,
  Radar,
  RadarChart,
  ResponsiveContainer,
  Tooltip,
  XAxis,
  YAxis,
} from "recharts";

const palette = ["#2563EB", "#16A34A", "#F59E0B", "#EF4444", "#A855F7"];

export function MetricsOverview({ metrics }: { metrics: Array<{ label: string; value: string; tone?: string }> }) {
  return (
    <div className="grid gap-3 sm:grid-cols-2 xl:grid-cols-4">
      {metrics.map((metric, index) => (
        <motion.div
          key={metric.label}
          initial={{ opacity: 0, y: 12 }}
          animate={{ opacity: 1, y: 0 }}
          transition={{ delay: index * 0.04 }}
          className="card"
        >
          <p className={`text-3xl font-semibold ${metric.tone ?? "text-ink"}`}>{metric.value}</p>
          <p className="mt-2 text-sm text-muted">{metric.label}</p>
        </motion.div>
      ))}
    </div>
  );
}

export function RiskRadar({ data }: { data: Array<{ subject: string; score: number; fullMark: number }> }) {
  return (
    <div className="h-72">
      <ResponsiveContainer width="100%" height="100%">
        <RadarChart data={data}>
          <PolarGrid />
          <PolarAngleAxis dataKey="subject" />
          <PolarRadiusAxis angle={30} domain={[0, 100]} />
          <Radar dataKey="score" stroke="#2563EB" fill="#2563EB" fillOpacity={0.45} />
          <Tooltip />
        </RadarChart>
      </ResponsiveContainer>
    </div>
  );
}

export function RiskPie({ data }: { data: Array<{ name: string; value: number }> }) {
  return (
    <div className="h-72">
      <ResponsiveContainer width="100%" height="100%">
        <PieChart>
          <Pie data={data} dataKey="value" nameKey="name" innerRadius={55} outerRadius={90} paddingAngle={3}>
            {data.map((_, index) => (
              <Cell key={String(index)} fill={palette[index % palette.length]} />
            ))}
          </Pie>
          <Tooltip />
        </PieChart>
      </ResponsiveContainer>
    </div>
  );
}

export function RiskBar({ data }: { data: Array<{ name: string; score: number }> }) {
  return (
    <div className="h-72">
      <ResponsiveContainer width="100%" height="100%">
        <BarChart data={data}>
          <CartesianGrid strokeDasharray="3 3" />
          <XAxis dataKey="name" />
          <YAxis domain={[0, 100]} />
          <Tooltip />
          <Bar dataKey="score" radius={[8, 8, 0, 0]} fill="#2563EB" />
        </BarChart>
      </ResponsiveContainer>
    </div>
  );
}

export function RiskTrend({ data }: { data: Array<{ week: string; score: number }> }) {
  return (
    <div className="h-72">
      <ResponsiveContainer width="100%" height="100%">
        <AreaChart data={data}>
          <defs>
            <linearGradient id="scoreFill" x1="0" y1="0" x2="0" y2="1">
              <stop offset="5%" stopColor="#2563EB" stopOpacity={0.5} />
              <stop offset="95%" stopColor="#2563EB" stopOpacity={0.05} />
            </linearGradient>
          </defs>
          <CartesianGrid strokeDasharray="3 3" />
          <XAxis dataKey="week" />
          <YAxis domain={[0, 100]} />
          <Tooltip />
          <Area type="monotone" dataKey="score" stroke="#2563EB" fill="url(#scoreFill)" strokeWidth={3} />
        </AreaChart>
      </ResponsiveContainer>
    </div>
  );
}

export function HeatMap({ data }: { data: Array<{ name: string; value: number }> }) {
  return (
    <div className="grid grid-cols-3 gap-2">
      {data.map((item) => (
        <div
          key={item.name}
          className="rounded-xl border p-3 text-center text-sm"
          style={{ backgroundColor: `rgba(37,99,235,${Math.min(item.value / 100, 0.35)})` }}
        >
          <div className="font-semibold">{item.name}</div>
          <div className="text-xs text-body">{item.value}%</div>
        </div>
      ))}
    </div>
  );
}
