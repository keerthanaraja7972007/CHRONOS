import { useMutation } from "@tanstack/react-query"; import { runAnalysis } from "../services/api";
export const useSwarm=()=>useMutation({mutationFn:runAnalysis});
