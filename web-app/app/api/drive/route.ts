import { NextRequest, NextResponse } from "next/server";

const ESP32_IP = "192.168.68.123";

export async function GET(request: NextRequest) {
  const cmd = request.nextUrl.searchParams.get("cmd");
  
  if (!cmd) {
    return NextResponse.json({ error: "missing cmd" }, { status: 400 });
  }

  try {
    const res = await fetch(`http://${ESP32_IP}/drive?cmd=${cmd}`);
    const data = await res.json();
    return NextResponse.json(data);
  } catch {
    return NextResponse.json({ error: "ESP32 unreachable" }, { status: 500 });
  }
}