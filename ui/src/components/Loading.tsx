import { Box, Loader, Skeleton } from '@mantine/core'

export const Loading: React.FC = () => {
  return (
    <Box>
      <Skeleton>
        <Box w="100vw" h="100vh"></Box>
      </Skeleton>
      <Box 