import { ncklConfig } from "@/lib/nckl-config";

export const API_BASE_URL = process.env.NEXT_PUBLIC_API_URL || "http://localhost:8000/api";
export const COMPANY_NAME = ncklConfig.companyName;
export const COMPANY_SHORT_NAME = ncklConfig.shortName;
export const COMPANY_SLOGAN = ncklConfig.slogan;
export const WHATSAPP_NUMBER = ncklConfig.primaryWhatsApp;
export const SUPPORT_EMAIL = ncklConfig.supportEmail;
export const TIKTOK_HANDLE = ncklConfig.tikTokHandle;
export const PICKUP_CITIES = ncklConfig.dropOffCities;
export const DELIVERY_CITIES = ["Cameroon", "Germany", "Europe"] as const;
export const ACCEPTED_ITEMS = ncklConfig.acceptedItems;
