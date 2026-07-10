"use client";
import Link from "next/link";
import { ArrowRight, CalendarCheck, CheckCircle2, MapPin, PackageCheck, Plane, ShoppingCart } from "lucide-react";
import WhatsAppCTA from "@/components/public/WhatsAppCTA";
import type { LoadingDate } from "@/types/api";
import { useTranslation } from "@/lib/i18n";
import { ACCEPTED_ITEMS, COMPANY_NAME, COMPANY_SLOGAN, NCKL_LOCATIONS, TIKTOK_HANDLE } from "@/lib/constants";

const routeCards = [
  { from: "Germany & Europe", to: "Cameroon", time: "3 - 10 days" },
  { from: "Cameroon", to: "Germany & Europe", time: "3 - 10 days" },
];

const serviceHighlights = [
  "Shopping assistance in Douala and Bamenda",
  "Package pickup from travel agencies in Douala",
  "Packages received from any region in Cameroon",
  "Shipping to all European countries",
];

function formatLoadingDate(iso: string): string {
  const [year, month, day] = iso.split("-");
  return day + "." + month + "." + year;
}

export default function HeroSection({ nextLoading }: { nextLoading?: LoadingDate | null }) {
  const { t } = useTranslation();
  const announcement = nextLoading
    ? t("Next NCKL departure: {date}", { date: formatLoadingDate(nextLoading.date) })
    : t("Germany and Europe to Cameroon. Cameroon to Germany and Europe.");

  return (
    <section className="relative overflow-hidden bg-brand-navy text-white">
      <div className="absolute inset-0 opacity-[0.18]" aria-hidden="true">
        <div className="h-full w-full bg-[linear-gradient(90deg,rgba(255,255,255,.08)_1px,transparent_1px),linear-gradient(0deg,rgba(255,255,255,.08)_1px,transparent_1px)] bg-[size:56px_56px]" />
      </div>
      <div className="container-page relative py-10 sm:py-14 lg:py-16">
        <div className="grid gap-8 lg:grid-cols-[1.05fr_.95fr] lg:items-center">
          <div>
            <div className="inline-flex items-center gap-3 border-b border-brand-red pb-3 pr-6">
              <span className="flex h-14 w-14 items-center justify-center rounded-md bg-white text-brand-navy shadow-soft">
                <Plane className="h-8 w-8 text-brand-red" />
              </span>
              <div>
                <p className="bg-gradient-to-b from-white to-gray-300 bg-clip-text font-display text-4xl font-black leading-none text-transparent sm:text-5xl">
                  NCKL
                </p>
                <p className="text-xs font-bold uppercase text-white sm:text-sm">Logistics Services</p>
              </div>
            </div>

            <p className="mt-5 font-display text-xl italic text-white sm:text-2xl">{COMPANY_SLOGAN}</p>
            <p className="mt-3 inline-flex rounded-md bg-brand-gold px-3 py-1 text-sm font-black uppercase text-brand-navy">
              {t("New in town")}
            </p>

            <h1 className="mt-6 max-w-3xl font-display text-4xl font-black leading-tight text-white sm:text-5xl lg:text-6xl">
              {t("Bidirectional air cargo between Cameroon, Germany and Europe")}
            </h1>
            <p className="mt-5 max-w-2xl text-base leading-7 text-navy-100 sm:text-lg">
              {t("Shopping assistance, drop-off handling, travel-agency pickup and parcel forwarding through NCKL locations in Bamenda, Douala, Berlin and Leipzig.")}
            </p>

            <div className="mt-8 flex flex-col gap-3 sm:flex-row sm:flex-wrap">
              <Link href="/demande" className="btn-primary !px-7 !py-3.5 text-base">
                {t("cta.request")} <ArrowRight className="h-5 w-5" />
              </Link>
              <WhatsAppCTA className="!px-7 !py-3.5 text-base" />
            </div>
          </div>

          <div className="rounded-lg border border-white/15 bg-white/10 p-4 shadow-soft-lg backdrop-blur-sm sm:p-5">
            <div className="mb-4 flex items-center gap-2 rounded-md bg-brand-red px-4 py-3 text-sm font-black uppercase text-white">
              <CalendarCheck className="h-5 w-5 text-brand-gold" />
              {announcement}
            </div>

            <div className="space-y-3">
              {routeCards.map((route) => (
                <div key={route.from} className="rounded-md border border-brand-gold/45 bg-brand-navy/85 p-4">
                  <div className="flex items-center justify-between gap-3 text-sm font-black uppercase sm:text-base">
                    <span>{t(route.from)}</span>
                    <Plane className="h-5 w-5 shrink-0 text-brand-gold" />
                    <span>{t(route.to)}</span>
                  </div>
                  <p className="mt-2 text-right text-lg font-black text-brand-gold">{route.time}</p>
                </div>
              ))}
            </div>

            <div className="mt-5 grid gap-4 sm:grid-cols-2">
              <div>
                <h2 className="flex items-center gap-2 text-sm font-black uppercase text-brand-gold">
                  <ShoppingCart className="h-4 w-4" /> {t("Services offered")}
                </h2>
                <ul className="mt-3 space-y-2 text-sm text-navy-100">
                  {serviceHighlights.map((item) => (
                    <li key={item} className="flex gap-2">
                      <CheckCircle2 className="mt-0.5 h-4 w-4 shrink-0 text-brand-gold" />
                      <span>{t(item)}</span>
                    </li>
                  ))}
                </ul>
              </div>

              <div>
                <h2 className="flex items-center gap-2 text-sm font-black uppercase text-brand-gold">
                  <PackageCheck className="h-4 w-4" /> {t("Accepted shipping items")}
                </h2>
                <div className="mt-3 flex flex-wrap gap-2">
                  {ACCEPTED_ITEMS.slice(0, 10).map((item) => (
                    <span key={item} className="rounded-md border border-white/15 bg-white/10 px-2 py-1 text-xs font-semibold text-white">
                      {t(item)}
                    </span>
                  ))}
                </div>
                <p className="mt-3 text-xs font-semibold text-brand-gold">
                  {t("Phones without battery: Germany to Cameroon only. Small household equipment: max 31 kg.")}
                </p>
              </div>
            </div>

            <div className="mt-5 rounded-md border border-white/10 bg-white/10 p-3">
              <div className="grid gap-2 sm:grid-cols-2">
                {NCKL_LOCATIONS.map((location) => (
                  <div key={location.city} className="flex gap-2 text-xs text-navy-100">
                    <MapPin className="mt-0.5 h-4 w-4 shrink-0 text-brand-red" />
                    <div>
                      <p className="font-black text-white">{location.city}</p>
                      <p>{location.label}</p>
                      <p className="font-semibold text-brand-gold">{location.contact}</p>
                    </div>
                  </div>
                ))}
              </div>
            </div>

            <p className="mt-4 text-right text-xs font-semibold text-navy-200">
              {COMPANY_NAME} · {TIKTOK_HANDLE}
            </p>
          </div>
        </div>
      </div>
    </section>
  );
}
