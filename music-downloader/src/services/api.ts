import axios from "axios";
import type { DownloadRequest, ProgressResponse } from "@/types";

const api = axios.create({
  baseURL: "http://localhost:5000",
  headers: { "Content-Type": "application/json" },
});

export const startDownload = (data: DownloadRequest) =>
  api.post("/download", data);

export const getProgress = () =>
  api.get<ProgressResponse>("/progress");

export default api;
