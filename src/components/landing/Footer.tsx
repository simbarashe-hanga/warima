import warimaLogo from "@/assets/warima-logo.png";
import { Button } from "@/components/ui/button";
import { Calendar } from "lucide-react";

const CALENDLY_LINK = "https://calendly.com/simba-hanga/30min";

const Footer = () => {
  return (
    <footer className="py-12 border-t border-border">
      <div className="container flex flex-col md:flex-row items-center justify-between gap-4">
        <a href="#" className="flex items-center gap-2">
          <img src={warimaLogo} alt="Warima" className="w-7 h-7" />
          <span className="font-display text-lg text-foreground">Warima</span>
        </a>
        
        <Button variant="outline" size="sm" className="gap-2" asChild>
          <a href={CALENDLY_LINK} target="_blank" rel="noopener noreferrer">
            <Calendar className="w-4 h-4" />
            Book a Demo
          </a>
        </Button>
        
        <p className="text-sm text-muted-foreground font-body">
          © {new Date().getFullYear()} Warima. All rights reserved.
        </p>
      </div>
    </footer>
  );
};

export default Footer;
