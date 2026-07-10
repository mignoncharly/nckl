"use client";
import { useForm } from "react-hook-form";
import { zodResolver } from "@hookform/resolvers/zod";
import { useRouter } from "next/navigation";
import { useState, useEffect, useMemo } from "react";
import { User, Boxes, MapPin, ImagePlus, NotebookPen, Route } from "lucide-react";
import { createTransportRequestSchema, type TransportRequestFormData } from "@/lib/validators";
import { api, parseApiError } from "@/lib/api";
import type { ServiceType, DestinationCity, RouteOption, AcceptedItemCategory, DropOffLocation, ShipmentSchedule } from "@/types/api";
import PageHeader from "@/components/ui/PageHeader";
import FormField from "@/components/ui/FormField";
import LoadingSpinner from "@/components/ui/LoadingSpinner";
import WhatsAppCTA from "@/components/public/WhatsAppCTA";
import { useTranslation } from "@/lib/i18n";

export default function DemandePage() {
  const router = useRouter();
  const { t } = useTranslation();
  const schema = useMemo(() => createTransportRequestSchema(t), [t]);
  const [services, setServices] = useState<ServiceType[]>([]);
  const [destinations, setDestinations] = useState<DestinationCity[]>([]);
  const [routes, setRoutes] = useState<RouteOption[]>([]);
  const [acceptedItems, setAcceptedItems] = useState<AcceptedItemCategory[]>([]);
  const [locations, setLocations] = useState<DropOffLocation[]>([]);
  const [shipmentSchedules, setShipmentSchedules] = useState<ShipmentSchedule[]>([]);
  const [loading, setLoading] = useState(false);
  const [error, setError] = useState<string | null>(null);

  useEffect(() => {
    api.get<ServiceType[]>("/services/").then(setServices).catch(console.error);
    api.get<DestinationCity[]>("/destination-cities/").then(setDestinations).catch(console.error);
    api.get<RouteOption[]>("/services/routes/").then(setRoutes).catch(console.error);
    api.get<AcceptedItemCategory[]>("/services/accepted-items/").then(setAcceptedItems).catch(console.error);
    api.get<DropOffLocation[]>("/pickup-schedules/drop-off-locations/").then(setLocations).catch(console.error);
    api.get<ShipmentSchedule[]>("/pickup-schedules/shipment-schedules/").then(setShipmentSchedules).catch(console.error);
  }, []);

  const {
    register,
    handleSubmit,
    formState: { errors, isSubmitting },
  } = useForm<TransportRequestFormData>({
    resolver: zodResolver(schema),
    defaultValues: {
      quantity: 1,
      consent: false as any,
    },
  });

  const onSubmit = async (data: TransportRequestFormData) => {
    setLoading(true);
    setError(null);
    const formData = new FormData();
    // Map frontend field names to the API serializer field names.
    const fieldNameMap: Partial<Record<keyof TransportRequestFormData, string>> = {
      service_type_id: "service_type",
      route_option_id: "route_option",
      accepted_item_id: "accepted_item",
      drop_off_location_id: "drop_off_location",
      shipment_schedule_id: "shipment_schedule",
      destination_city_id: "destination_city",
    };
    (Object.keys(data) as Array<keyof TransportRequestFormData>).forEach((key) => {
      const apiKey = fieldNameMap[key] ?? key;
      if (key === "consent") {
        formData.append(apiKey, data[key] ? "true" : "false");
      } else if (data[key] !== undefined && data[key] !== "") {
        formData.append(apiKey, String(data[key]));
      }
    });
    // Append files
    const fileInput = document.querySelector<HTMLInputElement>("#photos-upload");
    if (fileInput && fileInput.files) {
      Array.from(fileInput.files).forEach((file) => {
        formData.append("photos", file);
      });
    }

    try {
      const res = await api.postFormData<any>("/transport-requests/", formData);
      router.push(
        `/demande/confirmation?ref=${res.reference_code}&pickup=${encodeURIComponent(data.pickup_city)}&destination=${encodeURIComponent(
          destinations.find((d) => d.id === data.destination_city_id)?.name || ""
        )}`
      );
    } catch (err) {
      setError(parseApiError(err, t("Erreur lors de la soumission.")));
      window.scrollTo({ top: 0, behavior: "smooth" });
    } finally {
      setLoading(false);
    }
  };

  const submitting = isSubmitting || loading;

  return (
    <>
      <PageHeader
        hero
        icon={<Boxes className="h-8 w-8" />}
        title={t("cta.request")}
        subtitle={t("Remplissez le formulaire et notre équipe vous contacte rapidement pour confirmer les détails et le prix.")}
      />

      <div className="container-page max-w-3xl py-12">
        <form onSubmit={handleSubmit(onSubmit)} className="space-y-6" noValidate>
          {error && (
            <div role="alert" className="rounded-xl border border-red-200 bg-red-50 p-4 text-red-700">
              {error}
            </div>
          )}

          {/* Customer info */}
          <fieldset className="card">
            <legend className="mb-4 flex items-center gap-2 text-lg font-bold text-gray-900">
              <User className="h-5 w-5 text-brand-blue" /> {t("Vos informations")}
            </legend>
            <div className="grid gap-4 sm:grid-cols-2">
              <FormField label={t("Nom complet")} htmlFor="full_name" required error={errors.full_name?.message}>
                <input id="full_name" {...register("full_name")} className={`input ${errors.full_name ? "input-error" : ""}`} />
              </FormField>
              <FormField label={t("Téléphone / WhatsApp")} htmlFor="phone" required error={errors.phone?.message}>
                <input id="phone" {...register("phone")} className={`input ${errors.phone ? "input-error" : ""}`} />
              </FormField>
              <FormField label={t("Email")} htmlFor="email" error={errors.email?.message}>
                <input id="email" type="email" {...register("email")} className={`input ${errors.email ? "input-error" : ""}`} />
              </FormField>
              <FormField label={t("WhatsApp (si différent)")} htmlFor="whatsapp_number">
                <input id="whatsapp_number" {...register("whatsapp_number")} className="input" />
              </FormField>
            </div>
          </fieldset>

          {/* Route selection */}
          <fieldset className="card">
            <legend className="mb-4 flex items-center gap-2 text-lg font-bold text-gray-900">
              <Route className="h-5 w-5 text-brand-blue" /> {t("Route et mode de dépôt")}
            </legend>
            <div className="grid gap-4 sm:grid-cols-2">
              <FormField label={t("Route")} htmlFor="route_option_id">
                <select id="route_option_id" {...register("route_option_id")} className="input">
                  <option value="">{t("Sélectionnez…")}</option>
                  {routes.map((route) => (
                    <option key={route.id} value={route.id}>
                      {route.name}{route.transit_time_display ? ` - ${route.transit_time_display}` : ""}
                    </option>
                  ))}
                </select>
              </FormField>
              <FormField label={t("Lieu de dépôt ou retrait")} htmlFor="drop_off_location_id">
                <select id="drop_off_location_id" {...register("drop_off_location_id")} className="input">
                  <option value="">{t("Sélectionnez…")}</option>
                  {locations.map((location) => (
                    <option key={location.id} value={location.id}>
                      {location.city} - {location.name}
                    </option>
                  ))}
                </select>
              </FormField>
              <FormField label={t("Date / expédition publiée")} htmlFor="shipment_schedule_id" className="sm:col-span-2">
                <select id="shipment_schedule_id" {...register("shipment_schedule_id")} className="input">
                  <option value="">{t("Aucune date sélectionnée")}</option>
                  {shipmentSchedules.map((schedule) => (
                    <option key={schedule.id} value={schedule.id}>
                      {schedule.title || schedule.route?.name || t("Expédition publiée")}
                    </option>
                  ))}
                </select>
              </FormField>
            </div>
          </fieldset>

          {/* Goods info */}
          <fieldset className="card">
            <legend className="mb-4 flex items-center gap-2 text-lg font-bold text-gray-900">
              <Boxes className="h-5 w-5 text-brand-blue" /> {t("Type de marchandise")}
            </legend>
            <div className="grid gap-4 sm:grid-cols-2">
              <FormField label={t("Type de service")} htmlFor="service_type_id" required error={errors.service_type_id?.message}>
                <select id="service_type_id" {...register("service_type_id")} className={`input ${errors.service_type_id ? "input-error" : ""}`}>
                  <option value="">{t("Sélectionnez…")}</option>
                  {services.map((s) => (
                    <option key={s.id} value={s.id}>
                      {s.name}
                    </option>
                  ))}
                </select>
              </FormField>
              <FormField label={t("Catégorie d'article")} htmlFor="accepted_item_id">
                <select id="accepted_item_id" {...register("accepted_item_id")} className="input">
                  <option value="">{t("Sélectionnez…")}</option>
                  {acceptedItems.map((item) => (
                    <option key={item.id} value={item.id}>
                      {item.name}{item.max_weight_kg ? ` - max ${item.max_weight_kg} kg` : ""}
                    </option>
                  ))}
                </select>
              </FormField>
              <FormField label={t("Quantité")} htmlFor="quantity">
                <input id="quantity" type="number" min={1} {...register("quantity")} className="input" />
              </FormField>
              <FormField label={t("Dimensions (approx.)")} htmlFor="dimensions">
                <input id="dimensions" {...register("dimensions")} placeholder={t("ex: 50x30x20 cm")} className="input" />
              </FormField>
              <FormField label={t("Poids estimé (kg)")} htmlFor="item_weight_kg">
                <input id="item_weight_kg" type="number" min="0" step="0.01" {...register("item_weight_kg")} className="input" />
              </FormField>
            </div>
            <FormField label={t("Description supplémentaire")} htmlFor="description" className="mt-4">
              <textarea id="description" rows={3} {...register("description")} className="input" />
            </FormField>
            <div className="mt-4 grid gap-4 sm:grid-cols-2">
              <label className="flex items-start gap-2 rounded-lg border border-gray-100 p-3 text-sm text-gray-600">
                <input type="checkbox" {...register("phones_without_battery_confirmed")} className="mt-1 h-4 w-4 rounded border-gray-300 text-brand-red focus:ring-brand-red" />
                <span>{t("Le téléphone est sans batterie, si applicable.")}</span>
              </label>
              <label className="flex items-start gap-2 rounded-lg border border-gray-100 p-3 text-sm text-gray-600">
                <input type="checkbox" {...register("shopping_assistance_requested")} className="mt-1 h-4 w-4 rounded border-gray-300 text-brand-red focus:ring-brand-red" />
                <span>{t("Je demande une assistance shopping.")}</span>
              </label>
            </div>
            <FormField label={t("Détails shopping, si applicable")} htmlFor="shopping_details" className="mt-4">
              <textarea id="shopping_details" rows={2} {...register("shopping_details")} className="input" />
            </FormField>
          </fieldset>

          {/* Pickup & destination */}
          <fieldset className="card">
            <legend className="mb-4 flex items-center gap-2 text-lg font-bold text-gray-900">
              <MapPin className="h-5 w-5 text-brand-blue" /> {t("Ramassage et livraison")}
            </legend>
            <div className="grid gap-4 sm:grid-cols-2">
              <FormField label={t("Ville de ramassage")} htmlFor="pickup_city" required error={errors.pickup_city?.message}>
                <input id="pickup_city" {...register("pickup_city")} placeholder={t("ex: Frankfurt, Strasbourg…")} className={`input ${errors.pickup_city ? "input-error" : ""}`} />
              </FormField>
              <FormField label={t("Destination")} htmlFor="destination_city_id" required error={errors.destination_city_id?.message}>
                <select id="destination_city_id" {...register("destination_city_id")} className={`input ${errors.destination_city_id ? "input-error" : ""}`}>
                  <option value="">{t("Sélectionnez…")}</option>
                  {destinations.map((d) => (
                    <option key={d.id} value={d.id}>
                      {d.name}
                    </option>
                  ))}
                </select>
              </FormField>
              <FormField label={t("Adresse de ramassage")} htmlFor="pickup_address" required error={errors.pickup_address?.message} className="sm:col-span-2">
                <textarea id="pickup_address" rows={2} {...register("pickup_address")} className={`input ${errors.pickup_address ? "input-error" : ""}`} />
              </FormField>
              <FormField label={t("Date de ramassage souhaitée")} htmlFor="preferred_pickup_date">
                <input id="preferred_pickup_date" type="date" {...register("preferred_pickup_date")} className="input" />
              </FormField>
            </div>
          </fieldset>

          {/* Photos */}
          <fieldset className="card">
            <legend className="mb-4 flex items-center gap-2 text-lg font-bold text-gray-900">
              <ImagePlus className="h-5 w-5 text-brand-blue" /> {t("Photos (optionnel)")}
            </legend>
            <input
              id="photos-upload"
              type="file"
              multiple
              accept="image/*"
              className="w-full text-sm text-gray-500 file:mr-4 file:rounded-full file:border-0 file:bg-brand-gold/10 file:px-4 file:py-2 file:text-sm file:font-semibold file:text-brand-gold hover:file:bg-brand-gold/20"
            />
            <p className="mt-2 text-xs text-gray-400">{t("Vous pouvez joindre plusieurs photos. Formats : JPG, PNG, WEBP.")}</p>
          </fieldset>

          {/* Notes & consent */}
          <fieldset className="card">
            <legend className="mb-4 flex items-center gap-2 text-lg font-bold text-gray-900">
              <NotebookPen className="h-5 w-5 text-brand-blue" /> {t("Remarques")}
            </legend>
            <FormField label={t("Remarques supplémentaires")} htmlFor="customer_notes">
              <textarea id="customer_notes" rows={2} {...register("customer_notes")} className="input" />
            </FormField>
            <div className="mt-4 flex items-start gap-2.5">
              <input id="consent" type="checkbox" {...register("consent")} className="mt-1 h-4 w-4 rounded border-gray-300 text-brand-red focus:ring-brand-red" />
              <label htmlFor="consent" className="text-sm text-gray-600">
                {t("J'accepte d'être contacté par téléphone ou WhatsApp concernant cette demande.")} <span className="text-brand-red">*</span>
              </label>
            </div>
            {errors.consent && <p className="field-error">{errors.consent.message}</p>}
          </fieldset>

          <div className="flex flex-col gap-3 sm:flex-row sm:items-center">
            <button type="submit" disabled={submitting} className="btn-primary flex-1 !py-3.5 text-base">
              {submitting ? <LoadingSpinner className="h-5 w-5" /> : t("Envoyer la demande")}
            </button>
            <WhatsAppCTA className="!py-3.5 sm:w-auto" />
          </div>
          <p className="text-center text-xs text-gray-400">
            {t("Besoin d'aide pour remplir le formulaire ? Contactez-nous directement sur WhatsApp.")}
          </p>
        </form>
      </div>
    </>
  );
}
