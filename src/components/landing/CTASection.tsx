import { motion } from "framer-motion";
import { Button } from "@/components/ui/button";
import { MessageCircle, ArrowRight } from "lucide-react";

const WHATSAPP_LINK = "https://wa.me/27698913277?text=Hi%20Warima";

const CTASection = () => {
  return (
    <section className="py-20 md:py-28 bg-deep-forest">
      <div className="container text-center">
        <motion.div
          initial={{ opacity: 0, y: 20 }}
          whileInView={{ opacity: 1, y: 0 }}
          viewport={{ once: true }}
          transition={{ duration: 0.5 }}
          className="max-w-2xl mx-auto"
        >
          <h2 className="text-3xl md:text-5xl tracking-tight text-off-white mb-6">
            Your AI team is one message away
          </h2>
          <p className="text-lg text-off-white/70 font-body mb-10 max-w-md mx-auto">
            Join thousands of businesses already saving time, growing faster, and serving customers better.
          </p>

          <div className="flex flex-col sm:flex-row gap-4 justify-center">
            <Button size="xl" className="bg-gold-accent text-charcoal hover:bg-gold-accent/90 shadow-lg hover:shadow-xl hover:-translate-y-0.5 transition-all" asChild>
              <a href={WHATSAPP_LINK} target="_blank" rel="noopener noreferrer">
                <MessageCircle className="w-5 h-5" />
                Start on WhatsApp
              </a>
            </Button>
            <Button size="xl" className="bg-transparent border-2 border-off-white/30 text-off-white hover:bg-off-white/10 transition-all" asChild>
              <a href="#demo">
                Book a Demo
                <ArrowRight className="w-5 h-5" />
              </a>
            </Button>
          </div>
        </motion.div>
      </div>
    </section>
  );
};

export default CTASection;
