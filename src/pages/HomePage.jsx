import { Bell, Search, UserCircle2, ShieldCheck, Layers, TrendingUp, Phone, Mail, MapPin, ArrowRight } from 'lucide-react';

const features = [
  { title: 'Integrated Operations', description: 'Unified workforce, logistics and warehouse management for steel manufacturing.', icon: Layers },
  { title: 'Real-time Visibility', description: 'Live tracking, alerts and analytics to support timely decision-making.', icon: TrendingUp },
  { title: 'Secure Compliance', description: 'Built for enterprise-grade workflows with safety and compliance in mind.', icon: ShieldCheck },
];



function HomePage({ onNavigateToLogin = () => {} }) {
  return (
    <div className="min-h-screen light-page">
      <div className="border-b border-slate-200 bg-white/95 backdrop-blur-xl">
        <div className="mx-auto flex max-w-7xl items-center justify-between gap-4 px-4 py-4 sm:px-6 lg:px-8">
          <div className="flex items-center gap-3">
              <img src="src/images/logo.png" alt="logo" className='flex h-12 w-15'/>
            <div>
              <p className="text-xs uppercase tracking-[0.3em] text-slate-400">Swajit Engineering, Chhatrapati Sambhajinagar</p>
              <p className="text-sm font-semibold text-slate-950">ERP & Operations Platform</p>
            </div>
          </div>

          {/*<div className="flex flex-1 items-center justify-center">
            <div className="relative w-full max-w-xl">
              <Search className="pointer-events-none absolute left-4 top-1/2 h-4 w-4 -translate-y-1/2 text-slate-400" />
              <input
                type="search"
                placeholder="Search for products, services, contact..."
                className="h-11 w-full rounded-full border border-slate-200 bg-slate-50 px-12 text-sm text-slate-900 outline-none transition focus:border-brand-700 focus:ring-2 focus:ring-brand-100"
              />
            </div>
          </div>*/}

          <div className="flex items-center gap-3">
              <button type="button" onClick={onNavigateToLogin} className="flex h-16 w-16 flex-col items-center justify-center rounded-2xl border border-slate-200 bg-white text-slate-700 transition hover:border-slate-300 hover:text-slate-900">
                <UserCircle2 className="h-5 w-5" />
                  <span className="text-xs">Login</span>
              </button>
          </div>
        </div>
      </div>

        <main className="space-y-10">
          <section className="rounded-[2rem] border border-slate-200/80 bg-white p-8 shadow-xl">
            <div className="grid gap-8 lg:grid-cols-[1.2fr_0.8fr] lg:items-center">
              <div>
                <h1 className="mt-4 text-4xl font-semibold tracking-tight text-slate-950 sm:text-5xl">
                  Modern ERP for India's No.1 customized solution provider for industrial chains!!
                </h1>
                <p className="mt-6 max-w-2xl text-base leading-8 text-slate-600">
                  Swajit Engineering's enterprise dashboard brings manufacturing, logistics, and workforce intelligence into one premium portal. Designed for executives, operations teams, and manufacturing leaders.
                </p>
                <div className="mt-8 flex flex-wrap gap-4">
                  <button onClick={onNavigateToLogin} className="inline-flex items-center gap-2 rounded-full bg-brand-900 px-6 py-3 text-sm font-semibold text-white shadow-lg shadow-brand-900/10 transition hover:bg-brand-700">
                    Login to Dashboard
                    <ArrowRight className="h-4 w-4" />
                  </button>
                  <a href="#features" className="inline-flex items-center gap-2 rounded-full border border-slate-300 bg-white px-6 py-3 text-sm font-semibold text-slate-900 transition hover:border-slate-400 hover:bg-slate-50">
                    See Features
                  </a>
                </div>
              </div>

              <div className="rounded-[2rem] bg-slate-50 p-8 text-slate-900 shadow-xl">
                <h2 className="mt-5 text-3xl font-semibold text-slate-950">Swajit Engineering Pvt. Ltd.</h2>
                <p className="text-sm uppercase tracking-[0.24em] text-slate-500 mt-4 leading-7">
                  Chhatrapati Sambhajinagar
                </p>
                <p className="mt-4 leading-7 text-slate-700" align="justify">
                  Founded in 1991 in Chhatrapati Sambhajinagar, Maharashtra, Swajit Engineering Pvt. Ltd. has grown to become India's No. 1 conveyor chain manufacturer with over three decades of expertise serving diverse industries.
                  Our state-of-the-art facility spans 1,20,000+ sq ft, equipped with PLC-controlled heat treatment furnaces and advanced testing labs.
                </p>
                <div className="mt-8 space-y-4 text-sm text-slate-600">
                  <p className="flex items-center gap-3"><span className="inline-flex h-2.5 w-2.5 rounded-full bg-emerald-400" /> Trusted vendor for large-scale projects</p>
                  <p className="flex items-center gap-3"><span className="inline-flex h-2.5 w-2.5 rounded-full bg-emerald-400" /> 20+ years of manufacturing excellence</p>
                  <p className="flex items-center gap-3"><span className="inline-flex h-2.5 w-2.5 rounded-full bg-emerald-400" /> Secure, compliant, performance-driven operations</p>
                </div>
              </div>
            </div>
          </section>

          <section id="about" className="rounded-[2rem] border border-slate-200/80 bg-white p-8 shadow-xl">
            <div className="text-center">
              <p className="text-sm uppercase tracking-[0.2em] text-brand-700">About Our Company</p>
              <h2 className="mt-4 text-3xl font-semibold text-slate-950">India's No.1 customized solution provider for industrial chains — since 1991</h2>
            </div>
            <div className="mt-10 grid gap-8 lg:grid-cols-[1.1fr_0.9fr]">
              <div>
                <p className="text-sm font-semibold uppercase tracking-[0.2em] text-amber-600">Welcome to Swajit Engineering Pvt. Ltd.</p>
                <h3 className="mt-4 text-2xl font-semibold text-slate-950">CONVEYOR CHAINS, SLATS, AND SCRAPERS MANUFACTURERS AND SUPPLIERS IN CHHATRAPATI  SAMBHAJINAGAR, MAHARASHTRA, INDIA</h3>
                <div className="mt-6 space-y-5 text-sm leading-7 text-slate-600">
                  <p>
                    Swajit Engineering Pvt. Ltd. based at Aurangabad (M.S.), India has great pleasure to introduce as India's No.1 & one of the leading brands with "Customize Solution Provider for Industrial Chains".
                  </p>
                  <p>
                    Since the inception in 1991, Swajit has emerged as the leading manufacturer of all types of Roller Conveyor Chains and any type of Link, Pin and Bush Mechanism Heavy Duty Chains for Material Handling Systems.
                  </p>
                  <p>
                    Swajit is equipped with the latest technology comprising a 'State-of-the-Art Plant' with all infrastructure facilities & processes, and an advanced metallurgical laboratory to manufacture all types of Conveyor chains and Sprockets of the finest quality.
                  </p>
                </div>
              </div>

              <div className="grid gap-4 md:grid-cols-2">
                <div className="rounded-[1.65rem] border border-slate-200/80 bg-slate-50 p-6 shadow-sm">
                  <p className="text-sm font-semibold uppercase tracking-[0.24em] text-brand-700">Topmost Manufacturer in India</p>
                  <p className="mt-4 text-sm leading-6 text-slate-600">One of the topmost transmission and conveyor chain manufacturers in India.</p>
                </div>
                <div className="rounded-[1.65rem] border border-slate-200/80 bg-slate-50 p-6 shadow-sm">
                  <p className="text-sm font-semibold uppercase tracking-[0.24em] text-brand-700">ISI Specification Standards</p>
                  <p className="mt-4 text-sm leading-6 text-slate-600">We follow and continuously update all ISI specifications to set international standards.</p>
                </div>
                <div className="rounded-[1.65rem] border border-slate-200/80 bg-slate-50 p-6 shadow-sm">
                  <p className="text-sm font-semibold uppercase tracking-[0.24em] text-brand-700">Rigorous Quality Control</p>
                  <p className="mt-4 text-sm leading-6 text-slate-600">Our highly qualified QC team examines products on multiple parameters for flawless performance and durability.</p>
                </div>
                <div className="rounded-[1.65rem] border border-slate-200/80 bg-slate-50 p-6 shadow-sm">
                  <p className="text-sm font-semibold uppercase tracking-[0.24em] text-brand-700">Timely & Cost-Effective Delivery</p>
                  <p className="mt-4 text-sm leading-6 text-slate-600">We prioritize delivering rich-quality products and services within the agreed timeframe.</p>
                </div>
              </div>
            </div>
          </section>

          <section id="features" className="rounded-[2rem] border border-slate-200/80 bg-white p-8 shadow-xl">
            <div className="flex flex-col gap-6 sm:flex-row sm:items-end sm:justify-between">
              <div>
                <p className="text-sm uppercase tracking-[0.24em] text-slate-400">Features</p>
                <h2 className="mt-3 text-3xl font-semibold text-slate-950">Enterprise capabilities for production and logistics</h2>
              </div>
            </div>
            <div className="mt-8 grid gap-4 md:grid-cols-3">
              {features.map((feature) => {
                const Icon = feature.icon;
                return (
                  <div key={feature.title} className="rounded-[1.75rem] border border-slate-200/80 bg-slate-50 p-6 shadow-sm transition hover:-translate-y-1 hover:shadow-lg">
                    <div className="inline-flex h-12 w-12 items-center justify-center rounded-3xl bg-brand-900 text-white shadow-lg shadow-brand-900/10">
                      <Icon className="h-5 w-5" />
                    </div>
                    <h3 className="mt-6 text-xl font-semibold text-slate-950">{feature.title}</h3>
                    <p className="mt-3 text-sm leading-6 text-slate-600">{feature.description}</p>
                  </div>
                );
              })}
            </div>
          </section>

          <section id="contact" className="rounded-[2rem] border border-slate-200/80 bg-white p-8 shadow-xl">
            <div className="flex flex-col gap-6 lg:flex-row lg:items-start lg:justify-between">
              <div>
                <p className="text-sm uppercase tracking-[0.24em] text-slate-400">Contact Us</p>
                <h2 className="mt-3 text-3xl font-semibold text-slate-950">Reach Out to Swajit Engineering</h2>
                <p className="mt-4 max-w-xl text-sm leading-7 text-slate-600">
                  For inquiries, partnership requests, or enterprise demos, contact our support team directly. We deliver industry-leading steel manufacturing solutions with fast response and expert guidance.
                </p>
              </div>
              <div className="grid gap-4 rounded-[1.75rem] border border-slate-200/80 bg-slate-50 p-6 shadow-sm">
                <div className="flex items-start gap-3 text-slate-700">
                  <MapPin className="mt-1 h-5 w-5 text-brand-700" />
                  <div>
                    <p className="text-sm font-semibold text-slate-950">K-9, M.I.D.C., Waluj, Ch.Sambhajinagar</p>
                    <p className="text-sm text-slate-600">(Aurangabad) - 431136, Maharashtra, India</p>
                  </div>
                </div>
                <div className="flex items-center gap-3 text-slate-700">
                  <Phone className="h-5 w-5 text-brand-700" />
                  <span>+91 240 2555031 / 2554531</span>
                </div>
                <div className="flex items-center gap-3 text-slate-700">
                  <Phone className="h-5 w-5 text-brand-700" />
                  <span>+91 99229 41689 (WhatsApp)</span>
                </div>
                <div className="flex items-center gap-3 text-slate-700">
                  <Mail className="h-5 w-5 text-brand-700" />
                  <span>marketing@swajit.com</span>
                </div>
                <button onClick={onNavigateToLogin} className="mt-4 inline-flex w-full items-center justify-center rounded-full bg-brand-900 px-5 py-3 text-sm font-semibold text-white transition hover:bg-brand-700">
                  Login to continue
                </button>
              </div>
            </div>
          </section>
        </main>
    </div>
  );
}

export default HomePage;
