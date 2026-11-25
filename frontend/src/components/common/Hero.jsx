import { Link } from "react-router-dom";

export default function Hero() {
  return (
    <section className="bg-slate-50">
      <div className="mx-auto flex min-h-[85vh] max-w-7xl flex-col items-center justify-center px-6 text-center">
        <span className="mb-4 rounded-full bg-teal-100 px-4 py-2 text-sm font-medium text-teal-700">
          🇮🇳 AI Powered Government Welfare Assistant
        </span>

        <h1 className="max-w-4xl text-5xl font-extrabold leading-tight text-gray-900">
          Discover Government Welfare Schemes
          <span className="block text-teal-700">
            in Hindi, English & Hinglish
          </span>
        </h1>

        <p className="mt-6 max-w-2xl text-lg text-gray-600">
          Ask questions naturally, check your eligibility, and explore Central
          and State Government welfare schemes with AI-powered assistance.
        </p>

        <div className="mt-10 flex flex-wrap justify-center gap-4">
          <Link
            to="/chat"
            className="rounded-lg bg-teal-700 px-8 py-4 text-lg font-semibold text-white transition hover:bg-teal-800"
          >
            Start Chat
          </Link>
        </div>
      </div>
    </section>
  );
}