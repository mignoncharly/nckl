"use client";
import { ClipboardList, MapPin, MessageCircle, PackageCheck, Plane } from "lucide-react";
import { useTranslation } from "@/lib/i18n";

const steps = [
  { icon: ClipboardList, title: "Choose the NCKL route", text: "Select Germany/Europe to Cameroon or Cameroon to Germany/Europe." },
  { icon: PackageCheck, title: "Describe the shipment", text: "Choose the item category, enter the weight and confirm special rules such as phones without batteries." },
  { icon: MapPin, title: "Use an NCKL point", text: "Drop off or coordinate handling in Bamenda, Douala, Berlin or Leipzig." },
  { icon: MessageCircle, title: "Confirm by WhatsApp", text: "NCKL confirms shopping assistance, pickup details, price and schedule information." },
  { icon: Plane, title: "Follow the shipment", text: "Track request status from confirmation through departure, arrival and delivery." },
];

export default function HowItWorks() {
  const { t } = useTranslation();
  return (
    <ol className="grid grid-cols-1 gap-6 sm:grid-cols-2 lg:grid-cols-5">
      {steps.map(({ icon: Icon, title, text }, i) => (
        <li key={title} className="relative flex flex-col rounded-lg border border-gray-100 bg-white p-6 shadow-card">
          <div className="mb-4 flex items-center justify-between">
            <span className="flex h-11 w-11 items-center justify-center rounded-md bg-brand-navy text-white">
              <Icon className="h-6 w-6 text-brand-gold" />
            </span>
            <span className="font-display text-3xl font-black text-brand-red/15">{i + 1}</span>
          </div>
          <h3 className="font-semibold text-gray-900">{t(title)}</h3>
          <p className="mt-1.5 text-sm text-gray-600">{t(text)}</p>
        </li>
      ))}
    </ol>
  );
}
