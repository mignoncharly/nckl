export interface ServiceType {
  id: number;
  name: string;
  description: string;
  icon: string;
  active?: boolean;
  sort_order?: number;
}


export interface RouteOption {
  id: number;
  name: string;
  direction: "germany_cameroon" | "cameroon_germany";
  direction_display: string;
  origin_label: string;
  destination_label: string;
  transit_time_display: string;
  shopping_assistance_available: boolean;
  notes: string;
  active?: boolean;
  sort_order?: number;
}

export interface AcceptedItemCategory {
  id: number;
  name: string;
  description: string;
  max_weight_kg: string | null;
  requires_battery_removed: boolean;
  route_restriction: string;
  route_restriction_display: string;
  active?: boolean;
  sort_order?: number;
}

export interface DropOffLocation {
  id: number;
  name: string;
  city: string;
  country: string;
  location_type: string;
  location_type_display: string;
  address: string;
  details: string;
  phone: string;
  whatsapp: string;
  opening_hours: string;
  active?: boolean;
  sort_order?: number;
}

export interface ShipmentSchedule {
  id: number;
  route: RouteOption | null;
  title: string;
  drop_off_location: DropOffLocation | null;
  latest_dropoff_at: string | null;
  departure_date: string | null;
  estimated_arrival_date: string | null;
  notes: string;
  active?: boolean;
  sort_order?: number;
}

export interface PriceRule {
  id: number;
  service_type: number;
  service_name: string;
  label: string;
  price_amount: string;
  currency: string;
  unit: string;
  description?: string;
  active?: boolean;
  valid_from?: string | null;
  valid_until?: string | null;
}

export interface PickupSchedule {
  id: number;
  region?: number;
  region_name: string;
  title?: string;
  cities: string;
  start_date: string;
  end_date: string | null;
  notes: string;
  active?: boolean;
}

export interface LoadingDate {
  id: number;
  date: string;
  title: string;
  description: string;
  active?: boolean;
}

export interface DestinationCity {
  id: number;
  name: string;
  country: string;
}

export interface CustomerNotification {
  id: number;
  title: string;
  body: string;
  reference_code: string;
  read: boolean;
  created_at: string;
}

export interface NotificationPreference {
  language: string;
  regions: string;
  status_updates: boolean;
  pickup_alerts: boolean;
  updated_at: string;
}

export interface DashboardNotificationFailure {
  id: number;
  title: string;
  target_type: string;
  target_region: string;
  sent_count: number;
  failed_count: number;
  created_at: string;
}

export interface DashboardStats {
  total_requests: number;
  new_requests: number;
  confirmed_requests: number;
  by_pickup_city: Array<{ pickup_city: string; count: number }>;
  by_destination_city: Array<{ destination_city__name: string; count: number }>;
  by_status: Array<{ status: string; count: number }>;
  requests_over_time: Array<{ date: string; count: number }>;
  ops: {
    failed_notification_logs_30d: number;
    failed_notifications_30d: number;
    inactive_push_subscriptions: number;
    recent_failed_notifications: DashboardNotificationFailure[];
  };
}
