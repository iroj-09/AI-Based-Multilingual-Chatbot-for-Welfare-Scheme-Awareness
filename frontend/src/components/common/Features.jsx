import {
  Bot,
  Languages,
  Search,
  ShieldCheck,
} from "lucide-react";

const features = [
  {
    icon: <Bot size={40} className="text-teal-700" />,
    title: "AI Powered Assistance",
    description:
      "Get instant answers about Central and State Government welfare schemes using AI.",
  },
  {
    icon: <Languages size={40} className="text-teal-700" />,
    title: "Multilingual Support",
    description:
      "Ask questions naturally in English, Hindi, or Hinglish.",
  },
  {
    icon: <Search size={40} className="text-teal-700" />,
    title: "Smart Scheme Search",
    description:
      "Search hundreds of government schemes using semantic AI instead of keywords.",
  },
  {
    icon: <ShieldCheck size={40} className="text-teal-700" />,
    title: "Eligibility Guidance",
    description:
      "Check your eligibility and discover schemes that match your profile.",
  },
];

export default function Features() {
  return (
    <section className="bg-white py-20">
      <div className="mx-auto max-w-7xl px-6">

        <div className="text-center">
          <h2 className="text-4xl font-bold text-gray-900">
            Why Choose WelfareAI?
          </h2>

          <p className="mt-4 text-gray-600">
            Everything you need to discover and understand government welfare schemes.
          </p>
        </div>

        <div className="mt-14 grid gap-8 md:grid-cols-2 lg:grid-cols-4">

          {features.map((feature, index) => (
            <div
              key={index}
              className="rounded-2xl border bg-slate-50 p-8 transition hover:-translate-y-2 hover:shadow-xl"
            >
              {feature.icon}

              <h3 className="mt-6 text-xl font-semibold">
                {feature.title}
              </h3>

              <p className="mt-3 text-gray-600">
                {feature.description}
              </p>

            </div>
          ))}

        </div>
      </div>
    </section>
  );
}