import Cookies from "js-cookie";
import { Currency } from "../types/currency";
import { UserCurrency } from "../types/user";
import axios from "axios";
import { currencyLookup } from "../types/currency";
import { useQuery } from "@tanstack/react-query";

const isValidCurrency = (currency: string): currency is Currency =>
  Object.keys(currencyLookup).includes(currency);

const useGetUserCurrency = () => {
  const csrftoken = Cookies.get("csrftoken");

  return useQuery<UserCurrency & { currency_symbol: string }>({
    queryFn: async () => {
      try {
        // Fetch user currency data from the server
        const response = await axios.get<UserCurrency>("/api/currency/", {
          headers: {
            "X-CSRFToken": csrftoken || "",
          },
          withCredentials: true,
        });

        const currency = response.data.default_currency;

        if (!isValidCurrency(currency)) {
          throw new Error("Invalid currency received from the server.");
        }

        return {
          ...response.data,
          currency_name: currencyLookup[currency].name,
          currency_symbol: currencyLookup[currency].symbol,
        };
      } catch {
        // Fallback to localStorage with a default exchange rate
        const localCurrency = localStorage.getItem("currency") || "USD";

        if (!isValidCurrency(localCurrency)) {
          throw new Error("Invalid currency found in localStorage");
        }

        return {
          currency_name: currencyLookup[localCurrency].name,
          currency_symbol: currencyLookup[localCurrency].symbol,
          default_currency: localCurrency as Currency,
          exchange_rate: 1.0, // Default exchange rate
        };
      }
    },
    queryKey: ["userCurrency"],
    retry: false,
  });
};

export default useGetUserCurrency;