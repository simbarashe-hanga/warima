const Footer = () => {
  return (
    <footer className="py-12 border-t border-border">
      <div className="container flex flex-col md:flex-row items-center justify-between gap-4">
        <span className="font-display text-lg text-foreground">Mission Control AI</span>
        <p className="text-sm text-muted-foreground font-body">
          © {new Date().getFullYear()} Mission Control AI. All rights reserved.
        </p>
      </div>
    </footer>
  );
};

export default Footer;
