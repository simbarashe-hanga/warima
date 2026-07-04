import { motion } from "framer-motion";
import { TrendingDown, Megaphone, Clock } from "lucide-react";

const problems = [
  {
    icon: TrendingDown,
    title: "Stokvel management is messy",
    description: "Tracking contributions, payouts, and member balances on paper or spreadsheets leads to confusion, disputes, and lost trust.",
  },
  {
    icon: Megaphone,
    title: "Financial guidance is out of reach",
    description: "Communities want to save and invest together, but affordable, culturally relevant financial advice is hard to find.",
  },
  {
    icon: Clock,
    title: "Coordination takes too much time",
    description: "Chasing members for payments, scheduling meetings, and keeping everyone aligned eats into the time you could spend growing.",
  },
];

const ProblemSection = () => {
  return (
    <section className="py-20 md:py-28 bg-card">
      <div className="container">
        <motion.div
          initial={{ opacity: 0, y: 20 }}
          whileInView={{ opacity: 1, y: 0 }}
          viewport={{ once: true }}
          transition={{ duration: 0.5 }}
          className="text-center mb-16"
        >
          <p className="text-sm font-body font-semibold tracking-widest uppercase text-muted-foreground mb-3">The Problem</p>
          <h2 className="text-3xl md:text-4xl tracking-tight text-foreground">
            Saving together shouldn't be this hard
          </h2>
        </motion.div>

        <div className="grid md:grid-cols-3 gap-8">
          {problems.map((problem, i) => (
            <motion.div
              key={problem.title}
              initial={{ opacity: 0, y: 20 }}
              whileInView={{ opacity: 1, y: 0 }}
              viewport={{ once: true }}
              transition={{ duration: 0.5, delay: i * 0.1 }}
              className="bg-background rounded-2xl p-8 border border-border"
            >
              <div className="w-12 h-12 rounded-xl bg-sand-light flex items-center justify-center mb-5">
                <problem.icon className="w-6 h-6 text-foreground" />
              </div>
              <h3 className="text-xl mb-3 text-foreground">{problem.title}</h3>
              <p className="text-muted-foreground font-body leading-relaxed">{problem.description}</p>
            </motion.div>
          ))}
        </div>
      </div>
    </section>
  );
};

export default ProblemSection;
