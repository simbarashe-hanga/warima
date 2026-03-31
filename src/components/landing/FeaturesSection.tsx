import { motion } from "framer-motion";
import { PiggyBank, Users, TrendingUp, Lightbulb, FileText, Target, Zap, HeadphonesIcon, Clock } from "lucide-react";

const pillars = [
  {
    title: "Savings & Stokvel Manager",
    color: "bg-warima-green/15",
    features: [
      { icon: PiggyBank, label: "Contribution tracking" },
      { icon: Users, label: "Member management" },
      { icon: TrendingUp, label: "Payout scheduling" },
    ],
  },
  {
    title: "Financial Guidance",
    color: "bg-gold-accent/15",
    features: [
      { icon: Lightbulb, label: "Investment tips" },
      { icon: FileText, label: "Budgeting advice" },
      { icon: Target, label: "Savings goals" },
    ],
  },
  {
    title: "Community Coordination",
    color: "bg-muted",
    features: [
      { icon: Zap, label: "Smart reminders" },
      { icon: HeadphonesIcon, label: "Group Q&A" },
      { icon: Clock, label: "24/7 availability" },
    ],
  },
];

const FeaturesSection = () => {
  return (
    <section id="features" className="py-20 md:py-28 bg-card">
      <div className="container">
        <motion.div
          initial={{ opacity: 0, y: 20 }}
          whileInView={{ opacity: 1, y: 0 }}
          viewport={{ once: true }}
          transition={{ duration: 0.5 }}
          className="text-center mb-16"
        >
          <p className="text-sm font-body font-semibold tracking-widest uppercase text-muted-foreground mb-3">Features</p>
          <h2 className="text-3xl md:text-4xl tracking-tight text-foreground">
            Three agents. One mission.
          </h2>
        </motion.div>

        <div className="grid md:grid-cols-3 gap-8">
          {pillars.map((pillar, i) => (
            <motion.div
              key={pillar.title}
              initial={{ opacity: 0, y: 20 }}
              whileInView={{ opacity: 1, y: 0 }}
              viewport={{ once: true }}
              transition={{ duration: 0.5, delay: i * 0.15 }}
              className="bg-background rounded-2xl border border-border p-8"
            >
              <h3 className="text-2xl mb-6 text-foreground">{pillar.title}</h3>
              <div className="space-y-4">
                {pillar.features.map((f) => (
                  <div key={f.label} className="flex items-center gap-3">
                    <div className={`w-9 h-9 rounded-lg ${pillar.color} flex items-center justify-center shrink-0`}>
                      <f.icon className="w-4 h-4 text-foreground" />
                    </div>
                    <span className="font-body text-foreground">{f.label}</span>
                  </div>
                ))}
              </div>
            </motion.div>
          ))}
        </div>
      </div>
    </section>
  );
};

export default FeaturesSection;
