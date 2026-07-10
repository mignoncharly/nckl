import type { Metadata, Viewport } from "next";
import { Inter } from "next/font/google";
import "@/styles/globals.css";
import AppNavbar from "@/components/layout/AppNavbar";
import Footer from "@/components/layout/Footer";
import MobileBottomCTA from "@/components/layout/MobileBottomCTA";
import { AuthProvider } from "@/hooks/useAuth";
import { LanguageProvider } from "@/lib/i18n";
import { Toaster } from "sonner";
import ServiceWorkerRegistration from "@/components/pwa/ServiceWorkerRegistration";
import InstallPWAButton from "@/components/pwa/InstallPWAButton";
import { getServerTranslation } from "@/lib/i18n-server";
import { ncklConfig } from "@/lib/nckl-config";

const inter = Inter({ subsets: ["latin"], display: "swap" });

export function generateMetadata(): Metadata {
  const { t } = getServerTranslation();
  return {
    title: t("NCKL Logistics Services – Un colis, un sourire…"),
    description: t("Parcel shipping between Germany, Europe, and Cameroon with shopping assistance and managed drop-off locations."),
    manifest: "/manifest.webmanifest",
  };
}

export const viewport: Viewport = {
  width: "device-width",
  initialScale: 1,
  maximumScale: 1,
  themeColor: "#0A2540",
};

export default function RootLayout({
  children,
}: {
  children: React.ReactNode;
}) {
  const { locale } = getServerTranslation();
  return (
    <html lang={locale}>
      <body className={inter.className}>
        <LanguageProvider initialLocale={locale}>
          <AuthProvider>
            <AppNavbar />
            <main className="min-h-screen">{children}</main>
            <Footer />
            <MobileBottomCTA />
            <ServiceWorkerRegistration />
            <InstallPWAButton />
            <Toaster position="top-center" richColors />
          </AuthProvider>
        </LanguageProvider>
      </body>
    </html>
  );
}
