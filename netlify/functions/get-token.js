
import { getStore } from "@netlify/blobs";

export default async () => {
  const store = getStore("api-deploy");
  const data = await store.getJSON("config");
  if(!data) return Response.json({ ok: false });
  return Response.json({ ok: true, api: data.api });
};
