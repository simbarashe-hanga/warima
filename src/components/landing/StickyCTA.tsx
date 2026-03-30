import { useState, useEffect } from "react";
import { Button } from "@/components/ui/button";
import { MessageCircle } from "lucide-react";
import { motion, AnimatePresence } from "framer-motion";

const WHATSAPP_LINK = "https://wa.me/1234567890?text=Hi%20Warima";

const StickyCTA = () => {
  const [visible, setVisible] = useState(false);

  useEffect(() => {
    const onScroll = () => setVisible(window.scrollY > 600);
    window.addEventListener("scroll", onScroll);
    return () => window.removeEventListener("scroll", onScroll);
  }, []);

  return (
    <AnimatePresence>
      {visible && (
        <motion.div
          initial={{ y: 100, opacity: 0 }}
          animate={{ y: 0, opacity: 1 }}
          exit={{ y: 100, opacity: 0 }}
          transition={{ duration: 0.3 }}
          className="fixed bottom-6 right-6 z-50 md:hidden"
        >
          <Button variant="hero" size="lg" className="rounded-full shadow-2xl" asChild>
            <a href={WHATSAPP_LINK} target="_blank" rel="noopener noreferrer">
              <MessageCircle className="w-5 h-5" />
              WhatsApp
            </a>
          </Button>
        </motion.div>
      )}
    </AnimatePresence>
  );
};

export default StickyCTA;
