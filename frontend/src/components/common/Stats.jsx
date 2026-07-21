import { Database, Languages, Bot, Search } from "lucide-react";

const stats = [
  {
    icon: Database,
    value: "852+",
    label: "Government Schemes",
  },
  {
    icon: Languages,
    value: "3",
    label: "Supported Languages",
  },
  {
    icon: Search,
    value: "AI",
    label: "Semantic Search",
  },
  {
    icon: Bot,
    value: "24/7",
    label: "AI Assistance",
  },
];

export default function Stats() {
  return (
    <section className="bg-teal-700 py-20 text-white">
      <div className="mx-auto max-w-7xl px-6">
        <div className="grid gap-10 text-center md:grid-cols-2 lg:grid-cols-4">
          {stats.map((stat, index) => {
            const Icon = stat.icon;

            return (
              <div key={index}>
                <Icon className="mx-auto mb-4" size={40} />
                <h2 className="text-5xl font-bold">{stat.value}</h2>
                <p className="mt-2 text-lg">{stat.label}</p>
              </div>
            );
          })}
        </div>
      </div>
    </section>
  );
}