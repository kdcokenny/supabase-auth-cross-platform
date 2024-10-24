"use server";

import { createClient } from "@/utils/supabase/server";
import { redirect } from "next/navigation";


export async function signInWithGoogleOAuth() {
  const supabase = await createClient();
  const { data, error } = await supabase.auth.signInWithOAuth({
    provider: 'google',
    options: {
      redirectTo: `http://localhost:3000/auth/callback`,
    },
  });

  if (data.url) {
    redirect(data.url);
  }

  return { data, error };
}

export const signOutAction = async () => {
  const supabase = await createClient();
  await supabase.auth.signOut();
  return redirect("/sign-in");
};
