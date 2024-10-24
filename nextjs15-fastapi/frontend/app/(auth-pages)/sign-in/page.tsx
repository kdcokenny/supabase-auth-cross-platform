import { signInWithGoogleOAuth } from "@/app/actions";
import { Message } from "@/components/form-message";

export default async function Login(props: { searchParams: Promise<Message> }) {
  const searchParams = await props.searchParams;
  return (
    <form className="flex-1 flex flex-col min-w-64">
      <h1 className="text-2xl font-medium">Continue with Google</h1>
      {/* Add Google OAuth button */}
      <button
        type="button"
        className="mt-8 flex items-center justify-center gap-2 rounded-lg border border-gray-300 bg-white px-4 py-2 text-sm font-medium text-gray-700 hover:bg-gray-50 focus:outline-none focus:ring-2 focus:ring-gray-500 focus:ring-offset-2"
        onClick={signInWithGoogleOAuth}
      >
        <img
          src="https://www.gstatic.com/firebasejs/ui/2.0.0/images/auth/google.svg"
          alt="Google logo"
          className="h-5 w-5"
        />
        Continue with Google
      </button>
    </form>
  );
}
