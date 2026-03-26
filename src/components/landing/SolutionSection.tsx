import { motion } from "framer-motion";
import { MessageSquare, Brain, UserCheck } from "lucide-react";

const solutions = [
  {
    icon: MessageSquare,
    title: "Lives in WhatsApp",
    description: "No new apps to download. Chat with your AI team in the app you already use every day.",
  },
  {
    icon: Brain,
    title: "Multi-agent intelligence",
    description: "Specialized AI agents for finance, marketing, and support — all working together seamlessly.",
  },
  {
    icon: UserCheck,
    title: "Remembers & personalizes",
    description: "Smart memory means better answers over time. It learns your business and adapts to your needs.",
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
