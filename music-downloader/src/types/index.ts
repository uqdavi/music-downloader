export type DownloadStatus =
  | "idle"
  | "starting"
  | "downloading"
  | "processing"
  | "done";

export type TrackStatus = "pending" | "downloading" | "done";

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
