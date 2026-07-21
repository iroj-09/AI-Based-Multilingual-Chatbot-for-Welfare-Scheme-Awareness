export default function Footer() {
  return (
    <footer className="border-t bg-white">
      <div className="mx-auto max-w-7xl px-6 py-8 text-center text-gray-600">
        © {new Date().getFullYear()} WelfareAI • Built with React, FastAPI &
        Gemini
      </div>
    </footer>
  );
}