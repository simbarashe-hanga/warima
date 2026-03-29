import { useState, useEffect } from "react";
import { Button } from "@/components/ui/button";
import { Wallet } from "lucide-react";
import { motion, AnimatePresence } from "framer-motion";
import { ConnectButton } from "@rainbow-me/rainbowkit";

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
          <ConnectButton.Custom>
            {({ openConnectModal, account }) => (
              <Button
                variant="hero"
                size="lg"
                className="rounded-full shadow-2xl"
                onClick={openConnectModal}
              >
                <Wallet className="w-5 h-5" />
                {account ? account.displayName : "Connect"}
              </Button>
            )}
          </ConnectButton.Custom>
        </motion.div>
      )}
    </AnimatePresence>
  );
};

export default StickyCTA;
