import type { Translate } from "@/lib/i18n-config";

export interface FAQItem {
  question: string;
  answer: string;
}

const faqSource: FAQItem[] = [
  {
    question: "Which routes does NCKL support?",
    answer:
      "NCKL supports Germany/Europe to Cameroon and Cameroon to Germany/Europe. The transit wording is configurable because the supplied flyers show different timing claims.",
  },
  {
    question: "Where are the drop-off locations?",
    answer:
      "Confirmed NCKL locations are Bamenda, Douala, Berlin and Leipzig. Opening hours and contact numbers are shown on the calendar/contact pages and can be managed by administrators.",
  },
  {
    question: "Which items are accepted?",
    answer:
      "Confirmed categories include dry and frozen foodstuff, clothes, jewelry, bags, shoes, cosmetics, hair extensions, dry herbs, documents, phones without batteries and small household equipment up to 31 kg.",
  },
  {
    question: "Can NCKL buy products in Europe for delivery to Cameroon?",
    answer:
      "Yes. The supplied materials confirm a WhatsApp-led shopping-from-Europe service for delivery to the customer's doorstep in Cameroon.",
  },
  {
    question: "Are prices available online?",
    answer:
      "No confirmed public prices were supplied. NCKL confirms the final price after checking route, item type, weight, handling needs and destination.",
  },
  {
    question: "Can NCKL pick up from travel agencies in Douala?",
    answer:
      "Yes. The supplied materials confirm package pickup from travel agencies in Douala. Specific agency details should be confirmed by WhatsApp or configured by an administrator.",
  },
  {
    question: "How do I follow a request?",
    answer:
      "Use the tracking page with your NCKL reference number to see the status of your request.",
  },
];

export function getFaqItems(t: Translate): FAQItem[] {
  return faqSource.map((item) => ({ question: t(item.question), answer: t(item.answer) }));
}
