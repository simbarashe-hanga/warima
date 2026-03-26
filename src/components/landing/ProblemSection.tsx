import { motion } from "framer-motion";
import { TrendingDown, Megaphone, Clock } from "lucide-react";

const problems = [
  {
    icon: TrendingDown,
    title: "Managing finances is confusing",
    description: "Stokvels, savings, and investments feel overwhelming without expert guidance — but hiring one costs too much.",
  },
  {
    icon: Megaphone,
    title: "Marketing is expensive & complex",
    description: "Creating campaigns, content, and a brand presence takes time and money most small businesses don't have.",
  },
  {
    icon: Clock,
    title: "Customer support is draining",
    description: "Answering the same questions 24/7 pulls you away from growing your business.",
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
            Growing a business shouldn't be this hard
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
