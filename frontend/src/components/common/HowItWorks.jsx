import {
  MessageCircleQuestion,
  Languages,
  SearchCheck,
  FileText,
} from "lucide-react";

const steps = [
  {
    icon: MessageCircleQuestion,
    title: "Ask Your Question",
    description:
      "Ask naturally in English, Hindi, or Hinglish.",
  },
  {
    icon: Languages,
    title: "AI Understands",
    description:
      "The chatbot understands and normalizes your language.",
  },
  {
    icon: SearchCheck,
    title: "Finds Relevant Schemes",
    description:
      "Searches hundreds of government welfare schemes using AI-powered retrieval.",
  },
  {
    icon: FileText,
    title: "Get Personalized Guidance",
    description:
      "Receive eligibility information, benefits, required documents, and application guidance.",
  },
];

export default function HowItWorks() {
  return (
    <section className="bg-slate-50 py-20">
      <div className="mx-auto max-w-7xl px-6">

        <div className="text-center">
          <h2 className="text-4xl font-bold text-gray-900">
            How It Works
          </h2>

          <p className="mt-4 text-gray-600">
            Discover government welfare schemes in just a few simple steps.
          </p>
        </div>

        <div className="mt-14 grid gap-8 md:grid-cols-2 lg:grid-cols-4">
          {steps.map((step, index) => {
            const Icon = step.icon;

            return (
              <div
                key={index}
                className="rounded-2xl bg-white p-8 text-center shadow transition hover:-translate-y-2 hover:shadow-lg"
              >
                <div className="mx-auto flex h-16 w-16 items-center justify-center rounded-full bg-teal-100">
                  <Icon size={32} className="text-teal-700" />
                </div>

                <h3 className="mt-6 text-xl font-semibold">
                  {step.title}
                </h3>

                <p className="mt-3 text-gray-600">
                  {step.description}
                </p>
              </div>
            );
          })}
        </div>

      </div>
    </section>
  );
}