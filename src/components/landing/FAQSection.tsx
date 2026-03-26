import { motion } from "framer-motion";
import {
  Accordion,
  AccordionContent,
  AccordionItem,
  AccordionTrigger,
} from "@/components/ui/accordion";

const faqs = [
  {
    q: "Do I need to install anything?",
    a: "Nope! Mission Control AI works entirely through WhatsApp. Just send a message and you're connected — no downloads, no sign-ups, no extra apps.",
  },
  {
    q: "Is my data safe?",
    a: "Absolutely. We use end-to-end encryption and never share your data with third parties. Your conversations and financial information remain private and secure.",
  },
  {
    q: "Can I use it for my business?",
    a: "Yes! Mission Control AI is built specifically for small businesses, entrepreneurs, and community groups. Whether you run a shop, a stokvel, or a freelance business — we've got you covered.",
  },
  {
    q: "How does the multi-agent system work?",
    a: "When you send a message, our AI automatically detects whether you need help with finances, marketing, or customer support — and routes you to the right specialist agent. It all happens seamlessly in one chat.",
  },
  {
    q: "What does it cost?",
    a: "We offer a free tier to get started. Premium plans with advanced features are available for growing businesses. Message us on WhatsApp to learn more!",
  },
];

const FAQSection = () => {
  return (
    <section id="faq" className="py-20 md:py-28">
      <div className="container max-w-2xl">
        <motion.div
          initial={{ opacity: 0, y: 20 }}
          whileInView={{ opacity: 1, y: 0 }}
          viewport={{ once: true }}
          transition={{ duration: 0.5 }}
          className="text-center mb-12"
        >
          <p className="text-sm font-body font-semibold tracking-widest uppercase text-muted-foreground mb-3">FAQ</p>
          <h2 className="text-3xl md:text-4xl tracking-tight text-foreground">
            Questions? We've got answers.
          </h2>
        </motion.div>

        <motion.div
          initial={{ opacity: 0, y: 20 }}
          whileInView={{ opacity: 1, y: 0 }}
          viewport={{ once: true }}
          transition={{ duration: 0.5 }}
        >
          <Accordion type="single" collapsible className="space-y-3">
            {faqs.map((faq, i) => (
              <AccordionItem key={i} value={`faq-${i}`} className="bg-card border border-border rounded-xl px-6">
                <AccordionTrigger className="font-body font-semibold text-foreground text-left hover:no-underline">
                  {faq.q}
                </AccordionTrigger>
                <AccordionContent className="text-muted-foreground font-body leading-relaxed">
                  {faq.a}
                </AccordionContent>
              </AccordionItem>
            ))}
          </Accordion>
        </motion.div>
      </div>
    </section>
  );
};

export default FAQSection;
