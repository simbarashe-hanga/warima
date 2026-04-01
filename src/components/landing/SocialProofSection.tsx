import { motion } from "framer-motion";

const metrics = [
  { value: "10+", label: "Hours saved per week" },
  { value: "40%", label: "Increase in engagement" },
  { value: "24/7", label: "Always available" },
  { value: "3-in-1", label: "AI agents working for you" },
];

const recognition = {
  title: "\"On My Way\" Award Winner",
  description: "ALX Future Founder SA — sponsored by Yoma, SAP, FNB, UN Generation Unlimited & GoodWall.",
};

const SocialProofSection = () => {
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
          <p className="text-sm font-body font-semibold tracking-widest uppercase text-muted-foreground mb-3">Social Proof</p>
          <h2 className="text-3xl md:text-4xl tracking-tight text-foreground">
            Trusted by businesses across Africa
          </h2>
        </motion.div>

        {/* Recognition */}
        <motion.div
          initial={{ opacity: 0, y: 20 }}
          whileInView={{ opacity: 1, y: 0 }}
          viewport={{ once: true }}
          transition={{ duration: 0.5 }}
          className="mb-16 p-6 md:p-8 rounded-2xl bg-background border border-border text-center"
        >
          <p className="text-sm font-body font-semibold tracking-widest uppercase text-muted-foreground mb-2">Recognition</p>
          <h3 className="text-2xl md:text-3xl font-display text-foreground mb-2">{recognition.title}</h3>
          <p className="text-muted-foreground font-body max-w-lg mx-auto">{recognition.description}</p>
        </motion.div>

        {/* Metrics */}
        <div className="grid grid-cols-2 md:grid-cols-4 gap-6 mb-16">
          {metrics.map((m, i) => (
            <motion.div
              key={m.label}
              initial={{ opacity: 0, y: 20 }}
              whileInView={{ opacity: 1, y: 0 }}
              viewport={{ once: true }}
              transition={{ duration: 0.5, delay: i * 0.1 }}
              className="text-center p-6 rounded-2xl bg-background border border-border"
            >
              <div className="text-3xl md:text-4xl font-display text-foreground mb-1">{m.value}</div>
              <div className="text-sm text-muted-foreground font-body">{m.label}</div>
            </motion.div>
          ))}
        </div>

        {/* Testimonials */}
        <div className="grid md:grid-cols-3 gap-8">
          {testimonials.map((t, i) => (
            <motion.div
              key={t.name}
              initial={{ opacity: 0, y: 20 }}
              whileInView={{ opacity: 1, y: 0 }}
              viewport={{ once: true }}
              transition={{ duration: 0.5, delay: i * 0.1 }}
              className="bg-background rounded-2xl border border-border p-8"
            >
              <div className="flex gap-1 mb-4">
                {[...Array(5)].map((_, j) => (
                  <Star key={j} className="w-4 h-4 fill-gold-accent text-gold-accent" />
                ))}
              </div>
              <p className="text-foreground font-body leading-relaxed mb-6">"{t.quote}"</p>
              <div>
                <p className="font-body font-semibold text-foreground">{t.name}</p>
                <p className="text-sm text-muted-foreground font-body">{t.role}</p>
              </div>
            </motion.div>
          ))}
        </div>
      </div>
    </section>
  );
};

export default SocialProofSection;
