import { motion } from "framer-motion";
import { Button } from "@/components/ui/button";
import { MessageCircle, Play } from "lucide-react";
import heroPhone from "@/assets/hero-phone.png";

const WHATSAPP_LINK = "https://wa.me/27698913277?text=Hi%20Warima";

const HeroSection = () => {
  return (
    <section className="relative pt-32 pb-20 md:pt-40 md:pb-32 overflow-hidden">
      <div className="container">
        <div className="grid lg:grid-cols-2 gap-12 items-center">
          <motion.div
            initial={{ opacity: 0, y: 30 }}
            animate={{ opacity: 1, y: 0 }}
            transition={{ duration: 0.7, ease: "easeOut" }}
            className="max-w-xl"
          >
            <div className="inline-flex items-center gap-2 bg-warima-green/10 text-foreground px-4 py-1.5 rounded-full text-sm font-body mb-6">
              <span className="w-2 h-2 rounded-full bg-warima-green" />
              Powered by multi-agent AI
            </div>

            <h1 className="text-4xl md:text-5xl lg:text-6xl leading-[1.1] tracking-tight text-foreground mb-6">
              From stokvels to smart money on WhatsApp
            </h1>

            <p className="text-lg text-muted-foreground font-body leading-relaxed mb-8 max-w-md">
              Warima helps communities save, coordinate, and grow wealth together with AI-powered guidance — all inside the app they already use. No downloads. No complexity. Just progress.
            </p>

            <div className="flex flex-col sm:flex-row gap-4">
              <Button variant="hero" size="xl" asChild>
                <a href={WHATSAPP_LINK} target="_blank" rel="noopener noreferrer">
                  <MessageCircle className="w-5 h-5" />
                  Start on WhatsApp
                </a>
              </Button>
              <Button variant="hero-outline" size="xl" asChild>
                <a href="https://wa.me/27672489700?text=Hi%20Warima%2C%20I%27d%20like%20to%20book%20a%20demo" target="_blank" rel="noopener noreferrer">
                  <Play className="w-5 h-5" />
                  See Demo
                </a>
              </Button>
            </div>
          </motion.div>

          <motion.div
            initial={{ opacity: 0, scale: 0.95 }}
            animate={{ opacity: 1, scale: 1 }}
            transition={{ duration: 0.8, delay: 0.2, ease: "easeOut" }}
            className="relative flex justify-center lg:justify-end"
          >
            <div className="animate-float">
              <img
                src={heroPhone}
                alt="Warima WhatsApp conversation showing financial and marketing assistance"
                width={400}
                height={512}
                className="w-full max-w-[400px] drop-shadow-2xl"
              />
            </div>
          </motion.div>
        </div>
      </div>
    </section>
  );
};

export default HeroSection;
