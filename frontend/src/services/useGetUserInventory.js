import axios from "axios";
import { useQuery } from "@tanstack/react-query";

const useGetUserInventory = () => {
  const fetchData = async () => {
    const { data } = await axios.get("/api/inventory/", {
      withCredentials: true,
    });
    return data;
  };

  const {
    data: inventoryData,
    isLoading: inventoryDataIsLoading,
    isError: inventoryDataIsError,
  } = useQuery({
    queryFn: fetchData,
    queryKey: ["inventory"]
  });

  return { inventoryData, inventoryDataIsError, inventoryDataIsLoading };
};

export default useGetUserInventory;
