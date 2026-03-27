import { motion } from "framer-motion";

const messages = [
  { from: "user", text: "Hi, I want to start a stokvel with 10 members. How should we structure monthly contributions?" },
  { from: "ai", text: "Great idea! 🎯 For a 10-member stokvel, I'd suggest:\n\n• Fixed monthly contribution (e.g., R500/member)\n• Rotating payout schedule\n• Emergency fund reserve (10%)\n\nWant me to create a contribution tracker for your group?" },
  { from: "user", text: "Yes please! Also, can you help us promote our community savings group?" },
  { from: "ai", text: "Absolutely! 📢 I'll switch you to the marketing agent. Here's a quick campaign plan:\n\n1. WhatsApp broadcast to your network\n2. Social media post template\n3. Referral incentive structure\n\nShall I draft the content now?" },
];

const DemoChatSection = () => {
  return (
    <section id="demo" className="py-20 md:py-28">
      <div className="container max-w-2xl">
        <motion.div
          initial={{ opacity: 0, y: 20 }}
          whileInView={{ opacity: 1, y: 0 }}
          viewport={{ once: true }}
          transition={{ duration: 0.5 }}
          className="text-center mb-12"
        >
          <p className="text-sm font-body font-semibold tracking-widest uppercase text-muted-foreground mb-3">Live Preview</p>
          <h2 className="text-3xl md:text-4xl tracking-tight text-foreground">
            See it in action
          </h2>
        </motion.div>

        <motion.div
          initial={{ opacity: 0, y: 20 }}
          whileInView={{ opacity: 1, y: 0 }}
          viewport={{ once: true }}
          transition={{ duration: 0.6 }}
          className="bg-card rounded-2xl border border-border overflow-hidden shadow-lg"
        >
          {/* Chat header */}
          <div className="bg-foreground text-background px-6 py-4 flex items-center gap-3">
            <div className="w-10 h-10 rounded-full bg-sage flex items-center justify-center text-foreground font-body font-bold text-sm">W</div>
            <div>
              <div className="font-body font-semibold">Warima</div>
              <div className="text-xs opacity-70 font-body">Online</div>
            </div>
          </div>

          {/* Messages */}
          <div className="p-6 space-y-4 bg-sand-light/30">
            {messages.map((msg, i) => (
              <motion.div
                key={i}
                initial={{ opacity: 0, y: 10 }}
                whileInView={{ opacity: 1, y: 0 }}
                viewport={{ once: true }}
                transition={{ duration: 0.4, delay: i * 0.15 }}
                className={`flex ${msg.from === "user" ? "justify-end" : "justify-start"}`}
              >
                <div
                  className={`max-w-[80%] rounded-2xl px-4 py-3 font-body text-sm leading-relaxed whitespace-pre-line ${
                    msg.from === "user"
                      ? "bg-sage text-foreground rounded-br-md"
                      : "bg-card text-foreground border border-border rounded-bl-md"
                  }`}
                >
                  {msg.text}
                </div>
              </motion.div>
            ))}
          </div>
        </motion.div>
      </div>
    </section>
  );
};

export default DemoChatSection;
