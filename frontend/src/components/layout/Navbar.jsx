import { Link } from "react-router-dom";

export default function Navbar() {
  return (
    <nav className="sticky top-0 z-50 bg-white shadow-sm">
      <div className="mx-auto flex max-w-7xl items-center justify-between px-6 py-4">
        {/* Logo */}
        <Link to="/" className="text-2xl font-bold text-teal-700">
          WelfareAI
        </Link>

        {/* Navigation */}
        <div className="hidden items-center gap-8 md:flex">
          <Link
            to="/"
            className="font-medium text-gray-700 transition hover:text-teal-700"
          >
            Home
          </Link>

          <Link
            to="/chat"
            className="font-medium text-gray-700 transition hover:text-teal-700"
          >
            Chat
          </Link>
        </div>

        {/* CTA */}
        <Link
          to="/chat"
          className="rounded-lg bg-teal-700 px-5 py-2 text-white transition hover:bg-teal-800"
        >
          Get Started
        </Link>
      </div>
    </nav>
  );
}