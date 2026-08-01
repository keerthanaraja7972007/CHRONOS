const base="/api/v1";
export async function api<T>(path:string, init?:RequestInit):Promise<T>{const response=await fetch(`${base}${path}`,{headers:{"Content-Type":"application/json",...init?.headers},...init}); if(!response.ok){const body=await response.json().catch(()=>null); throw new Error(body?.error?.message??"Request failed");} return response.json() as Promise<T>}
export type Repository={id:string;full_name:string;default_branch:string;is_active:boolean};
export type Analysis={id:string;pull_request_id:string;status:string;pre_mortem?:string};
