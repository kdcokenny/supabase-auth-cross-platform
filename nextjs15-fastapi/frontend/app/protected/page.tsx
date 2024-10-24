"use client";
import { createClient } from "@/utils/supabase/client";
import { InfoIcon } from "lucide-react";
import { useEffect, useState } from "react";

const BACKEND_URL = "http://localhost:8000";

export default function ProtectedPage() {
  const supabase = createClient();
  const [user, setUser] = useState<any>(null);
  const [backendUserJson, setBackendUserJson] = useState<any>(null);
  const [backendUserBase64Json, setBackendUserBase64Json] = useState<any>(null);

  useEffect(() => {
    const fetchData = async () => {
      const { data: { user: supabaseUser } } = await supabase.auth.getUser();
      setUser(supabaseUser);

      const backendUser = await fetch(`${BACKEND_URL}/auth/me`, {
        credentials: "include",
        method: "GET",
      });
      if (backendUser.ok) {
        const userData = await backendUser.json();
        setBackendUserJson(userData);
      }
    };

    fetchData();
  }, []);

  return (
    <div className="flex-1 w-full flex flex-col gap-12">
      <div className="w-full">
        <div className="bg-accent text-sm p-3 px-5 rounded-md text-foreground flex gap-3 items-center">
          <InfoIcon size="16" strokeWidth={2} />
          This is a protected page that you can only see as an authenticated
          user
        </div>
      </div>
      <div className="flex flex-col gap-2 items-start">
        <h2 className="font-bold text-2xl mb-4">Your user details</h2>
        <pre className="text-xs font-mono p-3 rounded border max-h-32 overflow-auto">
          {JSON.stringify(user, null, 2)}
        </pre>
      </div>
      <div className="flex flex-col gap-2 items-start">
        <h2 className="font-bold text-2xl mb-4">Your user details from backend</h2>
        <pre className="text-xs font-mono p-3 rounded border max-h-32 overflow-auto">
          {JSON.stringify(backendUserJson, null, 2)}
        </pre>
      </div>
    </div>
  );
}
