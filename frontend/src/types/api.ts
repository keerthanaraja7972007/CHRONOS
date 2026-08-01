export type Severity="low"|"medium"|"high"|"critical";
export interface Repository {id:string;full_name:string;default_branch:string;is_active:boolean}
export interface DemoPR {number:number;risk:Severity;title:string;author:string;diff:string;status:string;files_changed:string[];date:string;description:string;short_description:string}
export interface Incident {id:string;title:string;severity:Severity;root_cause:string;affected_files:string[];occurred_on:string}
export interface DashboardMetrics {repository:{name:string;owner:string;description:string;default_branch:string;contributors:string[];file_count:number;languages:Record<string,number>;files:string[]};statistics:{repositories:number;indexed_files:number;incidents:number;analyses:number;high_risk:number};risk_trend:Array<{week:string;score:number}>;recent_analyses:Array<{id:string;number:number;title:string;author:string;risk_score:number;decision:string;created_at:string}>;high_risk_prs:DemoPR[]}
export interface Finding {category:string;severity:Severity;confidence:number;summary:string;evidence:string[];historical_references:string[]}
export interface AgentResult {agent_name:string;findings:Finding[];data:Record<string,unknown>;confidence:number;reasoning_summary:string}
export interface SwarmRun {run_id:string;results:Record<string,AgentResult>;debate_log:DebateEntry[];verdict:{verdict:string;final_risk_score:number;override_applied:boolean;executive_summary:string}}
export interface DebateEntry {sequence:number;agent_name:string;timestamp:string;category:string;severity:Severity;confidence:number;message:string;evidence:string[];historical_references:string[]}
