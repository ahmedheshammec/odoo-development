# Supabase Integration with Odoo CRM Lead

Do this in order:

1. **Create Odoo API key**
- Odoo → user menu → `My Profile` → `Account Security` → `API Keys` → create one.
- Keep it copied once.



2. **Add Supabase secrets**
- Supabase project → `Edge Functions` → `Secrets` → add:
- `ODOO_URL` = `https://the-secret-solutions.odoo.com`
- `ODOO_DB` = `the-secret-solutions`
- `ODOO_USERNAME` = info@thesecret-solutions.com
- `ODOO_API_KEY` = 2ba7c0a8c79a2e956d482566baef6929a694d7fe

3. **Create function**
- Supabase → `Edge Functions` → `Create function` → `Via Editor` 
- Name: `submit_opportunity`
- Replace code with:

```ts
import { serve } from "https://deno.land/std@0.224.0/http/server.ts";

const corsHeaders = {
  "Access-Control-Allow-Origin": "https://www.thesecret-solutions.com",
  "Access-Control-Allow-Headers": "content-type, authorization, x-client-info, apikey",
  "Access-Control-Allow-Methods": "POST, OPTIONS",
};

async function odooJsonRpc(url: string, service: string, method: string, args: any[]) {
  const res = await fetch(`${url}/jsonrpc`, {
    method: "POST",
    headers: { "Content-Type": "application/json" },
    body: JSON.stringify({
      jsonrpc: "2.0",
      method: "call",
      params: { service, method, args },
      id: Date.now(),
    }),
  });

  const data = await res.json();
  if (data.error) {
    throw new Error(data.error?.data?.message || data.error?.message || "Odoo RPC error");
  }
  return data.result;
}

serve(async (req) => {
  if (req.method === "OPTIONS") {
    return new Response("ok", { headers: corsHeaders });
  }

  if (req.method !== "POST") {
    return new Response(
      JSON.stringify({ success: false, error: "Method not allowed" }),
      { status: 405, headers: { ...corsHeaders, "Content-Type": "application/json" } }
    );
  }

  try {
    const ODOO_URL = Deno.env.get("ODOO_URL")!;
    const ODOO_DB = Deno.env.get("ODOO_DB")!;
    const ODOO_USERNAME = Deno.env.get("ODOO_USERNAME")!;
    const ODOO_API_KEY = Deno.env.get("ODOO_API_KEY")!;

    if (!ODOO_URL || !ODOO_DB || !ODOO_USERNAME || !ODOO_API_KEY) {
      throw new Error("Missing Odoo env secrets");
    }

    const body = await req.json();

    const contactName = body.contact_name || body.name || "";
    const partnerName = body.partner_name || body.company || "";
    const emailFrom = body.email_from || body.email || "";
    const phone = body.phone || "";
    const subject = body.subject || "Website Inquiry";
    const message = body.description || body.message || "";
    const requestRef = body.request_ref || "";
    const leadName = body.lead_name || body.opportunity_name || `${subject} - ${partnerName || contactName || "Unknown"}`;

    const uid = await odooJsonRpc(ODOO_URL, "common", "authenticate", [
      ODOO_DB,
      ODOO_USERNAME,
      ODOO_API_KEY,
      {},
    ]);

    if (!uid) {
      throw new Error("Odoo authentication failed");
    }

    const leadVals = {
      name: leadName,
      type: "opportunity",
      contact_name: contactName,
      partner_name: partnerName,
      email_from: emailFrom,
      phone: phone,
      description: `${message}\n\nRef: ${requestRef}`,
    };

    const leadId = await odooJsonRpc(ODOO_URL, "object", "execute_kw", [
      ODOO_DB,
      uid,
      ODOO_API_KEY,
      "crm.lead",
      "create",
      [leadVals],
    ]);

    return new Response(
      JSON.stringify({
        success: true,
        odoo_lead_id: leadId,
        message: "Lead created in Odoo",
      }),
      { status: 200, headers: { ...corsHeaders, "Content-Type": "application/json" } }
    );
  } catch (e) {
    return new Response(
      JSON.stringify({
        success: false,
        error: String(e?.message || e),
      }),
      { status: 500, headers: { ...corsHeaders, "Content-Type": "application/json" } }
    );
  }
});

```

4. Turn Off the Toggle `Verify JWT with legacy secret` in the details section of the function
5. **Deploy function**

- Click `Deploy`.

5. **Test from your website**
- Submit form once.
- Check Odoo CRM.

