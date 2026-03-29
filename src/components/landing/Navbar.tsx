import { useState } from "react";
import { Button } from "@/components/ui/button";
import { Menu, X, MessageCircle } from "lucide-react";
import { ConnectButton } from "@rainbow-me/rainbowkit";
import warimaLogo from "@/assets/warima-logo.png";

const WHATSAPP_LINK = "https://wa.me/1234567890?text=Hi%20Warima";

const Navbar = () => {
  const [open, setOpen] = useState(false);

  return (
    <nav className="fixed top-0 left-0 right-0 z-50 bg-background/80 backdrop-blur-md border-b border-border">
      <div className="container flex items-center justify-between h-16">
        <a href="#" className="flex items-center gap-2">
          <img src={warimaLogo} alt="Warima" className="w-8 h-8" />
          <span className="font-display text-xl tracking-tight text-foreground">Warima</span>
        </a>

        <div className="hidden md:flex items-center gap-8">
          <a href="#features" className="text-sm text-muted-foreground hover:text-foreground transition-colors">Features</a>
          <a href="#how-it-works" className="text-sm text-muted-foreground hover:text-foreground transition-colors">How it Works</a>
          <a href="#faq" className="text-sm text-muted-foreground hover:text-foreground transition-colors">FAQ</a>
          <ConnectButton
            chainStatus="icon"
            showBalance={false}
            accountStatus="address"
          />
        </div>

        <button className="md:hidden" onClick={() => setOpen(!open)}>
          {open ? <X className="w-6 h-6" /> : <Menu className="w-6 h-6" />}
        </button>
      </div>

      {open && (
        <div className="md:hidden bg-background border-b border-border px-6 pb-6 space-y-4">
          <a href="#features" onClick={() => setOpen(false)} className="block text-sm text-muted-foreground">Features</a>
          <a href="#how-it-works" onClick={() => setOpen(false)} className="block text-sm text-muted-foreground">How it Works</a>
          <a href="#faq" onClick={() => setOpen(false)} className="block text-sm text-muted-foreground">FAQ</a>
          <div className="pt-2">
            <ConnectButton
              chainStatus="icon"
              showBalance={false}
              accountStatus="address"
            />
          </div>
        </div>
      )}
    </nav>
  );
};

export default Navbar;
