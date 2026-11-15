
import { getStore } from "@netlify/blobs";

export default async (req) => {
  if(req.method !== "POST") return new Response("ใช้ POST นะคะพ่อ", {status: 405});
  const { api, token } = await req.json();
  const store = getStore("api-deploy");
  await store.setJSON("config", { api, token, savedAt: new Date().toISOString() });
  return Response.json({ ok: true, message: "บันทึกถาวรแล้วค่ะพ่อ" });
};
