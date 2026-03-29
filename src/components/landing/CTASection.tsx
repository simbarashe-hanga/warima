import { motion } from "framer-motion";
import { Button } from "@/components/ui/button";
import { Wallet, MessageCircle } from "lucide-react";
import { ConnectButton } from "@rainbow-me/rainbowkit";

const WHATSAPP_LINK = "https://wa.me/1234567890?text=Hi%20Warima";

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
            Your AI-powered DeFi team is one click away
          </h2>
          <p className="text-lg text-off-white/70 font-body mb-10 max-w-md mx-auto">
            Connect your wallet and unlock expert-level DeFi guidance powered by multi-agent AI.
          </p>

          <div className="flex flex-col sm:flex-row gap-4 justify-center">
            <ConnectButton.Custom>
              {({ openConnectModal, account }) => (
                <Button
                  size="xl"
                  className="bg-gold-accent text-charcoal hover:bg-gold-accent/90 shadow-lg hover:shadow-xl hover:-translate-y-0.5 transition-all"
                  onClick={openConnectModal}
                >
                  <Wallet className="w-5 h-5" />
                  {account ? account.displayName : "Connect Wallet"}
                </Button>
              )}
            </ConnectButton.Custom>
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
