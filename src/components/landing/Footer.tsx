import warimaLogo from "@/assets/warima-logo.png";

const Footer = () => {
  return (
    <footer className="py-12 border-t border-border">
      <div className="container flex flex-col md:flex-row items-center justify-between gap-4">
        <a href="#" className="flex items-center gap-2">
          <img src={warimaLogo} alt="Warima" className="w-7 h-7" />
          <span className="font-display text-lg text-foreground">Warima</span>
        </a>
        <p className="text-sm text-muted-foreground font-body">
          © {new Date().getFullYear()} Warima. All rights reserved.
        </p>
      </div>
    </footer>
  );
};

export default Footer;
