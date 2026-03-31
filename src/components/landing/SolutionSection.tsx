import { motion } from "framer-motion";
import { MessageSquare, Brain, UserCheck } from "lucide-react";

const solutions = [
  {
    icon: MessageSquare,
    title: "Lives in WhatsApp",
    description: "No new apps to download. Manage your stokvel, track savings, and get guidance in the app your community already uses.",
  },
  {
    icon: Brain,
    title: "AI-powered coordination",
    description: "Automated contribution tracking, payout scheduling, and smart reminders keep your group running smoothly.",
  },
  {
    icon: UserCheck,
    title: "Learns your community",
    description: "Warima adapts to your group's goals, saving patterns, and preferences — delivering smarter guidance over time.",
  },
];

const SolutionSection = () => {
  return (
    <section className="py-20 md:py-28">
      <div className="container">
        <motion.div
          initial={{ opacity: 0, y: 20 }}
          whileInView={{ opacity: 1, y: 0 }}
          viewport={{ once: true }}
          transition={{ duration: 0.5 }}
          className="text-center mb-16"
        >
          <p className="text-sm font-body font-semibold tracking-widest uppercase text-muted-foreground mb-3">The Solution</p>
          <h2 className="text-3xl md:text-4xl tracking-tight text-foreground max-w-2xl mx-auto">
            One AI platform. Three expert agents. Zero friction.
          </h2>
        </motion.div>

        <div className="grid md:grid-cols-3 gap-8">
          {solutions.map((s, i) => (
            <motion.div
              key={s.title}
              initial={{ opacity: 0, y: 20 }}
              whileInView={{ opacity: 1, y: 0 }}
              viewport={{ once: true }}
              transition={{ duration: 0.5, delay: i * 0.1 }}
              className="text-center p-8"
            >
              <div className="w-14 h-14 rounded-2xl bg-sage-light flex items-center justify-center mx-auto mb-5">
                <s.icon className="w-7 h-7 text-foreground" />
              </div>
              <h3 className="text-xl mb-3 text-foreground">{s.title}</h3>
              <p className="text-muted-foreground font-body leading-relaxed">{s.description}</p>
            </motion.div>
          ))}
        </div>
      </div>
    </section>
  );
};

export default SolutionSection;
