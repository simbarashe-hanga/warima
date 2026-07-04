import { motion } from "framer-motion";
import { MessageCircle, Brain, Sparkles } from "lucide-react";

const steps = [
  {
    icon: MessageCircle,
    number: "01",
    title: "Message on WhatsApp",
    description: "Open WhatsApp and send a message — just like texting a friend.",
  },
  {
    icon: Brain,
    number: "02",
    title: "AI understands your intent",
    description: "Our smart routing detects whether you need finance, marketing, or support help — backed by a trusted ledger with immutable records managed by AI, so nothing gets lost.",
  },
  {
    icon: Sparkles,
    number: "03",
    title: "Get personalized help",
    description: "Receive expert-level guidance tailored to your business, instantly.",
  },
];

const HowItWorksSection = () => {
  return (
    <section id="how-it-works" className="py-20 md:py-28">
      <div className="container">
        <motion.div
          initial={{ opacity: 0, y: 20 }}
          whileInView={{ opacity: 1, y: 0 }}
          viewport={{ once: true }}
          transition={{ duration: 0.5 }}
          className="text-center mb-16"
        >
          <p className="text-sm font-body font-semibold tracking-widest uppercase text-muted-foreground mb-3">How It Works</p>
          <h2 className="text-3xl md:text-4xl tracking-tight text-foreground">
            Three steps. That's it.
          </h2>
        </motion.div>

        <div className="grid md:grid-cols-3 gap-12">
          {steps.map((step, i) => (
            <motion.div
              key={step.number}
              initial={{ opacity: 0, y: 20 }}
              whileInView={{ opacity: 1, y: 0 }}
              viewport={{ once: true }}
              transition={{ duration: 0.5, delay: i * 0.15 }}
              className="text-center"
            >
              <div className="relative inline-flex mb-6">
                <div className="w-16 h-16 rounded-2xl bg-sage-light flex items-center justify-center">
                  <step.icon className="w-7 h-7 text-foreground" />
                </div>
                <span className="absolute -top-2 -right-2 w-7 h-7 rounded-full bg-foreground text-background text-xs font-body font-bold flex items-center justify-center">
                  {step.number}
                </span>
              </div>
              <h3 className="text-xl mb-3 text-foreground">{step.title}</h3>
              <p className="text-muted-foreground font-body leading-relaxed max-w-xs mx-auto">{step.description}</p>
            </motion.div>
          ))}
        </div>
      </div>
    </section>
  );
};

export default HowItWorksSection;
