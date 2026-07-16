import { WS_URL } from './api';

export interface RoomEvent {
  type: string;
  event_id?: string;
  client_action_id?: string | null;
  room_version?: number;
  sequence?: number;
  actor_member_id?: string | null;
  occurred_at?: string;
  payload: Record<string, unknown>;
}

type EventHandler = (event: RoomEvent) => void;

const HEARTBEAT_MS = 25_000;

/**
 * One WebSocket per active room (PRD FR-FE-03): heartbeat keep-alive,
 * namespaced command sender, clean close on leave.
 */
export class RoomSocket {
  private ws: WebSocket | null = null;
  private heartbeat: ReturnType<typeof setInterval> | null = null;
  private closedByUser = false;

  connect(joinCode: string, membershipToken: string, onEvent: EventHandler, onClose?: () => void): Promise<void> {
    this.closedByUser = false;
    return new Promise((resolve, reject) => {
      const ws = new WebSocket(`${WS_URL}/ws/rooms/${joinCode}?token=${membershipToken}`);
      this.ws = ws;

      ws.onopen = () => {
        this.heartbeat = setInterval(() => this.send('heartbeat.ping'), HEARTBEAT_MS);
        resolve();
      };
      ws.onerror = () => reject(new Error('Room connection failed'));
      ws.onmessage = (raw) => {
        const event = JSON.parse(raw.data) as RoomEvent;
        if (event.type === 'heartbeat.pong') return;
        onEvent(event);
      };
      ws.onclose = () => {
        this.cleanup();
        if (!this.closedByUser) onClose?.();
      };
    });
  }

  send(type: string, payload: Record<string, unknown> = {}): void {
    if (this.ws?.readyState === WebSocket.OPEN) {
      this.ws.send(JSON.stringify({ type, payload, client_action_id: crypto.randomUUID() }));
    }
  }

  get connected(): boolean {
    return this.ws?.readyState === WebSocket.OPEN;
  }

  close(): void {
    this.closedByUser = true;
    this.ws?.close();
    this.cleanup();
  }

  private cleanup(): void {
    if (this.heartbeat) clearInterval(this.heartbeat);
    this.heartbeat = null;
    this.ws = null;
  }
}
