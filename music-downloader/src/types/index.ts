export type DownloadStatus =
  | "idle"
  | "extracting"
  | "starting"
  | "downloading"
  | "processing"
  | "done"
  | "error";

export type TrackStatus = "pending" | "downloading" | "done" | "skipped";

export type Format = "mp3" | "mp4";

export interface Track {
  id: string;
  title: string;
  thumbnail: string;
  status: TrackStatus;
}

export interface ProgressResponse {
  status: DownloadStatus;
  percent: string;
  current: Track;
  playlist: Track[];
}

export interface DownloadRequest {
  url: string;
  format: Format;
}
