"use client";

import { useEffect, useRef, useState, useCallback } from "react";

const STREAM_URL = "/api/stream";

type DriveCmd = "forward" | "backward" | "stop";
type SteerCmd = "left" | "right" | "center";

export default function Home() {
  const [mounted, setMounted] = useState(false);
  const [drive, setDrive] = useState<DriveCmd>("stop");
  const [steer, setSteer] = useState<SteerCmd>("center");
  const [connected, setConnected] = useState(true);
  const [steerAngle, setSteerAngle] = useState(0);
  const [joystickPos, setJoystickPos] = useState({ x: 0, y: 0 });
  const imgRef = useRef<HTMLImageElement>(null);
  const joystickRef = useRef<HTMLDivElement>(null);
  const joystickActiveRef = useRef(false);
  const lastSteer = useRef<SteerCmd>("center");
  const lastDrive = useRef<DriveCmd>("stop");

  useEffect(() => { setMounted(true); }, []);

  const send = useCallback((cmd: string) => {
    fetch(`/api/drive?cmd=${cmd}`, { method: "GET" })
      .then(() => setConnected(true))
      .catch(() => setConnected(false));
  }, []);

  const pressDrive = (cmd: DriveCmd) => {
    if (cmd !== lastDrive.current) {
      lastDrive.current = cmd;
      setDrive(cmd);
      send(cmd);
    }
  };

  const releaseDrive = () => {
    if (lastDrive.current !== "stop") {
      lastDrive.current = "stop";
      setDrive("stop");
      send("stop");
    }
  };

  useEffect(() => {
    const onKeyDown = (e: KeyboardEvent) => {
      if (e.key === "w" || e.key === "W") pressDrive("forward");
      if (e.key === "s" || e.key === "S") pressDrive("backward");
    };
    const onKeyUp = (e: KeyboardEvent) => {
      if (e.key === "w" || e.key === "W" || e.key === "s" || e.key === "S") releaseDrive();
    };
    window.addEventListener("keydown", onKeyDown);
    window.addEventListener("keyup", onKeyUp);
    return () => {
      window.removeEventListener("keydown", onKeyDown);
      window.removeEventListener("keyup", onKeyUp);
    };
  }, []);

  const onJoystickDown = (e: React.PointerEvent) => {
    e.preventDefault();
    joystickActiveRef.current = true;
    (e.currentTarget as HTMLElement).setPointerCapture(e.pointerId);
  };

  const onJoystickMove = (e: React.PointerEvent) => {
    if (!joystickActiveRef.current || !joystickRef.current) return;
    const rect = joystickRef.current.getBoundingClientRect();
    const cx = rect.left + rect.width / 2;
    const cy = rect.top + rect.height / 2;
    const dx = e.clientX - cx;
    const dy = e.clientY - cy;
    const maxR = rect.width / 2 - 20;
    const dist = Math.sqrt(dx * dx + dy * dy);
    const clampedX = dist > maxR ? (dx / dist) * maxR : dx;
    const clampedY = dist > maxR ? (dy / dist) * maxR : dy;
    setJoystickPos({ x: clampedX, y: clampedY });

    const norm = clampedX / maxR;
    setSteerAngle(norm);
    const newSteer: SteerCmd = norm < -0.2 ? "left" : norm > 0.2 ? "right" : "center";
    if (newSteer !== lastSteer.current) {
      lastSteer.current = newSteer;
      setSteer(newSteer);
      send(newSteer);
    }
  };

  const onJoystickEnd = () => {
    joystickActiveRef.current = false;
    setJoystickPos({ x: 0, y: 0 });
    setSteerAngle(0);
    if (lastSteer.current !== "center") {
      lastSteer.current = "center";
      setSteer("center");
      send("center");
    }
  };

  if (!mounted) return null;

  return (
    <div className="root">

      {/* black underlay so flicker is black not red */}
      <div style={{ position: "absolute", inset: 0, background: "#000", zIndex: 0 }} />

      {/* Stream */}
      <img
        ref={imgRef}
        className="stream"
        src={STREAM_URL}
        alt="Camera feed"
        style={{
          position: "absolute",
          top: "50%",
          left: "50%",
          width: "100vh",
          height: "100vw",
          transform: "rotate(90deg) translate(-50%, -50%)",
          transformOrigin: "top left",
          objectFit: "cover",
          zIndex: 1,
        }}
        onError={(e) => {
          setTimeout(() => {
            (e.target as HTMLImageElement).src = `${STREAM_URL}?t=${Date.now()}`;
          }, 2000);
        }}
      />

      {/* HUD */}
      <div className="hud">

        {/* Top-left: connection */}
        <div className="conn-badge">
          <div className="conn-dot blink" style={{ background: connected ? "#4ade80" : "#ef4444" }} />
          <span className="conn-text" style={{ color: connected ? "#4ade80" : "#ef4444" }}>
            {connected ? "LIVE" : "OFFLINE"}
          </span>
        </div>

        {/* Top-right: stats */}
        <div className="stats">
          <div className="stat-pill">
            <span className="stat-label">Drive</span>
            <span className="stat-value" style={{ color: drive === "forward" ? "#4ade80" : drive === "backward" ? "#ef4444" : "#666" }}>
              {drive === "forward" ? "FWD" : drive === "backward" ? "REV" : "STOP"}
            </span>
            <div className="stat-dot" style={{ background: drive === "forward" ? "#4ade80" : drive === "backward" ? "#ef4444" : "#333" }} />
          </div>
          <div className="stat-pill">
            <span className="stat-label">Steer</span>
            <span className="stat-value" style={{ color: steer === "center" ? "#666" : "#3b82f6" }}>
              {steer === "left" ? "◀ L" : steer === "right" ? "R ▶" : "——"}
            </span>
            <div className="stat-dot" style={{ background: steer === "center" ? "#333" : "#3b82f6" }} />
          </div>
          <div className="stat-pill">
            <span className="stat-label">Angle</span>
            <span className="stat-value" style={{ color: "#fff" }}>
              {Math.round(steerAngle * 90)}°
            </span>
            <div className="stat-dot" style={{ background: "#444" }} />
          </div>
        </div>

        {/* Bottom-left: joystick */}
        <div className="joystick-area">
          <div
            ref={joystickRef}
            className="joystick-base"
            onPointerDown={onJoystickDown}
            onPointerMove={onJoystickMove}
            onPointerUp={onJoystickEnd}
            onPointerCancel={onJoystickEnd}
          >
            <div
              className="joystick-thumb"
              style={{
                transform: `translate(calc(-50% + ${joystickPos.x}px), calc(-50% + ${joystickPos.y}px))`,
              }}
            />
          </div>
          <span className="joystick-label">STEER</span>
        </div>

        {/* Bottom-right: gas & brake */}
        <div className="drive-area">
          <div className="drive-btns">
            <button
              className={`btn-gas ${drive === "forward" ? "active" : ""}`}
              onPointerDown={() => pressDrive("forward")}
              onPointerUp={releaseDrive}
              onPointerLeave={releaseDrive}
              onPointerCancel={releaseDrive}
            >
              <span className="btn-icon" style={{ color: drive === "forward" ? "#4ade80" : "rgba(255,255,255,0.3)" }}>▲</span>
              <span className="btn-text" style={{ color: drive === "forward" ? "#4ade80" : "rgba(255,255,255,0.3)" }}>Gas</span>
            </button>
            <button
              className={`btn-brake ${drive === "backward" ? "active" : ""}`}
              onPointerDown={() => pressDrive("backward")}
              onPointerUp={releaseDrive}
              onPointerLeave={releaseDrive}
              onPointerCancel={releaseDrive}
            >
              <span className="btn-icon" style={{ color: drive === "backward" ? "#ef4444" : "rgba(255,255,255,0.3)" }}>▼</span>
              <span className="btn-text" style={{ color: drive === "backward" ? "#ef4444" : "rgba(255,255,255,0.3)" }}>Brake</span>
            </button>
          </div>
          <span className="drive-label">Drive</span>
        </div>

      </div>
    </div>
  );
}