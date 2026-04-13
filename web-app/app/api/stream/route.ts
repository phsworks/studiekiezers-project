export const dynamic = "force-dynamic";
export const runtime = "nodejs";

import { NextResponse } from "next/server";

export async function GET() {
  const response = await fetch("http://192.168.68.125:81/stream", {
    cache: "no-store",
  });

  return new NextResponse(response.body, {
    status: 200,
    headers: {
      "Content-Type": response.headers.get("Content-Type") || "multipart/x-mixed-replace; boundary=frame",
      "Cache-Control": "no-cache",
      "Access-Control-Allow-Origin": "*",
    },
  });
}