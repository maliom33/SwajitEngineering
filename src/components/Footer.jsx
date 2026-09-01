function Footer() {
  return (
    <footer className="border-t border-slate-200/80 bg-white/90 py-6">
      <div className="mx-auto flex max-w-7xl flex-col gap-6 px-4 text-sm text-slate-600 sm:flex-row sm:items-center sm:justify-between sm:px-6 lg:px-8">
        <div>
          <p className="font-semibold text-slate-950">Swajit Engineering Pvt. Ltd.</p>
          <p>Industrial Estate, Haldia Port Road, West Bengal, India</p>
        </div>
        <div className="space-y-1">
          <p>Phone: +91 33 1234 5678</p>
          <p>Email: contact@swajitengineering.com</p>
          <p>Website: www.swajitengineering.com</p>
        </div>
      </div>
    </footer>
  );
}

export default Footer;
