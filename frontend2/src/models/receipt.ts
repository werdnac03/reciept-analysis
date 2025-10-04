export type Receipt = {
  id: string;
  storeName: string;
  totalAmount: number;
  createdAt: string; // ISO datetime
  imageUrl?: string;
  ocrText?: string;
};
