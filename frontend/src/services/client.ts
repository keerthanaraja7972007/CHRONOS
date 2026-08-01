import axios from "axios";
export const client=axios.create({baseURL:"/api/v1",timeout:30000,headers:{"Content-Type":"application/json"}});
client.interceptors.response.use(response=>response, error=>Promise.reject(new Error(error.response?.data?.error?.message??error.message??"Request failed")));
