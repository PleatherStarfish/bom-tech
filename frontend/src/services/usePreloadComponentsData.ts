import { QueryClient } from '@tanstack/react-query';
import { getComponentsByIds } from './useGetComponentsByIds';

export const prefetchComponentsData = async (queryClient: QueryClient, componentPks: string[]) => {
  await queryClient.prefetchQuery({
    queryKey: ['getComponentsByIds', componentPks],
    queryFn: () => getComponentsByIds(componentPks),
    staleTime: 60000, // Keep the data fresh for 60 seconds
  });
};