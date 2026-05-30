export interface Message {
  id: string;
  role: "user" | "assistant";
  content: string;
  sources?: Source[];
  timestamp: number;
}

export interface Source {
  title: string;
  url?: string;
  page?: number;
}

export interface Chat {
  id: string;
  title: string;
  agentId: string;
  messages: Message[];
  createdAt: number;
}

export interface Agent {
  id: string;
  name: string;
  description: string;
  urls: string[];
  files: UploadedFile[];
}

export interface UploadedFile {
  id: string;
  name: string;
  size: number;
  uploadedAt: number;
}
